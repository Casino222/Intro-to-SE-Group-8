from django.test import TestCase
from ecommerce_app.models import Inventory
from ecommerce_app.search import search_products
from decimal import Decimal  

class SearchProductsTestCase(TestCase):
    def setUp(self):
        Inventory.objects.create(name="FIFA 22", price=Decimal('59.99'), seller="EA Sports", category="Sports")
        Inventory.objects.create(name="The Legend of Zelda: Breath of the Wild", price=Decimal('49.99'), seller="Nintendo", category="Adventure")
        Inventory.objects.create(name="Call of Duty: Warzone", price=Decimal('0.00'), seller="Activision", category="Shooter")
        Inventory.objects.create(name="Minecraft", price=Decimal('29.99'), seller="Mojang Studios", category="Sandbox")
        Inventory.objects.create(name="Super Mario Odyssey", price=Decimal('59.99'), seller="Nintendo", category="Platformer")

    def test_search_by_keyword(self):
        search_results = search_products("FIFA 22")
        expected_results = [{'name': 'FIFA 22', 'price': Decimal('59.99'), 'seller': 'EA Sports', 'category': 'Sports'}]
        self.assertEqual(search_results, expected_results)

    def test_search_by_category(self):
        search_results = search_products(query="", category="Adventure")
        expected_results = [
            {'name': 'The Legend of Zelda: Breath of the Wild', 'price': Decimal('49.99'), 'seller': 'Nintendo', 'category': 'Adventure'}
        ]
        self.assertEqual(search_results, expected_results)

    def test_search_with_filters(self):
        search_results = search_products(query="", filters={"price": Decimal('59.99')})
        expected_results = [
            {'name': 'FIFA 22', 'price': Decimal('59.99'), 'seller': 'EA Sports', 'category': 'Sports'},
            {'name': 'Super Mario Odyssey', 'price': Decimal('59.99'), 'seller': 'Nintendo', 'category': 'Platformer'}
        ]
        self.assertEqual(search_results, expected_results)

    def test_search_by_category_and_filters(self):
        search_results = search_products(query="", category="Platformer", filters={"price": Decimal('59.99')})
        expected_results = [
            {'name': 'Super Mario Odyssey', 'price': Decimal('59.99'), 'seller': 'Nintendo', 'category': 'Platformer'}
        ]
        self.assertEqual(search_results, expected_results)

    def test_search_with_no_query(self):
        search_results = search_products(query="")
        expected_results = [
            {'name': 'FIFA 22', 'price': Decimal('59.99'), 'seller': 'EA Sports', 'category': 'Sports'},
            {'name': 'The Legend of Zelda: Breath of the Wild', 'price': Decimal('49.99'), 'seller': 'Nintendo', 'category': 'Adventure'},
            {'name': 'Call of Duty: Warzone', 'price': Decimal('0.00'), 'seller': 'Activision', 'category': 'Shooter'},
            {'name': 'Minecraft', 'price': Decimal('29.99'), 'seller': 'Mojang Studios', 'category': 'Sandbox'},
            {'name': 'Super Mario Odyssey', 'price': Decimal('59.99'), 'seller': 'Nintendo', 'category': 'Platformer'}
        ]
        self.assertEqual(search_results, expected_results)
