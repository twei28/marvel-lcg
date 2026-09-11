# L'autoplay est aveugle sur Iron Patriot, et la cause n'est pas le pack

**Constaté le 11/09/2026**, en vérifiant un chiffre laissé en suspens : Iron
Patriot perd **16 parties sur 16 au round 1,0**, là où le témoin `spider_man`
tient 3,6 rounds contre le même vilain, dans la même fournée.

## Ce n'est pas une régression, et ce n'est pas un défaut du pack

**Vérifié en remisant le correctif moteur du jour** (`git stash` des cinq
fichiers, autoplay relancé) : **chiffre identique sans lui**, 16/16 au round
1,0. Le canal des refus n'y est pour rien.

**Vérifié sur la carte** : l'Action *Enlistment* de `ip002a` Registration Act
n'a **aucune limite imprimée**, et une manigance-joueur ne peut pas s'incliner.
Elle est donc réellement répétable. C'est le texte de l'auteur, et le risque
qu'il a voulu : tu t'engages des sbires. Un humain la prend une ou deux fois.

## Ce qui se passe vraiment

Le pilote la prend **21 fois dans le round 1**. Les sbires REGISTERED entrent
en jeu par dizaines (33 cartes en jeu dans une partie d'un round), et leur
Incitation remplit le complot principal :

| Source de la menace | Occurrences |
|---|---|
| `ip025`, `ip022`, `ip032`, `ip031`, `ip029` (sbires REGISTERED) | 9 |
| deck Rencontre standard (`01130`, `01125`, `01121`, `01116b`) | 4 |

## La cause, mesurée et non supposée

`tools/autoplay.py:517`, branche par défaut du scorer : « une capacité proposée
et non forcée est presque toujours un gain » → **score fixe de 20**.

Première hypothèse, **fausse** : faire décroître ce score avec le nombre de
reprises dans le round. Essayée en `20/(1+n)` puis en `20/(1+n)²` : **21
reprises dans les deux cas**, 16/16 au round 1,0 inchangé.

Expérience discriminante : score forcé à **0,5 sans aucune condition**.
Résultat : **toujours 21 reprises**. Donc Attaque et Contre valent **moins de
0,5** au round 1.

**C'est là le vrai défaut.** `urgence(tours)` rend une valeur proche de zéro
tant que l'échéance est lointaine, et tous les gains pondérés
(`poids_menace * urgence * THW`, etc.) s'effondrent avec elle en début de
partie. N'importe quelle capacité à score fixe écrase donc les pouvoirs de
base. Le 20 ne créait pas le problème, il le masquait.

⚠ Le garde-fou de répétition existant (`etat["historique"]`) ne pouvait pas
l'attraper : il est indexé sur une **empreinte du contexte**, et chaque sbire
qui entre en jeu change le contexte. L'empreinte changeait à chaque coup.

## Ce que ça coûte, et pourquoi ça compte

**Les « 16 parties, 0 traceback » d'Iron Patriot ne valaient presque rien.**
Toutes finissaient avant la fin du premier round, sans exercer le pack. La gate
la plus chère du projet est aveugle sur ce pack, et le sera sur tout pack
offrant une capacité nommée répétable.

Les autres packs ne sont pas touchés de la même façon : Spider-Woman tient 3,9
et 5,8 rounds, Spider-Man 3,6 et 5,6. Le défaut ne se voit que quand une
capacité répétable est offerte en permanence.

## Ce qui n'a PAS été fait, et pourquoi

La correction du scorer a été **retirée** : elle n'apportait aucun bénéfice
mesuré, et garder une modification non probante dans l'instrument de mesure de
tout le projet aurait été pire que le défaut.

Le vrai chantier est ailleurs : **re-calibrer la courbe d'urgence pour que les
pouvoirs de base gardent une valeur en début de partie**. Le fichier montre que
ce modèle a été réglé par mesures successives (« essayée et retirée : elle
faisait tomber le bot de 6,3 à 4 rounds ») ; y toucher demande la même rigueur,
sur plusieurs decks témoins, et ce n'est pas un patch.

## Si on y revient

1. Instrumenter le scorer pour **afficher les scores** de chaque option offerte,
   pas seulement leurs noms. Aujourd'hui la trace ne montre que
   `offres r1: ['Change_Form', 'Enlistment', 'Play', 'Attack', 'Thwart']`, sans
   les valeurs : impossible de régler à l'aveugle.
2. Mesurer la courbe d'urgence sur 3 decks témoins AVANT de la changer.
3. Ne juger que sur les rounds tenus et les parties bloquées, jamais sur le taux
   de victoire seul.
