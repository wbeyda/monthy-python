from django.test import TestCase, Client
from django.http import HttpRequest
from django.http import HttpResponse
from django.core.urlresolvers import resolve
from django.http import JsonResponse

from .models import *
from .views import request_event
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

from faker import Faker

import random

fake = Faker('en_US')

class ScheduleRequestTests(TestCase):

    def setUp(self):
        self.joe = mommy.make('zipcode.Contractor')
        self.sally = mommy.make('zipcode.Customer', first_name="sally")
        self.joeshours = mommy.make('zipcode.Availability', prefered_zipcodes="84115,84101", contractor=self.joe)
        self.fixsink = mommy.make('zipcode.ContractorSchedule', firstname=self.joe, customer=self.sally)

    def test_request_page(self):
        contractor = self.joe
        url = '/schedule/' + str(contractor.id) + '/11/13/2015/10'
        request = HttpRequest()
        request.path = url
        request.method = 'GET'
        request.GET = {"year": u"2015", "month": u"11", "day": u"13", "hour": u"9", "id": contractor.id}
        c = Client()
        response = c.get(request.path, request.GET)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response)

    def test_request_event_get_form(self):
        contractor = self.joe
        url = '/schedule/' + str(contractor.id) + '/11/13/2015/10'
        request = HttpRequest()
        request.path = url
        request.method = 'GET'
        request.GET = {"year": u"2015", "month": u"11", "day": u"13", "hour": u"9", "id": contractor.id}
        response = request_event(request, contractor.id)
        self.assertTrue(response.content.startswith('\n<div class="row">'))

    def test_request_event_post_with_errors(self):
        contractor = self.joe
        customer = self.sally
        url = '/schedule/' + str(contractor.id) + '/11/13/2015/10'
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {"year": u"2015", "month": u"11", "day": u"13",
                        "hour": u"9", "id": contractor.id,
                        "customer": self.sally, "start_date_0": "11/7/2015",  "start_date_1": "9:00",
                        "end_date_0": "11/7/2015",  "end_date_1": "11:00",
                        "all_day": False, "repair": True, "estimate": False, "installation": False,
                        "maintenance": False, "value_care": False, "emergency": False, "descriptin": ""
                       }
        request.path = url
        response = request_event(request, contractor.id)
        self.assertEqual(type(response), JsonResponse)

    def test_request_event_post_form_is_valid(self):
        contractor = self.joe
        customer = self.sally
        url = '/schedule/' + str(contractor.id) + '/11/13/2015/10'
        request = HttpRequest()
        request.path = url

