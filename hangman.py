import random


word = random.choice (["soqquadro", "casa di cura", "hotel", "disinfestatore",
			"cimice", "specializzando di chimica", "mattia",
			"grassa", "gatta pelosa", "punghino",
			"bambino ritardato", "bambino super intelligente",
			"ratto di fogna", "elefante elegante","caravelle",
			"cristoforo colombo", "corona virus",
			"molly"])

get_letter = lambda i: i if i==" " else "_"

lifes = 8
printed_word = "".join(get_letter(i) for i in word)

while True:
	print("---------------------------")
	print(f"Hai ancora {lifes} vite")
	print("La parola da indovinare:")
	print(printed_word)
	x = input("Indovina la prossima lettera: ")
	
	if x in word:
		print("Giusto!")
		n = []
		for j, i in zip(printed_word, word):
			if i == x:
				n.append (i)
			else:
				n.append (j)
		printed_word = "".join(n)
	else:
		print("Errore!")
		lifes -= 1
	
	if lifes <= 0:
		print("Hai perso...")
		break

	if "_" not in printed_word:
		print("Hai vinto!!! Congratulazioni!")
		break


	print("\n\n\n")
