from django.contrib import admin
from .models import *

admin.site.register(Universidad)
admin.site.register(Curso)
admin.site.register(Tema)
admin.site.register (Pregunta)
admin.site.register(Practica)
admin.site.register(PracticaPregunta)