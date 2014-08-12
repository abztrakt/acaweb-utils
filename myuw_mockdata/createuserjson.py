import sys
sys.path.append('/home/cbessee/myuw_mobile/src/restclients/restclients/models')

from django.forms.models import model_to_dict
from myuw_mobile.models import *
import calendar
import configs
from datetime import date, timedelta
import json
import random
from sws import Person
import time

def courses():
    pass

def sws(regid, netid):
    lastname = netid[1:]
    fname = netid[:1]

    student = input("Is this user a student? (True/False): ")
    employee = input("Is this user an employee? (True/False): ")
    alumni = input("Is this user an alumni? (True/False): ")
    faculty = input("Is this user faculty? (True/False): ")
    staff = input("Is this user staff? (True/False): ")

    person = Person.objects.create(uwregid=regid, uwnetid=netid, surname=lastname, first_name=fname, full_name=netid, whitepages_publish="false", is_student=student, is_employee=employee, is_alum=alumni, is_faculty=faculty, is_staff=staff, email1=netid + "@uw.edu")

    sws = person.json_data()

    return sws

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end.strftime('%Y/%m/%dT%H:%M:%S'), format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%Y/%m/%dT%H:%M:%S', prop)


def hfs():
    addfundsurl = "https://www.hfs.washington.edu/olco"
    hfs = {}

    shc = {}
    shc["balance"] = round(random.random() * random.randint(0, 1000), 2)
    lu = randomDate("2014/1/1T15:17:16", datetime.now(), random.random())
    shc["last_updated"] = lu
    shc["adds_funds_url"] = addfundsurl

    employee = raw_input("Does this user have an employee husky card? (y/n): ")
    if employee == 'y':
        ehc = {}
        ehc["balance"] = round(random.random() * random.randint(0, 1000), 2)
        lu = randomDate("2014/1/1T15:17:16", datetime.now(), random.random())
        ehc["last_updated"] = lu
        ehc["adds_funds_url"] = addfundsurl
    else:
        ehc = null

    rd = {}
    rd["balance"] = round(random.random() * random.randint(0, 1000), 2)
    lu = randomDate("2014/1/1T15:17:16", datetime.now(), random.random())
    rd["last_updated"] = lu
    rd["adds_funds_url"] = addfundsurl

    hfs["student_husky_card"] = shc
    hfs["employee_husky_card"] = ehc
    hfs["resident_dining"] = rd

    return hfs


def libr():
    libinfo = raw_input("Does this user need library data? (y/n): ")
    if libinfo == 'y':
        data = {}
        data["holds_ready"] = random.randint(0, 10)
        data["fines"] = round(random.random() * random.randint(0, 10), 2)
        data["items_loaned"] = random.randint(0, 10)
        if data["items_loaned"] != 0:
            firstJan = date.today().replace(day=1, month=1)
            randomDay = firstJan + timedelta(days = random.randint(0, 365 if calendar.isleap(firstJan.year) else 364))
            data["next_due"] = str(randomDay)
        else:
            data["next_due"] = ''
        return data
    else:
        pass

def tuition():
    pass


def main():
    netid = configs.usernames[random.randint(0, len(configs.usernames))]
    regid = random.randint(10000000000, 99999999999)

    newuser = User.objects.create(uwnetid=netid, uwregid=regid)
    newuser.last_visit = str(newuser.last_visit)
    newuserdict = model_to_dict(newuser)

    libraries = libr()
    newuserdict["libraries"] = libraries

    hfsdata = hfs()
    newuserdict["hfs"] = hfsdata

    swsdata = sws(regid, netid)
    newuserdict['sws'] = swsdata

    filename = 'mockdata/' + netid + '.json'

    with open(filename, 'w') as outfile:
        json.dump(newuserdict, outfile)


if __name__ == "__main__":
    main()

