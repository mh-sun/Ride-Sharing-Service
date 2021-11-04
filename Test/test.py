import json

import redis


def format_string(s: str):
    s = str(s)
    s = s.lstrip('b').strip("'")
    return int(s)


def format_list(li: list):
    temp = []
    for i in li:
        temp.append(format_string(i))
    return temp


red = redis.Redis(host='localhost', port=6379)
red.set("BD", 'Dhaka')
red.delete('point')
temp = {
    'name': 'sun',
    'age': 23
}
red.rpush('point', json.dumps(temp))
red.rpush('point', 120)

# red.rpush('point', [1, 10])
x = (red.lrange('point', 0, -1))

print(x)
# import json
# test = {
#     'a':10,
#     'b':'hasan'
# }
# test = json.dumps(test)
# print(type(test))
# test = json.loads(test)
# print(test)
# print(type(test))
# print(type(test['a']))