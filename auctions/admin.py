from django.contrib import admin
from .models import *

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_date', 'id')
    filter_horizontal = ("watching",)

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)