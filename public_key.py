import client as c
import os

name = "dewarumez"
pkey_srv_f = 'srv_public.key'
my_skey_f = "my_secret.key"
my_pkey_f = "my_public.key"
get_pk = "/public-key-101/get-PK"
submit_pk ="/public-key-101/submit/" + name
query_pk = "/public-key-101/query/" + name
enc_msg_f = "encrypted_msg"
unc_msg = "Hi, how are you?"
tmp = "tmp"
out = "out"

if __name__ == '__main__':

	#############
	# Section 1 #
	#############
	print("*** Section 1 ***")
	resp = c.server_query(c.BASE_URL + get_pk)

	pkey_srv = open(pkey_srv_f, 'w')
	pkey_srv.write(resp)
	pkey_srv.close()

	os.system("echo -n \"" + unc_msg + "\" | openssl pkeyutl -encrypt -pubin -inkey " + pkey_srv_f + " | base64  > " + enc_msg_f)

	file = open(enc_msg_f, 'r')
	param = {"ciphertext" : file.read()}
	file.close()

	resp = c.server_query(c.BASE_URL + submit_pk, param)

	print(resp['my-status'])
	print(resp['status'])

	os.system("rm " + pkey_srv_f + " " + enc_msg_f)

	#############
	# Section 2 #
	#############
	print("\n*** Section 2 ***")
	print("Génération de la clé privé")
	os.system("openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 > " + my_skey_f)

	print("Génération de la clé public")
	os.system("openssl pkey -in " + my_skey_f + " -pubout > " + my_pkey_f)

	file = open(my_pkey_f, 'r')
	del(param)
	param = {'public-key' : file.read()}
	file.close()

	resp = c.server_query(c.BASE_URL + query_pk, param)
	file = open(enc_msg_f, 'w')
	file.write(resp)
	file.close()

	os.system('base64 -d ' + enc_msg_f + " > " + tmp)
	os.system("openssl rsautl -decrypt -in " + tmp + " -out " + out + " -inkey " + my_skey_f)

	file = open(out, 'r')
	resp = c.server_query(c.BASE_URL + file.read())
	file.close()

	print(resp['comment'])
	print(resp['status'])
	os.system("rm " + my_skey_f + " " + my_pkey_f + " " + tmp + " " + out)
