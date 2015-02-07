import client as c
import os
name = "dewarumez"
ex_url = "/encryption-101/ciphertext/" + name

if __name__ == "__main__":
	resp = c.server_query(c.BASE_URL + ex_url, None)
	file = open("test.txt", 'w')
	file.write(resp)
	file.close()
	os.system('openssl enc -aes-128-cbc -base64 -d -in test.txt -k "P4C rulzzz" > out')
	file_unc = open("out", 'r')
	msg = file_unc.read()
	file_unc.close()
	validation_tkn = msg[75:107]
	validtion_url = msg[148:173]
	param = {'token' : validation_tkn}
	resp = c.server_query(c.BASE_URL + validtion_url + name, param)
	os.system("rm test.txt out")
	print(resp['status'])
