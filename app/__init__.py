from flask import Flask,render_template,request
from flaskext.mysql import MySQL
import datetime
 
# connecting to sql
mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'madhav'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/loadbalancer', methods=["GET","POST"])  #load balancer website
def index():
    mem_need=request.args.get('mem_needed')    #checking suitable node for the request
    time_need=request.args.get('time_needed')
    cpu_need=request.args.get('cpu_needed')
    id_no=request.args.get('id')
    start=request.args.get('start_time')
    conn=mysql.connect()
    cur=conn.cursor()
    x=datetime.datetime.now()
    t=x.strftime("%X")
    cur.execute("SELECT * FROM nodes")
    data=cur.fetchall()

    for d in data:

        if d[2]>=int(cpu_need) and d[4]>=int(mem_need):  #checking suitable node
            temp1=d[2]-int(cpu_need)
            temp2=d[4]-int(mem_need)
            cur.execute('''UPDATE nodes  
                           SET Available_CPU=%s , Available_Memory=%s
                           WHERE Name=%s''',(temp1,temp2,d[0]))
                           
            cur.execute("INSERT INTO requests VALUES(%s,%s,%s,%s,%s,%s)",(int(id_no),d[0],
                        start,int(cpu_need),int(mem_need),time_need))
            conn.commit()
            return "succesfully added to  " + d[0]  #returning success message
    
    return "Can't handle requests!"


@app.route('/<nodename>')   #webpages for four nodes
def process(nodename):
    
    
    def compare(str1,str2,str3):  #function to find whether a process is complete
        x=str1.split(":")
        y=str2.split(":")
        z=str3.split(":")
        j=0
        temp=[0,0,0]
    
        for i in x:
            temp[j]=int(i)+int(y[j])
            j=j+1
           
        if(temp[0]<int(z[0])):
            return 1
        
        elif(temp[1]<int(z[1])):
            return 1            
        
        elif(temp[2]<int(z[2])):
            return 1
        else:
            return 0
   
    datanow=[]
    history=[]
    x=datetime.datetime.now()
    t=str(x.strftime("%X")) 
    conn=mysql.connect()
    cur=conn.cursor()
    cur.execute("SELECT Id,Starttime,completion_time FROM requests WHERE allocated_node_name='"+nodename+"'")
    data=cur.fetchall()
    if data is None:
        return "No process currently running"
    else:
        for d in data:
            a=compare(str(d[1]),str(d[2]),t)
            if a==1:
                history.append(d)
            else:
                datanow.append(d)
        return render_template("delta.html",nodename=nodename,data=datanow,history=history)

    
if __name__=="__main__":
app.run() 
