#!/usr/bin/env python
from app.models import *
from django.contrib.auth.models import Permission, Group, ContentType
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = ''
    help = 'Populate Database with the seed at /app/management/commands/populate_db.py'


    def handle(self, *args, **options):
        for i in Measure.objects.all():
            print('---------------------------')
            print(i.pk)
            print(i.ground.all())
            print(i.nutritional.all())
            print(i.biological.all())
            print('---------------------------')

        for i in Biological.objects.all():
            print('>>>>>>>>>>>>>>>>>>>>>>>>')
            print(i)
            print(i.measure)
            print('>>>>>>>>>>>>>>>>>>>>>>>>')



    
    
    
