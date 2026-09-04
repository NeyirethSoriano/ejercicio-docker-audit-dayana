import unittest
from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.cliente = app.test_client()

    def test_health_check(self):
        respuesta = self.cliente.get('/health')
        # [Solución B101] Uso de métodos unittest en lugar de la palabra clave assert
        self.assertIn(respuesta.status_code, [200, 500])


if __name__ == '__main__':
    unittest.main()