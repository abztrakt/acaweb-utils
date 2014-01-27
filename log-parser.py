import re
import gzip
import urllib
import pdb
import csv
import operator

DEBUG = False;

QUARTER = 'AUTUMN'
AUTUMN_START = '20120924'
AUTUMN_END = '20130106'
WINTER_START = '20130107'
WINTER_END = '20130331'
SPRING_START = '20130401'
SPRING_END = '20130623'
SUMMER_START = '20130624'
SUMMER_END = '20130710'

def main():
    if QUARTER == "AUTUMN":
        start = AUTUMN_START
        end = AUTUMN_END
    elif QUARTER == "WINTER":
        start = WINTER_START
        end = WINTER_END
    elif QUARTER == "SPRING":
        start = SPRING_START
        end = SPRING_END
    else: #QUARTER == SUMMER
        start = SUMMER_START
        end = SUMMER_END
    year = start[:4]      
  #  year = start / 10000
#    print "year is: " + year
    month = start[4:6]
  #  month = ( (start / 100) % 100 )
#    print "month is: " + month
    date = start[-2:]
  #  date = start % 100
#    print "date is: " + date
    data = LogReport()
  
    DATE = year + month + date

#    print "Date: " + DATE
   
#    print "start date: " + start
#    print "end date: " + end
    while ( DATE != end):
        filename = 'logs/access_log.' + DATE + '.gz'
        print "Filename: " + filename
        
        
        f = gzip.open(filename)
        split1 = filename.split('logs/access_log.');
        split2 = split1[1].split('.gz')
        fname = "%s%s%s%s/%s%s/%s%s" % (split2[0][0],split2[0][1],split2[0][2],split2[0][3],split2[0][4],split2[0][5],split2[0][6],split2[0][7])
