from flask import Flask,render_template,url_for,request,redirect
import json
import time
import string
import random
app = Flask('app')
def create_note(title,author,content):
  data=json.loads(open('data.json').read())
  id="".join(random.choices(string.ascii_letters + string.digits, k = 20))
  data.insert(0,{"id":id,"title":title,"author":author,"time":time.asctime(time.gmtime(time.time())),"content":content})
  with open('data.json', 'w') as json_file:
    json.dump(data, json_file)
  return id
def get_note(id):
  data=json.loads(open('data.json').read())
  found_note={}
  for note in data:
    if note['id']==id:
      found_note=note
      break
  return found_note
@app.route('/')
def home_page():
  return render_template("index.html",data=json.loads(open('data.json').read()))
@app.route('/view/<id>')
def view_note(id):
  note=get_note(id)
  return render_template("view.html",title=note['title'],author=note['author'],time=note['time'],content=note['content'])
@app.route('/create',methods = ['POST', 'GET'])
def create_new_page():
  if request.method == 'POST':
    title = request.form['title']
    author = request.form['author']
    content = request.form['content']
    id=create_note(title,author,content)
    return redirect(url_for('view_note',id = id))
  else:
    return render_template('create.html')

app.run(host='0.0.0.0', port=8080,debug=True)