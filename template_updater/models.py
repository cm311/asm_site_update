from django.db import models

class Action(models.Model):
  """Model representing actions taken for a ticket and the description."""
  subject = models.CharField(max_length=255) # The subject line
  description = models.TextField()
  actions_and_solutions = models.TextField()

  def __str__(self):
    return f"Action: {self.description[:25]}..."  # Truncate description for display


class Tag(models.Model):
  """Model representing a tag for tickets."""
  name = models.CharField(max_length=255, unique=True)

  def __str__(self):
    return self.name


class Ticket(models.Model):
  """Model representing a service ticket."""
  ka_number = models.IntegerField(primary_key=True)  # Unique KA number that this links to
  ka_title = models.CharField(max_length=255, default=' ') # The KA description
  service = models.CharField(max_length=355, default=' ') # The service dropbox
  configuration_item = models.CharField(max_length=355, default=' ') # the configuration item dropbox
  ticket_type = models.CharField(max_length=455, default=' ')

  actions = models.ManyToManyField(Action, related_name='tickets') # Each KA can have several possible actions and solutions
  tags = models.ManyToManyField(Tag, related_name='tickets') # Each KA has several tags.  Things are searched by this tag.

  

  def __str__(self):
    return f"KA #{self.ka_number} - {self.ka_title} - {self.actions}"


class SuggestedUpdate(models.Model):
  ka_number = models.IntegerField()  # Unique KA number that this links to
  service = models.CharField(max_length=355, default=' ') # The service dropbox
  configuration_item = models.CharField(max_length=355, default=' ') # the configuration item dropbox
  ticket_type = models.CharField(max_length=455, default=' ')
  subject = models.CharField(max_length=255, default=' ') # The subject line
  description = models.TextField(default=' ')
  actions_and_solutions = models.TextField(default=' ')

  def __str__(self):
    return self.subject




