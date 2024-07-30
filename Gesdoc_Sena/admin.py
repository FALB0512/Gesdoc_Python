from django.contrib import admin
from .models import DocumentoEnviado, DocumentoRecibido, OtrosRadicados, Ciudad, Dependencia, TipoDocumento
from .forms import DocumentoRecibidoForm, DocumentoEnviadoForm, OtrosRadicadosForm

class DocumentoEnviadoAdmin(admin.ModelAdmin):
    form = DocumentoEnviadoForm
    list_display = ('numero_radicado', 'fecha_radicacion', 'dependencia', 'nombre_remitente', 'asunto', 'respuesta_radicado', 'nombre_destinatario', 'ciudad', 'tipo_documento', 'ver_pdf')
    search_fields = ('numero_radicado', 'nombre_remitente__username', 'nombre_destinatario', 'asunto')
    list_filter = ('dependencia', 'ciudad', 'tipo_documento')
    date_hierarchy = 'fecha_radicacion'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "respuesta_radicado":
            kwargs["queryset"] = DocumentoRecibido.objects.filter(respuesta_radicado__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(nombre_remitente=request.user)

class DocumentoRecibidoAdmin(admin.ModelAdmin):
    form = DocumentoRecibidoForm
    list_display = ('numero_radicado', 'nombre_entidad_persona', 'asunto', 'radicado_origen', 'fecha_creacion_documento', 'fecha_recibido_documento', 'nombre_destinatario', 'ciudad', 'tipo_documento', 'ver_pdf', 'respuesta_radicado')
    search_fields = ('numero_radicado', 'nombre_entidad_persona', 'nombre_destinatario__username', 'asunto')
    list_filter = ('ciudad', 'tipo_documento')
    date_hierarchy = 'fecha_creacion_documento'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(nombre_destinatario=request.user)

class OtrosRadicadosAdmin(admin.ModelAdmin):
    form = OtrosRadicadosForm
    list_display = ('numero_radicado', 'fecha_recibido', 'nombre_remitente', 'nombre_funcionario_destino', 'radicado_origen', 'tipo_documento', 'ciudad', 'ver_pdf')
    search_fields = ('nombre_remitente', 'nombre_funcionario_destino__username', 'radicado_origen')
    list_filter = ('ciudad', 'tipo_documento')
    date_hierarchy = 'fecha_recibido'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(nombre_funcionario_destino=request.user)

class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


class DependenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


admin.site.register(DocumentoEnviado, DocumentoEnviadoAdmin)
admin.site.register(DocumentoRecibido, DocumentoRecibidoAdmin)
admin.site.register(OtrosRadicados, OtrosRadicadosAdmin)
admin.site.register(Ciudad, CiudadAdmin)
admin.site.register(Dependencia, DependenciaAdmin)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
