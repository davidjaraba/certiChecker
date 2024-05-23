import unittest

from openpyxl.reader.excel import load_workbook

from app.data_process import basic_process

url = 'https://raw.githubusercontent.com'
origin_url = 'www.acciona.com'


class TestBasicProcess(unittest.TestCase):
    def setUp(self):
        certs = []
        wb = load_workbook('Glosario_Certificaciones.xlsx')
        sheet = wb.active
        # Leer todas las filas de la columna B y convertirlas en un array de certificados
        for row in sheet.iter_rows(min_row=2, min_col=2, max_col=2, values_only=True):
            cell_value = row[0]
            if cell_value is not None:
                certs.append(cell_value)

        self.current_certs = certs

    def test_basic_process_txt(self):

        res_certs = ['ISO 9001', 'ISO 14001', ]
        data_type = 'txt'
        txt_for_test = 'site_text.txt'

        # Llamar a la función a probar
        try:
            needed_certs = basic_process(txt_for_test, data_type, url, origin_url, self.current_certs)
        except Exception as e:
            print(e)

        # Comparar el resultado con lo esperado
        self.assertEqual(res_certs, needed_certs)

    def test_basic_process_img_1(self):
        res_certs = ['ISO 9001']
        data_type = 'img'
        img_for_test = 'iso9001.jpg'

        # Llamar a la función a probar
        try:
            needed_certs = basic_process(img_for_test, data_type, url, origin_url, self.current_certs)
        except Exception as e:
            print(e)

        # Comparar el resultado con lo esperado
        self.assertEqual(res_certs, needed_certs)

    def test_basic_process_img_2(self):
        res_certs = ['Sustainalytics']
        data_type = 'img'
        img_for_test = 'sustainalytics.png'

        # Llamar a la función a probar
        try:
            needed_certs = basic_process(img_for_test, data_type, url, origin_url, self.current_certs)
        except Exception as e:
            print(e)

        # Comparar el resultado con lo esperado
        self.assertEqual(res_certs, needed_certs)

    def test_basic_process_img_3(self):
        res_certs = ['UN GLOBAL COMPACT']
        data_type = 'img'
        img_for_test = 'globalcompact.jpg'

        # Llamar a la función a probar
        try:
            needed_certs = basic_process(img_for_test, data_type, url, origin_url, self.current_certs)
        except Exception as e:
            print(e)

        # Comparar el resultado con lo esperado
        self.assertEqual(res_certs, needed_certs)

    def test_basic_process_img_4(self):
        res_certs = ['Euronext']
        data_type = 'img'
        img_for_test = 'euronext.jpg'

        # Llamar a la función a probar
        try:
            needed_certs = basic_process(img_for_test, data_type, url, origin_url, self.current_certs)
        except Exception as e:
            print(e)

        # Comparar el resultado con lo esperado
        self.assertEqual(res_certs, needed_certs)

    def test_basic_process_img_5(self):
        res_certs = ['Dow Jones Sustainability Index']
        data_type = 'img'
        img_for_test = 'dowjones.jpg'

        # Llamar a la función a probar
        try:
            needed_certs = basic_process(img_for_test, data_type, url, origin_url, self.current_certs)
        except Exception as e:
            print(e)

        # Comparar el resultado con lo esperado
        self.assertEqual(res_certs, needed_certs)

    def test_basic_process_img_6(self):
        res_certs = ['Gaïa Rating']
        data_type = 'img'
        img_for_test = 'gaia.jpg'

        # Llamar a la función a probar
        try:
            needed_certs = basic_process(img_for_test, data_type, url, origin_url, self.current_certs)
        except Exception as e:
            print(e)

        # Comparar el resultado con lo esperado
        self.assertEqual(res_certs, needed_certs)

    def test_basic_process_img_7(self):
        res_certs = ['Ecoact']
        data_type = 'img'
        img_for_test = 'ecoact.jpg'

        # Llamar a la función a probar
        try:
            needed_certs = basic_process(img_for_test, data_type, url, origin_url, self.current_certs)
        except Exception as e:
            print(e)

        # Comparar el resultado con lo esperado
        self.assertEqual(res_certs, needed_certs)

    def test_basic_process_img_8(self):
        res_certs = ['S&P Global']
        data_type = 'img'
        img_for_test = 'sp.jpg'

        # Llamar a la función a probar
        try:
            needed_certs = basic_process(img_for_test, data_type, url, origin_url, self.current_certs)
        except Exception as e:
            print(e)

        # Comparar el resultado con lo esperado
        self.assertEqual(res_certs, needed_certs)

    def test_basic_process_img_9(self):
        res_certs = ['Seal Awards']
        data_type = 'img'
        img_for_test = 'seal.jpg'

        # Llamar a la función a probar
        try:
            needed_certs = basic_process(img_for_test, data_type, url, origin_url, self.current_certs)
        except Exception as e:
            print(e)

        # Comparar el resultado con lo esperado
        self.assertEqual(res_certs, needed_certs)

    def test_basic_process_img_10(self):
        res_certs = []
        data_type = 'img'
        img_for_test = 'dolar.jpg'

        # Llamar a la función a probar
        try:
            needed_certs = basic_process(img_for_test, data_type, url, origin_url, self.current_certs)
        except Exception as e:
            print(e)

        # Comparar el resultado con lo esperado
        self.assertEqual(res_certs, needed_certs)

    def test_basic_process_img_11(self):
        res_certs = []
        data_type = 'img'
        img_for_test = 'dolar.jpg'

        # Llamar a la función a probar
        try:
            needed_certs = basic_process(img_for_test, data_type, url, origin_url, self.current_certs)
        except Exception as e:
            print(e)

        # Comparar el resultado con lo esperado
        self.assertEqual(res_certs, needed_certs)

    def test_basic_process_img_12(self):
        res_certs = []
        data_type = 'img'
        img_for_test = 'troncos.jpg'

        # Llamar a la función a probar
        try:
            needed_certs = basic_process(img_for_test, data_type, url, origin_url, self.current_certs)
        except Exception as e:
            print(e)

        # Comparar el resultado con lo esperado
        self.assertEqual(res_certs, needed_certs)

    def test_basic_process_img_13(self):
        res_certs = []
        data_type = 'img'
        img_for_test = 'mar.jpg'

        # Llamar a la función a probar
        try:
            needed_certs = basic_process(img_for_test, data_type, url, origin_url, self.current_certs)
        except Exception as e:
            print(e)

        # Comparar el resultado con lo esperado
        self.assertEqual(res_certs, needed_certs)

    def test_basic_process_img_14(self):
        res_certs = []
        data_type = 'img'
        img_for_test = 'hielo.jpg'

        # Llamar a la función a probar
        try:
            needed_certs = basic_process(img_for_test, data_type, url, origin_url, self.current_certs)
        except Exception as e:
            print(e)

        # Comparar el resultado con lo esperado
        self.assertEqual(res_certs, needed_certs)

    def test_basic_process_img_15(self):
        res_certs = []
        data_type = 'img'
        img_for_test = 'tren.jpg'

        # Llamar a la función a probar
        try:
            needed_certs = basic_process(img_for_test, data_type, url, origin_url, self.current_certs)
        except Exception as e:
            print(e)

        # Comparar el resultado con lo esperado
        self.assertEqual(res_certs, needed_certs)

    def test_basic_process_img_16(self):
        res_certs = []
        data_type = 'img'
        img_for_test = 'cueva.jpg'

        # Llamar a la función a probar
        try:
            needed_certs = basic_process(img_for_test, data_type, url, origin_url, self.current_certs)
        except Exception as e:
            print(e)

        # Comparar el resultado con lo esperado
        self.assertEqual(res_certs, needed_certs)

if __name__ == '__main__':
    unittest.main()
