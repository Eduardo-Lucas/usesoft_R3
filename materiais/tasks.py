from celery import task
from django.core.mail import send_mail
from .models import PedidoWeb


@task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    pedido = PedidoWeb.objects.get(id=order_id)
    subject = 'Pedido nr. {}'.format(pedido.id)
    message = 'Prezado(a) {},\n\nVocê gravou um pedido. O número do pedido é {}.'.format(pedido.first_name,
                                                                                         pedido.id)
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [pedido.email])
    return mail_sent
