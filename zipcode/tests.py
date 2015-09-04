from django.test import TestCase
from .models import *
import datetime


class ScheduleMethodTests(TestCase):

    def test_create_test_dates(self):
       pass

    def test_contractor_avialability(self):
        avail = Availability.objets.all() 
        for i in avial:
            if i.weekends == True
