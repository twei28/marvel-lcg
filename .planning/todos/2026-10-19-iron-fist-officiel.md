# Iron Fist officiel (Hero Pack MC64EN, novembre 2026) : à reprendre demain (20/10/2026)

**Statut** : lecture des cartes FAITE, aucune carte créée. Décision de l'utilisateur le 19/10/2026 : on garde la suite pour le lendemain.

## Fait
- Relevé de 29 cartes publiées (héros 1A/1B, 11 cartes signature en 15 exemplaires, 5 Protection, 4 Basic, 1 Aggression, 2 Leadership, etc.) : `.planning/iron-fist-officiel/releve-hall-of-heroes.md`.
  Source : https://hallofheroeslcg.com/iron-fist-danny-rand/ (images de spoil) et l'article FFG https://www.fantasyflightgames.com/way-of-the-iron-fist/.
- Logique des exemplaires déduite et confirmée : le « n/15 » imprimé = rang du premier exemplaire. Cartes signature n° 2 à 12 : Deep Breathing ×3, Dragon Punch, Fists of Fury ×2, The Way of Things ×2, Lei Kung, Book of the Iron Fist, Channel the Iron Fist, Embody the Dragon, Feel the Flow, Keep 'Em Coming, Redirect Chi.
- Lecture selon le processus : `.planning/iron-fist-officiel/lecture-cartes.md`, 5 questions tranchées dans `lecture-reponses.md` (attache des Techniques à l'identité ; Techniques défaussées à la fin du round au retour en héros ; Way of Things libre ; Deep Breathing vide le deck ; chi conservé au retournement).

## À faire (dans l'ordre, PROCESSUS-HEROS.md puis PROCESSUS-CARTE.md pour chaque carte)
1. Décider si on crée avant la sortie (spoils, textes possiblement modifiés) ou si l'on attend les scans de novembre.
2. Étape 2 du processus : carte de référence du moteur pour chaque capacité (compteur « ici » : modèle `calm` de Lockjaw `lj017` ; `retaliate X` dynamique ; Hero Resource ; « lose temporary »).
3. Moteur : compteur `chi`, traits (Technique, Martial Artist, K'un-Lun, Persona, Skill, Superpower).
4. Créer héros (1A/1B) + 11 cartes signature, deck de départ (`player_deck` vide sauf decklist de l'éditeur, voir PROCESSUS-HEROS), tests carte par carte.
5. Récupérer : les scans haute définition (11 cartes lues en 300 px) ; les cartes de rencontre du héros (némésis, obligation, manigance annexe : aucune info publiée) ; les numéros 26 à 29 et 34+ du pack ; le nombre d'exemplaires des cartes d'aspect.
6. Périmètre : seulement le héros et ses cartes signature (décision de l'utilisateur). Les cartes Protection/Basic/Aggression/Leadership du pack sont hors périmètre pour l'instant.

## Pièges notés
- MC4DB (https://mc4db.merlindumesnil.net) n'a pas encore le pack officiel au 19/10/2026 ; son pack « iron_fist_by_merlin » est un travail fan-made distinct (ne pas confondre).
- Une icône de ressource ne se nomme jamais à vue (Redirect Chi : étoile = wild, à confirmer contre une carte du même pack).

## Cartes d'aspect du pack (HORS PÉRIMÈTRE pour l'instant : 17 cartes relevées, aucune créée)
Source : mêmes images de Hall of Heroes ; textes complets dans `releve-hall-of-heroes.md`. Noms anglais, pas de version française connue.
- **Protection (8)** : Helpful Bystander (n° 13, allié 1, passant fragile, +1 main, attire l'attaque), Iron Fist / Lin Lie (n° 14, allié 4, étourdit après une attaque, −2 de contrecoup s'il achève),
  Defiance (n° 15, événement de défense, défausse un boost), Demoralize (n° 16, force un ennemi à attaquer puis le désoriente), The Night Nurse (n° 17, support, 3 soins),
  Redirection Mastery (n° 18, renvoie des dégâts égaux à la DÉF après une défense exacte), No Time to Bleed (n° 19, soigne 1 à chaque carte jouée, temporaire), Tonfa (n° 20, +1 DÉF ou riposte 1).
- **Basic (6)** : Luke Cage (n° 22), Colleen Wing (n° 21), Punch Reverse Punch (n° 23), Power Man and Iron Fist (n° 24), Thunder Dojo (n° 25), The Defenders (n° 33).
- **Aggression (1)** : Death by a Thousand Cuts (n° 30). **Leadership (2)** : Zen-Like Calm (n° 31), Sensei (n° 32).
- Manque : numéros 26 à 29 et 34+ ; nombre d'exemplaires non imprimé ; composition du deck préconstruit de 40 cartes (attendu : 15 Protection + 10 Basic en plus des 15 signature).
- Piège de vocabulaire : « consequential damage » (dégâts de contrecoup) est une notion des règles 1.8, à vérifier côté moteur (présente dans `face_action.py`, `can_attack.py`).
