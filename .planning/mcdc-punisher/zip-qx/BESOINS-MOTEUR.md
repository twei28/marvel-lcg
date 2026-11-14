# BESOINS-MOTEUR, pré-identification (sans modification du moteur)

**État : besoins fonctionnels repérés; API du dépôt non testée.** Ils doivent être confrontés aux capacités existantes avant de modifier quoi que ce soit.

### B1 - Positions individuelles sur une grille
Livret/source : Livret PDF p.4, The City (MC/DC 6005)
Ce que le jeu fait déjà de plus proche : Ce que le jeu sait déjà: non vérifié (dépôt absent)
Ce qui manque potentiellement : Positions par joueur dans des cases, adjacence orthogonale, déplacement pour un coût, contrôle de portée et application des effets localement
Dépend de : qx005, qx030 à qx038; scénario Big Apple
En attendant : A_FAIRE_CLAUDE dès que le script correspondant sera écrit et que le besoin sera confirmé.

### B2 - Un vilain actif par rangée (turf)
Livret/source : Livret PDF p.4, Gang War (MC/DC 6001A/B)
Ce que le jeu fait déjà de plus proche : non vérifié
Ce qui manque potentiellement : Trois CAPO simultanés (quatre en Uptown), activations seulement dans leur rangée; simultanéité d’actions du joueur en turfs différents
Dépend de : qx001a/b, qx048 à qx055
En attendant : A_FAIRE_CLAUDE dès que le script correspondant sera écrit et que le besoin sera confirmé.

### B3 - LEADS séparés et victoire alternative
Livret/source : Livret PDF p.4 et MC/DC 6001B/6002B
Ce que le jeu fait déjà de plus proche : non vérifié
Ce qui manque potentiellement : Deck Leads séparé, découverte/entrée en victoire, seuil par joueur et victoire par progression de complot sans défaite classique des vilains
Dépend de : qx001b, qx002b; qx039 à qx047
En attendant : A_FAIRE_CLAUDE dès que le script correspondant sera écrit et que le besoin sera confirmé.

### B4 - Phase entre Gang War / Silence / Warehouse
Livret/source : Livret PDF p.4 ; MC/DC 6003A/B
Ce que le jeu fait déjà de plus proche : non vérifié
Ce qui manque potentiellement : Réinitialiser HP des CAPO, compteurs quell, tirage du gunrunner, convertir attachements de lieux en cartes de rencontre
Dépend de : qx001 à qx004
En attendant : A_FAIRE_CLAUDE dès que le script correspondant sera écrit et que le besoin sera confirmé.

### B5 - Choix conditionnel du scénario 2
Livret/source : Livret PDF p.6, campagne
Ce que le jeu fait déjà de plus proche : non vérifié
Ce qui manque potentiellement : Choisir automatiquement Hobgoblin ou Jigsaw selon le Gunrunner; choisir variante du complot principal selon la position finale LEAD
Dépend de : qx133a; champs carnet gunrunner et final_lead_location
En attendant : A_FAIRE_CLAUDE dès que le script correspondant sera écrit et que le besoin sera confirmé.

### B6 - Punisher + UNDERLING simultanés
Livret/source : Livret PDF p.7, Justice or Punishment
Ce que le jeu fait déjà de plus proche : non vérifié
Ce qui manque potentiellement : Deux vilains co-présents avec adressage explicite des effets: «the villain» cible Punisher, UNDERLING reste ciblable par Punisher; défaite si Underling s’échappe
Dépend de : qx086 à qx092
En attendant : A_FAIRE_CLAUDE dès que le script correspondant sera écrit et que le besoin sera confirmé.

### B7 - Target Lock et effets sur la défausse
Livret/source : Livret PDF p.7 ; MC/DC 6091A/B
Ce que le jeu fait déjà de plus proche : non vérifié
Ce qui manque potentiellement : Punisher peut attaquer des ennemis, y compris lui-même en cas d’égalité; Target Lock bascule selon phase/action, dégâts et menace calculés par défausse de rencontre
Dépend de : qx091a/b
En attendant : A_FAIRE_CLAUDE dès que le script correspondant sera écrit et que le besoin sera confirmé.

### B8 - Sous-campagne épique Kingsfall
Livret/source : Livret PDF p.8 ; MC/DC 6135-6137
Ce que le jeu fait déjà de plus proche : non vérifié
Ce qui manque potentiellement : Plusieurs pods de 2 à 4 joueurs, support public partagé, progression Kingpin et condition globale de victoire, coordination inter-parties
Dépend de : qx135 à qx137
En attendant : A_FAIRE_CLAUDE dès que le script correspondant sera écrit et que le besoin sera confirmé.

### B9 - Transmission et persistance des récompenses
Livret/source : Livret PDF p.4-8 ; cartes 6132-6134
Ce que le jeu fait déjà de plus proche : non vérifié
Ce qui manque potentiellement : Seized Tech Crate parties 2-3, Ordnance Cache partie 3, Punisher joueur partie 4, valeurs persistées et contrôlées à chaque passage de partie
Dépend de : qx132 à qx134
En attendant : A_FAIRE_CLAUDE dès que le script correspondant sera écrit et que le besoin sera confirmé.
