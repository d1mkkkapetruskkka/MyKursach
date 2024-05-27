from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render


from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


@login_required
def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        # Создать заказ
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            price_model=form.cleaned_data['price_model'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )
                        # Создать заказанные товары
                        for cart_item in cart_items:
                            product=cart_item.product
                            name=cart_item.product.name
                            price=cart_item.product.price

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                            )
                            product.save()

                        # Очистить корзину пользователя после создания заказа
                        cart_items.delete()

                        messages.success(request, 'Заказ оформлен!')
                        return redirect('user:profile')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            }

        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Home - Оформление заказа',
        'form': form,
        'orders': True,
    }
    return render(request, 'orders/create_order.html', context=context)




def download_order_receipt(request, order_id):
    order = Order.objects.get(pk=order_id)
    order_items = OrderItem.objects.filter(order=order)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{order_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Регистрация шрифта с поддержкой кириллицы
    pdfmetrics.registerFont(TTFont('FreeSans', 'static/deps/font_text/FreeSans.ttf'))

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CustomHeading', fontName='FreeSans', fontSize=16, leading=20, alignment=1))
    styles.add(ParagraphStyle(name='CustomBodyText', fontName='FreeSans', fontSize=12, leading=14))

    elements.append(Paragraph(f'Чек заказа № {order.id}', styles['CustomHeading']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f'Имя: {order.user.first_name}', styles['CustomBodyText']))
    elements.append(Paragraph(f'Фамилия: {order.user.last_name}', styles['CustomBodyText']))
    elements.append(Spacer(1, 12))

    for item in order_items:
        elements.append(Paragraph(f'Товар: {item.name}', styles['CustomBodyText']))
        elements.append(Paragraph(f'Цена: {item.price}', styles['CustomBodyText']))
        elements.append(Paragraph(f'Время: {item.created_timestamp}', styles['CustomBodyText']))
        elements.append(Spacer(1, 6))

    elements.append(Paragraph(f'Ценовая модель: {order.price_model}', styles['CustomBodyText']))

    doc.build(elements)
    return response