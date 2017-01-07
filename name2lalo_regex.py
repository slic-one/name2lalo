import sys
import http.client
import json
import re
import codecs


class ParseError(Exception):
    def __init__(self, message):
        self.message = message


def parse_wiki(city):

    connection = http.client.HTTPSConnection("en.wikipedia.org")
    connection.request("GET", "/wiki/" + city)

    response = connection.getresponse()

    if response.status != 200:
        print(city + ': Page not found.')
        return -1

    # Some encodings trigger UnicodeDecodeError on feed()
    page = response.read().decode('utf-8')

    # REGEX
    la = re.search('latitude">.{8,12}</span', page)
    lo = re.search('longitude">.{8,12}</span', page)

    connection.close()

    if la is not None:
        la = la.group(0).split(">")[1].split("<")[0]
        lo = lo.group(0).split(">")[1].split("<")[0]
        return {
            'name': city,
            'la': la,
            'lo': lo,
        }
    else:
        print(city + ": No coordinates found on this page.")
        return -1


# Try getting command line argument, if none - ask for input:
file_name = ""
try:
    file_name = sys.argv[1]
except IndexError:
    file_name = input('Input file name: ')
# file_name = "in.json" # tmp

# Read input .json file:
try:
    with open(file_name) as data_file:
        city_names = json.load(data_file)
except IOError:
    print("Couldn't parse the file")
    quit(1)

try:
    output_file = sys.argv[1]
except IndexError:
    output_file = input('Output file name: ')

output_data = []
# Write output:
for index in range(len(city_names)):
    result = parse_wiki(city_names[index]["name"])
    if result != -1:
        output_data.append(result)
        print(result['name'] + ": " + result['la'] + ", " + result['lo'])

with codecs.open(output_file, 'w', encoding='utf-8') as output:
    json.dump(output_data, output, indent=4, sort_keys=True, ensure_ascii=False)
