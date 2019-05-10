from django.contrib import admin
from photo.models import Photo, ShipPhoto, Product
from photo.models import Supplier


# Register your models here.
#


class PhotoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user_name = request.user
        obj.save()


admin.site.register(Supplier,)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(ShipPhoto)
admin.site.register(Product)