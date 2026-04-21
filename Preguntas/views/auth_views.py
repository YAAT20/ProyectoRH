from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import UserProfile
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from ..forms import CustomUserCreationForm, ExcelImportForm
from functools import wraps
from django.db import transaction
import pandas as pd
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

@user_passes_test(lambda u: u.is_superuser)
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            password = form.cleaned_data.get('password1')
            messages.success(
                request,
                f"✅ Usuario '{user.username}' creado exitosamente. Contraseña: {password}"
            )
            return redirect('register') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, username):
    if request.method == 'POST':
        user = get_object_or_404(User, username=username)
        if user != request.user:  # Evitar que se elimine a sí mismo
            user.delete()
            messages.success(request, f"Usuario '{username}' eliminado correctamente.")
        else:
            messages.error(request, "No puedes eliminar tu propio usuario.")
    return redirect('admin-dashboard')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                user_profile = user.userprofile
            except UserProfile.DoesNotExist:
                user_profile = UserProfile.objects.create(user=user)

            if user_profile.is_active:
                login(request, user)
                next_url = request.GET.get('next', 'pregunta-list')
                return redirect(next_url)
            else:
                messages.error(request, 'Tu cuenta está suspendida. Comunícate con el administrador.')
                logout(request)
                return redirect('login')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'registration/login.html')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active')
    list_filter = ('is_active',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')

admin.site.register(UserProfile, UserProfileAdmin)

def exclude_supervisor(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'supervisor':
            return HttpResponseForbidden("No tienes permiso para acceder aquí")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def user_logout(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')

def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            # Verificar si el usuario tiene el perfil y el rol adecuado
            if hasattr(request.user, 'userprofile') and request.user.userprofile.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            # Si no tiene permiso, lanzamos un error 403 Forbidden
            raise PermissionDenied("No tienes permisos para ver esta página.")
        return _wrapped_view
    return decorator

@user_passes_test(lambda u: u.is_superuser)
def importar_alumnos_view(request):
    if request.method == "POST":
        archivo = request.FILES.get('archivo_excel')
        if not archivo:
            messages.error(request, "Por favor, selecciona un archivo.")
            return redirect('importar_alumnos')

        try:
            # Leer Excel (Pandas detectará las columnas automáticamente)
            df = pd.read_excel(archivo)
            
            # Limpiar nombres de columnas (quitar espacios y poner en minúsculas)
            df.columns = [str(c).lower().strip() for c in df.columns]
            
            creados = 0
            existentes = 0

            with transaction.atomic():
                for _, row in df.iterrows():
                    # Mapeo según tu tabla:
                    # nombre -> nombre completo
                    # usuario -> código (será el username)
                    # contraseña -> DNI (será el password)
                    nombre_completo = str(row['nombre']).strip()
                    codigo_user = str(row['usuario']).strip()
                    dni_pass = str(row['contraseña']).strip()

                    # 1. Crear Usuario Base
                    user, created = User.objects.get_or_create(
                        username=codigo_user,
                        defaults={
                            'first_name': nombre_completo[:150],
                            'is_active': True
                        }
                    )

                    if created:
                        # 2. Asignar DNI como contraseña
                        user.set_password(dni_pass)
                        user.save()
                        
                        # 3. Forzar rol de Estudiante en el Perfil
                        # Tu signal ya creó el UserProfile, aquí lo configuramos
                        perfil = user.userprofile
                        perfil.role = 'estudiante'
                        perfil.is_active = True
                        perfil.save()
                        
                        creados += 1
                    else:
                        existentes += 1

            messages.success(request, f"Importación finalizada. {creados} nuevos alumnos creados. {existentes} ya existían.")
            return redirect('admin-dashboard') # O la ruta que prefieras

        except Exception as e:
            messages.error(request, f"Error al procesar el Excel: {str(e)}")
            return redirect('importar_alumnos')

    return render(request, "registration/importar_alumnos.html")