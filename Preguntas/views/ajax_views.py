from ..models import Universidad, Curso, Tema, Pregunta, UserProfile
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def load_cursos(request):
    universidad_id = request.GET.get('universidad_id')
    if not universidad_id:
        return JsonResponse([], safe=False)
    
    if request.user.is_superuser:
        cursos = Curso.objects.filter(
            pregunta__universidad_id=universidad_id 
        ).distinct().order_by('nombre')
    else:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            cursos = Curso.objects.filter(
                pregunta__universidad_id=universidad_id, 
                pregunta__usuario=user_profile
            ).distinct().order_by('nombre')
        except UserProfile.DoesNotExist:
            return JsonResponse([], safe=False)
            
    data = [{'id': c.id, 'nombre': c.nombre} for c in cursos]
    return JsonResponse(data, safe=False)

@login_required
def load_temas(request):
    curso_id = request.GET.get('curso_id')
    universidad_id = request.GET.get('universidad_id')

    if not curso_id:
        return JsonResponse([], safe=False)
    
    if request.user.is_superuser:
        qs = Tema.objects.filter(curso_id=curso_id)
        if universidad_id:
            qs = qs.filter(pregunta__universidad_id=universidad_id)
        else:
            qs = qs.filter(pregunta__isnull=False)
            
    else:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            qs = Tema.objects.filter(curso_id=curso_id, pregunta__usuario=user_profile)
            if universidad_id:
                qs = qs.filter(pregunta__universidad_id=universidad_id)
        except UserProfile.DoesNotExist:
            return JsonResponse([], safe=False)

    temas = qs.distinct().order_by('nombre')
    data = [{'id': t.id, 'nombre': t.nombre} for t in temas]
    return JsonResponse(data, safe=False)

# views.py

@login_required
def load_cursos_creacion(request):
    universidad_id = request.GET.get('universidad_id')
    if not universidad_id:
        return JsonResponse([], safe=False)
    
    cursos = Curso.objects.filter(
        universidades__id=universidad_id
    ).distinct().order_by('nombre')
    
    data = [{'id': c.id, 'nombre': c.nombre} for c in cursos]
    return JsonResponse(data, safe=False)

@login_required
def load_temas_creacion(request):
    curso_id = request.GET.get('curso_id')
    if not curso_id:
        return JsonResponse([], safe=False)
    
    temas = Tema.objects.filter(
        curso_id=curso_id
    ).order_by('nombre')
    
    data = [{'id': t.id, 'nombre': t.nombre} for t in temas]
    return JsonResponse(data, safe=False)

@login_required
def load_cursos_practica(request):
    universidad_id = request.GET.get('universidad_id')
    if not universidad_id:
        return JsonResponse([], safe=False)
    
    # Filtra solo los cursos que tengan AL MENOS UNA pregunta en esta universidad
    cursos = Curso.objects.filter(
        pregunta__universidad_id=universidad_id
    ).distinct().order_by('nombre')
    
    data = [{'id': c.id, 'nombre': c.nombre} for c in cursos]
    return JsonResponse(data, safe=False)

@login_required
def load_temas_practica(request):
    curso_id = request.GET.get('curso_id')
    universidad_id = request.GET.get('universidad_id') # ¡Nuevo parámetro!
    
    if not curso_id or not universidad_id:
        return JsonResponse([], safe=False)
    
    # Filtra solo los temas que pertenezcan a este curso Y que 
    # tengan AL MENOS UNA pregunta en esta universidad específica
    temas = Tema.objects.filter(
        curso_id=curso_id,
        pregunta__universidad_id=universidad_id
    ).distinct().order_by('nombre')
    
    data = [{'id': t.id, 'nombre': t.nombre} for t in temas]
    return JsonResponse(data, safe=False)