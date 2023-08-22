from django.contrib import admin

from applications.user_wall import models


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title')


@admin.register(models.UserPost)
class UserPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'slug')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title', )}


@admin.register(models.UserComment)
class UserCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'creation_date', 'author')
    list_display_links = ('id', )
    readonly_fields = ('creation_date', )


