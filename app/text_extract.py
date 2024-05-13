from transformers import TFAutoModelForTokenClassification, AutoTokenizer, pipeline


def extract(text):
    tokenizer = AutoTokenizer.from_pretrained("mrm8488/bert-spanish-cased-finetuned-ner")
    model = TFAutoModelForTokenClassification.from_pretrained("mrm8488/bert-spanish-cased-finetuned-ner", from_pt=True)
    # Crear un pipeline de NER usando el modelo y el tokenizador cargados
    nlp = pipeline("ner", model=model, tokenizer=tokenizer)

    # Aplicar el pipeline al texto
    results = nlp(text)

    certificates = []
    current_cert = ""

    for entity in results:
        if entity['entity'] == 'B-MISC':  # Comienzo de un nuevo certificado
            if current_cert:  # Guardar el certificado anterior si existe
                certificates.append(current_cert)
            current_cert = entity['word'].replace("##", "")  # Iniciar nuevo certificado
        elif entity['entity'] == 'I-MISC':  # Continuación del certificado actual
            current_cert += entity['word'].replace("##", "")

    if current_cert:  # Asegurar que el último certificado se añada
        certificates.append(current_cert)

    return certificates
