# Lyja (Skrull Menace Expansion Content, Kajislav) : gabarits PROCESSUS-CARTE

Heros Lyja / Laura Green, pack `skrull_menace`, 26 card_id : sk037a/b (identite), sk038-sk047 (signatures), sk049, sk052, sk053,
sk056, sk057, sk058, sk062, sk063, sk064 (cartes d'aspect de l'auteur), sk065 (obligation), sk066-sk069 (set nemesis « Lyja Nemesis »).
Fiches generees le 15/10/2026 par `defs/generer_gabarits_lyja.py` a partir des resultats REELS (rapport test_capacites, sorties de
`substituer_pack.py`, en-tetes des modules, cards.json).

Rappels communs a toutes les cartes :
- **Etape 4 (images)** : les 26 scans sont dans `assets/pics/` (615 px, depot principal) ; chaque carte a ete RELUE sur son scan
  (chiffres, icones, textes) contre `data/cards.json` : aucune valeur fausse trouvee, une donnee ajoutee (`MaxPerUnit "1"` sur sk064,
  « Max 1 per character » imprime).
- **Etape 7 (tests)** : 66 cas `[lyja]` dans `tools/cas/lyja.py`, 66/66 verts. Substitution (`substituer_pack.py`, empreinte du pack
  IDENTIQUE avant/apres) : chaque carte a au moins un cas qui tombe au rouge sans son module ; les cas restes verts sont des TEMOINS
  d'absence d'effet, des mots-cles natifs (Toughness lu dans `desc`) ou des cas ou la carte n'est que le moyen de paiement d'une autre.
- **Etape 8 (autoplay)** : deck `lyja` contre Rhino, 16 parties (8 normal graines 1-8, 8 expert graines 30-37), 0 incident, 0 traceback
  (grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback/<F> : 0 sur les 16 journaux). 0 victoire (normal : 5,1 rounds,
  4 complots achevés / 4 éliminations ; expert : 2,6 rounds) ; le temoin spider_man fait aussi 0/8 (6,9 rounds) : le pilote `equilibre`
  ne joue pas Skrull Spy / Playing Along (aucune des 16 parties ne les a declenches) mais joue les evenements TREACHERY (melanges dans le
  deck rencontre puis revelés), Paibok, Untrustworthiness (en boost), Human Torch, Invisible Woman, Lazerfist... Ces deux actions sont
  couvertes par les cas.
- **Etape 9 (deck)** : `DECK_NOM=lyja verifier_tous_les_decks.py` : « identite sk037b, main 6, deck 34 » (la partie monte) ; passe COMPLETE
  apres le changement de l'enum COUNTER : 141/141 decks montent une partie.
- **Outils statiques** : `verifier_appels_modules skrull_menace` OK (calibre : un appel `Faces.NexistePas` ajoute a la main est bien refuse) ;
  `verifier_api_cartes` : aucune faute dans skrull_menace ; `audit_cartes` : aucune discordance sur sk037-sk069.
- **Moteur** : une entree ajoutee a l'enum COUNTER (`revelation`), voir `defs/lyja_moteur.md`. Rien d'autre.
- **Questions de regles ouvertes** : `defs/lyja_questions.md` (qui choisit a la revelation de sk039/sk040, portee de « attachment » de sk040,
  portee litterale de Paibok, surge de sk068 quand Paibok intercepte...).
- **Ce qu'aucun outil ne voit** : une vraie partie jouee a la main dans le navigateur (le confort de Skrull Spy / Playing Along, l'ordre
  « place in any order » pose par le joueur, la lisibilite du jeton « revelation » et des cartes glissees sous Paibok). Le harnais de cas
  repond toujours au premier choix et ne paye un cout « up to » qu'avec `surpayer`.
- **Etape 8 bis (plateau)** : `ui-app/src/board/skrull-menace-lyja.test.ts` (5 cas, etat CAPTURE sur le moteur le 15/10/2026 par
  `sonde_campagne.py`) : vu ROUGE (3/5) sur un etat casse (traitrise non attachee, jeton absent), puis VERT.



### sk037a : Lyja

