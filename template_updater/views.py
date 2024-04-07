from django.shortcuts import  render, redirect
from django.http import JsonResponse
from django.db import connection
from .models import Ticket, Action
from .forms import TicketForm, ActionForm


def update_ticket(request):
  if request.method == 'POST':
    # Create a form instance with submitted data
    ticket_form = TicketForm(request.POST)
    actions_form = ActionForm(request.POST)

    if ticket_form.is_valid() and actions_form.is_valid():
      print('ticket is valid')
      # Retrieve ticket object based on submitted ka_number
      print(ticket_form.cleaned_data)

      ticket = Ticket()
      actions = Action()

      # Update the ticket object with form data
      ticket.ka_number = ticket_form.cleaned_data['ka_number']
      ticket.ka_title = ticket_form.cleaned_data['ka_title']
      ticket.service = ticket_form.cleaned_data['service']
      ticket.configuration_item = ticket_form.cleaned_data['configuration_item']
      ticket.save()

      actions.subject = actions_form.cleaned_data['subject']
      actions.description = actions_form.cleaned_data['description']
      actions.actions_and_solutions = actions_form.cleaned_data['actions_and_solutions']
      actions.save()

      ticket.actions.add(actions)
      
      
    for e in Action.objects.all():
      print(e.subject)

      # Redirect to success page (or display success message)
      return redirect('success')  # Replace with your actual success URL pattern name
  else:
    # Render the empty form
    ticket_form = TicketForm()
    actions_form = ActionForm()

  context = {'ticket_form': ticket_form, 'actions_form' : actions_form}
  return render(request, 'update_ticket.html', context)

def success(request):
    print('it worked')
    return render(request, 'success.html', {})


def list_tickets_raw(request):
  # Execute a raw SQL query
  with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM template_updater_ticket")  # Replace with your table name
    tickets = cursor.fetchall()

  # Iterate through query results and print data
  for ticket in tickets:
    print(f"Ticket #{ticket[0]} - {ticket[1]}")  # Assuming column order (number, subject)

  return render(request, 'list_tickets.html', {})  # No context needed here



def search_ka_number(request, ka_number):
    # Implement your logic to search for the KA number (e.g., database lookup)
    # Assuming you have a function to retrieve ticket details by KA number:
    ticket_data = Ticket.objects.get(ka_number=ka_number)
    print(type(ticket_data))

    if ticket_data:
        # Return relevant data as a dictionary for the response
        return JsonResponse({
            'ka_number': ticket_data['ka_number'],
            'ka_title': ticket_data['ka_title'],
            # ... include other relevant data
        })
    else:
        # Handle case where no ticket is found
        return JsonResponse({'error': 'KA number not found.'}, status=404)

