from django.db import models
import os


def upload_location(instance, filename):
    return f"gallery/{instance.event_date.strftime('%Y-%m-%d')}/{filename}"


# Create your models here.
class Gallery(models.Model):
    event_id = models.IntegerField(default=0)
    event_date = models.DateField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    author_id = models.IntegerField(default=0)
    image = models.ImageField(upload_to=upload_location, default='gallery/default.jpg')

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


class GalleryMarked(models.Model):
    gallery = models.OneToOneField(Gallery, on_delete=models.CASCADE)
    marked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.id}) Gallery ID: {self.gallery.id}, Marked At: {self.marked_at.strftime('%d/%m/%Y')}"


class GalleryMarkedUser(models.Model):
    gallery_marked = models.ForeignKey(GalleryMarked, related_name='marked_users', on_delete=models.CASCADE)
    print('gallery_marked:', gallery_marked)
    marked_confirm = models.BooleanField(default=False)
    user_id = models.IntegerField()

    def __str__(self):
        return f"({self.id}) GalleryMarked ID: {self.gallery_marked.id}, User ID: {self.user_id}"
