import sys
import http.client
import json
import re

is_latitude = False
is_longitude = False

is_coordinates = False
res_data = []

la = ""
lo = ""


def parse_wiki(city):
    global la
    global lo

    # connection = http.client.HTTPConnection('en.wikipedia.org', 80)
    # connection.request("GET", "/wiki/" + city)

    connection = http.client.HTTPSConnection("en.wikipedia.org")
    connection.request("GET", "/wiki/" + city)

    # Clear values:
    la = ""
    lo = ""

    # try:
    response = connection.getresponse()
    # except httplib.ResponseNotReady:
    #     return -1

    if response.status != 200:
        print(city + ': Page not found.')
        return -1

    # Some encodings trigger UnicodeDecodeError on feed()
    page = response.read().decode('utf-8')

    # TODO get data==========================================================================================
    # REGEX
    la = re.search('latitude">..........</span', page)
    lo = re.search('longitude">..........</span', page)
    la = la.group(0).split(">")[1].split("<")[0]
    lo = lo.group(0).split(">")[1].split("<")[0]

    # TODO get data==========================================================================================

    connection.close()

    if la == "" or lo == "":
        print(city + ": No coordinates found on this page")
        return -1

    return {
        'name': city,
        'la': la,
        'lo': lo,
    }


# Try getting command line argument, if none - ask for input:
# file_name = ""
# try:
#     file_name = sys.argv[1]
# except IndexError:
#     file_name = input('Please input file name: ')
file_name = "in.json" # tmp

# Read input .json file:
try:
    with open(file_name) as data_file:
        city_names = json.load(data_file)
except IOError:
    print("Couldn't parse the file")
    quit(1)

output_file = open('out.json', 'w')
output_data = []
# Write output:
for index in range(len(city_names)):
    try :
        result = parse_wiki(city_names[index]["name"])
        if result != -1:
            output_data.append(result)
            print(result['name'] + ": " + result['la'] + ", " + result['lo'])
    except AttributeError:
        print("nope")

json.dump(output_data, output_file, indent=4, sort_keys=True, ensure_ascii=True)

output_file.close()
