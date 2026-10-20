# Punisher MC×DC 2026 « La ville ne dort jamais » : questions pour l'utilisateur (20/10/2026)

Les 8 décisions à poser (P1 à P8) de `docs/rapports/cadrage-14-15-19-2026-10-20.md` §1.6, reformulées une
par une, recommandation en premier marquée, avec ce que change chaque option **en jeu**. Une question à la
fois, capture à l'appui quand une image est citée. Contexte complet : `docs/packs/mcdc-2026-punisher/README.md`
(décisions déjà prises 1 à 6 le 19/10/2026), `cartes.md`, `regles-fr.md`. Rien n'est tranché ici.

⚠ **Depuis le 19/10/2026** : les briques moteur communes M6 (un ennemi attaque un ennemi ou un allié) et M7
(méchant actif / CIBLÉ, insensible aux cartes joueur) ont été écrites le 20/10/2026 pour Galactic Storm et sont
**déjà réutilisables ici sans redéveloppement** (`src/game/operate/immunity.py`, `src/game/operate/villains.py`,
fiches `docs/reference/mots-cles/immunite-cartes-joueur.md` et `mechants-multiples.md`, recette
`docs/reference/RECETTES-MOTEUR.md` §16). Ça ne change aucune des 8 questions ci-dessous, mais ça retire une
dépendance : le scénario 3 (Punishment, question Q6 ci-dessous n'existe pas — ce point n'était pas un P du
cadrage, juste un repère) peut démarrer dès que Jigsaw/Hobgoblin (contenu indépendant) sont portés, sans
attendre un lot « briques communes » séparé.

## Q1. Kingsfall (scénario 4, combat multi-tables) : que fait-on ?

Kingsfall n'est pas un scénario mais un **format d'événement** (plusieurs tables jouent Kingpin en même temps
et s'échangent des jetons de « Soutien des Citoyens » pendant la partie ; *The King* compare les résultats de
TOUTES les tables). Fidèle en solo/coop : impossible sans un serveur qui relie plusieurs parties en direct
(aucune brique existante) et sans groupes réels pour le faire vivre. Cartes : `cartes.md` p269-p273.
1. **(Recommandé) Hors périmètre.** La campagne s'arrête au combat 3 (victoire = allié Punisher gagné) ;
   après le 3e combat, l'écran de campagne dit que la campagne est gagnée et renvoie au livret pour le 4e.
   Change en jeu : aucune « vraie » fin de campagne jouable dans le moteur ; rien d'inventé.
2. Plus tard, en vrai format multi-tables (serveur + interface neufs, plusieurs groupes connectés en même
   temps). Change en jeu : fidèle, mais chantier à part entière, sans rapport avec le reste de la campagne.
3. Version « une table » adaptée (Kingpin + SWAT + Tracksuit Mafia + allié Punisher, sans assemblée). Change
   en jeu : jouable par tous, mais règles inventées — contredit la règle du projet « fidélité 100 % des
   cartes » (mémoire `fidelite-cartes-100-pour-cent`).

## Q2. L'extension Uptown (4e rangée, 3 lieux et 3 pistes de plus, 4 CAPO)

`cartes.md` p045-p055 (Upper West Side, Harlem, The Bronx + leurs 3 pistes LEAD). Le combat 1 de la campagne
exclut Uptown de toute façon (« Do not include Uptown Expansion »).
1. **(Recommandé) Le moteur est écrit pour N rangées dès le départ**, les 7 cartes Uptown viennent dans un
   second temps (lot PU-10 du découpage). Change en jeu : aucun au lancement (Uptown pas encore jouable) ;
   aucun surcoût de conception plus tard.
2. Tout de suite, avec le scénario 1 (grille 4×3 dès la première version, mini-carte plus haute). Change en
   jeu : Uptown disponible dès le scénario 1, mais plus de travail avant que le scénario 1 soit jouable.
3. Jamais. Change en jeu : aucune option Uptown, y compris plus tard.

