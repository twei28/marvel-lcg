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


### sk189a : Spider-Woman (Veranke)

- [x] Etape 2 : carte(s) de reference : `60131`, `sk150`, `sk086`, `25036`, `60110a` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk189a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : voir en-tete du module.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "14*", "ATK": "2*", "SCH": "2", "Stage": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 11/11 cas verts : « k189a Setup (1A sk192a, puis 1B sk192b) : Veranke CAMOUFLAGED, environnement en jeu, paquet IMPOSTOR de 20 cartes » VERT; « k189a valeurs imprimees : PV 14[per_hero], MNG 2, ATQ 2 » VERT; « k189a ne peut pas subir de degats ; TEMOIN sk189b (face REVEALED) : les degats passent » VERT; « k189a ne subit aucun degat meme a 99 : jamais vaincue sous sa forme CAMOUFLAGED » VERT; « k189a Reponse forcee : apres qu'elle t'attaque, 1 jeton de soupcon ; TEMOIN sk189b : aucun » VERT; « k189a « You are a Skrull! » : incline un heros et depense 1 ressource -> Veranke se retourne sur sk189b » VERT; « k189a « You are a Skrull! » sans ressource : le cout n'est pas paye, Veranke reste sk189a » VERT; « k189a « You are a Skrull! » : 2 joueurs, le cout (2 ressources) se paie EN GROUPE avec la main de l'autre joueur » VERT; « k189a « You are a Skrull! » : meme montage mais Mistrust and Paranoia (sk201) interdit le paiement en groupe : rien » VERT; « k189a Avancee de stade depuis la face A : le stade II arrive sur la face A (sk190a) » VERT; « k223b Une fois vaincu : retourne Queen Veranke (sk189b -> Spider-Woman sk189a) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 7/10 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie ; l'Action de heros « You are a Skrull! » portee par le mechant n'a pas ete vue dans la barre d'actions du plateau).

Carte terminée : OUI

### sk189b : Queen Veranke

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk189b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : voir en-tete du module.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "14*", "ATK": "2", "SCH": "2", "Stage": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 11/11 cas verts : « k189b valeurs imprimees : PV 14[per_hero], MNG 2, ATQ 2 » VERT; « k189a ne peut pas subir de degats ; TEMOIN sk189b (face REVEALED) : les degats passent » VERT; « k189a Reponse forcee : apres qu'elle t'attaque, 1 jeton de soupcon ; TEMOIN sk189b : aucun » VERT; « k189a « You are a Skrull! » : incline un heros et depense 1 ressource -> Veranke se retourne sur sk189b » VERT; « k189b Reponse forcee : fin de la phase du mechant avec un joueur en ALTER EGO -> Queen Veranke se retourne sur Spider-Woman » VERT; « k189b Reponse forcee : TEMOIN, tous les joueurs en forme HEROS -> Queen Veranke reste REVEALED » VERT; « k189b Une fois vaincue : retire TOUS les jetons de soupcon ; le stade II arrive du MEME COTE (Queen Veranke, sk190b) » VERT; « k189b TEMOIN : meme montage SANS vaincre la reine (13 degats sur 14) : les jetons restent » VERT; « k189b Avancee de stade depuis la face B (REVEALED) : le stade II arrive sur la face B (sk190b), les degats restent » VERT; « k189b Retournements successifs : les degats RESTENT sur la carte (5 apres deux retournements) » VERT; « k223b Une fois vaincu : retourne Queen Veranke (sk189b -> Spider-Woman sk189a) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/10 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie).

Carte terminée : OUI

### sk190a : Spider-Woman (Veranke)

- [x] Etape 2 : carte(s) de reference : `60131`, `sk150`, `sk086`, `25036`, `60110a` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk190a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : voir en-tete du module.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "18*", "ATK": "2*", "SCH": "3", "Stage": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 9/9 cas verts : « k192a Setup EXPERT : on commence au stade II (sk190a), meme paquet et meme environnement » VERT; « k190a valeurs imprimees : PV 18[per_hero], MNG 3, ATQ 2 » VERT; « k190a ne peut pas subir de degats ; TEMOIN sk190b (face REVEALED) : les degats passent » VERT; « k190a ne subit aucun degat meme a 99 : jamais vaincue sous sa forme CAMOUFLAGED » VERT; « k190a Reponse forcee : apres qu'elle t'attaque, 1 jeton de soupcon ; TEMOIN sk190b : aucun » VERT; « k190a « You are a Skrull! » : incline un heros et depense 1 ressource -> Veranke se retourne sur sk190b » VERT; « k190a « You are a Skrull! » sans ressource : le cout n'est pas paye, Veranke reste sk190a » VERT; « k190b Reponse forcee : stade II, un alter ego -> retourne sur Spider-Woman (sk190a) » VERT; « k189a Avancee de stade depuis la face A : le stade II arrive sur la face A (sk190a) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 5/6 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie ; l'Action de heros « You are a Skrull! » portee par le mechant n'a pas ete vue dans la barre d'actions du plateau).

Carte terminée : OUI

### sk190b : Queen Veranke

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk190b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : voir en-tete du module.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "18*", "ATK": "3", "SCH": "2", "Stage": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 9/9 cas verts : « k190b valeurs imprimees : PV 18[per_hero], MNG 2, ATQ 3 » VERT; « k190a ne peut pas subir de degats ; TEMOIN sk190b (face REVEALED) : les degats passent » VERT; « k190a Reponse forcee : apres qu'elle t'attaque, 1 jeton de soupcon ; TEMOIN sk190b : aucun » VERT; « k190a « You are a Skrull! » : incline un heros et depense 1 ressource -> Veranke se retourne sur sk190b » VERT; « k190b Reponse forcee : stade II, un alter ego -> retourne sur Spider-Woman (sk190a) » VERT; « k190b Reponse forcee : TEMOIN stade II, forme heros -> reste sk190b » VERT; « k189b Une fois vaincue : retire TOUS les jetons de soupcon ; le stade II arrive du MEME COTE (Queen Veranke, sk190b) » VERT; « k190b Une fois vaincue : retire les jetons ; stade III du meme cote (sk191b) » VERT; « k189b Avancee de stade depuis la face B (REVEALED) : le stade II arrive sur la face B (sk190b), les degats restent » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/6 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie).

Carte terminée : OUI

### sk191a : Spider-Woman (Veranke)

- [x] Etape 2 : carte(s) de reference : `60131`, `sk150`, `sk086`, `25036`, `60110a` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk191a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : voir en-tete du module.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "21*", "ATK": "3*", "SCH": "3", "Stage": "3"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 6/6 cas verts : « k191a valeurs imprimees : PV 21[per_hero], MNG 3, ATQ 3 » VERT; « k191a ne peut pas subir de degats ; TEMOIN sk191b (face REVEALED) : les degats passent » VERT; « k191a ne subit aucun degat meme a 99 : jamais vaincue sous sa forme CAMOUFLAGED » VERT; « k191a Reponse forcee : apres qu'elle t'attaque, 1 jeton de soupcon ; TEMOIN sk191b : aucun » VERT; « k191a « You are a Skrull! » : incline un heros et depense 1 ressource -> Veranke se retourne sur sk191b » VERT; « k191a « You are a Skrull! » sans ressource : le cout n'est pas paye, Veranke reste sk191a » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 5/6 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie ; l'Action de heros « You are a Skrull! » portee par le mechant n'a pas ete vue dans la barre d'actions du plateau).

Carte terminée : OUI

### sk191b : Queen Veranke

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk191b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : voir en-tete du module.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "21*", "ATK": "4", "SCH": "2", "Stage": "3"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 9/9 cas verts : « k191b valeurs imprimees : PV 21[per_hero], MNG 2, ATQ 4 » VERT; « k191a ne peut pas subir de degats ; TEMOIN sk191b (face REVEALED) : les degats passent » VERT; « k191a Reponse forcee : apres qu'elle t'attaque, 1 jeton de soupcon ; TEMOIN sk191b : aucun » VERT; « k191a « You are a Skrull! » : incline un heros et depense 1 ressource -> Veranke se retourne sur sk191b » VERT; « k191b Reponse forcee : stade III, un alter ego -> retourne sur Spider-Woman, SANS defausser la carte du deck » VERT; « k191b Reponse forcee : stade III, forme heros, la carte defaussee est une TRAITRISE -> Queen Veranke se retourne » VERT; « k191b Reponse forcee : TEMOIN stade III, forme heros, la carte defaussee n'est PAS une traitrise -> reste sk191b » VERT; « k190b Une fois vaincue : retire les jetons ; stade III du meme cote (sk191b) » VERT; « k191b Dernier stade vaincu : pas de « When Defeated », les jetons restent et les joueurs GAGNENT » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/7 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie).

Carte terminée : OUI

### sk192a : The Infiltration Has Begun

- [x] Etape 2 : carte(s) de reference : `hs107a` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk192a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : voir en-tete du module.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k189a Setup (1A sk192a, puis 1B sk192b) : Veranke CAMOUFLAGED, environnement en jeu, paquet IMPOSTOR de 20 cartes » VERT; « k192a Setup EXPERT : on commence au stade II (sk190a), meme paquet et meme environnement » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (complot principal a deux faces ; menace et objectif affiches par le plateau (existant)).

Carte terminée : OUI

### sk192b : The Infiltration Has Begun

- [x] Etape 2 : carte(s) de reference : `60121b`, `16091b` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk192b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « each SKRULL ENEMY »; « each IMPOSTOR ALLY ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "1", "TargetThreat": "8*", "EscalationThreat": "1*", "StartingThreat": "2*"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 10/10 cas verts : « k189a Setup (1A sk192a, puis 1B sk192b) : Veranke CAMOUFLAGED, environnement en jeu, paquet IMPOSTOR de 20 cartes » VERT; « k192b Valeurs par joueur : 2 joueurs, Veranke I a 28 PV et la menace de depart vaut 4 » VERT; « k192b TEMOIN de la manigance de l'allie : sans allie, la menace est inferieure de 2 (1 d'escalade supplementaire + 1 de SCH) » VERT; « k192b ★ Escalade : +1 par ennemi SKRULL et par allie IMPOSTOR : Veranke seule -> 1 (imprime) + 1 = 2 » VERT; « k192b ★ Escalade : avec UN allie IMPOSTOR en plus : 3 » VERT; « k192b ★ Escalade : un SBIRE SKRULL compte (+1) mais pas comme « allie IMPOSTOR » ; Veranke + Skrull Warrior + allie = 4 » VERT; « k192b Reponse forcee : fin du tour, moins de 2[per_hero] jetons de soupcon -> un allie CAMOUFLAGED au hasard sous le controle du joueur » VERT; « k192b Reponse forcee : 1 jeton de soupcon (< 2) : l'allie arrive encore » VERT; « k192b Reponse forcee : TEMOIN, 2 jetons de soupcon (= 2[per_hero]) : aucun allie n'arrive » VERT; « k192b Reponse forcee : 2 joueurs, seuil 2[per_hero] = 4 : 3 jetons laissent encore arriver un allie, sous le controle du joueur dont le tour finit » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 7/9 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (complot principal a deux faces ; menace et objectif affiches par le plateau (existant)).

Carte terminée : OUI

### sk193a : The Skrull Invasion

- [x] Etape 2 : carte(s) de reference : `01136` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk193a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « IF Mistrust and Paranoia IS IN PLAY ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k193a Une fois revele (Mistrust and Paranoia DEJA en jeu) : retire 2[per_hero] jetons de soupcon et ne cherche rien » VERT; « k193a Une fois revele (Mistrust absent) : cherche Mistrust and Paranoia dans le deck rencontre et le REVELE, sans retirer de jeton » VERT; « k193a Une fois revele : Mistrust cherche aussi dans la DEFAUSSE rencontre » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (complot principal a deux faces ; menace et objectif affiches par le plateau (existant)).

Carte terminée : OUI

### sk193b : The Skrull Invasion

- [x] Etape 2 : carte(s) de reference : `sk192b`, `sk082b`, `sk085b` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk193b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « TWICE the number of SKRULL ENEMIES ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "2", "TargetThreat": "14*", "EscalationThreat": "0", "StartingThreat": "1*"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 6/6 cas verts : « k193b ★ Escalade X : 2 par ennemi SKRULL : Veranke + Skrull Warrior = 4 » VERT; « k193b ★ Escalade X : Veranke seule : 2 » VERT; « k193b Valeurs imprimees : objectif 14[per_hero], escalade 0 (X), menace de depart 1[per_hero] » VERT; « k193b Reponse forcee : fin du tour, moins de 2[per_hero] jetons -> un SBIRE REVEALED du paquet, ENGAGE avec le joueur » VERT; « k193b Reponse forcee : TEMOIN 2 jetons de soupcon : aucun sbire » VERT; « k193b Dernier stade : un complot accompli = les joueurs PERDENT » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/6 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (complot principal a deux faces ; menace et objectif affiches par le plateau (existant)).

Carte terminée : OUI

### sk194 : "Who Do You Trust?"

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk194.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « placed ON THE MAIN SCHEME »; « an EQUAL amount ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « k194 Menace POSEE sur le complot principal (manigance du mechant) : autant de jetons de soupcon sont RETIRES » VERT; « k194 Menace posee : les jetons ne descendent pas sous 0 » VERT; « k194 Menace RETIREE du complot principal (contre du heros) : autant de jetons de soupcon sont POSES » VERT; « k194 Menace retiree : seule la menace REELLEMENT retiree compte (1 menace presente, retrait de 3 : 1 jeton de plus) » VERT; « k194 Menace posee sur un complot ANNEXE : aucun jeton retire (seul le complot PRINCIPAL compte) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (jetons de SOUPCON sur l'environnement : nom francais dans `ui-app/src/board/compteurs-fr.test.ts` (vert)).

Carte terminée : OUI

### sk195 : Impostor

- [x] Etape 2 : carte(s) de reference : `sk098`, `36038` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk195.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « NON-SKRULL ally ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k195 Impostor : un allie NON SKRULL (01002 Black Cat) devient un sbire SKRULL engage » VERT; « k195 Impostor : les allies Impostor CAMOUFLAGED sont deja SKRULL, ils ne sont pas cibles : le mechant maniganche » VERT; « k195 Impostor : sans allie, le mechant maniganche » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk196 : Super-Skrull Enhancement

- [x] Etape 2 : carte(s) de reference : `sk098`, `sk103`, `sk107`, `sk115`, `sk122` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk196.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the SKRULL minion »; « WITHOUT ANOTHER Super-Skrull Enhancement ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"ATK+": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « k196 Super-Skrull Enhancement : s'attache au sbire SKRULL qui a le plus de PV restants (Skrull Commander, 5 PV) » VERT; « k196 Super-Skrull Enhancement : « without another » : une SECONDE amelioration va sur l'AUTRE sbire (Skrull Warrior) » VERT; « k196 Super-Skrull Enhancement : sans sbire SKRULL, l'allie CAMOUFLAGED est RETOURNE puis la carte s'attache au sbire revele » VERT; « k196 Super-Skrull Enhancement : ni sbire SKRULL ni allie CAMOUFLAGED : la carte gagne SURGE (revele la suivante) » VERT; « k196 Super-Skrull Enhancement ★ Boost : revelee APRES l'activation, elle s'attache au Skrull Commander » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 5/5.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk197 : Super-Skrull Enhancement

- [x] Etape 2 : carte(s) de reference : `sk098`, `sk103`, `sk107`, `sk115`, `sk122` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk197.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the SKRULL minion »; « WITHOUT ANOTHER Super-Skrull Enhancement ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"ATK+": "3"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « k197 Super-Skrull Enhancement : s'attache au sbire SKRULL qui a le plus de PV restants (Skrull Commander, 5 PV) » VERT; « k197 Super-Skrull Enhancement : « without another » : une SECONDE amelioration va sur l'AUTRE sbire (Skrull Warrior) » VERT; « k197 Super-Skrull Enhancement : sans sbire SKRULL, l'allie CAMOUFLAGED est RETOURNE puis la carte s'attache au sbire revele » VERT; « k197 Super-Skrull Enhancement : ni sbire SKRULL ni allie CAMOUFLAGED : la carte gagne SURGE (revele la suivante) » VERT; « k197 Super-Skrull Enhancement ★ Boost : revelee APRES l'activation, elle s'attache au Skrull Commander » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 5/5.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk198 : Super-Skrull Enhancement

- [x] Etape 2 : carte(s) de reference : `sk098`, `sk103`, `sk107`, `sk115`, `sk122` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk198.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the SKRULL minion »; « WITHOUT ANOTHER Super-Skrull Enhancement ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"ATK+": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « k198 Super-Skrull Enhancement : s'attache au sbire SKRULL qui a le plus de PV restants (Skrull Commander, 5 PV) » VERT; « k198 Super-Skrull Enhancement : « without another » : une SECONDE amelioration va sur l'AUTRE sbire (Skrull Warrior) » VERT; « k198 Super-Skrull Enhancement : sans sbire SKRULL, l'allie CAMOUFLAGED est RETOURNE puis la carte s'attache au sbire revele » VERT; « k198 Super-Skrull Enhancement : ni sbire SKRULL ni allie CAMOUFLAGED : la carte gagne SURGE (revele la suivante) » VERT; « k198 Super-Skrull Enhancement ★ Boost : revelee APRES l'activation, elle s'attache au Skrull Commander » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 5/5.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk199 : Chaos on the Battlefield

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk199.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the TOTAL SCH of ALL IMPOSTOR CHARACTERS in play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "1", "Acceleration": "1", "Boost": "3", "Incite": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k199 Chaos on the Battlefield : X = SCH total des IMPOSTOR en jeu (allie sk208a SCH 1 + sbire sk212b SCH 2 = 3) : 1 + 3 = 4 menaces » VERT; « k199 Chaos on the Battlefield : sans IMPOSTOR, X = 0 : seulement la menace de depart (1) » VERT; « k199 Chaos on the Battlefield : Incite 2 (+2 sur le complot principal) et icone Acceleration » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk200 : Fulfill the Prophecy

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk200.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH SKRULL MINION »; « guard AND patrol ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "3", "Hinder": "1*", "Acceleration": "1", "Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k200 Fulfill the Prophecy : chaque sbire SKRULL gagne Guard ET Patrol (Skrull Warrior, qui a deja Guard) » VERT; « k200 Fulfill the Prophecy : TEMOIN sans la carte, le Commander n'a ni Guard ni Patrol » VERT; « k200 Fulfill the Prophecy : Hinder 1[per_hero] et menace 3 » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk201 : Mistrust and Paranoia

- [x] Etape 2 : carte(s) de reference : `sk070` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk201.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « minions engaged with OTHER players ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "2", "Acceleration": "1", "Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 7/7 cas verts : « k189a « You are a Skrull! » : meme montage mais Mistrust and Paranoia (sk201) interdit le paiement en groupe : rien » VERT; « k201 Mistrust and Paranoia : menace de depart 2 + 1 par personnage ami en jeu (2 joueurs : 2 identites -> 4) » VERT; « k201 Mistrust and Paranoia : compte aussi les allies (1 joueur, identite + Black Cat = 2) : 2 + 2 = 4 » VERT; « k201 Mistrust and Paranoia : un joueur ne peut PAS attaquer un sbire engage avec un AUTRE joueur » VERT; « k201 Mistrust and Paranoia : TEMOIN, le meme sbire engage avec le joueur 0 est attaque normalement (2 degats) » VERT; « k201 Mistrust and Paranoia : un allie du joueur 1 ne peut PAS defendre contre un sbire engage avec le joueur 0 » VERT; « k201 TEMOIN : sans Mistrust, l'allie du joueur 1 defend bien contre le sbire du joueur 0 » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/6 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk202 : Arrival of Impostors

- [x] Etape 2 : carte(s) de reference : `sk104` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk202.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH player ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « k202 Arrival of Impostors ★ Boost : un allie CAMOUFLAGED arrive sous le controle du joueur attaque » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk203 : Camouflage

- [x] Etape 2 : carte(s) de reference : `sk189b`, `sk098`, `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk203.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « When Revealed ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « k203 Camouflage Une fois revelee (Queen Veranke) : la retourne SUR Spider-Woman et retire 3 jetons de soupcon » VERT; « k203 Camouflage Une fois revelee (Spider-Woman) : Spider-Woman MANIGANCE, ne se retourne pas, ne touche pas aux jetons » VERT; « k203 Camouflage ★ Boost : Queen Veranke se retourne sur Spider-Woman APRES l'activation » VERT; « k203 Camouflage ★ Boost : TEMOIN, Spider-Woman (deja camouflee) n'est pas retournee » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk204 : Glory to the Skrull Empire

- [x] Etape 2 : carte(s) de reference : `sk103` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk204.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « If the villain ALREADY has a tough status card ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « k204 Glory to the Skrull Empire : le mechant ET chaque sbire SKRULL engage avec toi recoivent une carte Robuste » VERT; « k204 Glory to the Skrull Empire : un sbire SKRULL engage avec un AUTRE joueur ne recoit rien » VERT; « k204 Glory to the Skrull Empire : le mechant avait DEJA une carte Robuste : la carte gagne SURGE » VERT; « k204 Glory to the Skrull Empire : TEMOIN sans carte Robuste prealable, pas de surge » VERT; « k204 Glory to the Skrull Empire ★ Boost : le mechant recoit une carte Robuste » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk205 : Infiltration Ritual

- [x] Etape 2 : carte(s) de reference : `sk103`, `sk104` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk205.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « under ANY player's control »; « If you cannot ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « k205 Infiltration Ritual : un allie CAMOUFLAGED du paquet entre en jeu sous le controle d'UN joueur (1 joueur : lui) » VERT; « k205 Infiltration Ritual : 2 joueurs, le joueur qui revele DESIGNE le joueur : l'allie arrive sous le controle de l'un des deux » VERT; « k205 Infiltration Ritual : paquet et defausse vides -> la carte gagne SURGE » VERT; « k205 Infiltration Ritual ★ Boost : retire 3 jetons de soupcon » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/4.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk206 : Invasion Fleet

- [x] Etape 2 : carte(s) de reference : `sk202` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk206.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH player ... engaged with THEM »; « REVEALED minion ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k206 Invasion Fleet : CHAQUE joueur recoit un sbire REVEALED du paquet, engage avec LUI (2 joueurs) » VERT; « k206 Invasion Fleet ★ Boost : un sbire REVEALED du paquet, engage avec le joueur attaque » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk207 : Revelation

- [x] Etape 2 : carte(s) de reference : `sk098`, `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk207.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the CAMOUFLAGED ally with the MOST REMAINING hit points ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k207 Revelation : retourne l'allie CAMOUFLAGED qui a le PLUS de PV RESTANTS (l'autre, blesse, reste allie) » VERT; « k207 Revelation : sans allie CAMOUFLAGED, un sbire REVEALED du paquet vient engager le joueur » VERT; « k207 Revelation ★ Boost : retourne UN allie CAMOUFLAGED que tu controles, APRES l'activation » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk208a : Captain America (Pitt'o Nili)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk208a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "ATK": "2**"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 16/16 cas verts : « k208a Interruption forcee : l'allie Pitt'o Nili devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk208b engage, PV soignes » VERT; « k208a valeurs imprimees de l'allie : PV 4, ATQ avec 2 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT; « k208a attaque : subit ses 2 degat(s) consequentiel(s) (les pastilles de l'ATQ) et peut attaquer le mechant » VERT; « k208a ne peut pas CONTRER : son pouvoir THW ne retire aucune menace » VERT; « k208a TEMOIN du contre : un allie ordinaire (01041 Shuri, THW 1) retire bien de la menace » VERT; « k208a defend : un allie CAMOUFLAGED peut defendre (il encaisse l'attaque, 1 degat de l'Hydra Mercenary) » VERT; « k208a Interruption forcee : une DEFAUSSE ordinaire (pas une defaite) retourne aussi l'allie » VERT; « k208a Retourner l'allie : cartes d'etat, ameliorations (01074 Inspired) et jetons partent, le sbire arrive nu » VERT; « k208a Retourner l'allie d'un AUTRE joueur : le sbire engage le joueur qui CONTROLAIT l'allie (pas celui qui revele) » VERT; « k208a Mise en jeu sous le controle d'un joueur : Arrival of Impostors donne UN allie a CHAQUE joueur (2 joueurs) » VERT; « k208a Paquet vide : on y REMELANGE la defausse IMPOSTOR, sans penalite (aucun jeton d'acceleration) » VERT; « k208a Une allie en trop : la limite d'allies (3) s'applique a un allie CAMOUFLAGED ; l'excedent se retourne ou part » VERT; « k208a Phase du mechant, joueur en ALTER EGO : l'allie maniganche (SCH 1), subit 1 degat consequentiel et ne s'incline pas » VERT; « k208a TEMOIN : joueur en forme HEROS, l'allie ne maniganche pas (aucun degat consequentiel) » VERT; « k208a Menace posee par la manigance de l'allie : SCH 1 de plus que sans lui (temoin : meme montage sans allie) » VERT; « k199 Chaos on the Battlefield : X = SCH total des IMPOSTOR en jeu (allie sk208a SCH 1 + sbire sk212b SCH 2 = 3) : 1 + 3 = 4 menaces » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/16 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk208b : Pitt'o Nili

- [x] Etape 2 : carte(s) de reference : `sk098` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk208b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "ATK": "2", "SCH": "1", "Guard": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « k208a Interruption forcee : l'allie Pitt'o Nili devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk208b engage, PV soignes » VERT; « k208b Le sbire REVEALED qui quitte le jeu va dans la DEFAUSSE IMPOSTOR (pas dans la defausse rencontre) » VERT; « k208b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k208b Guard : mot-cle natif lu dans desc, le sbire garde le mechant » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk209a : Captain Marvel (Khn'nr)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk209a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "2*"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k209a Interruption forcee : l'allie Khn'nr devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk209b engage, PV soignes » VERT; « k209a valeurs imprimees de l'allie : PV 3, ATQ avec 1 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT; « k209a attaque : subit ses 1 degat(s) consequentiel(s) (les pastilles de l'ATQ) et peut attaquer le mechant » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk209b : Khn'nr

- [x] Etape 2 : carte(s) de reference : `sk098`, `44038`, `sk189b` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk209b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "2", "SCH": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « k209a Interruption forcee : l'allie Khn'nr devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk209b engage, PV soignes » VERT; « k209b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k209b Une fois vaincu : retire TOUS les jetons de soupcon de Who Do You Trust? » VERT; « k209b TEMOIN : sans la defaite, les 3 jetons restent » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk210a : Captain Marvel (M'lanz)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk210a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "ATK": "2**"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k210a Interruption forcee : l'allie M'lanz devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk210b engage, PV soignes » VERT; « k210a valeurs imprimees de l'allie : PV 4, ATQ avec 2 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk210b : M'lanz

- [x] Etape 2 : carte(s) de reference : `sk098`, `sk162` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk210b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "ATK": "2*", "SCH": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « k210a Interruption forcee : l'allie M'lanz devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk210b engage, PV soignes » VERT; « k210b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k210b ★ Interruption forcee : quand M'lanz t'attaque, son attaque est AUSSI resolue contre chaque autre heros (2 joueurs en forme heros) » VERT; « k210b TEMOIN : un sbire ordinaire (01101) n'attaque que SON joueur, le heros 2 est indemne » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk211a : Carnage (Zr'x)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk211a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "2**"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k211a Interruption forcee : l'allie Zr'x devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk211b engage, PV soignes » VERT; « k211a valeurs imprimees de l'allie : PV 3, ATQ avec 2 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk211b : Zr'x

- [x] Etape 2 : carte(s) de reference : `sk098` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk211b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "2", "SCH": "1", "Toughness": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k211a Interruption forcee : l'allie Zr'x devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk211b engage, PV soignes » VERT; « k211b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k211b Toughness : le sbire entre en jeu avec une carte Robuste » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk212a : Daredevil (Trl'k)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk212a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "2", "ATK": "1*"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « k212a Interruption forcee : l'allie Trl'k devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk212b engage, PV soignes » VERT; « k212a valeurs imprimees de l'allie : PV 2, ATQ avec 1 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT; « k212a attaque : subit ses 1 degat(s) consequentiel(s) (les pastilles de l'ATQ) et peut attaquer le mechant » VERT; « k212a ne peut pas CONTRER : son pouvoir THW ne retire aucune menace » VERT; « k212a Phase du mechant, joueur en ALTER EGO : l'allie maniganche (SCH 2), subit 1 degat consequentiel et ne s'incline pas » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk212b : Trl'k

- [x] Etape 2 : carte(s) de reference : `sk098` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk212b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "2", "ATK": "1", "SCH": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « k212a Interruption forcee : l'allie Trl'k devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk212b engage, PV soignes » VERT; « k212b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k212b ne peut pas subir de degats tant que le joueur engage est engage avec un AUTRE sbire SKRULL (Skrull Warrior sk110) » VERT; « k212b TEMOIN : seul engage, Trl'k subit les 3 degats » VERT; « k199 Chaos on the Battlefield : X = SCH total des IMPOSTOR en jeu (allie sk208a SCH 1 + sbire sk212b SCH 2 = 3) : 1 + 3 = 4 menaces » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk213a : Deathlok (Fry'lu)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk213a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "2**"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k213a Interruption forcee : l'allie Fry'lu devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk213b engage, PV soignes » VERT; « k213a valeurs imprimees de l'allie : PV 3, ATQ avec 2 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk213b : Fry'lu

- [x] Etape 2 : carte(s) de reference : `sk098`, `44038`, `21128` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk213b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "2", "SCH": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k213a Interruption forcee : l'allie Fry'lu devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk213b engage, PV soignes » VERT; « k213b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k213b Une fois vaincu : le joueur qui l'a vaincu recoit une carte rencontre FACE CACHEE » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk214a : Dum Dum Dugan (Sn'Tlo)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk214a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "ATK": "1*"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k214a Interruption forcee : l'allie Sn'Tlo devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk214b engage, PV soignes » VERT; « k214a valeurs imprimees de l'allie : PV 4, ATQ avec 1 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk214b : Sn'Tlo

- [x] Etape 2 : carte(s) de reference : `sk098` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk214b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "ATK": "1", "SCH": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « k214a Interruption forcee : l'allie Sn'Tlo devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk214b engage, PV soignes » VERT; « k214b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k214b Reduit de 1 les degats de chaque attaque : l'ATQ 2 de Spider-Man n'en inflige que 1 » VERT; « k214b TEMOIN : un sbire ordinaire subit les 2 degats de la meme attaque » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk215a : Elektra (Siri)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk215a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "ATK": "2**"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k215a Interruption forcee : l'allie Siri devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk215b engage, PV soignes » VERT; « k215a valeurs imprimees de l'allie : PV 4, ATQ avec 2 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk215b : Siri

- [x] Etape 2 : carte(s) de reference : `sk098` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk215b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "ATK": "2", "SCH": "1", "Patrol": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k215a Interruption forcee : l'allie Siri devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk215b engage, PV soignes » VERT; « k215b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k215b Patrol : mot-cle natif, le joueur engage ne peut pas contrer le complot principal » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk216a : Giant-Man (D'lutz)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk216a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "ATK": "2**"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k216a Interruption forcee : l'allie D'lutz devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk216b engage, PV soignes » VERT; « k216a valeurs imprimees de l'allie : PV 4, ATQ avec 2 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk216b : D'lutz

- [x] Etape 2 : carte(s) de reference : `sk098` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk216b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "ATK": "2", "SCH": "1", "Retaliate": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k216a Interruption forcee : l'allie D'lutz devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk216b engage, PV soignes » VERT; « k216b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k216b Retaliate 1 : le heros qui l'attaque subit 1 degat » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk217a : Invisible Woman (De'Lila)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk217a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "1*"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k217a Interruption forcee : l'allie De'Lila devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk217b engage, PV soignes » VERT; « k217a valeurs imprimees de l'allie : PV 3, ATQ avec 1 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk217b : De'Lila

- [x] Etape 2 : carte(s) de reference : `sk098`, `sk123`, `58027` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk217b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "1", "SCH": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « k217a Interruption forcee : l'allie De'Lila devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk217b engage, PV soignes » VERT; « k217b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k217b Cout additionnel : pour l'attaquer il faut depenser 1 ressource (la carte 01088 de la main est depensee) » VERT; « k217b Cout additionnel : sans ressource a depenser, l'attaque n'a pas lieu (aucun degat) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk218a : Iron Fist (Grrix)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk218a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "1*"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k218a Interruption forcee : l'allie Grrix devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk218b engage, PV soignes » VERT; « k218a valeurs imprimees de l'allie : PV 3, ATQ avec 1 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk218b : Grrix

- [x] Etape 2 : carte(s) de reference : `sk098`, `sk100` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk218b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "1", "SCH": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « k218a Interruption forcee : l'allie Grrix devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk218b engage, PV soignes » VERT; « k218b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k218b Une fois vaincu : le mechant attaque le joueur qui l'a vaincu, MEME SI ce joueur est en alter ego » VERT; « k218b TEMOIN : tant que Grrix vit, le mechant n'attaque pas » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk219a : Iron Man (Ssrov)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk219a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "ATK": "2**"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k219a Interruption forcee : l'allie Ssrov devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk219b engage, PV soignes » VERT; « k219a valeurs imprimees de l'allie : PV 4, ATQ avec 2 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk219b : Ssrov

- [x] Etape 2 : carte(s) de reference : `sk098` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk219b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "ATK": "2*", "SCH": "1*"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « k219a Interruption forcee : l'allie Ssrov devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk219b engage, PV soignes » VERT; « k219b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k219b ★ Tant que le mechant est CAMOUFLAGED : SCH et ATQ imprimes (1 / 2) » VERT; « k219b ★ Tant que le mechant est REVEALED (Queen Veranke) : +1 SCH et +1 ATQ (2 / 3), puis retour a 1 / 2 quand elle se camoufle » VERT; « k219b ★ +1 SCH +1 ATQ : le bonus RETOMBE quand le mechant repasse CAMOUFLAGED » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk220a : Moon Knight (Hs'fld)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk220a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "2**"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k220a Interruption forcee : l'allie Hs'fld devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk220b engage, PV soignes » VERT; « k220a valeurs imprimees de l'allie : PV 3, ATQ avec 2 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk220b : Hs'fld

- [x] Etape 2 : carte(s) de reference : `sk098`, `44038` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk220b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "2", "SCH": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k220a Interruption forcee : l'allie Hs'fld devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk220b engage, PV soignes » VERT; « k220b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k220b Une fois vaincu : le joueur qui l'a vaincu met un allie CAMOUFLAGED du paquet en jeu sous son controle » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk221a : Nick Fury (H'kurrek)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk221a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "2", "ATK": "2*"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k221a Interruption forcee : l'allie H'kurrek devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk221b engage, PV soignes » VERT; « k221a valeurs imprimees de l'allie : PV 2, ATQ avec 1 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk221b : H'kurrek