#        print fname
        regex = re.compile('\/api\/v1\/spot\/\?')
        count = 0
        pCount = 0
        dictionary = {}
            
        for line in f:
            search_terms = re.search(regex, line)
            if search_terms:
                count = count + 1
                if DEBUG == True: 
                    print "Entry #%d: " % count
                    print "Original log entry: %s" % line  #print the entire log line
                line = urllib.unquote(line) #decode URL
                if DEBUG == True:
                    print "Original log entry with decoded url: %s" % line
                
                phrases = line.split('&')   #split the line by different filters
                firstLine = phrases[0].split('?')   #strip the stuff before question mark that's attached to the filter
                phrases[0] = firstLine[1]
           
                length = len(phrases)
                lastLine = phrases[length - 1].split('HTTP')  #strip the unnecessary stuff attached to the last filter
                phrases[length - 1] = lastLine[0]
                
                for index in range(len(phrases)):
                    if index < len(phrases):
                        if phrases[index].find('=') == -1:
                            phrases[index - 1] += '&' + phrases[index]
                            phrases.remove(phrases[index])

                pCount = 0
                for phrase in phrases:
                    pCount = pCount + 1
                    
                    if phrase.endswith(' '):
                        phrase = phrase[:-1]
                    
                    if DEBUG == True:
                        print "Filter #%d: %s" % (pCount, phrase)
                            
                    if not phrase.startswith('T'):
                        request = phrase.split('=')
                    
                    key = request[0]        #outer dict keys(filters) are text to the left of equal sign 
                    innerKey = request[1]   #inner dict keys(corresponding options) are text to the right of equal sign
                    temp = innerKey.split('+')
                    innerKey = ' '.join(temp)
                    
                    if key.startswith('extended_info'):
                        key = key[14:]      #strip 'extended_info' from key
                    
                    if key in dictionary:   #if key(filter) already exists
                        if innerKey in dictionary[key]:
                            dictionary[key][innerKey] += 1   #increment of the option frequency
                        else:
                            dictionary[key][innerKey] = 1    #create new mapping and set the value(frequency of a certain option) to 1
                    else:                   #key(filter) not exist
                        dictionary[key] = {innerKey: 1}      #create new mapping --- inner dict key:option; inner dict value: frequency(1); outer dict key: filter term; outer dict value: inner dict

                if DEBUG == True: 
                    print '\n'
        
        #delete the following because they are not very useful?
        if 'center_latitude' in dictionary:
            del dictionary['center_latitude']
        if 'center_longitude' in dictionary:
            del dictionary['center_longitude']
        if 'distance' in dictionary:
            del dictionary['distance']
        if 'limit' in dictionary:
            del dictionary['limit']
        if 'q' in dictionary:
            del dictionary['q']
        if 'cx' in dictionary:
            del dictionary['cx']
        if 'cof' in dictionary:
            del dictionary['cof']
        if 'sa' in dictionary:
            del dictionary['sa']

    #    print dictionary
    #    print "Total search found: %d" % count + '\n'
        
    #    print "Search Summary:" + '\n'
        for keys in dictionary:
    #        print keys + ": " 
            for filters in dictionary[keys]:
    #            print "    " + filters + ": " + str(dictionary[keys][filters])
                if keys == 'capacity':
                    data.update_capacity(filters, dictionary[keys][filters])
                    #print data.capacity
                if keys == 'noise_level':
                    data.update_noiselvl(filters, dictionary[keys][filters])
                    #print data.noise_level
                if keys == 'type':
                    data.update_type(filters, dictionary[keys][filters])
                    #print data.space_type
                if keys == 'building_name':
                    data.update_building(filters, dictionary[keys][filters])
                    #print data.building_name
                if keys == 'reservable':
                    data.update_reservable(dictionary[keys][filters])
                    #print data.reservable
                if keys == 'food_nearby':
                    data.update_food(filters, dictionary[keys][filters])
                    #print data.food_nearby
                if keys == 'open_now':
                    data.update_openNow(dictionary[keys][filters])
                if keys == 'open_at':
                    data.update_openAt(filters, dictionary[keys][filters])
                if keys == 'open_until':
                    data.update_openTil(filters, dictionary[keys][filters])
                if keys.startswith('has_'):
                    data.update_info(keys, dictionary[keys][filters])
            
    #        print '\n'
        
        if (month == '01' or month == '03' or month == '05' or month == '07' or month == '08' or month == '10' or month == '12'):
            if (date == '31' and month == '12'):
                month = '01'
                date = '01'
                year = str(int(year) + 1)
            if (date == '31' and month < '12'):
                month = str(int(month) + 1)
                if int(month) < 10:
                    month = '0' + str(month)
                date = '01'
            if date < '31':
                date = str(int(date) + 1)
                if int(date) < 10:
                    date = '0' + str(date)
                        
        else:
            if date < '30':
                date = str(int(date) + 1)
                if int(date) < 10:
                    date = '0' + str(date)
            if ((date == '30' and month < '12') or (date == '28' and month == '02')):
                month = str(int(month) + 1)
                if int(month) < 10:
                    month = '0' + str(month)
                date = '01'

   #     print "month - " + month
        
   #     print "date - " + date

        DATE = year + month + date
   #     print "the next date is: " + DATE

    

