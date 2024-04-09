from django.shortcuts import  render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers  # Import for general serializer usage
from .models import Ticket, Action, SuggestedUpdate
from .forms import TicketForm, ActionForm, TagForm, KASearchForm



def update_ticket(request):

  if request.method == 'POST' and 'updated' in request.POST:
    ticket_form = TicketForm(request.POST)
    actions_form = ActionForm(request.POST)
    ka_search_form = KASearchForm(request.POST)


    suggested = SuggestedUpdate()
    suggested.subject = request.POST['subject']
    suggested.description = request.POST['description']
    suggested.actions_and_solutions = request.POST['actions_and_solutions']
    suggested.ka_number = request.POST['ka_number']
    suggested.service = request.POST['service']
    suggested.configuration_item = request.POST['configuration_item']
    suggested.ticket_type = request.POST['ticket_type']

    suggested.save()

    return redirect('success')
  
  elif request.method == 'POST' and 'searched' in request.POST:
    ticket_form = TicketForm()
    actions_form = ActionForm()

    ka_number = request.POST['search_ka']
    if Ticket.objects.filter(ka_number=int(ka_number)).exists():
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
        'ticket_type' : ticket.ticket_type})
      actions_form = ActionForm(initial={'actions_and_solutions' : actions['actions_and_solutions'], 'subject' : actions['subject'], 'description' : actions['description']})

      context = {'ticket_form': ticket_form, 'actions_form' : actions_form}
      return render(request, 'update_ticket.html', context)
    else:
      ticket_form = TicketForm()
      actions_form = ActionForm()
      context = {'ticket_form': ticket_form, 'actions_form' : actions_form, 'nonexistant' : 'KA not found'}
      return render(request, 'update_ticket.html', context)
    
  else:
    # Render the empty form
    ticket_form = TicketForm()
    actions_form = ActionForm()
    ka_search_form = KASearchForm()

  context = {'ticket_form': ticket_form, 'actions_form' : actions_form, 'ka_search_form' : ka_search_form}
  return render(request, 'update_ticket.html', context)


def success(request):
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


@login_required
def approve_updates(request):
    # This view will only be accessible to logged-in users

    suggested_updated = SuggestedUpdate.objects.all()
    ticket_form1 = TicketForm()
    actions_form1 = ActionForm()
    ticket_form2 = TicketForm()
    actions_form2 = ActionForm()
    ka_search_form = KASearchForm()

    context = {'suggested_updated' : suggested_updated, 'ticket_form1': ticket_form1, 'actions_form1' : actions_form1, 'ticket_form2': ticket_form2, 'actions_form2' : actions_form2}
    return render(request, 'approve_updates.html', context)














@login_required
def finalize_update(request):
  if request.method == 'POST':
    todelete = SuggestedUpdate.objects.get(id=int(request.POST['todelete']))
    todelete.delete()

    if 'reject' in request.POST:
      message = "Template for KA " + request.POST['ka_number'] + " not updated."
      return render(request, 'finalized.html', {'message' : message})


    
    ticket_form = TicketForm(request.POST)
    actions_form = ActionForm(request.POST)
    ka_search_form = KASearchForm(request.POST)

    if Ticket.objects.filter(ka_number=int(request.POST['ka_number'])).exists():
      ticket = Ticket.objects.filter(ka_number=int(request.POST['ka_number']))[0]

      actions = ticket.actions.all()  # Fetches all related Action objects

      # Update fields (consider iteration or filtering for specific actions)
      for action in actions:
          action.subject = request.POST['subject']  # Update subject for all related actions
          action.description = request.POST['description']
          action.actions_and_solutions = request.POST['actions_and_solutions']

      # Save changes to all Action objects
      for action in actions:
          action.save()

      ticket.ka_number = request.POST['ka_number']
      ticket.service = request.POST['service']
      ticket.ticket_type = request.POST['ticket_type']
      ticket.configuration_item = request.POST['configuration_item']

      ticket.save()

    else:
      # Create a form instance with submitted data
      if ticket_form.is_valid() and actions_form.is_valid():
        print('ticket is valid')

        ticket = ticket_form.save()  # Save the ticket form and get the instance

        # Access the Action instance created by actions_form.save()
        action = actions_form.save()  

        # Add the action to the ticket's actions ManyToManyField
        ticket.actions.add(action)
    
    message = "Success!!  Template for KA " + request.POST['ka_number'] + "  updated."
    return render(request, 'finalized.html', {'message' : message})




















def custom_logout(request):
    logout(request)
    context = {}  # Add any custom context data if needed
    return render(request, 'logout.html', context=context)

def detail(request, id):
  suggested_updated = SuggestedUpdate.objects.all()
  

  suggested = SuggestedUpdate.objects.filter(id=id)[0]

  ticket_form1 = TicketForm(initial={'ka_number': suggested.ka_number, 'service' : suggested.service, 'configuration_item' : suggested.configuration_item,
  'ticket_type' : suggested.ticket_type})

  actions_form1 = ActionForm(initial={'subject' : suggested.subject, 'actions_and_solutions' : suggested.actions_and_solutions,
  'description' : suggested.description})


  #search for the ticket object already in the DB

  try:
    ticket = Ticket.objects.filter(ka_number=suggested.ka_number)[0]
    actions = ticket.actions.all().values()[0]

    ticket_form2 = TicketForm(initial={'ka_number': suggested.ka_number,'service': ticket.service,'configuration_item':ticket.configuration_item,
          'ticket_type' : ticket.ticket_type})
    actions_form2 = ActionForm(initial={'actions_and_solutions' : actions['actions_and_solutions'], 'subject' : actions['subject'], 'description' : actions['description']})
  
  #no ticket found for that KA number in the existing DB
  except:
    ticket_form2 = TicketForm(initial={'ka_number': suggested.ka_number})
    actions_form2 = ActionForm(initial={'subject' : 'NO KA DATA FOUND', 'description' : 'NO KA DATA FOUND'})


  context = {'suggested_updated' : suggested_updated, 'ticket_form1': ticket_form1,
   'actions_form1' : actions_form1, 'ticket_form2': ticket_form2, 'actions_form2' : actions_form2, 'suggested_id' : suggested.id}

  return render(request, 'approve_updates.html', context)
