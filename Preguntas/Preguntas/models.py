from django.db import models
from django.core.validators import FileExtensionValidator 
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Universidad(models.Model):
    nombre = models.CharField(max_length=200, unique= True)

    def __str__(self):
        return self.nombre

class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    universidad = models.ForeignKey(Universidad, on_delete=models.SET_NULL, null=True, blank=True, related_name='cursos')
    universidad_nombre = models.CharField(max_length=200, blank=True)
    
    class Meta:
        unique_together = ('nombre', 'universidad')

    def save(self, *args, **kwargs):
        if self.universidad:
            self.universidad_nombre = self.universidad.nombre
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.universidad_nombre or 'Sin universidad'}"

class Tema(models.Model):
    nombre = models.CharField(max_length=200)
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, blank=True, related_name='temas')
    curso_nombre = models.CharField(max_length=200, blank=True)
    universidad_nombre = models.CharField(max_length=200, blank=True)
    
    class Meta:
        unique_together = ('nombre', 'curso')

    def save(self, *args, **kwargs):
        if self.curso:
            self.curso_nombre = self.curso.nombre
            self.universidad_nombre = self.curso.universidad_nombre
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.curso_nombre or 'Sin curso'}"

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
    universidad = models.ForeignKey(Universidad, on_delete=models.SET_NULL, null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, blank=True)
    tema = models.ForeignKey(Tema, on_delete=models.SET_NULL, null=True, blank=True)

    universidad_nombre = models.CharField(max_length=200, blank=True)
    curso_nombre = models.CharField(max_length=200, blank=True)
    tema_nombre = models.CharField(max_length=200, blank=True)

    nivel = models.IntegerField(default=1)
    nombre = models.CharField(max_length=300, blank=True)
    contenido = models.FileField(upload_to='preguntas/', validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx'])])
    usuario = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null = True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.universidad:
            self.universidad_nombre = self.universidad.nombre
        if self.curso:
            self.curso_nombre = self.curso.nombre
        if self.tema:
            self.tema_nombre = self.tema.nombre

        if not self.nombre:
            count = Pregunta.objects.filter(
                universidad=self.universidad,
                curso=self.curso,
                tema=self.tema,
                nivel=self.nivel
            ).count() + 1

            self.nombre = f"{slugify(self.universidad_nombre)}_{slugify(self.curso_nombre)}_{slugify(self.tema_nombre)}_{self.nivel}_{count}"

        if not self.id:
            self.fecha_creacion = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
