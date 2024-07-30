from django import forms
from .models import DocumentoRecibido, DocumentoEnviado, OtrosRadicados
from datetime import date

def generate_radicado_number(prefix, model):
    current_year = date.today().year
    last_radicado = model.objects.filter(numero_radicado__startswith=f'{prefix}-{current_year}').order_by('id').last()
    if last_radicado:
        last_number = int(last_radicado.numero_radicado.split('-')[-1])
        new_number = last_number + 1
    else:
        new_number = 1
    return f'{prefix}-{current_year}-{str(new_number).zfill(4)}'

class DocumentoRecibidoForm(forms.ModelForm):
    class Meta:
        model = DocumentoRecibido
        exclude = ['numero_radicado']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.numero_radicado:
            instance.numero_radicado = generate_radicado_number('1', DocumentoRecibido)
        if commit:
            instance.save()
        return instance

class DocumentoEnviadoForm(forms.ModelForm):
    class Meta:
        model = DocumentoEnviado
        exclude = ['numero_radicado']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.numero_radicado:
            instance.numero_radicado = generate_radicado_number('2', DocumentoEnviado)
        if commit:
            instance.save()
        return instance

class OtrosRadicadosForm(forms.ModelForm):
    class Meta:
        model = OtrosRadicados
        exclude = ['numero_radicado']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.numero_radicado:
            instance.numero_radicado = generate_radicado_number('3', OtrosRadicados)
        if commit:
            instance.save()
        return instance