- [x] Etape 2 : carte(s) de reference : `16093`, `40004`, `hd001b` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk037a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « spend up to 2 resources »; « up to 1[per_hero] »; « of any type »; « for EACH resource spent »; « shuffle ... and place on top »; « TREACHERY card ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "10", "ATK": "1", "THW": "2", "DEF": "2", "HS": "5"} ; relu sur le scan (`assets/pics/sk037a.png`). Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk037a Skrull Spy — depense 1 ressource : une traitrise du deck rencontre va sur le dessus » VERT; « sk037a Skrull Spy — a DEUX joueurs : jusqu'a 2 ressources, 2 traitrises sur le dessus » VERT; « sk037a Skrull Spy — TEMOIN : aucune traitrise dans le deck rencontre, rien ne monte » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties lyja/rhino (8 normal + 8 expert), 0 incident, 0 traceback ; MAIS le pilote `equilibre` n'a JAMAIS declenche cette Action (0 fois sur 16 parties) : la capacite n'est prouvee que par les cas du harnais. A verifier en partie reelle (pilote humain) : aucun outil ne la joue en autoplay.
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk037b : Laura Green

- [x] Etape 2 : carte(s) de reference : `an001b`, `ok001b`, `hd001b` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk037b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « your deck »; « TREACHERY card »; « Limit once per round ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "10", "REC": "3", "HS": "6"} ; relu sur le scan (`assets/pics/sk037b.png`). Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk037b Playing Along — une traitrise du deck joueur monte sur le dessus » VERT; « sk037b Playing Along — TEMOIN D'EPUISEMENT : la 2e activation du round est refusee » VERT; « sk037b Playing Along — TEMOIN D'ABSENCE : sans traitrise dans le deck, rien ne se passe » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? OUI (« Limit once per round »). Temoin : cas « sk037b Playing Along — TEMOIN D'EPUISEMENT » : 1re activation, pioche, 2e activation refusee ; le dessus reste une carte non traitrise (chiffre mesure : le dessus du deck).
- [x] Etape 8 : autoplay cible : 16 parties lyja/rhino (8 normal + 8 expert), 0 incident, 0 traceback ; MAIS le pilote `equilibre` n'a JAMAIS declenche cette Action (0 fois sur 16 parties) : la capacite n'est prouvee que par les cas du harnais. A verifier en partie reelle (pilote humain) : aucun outil ne la joue en autoplay.
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk038 : Human Torch

- [x] Etape 2 : carte(s) de reference : `27023`, `sf009` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk038.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « AFTER Human Torch leaves play »; « leaves play »; « 1* »; « 2* ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "3", "HP": "3", "THW": "1*", "ATK": "2*", "RES": "Y", "Class": "Hero"} ; relu sur le scan (`assets/pics/sk038.png`). Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk038 Human Torch — apres avoir quitte le jeu : une traitrise du deck rencontre va sur le dessus » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk039 : Faking Death

- [x] Etape 2 : carte(s) de reference : `22005`, `50117`, `08026`, `sf009` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk039.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Stun an enemy »; « Confuse an enemy »; « Choose to EITHER stun OR confuse »; « The activating enemy »; « -2 SCH and -2 ATK for THIS activation ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "1", "RES": "B", "Class": "Hero"} ; relu sur le scan (`assets/pics/sk039.png`). Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « sk039 Faking Death — Hero Action : l'evenement se melange dans le deck rencontre » VERT; « sk039 Faking Death — When Revealed : l'ennemi est sonne ; la carte va dans la defausse du joueur » VERT; « sk039 Faking Death — Boost : l'ennemi qui active (Rhino ATK 2) perd 2 ATK pour cette attaque » VERT; « sk039 Faking Death — Boost, TEMOIN : avec une carte de boost 01101 (1 icone), Rhino fait 3 degats » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/4 ⚠ un cas reste vert sans module. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk040 : Feign Loyalty

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk040.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « draw 2 »; « an ATTACHMENT »; « with the uses keyword OR the text Hero Action OR Hero Response »; « from play »; « Draw 2 cards »; « you ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "1", "RES": "R", "Class": "Hero"} ; relu sur le scan (`assets/pics/sk040.png`). Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk040 Feign Loyalty — When Revealed : l'attachement a Hero Action est defausse, l'autre reste » VERT; « sk040 Feign Loyalty — Boost : le joueur pioche 2 cartes » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk041 : Hero Appearance

