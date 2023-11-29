import json
import sqlite3
from threading import Thread
from flask import Flask
from peewee import *


app = Flask('')



@app.route('/')
def home():
  return "I'm alive"


@app.route('/new-user')
def new_user():
  with open("users.json",'r+') as file:
    data = file.read()
    data = json.loads(data)
    users_list = data["data"]
    ids_list = []
    id = 0
    for user in users_list:
        ids_list.append(user["id"])
    if len(users_list) == 0:
        return "0"
    else:
        for i in range(0,max(ids_list)):
            if i not in ids_list:
                return str(i)
    id =  max(ids_list)+1
    user = {
      "id": id,
      "entries" :[]
    }
    users_list.append(user)
    data["data"]  = users_list
    file.seek(0)
    file.write(json.dumps(data))
    return id


@app.route('/get-entries/<id>')
def get_entries(id):
  with open("users.json",'r+') as file:
    data = file.read()
    data = json.loads(data)
    users_list = data["data"]
    user = None
    for u in users_list:
      if u["id"] == int(id):
        user = u
    if user is None:
      return "User not found"
    else:
      return json.dumps(user["entries"])

@app.route('/set-entries/<id>/<entries>')
def set_entries(id,entries_json):
  with open("users.json",'r+') as file:
    data = file.read()
    data = json.loads(data)
    users_list = data["data"]
    user = None
    for u in users_list:
      if u["id"] == int(id):
        user = u
    if user is None:
      return "User not found"
    else:
      entries = json.loads(entries_json)
      user["entries"] = entries
      users_list
      data["data"]  = users_list
      file.seek(0)
      file.write
  return "OK"




@app.route('/getfieldsbysport/<sport>')
def get_football(sport):
  try:
  
    conn = sqlite3.connect('database1.db')
    cursor = conn.cursor()
    cursor.execute("SELECT court_name, pos_x, pos_y FROM "+sport)
    conn.commit()
    courts_from_db = cursor.fetchall()
    courts = []
    
    for court_db in courts_from_db:
      court = {}
      court["name"] = court_db[0]
      court["lat"] = court_db[1]
      court["lon"] = court_db[2]
      
      courts.append(court)
    data ={}
    data["data"] = courts
    return json.dumps(data)
  except:
    return "error, no sport found"



def run():
  app.run(host='0.0.0.0', port=80)

def keep_alive():
  t = Thread(target=run)
  t.start()


if __name__ == "__main__":
  keep_alive()














