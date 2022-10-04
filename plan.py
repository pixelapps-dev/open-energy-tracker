from mimetypes import guess_extension
import os
import requests
import json

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36', 'x-v': '1'}

def get_data(url):
    r = requests.get(url, headers=headers)
    response = r.json()

    return response

# https://stackoverflow.com/a/25851972/9389353
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

raw_file = open("brands/brands.json", "r")
brands = json.load(raw_file)
raw_file.close()

changed_product = 0

for file in os.listdir('brands/plans/'):
    id = file.replace(".json","")

    raw_file = open("brands/plans/"+file, "r")
    brand = json.load(raw_file)
    raw_file.close()

    if 'data' not in brand:
        continue

    folder = "brands/plan/" + id
    if not os.path.exists(folder):
        os.makedirs(folder)

    try:
        for plan in brand['data']['plans']:
            try:
                url = (brands[id]['publicBaseUri'].rstrip('/') + "/cds-au/v1/energy/plans/" + plan['planId'])

                response = get_data(url)

                skip_update = False

                try:
                    for file in os.listdir('brands/plan/' + id):
                        if file == (plan['planId'] + ".json"):
                            raw_file = open("brands/plan/"+id+"/"+file, "r")
                            response_compare = json.load(raw_file)
                            raw_file.close()
                            if ordered(response) == ordered(response_compare):
                                skip_update = True

                except Exception as e:
                    print(e)

                path = 'brands/plan/' + id + "/" + plan['planId'] + ".json"

                if (skip_update == False):
                    raw_file = open(path, "w")
                    json.dump(response, raw_file, indent = 4)
                    raw_file.close()

                print(path)

            except Exception as e:
                print(e)

    except Exception as e:
        print(e)

for root, dirs, files in os.walk("brands/plan/"):
    for file in files:
        try:
            brand = root.split("/")[2]
            id = os.path.splitext(file)[0]

            raw_file = open("brands/plans/"+brand+".json", "r")
            plans = json.load(raw_file)
            raw_file.close()

            if 'data' not in plans or 'plans' not in plans['data']:
                continue

            found = False

            for plan in plans['data']['plans']:
                print(plan['planId'])
                if plan['planId'] == id:
                    found = True
            
            if found is False:
                path = "brands/plan/" + brand + "/" + file
                os.remove(path)
                changed_product += 1

        except Exception as e:
            print(e)