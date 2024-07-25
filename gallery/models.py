from django.db import models
import os


# Upload das imagens para a pasta gallery
def upload_location(instance, filename):
    return f"gallery/{instance.event_date.strftime('%Y-%m-%d')}/{filename}"


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
    image = models.ImageField(upload_to=upload_location, default='gallery/default.jpg')

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

    def __str__(self):
        return f"({self.id}) ({self.event_date.strftime('%d/%m/%Y')})"


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
