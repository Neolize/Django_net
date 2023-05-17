from django.contrib import admin

from applications.groups import models


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'creator', 'slug')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title', )}


@admin.register(models.GroupPost)
class GroupPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'slug')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title', )}


@admin.register(models.GroupComment)
class GroupCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'creation_date', 'author')
    list_display_links = ('id', )
