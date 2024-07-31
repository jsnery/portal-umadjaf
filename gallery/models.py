from django.db import models
from users.models import User
import os
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile


# Upload das imagens para a pasta gallery
def upload_location(instance, filename):
    return f"gallery/{instance.event_date.strftime('%Y-%m-%d')}/{filename}"


# Recebe nome do autor o upload
def get_author_name(self):
    return User.objects.get(id=self.author_id).complete_name  # type: ignore


# Model para a galeria de fotos
class Gallery(models.Model):
    '''
    Model para a galeria de fotos

    Atributos:
    - event_id: ID do evento
    - event_date: Data do evento
    - uploaded_at: Data de upload
    - author_id: ID do autor
    - image: Imagem
    '''

    event_id = models.IntegerField(default=0)
    event_date = models.DateField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    author_id = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to=upload_location,
        default='gallery/default.jpg'
        )

    # Deletar a imagem do disco ao deletar o objeto
    def delete(self, *args, **kwargs):
        if self.image:
            image_path = self.image.path
            if os.path.isfile(image_path):
                os.remove(image_path)
                image_dir = os.path.dirname(image_path)
                if not os.listdir(image_dir):
                    os.rmdir(image_dir)
        super(Gallery, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Abrindo a imagem usando Pillow
        img = Image.open(self.image)
        max_size = 500 * 1024  # 500 KB
        quality = 75

        # Comprimir a imagem
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=quality)
        while output.tell() > max_size and quality > 20:
            quality -= 5
            output.seek(0)
            img.save(output, format='JPEG', quality=quality)

        output.seek(0)

        # Alterar o ImageField para a imagem comprimida
        self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg', output.getbuffer().nbytes, None)
        super(Gallery, self).save(*args, **kwargs)

    def __str__(self):
        return f"({self.id}) Enviado em: {self.uploaded_at.strftime('%d/%m/%Y')}, Por: {get_author_name(self)}"


# Model para marcar a foto
class GalleryMarked(models.Model):
    '''
    Model para gerar o sistema de marcação da foto

    Atributos:
    - gallery: ID da galeria
    - marked_at: Data de marcação
    '''

    gallery = models.OneToOneField(Gallery, on_delete=models.CASCADE)
    marked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.id}) Gallery ID: {self.gallery.id}, Marked At: {self.marked_at.strftime('%d/%m/%Y')}"


# Model para marcar o usuário que marcou a foto
class GalleryMarkedUser(models.Model):
    '''
    Model para marcar o usuário que marcou a foto

    Atributos:
    - gallery_marked: ID da galeria marcada
    - marked_confirm: Confirmação de marcação
    - user_id: ID do usuário
    '''

    gallery_marked = models.ForeignKey(GalleryMarked, related_name='marked_users', on_delete=models.CASCADE)
    marked_confirm = models.BooleanField(default=False)
    user_id = models.IntegerField()

    def __str__(self):
        return f"({self.id}) GalleryMarked ID: {self.gallery_marked.id}, User ID: {self.user_id}"
