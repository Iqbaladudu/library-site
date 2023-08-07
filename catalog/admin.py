from django.contrib import admin
from django.db import models

# Register your models here.
from .models import Author, Genre, Book, BookInstance, NaturalLang, Language


# admin.site.register(Author)
# Define the admin class
class AuthorAdminInline(admin.TabularInline):
    model = Book
    extra = 0
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','date_of_birth', 'date_of_death')
    fields = ['first_name','last_name', ('date_of_birth', 'date_of_death')]
    inlines = [AuthorAdminInline]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)
# admin.site.register(Book)
# admin.site.register(BookInstance)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','display_genre')
    inlines = [BookInstanceInline]
    
# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    last_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('book','status','due_back', 'id')
    fieldsets = (
        (None, {
            'fields': ('book','imprint','id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

admin.site.register(Genre)
admin.site.register(NaturalLang)
admin.site.register(Language)