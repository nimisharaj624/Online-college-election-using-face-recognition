from flask import *
from database import *
from core import *
import os
student=Blueprint('student',__name__)

@student.route('/studenthome')
def studenthome():
	return render_template('studenthome.html')

@student.route('/studentviewelection',methods=['get','post'])
def studentviewelection():
	data={}
	q="select * from election"
	res=select(q)
	data['election']=res
	return render_template('studentviewelection.html',data=data)

@student.route('/studentviewcandidates',methods=['get','post'])
def studentviewcandidates():
	data={}
	eid=request.args['eid']
	if "cid" in request.args:
		cid=request.args['cid']
		#s=val(vid,cids,eid)

	q="select * from categories"
	res=select(q)
	data['categ']=res
	

	q="SELECT * FROM candidates INNER JOIN election USING(election_id) INNER JOIN student USING(student_id) INNER JOIN `categories` USING(`category_id`) WHERE `election_id`='%s'"%(eid)
	print(q)
	res=select(q)
	data['candidates']=res

	if 'filter' in request.form:
		cat_id=request.form['cat_id']
		q="SELECT * FROM candidates INNER JOIN election USING(election_id) INNER JOIN student USING(student_id) INNER JOIN `categories` USING(`category_id`) WHERE `election_id`='%s' and category_id='%s'"%(eid,cat_id)
		res=select(q)
		data['candidates']=res
	return render_template('studentviewcandidates.html',data=data)

@student.route('/studentviewresult',methods=['get','post'])
def studentviewresult():
	eid=request.args['eid']
	data={}

	q="select * from categories"
	res=select(q)
	data['categ']=res

	q="SELECT * FROM results INNER JOIN election USING(election_id) INNER JOIN candidates USING(candidate_id) INNER JOIN `categories` USING(`category_id`) WHERE results.election_id='%s'"%(eid)
	print(q)
	res=select(q)
	data['results']=res

	if 'filter' in request.form:
		cat_id=request.form['cat_id']
		q="SELECT * FROM results INNER JOIN election USING(election_id) INNER JOIN candidates USING(candidate_id) INNER JOIN `categories` USING(`category_id`) WHERE results.election_id='%s' and category_id='%s'  ORDER BY `number of votes` DESC"%(eid,cat_id)
		print(q)
		res=select(q)
		data['results']=res
	return render_template('studentviewresult.html',data=data)



