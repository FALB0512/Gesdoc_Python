from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import DocumentoRecibido

@receiver(post_save, sender=DocumentoRecibido)
def enviar_correo_documento_recibido(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Nuevo Documento Asignado',
            f'A usted se le ha asignado un nuevo documento con número de radicado: {instance.numero_radicado}.',
            'farudlopez36@gmail.com', 
            [instance.correo_funcionario_destinatario],
            fail_silently=False,
        )
