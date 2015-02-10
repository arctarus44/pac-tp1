import client as c
import os
import random

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

pk_validate = "/public-key-101/validate"
hybrid = "/public-key-101/hybrid/" + name
sessionKey_f = "session.key"
cipher64_f = "cipher.64"
cipherBin_f = "cipher.bin"
plainttext_f = "msg.txt"
new_pass = "0x15c4bc87ac942353f6973816945515e9"

if __name__ == '__main__':

	#############
	# Section 1 #
	#############
	print("*** Section 1 ***")
	resp = c.server_query(c.BASE_URL + get_pk)

	print(resp);
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

	os.system("rm " + enc_msg_f)

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
	del(param)
	os.system("rm " + tmp + " " + out)

	#############
	# Section 3 #
	#############
	print("*** Section 3 ***")

	# envoie de la clé publique
	file = open(my_pkey_f, 'r')
	param = {'public-key' : file.read()}
	file.close()
	resp = c.server_query(c.BASE_URL + hybrid, param)
	session_key = resp['session-key']
	cipher_64 = resp['ciphertext']

	file = open(tmp, 'w')
	file.write(session_key);
	file.close()

	# Je récupère la clé de session (symétrique)
	os.system('base64 -d ' + tmp + " > " + out)
	os.system("openssl rsautl -decrypt -in " + out + " -out " + sessionKey_f + " -inkey " + my_skey_f)

	file = open(sessionKey_f, 'r')
	passwd = file.read()
	file.close()

	decrypt_msg = c.enc(cipher_64, passphrase=passwd, base64=True, decrypt=True)
	print("message déchiffré " + decrypt_msg)

	#############################
	# Préparation de la réponse #
	#############################
	del(param)
	msg = decrypt_msg[30:93]
	url = decrypt_msg[106:130]

	# chiffremet du message à envoyer avec une clé secrete
	nw_session_key = "0x92d239d867dce0c61d30111fceeb0eec" # générer avec "tr -dc a-f0-9 < /dev/urandom | head -c 32"
	msg_to_send = c.enc(msg, passphrase=nw_session_key)

	# chiffrement du message
	file = open("nw_session.key", 'w')
	file.write(nw_session_key)
	file.close()
	print("echo "+ nw_session_key + " | openssl pkeyutl -encrypt -pubin -inkey srv_public.key -out nw_msg.bin")
	os.system("echo "+ nw_session_key + " | openssl pkeyutl -encrypt -pubin -inkey srv_public.key -out nw_msg.bin")
	print("base64 nw_msg.bin > nw_msg.64")
	os.system("base64 nw_msg.bin > nw_msg.64")

	file = open("nw_msg.64", 'r')

	param = {"session-key" : file.read(), 'ciphertext' : msg_to_send}

	print("session = " +param['session-key'])
	print("ciphertex = " +param['ciphertext'])

	resp = c.server_query(c.BASE_URL + pk_validate, param)
	print(resp)
