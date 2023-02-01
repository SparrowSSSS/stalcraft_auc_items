import requests, json, http.client, os, time

while True:
    try:
        conn = http.client.HTTPSConnection("eapi.stalcraft.net")
        break
    except:
        print("---")
        print("breaking the connection...")
        print("---")

token = os.environ["TOKEN"]
headers = {
    'Content-Type': "application/json",
    'Authorization': f"Bearer {token}"
    }

for i in range(1, 3):
    if i == 1:
        type = "ru"
    else:
        type = "global"
    try:
        r = requests.get(f"https://raw.githubusercontent.com/EXBO-Studio/stalcraft-database/main/{type}/listing.json")
    except:
        print("---")
        print("breaking the connection...")
        print("---")
        continue
    data = json.loads(r.text)
    newData = []
    a = 0
    b = 0
    while a < len(data):
        try:
            conn.request("GET", f"/ru/auction/{data[a]['data'][-9: -5]}/history", headers=headers)
            res = conn.getresponse()
        except:
            print("---")
            print("breaking the connection...")
            print("---")
            continue
        d = json.loads(res.read().decode("utf-8"))
        print(a/len(data)*100)
        try:
            if d["total"] > 0:
                while True:
                    try:
                        response = requests.get(f"https://raw.githubusercontent.com/EXBO-Studio/stalcraft-database/main/{type}/{data[a]['data']}")
                        break
                    except:
                        print("---")
                        print("breaking the connection...")
                        print("---")
                        continue
                c = json.loads(response.text)
                newData.append({'data': "", 'icon': "", 'name_ru': "", 'name_en': "", 'id': "", 'one_category': "", 'two_category': "", 'category': ""})
                newData[b]['data'] = data[a]['data']
                newData[b]['icon'] = data[a]['icon']
                newData[b]['name_ru'] = data[a]['name']['lines']['ru']
                newData[b]['name_en'] = data[a]['name']['lines']['en']
                newData[b]['id'] = data[a]['data'][-9: -5]
                one_category = ""
                for i in range(len(c['category'])):
                    if c['category'][i] == "/":
                        one_category = c['category'][ : i]
                        two_category = c['category'][i+1 : ]
                if one_category != "":
                    newData[b]['one_category'] = one_category
                    newData[b]['two_category'] = two_category
                else:
                    newData[b]['one_category'] = c['category']
                newData[b]['category'] = c['category']
                b+=1
            a+=1
        except KeyError:
            print("---")
            print("wait")
            time.sleep(60)
            print("wait is over")
            print("---")
    with open(f"s_data_{type}.json", "w") as write_file:
        json.dump(newData, write_file, ensure_ascii=False)
        print("---")
        print(f"s_data_{type}.json is saved")
        print("---")