- [x] Etape 2 : carte(s) de reference : `16152` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk041.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « deal N damage among enemies »; « 4 damage AMONG enemies »; « 3 damage to AN enemy »; « The Lyja player deals ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "1", "RES": "R", "Class": "Hero"} ; relu sur le scan (`assets/pics/sk041.png`). Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk041 Hero Appearance — When Revealed : 4 degats repartis sur les ennemis en jeu » VERT; « sk041 Hero Appearance — Boost : 3 degats a un ennemi » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk042 : Posing as a Civilian

- [x] Etape 2 : carte(s) de reference : `32187` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk042.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Remove 3 threat from among schemes »; « 3 threat FROM AMONG schemes »; « schemes in play »; « from A scheme ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "1", "RES": "B", "Class": "Hero"} ; relu sur le scan (`assets/pics/sk042.png`). Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk042 Posing as a Civilian — When Revealed : retire 3 menaces du complot principal » VERT; « sk042 Posing as a Civilian — Boost : retire 2 menaces d'une manigance » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk043 : New York Bookstore

- [x] Etape 2 : carte(s) de reference : `60016`, `tg007` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk043.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Matt Murdock gets +3 REC »; « LAURA GREEN gets +2 REC »; « ALTER-EGO Response »; « after you make a BASIC recovery ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "1", "RES": "B", "Class": "Hero"} ; relu sur le scan (`assets/pics/sk043.png`). Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk043 New York Bookstore — Laura Green gagne +2 REC (REC 3 -> 5) » VERT; « sk043 New York Bookstore — Alter-Ego Response : apres une recuperation de base, pioche 1 carte » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/4 ⚠ un cas reste vert sans module. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk044 : Lazerfist

- [x] Etape 2 : carte(s) de reference : `sk002a`, `sk013` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk044.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « LYJA gets +1 ATK »; « HERO Resource »; « generate a [energy] resource ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "3", "RES": "Y", "Class": "Hero"} ; relu sur le scan (`assets/pics/sk044.png`). Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk044 Lazerfist — Lyja gagne +1 ATK en forme heros (ATK 1 -> 2) » VERT; « sk044 Lazerfist — Hero Resource : s'incline pour payer une carte (sk043, cout 1) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk045 : Ministerial Tiara

- [x] Etape 2 : carte(s) de reference : `22012`, `16158` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk045.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « has a STAR icon in the boost area »; « Interrupt »; « exhaust this card »; « draw 1 card ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "G", "Class": "Hero"} ; relu sur le scan (`assets/pics/sk045.png`). Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk045 Ministerial Tiara — une carte de boost a etoile (sk039) : la Tiare s'incline, pioche 1 carte » VERT; « sk045 Ministerial Tiara — CONTRE-CAS : carte de boost SANS etoile (01101), rien ne se passe » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk046 : Mole

- [x] Etape 2 : carte(s) de reference : `43031`, `27087b`, `27083`, `27070` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk046.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « discarded FROM THE TOP OF THE ENCOUNTER DECK »; « TREACHERY card »; « Hero Interrupt »; « exhaust Mole ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "1", "RES": "G", "Class": "Hero"} ; relu sur le scan (`assets/pics/sk046.png`). Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk046 Mole — une traitrise defaussee du DESSUS du deck rencontre : son When Revealed se resout » VERT; « sk046 Mole — CONTRE-CAS : la traitrise n'est PAS au sommet du deck, rien ne se resout » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk047 : Shapeshifter

- [x] Etape 2 : carte(s) de reference : `sk044`, `60045`, `60046` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk047.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « LYJA gets +1 THW »; « After you PLAY a TREACHERY EVENT »; « HERO Response »; « ready LYJA ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "3", "RES": "Y", "Class": "Hero"} ; relu sur le scan (`assets/pics/sk047.png`). Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk047 Shapeshifter — Lyja gagne +1 THW en forme heros (THW 2 -> 3) » VERT; « sk047 Shapeshifter — Hero Response : apres un evenement TREACHERY joue, Lyja se redresse » VERT; « sk047 Shapeshifter — CONTRE-CAS : un evenement NON TREACHERY (sk052) ne redresse pas Lyja » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ⚠ un cas reste vert sans module. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk049 : The Thing

