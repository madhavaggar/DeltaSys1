import requests
import random
import datetime 

memory=random.randint(1,10000)
hrs=random.randint(0,10)
minutes=random.randint(0,59)
sec=random.randint(0,59)
cpu=random.randint(1,20)
id1=random.randint(1,100)
time=str(hrs)+":"+str(minutes) + ":" + str(sec)
t=datetime.datetime.now()
st=str(t.strftime("%X"))

req={ 'mem_needed': str(memory),
       'time_needed':time,
       'cpu_needed':str(cpu), 
       'id':str(id1),
       'start_time':st}
r=requests.post("http://localhost:5000/loadbalancer",data=req)
