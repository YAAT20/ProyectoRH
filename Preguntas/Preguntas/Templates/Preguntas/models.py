from django.db import models
from django.core.validators import FileExtensionValidator 
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Universidad(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    universidad = models.ForeignKey(Universidad, on_delete=models.SET_NULL, null=True, related_name='cursos')

    def __str__(self):
        return f"{self.nombre} - {self.universidad.nombre}"

class Tema(models.Model):
    nombre = models.CharField(max_length=200)
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, related_name='temas')

    def __str__(self):
        return f"{self.nombre} - {self.curso.nombre}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)  # Campo para activar/desactivar

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User )
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User )
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save() 

@receiver(post_save, sender=UserProfile)
def update_user_status(sender, instance, **kwargs):
    if instance.user.is_active != instance.is_active:
        User.objects.filter(id=instance.user.id).update(is_active=instance.is_active)

class Pregunta(models.Model):
    universidad = models.ForeignKey(Universidad, on_delete=models.SET_NULL, null=True)
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True)
    tema = models.ForeignKey(Tema, on_delete=models.SET_NULL, null=True)
    nivel = models.IntegerField(default=1)
    nombre = models.CharField(max_length=300, blank=True)
    contenido = models.FileField(upload_to='preguntas/', validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx'])])
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE) 
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.nombre:
            # Generar nombre automático
            count = Pregunta.objects.filter(
                universidad=self.universidad,
                curso=self.curso,
                tema=self.tema,
                nivel=self.nivel
            ).count() + 1
            
            self.nombre = f"{slugify(self.universidad.nombre)}_{slugify(self.curso.nombre)}_{slugify(self.tema.nombre)}_{self.nivel}_{count}"
        
        if not self.id:  
            self.fecha_creacion = timezone.now()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre