# Secret Invasion (scenario 5 de Skrull Menace, Kajislav) — gabarits PROCESSUS-CARTE

Pack `skrull_menace`, card_id sk189-sk227 : 6 faces de mechant (Spider-Woman (Veranke) / Queen Veranke, stades I a III), 2 complots
principaux a deux faces (The Infiltration Has Begun, The Skrull Invasion), l'environnement « Who Do You Trust? », 13 cartes de rencontre
(Impostor, 3 Super-Skrull Enhancement, 3 complots annexes, 6 traitrises) et le PAQUET IMPOSTOR de 20 cartes double face (allie CAMOUFLAGED en
face `a`, sbire REVEALED en face `b`). Fiches generees a partir des resultats REELS (rapport test_capacites, sorties de
`substituer_pack.py`, en-tetes des modules) par `.planning/skrull-menace/defs/generer_gabarits_secret_invasion.py`.

Rappels communs a toutes les cartes :
- **Etape 6 (nombres)** : stats, PV, menaces (depart / objectif / escalade), boosts et icones relus sur les SCANS de l'auteur (1500x2150) contre
  `data/cards.json` : les 6 faces de mechant, les 4 complots, l'environnement, les 13 cartes de rencontre et 9 paires Impostor ouvertes une a une,
  les 11 autres paires verifiees a partir de la transcription (qui s'est revelee exacte sur toutes les paires ouvertes). Lectures corrigees par
  rapport a la transcription : l'icone des complots annexes sk199/sk200/sk201 est ACCELERATION (comparee a sk156), les triangles rouges de
  leur coin sont des icones de boost (3, 2, 2). Voir `defs/secret_invasion_questions.md`.
- **Etape 7 (tests)** : 225 cas `[secret_invasion]` dans `tools/cas/secret_invasion.py` (charge par `tools/test_capacites.py`), **225/225 verts**.
  Pieges payes pendant les tests :
  - la main de depart de Spider-Man contient `01061` Great Responsibility, que le pilote joue : il remplace toute menace posee sur le complot par
    des degats (les `SetThreat` d'abord sans effet). Le constructeur de cas vide la main avant tout `SetThreat` ;
  - un heros PRET defend automatiquement (DEF 3 de Spider-Man annule les attaques de test) : les cas qui mesurent des degats sur l'identite
    inclinent d'abord le heros (`Puzzle.Exhaust`) ;
  - `SetThreat` vers le BAS retire de la menace donc pose des jetons de soupcon : les cas du complot posent leurs jetons apres ;
  - `Puzzle.PutIntoPlay` engage deja un sbire : ne PAS appeler `Puzzle.Engage` ensuite (il desengage) ;
  - le paquet IMPOSTOR est rendu deterministe par `Puzzle.Remove` de toutes les autres cartes (`GARDER`).
- **Substitution (`substituer_pack.py`, 14 passes de <= 16 modules, empreinte md5 du pack identique avant/apres)** : les 64 modules ont au moins un
  cas ROUGE sans eux. Les cas qui restent verts sans module sont, fiche par fiche, des TEMOINS d'absence d'effet (nom « TEMOIN »), des cas de
  VALEURS imprimees (desc, aucun script), ou des mots-cles NATIFS lus dans `desc` (Guard, Patrol, Retaliate, Toughness, Quickstrike, Villainous,
  Incite, Hinder, Acceleration) : assumes comme le prevoit l'etape 7.
- **Etape 7 bis** : aucune limite imprimee (« once per ... ») dans ce scenario.
- **Etape 8 (autoplay)** : 40 parties `equilibre` contre `sk_secret_invasion` (normal et expert, 8 graines chacun) : spider_man 16 et
  hulkling_kajislav 16, plus 8 parties spider_man contre Rhino comme TEMOIN. Grep exhaustif `NameError|AttributeError|TypeError|KeyError|
  AssertionError` sur les 32 journaux : **0**. 0 victoire (spider_man : 12 « Main Scheme completed » et 4 eliminations ; hulkling : 14 et 2) en ~4
  rounds : le bot `equilibre` ne fait pas tomber un mechant qu'il faut d'abord retourner, et le temoin Rhino ne gagne pas non plus (0/8, 6,9
  rounds) : ce n'est pas un signal d'equilibrage. Journaux lus : jetons de soupcon qui montent a chaque attaque de Spider-Woman et redescendent
  avec la menace posee, allies Impostor mis en jeu a la fin des tours.
- **Outils statiques** : `verifier_appels_modules skrull_menace` OK (porte calibree : un appel inexistant glisse dans un module est detecte et
  la gate tombe) ; `verifier_api_cartes` : aucune faute dans skrull_menace.
- **Tous les decks** : `verifier_tous_les_decks.py` : 141/141 decks montent une partie (fichiers moteur partages touches).
- **Moteur partage** : 3 traits, 1 compteur, 1 nom de paquet de scenario, le paiement en groupe (`resources.py`) et une branche « Villain » dans
  `manager.py` (`defs/secret_invasion_moteur.md`).
- **Limites connues et questions** : `defs/secret_invasion_questions.md` (tour « your turn » des complots, manigance de l'allie, Mistrust, etc.).
  Non teste : le mot-cle Alliance sous Mistrust and Paranoia (le garde est dans `resources.py` mais aucun evenement Alliance n'est joue dans les cas) ;
  la phrase « at the same time as minions » (l'allie maniganche juste apres le mechant, avant les sbires).
- **Ce qu'aucun outil ne voit** : une vraie partie jouee par un humain dans le navigateur (rendu des deux faces des cartes Impostor, de la
  carte Veranke retournee et de l'Action de heros portee par le mechant dans la barre d'actions), non faite.