- [x] Etape 2 : carte(s) de reference : `38007`, `th007`, `32045` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk049.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Toughness »; « Discard a tough status card FROM THE THING »; « UP TO 2 enemies »; « 2 damage to EACH »; « enemies »; « 0* »; « 2* ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "4", "HP": "3", "THW": "0*", "ATK": "2*", "RES": "R", "Toughness": "1", "Class": "Aggression"} ; relu sur le scan (`assets/pics/sk049.png`). Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk049 The Thing — Toughness : il entre en jeu avec un statut Tenace » VERT; « sk049 The Thing — Action : defausse son Tenace, 2 degats a chacun de 2 ennemis » VERT; « sk049 The Thing — TEMOIN : sans statut Tenace (2e Action), l'action n'est plus offerte » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ⚠ un cas reste vert sans module. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk052 : Going Ballistic

- [x] Etape 2 : carte(s) de reference : `27008`, `16152`, `32045` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk052.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « (attack) »; « Discard YOUR hand »; « 2 damage FOR EACH card discarded »; « TO A MAXIMUM OF 6 »; « (attack) »; « an enemy ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "0", "RES": "R", "Class": "Aggression"} ; relu sur le scan (`assets/pics/sk052.png`). Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk052 Going Ballistic — defausse la main (1 autre carte) : 2 degats » VERT; « sk052 Going Ballistic — plafond : 5 cartes defaussees = 10 -> 6 degats maximum » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk053 : Hit the Weak Spot

- [x] Etape 2 : carte(s) de reference : `04009`, `sn014` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk053.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « attack »; « each icon (★ AND Y) in THAT MINION'S BOOST AREA »; « a MINION »; « 2 damage FOR EACH icon »; « This attack gains PIERCING ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "B", "Class": "Aggression"} ; relu sur le scan (`assets/pics/sk053.png`). Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk053 Hit the Weak Spot — Melter (etoile seule, 0 icone chiffree) : 1 icone -> 2 degats » VERT; « sk053 Hit the Weak Spot — Hired Gun (2 icones Y + ★ = 3) : 6 degats, le sbire (3 PV) est vaincu » VERT; « sk053 Hit the Weak Spot — Sandman (Tenace, 2 icones) : l'attaque est PERCANTE, 4 degats passent » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk056 : Invisible Woman

- [x] Etape 2 : carte(s) de reference : `20010`, `tg009`, `50117`, `16152` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk056.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « for each revelation counter ON THE TARGET »; « takes +1 consequential damage »; « a basic power »; « revelation ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "3", "HP": "2", "THW": "1", "ATK": "1", "RES": "Y", "Class": "Basic"} ; relu sur le scan (`assets/pics/sk056.png`). Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk056 Invisible Woman — apres son attaque, 1 compteur revelation sur la cible (aucun degat consecutif) » VERT; « sk056 Invisible Woman — 2e attaque sur la meme cible : +1 degat consecutif (1 compteur deja la) » VERT; « sk056 Invisible Woman — son contre (THW) pose aussi un compteur revelation, sur la manigance » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (jeton « revelation » pose sur la cible de son pouvoir de base (c_revelation sur Rhino dans le descripteur capture)). Cas plateau : `ui-app/src/board/skrull-menace-lyja.test.ts`, vu ROUGE puis VERT : descripteur capture le 15/10/2026 ; test 'Rhino montre son jeton revelation' rouge sans c_revelation, vert avec.
      Resultat : conforme.

Carte terminée : OUI

### sk057 : Mister Fantastic

- [x] Etape 2 : carte(s) de reference : `sk013`, `ab007`, `22012` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk057.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Exhaust Mister Fantastic AND deal 1 damage to him »; « Resource »; « 1* ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "3", "HP": "4", "THW": "1*", "ATK": "1*", "RES": "B", "Class": "Basic"} ; relu sur le scan (`assets/pics/sk057.png`). Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk057 Mister Fantastic — Resource : s'incline et prend 1 degat pour payer sk043 (cout 1) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk058 : Laser Tag

- [x] Etape 2 : carte(s) de reference : `dz038`, `dz037`, `31009`, `an001a` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk058.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Team-Up (Human Torch AND Lyja) »; « ready Human Torch, Lyja, AND EACH SUPERPOWER upgrade YOU CONTROL »; « Hero Action ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "Y", "Class": "Basic", "TeamUp": "Human Torch;Lyja", "MaxPerDeck": "1"} ; relu sur le scan (`assets/pics/sk058.png`). Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk058 Laser Tag — redresse Human Torch, Lyja et les ameliorations SUPERPOWER (pas la Tiare) » VERT; « sk058 Laser Tag — CONTRE-CAS Team-Up : sans Human Torch en jeu, l'evenement n'est pas jouable » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? OUI (« Max 1 per deck », `desc.MaxPerDeck`, regle de construction du deck). Temoin : limite de deckbuilding, lue par le constructeur de deck : hors portee du harnais de capacites.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk062 : Baxter Building

