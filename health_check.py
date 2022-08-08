from flask import Flask
from threading import Thread

app = Flask('')

def health_check(client):

  @app.route('/')
  def home():
    return "Hello. I am alive!"

  @app.route('/test')
  def test():
    return "Hello from {}".format(client.user.name)

  def run():
    app.run(host='0.0.0.0',port=8080)


  t = Thread(target=run)
  t.start()