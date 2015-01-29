import client as c

if __name__ == '__main__':
	file = open("my_pkey", 'r')

	d = {'public-key' : file.read()}

	resp = c.server_query(c.BASE_URL + "/public-key-101/query/dewarumez", d)
	file = open('./enc_resp', 'w')
	file.write(resp)
	file.close()
