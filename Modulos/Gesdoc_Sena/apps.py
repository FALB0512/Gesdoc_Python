from django.apps import AppConfig

class GesdocSenaConfig(AppConfig):
    name = 'Modulos.Gesdoc_Sena'

    def ready(self):
        import Modulos.Gesdoc_Sena.signals
