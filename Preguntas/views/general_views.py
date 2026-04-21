from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..views.practicas import Practica
# Página principal
@login_required
def home(request):
    ultima_practica = None
    
    # Verificamos si el usuario tiene perfil antes de consultar
    if hasattr(request.user, 'userprofile'):
        ultima_practica = Practica.objects.filter(
            usuario=request.user.userprofile,
            finalizado=True
        ).order_by('-id').first()

    return render(request, 'Preguntas/home.html', {
        'ultima_practica': ultima_practica
    })
