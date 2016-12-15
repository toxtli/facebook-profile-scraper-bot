# python batch.py -c ../../config/facebook-config.txt -u ../../data/list.txt

import sys
import json
import getopt
import urllib2
import ConfigParser
from FacebookProfile import FacebookProfile

def main(argv):
    filePath = ''
    configPath = ''
    opts, args = getopt.getopt(argv, "u:c:")
    if opts:
        for o, a in opts:
            if o == "-u":
                filePath = a
            if o == "-c":
                configPath = a
    if filePath and configPath:
        configObj = ConfigParser.ConfigParser()
        configObj.read(configPath)
        email = configObj.get('credentials', 'email')
        password = configObj.get('credentials', 'password')
    	facebook = FacebookProfile({'email':email, 'password':password})
        dataInput = urllib2.urlopen(filePath)
        users = facebook.extractProfiles(dataInput)
        print json.dumps(users)
    else:
        print 'No file path is provided.'

if __name__ == "__main__":
    main(sys.argv[1:])