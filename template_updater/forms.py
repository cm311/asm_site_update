from django import forms
from .models import Ticket, Action, Tag

class TicketForm(forms.ModelForm):
  class Meta:
    model = Ticket
    fields = ['ka_number', 'service', 'configuration_item', 'ticket_type']

  def __init__(self, *args, **kwargs):
    super(TicketForm, self).__init__(*args, **kwargs)
    self.fields['ticket_type'].widget = forms.Textarea(attrs={'cols': 80, 'rows': 1})  # Adjust cols and rows as needed


class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ['subject', 'description', 'actions_and_solutions']

    def __init__(self, *args, **kwargs):
        super(ActionForm, self).__init__(*args, **kwargs)








class KASearchForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ka_number']
    def __init__(self, *args, **kwargs):
        super(KASearchForm, self).__init__(*args, **kwargs)



class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Tags, separated by commas"

