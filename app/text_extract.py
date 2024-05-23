from fuzzywuzzy import process, fuzz
from transformers import AutoTokenizer, TFAutoModelForTokenClassification, pipeline
from langdetect import detect, detect_langs
import spacy


def extract(text, certs, use_nlp, umbral=80):
    found_certs = []

    if use_nlp:
        lang = 'en'
        try:
            lang = detect(text)
        except Exception as e:
            print(e)

        nlp = None

        if lang == 'es':
            nlp = spacy.load("es_core_news_sm")
        else:
            nlp = spacy.load("en_core_web_sm")

        # Procesar el texto
        doc = nlp(text)

        found_certs = [ent.text for ent in doc.ents if ent.text in certs]
    else:
        text = text.replace('\n', ' ').replace('\r', '').replace(' ', '')
        # print(text)
        best_cert_score = 0
        best_cert = None
        for cert in certs:
            matches = process.extract(cert.lower().replace(' ', ''), [word.lower() for word in text.split()], limit=1,
                                      scorer=fuzz.partial_ratio)
            for match in matches:
                # print(cert + ' ' + str(match[1]))
                if match[1] >= umbral and match[1] > best_cert_score:  # 75 es un umbral de similitud, puedes ajustarlo según sea necesario
                    best_cert_score = match[1]
                    best_cert = cert

        if best_cert is not None:
            found_certs.append(best_cert)

    print(found_certs)

    return found_certs
