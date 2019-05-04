from django.contrib import admin
from core.models import Post, Category, Tag, UserProfil, WriterProfil, Like, User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from image_cropping import ImageCroppingMixin

# Register your models here.


class Writer(get_user_model()):
    def clean(self):
        print("koza")

    class Meta:
        proxy = True


class Reader(get_user_model()):
    class Meta:
        proxy = True


# Inlines
class PostTagsInline(admin.TabularInline):
    model = Post.tag_set.through
    extra = 0
    classes = ("collapse",)  # show all collapse
    verbose_name = "Tag"
    verbose_name_plural = "Assigned Tags"


class LikesInline(admin.TabularInline):
    model = Like
    extra = 0


class WriterProfileInline(admin.TabularInline):
    model = WriterProfil
    min_num = 1
    max_num = 1
    extra = 1

    
    def save_model(self, request, obj, form, change):
        print("ole")
        saved = super().save_model(request, obj, form, change)
        return saved


class ReaderProfileInlineForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    

    def save_model(self, request, obj, form, change):
        print("ole")
        saved = super().save_model(request, obj, form, change)
        return saved


class CustomInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        if not self.forms or not len(self.forms) == 1:
            raise ValidationError("One Form is required")


class ReaderProfileInline(admin.TabularInline):
    model = UserProfil
    form = ReaderProfileInlineForm
    formset = CustomInlineFormset
    max_num = 1
    extra = 1


# class PersonForm(forms.ModelForm):

#     class Meta:
#         model = Person



@admin.register(Post)
class PostAdmin(ImageCroppingMixin, admin.ModelAdmin):
    inlines = [PostTagsInline]
    list_filter = ["is_featured", "category", "tag", "author"]
    # list_editable = ['is_featured',]
    list_display = ["title", "category", "is_featured", "created_at", "get_tags"]
    search_fields = ["title"]
    date_hierarchy = "created_at"
    def save_model(self, request, obj, form, change):
        print('ole')
        super().save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [PostTagsInline]
    fields = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass


@admin.register(Writer)
class WriterUserAdmin(admin.ModelAdmin):
    # inlines = [WriterProfileInline]

    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super().add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = [WriterProfileInline]
        return super().change_view(*args, **kwargs)

    def save_model(self, request, obj, form, change):
        print('ole')
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_writer=True)
    
    # def save_formset(self, request, form, formset, change):
    #     print('olw')
    #     saved_formset = formset.save(commit=False)
    #     print('olw')
    #     saved_formset.save()


class ReaderUserForm(forms.ModelForm):
    def clean_is_writer(self):
        data = self.cleaned_data["is_writer"]
        if data is True:
            raise ValidationError("Reader cannot be writer.")
        return data

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    # def save_model(self, request, obj, form, change):
    #     try:
    #         return super().save_model(request, obj, form, change)
    #     except:
    #         print("error")


@admin.register(Reader)
class ReaderUserAdmin(admin.ModelAdmin):
    inlines = [ReaderProfileInline]
    form = ReaderUserForm

    def save_model(self, request, obj, form, change):
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_writer=False)
