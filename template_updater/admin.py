from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Ticket, Action, SuggestedUpdate  # Assuming these are your model names

User = get_user_model()

admin.site.register(Ticket)
admin.site.register(Action)
admin.site.register(SuggestedUpdate)



