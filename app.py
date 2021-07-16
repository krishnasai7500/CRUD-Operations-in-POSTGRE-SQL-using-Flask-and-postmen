#app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask.json import jsonify
import psycopg2 #pip install psycopg2 
import psycopg2.extras
 
app = Flask(__name__)
#app.secret_key = "cairocoders-ednalan"
 
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "167303361"
try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    print("success")
except:
    print("Error")
 
@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM students;"
    #print(s)
    cur.execute(s) # Execute the SQL
    list_users = cur.fetchall()
    print(list_users)
    #print("1")
    #return render_template('index.html', list_users = list_users)
    return jsonify(list_users)
 
@app.route('/add_student', methods=['POST'])
def add_student():
    #print(request.form)
    req=request.json
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = req['fname']
        lname = req['lname']
        email = req['email']
        query='''INSERT INTO students (fname, lname, email) VALUES (%s,%s,%s);'''
        l=(fname,lname,email)
        cur.execute(query,l)
        conn.commit()
        return jsonify('Student Added successfully')

 
@app.route('/find/<string:id>', methods = ['POST', 'GET'])
def get_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('SELECT * FROM students WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return  jsonify(data)
 
@app.route('/update/<string:id>', methods=['POST'])
def update_student(id):
    req=request.json
    if request.method == 'POST':
        fname = req['fname']
        lname = req['lname']
        email = req['email']
         
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query="""UPDATE students SET fname = %s,lname = %s,email = %s WHERE id = %s;"""
        l=(str(fname), str(lname), str(email), str(id))
        cur.execute(query,l)
        
        conn.commit()
        return jsonify('Student updated Successfully')

@app.route('/delete/<string:id>')
def delete_student(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('DELETE FROM students WHERE id = {};'.format(id))
    conn.commit()
    
    return jsonify('Student Removed Successfully')
 
if __name__ == "__main__":
    app.run(port= 9000,debug=True)
