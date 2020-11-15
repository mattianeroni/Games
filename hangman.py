import random


word = random.choice (["bad boy", "swarm of bees", "birds flock", "elephant", "the day after tomorrow", "the end of the world", "pandemic",
		      "donald trump sucks", "obama rocks", "madonna", "elvis presley"])

get_letter = lambda i: i if i==" " else "_"

lifes = 8
printed_word = "".join(get_letter(i) for i in word)

while True:
	print("---------------------------")
	print(f"You still have {lifes} lifes")
	print("The word to guess:")
	print(printed_word)
	x = input("Guess the next letter: ")
	
	if x in word:
		print("Good job!")
		n = []
		for j, i in zip(printed_word, word):
			if i == x:
				n.append (i)
			else:
				n.append (j)
		printed_word = "".join(n)
	else:
		print("Error!")
		lifes -= 1
	
	if lifes <= 0:
		print("Sorry, you lost...")
		break

	if "_" not in printed_word:
		print("You won!!! Congratulations!")
		break


	print("\n\n\n")
