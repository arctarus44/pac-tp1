import client as c
import time

key="a7940a90c5a663a2e45faaf6"
service="/kerberos/230.128.213.245"

if __name__ == '__main__':

	# Identification auprès de l'AS
	parameters = {'login': 'dewarumez'}
	credentials = c.server_query(c.BASE_URL + '/kerberos/AS', parameters)


	# Identification auprès du TGS
	tgs_key = c.enc(credentials['Client-TGS-key'], passphrase=key, decrypt=True)
	json_dic = { 'login' : 'dewarumez', 'timestamp' : time.time()}

	ticket = {'Ticket-Granting-Ticket' : credentials['Ticket-Granting-Ticket'],
		'server' : '230.128.213.245',
		'authenticator' : c.enc(c.json.dumps(json_dic), passphrase=tgs_key)}
	res = c.server_query(c.BASE_URL + '/kerberos/TGS', ticket)

	# Établissement de la confiance avec le service
	clt_srv_key = c.enc(res['Client-Server-key'], passphrase=tgs_key, decrypt=True)
	json_dic['timestamp'] = time.time()

	ticket = {'Client-to-Server-Ticket' : res['Client-to-Server-Ticket'],
		'authenticator' : c.enc(c.json.dumps(json_dic), passphrase=clt_srv_key)}

	res = c.server_query(c.BASE_URL + service, ticket)
	response = c.enc(res, passphrase=clt_srv_key, decrypt=True)
	response = eval(response)

	param = {'proof' : response['proof']}
	res = c.server_query(c.BASE_URL + '/kerberos/mission-accomplished', param)
	print(res['status'])
