import unittest
from app import validate_product 

class TestBusinessLogic(unittest.TestCase):

    def test_valid_product(self):
        """Перевірка успішної валідації"""
        try:
            validate_product("Смартфон", 15000.0)
        except ValueError:
            self.fail("validate_product підняв помилку для валідних даних!")

    def test_short_name(self):
        """Перевірка інваріанту: назва має бути >= 3 символів"""
        with self.assertRaises(ValueError) as context:
            validate_product("А", 100.0)
        self.assertEqual(str(context.exception), "Назва товару має бути довшою за 3 символи")

    def test_negative_price(self):
        """Перевірка інваріанту: ціна не може бути від'ємною"""
        with self.assertRaises(ValueError) as context:
            validate_product("Книга", -50.0)
        self.assertEqual(str(context.exception), "Ціна не може бути від'ємною")

if __name__ == '__main__':
    unittest.main()
