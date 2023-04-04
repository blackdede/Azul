import os.path
from upemtk import *
from random import *


def sauvegarder_partie():
	flux = open('Sauvegarde.txt', 'w')
	flux.write(str(gamemode) + '\n')
	flux.write(str(tour_joueur) + '\n')

	# Sacs
	for i in range(len(all_lst_filled)):
		flux.write(str(i) + '\n')
		for lst_sec in all_lst_filled[i]:
			flux.write(lst_sec + '\n')
	flux.write('X\n')

	# Malus
	for i in range(len(lst_malus)):
		flux.write(str(i) + '\n')
		for lst_sec in lst_malus[i]:
			flux.write(lst_sec + '\n')
	flux.write('X\n')

	# Murs
	for i in range(len(murs)):
		flux.write(str(i) + '\n')
		for lst_sec in murs[i]:
			for boolean in lst_sec:
				flux.write(str(boolean))
				flux.write('\n')
	flux.write('X\n')

	# Restes
	for e in reste_lst:
		flux.write(e + '\n')
	flux.write('X\n')

	# Motifs joueurs
	for i in range(len(motif_joueur)):
		flux.write(str(i) + '\n')
		for li in motif_joueur["joueur" + str(i + 1)]:
			for carre in li:
				flux.write(str(carre))
				flux.write('\n')
			flux.write('A\n')
	flux.write('X\n')

	# Scores
	for njr in scores:
		flux.write(str(njr) + '\n')
	flux.write('X\n')

	# Malus commun
	flux.write(str(malus_commun) + '\n')
	flux.write('X\n')

	flux.close()


def lire_sauvegarde():

	lect_gamemode = 0
	lect_tour_joueur = 0

	lect_all_lst_filled = [["vide"] * 4, ["vide"] *
						   4, ["vide"] * 4, ["vide"] * 4, ["vide"] * 4]

	lect_lst_malus = [[], []]

	lect_murs = list()
	lect_motif_joueur = list()

	lect_reste_lst = []
	lect_scores = [0, 0, 0, 0]

	flux = open('Sauvegarde.txt', 'r')

	lignes = flux.readlines()

	etape_lecture = "sacs"
	nombre_joueurs = 2

	num_li = 0
	while num_li < len(lignes):
		line = lignes[num_li][:-1]

		if num_li == 0:
			lect_gamemode = int(line)

		elif num_li == 1:
			lect_tour_joueur = int(line)

		else:
			if etape_lecture == "sacs":
				nb_sacs = 0

				if lect_gamemode == 0 or lect_gamemode == 2:
					nb_sacs = 5

				if lect_gamemode >= 3:
					lect_all_lst_filled.append(["vide"] * 4)
					lect_all_lst_filled.append(["vide"] * 4)
					nombre_joueurs = 3
					nb_sacs = 7

				if lect_gamemode == 4:
					lect_all_lst_filled.append(["vide"] * 4)
					lect_all_lst_filled.append(["vide"] * 4)
					nombre_joueurs = 4
					nb_sacs = 9

				for num_s in range(nb_sacs):
					for num_rect in range(4):
						num_li += 1
						line = lignes[num_li][:-1]
						lect_all_lst_filled[num_s][num_rect] = line

					num_li += 1
				etape_lecture = "malus"
			num_li += 1

			if etape_lecture == "malus":
				if nombre_joueurs >= 3:
					lect_lst_malus.append([])

				if nombre_joueurs == 4:
					lect_lst_malus.append([])

				num_j = 0

				while line != 'X':
					num_li += 1
					line = lignes[num_li][:-1]
					# On en est à la couleur ou au num suivant ou au X
					while (len(line) > 1):
						lect_lst_malus[num_j].append(line)
						num_li += 1
						line = lignes[num_li][:-1]
					# On en est au num du joueur ou au X
					num_j += 1
				# On est au X
				etape_lecture = "murs"
				num_li += 1
				line = lignes[num_li][:-1]

			# On est au num du joueur du mur
			num_j = 0
			if etape_lecture == "murs":

				for nj in range(nombre_joueurs):
					lect_murs.append([])
					for i in range(5):
						lect_murs[nj].append([])
						for j in range(5):
							lect_murs[nj][i].append("VIDE")

				for num_j in range(nombre_joueurs):
					# On est au numero du joueur
					num_li += 1
					line = lignes[num_li][:-1]
					# On est au True ou False
					for i in range(5):
						for j in range(5):
							if line == "False":
								lect_murs[num_j][i][j] = False

							elif line == "True":
								lect_murs[num_j][i][j] = True

							num_li += 1
							line = lignes[num_li][:-1]
				etape_lecture = "reste"

			# On est au X
			num_li += 1
			line = lignes[num_li][:-1]
			# On est au 1er reste
			if etape_lecture == "reste":
				while len(line) > 1:
					lect_reste_lst.append(line)
					num_li += 1
					line = lignes[num_li][:-1]
				etape_lecture = "motif_joueur"

			# On est au X
			num_li += 1
			line = lignes[num_li][:-1]

			if etape_lecture == "motif_joueur":

				lect_motif_joueur = dict()
				for num_j in range(nombre_joueurs):
					lect_motif_joueur["joueur" + str(num_j + 1)] = [
						[-1], [-1, -1], [-1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1, -1]]

				for numer_j in range(len(lect_motif_joueur)):
					# on est au num du joueur
					num_li += 1
					line = lignes[num_li][:-1]
					# On est au premier carré
					for lin in range(len(lect_motif_joueur["joueur" + str(numer_j + 1)])):
						for num_case in range(len(lect_motif_joueur["joueur" + str(numer_j + 1)][lin])):
							if line == '0':
								lect_motif_joueur["joueur" +
												  str(numer_j + 1)][lin][num_case] = 0

							else:
								lect_motif_joueur["joueur" +
												  str(numer_j + 1)][lin][num_case] = line

							num_li += 1
							line = lignes[num_li][:-1]
						# on est sur le A
						num_li += 1
						line = lignes[num_li][:-1]
						# On est sur la 1ere case de la ligne suivante
				assert line == 'X'
				etape_lecture = "scores"
				# On est sur le X

			num_li += 1
			line = lignes[num_li][:-1]
			# On est sur le 1er score

			if etape_lecture == "scores":
				for i in range(4):
					lect_scores[i] = int(line)
					num_li += 1
					line = lignes[num_li][:-1]
				assert line == 'X'
				etape_lecture = "malus commun"
				# On est sur le X

			if etape_lecture == "malus commun":
				num_li += 1
				line = lignes[num_li][:-1]
				lect_malus_commun = (line == "True")
				num_li += 1
				line = lignes[num_li][:-1]
				assert line == 'X'

		num_li += 1

	return (lect_gamemode, lect_tour_joueur, lect_all_lst_filled, lect_lst_malus, lect_murs, lect_reste_lst, lect_motif_joueur, lect_scores, lect_malus_commun)


