import json
import tornado.ioloop
import tornado.web
from sql import insert_to_sql
from datetime import datetime as dt

allowed_beacons = ['E7DEEF8685B7', 'D4E16B84153D', 'EE6630AB3C8D', 'C4712E94C47B', 'E82573E39FF2']

class Hello(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class Post(tornado.web.RequestHandler):

    def get(self):
        form = """<form method="post">
        <input type="text" name="username"/>
        <input type="text" name="designation"/>
        <input type="submit"/>
        </form>"""
        self.write(form)

    def post(self):
        try:
            my_json = self.request.body.decode('utf8').replace("'", '"')
            my_json = json.loads(my_json)
            beamId = ""
            for js in my_json:
                if js["type"] == 'Gateway':
                    beamId = js["mac"]
                else:
                    js["timestamp"] = dt.strptime(
                        js["timestamp"], '%Y-%m-%dT%H:%M:%SZ')

                    sensId = js["mac"]
                    if sensId not in allowed_beacons:
                        continue
                    print('data',js)
                    try:
                        insert_to_sql(int(js["rssi"]),sensId,beamId,js["timestamp"],js["ibeaconUuid"],js["ibeaconMajor"],js["ibeaconMinor"])
                    except Exception as e:
                        print("exception:",e)
        except Exception as e:
            print("exception:",e)

application = tornado.web.Application([
    (r"/", Hello),
    (r"/status", Post),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
