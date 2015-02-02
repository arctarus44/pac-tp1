import client as c
import os

if __name__ == '__main__':
	file = open("my_pkey", 'r')

	d = {'public-key' : file.read()}

	resp = c.server_query(c.BASE_URL + "/public-key-101/query/dewarumez", d)
	file = open('./enc_resp', 'w')
	file.write(resp)
	file.close()
	os.system('base64 -d enc_resp > out')
	os.system('openssl rsautl -decrypt -in out -out unc_msg -inkey my_skey ')

	file = open("./unc_msg", 'r')
	end = {}

	print(file.read())
	print(c.BASE_URL);


	# print(c.BASE_URL + c.server_query(, end))
