import factory
from . import models
from faker import Factory as FakerFactory
from faker import Faker

fake = Faker()
faker = FakerFactory.create()

class RandomContractorSchedule(factory.Factory):
    class Meta:

        model = models.ContractorSchedule
    
    start_date = fake.date_time_this_month()
    end_date = fake.date_time_this_month()
     
