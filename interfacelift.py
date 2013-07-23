#!/usr/bin/python
import sys
import urllib2
import re
import commands

list_file = 'photos.txt'
curl_command = 'curl -# -L -O http://interfacelift.com%s -e "%s" -A "%s"'
sizes = [
    '1440x900',   # Macbook Pro
    '1024x1024',  # iPad 2
    '640x960',    # iPhone 4G
    '1440x1280'   # Android
]

# -- Changable Variables

 #Browse to the page that has all the wallpaper you want and paste here
url = ('http://interfacelift.com/wallpaper/downloads/date/widescreen/%s/'
       % sizes[0])

# -- Should not need to edit below here unless something stops working --

#Fake useragent since wget is blocked
useragent = ('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3)'
             ' Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729)')

# The regex pattern used to look up picture url paths
pattern = '(?<=<a href=")/wallpaper/.*jpg(?=">)'


def make_request(s_count):
    headers = {'User-Agent': useragent}
    request = urllib2.Request(url + "index" + str(s_count) + ".html",
                              None, headers)
    data = urllib2.urlopen(request).read()
    pictures = re.findall(pattern, data)
    urlcount = len(pictures)

    return request.get_full_url(), pictures


def main():
    # Get the list of photo IDs
    photo_list = sorted(sys.argv[1:], reverse=True)
    if len(photo_list) == 0:
        photo_list = sorted(open(list_file).read().split('\n'), reverse=True)

    count = 1
    refer, pictures = make_request(count)

    for photo_id in photo_list:
        photo_uri = [i for i in pictures if photo_id + '_' in i]

        # Load another page and find it if the photo's on the current page
        while len(photo_uri) != 1:
            count = count + 1
            refer, pictures = make_request(count)
            photo_uri = [i for i in pictures if photo_id + '_' in i]

        # Download all sizes for each requested photo
        for uri in [photo_uri[0].replace(sizes[0], i) for i in sizes]:
            command = curl_command % (uri, refer, useragent)
            status, output = commands.getstatusoutput(command)
            if status == 0:
                print "OK:", uri[uri.rfind('/') + 1:]
            else:
                print "FAIL:", output

if __name__ == '__main__':
    main()
