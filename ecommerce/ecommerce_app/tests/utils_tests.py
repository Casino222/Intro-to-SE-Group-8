from django.test import TestCase
from ecommerce_app.utils import retrieveInventory, retrieveCustomerFeedback, addProduct, editProduct, removeProduct
from ecommerce_app.models import Product, Comment

class ProductInventoryTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="Product 1", price=1.99, description="Good product", stock=1)
        Product.objects.create(name="Product 2", price=4.99, description="Ok product", stock=2)
        Product.objects.create(name="Product 3", price=9.99, description="Meh product", stock=3)
        Product.objects.create(name="Product 4", price=19.99, description="Bad product", stock=4)
        Product.objects.create(name="Product 5", price=15, description="Horrible product", stock=5)

    def test_Inventory(self):
        product_id = Product.objects.first().id
        inventory = retrieveInventory(product_id)
        product = Product.objects.get(pk=product_id)
        self.assertEqual(inventory, product.stock)

    def test_ZeroStock(self):
        product = Product.objects.create(name="Zero Stock Product", price=5.99, description="Zero stock item", stock=0)
        inventory = retrieveInventory(product.id)
        self.assertEqual(inventory, 0)

    def test_ExistingProductID(self):
        product = Product.objects.create(name="Test Product", price=9.99, description="Test product", stock=10)
        inventory = retrieveInventory(product.id)
        self.assertEqual(inventory, 10)

    def test_LargeProductStock(self):
        product = Product.objects.create(name="Popular item", price=10, description="this product is very popular", stock=99999999999999999)
        inventory = retrieveInventory(product.id)
        self.assertEqual(inventory, 99999999999999999)

    def test_StockIsNotNegative(self):
        product = Product.objects.create(name="Popular item", price=10, description="this product is very popular", stock=10)
        inventory = retrieveInventory(product.id)
        self.assertGreaterEqual(inventory, 0)

class ProductFeedbackTestCase(TestCase):
    def setUp(self):
        self.product_with_comments = Product.objects.create(name="Product with Comments", price=9.99, description="Test product with comments", stock=10)
        Comment.objects.create(product=self.product_with_comments, author="User1", content="Good product")
        Comment.objects.create(product=self.product_with_comments, author="User2", content="Nice product")

        self.product_without_comments = Product.objects.create(name="Product without Comments", price=19.99, description="Test product without comments", stock=5)

        self.product_with_many_comments = Product.objects.create(name="Product with Many Comments", price=14.99, description="Test product with many comments", stock=20)
        for i in range(10):
            Comment.objects.create(product=self.product_with_many_comments, author=f"User{i}", content=f"Comment {i}")

        self.product_with_no_stock = Product.objects.create(name="Product with No Stock", price=29.99, description="Test product with no stock", stock=0)

    def test_ExistingProductWithFeedback(self):
        feedback = retrieveCustomerFeedback(self.product_with_comments.id)
        self.assertEqual(feedback, ["Good product", "Nice product"])

    def test_ProductWithoutFeedback(self):
        feedback = retrieveCustomerFeedback(self.product_without_comments.id)
        self.assertEqual(feedback, [])

    def test_ProductWithManyComments(self):
        feedback = retrieveCustomerFeedback(self.product_with_many_comments.id)
        self.assertEqual(len(feedback), 10)

    def test_ProductWithNoStock(self):
        feedback = retrieveCustomerFeedback(self.product_with_no_stock.id)
        self.assertEqual(feedback, [])

    def test_commentsQuantity(self):
        feedback =  retrieveCustomerFeedback(self.product_with_comments.id)
        self.assertEqual(len(feedback), 2)

class ProductManagementTestCase(TestCase):
    def test_add_product(self):
        initial_product_count = Product.objects.count()
        new_product = addProduct(name="New Product", description="New Description", price=10.99, stock=20)
        self.assertIsNotNone(new_product.id)
        self.assertEqual(Product.objects.count(), initial_product_count + 1)

    def test_edit_product(self):
        initial_product = Product.objects.create(name="Initial Product", description="Initial Description", price=5.99, stock=10)
        edited_product = editProduct(initial_product.id, name="Edited Product", description="Edited Description", price=7.99, stock=15)
        self.assertEqual(edited_product.name, "Edited Product")
        self.assertEqual(edited_product.description, "Edited Description")
        self.assertEqual(edited_product.price, 7.99)
        self.assertEqual(edited_product.stock, 15)

    def test_remove_product(self):
        product_to_remove = Product.objects.create(name="Product to Remove", description="Description", price=9.99, stock=5)
        initial_product_count = Product.objects.count()
        removeProduct(product_to_remove.id)
        self.assertEqual(Product.objects.count(), initial_product_count - 1)
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(pk=product_to_remove.id)

    def test_edit_nonexistent_product(self):
        with self.assertRaises(Product.DoesNotExist):
            editProduct(999, name="Nonexistent Product", description="Description", price=5.99, stock=10)

    def test_remove_nonexistent_product(self):
        with self.assertRaises(Product.DoesNotExist):
            removeProduct(999)