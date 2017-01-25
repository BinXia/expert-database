# coding=UTF-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
from apps import dbconn


# Create your views here.
def PullComboInfo(request):
	try:
		database = dbconn()
		cursor = database.cursor()
		respondData = list()

		cursor.execute('SELECT DISTINCT {0} FROM experts'.format(request.GET['type']))
		data = cursor.fetchall()
		respondData = map(lambda x:x[0],data)
		cursor.close()
		database.close()

		message = json.dumps(respondData);
		response = HttpResponse(message,content_type='application/json');
		response['Access-Control-Allow-Origin'] = '*';
		return response;

	except Exception, e:
		print e
		response = HttpResponse(json.dumps({"msg":e}),content_type='application/json')
		response['Access-Control-Allow-Origin'] = '*'
		return response


@csrf_exempt
def ShowExpertList(request):
	try:
		respondData = dict()
		search = dict()
		start = 0
		length = 0
		order = dict()
		columns = list()

		# load request from front end
		for key,value in json.loads(request.body).items():
			if key == 'search':
				search = value
			elif key == 'draw':
				respondData['draw'] = int(value)
			elif key == 'start':
				start = int(value)
			elif key == 'length':
				length = int(value)
			elif key == 'order':
				order = value[0]
			elif key == 'columns':
				columns = value


		database = dbconn()
		cursor = database.cursor()

		# initialize expert list
		if len(search['value']) == 0:

			cursor.execute('SELECT * FROM experts ORDER BY CONVERT({0} USING gbk) {1}'.format(
				filter(lambda x:x['data']==order['column'],columns)[0]['name'],
				order['dir']
				)
			)

			data = cursor.fetchall()
			respondData['recordsTotal'] = len(data)
			respondData['recordsFiltered'] = len(data)
			respondData['data'] = list()
			for datum in data[start:start+length]:
				respondData['data'].append(list(datum))

		# search expert list
		else:
			cursor.execute('SELECT count(*) FROM experts')
			data = cursor.fetchall()
			respondData['recordsTotal'] = data[0]
			cursor.close()


			searchableCol = filter(lambda x:x['searchable']==True,columns)

			cursor = database.cursor()
			cursor.execute('SELECT * FROM experts WHERE CONCAT_WS(",",{0}) LIKE \'%{1}%\' ORDER BY CONVERT({2} USING gbk) {3}'.format(
				','.join(map(lambda x:x['name'],searchableCol)),
				search['value'].encode('UTF-8'),
				filter(lambda x:x['data']==order['column'],columns)[0]['name'],
				order['dir']
				)
			)

			data = cursor.fetchall()
			respondData['recordsFiltered'] = len(data)
			respondData['data'] = list()
			for datum in data:
				respondData['data'].append(list(datum))

		cursor.close()
		database.close()

		
		message = json.dumps(respondData)
		response = HttpResponse(message,content_type='application/json')
		response['Access-Control-Allow-Origin'] = '*'
		return response

	except Exception, e:
		print e
		response = HttpResponse(json.dumps({"msg":e}),content_type='application/json')
		response['Access-Control-Allow-Origin'] = '*'
		return response

@csrf_exempt
def InsertDatum(request):
	try:
		respondData = dict()
		datum = json.loads(request.body)

		# insert datum
		database = dbconn()
		cursor = database.cursor()

		cursor.execute('INSERT INTO experts VALUES (NULL,\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\')'.format(
			datum['name'].encode('UTF-8'),
			datum['code'].encode('UTF-8'),
			datum['phone'].encode('UTF-8'),
			datum['email'].encode('UTF-8'),
			datum['unit'].encode('UTF-8'),
			datum['duty'].encode('UTF-8'),
			datum['education'].encode('UTF-8'),
			datum['domain'].encode('UTF-8'),
			datum['remark'].encode('UTF-8')
			)
		)
		database.commit()

		respondData['msg'] = 'OK'

		cursor.close()
		database.close()


		message = json.dumps(respondData)
		response = HttpResponse(message,content_type='application/json')
		response['Access-Control-Allow-Origin'] = '*'
		return response

	except Exception, e:
		print e
		response = HttpResponse(json.dumps({"msg":e}),content_type='application/json')
		response['Access-Control-Allow-Origin'] = '*'
		return response





@csrf_exempt
def CorrectDatum(request):
	try:
		respondData = dict()
		datum = json.loads(request.body)

		# update data
		database = dbconn()
		cursor = database.cursor()

		cursor.execute('UPDATE experts SET \
			name=\'{1}\',\
			code=\'{2}\',\
			phone=\'{3}\',\
			email=\'{4}\',\
			unit=\'{5}\',\
			duty=\'{6}\',\
			education=\'{7}\',\
			domain=\'{8}\',\
			remark=\'{9}\'\
			WHERE id={0}'.format(
				datum['id'],
				datum['name'].encode('UTF-8'),
				datum['code'].encode('UTF-8'),
				datum['phone'].encode('UTF-8'),
				datum['email'].encode('UTF-8'),
				datum['unit'].encode('UTF-8'),
				datum['duty'].encode('UTF-8'),
				datum['education'].encode('UTF-8'),
				datum['domain'].encode('UTF-8'),
				datum['remark'].encode('UTF-8')
				)
			)

		database.commit()

		respondData['msg'] = 'OK'

		cursor.close()
		database.close()

		message = json.dumps(respondData)
		response = HttpResponse(message,content_type='application/json')
		response['Access-Control-Allow-Origin'] = '*'
		return response

	except Exception, e:
		print e
		response = HttpResponse(json.dumps({"msg":e}),content_type='application/json')
		response['Access-Control-Allow-Origin'] = '*'
		return response




@csrf_exempt
def DeleteDatum(request):
	try:
		respondData = dict()
		data_id = json.loads(request.body)

		# delete data
		database = dbconn()
		cursor = database.cursor()

		cursor.execute('DELETE FROM experts WHERE id IN ({0})'.format(
			','.join(map(str,data_id))
			)
		)

		database.commit()

		respondData['msg'] = 'OK'

		cursor.close()
		database.close()

		message = json.dumps(respondData)
		response = HttpResponse(message,content_type='application/json')
		response['Access-Control-Allow-Origin'] = '*'
		return response

	except Exception, e:
		print e
		response = HttpResponse(json.dumps({"msg":e}),content_type='application/json')
		response['Access-Control-Allow-Origin'] = '*'
		return response