## Q3. Affichage des neuf lieux sur le plateau : on confirme « A + B » ?

Le README (`docs/packs/mcdc-2026-punisher/README.md`, décision 4) note « ça a l'air pas mal A et B », pas un
« oui » net — à confirmer explicitement. Maquette : `docs/packs/mcdc-2026-punisher/maquette-ville.html`.
1. **(Recommandé) A + B** : la table ne montre que mon territoire (chef de ma rangée, sbires engagés), une
   mini-carte 3×3 reste dans un coin (chef par rangée, pion de position, pastille des cartes attachées), un
   clic ouvre une fenêtre « La Ville » déplaçable avec les 9 lieux en grand, un sélecteur « voir le
   territoire de [joueur] » si deux joueurs sont dans des territoires différents. Change en jeu : vue
   complète à la demande, le plus de travail d'interface des trois options (lot PU-8, moyen à gros).
2. A seul (table + mini-carte, sans fenêtre détaillée). Change en jeu : moins de travail, mais les lieux ne
   sont jamais vus en grand nulle part.
3. B seul (la ville en grand en permanence). Change en jeu : prend la place de la table, gênant pendant la
   phase du méchant (trois territoires actifs en même temps).

## Q4. Les quatre défis (Rise of the Machines, Secret Agent, It's a Trap!, Angry Birds)

`cartes.md` p279-p282. Règles spéciales sur des scénarios **officiels déjà portés**, aucune carte Punisher
en jeu. Modèle existant : `src/cards/pack/challenges/` (25 défis, type `Challenge`,
`AbilityFactory.UsingOnlyHeroes`).
1. **(Recommandé) Après la campagne**, comme défis indépendants sur le modèle du pack `challenges`. Change
   en jeu : rien avant d'y arriver ; Angry Birds exige des règles de constitution de deck particulières à
   vérifier au portage.
2. Avec la campagne, dans le même lot. Change en jeu : disponibles plus tôt, mais mélange deux types de
   contenu (campagne vs. défis isolés) dans un seul lot d'agent.
3. Non. Change en jeu : les 4 défis ne sont jamais portés.

## Q5. Version MC×DC de Hawkeye (nouvelles valeurs et nouvelles capacités, p283-p284)

`cartes.md` p283-p284 (détail complet des écarts avec le Hawkeye officiel : héros THW 2/ATK 1/DEF 2 au lieu
de THW 1/ATK 2/DEF 1, trait S.H.I.E.L.D. en plus, « basic attacks gain ranged », alter-ego avec une Réponse
EN PLUS de son unique aptitude officielle). Vérifié le 20/10/2026 (point 6 du présent lot) : le Hawkeye
officiel (`04001a`/`04001b`/`04002`/`04003`, set `trors`) et les cartes au trait ARROW (6 au total : 5 dans
`trors` + `kb006` Smoke Arrow du pack Kate Bishop) sont bien dans `data/cards.json` — la question « les
flèches existent-elles ? » du README est confirmée réglée, « oui ».
1. **(Recommandé) Une identité alternative à choisir** (« Hawkeye (MC×DC 2026) »), avec le deck officiel de
   Hawkeye (Arc, Carquois, flèches). Change en jeu : le Hawkeye officiel reste intact, un second choix
   d'identité Hawkeye apparaît au deck-building.
2. Ne pas l'inclure (ce n'est qu'une fiche de héros fournie aux participants de l'événement). Change en jeu :
   aucun changement au roster de héros.
3. Remplacer le Hawkeye officiel. **Déconseillé** : change les parties de tous les joueurs qui ont déjà un
   Hawkeye officiel en cours.

## Q6. « +1 compteur par joueur qui n'a pas joué la partie précédente avec vous » (récompenses 1 à 3)

