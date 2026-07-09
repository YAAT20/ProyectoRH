from Preguntas.models import Pregunta
from docx import Document
from django.conf import settings
import os
from docx.oxml.ns import qn


def detectar_clave_resaltada(elements):
    """
    Detecta la alternativa correcta basada en highlight amarillo.
    Soporta formatos: A), A., (A), A:, A , etc.
    """
    for element in elements:
        runs = element.xpath('.//w:r')

        for r in runs:
            rPr = r.find(qn('w:rPr'))

            if rPr is not None:
                highlight = rPr.find(qn('w:highlight'))

                if highlight is not None and highlight.get(qn('w:val')) == 'yellow':
                    texto = "".join(
                        t.text for t in r.xpath('.//w:t') if t.text
                    ).strip().upper()

                    # 🔥 DETECTOR ROBUSTO
                    for letra in ['A', 'B', 'C', 'D', 'E']:
                        if texto.startswith(letra):
                            return letra

    return None


actualizadas = 0
no_detectadas = 0
errores = 0

for p in Pregunta.objects.all():

    if not p.contenido:
        continue

    try:
        ruta = os.path.join(settings.MEDIA_ROOT, p.contenido.name)

        if not os.path.exists(ruta):
            print(f"⚠️ Archivo no existe: {ruta}")
            continue

        doc = Document(ruta)
        elementos = list(doc.element.body)

        clave = detectar_clave_resaltada(elementos)

        if clave:
            if p.respuesta != clave:
                print(f"ID {p.id}: {p.respuesta} → {clave}")
                p.respuesta = clave
                p.save()
                actualizadas += 1
        else:
            print(f"❌ No detectada en ID {p.id}")
            no_detectadas += 1

    except Exception as e:
        print(f"💥 Error en ID {p.id}: {e}")
        errores += 1


print("\n========== RESUMEN ==========")
print(f"Actualizadas: {actualizadas}")
print(f"No detectadas: {no_detectadas}")
print(f"Errores: {errores}")