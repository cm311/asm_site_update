from django.shortcuts import  render, redirect
from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers  # Import for general serializer usage
from .models import Ticket, Action
from .forms import TicketForm, ActionForm, TagForm, KASearchForm


def update_ticket(request):
  if request.method == 'POST':
    # Create a form instance with submitted data
    ticket_form = TicketForm(request.POST)
    actions_form = ActionForm(request.POST)
    ka_search_form = KASearchForm(request.POST)

    if ticket_form.is_valid() and actions_form.is_valid():
      print('ticket is valid')

      ticket = ticket_form.save()  # Save the ticket form and get the instance

      # Access the Action instance created by actions_form.save()
      action = actions_form.save()  

      # Add the action to the ticket's actions ManyToManyField
      ticket.actions.add(action)

      # Redirect to success page or display success message
      return redirect('success')
   
  else:
    # Render the empty form
    ticket_form = TicketForm()
    actions_form = ActionForm()
    ka_search_form = KASearchForm()

  context = {'ticket_form': ticket_form, 'actions_form' : actions_form, 'ka_search_form' : ka_search_form}
  return render(request, 'update_ticket.html', context)


def search_ticket(request):
    if request.method == 'POST':
      # Create a form instance with submitted data
      ticket_form = TicketForm(request.POST)
      actions_form = ActionForm(request.POST)
      ka_search_form = KASearchForm(request.POST)
      ka_number = int(ka_search_form['ka_number'].value())
      ticket = Ticket.objects.filter(ka_number=ka_number)[0]
      actions = ticket.actions.all().values()[0]
      template = {}

      template[str(ticket.ka_number)] = {}
      template[str(ticket.ka_number)]['Subject'] = actions['subject']
      template[str(ticket.ka_number)]['Service'] = ticket.service
      template[str(ticket.ka_number)]['Configuration Item'] = ticket.configuration_item
      template[str(ticket.ka_number)]['Type'] = ticket.ticket_type
      template[str(ticket.ka_number)]['Description'] = actions['description']
      template[str(ticket.ka_number)]['Actions & Solutions'] = actions['actions_and_solutions']

      ticket_form = TicketForm(initial={'ka_number': ka_number,'service': ticket.service,'configuration_item':ticket.configuration_item,
        'type' : ticket.ticket_type})
      actions_form = ActionForm(initial={'actions_and_solutions' : actions['actions_and_solutions'], 'subject' : actions['subject'], 'description' : actions['description']})

      context = {'ticket_form': ticket_form, 'actions_form' : actions_form, 'ka_search_form' : ka_search_form}
      return render(request, 'update_ticket.html', context)


def success(request):
    print('it worked')
    return render(request, 'success.html', {})


def update_KA_json(request):
  tickets = Ticket.objects.all()
  d = {}
  for ticket in tickets:
    print(ticket)
    actions = ticket.actions.all().values()[0]

    d[str(ticket.ka_number)] = {}
    d[str(ticket.ka_number)]['Subject'] = actions['subject']
    d[str(ticket.ka_number)]['Service'] = ticket.service
    d[str(ticket.ka_number)]['Configuration Item'] = ticket.configuration_item
    d[str(ticket.ka_number)]['Type'] = ticket.ticket_type
    d[str(ticket.ka_number)]['Description'] = actions['description']
    d[str(ticket.ka_number)]['Actions & Solutions'] = actions['actions_and_solutions']
    #d[str(ticket.ka_number)]['Tags'] = To add later, will be the tags that the user can search

  response = JsonResponse(d, safe=False)
  response['Access-Control-Allow-Origin'] = '*'
  return response





def search_ka_number(request, ka_number):
    # Implement your logic to search for the KA number (e.g., database lookup)
    # Assuming you have a function to retrieve ticket details by KA number:
    ticket_data = Ticket.objects.get(ka_number=ka_number)
    print(type(ticket_data))

    if ticket_data:
        # Return relevant data as a dictionary for the response
        return JsonResponse({
            'ka_number': ticket_data['ka_number'],
            'ka_title': ticket_data['ka_title']
        })
    else:
        # Handle case where no ticket is found
        return JsonResponse({'error': 'KA number not found.'}, status=404)

