from flask import Flask, request, render_template
from cassandra.cluster import Cluster
import os
import socket
def cassandra_connection():
	"""
	Connection object for Cassandra
	:return: session, cluster
	"""
	cluster = Cluster(['cassandrai'],port=9042)
	session = cluster.connect()
	session.execute("""CREATE KEYSPACE IF NOT EXISTS quantiphi WITH REPLICATION={'class':'SimpleStrategy','replication_factor':1} AND durable_writes='true' """)
	session.set_keyspace('quantiphi')
	session.execute("create table if not exists employee(id int primary key,name text,address text)")
	return session,cluster


#init app
app=Flask(__name__)

session,cluster=cassandra_connection()
print('connection successfull ---------------- SUCCCCCEEEEEEEEEEEEEEEEEEEEESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
@app.route("/")
def pri():
	return render_template("employee.html",title="employee registration")


@app.route("/register",methods=["POST"])
def register():
	idd=request.form["idd"]
	name=request.form["name"]
	address=request.form["address"]
	try:
		print(idd,name,address)
		hostname = socket.gethostname()    
		IPAddr = socket.gethostbyname(hostname) 
		session.execute("insert into employee(id,name,address) values({},'{}','{}')".format(idd,name,address))
		return 'written successfull {}----{}'.format(hostname,IPAddr)
	except Exception as e:
		return e


if __name__=="__main__":
	app.run(host='0.0.0.0',port=5001,debug = True)
