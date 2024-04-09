# Generated by Django 4.2.11 on 2024-04-08 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('template_updater', '0002_ticket_ticket_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuggestedUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ka_number', models.IntegerField()),
                ('ka_title', models.CharField(max_length=255)),
                ('service', models.CharField(max_length=355)),
                ('configuration_item', models.CharField(max_length=355)),
                ('ticket_type', models.CharField(max_length=455)),
                ('subject', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('actions_and_solutions', models.TextField()),
            ],
        ),
    ]