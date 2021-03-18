import os

for i in os.listdir('txt'):


	with open('txt/' + i, 'r') as f:

		lines = f.readlines()

		for j, l in enumerate(lines):
			l = l.strip()
			l = "|".join(l.split('|')[::-1])
			print("{}/{:04d}.mp3|{}".format(i[:-4],j,l.strip()))

			# break
	# break