def lire_motifs_mur():
	flux = open('motifs_mur.txt', "r")
	lines = flux.readlines()
	flux.close()

	mat = []
	for i in range(5):
		mat.append(dict())

	for num_line in range(len(lines)):
		for num_coul in range(len(lines[num_line].split(','))):
			mat[num_line][lines[num_line][:-1].split(',')[num_coul]] = num_coul

	return mat


def main_selecteur():
	"""Définie l'écran principal pour le choix du nombre de joueur"""

	texte(328, 55, "Azul", couleur="blue", taille=35,police="arial")
	texte(200, 125, "Sélection du mode de jeu", couleur="orange",police="arial")

	rectangle(230, 300, 355, 200)
	texte(235, 230, "2 joueurs", taille=21,police="arial")
	rectangle(400, 300, 525, 200)
	texte(405, 230, "Joueur vs 2 IA", taille=13,police="arial")

	rectangle(230, 325, 355, 425)
	texte(235, 352, "Joueur vs 3 IA", taille=13,police="arial")
	rectangle(400, 325, 525, 425)
	texte(405, 358, "Joueur VS 1 IA", taille=13,police="arial")

	# Redirect to the menu for each gamemode
	global gamemode
	while True:
		x, y, _ = attente_clic()

		if 230 <= x <= 355 and 200 <= y <= 300:
			gamemode = 2
			return menu_2_players()
		if 400 <= x <= 525 and 200 <= y <= 300:
			gamemode = 3
			return menu_3_players()
		if 230 <= x <= 355 and 325 <= y <= 425:
			gamemode = 4
			return menu_4_players()
		if 400 <= x <= 525 and 325 <= y <= 425:
			gamemode = 0
			return menu_IA_players()
	# attente_clic()


def menu_2_players():
	"""Génération du plateau entier pour le mode de jeux à 2 joueurs"""

	efface_tout()
	ligne(430, 0, 430, window_lenght, couleur="black", epaisseur=2)
	ligne(930, 0, 930, window_lenght, couleur="black", epaisseur=2)
	ligne(0, window_lenght//2, 930, window_lenght //
		  2, couleur="black", epaisseur=2)

	texte(window_wight*(2/5)/2, 0, "Joueur 1",police="arial")
	texte(window_wight*(2/5)/2, 35, "Score = " +
		  str(scores[0]), couleur="brown", taille=18,police="arial")

	texte(window_wight*(2/5)/2, window_lenght-50, "Joueur 2",police="arial")
	texte(window_wight*(2/5)/2, window_lenght-85, "Score = " +
		  str(scores[1]), couleur="brown", taille=18,police="arial")

	texte(window_wight*(4.03/5), 0, "Plateau", couleur="blue",police="arial")

	texte(0, 0, "Save", couleur="blue",police="arial")
	rectangle(80, 2, 110, 32, couleur="black", remplissage="green")

	flux = open('motifs_mur.txt', "r")
	lines = flux.readlines()
	flux.close()

	global couleures_pales_mur
	global couleures_foncees_mur
	couleures_pales_mur = []
	couleures_foncees_mur = []

	for i in range(5):
		couleures_pales_mur.append([None] * 5)
		couleures_foncees_mur.append([None] * 5)

	for num_line in range(len(lines)):
		for num_coul in range(len(lines[num_line].split(','))):
			couleures_foncees_mur[num_line][num_coul] = lines[num_line][:-1].split(',')[
				num_coul]

			if lines[num_line][:-1].split(',')[num_coul] == 'grey':
				couleures_pales_mur[num_line][num_coul] = "gray70"

			elif lines[num_line][:-1].split(',')[num_coul] == 'blue':
				couleures_pales_mur[num_line][num_coul] = "light blue"

			elif lines[num_line][:-1].split(',')[num_coul] == 'green':
				couleures_pales_mur[num_line][num_coul] = "pale green"

			elif lines[num_line][:-1].split(',')[num_coul] == 'red':
				couleures_pales_mur[num_line][num_coul] = "orange"

			elif lines[num_line][:-1].split(',')[num_coul] == 'black':
				couleures_pales_mur[num_line][num_coul] = "gray30"

	# Motif - Joueur 1

	global lst_seles
	lst_seles = [[], []]

	for i in range(1, 6):
		for j in range(i):
			rectangle(170-j*30, 50+i*30, 190-j*30, 70+i*30)

		# Générer la case de sélection
		rectangle(170-j*30-40, 50+i*30+5, 190-j *
				  30-50, 70+i*30-5, couleur="orange")
		lst_seles[0].append([170-j*30-40, 50+i*30+5, 190-j*30-50, 70+i*30-5])
	rectangle(5, 255, 15, 265, couleur="orange")
	lst_seles[0].append([5, 255, 15, 265])

	# Motif - Joueur 2
	for i in range(1, 6):
		for j in range(i):
			rectangle(170-j*30, 300+i*30, 190-j*30, 320+i*30)

		# Générer la case de sélection
		rectangle(170-j*30-40, 300+i*30+5, 190-j *
				  30-50, 320+i*30-5, couleur="orange")
		lst_seles[1].append([170-j*30-40, 300+i*30+5, 190-j*30-50, 320+i*30-5])
	rectangle(5, 505, 15, 515, couleur="orange")
	lst_seles[1].append([5, 505, 15, 515])

	# Mur - Joueur 1
	for i in range(1, 6):
		for j in range(1, 6):
			rectangle(220+j*30, 50+i*30, 240+j*30, 70+i*30, couleur="black",
					  remplissage=couleures_pales_mur[i - 1][j - 1])

	# Mur - Joueur 2
	for i in range(1, 6):
		for j in range(1, 6):
			rectangle(220+j*30, 300+i*30, 240+j*30, 320+i*30, couleur="black",
					  remplissage=couleures_pales_mur[i - 1][j - 1])

	# Ligne Plancher (ligne malus) - Joueur 1
	texte_malus = "-1"
	var_malus = 0
	for i in range(1, 8):
		var_malus += 1
		if 2 < var_malus <= 5:
			texte_malus = "-2"
		if 5 < var_malus <= 7:
			texte_malus = "-3"

		rectangle(i*30-10, 250, 20+i*30-10, 270)
		texte(i*30-5, 250+20, texte_malus, taille=10,police="arial")

	# Ligne Plancher (ligne malus) - Joueur 2
	texte_malus = "-1"
	var_malus = 0
	for i in range(1, 8):
		var_malus += 1
		if 2 < var_malus <= 5:
			texte_malus = "-2"
		if 5 < var_malus <= 7:
			texte_malus = "-3"

		rectangle(i*30-10, 500, 20+i*30-10, 520)
		texte(i*30-5, 500+20, texte_malus, taille=10,police="arial")

	# Génération du plateau
	val_temp = window_wight*(4/5)

	for j in range(0, 2):
		for i in range(0, 2):
			cercle(val_temp+(i*120), 100+(j*100), 40)
	cercle(val_temp, 100+200, 40)