#    print "Capacity: " + str(data.capacity)
#    print "Noise Level: " + str(data.noise_level)
#    print "Space Type: " + str(data.space_type)
#    print "Building Name: " + str(data.building_name)
#    print "Reservable: " + str(data.reservable)
#    print "Food Nearby: " + str(data.food_nearby)
#    print "Open Now: " + str(data.open_now)
#    print "Open At: " + str(data.open_at)
#    print "Open Until: " + str(data.open_until)
#    print "Extended Info: " + str(data.info)

    print "Search Summary:" + '\n'
    
    print "Capacity: "
    sorted_capacity = sorted(data.capacity.iteritems(), key=operator.itemgetter(1))
    sorted_capacity.reverse()
    for (key, value) in sorted_capacity:
        print "    " + key + ": " + str(value)
    print '\n'

    print "Noise Level: "
    sorted_noiselvl = sorted(data.noise_level.iteritems(), key=operator.itemgetter(1))
    sorted_noiselvl.reverse()
    for (key, value) in sorted_noiselvl:
        print "    " + key + ": " + str(value)
    print '\n'

    print "Space Type: "
    sorted_type = sorted(data.space_type.iteritems(), key=operator.itemgetter(1))
    sorted_type.reverse()
    for (key, value) in sorted_type:
        print "    " + key + ": " + str(value)
    print '\n'

    print "Extended Info: "
    sorted_info = sorted(data.info.iteritems(), key=operator.itemgetter(1))
    sorted_info.reverse()
    for (key, value) in sorted_info:
        print "    " + key + ": " + str(value)
    print '\n'

    print "Building Name: "
    sorted_building = sorted(data.building_name.iteritems(), key=operator.itemgetter(1))
    sorted_building.reverse()
    for (key, value) in sorted_building:
        print "    " + key + ": " + str(value)
    print '\n'

    print "Reservable: "
    print "    " + "True" + ": " + str(data.reservable)
    print '\n'

    print "Food Nearby: "
    sorted_food = sorted(data.food_nearby.iteritems(), key=operator.itemgetter(1))
    sorted_food.reverse()
    for (key, value) in sorted_food:
        print "    " + key + ": " + str(value)
    print '\n'

    print "Open Now: "
    print "    " + "True" + ": " + str(data.open_now)
    print '\n'

    print "Open At: "
    sorted_openAt = sorted(data.open_at.iteritems(), key=operator.itemgetter(1))
    sorted_openAt.reverse()
    for (key, value) in sorted_openAt:
        print "    " + key + ": " + str(value)
    print '\n'

    print "Open Until: " 
    sorted_openTil = sorted(data.open_until.iteritems(), key=operator.itemgetter(1))
    sorted_openTil.reverse()
    for (key, value) in sorted_openTil:
        print "    " + key + ": " + str(value)

#    with open('spring_quarter.csv', 'wb') as csvfile:
#        excelwriter = csv.writer(csvfile, delimiter='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#
#        for key in data.capacity:
#            excelwriter.writerow([key, data.capacity[key]])
#        for key in data.noise_level:
#            excelwriter.writerow([key, data.noise_level[key]])
#        for key in data.space_type:
#            excelwriter.writerow([key, data.space_type[key]])
#        for key in data.building_name:
#            excelwriter.writerow([key, data.building_name[key]])
#        for key in data.food_nearby:
#            excelwriter.writerow([key, data.food_nearby[key]])  
#        for key in data.open_at:
#            excelwriter.writerow([key, data.open_at[key]])
#        for key in data.open_until:
#            excelwriter.writerow([key, data.open_until[key]])
#        for key in data.info:
#            excelwriter.writerow([key, data.info[key]])
#    
#
#        excelwriter.writerow([data.reservable])
#        excelwriter.writerow([data.open_now])


class LogReport:
    """Parse log files and report data"""
    capacity = {}
    noise_level = {}
    space_type = {}
    building_name = {}
    info = {}
    open_at = {}
    open_now = 0
    open_until = {}
    reservable = 0
    food_nearby = {}

    def update_capacity(self, key, value):
        if key in LogReport.capacity:
            LogReport.capacity[key] += value
        else:
            LogReport.capacity[key] = value

    def update_noiselvl(self, key, value):
        if key in LogReport.noise_level:
            LogReport.noise_level[key] += value
        else:
            LogReport.noise_level[key] = value
    
    def update_type(self, key, value):
        if key in LogReport.space_type:
            LogReport.space_type[key] += value
        else:
            LogReport.space_type[key] = value
    
    def update_building(self, key, value):
        if key in LogReport.building_name:
            LogReport.building_name[key] += value
        else:
            LogReport.building_name[key] = value

    def update_reservable(self, value):
        LogReport.reservable += value

    def update_food(self, key, value):
        if key in LogReport.food_nearby:
            LogReport.food_nearby[key] += value
        else:
            LogReport.food_nearby[key] = value

    def update_openNow(self, value):
        LogReport.open_now += value

    def update_openAt(self, key, value):
        if key in LogReport.open_at:
            LogReport.open_at[key] += value
        else:
            LogReport.open_at[key] = value

    def update_openTil(self, key, value):
        if key in LogReport.open_until:
            LogReport.open_until[key] += value
        else:
            LogReport.open_until[key] = value

    def update_info(self, key, value):
        if key in LogReport.info:
            LogReport.info[key] += value
        else:
            LogReport.info[key] = value

if __name__ == '__main__':
    main()