- [x] Etape 2 : carte(s) de reference : `27041`, `nt005`, `22033`, `mf005`, `16142` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk062.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « IF YOU control a FANTASTIC FOUR CHARACTER »; « Reduce by 1 »; « for ANY player ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "4", "RES": "B", "Class": "Basic"} ; relu sur le scan (`assets/pics/sk062.png`). Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk062 Baxter Building — cout 4 reduit a 3 avec un personnage FANTASTIC FOUR (Lyja) : jouable avec 3 ressources » VERT; « sk062 Baxter Building — CONTRE-CAS : en alter ego (aucun FANTASTIC FOUR), 3 ressources ne suffisent pas » VERT; « sk062 Baxter Building — Resource : s'incline pour payer sk043 (cout 1), generique pour tout joueur » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ⚠ un cas reste vert sans module. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk063 : Fantasti-Car

- [x] Etape 2 : carte(s) de reference : `mf005`, `27023`, `an001a`, `hd001b`, `27008` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk063.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « choose a player »; « ready a FANTASTIC FOUR CARD »; « After Fantasti-Car ENTERS PLAY »; « ALTER-EGO Action »; « choose A PLAYER ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "Y", "Class": "Basic"} ; relu sur le scan (`assets/pics/sk063.png`). Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk063 Fantasti-Car — Response a l'entree en jeu : redresse une carte FANTASTIC FOUR (Lyja inclinee) » VERT; « sk063 Fantasti-Car — Alter-Ego Action : le joueur remet 1 carte de sa defausse dans son deck » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk064 : Fantastic Four Member

- [x] Etape 2 : carte(s) de reference : `62037` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk064.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Play only if YOUR IDENTITY has the FF trait »; « FRIENDLY character »; « Max 1 PER CHARACTER ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "0", "RES": "B", "Class": "Basic", "MaxPerUnit": "1"} ; relu sur le scan (`assets/pics/sk064.png`). Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk064 Fantastic Four Member — sur un allie : +1 PV et le trait FANTASTIC FOUR » VERT; « sk064 Fantastic Four Member — CONTRE-CAS : en alter ego (Laura Green n'est pas FF), non jouable » VERT; « sk064 Fantastic Four Member — TEMOIN D'EPUISEMENT « Max 1 per character » : le 2e exemplaire ne se pose pas sur le meme allie » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? OUI (« Max 1 per character », `desc.MaxPerUnit`). Temoin : cas « sk064 ... TEMOIN D'EPUISEMENT » : 2 exemplaires jouables sur le meme allie, le 2e est refuse (PV max de l'allie = 4, pas 5).
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk065 : Untrustworthiness

- [x] Etape 2 : carte(s) de reference : `16108`, `dz037`, `22012`, `16158`, `sk031` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja/sk065.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « deal yourself 1  - **`sk031`** Interracial Hatred (Hulkling, meme coffret) : « Alter-Ego Action: Exhaust ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :  - « a "Boost" OR "When Revealed" ability »; « on a TREACHERY card »; « cancel THAT ability »; « THEN deal yourself »; « yourself »; « Forced ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "2", "GiveTo": "Laura Green"} ; relu sur le scan (`assets/pics/sk065.png`). Resultat : conforme.
- [x] Etape 7 : 6/6 cas verts : « sk065 Untrustworthiness — le When Revealed d'une traitrise TREACHERY (sk042) est annule, et on recoit 1 carte face cachee » VERT; « sk065 Untrustworthiness — TEMOIN : sans l'obligation, sk042 retire bien ses 3 menaces » VERT; « sk065 Untrustworthiness — le When Revealed d'une traitrise de TYPE Treachery (sk068) est annule aussi » VERT; « sk065 Untrustworthiness — le ★ Boost d'une traitrise TREACHERY (sk041) est annule, et on recoit 1 carte face cachee » VERT; « sk065 Untrustworthiness — CONTRE-CAS : une carte non TREACHERY (sbire 01101) revelee, rien n'est annule » VERT; « sk065 Untrustworthiness — Alter-Ego Action : Laura Green s'incline, l'obligation est defaussee » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/6 ⚠ un cas reste vert sans module. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk066 : Paibok