def menu_3_players():
	menu_2_players()

	# Motif - Joueur 3
	texte(window_wight*(2/5)/2 + 470, 0, "Joueur 3",police="arial")
	texte(window_wight*(2/5)/2 + 470, 35, "Score = " +
		  str(scores[2]), couleur="brown", taille=18,police="arial")

	lst_seles.append([])

	for i in range(1, 6):
		for j in range(i):
			rectangle((170 + 470)-j*30, 50+i*30, (190 + 470)-j*30, 70+i*30)

		# Générer la case de sélection
		rectangle(170-j*30-40 + 470, 50+i*30+5, 190-j *
				  30-50 + 470, 70+i*30-5, couleur="orange")
		lst_seles[2].append([170-j*30-40 + 470,  50+i*30+5,
							190-j*30-50 + 470,  70+i*30-5])

	rectangle((5 + 470), 255, (15 + 470), 265, couleur="orange")
	lst_seles[2].append([(5 + 470), 255, (15 + 470), 265])

	# Mur - Joueur 3
	for i in range(1, 6):
		for j in range(1, 6):
			rectangle((220 + 470)+j*30, 50+i*30, (240 + 470)+j*30, 70+i*30,
					  couleur="black", remplissage=couleures_pales_mur[i - 1][j - 1])

	# Ligne Plancher (ligne malus) - Joueur 3
	texte_malus = "-1"
	var_malus = 0
	for i in range(1, 8):
		var_malus += 1
		if 2 < var_malus <= 5:
			texte_malus = "-2"
		if 5 < var_malus <= 7:
			texte_malus = "-3"

		rectangle(i*30-10 + 470, 250, 20+i*30-10 + 470, 270)
		texte(i*30-5 + 470, 250+20, texte_malus, taille=10,police="arial")

	# Génération du plateau
	val_temp = window_wight*(4/5)

	cercle(val_temp+120, 100+200, 40)
	cercle(val_temp, 400, 40)


def menu_4_players():
	menu_3_players()

	# Motif - Joueur 4
	texte(window_wight*(2/5)/2 + 470, window_lenght-50, "Joueur 4",police="arial")
	texte(window_wight*(2/5)/2 + 470, window_lenght-85,
		  "Score = " + str(scores[3]), couleur="brown", taille=18,police="arial")

	lst_seles.append([])

	for i in range(1, 6):
		for j in range(i):
			rectangle((170 + 470)-j*30, 300+i*30, (190 + 470)-j*30, 320+i*30)

		# Générer la case de sélection
		rectangle(170-j*30-40 + 470, 300+i*30+5, 190-j *
				  30-50 + 470, 320+i*30-5, couleur="orange")
		lst_seles[3].append([170-j*30-40 + 470,  300+i*30+5,
							190-j*30-50 + 470,  320+i*30-5])

	rectangle((5 + 470), 505, (15 + 470), 515, couleur="orange")
	lst_seles[3].append([(5 + 470), 505, (15 + 470), 515])

	# Mur - Joueur 4
	for i in range(1, 6):
		for j in range(1, 6):
			rectangle((220 + 470)+j*30, 300+i*30, (240 + 470)+j*30, 320+i*30,
					  couleur="black", remplissage=couleures_pales_mur[i - 1][j - 1])

	# Ligne Plancher (ligne malus) - Joueur 4
	texte_malus = "-1"
	var_malus = 0
	for i in range(1, 8):
		var_malus += 1
		if 2 < var_malus <= 5:
			texte_malus = "-2"
		if 5 < var_malus <= 7:
			texte_malus = "-3"

		rectangle(i*30-10 + 470, 500, 20+i*30-10 + 470, 520)
		texte(i*30-5 + 470, 500+20, texte_malus, taille=10,police="arial")

	# Génération du plateau
	val_temp = window_wight*(4/5)

	cercle(val_temp+120, 400, 40)
	cercle(val_temp + 60, 470, 40)


def menu_IA_players():
	menu_2_players()
	pass


def gen_listes_tuiles():
	"""Génère la liste des tuiles dans un ordre aléatoire"""
	if gamemode == 0 or gamemode == 2:
		nb_de_tuiles_par_couleur = 20
	elif gamemode == 3:
		nb_de_tuiles_par_couleur = 28
	elif gamemode == 4:
		nb_de_tuiles_par_couleur = 36

	tuiles_lst_all = []
	for i in range(nb_de_tuiles_par_couleur):
		tuiles_lst_all.append("red")
		tuiles_lst_all.append("blue")
		tuiles_lst_all.append("green")
		tuiles_lst_all.append("black")
		tuiles_lst_all.append("grey")
	shuffle(tuiles_lst_all)
	return tuiles_lst_all


