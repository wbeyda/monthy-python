from django.test import TestCase
from django.http import HttpRequest
from django.http import HttpResponse
from django.core.urlresolvers import resolve

from zipcode.models import *
from zipcode.views import request_event 
from zipcode.factories import CustomerFactory, ContractorFactory, ContractorScheduleFactory

import random

class ScheduleRequestTests(TestCase):

    def test_request_page(self):
        #contractor = Contractor.objects.get(id=random.randint(1,2))
        contractor = Contractor.objects.get(id=1)
        con_page = '/' + contractor.firstname + '/' + contractor.id + '/' + contractor.lastname + '/'
        found = resolve(con_page)
        self.assertEqual(found.func, request_event(contractor.id))

    def test_request_event(self):
        #contractor = Contractor.objects.get(id=random.randint(1,2))
        contractor = Contractor.objects.get(id=1)
        con_page = '/' + contractor.firstname + '/' + contractor.id + '/' + contractor.lastname + '/'

        request = HttpRequest(con_page,'POST')
        response = request_event(request, 1)
        print(response)
        self.assertTrue(response.content.startswith(b'<html>'))
