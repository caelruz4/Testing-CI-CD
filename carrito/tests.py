from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import *

class PlatilloModelTest(TestCase):
    def test_precio_mayor_que_cero(self):
        platillo = Platillo(nombre='Ensalada', descripcion='Ensalada cesar', precio=100)
        platillo.clean()  

        # Intenta crear un Platillo con precio <= 0, debería levantar ValidationError
        with self.assertRaises(ValidationError):
            platillo = Platillo(nombre='Pescado', descripcion='Pescado frito', precio=0)
            platillo.clean()

    def test_str_metodo(self):
        platillo = Platillo(nombre='Ensalada', descripcion='Ensalada cesar', precio=100)
        self.assertEqual(str(platillo), "Ensalada")  # Verifica que el método __str__ devuelva el resultado esperado

class PedidoModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='admin', password='admin123')
        platillo = Platillo.objects.create(nombre='Pasta', descripcion='Pasta con pollo al pesto.', precio=200)

    def test_cantidad_mayor_que_cero(self):
        # Intenta crear un Pedido con cantidad <= 0, debería levantar ValidationError
        with self.assertRaises(ValidationError):
            pedido = Pedido(usuario=User.objects.get(username='admin'), platillo=Platillo.objects.get(nombre='Pasta'), cantidad=0)
            pedido.clean()

    def test_calculo_total_al_guardar_pedido(self):
        pedido = Pedido(usuario=User.objects.get(username='admin'), platillo=Platillo.objects.get(nombre='Pasta'), cantidad=2)
        pedido.save()  # Debería calcular el total correctamente
        self.assertEqual(pedido.total, 400 )  # Verifica que el total sea el esperado

    def test_str_metodo(self):
        pedido = Pedido(usuario=User.objects.get(username='admin'), platillo=Platillo.objects.get(nombre='Pasta'), cantidad=2)
        self.assertEqual(str(pedido), "Orden: Pasta - 2")  # Verifica que el método __str__ devuelva el resultado esperado

    def test_calculo_total_con_otro_platillo(self):
        otro_platillo = Platillo.objects.create(nombre='Ensalada', descripcion='Ensalada cesar', precio=150)
        pedido = Pedido(usuario=User.objects.get(username='admin'), platillo=otro_platillo, cantidad=3)
        pedido.save()
        self.assertEqual(pedido.total, 450)  # Verifica que el total se calcule correctamente con otro platillo

    def test_pedido_con_cantidad_negativa(self):
        with self.assertRaises(ValidationError):
            pedido = Pedido(usuario=User.objects.get(username='admin'), platillo=Platillo.objects.get(nombre='Pasta'), cantidad=-1)
            pedido.clean()  # Debería levantar ValidationError

    def test_pedido_str_metodo_con_cantidad_singular(self):
        pedido = Pedido(usuario=User.objects.get(username='admin'), platillo=Platillo.objects.get(nombre='Pasta'), cantidad=1)
        self.assertEqual(str(pedido), "Orden: Pasta - 1")  # Verifica que el método __str__ maneje correctamente la cantidad singular