def fill_list(lst):
	"""Remplis un nombre de liste définie via une lst de 4 éléments chacune et les retournent"""

	if gamemode == 0 or gamemode == 2:
		tuple_lst = [lst_lsts[0], lst_lsts[1],
					 lst_lsts[2], lst_lsts[3], lst_lsts[4]]
		for i in range(5):
			for j in range(4):
				tuple_lst[i].append(lst[-1])
				lst.pop(-1)

		return tuple_lst

	if gamemode == 3:
		tuple_lst = [lst_lsts[0], lst_lsts[1], lst_lsts[2],
					 lst_lsts[3], lst_lsts[4], lst_lsts[5], lst_lsts[6]]
		for i in range(7):
			for j in range(4):
				tuple_lst[i].append(lst[-1])
				lst.pop(-1)

		return tuple_lst

	if gamemode == 4:
		tuple_lst = [lst_lsts[0], lst_lsts[1], lst_lsts[2], lst_lsts[3],
					 lst_lsts[4], lst_lsts[5], lst_lsts[6], lst_lsts[7], lst_lsts[8]]
		for i in range(9):
			for j in range(4):
				tuple_lst[i].append(lst[-1])
				lst.pop(-1)

		return tuple_lst


def affiche_sac(lst, num_sac):
	"""Affiche dans le menu le contenant de chaque sac en couleur"""

	x, y = num_sac_pos(num_sac)

	count = 0
	for i in range(2):
		for j in range(2):
			rectangle(x+j*20, y+i*20, x+20+j*20, y+20+i*20,
					  remplissage=lst[count], couleur="#d9d9d9")
			count += 1


def actualiser_sacs(lst):
	"""Actualise la couleur de chaque elem dans tous les sacs"""
	for i in range(len(lst)):
		affiche_sac(lst[i], i+1)


def num_sac_pos(num_sac):
	"""Retourne la position x et y du premier coin du premier carré du sac n°num_sac"""
	if num_sac == 1:
		x = 555 + 465
		y = 80

	elif num_sac == 2:
		x = 555 + 465+120
		y = 80

	elif num_sac == 3:
		x = 555 + 465
		y = 80+100

	elif num_sac == 4:
		x = 555 + 465+120
		y = 80+100

	elif num_sac == 5:
		x = 555 + 465
		y = 80 + 100 + 100

	elif num_sac == 6:
		x = 555 + 465 + 120
		y = 80 + 100 + 100

	elif num_sac == 7:
		x = 555 + 465
		y = 80 + 100 + 100 + 100

	elif num_sac == 8:
		x = 555 + 465 + 120
		y = 80 + 100 + 100 + 100

	elif num_sac == 9:
		x = 555 + 465 + 60
		y = 80 + 100 + 100 + 100 + 70

	return x, y


def get_num_sac_and_rectangle_via_pos():
	"""Retourne le numéro du sac et le numéro du rectangle du click (retourne None,num rectangle si le click est dans le reste)"""
	while True:
		x, y, _ = attente_clic()
		for i in range(len(lst_lsts)):
			val_temp_x = num_sac_pos(i+1)[0]
			val_temp_y = num_sac_pos(i+1)[1]
			if val_temp_x <= x <= val_temp_x+40 and val_temp_y <= y <= val_temp_y+40:
				val_to_return = get_num_rectangle_via_pos(i+1, (x, y))
				return val_to_return

		# Partie pour le reste du plateau
		for i in range(len(reste_lst)):
			if 500+i*30 + 465 <= x <= 520+i*30 + 465 and 400 + 130 <= y <= 420 + 130:
				return None, i
			if 500+i*30 + 465 <= x <= 520+i*30 + 465 and 430 + 130 <= y <= 450 + 130:
				return None, 10+i

		# Bouton de sauvegarde :
		if 80 <= x <= 110 and 2 <= y <= 32:
			return (-1, -1)


def get_num_rectangle_via_pos(num_sac, pos_x_y):
	"""Récupère le numéro du rectangle dans le sac num_sac via la pos_x_y"""
	x, y = num_sac_pos(num_sac)
	pos_x_click = pos_x_y[0]
	pos_y_click = pos_x_y[1]
	count = 0
	for i in range(2):
		for j in range(2):
			count += 1
			if x+j*20 <= pos_x_click <= x+20+j*20 and y+i*20 <= pos_y_click <= y+20+i*20:
				return num_sac, count


def get_color_rectangle(num_sac, num_rectangle):
	"""Retourne la couleur associé au num_rectangle dans le num_sac"""
	# Gestion du cas ou on choisis le reste du plateau

	for i in range(len(all_lst_filled)):
		if len(all_lst_filled[i]) > 4:
			all_lst_filled[i] = all_lst_filled[i][len(all_lst_filled[i])-4:]

	if num_sac == None:
		return reste_lst[num_rectangle]

	else:
		return (all_lst_filled[num_sac-1][num_rectangle-1])


def nb_rectangle_de_meme_couleur(num_sac, couleur):
	"""Renvoie le nombre de rectangle de la couleur dans le sac n°num_sac"""
	# Gestion du cas ou on choisis le reste du plateau
	if num_sac == None:
		return reste_lst.count(couleur)

	else:
		return (all_lst_filled[num_sac-1].count(couleur))


