import json


data = {
1: {
"start": "toronto",
"end": "montreal",
"date": "12042022",
"price": "400",
"travel_time": "4 hours",
"layover": "no"
},
2: {
"start": "toronto",
"end": "calgary",
"date": '12052022',
"price": "600",
"travel_time": "3",
"layover": "1 hour"
},
3: {
"start": "new york",
"end": "toronto",
"date": '12082022',
"price": "500",
"travel_time": "3",
"layover": "50 minutes"
},
4: {
"start": "toronto",
"end": "edmonton",
"date": '12072022',
"price": "400",
"travel_time": "5 hours",
"layover": "1 hour"
},
5: {
"start": "toronto",
"end": "halifax",
"date": "12062022",
"price": "300",
"travel_time": "4 hours",
"layover": "30 minutes"
},
6: {
"start": "halifax",
"end": "calgary",
"date": '12092022',
"price": "600",
"travel_time": "3",
"layover": "1 hour"
},
7: {
"start": "new york",
"end": "dallas",
"date": '12042022',
"price": "700",
"travel_time": "3",
"layover": "50 minutes"
},
8: {
"start": "toronto",
"end": "thunderbay",
"date": '12072022',
"price": "250",
"travel_time": "1.5 hours",
"layover": "no"
},
9: {
"start": "huston",
"end": "montreal",
"date": "12092022",
"price": "450",
"travel_time": "5 hours",
"layover": "no"
},
10: {
"start": "toronto",
"end": "delhi",
"date": '12092022',
"price": "1600",
"travel_time": "23",
"layover": "5 hour"
},
11: {
"start": "new york",
"end": "london",
"date": '12082022',
"price": "1500",
"travel_time": "11",
"layover": "2 hours"
},
12: {
"start": "toronto",
"end": "st johns",
"date": '12102022',
"price": "800",
"travel_time": "5 hours",
"layover": "1 hour"
},
13: {
"start": "toronto",
"end": "montreal",
"date": "12052022",
"price": "350",
"travel_time": "5 hours",
"layover": "no"
},
14: {
"start": "toronto",
"end": "new york",
"date": "12072022",
"price": "250",
"travel_time": "9 hours",
"layover": "no"
},
15: {
"start": "toronto",
"end": "new york",
"date": "12082022",
"price": "800",
"travel_time": "2 hours",
"layover": "no"
},
16: {
"start": "toronto",
"end": "montreal",
"date": "12092022",
"price": "550",
"travel_time": "8 hours",
"layover": "no"
},
}


output = json.dumps(data)
print(output)

with open(".\\flights\\flights.txt", "w+") as f:
    f.write(output)

print("finish")