- [x] Etape 2 : carte(s) de reference : `sk098`, `sk162` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk221b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "2", "ATK": "2*", "SCH": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 8/8 cas verts : « k221a Interruption forcee : l'allie H'kurrek devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk221b engage, PV soignes » VERT; « k221b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k221b ★ Ses attaques gagnent OVERKILL : un allie qui defend a 1 PV restant, l'exces d'un degat passe au heros » VERT; « k221b TEMOIN overkill : Hydra Mercenary (ATQ 1) contre le meme defenseur : pas d'exces, le heros est indemne » VERT; « k221b ★ Ses attaques gagnent PIERCING : le heros Robuste subit quand meme les 2 degats » VERT; « k221b TEMOIN piercing : Hydra Mercenary contre le heros Robuste : la carte Robuste absorbe, aucun degat » VERT; « k221b ★ Ses attaques gagnent RANGED : le defenseur 04014 U.S. Agent (Riposte) ne riposte pas » VERT; « k221b TEMOIN ranged : Hydra Mercenary contre U.S. Agent (Riposte 1) : il subit 1 degat » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/8 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk222a : Phoenix (Korya)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk222a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "2**"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k222a Interruption forcee : l'allie Korya devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk222b engage, PV soignes » VERT; « k222a valeurs imprimees de l'allie : PV 3, ATQ avec 2 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk222b : Korya

- [x] Etape 2 : carte(s) de reference : `sk098`, `sk150`, `32073`, `gb022` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk222b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "2*", "SCH": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « k222a Interruption forcee : l'allie Korya devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk222b engage, PV soignes » VERT; « k222b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k222b ★ Reponse forcee : apres qu'elle t'attaque, la carte du dessus de TON deck est defaussee (deck de 3 cartes : le temoin suivant en perd 1 par la pioche, Korya en perd 2) » VERT; « k222b TEMOIN : un sbire ordinaire (01101) qui attaque ne defausse rien du deck » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk223a : Spider-Man (Ch'Gra)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk223a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "2", "ATK": "2*"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k223a Interruption forcee : l'allie Ch'Gra devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk223b engage, PV soignes » VERT; « k223a valeurs imprimees de l'allie : PV 2, ATQ avec 1 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk223b : Ch'Gra

- [x] Etape 2 : carte(s) de reference : `sk098`, `44038` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk223b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "2", "ATK": "2", "SCH": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k223a Interruption forcee : l'allie Ch'Gra devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk223b engage, PV soignes » VERT; « k223b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k223b Une fois vaincu : retourne Queen Veranke (sk189b -> Spider-Woman sk189a) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk224a : Thor (Hagar)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk224a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "ATK": "2**"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k224a Interruption forcee : l'allie Hagar devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk224b engage, PV soignes » VERT; « k224a valeurs imprimees de l'allie : PV 4, ATQ avec 2 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk224b : Hagar

- [x] Etape 2 : carte(s) de reference : `sk098`, `sk166` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk224b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "ATK": "2*", "SCH": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k224a Interruption forcee : l'allie Hagar devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk224b engage, PV soignes » VERT; « k224b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k224b ★ Ses attaques infligent des degats INDIRECTS : le defenseur n'encaisse rien » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk225a : Venom (Dharr)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk225a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "1*"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k225a Interruption forcee : l'allie Dharr devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk225b engage, PV soignes » VERT; « k225a valeurs imprimees de l'allie : PV 3, ATQ avec 1 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk225b : Dharr

- [x] Etape 2 : carte(s) de reference : `sk098` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk225b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "1", "SCH": "2", "Villainous": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k225a Interruption forcee : l'allie Dharr devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk225b engage, PV soignes » VERT; « k225b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k225b Villainous : mot-cle natif, une carte de boost a chaque activation » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk226a : Wolverine (V'lrym)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk226a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "2*"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k226a Interruption forcee : l'allie V'lrym devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk226b engage, PV soignes » VERT; « k226a valeurs imprimees de l'allie : PV 3, ATQ avec 1 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk226b : V'lrym

- [x] Etape 2 : carte(s) de reference : `sk098` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk226b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "2", "SCH": "1", "Quickstrike": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k226a Interruption forcee : l'allie V'lrym devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk226b engage, PV soignes » VERT; « k226b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k226b Quickstrike : en arrivant engage avec un heros, il attaque immediatement (au moins 2 degats) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk227a : Yellowjacket (Criti Noll)

- [x] Etape 2 : carte(s) de reference : `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk227a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « would LEAVE play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "1*"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « k227a Interruption forcee : l'allie Criti Noll devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk227b engage, PV soignes » VERT; « k227a valeurs imprimees de l'allie : PV 3, ATQ avec 1 degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL » VERT; « k227a ne peut pas CONTRER : son pouvoir THW ne retire aucune menace » VERT; « k227a Phase du mechant, joueur en ALTER EGO : l'allie maniganche (SCH 3), subit 1 degat consequentiel et ne s'incline pas » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI

### sk227b : Criti Noll

- [x] Etape 2 : carte(s) de reference : `sk098` (detail et justification en tete de `src/cards/pack/skrull_menace/secret_invasion/sk227b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « heal ALL damage »; « engaged with YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "ATK": "1", "SCH": "3", "Incite": "3"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k227a Interruption forcee : l'allie Criti Noll devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire sk227b engage, PV soignes » VERT; « k227b Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur) » VERT; « k227b Incite 3 : a la revelation, 3 menaces sur le complot principal » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte double face : le plateau montre la face courante (mecanisme de retournement existant, Spiral / Typhoid Mary) ; pas de test plateau dedie (allie <-> sbire, la carte change de zone)).

Carte terminée : OUI
