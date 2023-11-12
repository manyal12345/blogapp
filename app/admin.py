from django.contrib import admin

from app.models import Comments, Post, Subscribe, Tag, Profile, VideoSlider, WebsiteMeta

# Register your models here.
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comments)
admin.site.register(Subscribe)
admin.site.register(Profile)
admin.site.register(WebsiteMeta)
admin.site.register(VideoSlider)