Cartes 6132B/6133B/6134B (`cartes.md` p264, p266, p268) : « Place 1 counter here, plus 1 more for each player
who did not play the last game together. » Comment le moteur reconnaît-il « un joueur qui n'a pas joué la
dernière partie » ?
1. **(Recommandé) Par le compte en ligne, et par le héros en partie locale** (la campagne connaît déjà
   l'équipe de chaque scénario). Change en jeu : un changement de héros en local compte comme un nouveau
   joueur ; cohérent avec la lettre de la carte (« player », pas « account »).
2. Par le siège seulement (joueur 1, joueur 2…). Change en jeu : plus simple à coder, mais faux si deux amis
   échangent leur place à la table entre deux parties.
3. Toujours demander à l'écran de campagne « qui n'a pas joué la dernière partie ? ». Change en jeu : fiable
   dans tous les cas, mais une question de plus à chaque combat 2 et 3.

## Q7. Texte français des cartes (le livret FR n'a traduit que les règles)

`regles-fr.md` traduit intégralement les règles mais ne traduit aucune carte. Rappel : les briques communes
M6/M7 citées en tête de ce fichier n'ont aucun impact sur cette question (traduction de texte, pas de
mécanique).
1. **(Recommandé) Nous traduisons**, avec les noms du livret FR (`regles-fr.md`, section « Noms français »)
   et le lexique officiel déjà utilisé pour les autres packs (Skrull Menace, Galactic Storm). Change en
   jeu : rien n'attend personne, les cartes sortent en français dès le portage ; l'utilisateur relit ensuite
   les cartes qu'il veut (lot PU-12).
2. Demander d'abord à Batou et à l'équipe VF (crédités dans `regles-fr.md`) s'ils traduisent les cartes.
   Change en jeu : traduction potentiellement plus fidèle au style de l'équipe MC/DC, mais risque d'attendre
   une réponse avant de pouvoir afficher les cartes en français.
3. Laisser les cartes en anglais pour la première version. Change en jeu : sortie plus rapide, mais rupture
   avec le reste du jeu (tout le contenu existant est en français).

## Q8. Crédits MC×DC (mémoire `credits-mcdc-2026`) : où les montrer ?

Rappel mémoire utilisateur : nommer le groupe MC×DC dans les remerciements à l'intégration de la campagne
Punisher. Liste complète déjà rassemblée dans `regles-fr.md` (organisateurs, développeurs, testeurs, Batou
et l'équipe VF, Huzzah Hobbies) + les illustrateurs imprimés sur chaque carte (`cartes.md`, un nom par
carte).
1. **(Recommandé) Page Crédits du jeu (liste complète) + une ligne sous le titre de la campagne** dans
   l'écran de campagne (« créée par MC/DC, Huzzah Hobbies 2026 ; version française : Batou et son équipe »).
   Change en jeu : les crédits complets restent consultables en un endroit, et un rappel court apparaît à
   chaque lancement de la campagne.
2. Page Crédits seulement. Change en jeu : moins visible pendant le jeu, mais moins de travail d'interface.
3. Page Crédits + écran de chargement de chaque scénario. Change en jeu : le plus visible des trois, mais un
   rappel répété à chaque scénario (4 fois) plutôt qu'une seule fois par campagne.

## Réponses de l'utilisateur (20/10/2026)

Toutes en option recommandée.
- P1 Kingsfall : hors périmètre, la campagne s'arrête au combat 3.
- P2 Uptown : moteur écrit pour N rangées dès le départ, les 7 cartes Uptown portées après le reste.
- P3 Affichage ville : A + B (territoire sur la table, mini-carte, fenêtre « La Ville »).
- P4 Défis : après la campagne, sur le modèle du pack `challenges`.
- P5 Hawkeye MC×DC : identité alternative à choisir, le Hawkeye officiel reste intact.
- P6 Reconnaissance du joueur (récompenses) : compte en ligne, héros en local.
- P7 Textes FR des cartes : traduits par nous, avec le lexique officiel.
- P8 Crédits MC×DC : page Crédits + ligne sous le titre de campagne.
