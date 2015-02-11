import client as c
import os

public_key = 'public-key'

name = "owczarek"
name_me = "dewarumez"
other_key = name + "_pkey.pem"
other_sign_key = name + "pkey.sign"
my_sign_key = "my_sign.key"
wot = "/web-of-trust/"
sign = wot + "sign/" + name_me
get = wot + "get/" + name
secret_key = "secret_key.pem"
sig_key = "openssl pkeyutl -sign -inkey {0} -in {1} | base64 > {2}"
# O -> privatekey
# 1 -> other key/stuff to sign
# 2 -> out


param_signer = "signer"
param_signature = "signature"
param_auth = "auth"

if __name__ == "__main__":

	# Téléchargement de la clé de la victime
	pkey = c.server_query(c.BASE_URL + get);

	file = open(other_key, 'w')
	file.write(pkey[public_key])
	file.close()

	# Signature de la clé de other
	os.system(sig_key.format(secret_key, other_key, other_sign_key))
	os.system("base64 " + other_sign_key + " > " + name + ".sign")

	Signature de la signature de ma clé
	os.system(sig_key.format(secret_key, my_sign_key, "tmp2.bin"))
	os.system("base64 tmp2.bin > tmp2.64")

	La signature de ma clé en base64
	os.system("base64 " + my_sign_key +" > " + my_sign_key + ".64")

	file1 = open(my_sign_key+".64", 'r')
	file2 = open("tmp2.64" , 'r')
	param = {param_signer : name,
			 param_signature : file1.read(),
			 param_auth : file2.read()}

	file1.close()
	file2.close()

	resp = c.server_query(c.BASE_URL + sign, param)
	print(resp)
