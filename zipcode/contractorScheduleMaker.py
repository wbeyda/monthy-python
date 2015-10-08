import random
import datetime
from faker import Faker
from django.core.exceptions import ValidationError


fake = Faker()

def begining_of_the_month():
    d = datetime.datetime.now()
    d = d.replace(day=1, hour=0, minute=0, microsecond =0)
    return d

def end_of_the_month():
    d = datetime.datetime.now()
    d = d.replace(month = d.month +1 % 12, day=1, hour=0, minute=0, microsecond =0)
    return d

while True:
    #import pdb; pdb.set_trace()
    fn = Contractor.objects.get(id=random.randint(1,2))
    sd = fake.date_time_between_dates(datetime_start = begining_of_the_month(), datetime_end= end_of_the_month())
    ed = fake.date_time_between_dates(datetime_start = sd, datetime_end= end_of_the_month())
    rr = random.randint(0,1)
    et = random.randint(0,1)
    ins = random.randint(0,1)
    mn = random.randint(0,1)
    ad = random.randint(0,1)
    tt = fake.sentence()
    dc = fake.paragraph()
    lc = fake.street_address()


    c =ContractorSchedule( firstname=fn,
                        start_date=sd,
                        end_date=ed,
                        repair=rr,
                        estimate=et,
                        installation=ins,
                        maintenance=mn,
                        all_day=ad,
                        title=tt,
                        description=dc,
                      )
    print('start and end: ', sd,ed) 

    try:
       # c.start_date_before_now()
        c.end_date_before_start_date()
        #c.is_chunk()
        c.double_booked()
        c.two_hour_blocks()
        c.multiple_days()     
        c.all_day_double()
        c.day_is_full()
        c.before_prefered_start_time()
        c.after_prefered_end_time()
        c.save()

    except ValidationError as v:
        print(v)
        continue
    else:
        break

