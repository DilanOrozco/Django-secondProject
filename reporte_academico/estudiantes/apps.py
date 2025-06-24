from django.apps import AppConfig
from django.contrib import admin

class EstudiantesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'estudiantes'
    
    def ready(self):
        admin.site.site_header = 'Panel de Administración'
        admin.site.site_title = 'Bienvenido al panel de Administración '
        admin.site.index_title = 'panel de administración'

