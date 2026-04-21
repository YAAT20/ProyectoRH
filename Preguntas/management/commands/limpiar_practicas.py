import os
import time
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Limpia archivos .docx de prácticas generadas con más de 24 horas de antigüedad'

    def handle(self, *args, **options):
        # Ruta de la carpeta de prácticas
        carpeta_practicas = os.path.join(settings.MEDIA_ROOT, 'practicas')
        
        if not os.path.exists(carpeta_practicas):
            self.stdout.write(self.style.WARNING(f'La carpeta {carpeta_practicas} no existe.'))
            return

        ahora = time.time()
        # 86400 segundos = 24 horas
        segundos_limite = 24 * 60 * 60 
        contador = 0

        for archivo in os.listdir(carpeta_practicas):
            ruta_completa = os.path.join(carpeta_practicas, archivo)
            
            # Solo archivos .docx
            if archivo.endswith('.docx'):
                # Verificar tiempo de última modificación
                if os.stat(ruta_completa).st_mtime < ahora - segundos_limite:
                    try:
                        os.remove(ruta_completa)
                        contador += 1
                        self.stdout.write(f'Eliminado: {archivo}')
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'No se pudo eliminar {archivo}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Limpieza completada. Se eliminaron {contador} archivos.'))