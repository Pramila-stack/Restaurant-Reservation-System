from django.contrib import admin

from reservation.models import MenuItem, Profile, Reservation, Table

# Register your models here.
admin.site.register(Profile)
admin.site.register(MenuItem)
admin.site.register(Table)
admin.site.register(Reservation)