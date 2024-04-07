from django import forms
from .models import Ticket, Action, Tag

class TicketForm(forms.ModelForm):
  class Meta:
    model = Ticket
    fields = ['ka_number', 'ka_title', 'service', 'configuration_item']

  def __init__(self, *args, **kwargs):
    super(TicketForm, self).__init__(*args, **kwargs)

class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ['subject', 'description', 'actions_and_solutions']

    def __init__(self, *args, **kwargs):
        super(ActionForm, self).__init__(*args, **kwargs)

