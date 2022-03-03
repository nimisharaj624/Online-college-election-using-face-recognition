from flask import *
from database import *
staff=Blueprint('staff',__name__)

@staff.route('/staffhome')
def staffhome():
	return render_template('staffhome.html')

@staff.route('/staffmanage_category',methods=['get','post'])
def staffmanage_category():
	data={}
	q="select * from categories"
	res=select(q)
	data['category']=res

	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None
	if action=="delete":
		q="delete from categories where category_id='%s'"%(id)
		delete(q)
		return redirect(url_for('staff.staffmanage_category'))
	if action=="update":
		q="select * from categories where category_id='%s'"%(id)
		res=select(q)
		data['cat']=res
	if 'update' in request.form:
		category=request.form['category']
		q="update categories set category_name='%s' where category_id='%s'"%(category,id)
		update(q)
		return redirect(url_for('staff.staffmanage_category'))


	if 'submit' in request.form:
		category=request.form['category']
		q="insert categories values(null,'%s')"%(category)
		insert(q)
		return redirect(url_for('staff.staffmanage_category'))
	return render_template('staffmanage_category.html',data=data)

@staff.route('/staffviewelection',methods=['get','post'])
def staffviewelection():
	data={}
	q="select * from election"
	res=select(q)
	data['election']=res
	return render_template('staffviewelection.html',data=data)

@staff.route('/staffviewcandidates',methods=['get','post'])
def staffviewcandidates():
	data={}
	q="select * from candidates inner join election using(election_id) inner join student using(student_id)"
	res=select(q)
	data['candidates']=res
	return render_template('staffviewcandidates.html',data=data)

@staff.route('/staffviewresult',methods=['get','post'])
def staffviewresult():
	eid=request.args['eid']
	data={}
	q="SELECT * FROM results INNER JOIN election USING(election_id) INNER JOIN candidates USING(candidate_id) WHERE results.election_id='%s'"%(eid)
	res=select(q)
	data['results']=res
	return render_template('staffviewresult.html',data=data)


@staff.route('/staff_manage_candidates',methods=['get','post'])
def staff_manage_candidates():
	eid=request.args['eid']
	data={}
	data['eid']=eid
	
	q="select * from student"
	res=select(q)
	data['stud']=res

	q="select * from categories"
	res=select(q)
	data['categ']=res

	q="select * from candidates inner join election using(election_id) inner join student using(student_id) INNER JOIN `categories` USING(`category_id`)"
	res=select(q)
	data['candidates']=res
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None
	if action=="delete":
		q="delete from candidates where candidate_id='%s'"%(id)
		delete(q)
		return redirect(url_for('staff.staff_manage_candidates',eid=eid))

	if action=="update":
		q="select * from candidates where candidate_id='%s'"%(id)
		res=select(q)
		data['candi']=res
	if 'update' in request.form:
		sname=request.form['sname']

		q="update candidates set student_id='%s' where candidate_id='%s'"%(sname,id)
		update(q)
		return redirect(url_for('staff.staff_manage_candidates',eid=eid))



	if 'submit' in request.form:
		sname=request.form['sname']
		cat_id=request.form['cat_id']
		q="insert into candidates values(NULL,'%s','%s','%s','pending')"%(sname,eid,cat_id)
		insert(q)
		return redirect(url_for('staff.staff_manage_candidates',eid=eid))
	return render_template('staff_manage_candidates.html',data=data)