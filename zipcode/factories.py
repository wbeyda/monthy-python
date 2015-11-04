import factory
from Faker import faker
import random
from zipcode import models
import glob
import os
import datetime

fake = Faker()
profile_pics = glob.glob(os.path.expanduser('~/Desktop/profiles/*.*'))

def begining_of_the_month():
    d = datetime.datetime.now()
    d = d.replace(day=1, hour=0, minute=0, microsecond =0)
    return d

def end_of_the_month():
    d = datetime.datetime.now()
    d = d.replace(month = d.month +1 % 12, day=1, hour=0, minute=0, microsecond =0)
    return d


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'zipcode.Customer'
        django_get_or_create = ('first_name', 'last_name', 'email', 
                                'phone_number', 'address_line_1', 
                                'address_line_2', 'city', 'state' 
                                'zipcode', 'subscribed', 'special_notes',)

        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone_number = fake.phone_number()
        address_line_1 = fake.street_address()
        address_line_2 = fake.secondary_address()
        city = fake.city()
        state = fake.state_abbr()
        zipcode = fake.postcode()
        subscribed = True
        special_notes = fake.paragraph()

class ContractorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'zipcode.Contractor'
        django_get_or_create = ( "user", "areacode", "firstname", "lastname", "trade", "secondaryTrades", "bio", "pic",)

    user = factory.SubFactory(CustomerFactory)  
    areacode = fake.postcode()
    firstname = fake.first_name() 
    lastname = fake.last_name()
    trade = fake.bs()
    secondayTrades = fake.bs()
    bio = fake.paragraph()
    pic = random.choice(profile_pics)

class ContractorScheduleFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'zipcode.Customer'
        django_get_or_create = ("firstname", "customer", "start_date",
                                "end_date", "repair", "estimate", 
                                "installation", "maintenance", 
                                "all_day", "value_care", "emergency", "title", "description",)

        firstname = factory.SubFactory(ContractorFactory)
        customer = factory.SubFactory(CustomerFactory)
        start_date = fake.date_time_between_dates(datetime_start = begining_of_the_month(), datetime_end= end_of_the_month())
        end_date = fake.date_time_between_dates(datetime_start = sd, datetime_end= end_of_the_month())
        repair = random.randint(0,1)
        estimate = random.randint(0,1)
        installation = random.randint(0,1)
        maintenance = random.randint(0,1)
        all_day = random.randint(0,1)
        emergency = random.randint(0,1)
        value_care = random.randint(0,1)
        title = fake.sentence()
        description = fake.paragraph()
        location = fake.street_address()
        completed = random.randint(0,1)
        pending = random.randint(0,1)
        requested = random.randint(0,1)
        cancelled = random.randint(0,1)
