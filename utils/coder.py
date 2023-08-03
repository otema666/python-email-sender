import base64

def codear(texto, veces):
	for a in range(veces):
		coded = base64.b64encode(texto.encode('utf-8')).decode('utf-8')
		texto = coded
	return coded

def descodear(texto, veces):
	for a in range(veces):
		decoded = base64.b64decode(texto).decode('utf-8')
		texto = decoded
	return decoded

def main():
	var = str(input("Cadena: "))
	num = int(input("Numero de veces: "))
	cod = int(input("1. Encode\n2. Decode\n"))
	if cod == 1:
		print(codear(var, num))
	elif cod == 2:
		print(descodear(var, num))

if __name__ == '__main__':
	main()