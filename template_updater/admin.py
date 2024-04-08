from django.contrib import admin
from .models import Ticket, Action  # Assuming these are your model names

admin.site.register(Ticket)
admin.site.register(Action)
