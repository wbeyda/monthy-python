import random
import datetime
import glob
import os
from django.core.files import File
from faker import Faker
from django.core.exceptions import ValidationError
from zipcode import models 

fake = Faker()
gallery_pics = glob.glob(os.path.expanduser('~/Desktop/gallery/*.*'))

def begining_of_the_month():
    d = datetime.datetime.now()
    d = d.replace(day=1, hour=0, minute=0, microsecond =0)
    return d

def end_of_the_month():
    d = datetime.datetime.now()
    if d.month == 12:
        d = d.replace(year = d.year + 1, month=1, day=1, hour=0, minute=0, microsecond=0)
    else:
        d = d.replace(month = d.month +1 % 12, day=1, hour=0, minute=0, microsecond =0)
    return d

while True:
    cust = Customer( first_name = fake.first_name(),
                          last_name = fake.last_name(),
                          email = fake.email(),
                          phone_number = fake.phone_number(),
                          address_line_1 = fake.street_address(),
                          address_line_2 = fake.secondary_address(),
                          city = fake.city(),
                          state = fake.state_abbr(),
                          zipcode = fake.postcode(),
                          subscribed = True,
                          special_notes = fake.paragraph() ,
                        )
    cust.save()

    fn = Contractor.objects.get(id=random.randint(1,2))
    sd = fake.date_time_between_dates(datetime_start = begining_of_the_month(), datetime_end= end_of_the_month())
    ed = fake.date_time_between_dates(datetime_start = sd, datetime_end= end_of_the_month())
    rr = random.randint(0,1)
    et = random.randint(0,1)
    ins = random.randint(0,1)
    mn = random.randint(0,1)
    ad = random.randint(0,1)
    vc = random.randint(0,1)
    em = random.randint(0,1)
    tt = fake.sentence()
    dc = fake.paragraph()
    lc = fake.street_address()


    c =ContractorSchedule( firstname=fn,
                        customer = cust,
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

    try:
       # c.start_date_before_now()
        c.end_date_before_start_date()
        c.clean_seconds()
        #c.is_chunk()
        c.double_booked()
        c.two_hour_blocks()
        c.multiple_days()     
        c.all_day_double()
        c.day_is_full()
        c.before_prefered_start_time()
        c.after_prefered_end_time()
        c.save()
        
        galpic = random.choice(gallery_pics)
        testi = Testimonial(customer= cust,
                            customer_testimonial = fake.paragraph(),
                            customer_date = fake.date_time_between_dates(datetime_start = begining_of_the_month(), datetime_end= end_of_the_month()),
                            contractor = c.firstname,
                            job = c,
                            job_pic_url = fake.uri() + fake.uri_path(),
                            hashtags = '#' + fake.word(),
                            socialtags = '@'+ fake.company_email().split('@')[1].split('.')[0],
                            approved_status = random.randint(0,1),
                            best_of = random.randint(0,1),
                    )

        testi.job_pic.save(galpic, File(open(galpic, 'r')))
        gall = Gallery(caption = fake.paragraph(), testimonial=testi)
        gall.save()
        print "MADE ONE!! ", c.id

    except ValidationError as v:
        cust.delete()
        print(v)
        continue
    else:
        break


    