def num_case_selec_via_pos(num_joueur):
	"""Retourne le numéro de la case de sélection choisie"""

	error_count = 0
	while True:
		# Si pas le tour du bot, on demande x,y
		if num_joueur == 1 or gamemode == 2:
			x, y, _ = attente_clic()
		print(motif_joueur["joueur"+str(num_joueur)])
		for i in range(len(lst_seles[num_joueur - 1])):
			
			if (i == len((lst_seles[num_joueur - 1]))-1) or (couleur_lst(motif_joueur["joueur"+str(num_joueur)][i]) == couleur_choisie or couleur_lst(motif_joueur["joueur"+str(num_joueur)][i]) == None) and motif_joueur["joueur"+str(num_joueur)][i].count(0) > 0:

				# Si c'est pas le tour du bot
				if num_joueur == 1 or gamemode == 2:
					if lst_seles[num_joueur - 1][i][0] <= x <= lst_seles[num_joueur - 1][i][2] and lst_seles[num_joueur - 1][i][1] <= y <= lst_seles[num_joueur - 1][i][3]:

						# Si c'est pas le malus qui est choisi
						if i < 5:
							if murs[num_joueur - 1][i][motifs_mur[i][couleur_choisie]] == True:
								return None

						if confirmation_choix(i+1) == True:
							return i+1
						else:
							actualiser_motif()
							dessiner_mur()
							return None

				# Partie ou le bot choisis la case de sélection
				if num_joueur != 1 and gamemode != 2:

					# On choisis un int au hazard parmi le nombre de ligne possible de sélection
					var_tmp = randint(0, len(lst_seles[num_joueur - 1])-2)
					print("On choisir la liste de selec :"+str(var_tmp))
					print("error count="+str(error_count))
					if error_count < 100:
						if (couleur_lst(motif_joueur["joueur"+str(num_joueur)][var_tmp]) == couleur_choisie or couleur_lst(motif_joueur["joueur"+str(num_joueur)][var_tmp]) == None) and motif_joueur["joueur"+str(num_joueur)][var_tmp].count(0) > 0:

							#On vérifie si la couleur n'est pas dans le mur déjà

							#On récup d'abord les couleurs présentes dans le mur
							lst_color_in_mur = []
							for i in range(len(murs[num_joueur-1][var_tmp])):
								if murs[num_joueur-1][var_tmp][i] == True:
									couleur = couleures_foncees_mur[var_tmp][i]
									lst_color_in_mur.append(couleur)

							# Si la couleur est dans le mur, on skip
							if couleur_choisie in lst_color_in_mur:
								#print("Le bot a voulu mais pas le droit")
								continue
							
							
							#--------------------------------------------------
							if confirmation_choix(var_tmp+1) == True:
								return var_tmp+1
							else:
								actualiser_motif()
								return None

						else:
							# On compte le nombre de fois que le bot essaie de mettre un rectangle dans une ligne de sélection mais sans succès
							error_count += 1
							continue
					else:
						# Si on a 100 erreurs ou +, on return le nb de rectangle pour les ajouter dans le malus
						print("Le bot ne peut mettre nulle part sa séléction, il la met dans le malus")
						return 6

				# Si c'est pas le tour du bot
				if num_joueur == 1 or gamemode == 2:
					if lst_seles[num_joueur - 1][i][0] <= x <= lst_seles[num_joueur - 1][i][2] and lst_seles[num_joueur - 1][i][1] <= y <= lst_seles[num_joueur - 1][i][3]:

						# Si c'est pas le malus qui est choisi
						if i < 5:
							if murs[num_joueur - 1][i][motifs_mur[i][couleur_choisie]] == True:
								return None

						if confirmation_choix(i+1) == True:
							return i+1
						else:
							actualiser_motif()
							return None


def check_fin_partie():
	for nj in range(nb_joueurs):
		for i in range(len(murs[nj])):
			if False not in murs[nj][i]:
				return True
	return False


def couleur_lst(lst):
	"""Retourne la couleur présente dans la lst, si aucune couleur, return None"""
	for i in range(len(lst)):
		if lst[i] != 0:
			return lst[i]
	return None