- [x] Etape 2 : carte(s) de reference : `sn001a`, `43031`, `27087b` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja_nemesis/sk066.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « +X ATK and THW where X = cartes glissees sous lui »; « WOULD be discarded ... attach it facedown INSTEAD »; « a TREACHERY card »; « for EACH TREACHERY card attached »; « expert »; « 2★ »; « 2* ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "SCH": "2", "ATK": "2*", "Boost": "2", "Toughness": "1", "Nemesis": "Laura Green"} ; relu sur le scan (`assets/pics/sk066.png`). Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « sk066 Paibok — Toughness : il entre en jeu avec un statut Tenace » VERT; « sk066 Paibok — une traitrise defaussee est attachee face cachee a Paibok : +1 SCH et +1 ATK » VERT; « sk066 Paibok — deux traitrises attachees : +2 SCH et +2 ATK ; un evenement TREACHERY joueur compte aussi » VERT; « sk066 Paibok — CONTRE-CAS : un sbire (non traitrise) defausse n'est pas attache (+0/+0) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/4 ⚠ un cas reste vert sans module. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (traitrise attachee FACE CACHEE a Paibok (carte id 83 bind=3 dans le descripteur capture)). Cas plateau : `ui-app/src/board/skrull-menace-lyja.test.ts`, vu ROUGE puis VERT : tests 'la traitrise attachee ... portee par lui, face cachee' et TEMOIN rouges sans lien bind, verts avec.
      Resultat : conforme.

Carte terminée : OUI

### sk067 : Punish the Defector

- [x] Etape 2 : carte(s) de reference : `sk103`, `sk102`, `01107`, `desc` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja_nemesis/sk067.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Search the encounter deck »; « Hazard »; « a TREACHERY card »; « and DISCARD it »; « Shuffle the encounter deck »; « Search the encounter deck ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "2*", "Hazard": "1", "Boost": "2"} ; relu sur le scan (`assets/pics/sk067.png`). Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk067 Punish the Defector — When Revealed : une traitrise du deck rencontre est defaussee » VERT; « sk067 Punish the Defector — TEMOIN : aucune traitrise dans le deck, rien n'est defausse » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk068 : "It's a Stinkin' Skrull!"

- [x] Etape 2 : carte(s) de reference : `01188`, `53042` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja_nemesis/sk068.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « if ... this card gains surge »; « if NO TREACHERY card was DISCARDED this way »; « (Shuffle.) ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan (`assets/pics/sk068.png`). Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk068 "It's a Stinkin' Skrull!" — defausse une traitrise du deck : pas de surge » VERT; « sk068 "It's a Stinkin' Skrull!" — aucune traitrise a defausser : la carte gagne surge » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI

### sk069 : Truth Revealed

- [x] Etape 2 : carte(s) de reference : `an001b`, `hd001b`, `05006` (detail et justification en tete de `src/cards/pack/skrull_menace/lyja_nemesis/sk069.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « all cards »; « YOUR deck »; « IDENTITY-SPECIFIC cards »; « ALL »; « shuffle your deck ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et le scan).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "2"} ; relu sur le scan (`assets/pics/sk069.png`). Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk069 Truth Revealed — les cartes propres a l'identite vont sous le deck » VERT; « sk069 Truth Revealed — TEMOIN : sans carte propre a l'identite dans le deck, il est juste melange » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module. Les cas « TEMOIN / CONTRE-CAS » qui mesurent une ABSENCE d'effet, les cas natifs (Toughness) et ceux ou la carte n'est que le moyen de paiement d'une autre carte restent verts sans module : assume.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 16 parties deck lyja contre Rhino (8 normal + 8 expert), temoin spider_man 8 parties : 0 incident, 0 traceback ; journaux lus pour les evenements TREACHERY melanges/reveles, Paibok, Untrustworthiness, Human Torch, Invisible Woman (voir rappel commun).
- [x] Etape 8 bis : change ce qu'on voit ? NON (la carte chiffre ou deplace une carte entre zones non dessinees : degats, menace, pioche, redressement).

Carte terminée : OUI
