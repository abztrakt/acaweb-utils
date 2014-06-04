import re
import gzip
import urllib
import pdb
import argparse
import csv

DEBUG = True;

def main(args):
    if args.filename:
        

        f = gzip.open(args.filename)
        split1 = args.filename.split('logs/access_log.');
        split2 = split1[1].split('.gz')
        fname = "%s%s%s%s/%s%s/%s%s" % (split2[0][0],split2[0][1],split2[0][2],split2[0][3],split2[0][4],split2[0][5],split2[0][6],split2[0][7])
        #print fname
        regex = re.compile('\/search\/\?')
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
                
                pCount = 0
                for phrase in phrases:
                    pCount = pCount + 1
                    if DEBUG == True:
                        print "Filter #%d: %s" % (pCount, phrase)
                    request = phrase.split('=')
                    
                    key = request[0]        #outer dict keys(filters) are text to the left of equal sign 
                    innerKey = request[1]   #inner dict keys(corresponding options) are text to the right of equal sign
        
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

        
        if DEBUG == True:
            print dictionary
            print
        print "Total search found: %d" % count + '\n'
        
        print "Search Summary:" + '\n'
        for keys in dictionary:
            print keys + ": " 
            for filters in dictionary[keys]:
                print "    " + filters + ": " + str(dictionary[keys][filters])
            print

        print "debug......"
        pdb.set_trace()

        with open('result.csv', 'a') as csvfile:
            excelwriter = csv.writer(csvfile, delimiter='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            excelwriter.writerow(['----------'])
            excelwriter.writerow([fname])
            for keys in dictionary:
                excelwriter.writerow([keys])
                for filters in dictionary[keys]:
                    excelwriter.writerow([filters, dictionary[keys][filters]])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', metavar='F', help='parse the log file')
    args = parser.parse_args()
    main(args)
