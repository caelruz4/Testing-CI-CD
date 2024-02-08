# test_calculadora.py
import unittest
from suma import sumar

class TestCalculadora(unittest.TestCase):

    def test_sumar_numeros_positivos(self):
        resultado = sumar(2, 3)
        self.assertEqual(resultado, 5)

    def test_sumar_numeros_negativos(self):
        resultado = sumar(-2, -3)
        self.assertEqual(resultado, -5)

    def test_sumar_positivo_y_negativo(self):
        resultado = sumar(2, -3)
        self.assertEqual(resultado, -1)

if __name__ == '__main__':
    unittest.main()
