import re
import gzip
import urllib
import pdb
import argparse

def main(args):
    if args.filename:
    
        f = gzip.open(args.filename)
        #f = gzip.open('access_log.20130529.gz')
        #newfile = open('result.txt', 'w')
        #newfile2 = open('phrases.txt', 'w')
        regex = re.compile('\/search\/\?')
        count = 0
        pCount = 0
        dictionary = {}
            
            
        for line in f:
            search_terms = re.search(regex, line)
            if search_terms:
         #       pdb.set_trace()
        
                count = count + 1
         #       print count, line    #print the entire log line
                
                line = urllib.unquote(line) #decode URL
         #       print line
         #       newfile.write(line)
            
            
                pCount = 0
                phrases = line.split('&')   #split the line by different request components
               # print phrases[0]
                firstLine = phrases[0].split('?')   #strip the stuff before question mark
               # print firstLine[1]
                phrases[0] = firstLine[1]
            
                length = len(phrases)
               # print phrases[length - 1]
                lastLine = phrases[length - 1].split('HTTP')
               # print lastLine[0]
                phrases[length - 1] = lastLine[0]
                for phrase in phrases:
                    pCount = pCount + 1
         #           print pCount, phrase
                    request = phrase.split('=')
                    
                    key = request[0]
                   # print request[0]
                    innerKey = request[1]
                   # print request[1]
        
                    if key.startswith('extended_info'):
                        key = key[14:]
                    
                    if key in dictionary:
                        if innerKey in dictionary[key]:
                            dictionary[key][innerKey] += 1
         #                   print "innerkey exists: " + str(dictionary[key][innerKey])
                        else:
                            dictionary[key][innerKey] = 1
         #                   print "create new innerKey: " + str(dictionary[key][innerKey])
                    else:
                        
                        dictionary[key] = {innerKey: 1}
         #               print "create new key: " + str(dictionary[key][innerKey])
        
         #       print '\n'
        
        if 'center_latitude' in dictionary:
            del dictionary['center_latitude']
        if 'center_longitude' in dictionary:
            del dictionary['center_longitude']
        if 'distance' in dictionary:
            del dictionary['distance']
        if 'limit' in dictionary:
            del dictionary['limit']
        
        print dictionary
        print 'Total search found:', count
        
        print "Search Summary:" + '\n'
        for keys in dictionary:
            print keys + ": " 
            for filters in dictionary[keys]:
                print "    " + filters + ": " + str(dictionary[keys][filters])
            print

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', metavar='F', help='parse the log file')
    args = parser.parse_args()
    main(args)
