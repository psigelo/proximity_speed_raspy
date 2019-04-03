import json
import tornado.ioloop
import tornado.web
from sql import insert_to_sql
from datetime import datetime as dt
mac = "E817557FE91B"

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
                    try:
                        insert_to_sql(int(js["rssi"]),sensId,beamId,js["timestamp"])
                    except Exception as e:
                        print("exception:",e)
        except Exception as e:
            print("exception:",e)

application = tornado.web.Application([
    (r"/", Hello),
    (r"/post", Post),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()