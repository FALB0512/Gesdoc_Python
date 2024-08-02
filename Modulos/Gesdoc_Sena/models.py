from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
import logging
from datetime import date

logger = logging.getLogger(__name__)

class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Ciudades'

class Dependencia(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


def generate_radicado_number(prefix, model):
    current_year = date.today().year
    last_radicado = model.objects.filter(numero_radicado__startswith=f'{prefix}-{current_year}').order_by('id').last()
    if last_radicado:
        last_number = int(last_radicado.numero_radicado.split('-')[-1])
        new_number = last_number + 1
    else:
        new_number = 1
    return f'{prefix}-{current_year}-{str(new_number).zfill(4)}'


class DocumentoRecibido(models.Model):
    id = models.AutoField(primary_key=True)
    numero_radicado = models.CharField(max_length=20, unique=True, blank=True)
    fecha_recibido_documento = models.DateField(auto_now_add=True)
    nombre_entidad_persona = models.CharField(max_length=255)
    asunto = models.CharField(max_length=100)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.SET_NULL, null=True)
    radicado_origen = models.CharField(max_length=20)
    contenido = models.TextField()
    fecha_creacion_documento = models.DateField()
    anexos = models.IntegerField()
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.SET_NULL, null=True)
    nombre_destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documentos_recibidos_asignados')
    archivo_pdf = models.FileField(upload_to='pdfs/')
    correo_funcionario_destinatario = models.EmailField()
    observaciones = models.TextField(blank=True, null=True)
    respuesta_radicado = models.ForeignKey('DocumentoEnviado', on_delete=models.SET_NULL, null=True, blank=True, related_name='respuestas_recibidas')

    def save(self, *args, **kwargs):
        if not self.numero_radicado:
            self.numero_radicado = generate_radicado_number('1', DocumentoRecibido)
        super().save(*args, **kwargs)

    def ver_pdf(self):
        if self.archivo_pdf:
            return format_html('<a href="{}" target="_blank">Ver PDF</a>', self.archivo_pdf.url)
        return "No hay PDF"

    ver_pdf.short_description = 'Archivo PDF'

    def __str__(self):
        return self.numero_radicado


class DocumentoEnviado(models.Model):
    id = models.AutoField(primary_key=True)
    numero_radicado = models.CharField(max_length=20, unique=True, blank=True)
    fecha_radicacion = models.DateField(auto_now_add=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.SET_NULL, null=True)
    nombre_remitente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documentos_enviados')
    asunto = models.CharField(max_length=100)
    anexos = models.IntegerField()
    respuesta_radicado = models.ForeignKey(DocumentoRecibido, on_delete=models.SET_NULL, null=True, blank=True, related_name='respuestas_enviadas')
    nombre_destinatario = models.CharField(max_length=255)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.SET_NULL, null=True)
    observaciones = models.TextField(blank=True, null=True)
    archivo_pdf = models.FileField(upload_to='pdfs/')

    def save(self, *args, **kwargs):
        if not self.numero_radicado:
            self.numero_radicado = generate_radicado_number('2', DocumentoEnviado)
        super().save(*args, **kwargs)
        if self.respuesta_radicado:
            documento_recibido = self.respuesta_radicado
            documento_recibido.respuesta_radicado = self
            documento_recibido.save()

    def ver_pdf(self):
        if self.archivo_pdf:
            return format_html('<a href="{}" target="_blank">Ver PDF</a>', self.archivo_pdf.url)
        return "No hay PDF"

    ver_pdf.short_description = 'Archivo PDF'

    def __str__(self):
        return f'{self.numero_radicado} - {self.nombre_destinatario}'


class OtrosRadicados(models.Model):
    id = models.AutoField(primary_key=True)
    numero_radicado = models.CharField(max_length=20, unique=True, blank=True)
    fecha_recibido = models.DateField(auto_now_add=True)
    nombre_remitente = models.CharField(max_length=255)
    nombre_funcionario_destino = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otros_radicados')
    radicado_origen = models.CharField(max_length=20)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.SET_NULL, null=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True)
    anexos = models.IntegerField()
    dependencia = models.ForeignKey(Dependencia, on_delete=models.SET_NULL, null=True)
    archivo_pdf = models.FileField(upload_to='pdfs/')

    def save(self, *args, **kwargs):
        if not self.numero_radicado:
            self.numero_radicado = generate_radicado_number('3', OtrosRadicados)
        super().save(*args, **kwargs)

    def ver_pdf(self):
        if self.archivo_pdf:
            return format_html('<a href="{}" target="_blank">Ver PDF</a>', self.archivo_pdf.url)
        return "No hay PDF"

    ver_pdf.short_description = 'Archivo PDF'

    def __str__(self):
        return self.radicado_origen

    class Meta:
        verbose_name = 'Otro radicado'
        verbose_name_plural = 'Otros radicados'
        #hacer commit
