from django.test import Client, TestCase
from django.urls import reverse

from goods.models import Products
from orders.models import Order, OrderItem
from users.models import User
from carts.models import Cart

class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='testpass')
        product = Products.objects.create(name='Test Product', price=10.99)
        Cart.objects.create(user=user, product=product)
        Order.objects.create(user=user, phone_number='1234567890', price_model='CPC', payment_on_get='card')

    def test_order_display(self):
        order = Order.objects.get(id=1)
        self.assertEqual(order.user_display(), 'testuser')

    def test_order_items_display(self):
        order = Order.objects.get(id=1)
        self.assertEqual(order.order_items_display(), 'Test Product')

    def test_total_price(self):
        orders = Order.objects.all()
        self.assertEqual(orders.total_price(), 10.99)

class OrderViewTest(TestCase):
    def test_create_order_view_redirects_to_profile(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(user)
        response = self.client.post(reverse('create_order'), {'phone_number': '1234567890', 'price_model': 'CPC', 'payment_on_get': 'card'})
        self.assertRedirects(response, reverse('user:profile'))

    def test_create_order_view_creates_new_order(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(user)
        response = self.client.post(reverse('create_order'), {'phone_number': '1234567890', 'price_model': 'CPC', 'payment_on_get': 'card'})
        self.assertEqual(Order.objects.count(), 1)

    def test_download_order_receipt_view_redirects_to_home(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(user)
        order = Order.objects.create(user=user, phone_number='1234567890', price_model='CPC', payment_on_get='card')
        response = self.client.get(reverse('download_order_receipt', kwargs={'order_id': order.id}))
        self.assertRedirects(response, reverse('home'))

    def test_download_order_receipt_view_downloads_receipt(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(user)
        order = Order.objects.create(user=user, phone_number='1234567890', price_model='CPC', payment_on_get='card')
        response = self.client.get(reverse('download_order_receipt', kwargs={'order_id': order.id}))
        self.assertEqual(response.status_code, 200)