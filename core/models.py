from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError
from PIL import Image
from image_cropping import ImageRatioField

# Create your models here.


class User(AbstractUser):
    is_writer = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_writer == False:
            try:
                profil = UserProfil.objects.get(user=self.id)
            except UserProfil.DoesNotExist:
                #uwazac tu musze instancje podac
                UserProfil.objects.create(user=self)
        else:
            try:
                profil = WriterProfil.objects.get(user=self.id)
            except WriterProfil.DoesNotExist:
                WriterProfil.objects.create(user=self)


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)
    posts = models.ManyToManyField("Post")

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        "WriterProfil", on_delete=models.SET_NULL, null=True, blank=False
    )
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=False
    )
    sneekpeek = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to="images/")
    cropping = ImageRatioField("image", "730x390")
    # auto_add_now - hard to test later with mock data
    created_at = models.DateTimeField(default=timezone.now)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.is_featured == True:
            if Post.objects.filter(is_featured=True).count() >= 5:
                ownInst = Post.objects.get(pk=self.id)
                if ownInst and ownInst.is_featured == True:
                    return
                raise ValidationError("There cannot be more than 5 featured articles")

    def __str__(self):
        return self.title

    def get_tags(self):
        return "\n".join([p.name for p in self.tag_set.all()])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        if self.image:
            pass
            # image = Image.open(self.image)
            # width, height = image.size
            # left = (width - 730)/2
            # top = (height - 390)/2
            # right = (width + 730)/2
            # bottom = (height + 390)/2
            # # resized_image = image.resize((750,400))
            # resized_image = image.crop((left,top,right,bottom))
            # resized_image.save(self.image.path)

    # Overwriting get_tags name display in django admin
    get_tags.short_description = "Tags"


class Like(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    profil = models.ForeignKey("UserProfil", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "profil")


class AbstractProfil(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, blank=False)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Dont generate additional table
    class Meta:
        abstract = True


class WriterProfil(AbstractProfil):
    def __str__(self):
        return self.user.username

    def clean(self):
        if self.user.is_writer == False:
            raise ValidationError("User is a writer")

    def save(self, *args, **kwargs):
        print("save")
        super().save(*args, **kwargs)
        print("saveed")

    class Meta:
        verbose_name_plural = "Writer Profiles"


class UserProfil(AbstractProfil):
    posts = models.ManyToManyField("Post", through="Like")

    def __str__(self):
        return self.user.username

    def clean(self):
        if self.user.is_writer == True:
            raise ValidationError("User cannot be writer")

    class Meta:
        verbose_name_plural = "User Profiles"
