from flask import *
from database import *

admin=Blueprint('admin',__name__)

@admin.route('/adminhome')
def adminhome():
	return render_template('adminhome.html')

@admin.route('/adminmanage_election',methods=['get','post'])
def adminmanage_election():

	data={}
	if 'manage' in request.form:
		title=request.form['title']
		date=request.form['edate']
		q="insert into election values(NULL,'%s','%s','pending')"%(title,date)
		insert(q) 

	q="select * from election"
	res=select(q)
	data['election']=res

	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None

	if action=="delete":
		q="delete from election where election_id='%s'"%(id)
		delete(q)
		return redirect(url_for('admin.adminmanage_election'))

	if action=="update":
		q="select * from election where election_id='%s'"%(id)
		res=select(q)
		data['ele']=res
	if 'update' in request.form:
		title=request.form['title']
		date=request.form['edate']
		q="update election set title='%s',election_date='%s' where election_id='%s'"%(title,date,id)
		update(q)
		return redirect(url_for('admin.adminmanage_election'))

	if 'action1' in request.args:
		action1=request.args['action1']
		eid=request.args['eid']
	else:
	 action1=None
	if action1=="start":
		q="update election set voting_status='start' where election_id='%s'"%(eid)
		update(q)
		return redirect(url_for('admin.adminmanage_election'))
	if action1=="stop":
		q="update election set voting_status='stop' where election_id='%s'"%(eid)
		update(q)
		return redirect(url_for('admin.adminmanage_election'))


	return render_template('adminmanage_election.html',data=data)


@admin.route('/adminviewstudent',methods=['get','post'])
def adminviewstudent():
	data={}

	q="select * from student"
	res=select(q)
	data['st']=res
		
	return render_template('adminviewstudent.html',data=data)

@admin.route('/adminpublishresult',methods=['get','post'])
def adminpublishresult():
	data={}
	eid=request.args['eid']
	q="select * from candidates inner join student using(student_id)"
	res=select(q)
	data['candid']=res

	q="SELECT * FROM results INNER JOIN election USING(election_id) INNER JOIN candidates USING(candidate_id) WHERE results.election_id='%s'"%(eid)
	res=select(q)
	data['results']=res


	if 'submit' in request.form:
		candidate=request.form['candidate']
		votes=request.form['votes']
		q="insert into results values(null,'%s','%s','%s')"%(eid,candidate,votes)
		insert(q)
		return redirect(url_for('admin.adminpublishresult',eid=eid))
	return render_template('adminpublishresult.html',data=data)



