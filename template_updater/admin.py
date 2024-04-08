from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Ticket, Action  # Assuming these are your model names

User = get_user_model()

admin.site.register(Ticket)
admin.site.register(Action)



