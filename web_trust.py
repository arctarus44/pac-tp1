import client as c
import os

name = "dewarumez"
wot_param = "/web-of-trust/ecdsa-parameters.pem"
wot_put = "/web-of-trust/put/" + name
param_file = "ecda-parameters.pem"
secret_ecdsa = "secret_key.pem"
public_ecdsa = "public_key.pem"
auth = "auth"
sign64 = "sign.64"
gen_secret_ecdsa_key = "openssl genpkey -paramfile " + param_file + " -out " + secret_ecdsa
gen_public_ecdsa_key = "openssl pkey -in " + secret_ecdsa + " -pubout -out " + public_ecdsa
sig_public_ecdsa_key = "openssl pkeyutl -sign  -inkey " + secret_ecdsa + " -in " + public_ecdsa + " | base64 > " + sign64

param_pub_key = "public-key"

if __name__ == "__main__":

	# todo delete param_file public_ecdsa

	# Récupération du jeu de paramêtre ECDSA
	param = c.server_query(c.BASE_URL + wot_param)

	file = open(param_file, 'w')
	file.write(param)
	file.close()

	# Génération d'une clé privée ECDSA
	os.system(gen_secret_ecdsa_key)

	# Génération d'une clé public ECDSA
	os.system(gen_public_ecdsa_key)

	# Génération de la signature de la clé public
	os.system(sig_public_ecdsa_key)

	# Ajout de la clé public dans le parametre
	file = open(public_ecdsa, 'r')
	param = {param_pub_key : file.read()}
	file.close()

	# Ajout de la signature de la clé public dans le parametre
	file = open(sign64, 'r')
	param[auth] = file.read()
	file.close()

	# # Téléversement de la la clé et de sa signature
	print("Téléversement de la clé public et de sa signature")
	resp = c.server_query(c.BASE_URL + wot_put, param)
	print(resp)