def confirmation_choix(indice_ligne_choisie):
	"""Retourn True si on confirme le choix, sinon False"""
	ferme_fenetre()

	window_wight = 500
	window_lenght = 200
	cree_fenetre(window_wight, window_lenght)
	if indice_ligne_choisie == 6:
		indice_ligne_choisie = "de malus"
	text = "Confirmez vous l'ajout de "+str(nb_de_rectangle_choisis)+" case(s) "+str(
		couleur_choisie)+" dans la ligne "+str(indice_ligne_choisie)+" ?"
	texte(0, 10, text, taille=13,police="arial")

	ligne(0, 35, 500, 35)
	ligne(window_wight//2, 35, window_wight//2, window_lenght)
	texte(100, (window_lenght-35)//2, "Oui",police="arial")
	texte(350, (window_lenght-35)//2, "Non",police="arial")

	val_to_return = 0

	# On vérif que ça soit pas le bot qui joue
	if tour_joueur == 1 or gamemode == 2:
		while True:
			x, y, _ = attente_clic()
			if 0 <= x < window_wight//2 and 35 < y <= window_lenght:
				val_to_return = True
				break
			if window_wight//2 < x < window_wight and 35 < y <= window_lenght:
				val_to_return = False
				break

	# Si c'est le bot, on return True, car le bot confirme tous le temps
	else:
		val_to_return = True

	ferme_fenetre()

	cree_fenetre(1300, 600)
	if gamemode == 0 or gamemode == 2:
		menu_2_players()
	elif gamemode == 3:
		menu_3_players()
	elif gamemode == 4:
		menu_4_players()

	actualiser_sacs(all_lst_filled)
	mise_a_jour_malus()
	actualiser_reste(reste_lst)
	return val_to_return


def remplissage_malus(n, num_joueur):
	"""Remplis la ligne malus avec un nombre n de rectangle"""
	for i in range(n):
		lst_malus[num_joueur - 1].append(couleur_choisie)
	mise_a_jour_malus()


def mise_a_jour_malus():

	# Joueur 1
	count = 0
	for i in range(1, len(lst_malus[0])+1):
		rectangle(i*30-10, 250, 20+i*30-10, 270,
				  remplissage=lst_malus[0][count])
		count += 1

	# Joueur 2
	count = 0
	for i in range(1, len(lst_malus[1])+1):
		rectangle(i*30-10, 500, 20+i*30-10, 520,
				  remplissage=lst_malus[1][count])
		count += 1

	# Joueur 3
	if gamemode >= 3:
		count = 0
		for i in range(1, len(lst_malus[2])+1):
			rectangle(i*30-10 + 470, 250, 20+i*30-10 + 470,
					  270, remplissage=lst_malus[2][count])
			count += 1

	# Joueur 4
	if gamemode == 4:
		count = 0
		for i in range(1, len(lst_malus[3])+1):
			rectangle(i*30-10 + 470, 500, 20+i*30-10 + 470,
					  520, remplissage=lst_malus[3][count])
			count += 1

	#On retire le surplus de malus si il y en a
	for i in range(len(lst_malus)):
		while len(lst_malus[i]) > 7:
			lst_malus[i].pop()


def mise_a_jour_dict_motif_joueur():
	str_j = "joueur" + str(tour_joueur)

	nb_a_remplir = 0
	count0 = motif_joueur[str_j][num_case_chosie-1].count(0)
	if count0 >= nb_de_rectangle_choisis:
		nb_a_remplir = nb_de_rectangle_choisis
	else:
		count = 0
		for i in range(nb_de_rectangle_choisis):
			if count < count0:
				count += 1
		nb_a_remplir = count

	for i in range(len(motif_joueur[str_j][num_case_chosie-1])):
		if motif_joueur[str_j][num_case_chosie-1][-i-1] == 0:
			for j in range(nb_a_remplir):
				motif_joueur[str_j][num_case_chosie -
									1][-i-1-j] = couleur_choisie
			break
	return nb_de_rectangle_choisis-nb_a_remplir


def actualiser_motif():
	"""Actualise le motif de tout le plateau de jeux"""

	color_lst = [[], [], [], []]

	nb_joueurs = 2
	if gamemode > 2:
		nb_joueurs = gamemode

	for k in range(nb_joueurs):
		str_j = "joueur" + str(k+1)
		for i in range(len(motif_joueur[str_j])):
			for j in range(len(motif_joueur[str_j][i])):
				color = motif_joueur[str_j][i][-j-1]
				if color == 0:
					color = "#d9d9d9"
				color_lst[int(ord(str_j[-1]) - ord('1'))].append(color)


	# Affichage des murs des joueurs :
	count = 0
	for i in range(1, 6):
		for j in range(i):
			rectangle(170-j*30, 50+i*30, 190-j*30, 70+i*30,
					  remplissage=color_lst[0][count])  # J1
			rectangle(170-j*30, 300+i*30, 190-j*30, 320+i*30,
					  remplissage=color_lst[1][count])  # J2

			if gamemode >= 3:
				rectangle(170-j*30 + 470, 50+i*30, 190-j*30 + 470,
						  70+i*30, remplissage=color_lst[2][count])  # J3

			if gamemode == 4:
				rectangle(170-j*30 + 470, 300+i*30, 190-j*30 + 470,
						  320+i*30, remplissage=color_lst[3][count])  # J4

			count += 1

	


def nb_sac_remplis():
	"""Compte le nombre de sac qui n'est pas vide"""
	count = 0
	for i in range(len(all_lst_filled)):
		for j in range(len(all_lst_filled[i])):
			if all_lst_filled[i][j] != "#d9d9d9":
				count += 1
	return count


def reset():
	print("On reset")
	reste_lst = []
	#tuiles_lst_all = gen_listes_tuiles()

	# Liste de chaque sac contenant 4 tuiles
	lst_lsts = list()
	# On remplis les listes d'éléments de tuiles_lst_all
	global all_lst_filled
	all_lst_filled = fill_list(tuiles_lst_all)

	for i in range(len(all_lst_filled)):
		if len(all_lst_filled[i]) > 4:
			all_lst_filled[i] = all_lst_filled[i][len(all_lst_filled[i])-4:]

	global malus_commun
	malus_commun = True

	reste_remplissage = 0
	global lst_malus
	lst_malus = [[], []]

	if gamemode >= 3:
		lst_malus.append([])
	if gamemode == 4:
		lst_malus.append([])

	for t in range(nb_joueurs):
		mise_a_jour_malus()

	ferme_fenetre()
	cree_fenetre(1300, 600)
	if gamemode == 0 or gamemode == 2:
		menu_2_players()
	elif gamemode == 3:
		menu_3_players()
	elif gamemode == 4:
		menu_4_players()

	actualiser_sacs(all_lst_filled)
	actualiser_motif()
	dessiner_mur()


def compter_score_pose_mur(num_jo, num_ligne, num_col):
	score_a_ajouter = 0

	# Comptage points ligne
	tmp = 0
	for i in range(5):
		if murs[num_jo][num_ligne][i] == True:
			tmp += 1
			if i == 4:
				score_a_ajouter += tmp
		else:
			if i > num_col:
				score_a_ajouter += tmp
				break
			else:
				tmp = 0
				continue

	# Comptage points colonne
	tmp = 0
	for i in range(5):
		if murs[num_jo][i][num_col] == True:
			tmp += 1
			if i == 4:
				if tmp > 1:
					score_a_ajouter += tmp
		else:
			if i > num_col:
				if tmp > 1:
					score_a_ajouter += tmp
				break
			else:
				tmp = 0
				continue

	return score_a_ajouter


def calcul_malus(nu_j):
	deduction = 0
	primitive_valeurs_malus = [0, 1, 2, 4, 6, 8, 11, 14]

	deduction = primitive_valeurs_malus[len(lst_malus[nu_j])]
	return deduction


def jouer():
	"""Boucle principale du jeux"""
	global malus_commun

	global tour_joueur
	if tour_joueur == -1:
		tour_joueur = 1
	actualisation_tour_du_joueur()
	jeu_non_fini = True

	while jeu_non_fini:
		while len(reste_lst) > 0 or nb_sac_remplis() > 0:

			global nb_de_rectangle_choisis
			global num_sac
			global num_rectangle
			global couleur_choisie
			global num_case_chosie

			# On récupère le num du sac et du rectangle cliqué
			while True:
				actualisation_tour_du_joueur()

				# Si c'est le tour du bot
				print(tour_joueur,gamemode)
				if tour_joueur != 1 and gamemode != 2:
					print("tour du bot")
					# Si 1 on va prendre dans les sacs, si 2 dans le reste
					choix_random = randint(1, 2)

					random_list_1 = list(range(1,len(all_lst_filled)+1))


					random_number_1 = randint(0, 4)

					if choix_random == 1:
						num_sac = choice(random_list_1)
						num_rectangle = random_number_1
					elif choix_random == 2 and len(reste_lst) > 0:
						num_sac = None
						num_rectangle = randint(0, len(reste_lst)-1)
					else:
						num_sac = choice(random_list_1)
						num_rectangle = random_number_1
					
					

					

				else:
					num_sac, num_rectangle = get_num_sac_and_rectangle_via_pos()
					print("Sac n°"+str(num_sac)+" num_rectangle="+str(num_rectangle))

				# Si on sauvegarde la partie
				if (num_sac, num_rectangle) == (-1, -1):
					sauvegarder_partie()
					continue
				print("num_sac:"+str(num_sac)+" num_rectangle:"+str(num_rectangle))
				print(all_lst_filled)


				couleur_choisie = get_color_rectangle(num_sac, num_rectangle)
				print("Couleur choisie:"+couleur_choisie)
				if couleur_choisie == "#d9d9d9":
					continue

				global nb_de_rectangle_choisis
				nb_de_rectangle_choisis = nb_rectangle_de_meme_couleur(
					num_sac, couleur_choisie)
				num_case_chosie = num_case_selec_via_pos(tour_joueur)
				print("num_case_chosie:"+str(num_case_chosie))

				# Si il se prend le malus commun il a pas le droit de mettre dans ses malus le reste
				if num_case_chosie == 6 and malus_commun == True and num_sac == None:
					actualiser_motif()
					dessiner_mur()
					continue

				# Si la confirmation n'est passé, on reprend de 0
				if num_case_chosie != None:
					break

			if malus_commun == True and num_sac == None:
				malus_commun = False
				lst_malus[tour_joueur - 1].append(couleur_choisie)
				mise_a_jour_malus()

			if num_case_chosie != 6:
				reste_remplissage = mise_a_jour_dict_motif_joueur()
			else:
				reste_remplissage = nb_de_rectangle_choisis

			if reste_remplissage > 0:
				remplissage_malus(reste_remplissage, tour_joueur)
			actualiser_motif()
			dessiner_mur()
			actualiser_reste(reste_lst)
			mise_a_jour_malus()

			# On réactualise les sacs pour faire disparaître les carrés choisis en les mettant blanc
			# On ajoute dans la liste reste_lst les elems non utilisés
			if num_sac != None:
				for i in range(len(all_lst_filled[num_sac-1])):
					if not all_lst_filled[num_sac-1][i] == couleur_choisie:
						reste_lst.append(all_lst_filled[num_sac-1][i])
					all_lst_filled[num_sac-1][i] = "#d9d9d9"
			# On réactualise le reste en enlevant les elem qui ont été choisis
			else:
				while couleur_choisie in reste_lst:
					reste_lst.remove(couleur_choisie)

			# Ajouter le reste après chaque tour
			actualiser_reste(reste_lst)

			actualiser_sacs(all_lst_filled)

			tour_joueur += 1
			# Si on a fait un tour de plateau
			if (tour_joueur > gamemode and gamemode != 0) or (tour_joueur == 3 and gamemode == 0):
				tour_joueur = 1


		# Remplissage des murs :

		for num_jou in range(nb_joueurs):
			escalier_joueur = motif_joueur["joueur" + str(num_jou + 1)]
			for ligne in escalier_joueur:
				numero_ligne = len(ligne) - 1

				# Si il s'agit d'un ligne complète :
				if 0 not in ligne:

					# On l'ajoute au mur
					murs[num_jou][numero_ligne][motifs_mur[numero_ligne]
												[ligne[0]]] = True
					scores[num_jou] += compter_score_pose_mur(
						num_jou, numero_ligne, motifs_mur[numero_ligne][ligne[0]])

					# On supprime la ligne du motif_joueur également
					for i in range(len(escalier_joueur[numero_ligne])):
						escalier_joueur[numero_ligne][i] = 0
					

		# On déduit les points de malus des scores :
		for nu_j in range(nb_joueurs):
			scores[nu_j] -= calcul_malus(nu_j)
			if scores[nu_j] < 0:
				scores[nu_j] = 0



		if check_fin_partie() == True:
			jeu_non_fini = False
			return

		reset()

def actualiser_reste(lst):
	"""Actualise l'affichage du reste"""
	# On reset le reste, pour qu'il soit blanc
	reset_rest()

	count = 0
	for i in range(len(reste_lst)):
		if i < 10:

			rectangle(500+i*30 + 465, 400 + 130, 520+i*30 + 465,
					  420 + 130, remplissage=reste_lst[i], couleur="#d9d9d9")
		else:
			rectangle(500+count*30 + 465, 400+30 + 130, 520+count*30 + 465,
					  420+30 + 130, remplissage=reste_lst[i], couleur="#d9d9d9")
			count += 1


def dessiner_mur():
	# Mur - Joueur 1
	for i in range(1, 6):
		for j in range(1, 6):
			if murs[0][i - 1][j - 1] == True:
				rectangle(220+j*30, 50+i*30, 240+j*30, 70+i*30, couleur="purple",
						  epaisseur=2, remplissage=couleures_foncees_mur[i - 1][j - 1])

			else:
				rectangle(220+j*30, 50+i*30, 240+j*30, 70+i*30, couleur="black",
						  remplissage=couleures_pales_mur[i - 1][j - 1])

	# Mur - Joueur 2
	for i in range(1, 6):
		for j in range(1, 6):
			if murs[1][i - 1][j - 1] == True:
				rectangle(220+j*30, 300+i*30, 240+j*30, 320+i*30, couleur="purple",
						  epaisseur=2, remplissage=couleures_foncees_mur[i - 1][j - 1])

			else:
				rectangle(220+j*30, 300+i*30, 240+j*30, 320+i*30, couleur="black",
						  remplissage=couleures_pales_mur[i - 1][j - 1])

	# Mur - Joueur 3
	if gamemode >= 3:
		for i in range(1, 6):
			for j in range(1, 6):
				if murs[2][i - 1][j - 1] == True:
					rectangle((220 + 470)+j*30, 50+i*30, (240 + 470)+j*30, 70+i*30, couleur="purple",
							  epaisseur=2, remplissage=couleures_foncees_mur[i - 1][j - 1])
				else:
					rectangle((220 + 470)+j*30, 50+i*30, (240 + 470)+j*30, 70+i*30,
							  couleur="black", remplissage=couleures_pales_mur[i - 1][j - 1])

	# Mur - Joueur 4
	if gamemode == 4:
		for i in range(1, 6):
			for j in range(1, 6):
				if murs[3][i - 1][j - 1] == True:
					rectangle((220 + 470)+j*30, 300+i*30, (240 + 470)+j*30, 320+i*30,
							  couleur="purple", epaisseur=2, remplissage=couleures_foncees_mur[i - 1][j - 1])
				else:
					rectangle((220 + 470)+j*30, 300+i*30, (240 + 470)+j*30, 320+i*30,
							  couleur="black", remplissage=couleures_pales_mur[i - 1][j - 1])


def reset_rest():
	"""Affiche un carré blanc dans le reste pour permettre de repartir sur une base blanche"""
	rectangle(500 + 465, 400 + 130, 800 + 465, 450 + 130,
			  remplissage="#d9d9d9", couleur="#d9d9d9")


def actualisation_tour_du_joueur():
	"""Affiche quel joueur doit jouer"""
	texte(465, 5, "Joueur n°"+str(tour_joueur), couleur="purple",police="arial")


def calcul_scores_supplementaires():
	scores_supp = [0, 0, 0, 0]
	for nu_j in range(nb_joueurs):

		# 2 points par ligne complète
		for num_l in range(len(murs[nu_j])):
			if False not in murs[nu_j][num_l]:
				scores_supp[nu_j] += 2

		# 7 points par colonne complète
		for num_c in range(len(murs[nu_j])):
			valide = True
			for num_l in range(len(murs[nu_j])):
				if murs[nu_j][num_l][num_c] == False:
					valide = False
					break
			if valide == True:
				scores_supp[nu_j] += 7

		# 10 points par couleur entièrement placée sur le mur
		couleurs = ["red", "blue", "green", "grey", "black"]
		for n_coul in range(len(couleurs)):
			valide = True
			for num_l in range(len(murs[nu_j])):
				if murs[nu_j][num_l][motifs_mur[num_l][couleurs[n_coul]]] == False:
					valide = False
					break
			if valide == True:
				scores_supp[nu_j] += 10

	return scores_supp


def comparer_murs_egalite(a, b):

	compteur_lignes_non_vides_a = 0
	for ligne in murs[a]:
		if False not in ligne:
			compteur_lignes_non_vides_a += 1

	compteur_lignes_non_vides_b = 0
	for ligne in murs[b]:
		if False not in ligne:
			compteur_lignes_non_vides_b += 1

	if a > b:
		return a
	else:
		return b


if '__main__' == __name__:
	window_wight = 1300
	window_lenght = 600

	global scores
	scores = [0, 0, 0, 0]

	global motifs_mur
	motifs_mur = lire_motifs_mur()

	global malus_commun
	malus_commun = True

	cree_fenetre(window_wight, window_lenght)

	fname = "Sauvegarde.txt"

	global nb_joueurs
	tour_joueur = -1

	# Charger à partir de la sauvegarde

	if os.path.exists(fname):
		(gamemode, tour_joueur, all_lst_filled, lst_malus, murs,
		 reste_lst, motif_joueur, scores, malus_commun) = lire_sauvegarde()
		if gamemode == 0 or gamemode == 2:
			nb_joueurs = 2
			menu_2_players()

		elif gamemode == 3:
			nb_joueurs = 3
			menu_3_players()

		elif gamemode == 4:
			nb_joueurs = 4
			menu_4_players()

		lst_lsts = list(all_lst_filled)
		actualiser_motif()
		dessiner_mur()
		actualiser_reste(reste_lst)
		mise_a_jour_malus()

	else:
		main_selecteur()

		if gamemode == 0:
			nb_joueurs = 2
		else:
			nb_joueurs = gamemode

		reste_lst = []
		tuiles_lst_all = gen_listes_tuiles()

		# Liste de chaque sac contenant 4 tuiles
		lst_lsts = list()
		if gamemode == 0 or gamemode == 2:
			for i in range(5):
				lst_lsts.append([])
		elif gamemode == 3:
			for i in range(7):
				lst_lsts.append([])

		elif gamemode == 4:
			for i in range(9):
				lst_lsts.append([])

		# On remplis les listes d'éléments de tuiles_lst_all
		all_lst_filled = fill_list(tuiles_lst_all)
		murs = list()

		for num_joueur in range(nb_joueurs):
			murs.append([])
			for j in range(5):
				murs[num_joueur].append([False] * 5)

		lst_malus = [[], []]
		if gamemode >= 3:
			lst_malus.append([])
		if gamemode == 4:
			lst_malus.append([])

		motif_joueur = dict()
		if gamemode == 0 or gamemode == 2:
			motif_joueur["joueur1"] = [[0], [0, 0], [
				0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0]]
			motif_joueur["joueur2"] = [[0], [0, 0], [
				0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0]]

		else:
			for num_j in range(1, gamemode + 1):
				motif_joueur["joueur" + str(num_j)] = [[0], [0, 0],
													   [0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0]]

	actualiser_sacs(all_lst_filled)
	jouer()

	# La partie est finie, on calcule les scores finaux
	scores_supp = calcul_scores_supplementaires()
	for i in range(len(scores)):
		scores[i] += scores_supp[i]

	# On recherche le gagnant
	gagnant = -1
	score_max = max(scores)
	for i in range(len(scores)):
		if scores[i] == score_max:

			# Si il y a égalité :
			if gagnant != -1:
				gagnant = comparer_murs_egalite(gagnant, i)

			# Sinon :
			else:
				gagnant = i

	if nb_joueurs == 2:
		menu_2_players()

	if nb_joueurs == 3:
		menu_3_players()

	if nb_joueurs == 4:
		menu_4_players()

	actualiser_motif()
	dessiner_mur()
	actualiser_reste(reste_lst)
	mise_a_jour_malus()

	texte(350, 250, "Gagnant : Joueur " + str(gagnant + 1),
		  taille=60, couleur="orange red",police="arial")

	# Fin du jeux
	attente_clic()
