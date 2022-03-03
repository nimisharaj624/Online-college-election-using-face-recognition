from flask import  Flask,Blueprint,render_template,request,redirect,url_for
from database import *
import uuid
import os
from core import *
public=Blueprint('public',__name__)

@public.route('/')
def home():
	return render_template("home.html")

@public.route('/login',methods=['get','post'])
def login():
	if 'login' in request.form:
		uname=request.form['username']
		pwd=request.form['password']
		q="select * from login1 where username='%s'  and password='%s'"%(uname,pwd)
		res=select(q)
		print(res)
		if res:
			if res[0]['user_type']=='admin':
				return redirect(url_for('admin.adminhome'))
			elif res[0]['user_type']=='staff':
				return redirect(url_for('staff.staffhome'))
			elif res[0]['user_type']=='student':
				return redirect(url_for('student.studenthome'))
	return render_template("login.html")

@public.route('/student_registration',methods=['get','post'])
def student_registration():
	if 'register' in request.form:
		registern=request.form['regno']
		firstname=request.form['fname']	
		lastname=request.form['lname']
		photo=request.files['photo']
		batch=request.form['batch']
		phn=request.form['phn']	
		email=request.form['email']	
		course=request.form['cname']
		uname=request.form['uname']
		pwd=request.form['pwd']
		path='static/'+str(uuid.uuid4())+photo.filename
		photo.save(path)
		q="select * from student inner join login1 using(login_id) where register_number='%s' or phone_number='%s' or email='%s' or username='%s' "%(registern,phn,email,uname)
		res=select(q)
		print(q)
		print(res)
		if res:
			flash("ALREADY REGISTERED")
			return redirect(url_for('public.student_registration'))
		else:

			
			q="insert into login1 values(NULL,'%s','%s','student')"%(uname,pwd)
			loginid=insert(q)
			q="insert into student values(NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(loginid,registern,firstname,lastname,path,course,batch,phn,email)
			id=insert(q)
			pid=str(id)
			isFile = os.path.isdir("static/trainimages/"+pid)  
			print(isFile)
			if(isFile==False):
				os.mkdir('static\\trainimages\\'+pid)
			image1=request.files['image1']
			path="static/trainimages/"+pid+"/"+str(uuid.uuid4())+image1.filename
			image1.save(path)

			image2=request.files['image2']
			path="static/trainimages/"+pid+"/"+str(uuid.uuid4())+image2.filename
			image2.save(path)

			image3=request.files['image3']
			path="static/trainimages/"+pid+"/"+str(uuid.uuid4())+image3.filename
			image3.save(path)
			enf("static/trainimages/")

	return render_template("student_registration.html")
	
		


@public.route('/staff_registration',methods=['get','post'])
def staff_registraion():
	if 'register' in request.form:
		firstname=request.form['fname']	
		lastname=request.form['lname']
		age=request.form['age']
		phn=request.form['phn']	
		email=request.form['email']	
		uname=request.form['uname']
		pwd=request.form['pwd']
		q="insert into login1 values(NULL,'%s','%s','staff')"%(uname,pwd)
		loginid=insert(q)
		q="insert into staff values(NULL,'%s','%s','%s','%s','%s','%s')"%(loginid,firstname,lastname,age,phn,email)
		insert(q)

	return render_template("staff_registration.html")

