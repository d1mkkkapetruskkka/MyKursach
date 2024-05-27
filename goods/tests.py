from django.test import Client, TestCase
from django.urls import reverse

from goods.models import Categories, Products

class CategoriesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Categories.objects.create(name='Test Category', slug='test-category')

    def test_name_label(self):
        category = Categories.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Название')

    def test_slug_label(self):
        category = Categories.objects.get(id=1)
        field_label = category._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'URL')

    def test_object_name_is_name(self):
        category = Categories.objects.get(id=1)
        expected_object_name = category.name
        self.assertEqual(str(category), expected_object_name)

class ProductsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Categories.objects.create(name='Test Category', slug='test-category')
        Products.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test description',
            price=10.99,
            category=category
        )

    def test_name_label(self):
        product = Products.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Название')

    def test_slug_label(self):
        product = Products.objects.get(id=1)
        field_label = product._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'URL')

    def test_description_label(self):
        product = Products.objects.get(id=1)
        field_label = product._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'Описание')

    def test_price_label(self):
        product = Products.objects.get(id=1)
        field_label = product._meta.get_field('price').verbose_name
        self.assertEqual(field_label, 'Цена')

    def test_category_label(self):
        product = Products.objects.get(id=1)
        field_label = product._meta.get_field('category').verbose_name
        self.assertEqual(field_label, 'Категория')

    def test_object_name_is_name(self):
        product = Products.objects.get(id=1)
        expected_object_name = product.name
        self.assertEqual(str(product), expected_object_name)

class CatalogViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/catalog.html')