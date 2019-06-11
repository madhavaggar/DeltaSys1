from flask import Flask
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'madhav'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/createtable')
def createtable():
    conn=mysql.connect()
    cur=conn.cursor()
    
    #creating nodes and requests table
    
    cur.execute(''' CREATE TABLE nodes (
                    Name VARCHAR(100),
                    CPU_Number INT, 
                    Available_CPU INT, 
                    Memory_Size INT, 
                    Available_Memory INT)''')
    cur.execute('''CREATE TABLE Requests (
                   Id INT, 
                   allocated_node_name VARCHAR(100), 
                   Starttime TIME, 
                   CPU_required INT, 
                   Memory INT, 
                   completion_time TIME)''')
    
    #adding four values manually into nodes
    
    cur.execute('''INSERT INTO nodes                     
                   VALUES('Node1',20,5,1000,400)''')
    cur.execute('''INSERT INTO nodes
                   VALUES('Node2',50,10,10000,2000)''')
    cur.execute('''INSERT INTO nodes
                   VALUES('Node3',27,10,3000,1200)''')
    cur.execute('''INSERT INTO nodes
                   VALUES('Node4',100,30,10000,3300)''')

if __name__=="__main__":
	app.run() 
