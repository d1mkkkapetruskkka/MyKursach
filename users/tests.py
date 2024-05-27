import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from carts.models import Cart
from orders.models import Order, OrderItem

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser', password='testpass', email='test@example.com'
    )

@pytest.mark.django_db
def test_login_view(client):
    url = reverse('user:login')
    
    # Test GET request
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], UserLoginForm)
    
    # Test POST request with valid data
    data = {'username': 'testuser', 'password': 'testpass'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('user:profile')
    assert '_auth_user_id' in client.session
    
    # Test POST request with invalid data
    data = {'username': 'invaliduser', 'password': 'invalidpass'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], UserLoginForm)

@pytest.mark.django_db
def test_registration_view(client):
    url = reverse('user:registration')
    
    # Test GET request
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], UserRegistrationForm)
    
    # Test POST request with valid data
    data = {
        'username': 'newuser', 'email': 'new@example.com',
        'password1': 'newpassword', 'password2': 'newpassword'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('main:index')
    assert User.objects.filter(username='newuser').exists()
    
    # Test POST request with invalid data
    data = {
        'username': '', 'email': 'invalid',
        'password1': 'newpassword', 'password2': 'wrongpassword'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], UserRegistrationForm)

@pytest.mark.django_db
def test_profile_view(client, user):
    url = reverse('user:profile')
    client.force_login(user)
    
    # Test GET request
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], ProfileForm)
    assert 'orders' in response.context
    
    # Test POST request with valid data
    image = SimpleUploadedFile('test.jpg', b'file_content', content_type='image/jpeg')
    data = {
        'first_name': 'Updated', 'last_name': 'User',
        'email': 'updated@example.com', 'image': image
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('user:profile')
    user.refresh_from_db()
    assert user.first_name == 'Updated'
    assert user.last_name == 'User'
    assert user.email == 'updated@example.com'
    assert user.image

@pytest.mark.django_db
def test_logout_view(client, user):
    url = reverse('user:logout')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('main:index')
    assert '_auth_user_id' not in client.session