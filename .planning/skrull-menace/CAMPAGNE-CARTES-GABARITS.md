# Cartes de campagne (sk263-sk289b) — gabarits PROCESSUS-CARTE

Un gabarit par card_id (26 cartes numerotees + le rappel sans numero sk289a / sk289b), rempli avec les resultats REELS du
15/10/2026 : cas `tools/cas/campagne_cartes.py` (110), substitution du bloc (module remplace par `GetAbilities -> []`, empreinte
du dossier identique avant/apres), autoplay du deck `campagne` (26 cartes) et d'un temoin, cas plateau, passes statiques.
Fichier genere par `defs/generer_gabarits_campagne_cartes.py` ; ne pas editer a la main.

## Rappel commun

- **Lecture de la substitution** : « rouges N/M » = N cas sur M tombent sans le module. Les M-N verts restants sont tous soit
  des TEMOINS d'ABSENCE d'effet (restent verts par construction, assume ici), soit des valeurs NATIVES lues dans `desc`
  (Toughness de sk265, icone Acceleration de sk271, Temporary de sk284/sk285), soit le TEMOIN POSITIF d'une restriction (sk275 :
  l'allie SKRULL a le droit de deplacer la menace ; sk281 : jouable avec un allie SKRULL) dont la restriction est prouvee rouge
  par les autres cas. Aucun cas NOMINAL de capacite ne reste vert sans module (liste complete dans la ligne « Substitution »).
- **Alliance de sk280** : le cas est vert sans module (le cout y vaut 0) ; la preuve est une MUTATION (la ligne
  `jouer.cout_en_groupe = True` retiree : le cas passe au ROUGE, remise : VERT), consignee ici et dans `RECETTES-MOTEUR §7octodecies`.
- **Autoplay** (deck `campagne` : Spider-Man + les 26 cartes, 8 parties par scenario, scenarios `rhino`, `sk_paibok`,
  `sk_super_skrull`, `sk_skrull_empire`, temoin `spider_man` de depart) : voir le resume en fin de fichier ; 0 trace
  `Traceback`/`NameError`/`AttributeError`/`TypeError`/`KeyError`/`AssertionError` apres le correctif de `player_action.py`
  (un plantage reel trouve par l'autoplay : sk288, voir `defs/campagne_cartes_moteur.md`). La phase du mechant SAUTEE par sk280
  s'est vue dans 6 parties (journal « --- Phase : Villain (skipped) ---»).
- **Passes statiques** : `verifier_appels_modules` OK (calibre : il a attrape `Message.AfterPlayerEngageMinion n'existe pas`
  dans sk286 avant correction), `verifier_api_cartes` : aucune faute dans skrull_menace.
- **Ce que ces blocs ne voient pas** : une vraie partie jouee par un humain dans le navigateur n'a pas ete faite (aucun outil
  de ce depot ne pilote un navigateur ici). A faire en partie reelle : le texte des cartes a l'ecran (X du cout de Buddy Training
  et de Princess Anelle affiche), les invites de reponse optionnelle, le choix de cible de Xavin (premiere cible legale),
  et la Cooperation Area (autre bloc) qui n'existe pas encore.

### sk263 : Crusader

- [x] Etape 2 : carte(s) de reference : `ho004`, `04006`, `01083` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk263.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "HP": "4", "THW": "2**", "ATK": "2**", "RES": "R", "Class": "Campaign;Aggression"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k263 Crusader : 1 degat au mechant et au sbire engage ; un sbire acheve = 1 carte piochee » VERT; « k263 Crusader : DEUX sbires achieves = 2 cartes piochees (un compte par ennemi vaincu) » VERT; « k263 Crusader, TEMOIN : aucun ennemi achieve = aucune carte piochee » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement : degats et pioche).

Carte terminée : OUI

### sk264 : Jazinda

- [x] Etape 2 : carte(s) de reference : `55063`, `an002`, `06007`, `29004` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk264.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « YOUR hero ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "3", "HP": "4", "THW": "3**", "ATK": "1*", "RES": "B", "Class": "Campaign;Justice"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 6/6 cas verts : « k264 Jazinda : inclinee, le heros gagne +1 CTR (forme heros) » VERT; « k264 Jazinda, TEMOIN : redressee, aucun bonus de CTR » VERT; « k264 Jazinda : elle ne compte PAS contre la limite d'allies (3 allies + Jazinda, tous restent en jeu) » VERT; « k264 Jazinda, TEMOIN : 4 allies SANS Jazinda -> la limite de 3 s'applique (un seul est compte en trop) » VERT; « k264 Jazinda : le bonus de CTR ne profite PAS au heros d'un AUTRE joueur » VERT; « k275 Skrull Military Training : un allie SKRULL (sk264 Jazinda, CTR 3) retire la menace, vainc le complot : pile de victoire » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 3/5 ; VERTS SANS MODULE : [campagne_cartes] sk264 Jazinda, TEMOIN : redressee, aucun bonus de CTR || [campagne_cartes] sk264 Jazinda, TEMOIN : 4 allies SANS Jazinda -> la limite de 3 s'applique (un seul est compte.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (bonus de CTR (chiffre du moteur) et inclinaison, rendus natifs).

Carte terminée : OUI

### sk265 : Paibok

- [x] Etape 2 : carte(s) de reference : `sk066`, `bk007`, `sw014` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk265.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "3", "HP": "4", "THW": "2**", "ATK": "2**", "RES": "R", "Toughness": "1", "Class": "Campaign;Basic"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 6/6 cas verts : « k265 Paibok : entre en jeu avec une carte Robuste (Toughness lu dans le desc) » VERT; « k265 Paibok : apres la defausse d'une traitrise, il prend 1 degat et l'attache face cachee ; +1 THW / +1 ATQ » VERT; « k265 Paibok, TEMOIN : une carte qui n'est PAS une traitrise (sbire) defaussee : rien n'est attache » VERT; « k265 Paibok : un evenement de Lyja portant le trait TREACHERY compte aussi (decision du 15/10/2026) » VERT; « k265 Paibok : « to a maximum of 2 » : la troisieme traitrise defaussee n'est PAS attachee » VERT; « k265 Paibok : tant qu'il est Robuste, le cout « take 1 damage » ne peut pas etre paye (rien n'est attache) » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 3/6 ; VERTS SANS MODULE : [campagne_cartes] sk265 Paibok : entre en jeu avec une carte Robuste (Toughness lu dans le desc) || [campagne_cartes] sk265 Paibok, TEMOIN : une carte qui n'est PAS une traitrise (sbire) defaussee || [campagne_cartes] sk265 Paibok : tant qu'il est Robuste, le cout « take 1 damage » ne peut pas etre pay.
- [x] Etape 7 bis : limite imprimee ? NON de limite par round ; plafond « to a maximum of 2 » (cas dedie).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte glissee face cachee sous l'allie + bonus de CTR/ATQ). Cas plateau : `ui-app/src/board/campagne-cartes-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk266 : Skymax

- [x] Etape 2 : carte(s) de reference : `01083`, `hd012`, `ok001b` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk266.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « ALL allies »; « YOUR discard pile ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "3", "HP": "5", "THW": "2**", "ATK": "3**", "RES": "R", "Class": "Campaign;Leadership"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k266 Skymax : les allies de la defausse retournent dans le deck, pas les autres cartes » VERT; « k266 Skymax, TEMOIN : un allie EN JEU n'est pas touche » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 1/2 ; VERTS SANS MODULE : [campagne_cartes] sk266 Skymax, TEMOIN : un allie EN JEU n'est pas touche.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (melange de cartes dans le deck, aucun rendu propre).

Carte terminée : OUI

### sk267 : Super-Skrull

- [x] Etape 2 : carte(s) de reference : `sk265`, `sk066`, `bk007` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk267.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "3", "HP": "4", "THW": "2**", "ATK": "2**", "RES": "Y", "Class": "Campaign;Basic"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « k267 Super-Skrull : un SUPERPOWER defausse est attache face cachee ; +1 THW / +1 ATQ » VERT; « k267 Super-Skrull : DEUX pouvoirs DIFFERENTS = +2 / +2 » VERT; « k267 Super-Skrull : deux COPIES du meme pouvoir = +1 / +1 seulement (noms distincts) » VERT; « k267 Super-Skrull : « to a maximum of 4 » : le cinquieme SUPERPOWER n'est PAS attache » VERT; « k267 Super-Skrull, TEMOIN : une carte sans le trait SUPERPOWER defaussee : rien n'est attache » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 4/5 ; VERTS SANS MODULE : [campagne_cartes] sk267 Super-Skrull, TEMOIN : une carte sans le trait SUPERPOWER defaussee.
- [x] Etape 7 bis : limite imprimee ? NON de limite par round ; plafond « to a maximum of 4 » (cas dedie).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (cartes SUPERPOWER glissees face cachee sous l'allie). Cas plateau : `ui-app/src/board/campagne-cartes-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk268 : Chilly McHotpants

- [x] Etape 2 : carte(s) de reference : `36038`, `sk098`, `sk243` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk268.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "0", "HP": "5", "THW": "2", "ATK": "2", "RES": "R", "Class": "Campaign;'Pool"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « k268 Chilly McHotpants : entre en jeu comme un SBIRE engage avec le joueur (MNG 2, ATQ 2, 5 PV) » VERT; « k268 Chilly McHotpants : ne compte PAS contre la limite d'allies (3 allies en jeu, tous restent) » VERT; « k268 Chilly McHotpants : apres avoir attaque, 1 carte piochee (degats subis, pas de 2e carte) » VERT; « k268 Chilly McHotpants : si le joueur ne subit AUCUN degat, 2 cartes piochees » VERT; « k268 Chilly McHotpants vaincu : la carte revient dans la defausse du joueur, sous sa forme d'allie » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 5/5.
      Gabarit sbire `skrull_war_minion` (porte la Reponse) : rouges 2/5 ; VERTS SANS MODULE : [campagne_cartes] sk268 Chilly McHotpants : entre en jeu comme un SBIRE engage avec le joueur (MNG 2, ATQ 2, 5 PV) || [campagne_cartes] sk268 Chilly McHotpants : ne compte PAS contre la limite d'allies (3 allies en jeu, tous restent || [campagne_cartes] sk268 Chilly McHotpants vaincu : la carte revient dans la defausse du joueur, sous sa forme d'allie.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (l'allie devient un SBIRE engage (autre face, image sk268 conservee)). Cas plateau : `ui-app/src/board/campagne-cartes-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk269 : Xavin

- [x] Etape 2 : carte(s) de reference : `dz035` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk269.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « an EVENT with a Hero Action ability »; « Hero Action ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "3", "HP": "5", "THW": "2**", "ATK": "3**", "RES": "B", "Class": "Campaign;Protection"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k269 Xavin : defausse du deck jusqu'a un evenement a « Hero Action » et la resout (01022 : 1 degat a chaque ennemi) » VERT; « k269 Xavin, TEMOIN : un evenement SANS « Hero Action » (01086 First Aid, Action) est defausse mais pas pris pour cible » VERT; « k269 Xavin : deck epuise sans evenement a « Hero Action » : rien n'est resolu, rien ne reste en resolution » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 2/3 ; VERTS SANS MODULE : [campagne_cartes] sk269 Xavin : deck epuise sans evenement a « Hero Action ».
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (defausse et resolution d'une action : rien de nouveau a dessiner).

Carte terminée : OUI

### sk270 : Buddy Training Program

- [x] Etape 2 : carte(s) de reference : `hd011`, `21013`, `ar010`, `ss004` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk270.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "0", "RES": "R", "StartingThreat": "2", "Victory": "0", "Class": "Campaign;Protection"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « k270 Buddy Training Program : cout X = stade du mechant : stade 1 = 1 ressource » VERT; « k270 Buddy Training Program : au stade 2 (Rhino II) le cout est 2 » VERT; « k270 Buddy Training Program : au stade 2, une carte a 2 icones (01088 YY) paie et la carte se joue » VERT; « k270 Buddy Training Program : vaincue, donne une carte Robuste au heros (jusqu'a X = 1 personnage amical) » VERT; « k270 Buddy Training Program : jusqu'a X = 2 personnages au stade 2 (heros ET allie recoivent chacun une carte Robuste) » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 4/5 ; VERTS SANS MODULE : [campagne_cartes] sk270 Buddy Training Program : au stade 2, une carte a 2 icones (01088 YY) paie et la carte se joue.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (statut Robuste : cartes d'etat deja rendues nativement (area_status_cards, vu dans la capture C1)).

Carte terminée : OUI

### sk271 : Cloning Faux Pas

- [x] Etape 2 : carte(s) de reference : `hd011`, `hd012`, `ss004`, `56086` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk271.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "0", "RES": "Y", "StartingThreat": "3", "Acceleration": "1", "Victory": "0", "Class": "Campaign;'Pool"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k271 Cloning Faux Pas : porte 1 icone ACCELERATION en jeu (desc, aucun script) » VERT; « k271 Cloning Faux Pas : vaincue, 3 degats a CHAQUE sbire SKRULL engage ; un sbire non Skrull est epargne » VERT; « k271 Cloning Faux Pas, TEMOIN : montant 0 declare : aucun degat » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 1/3 ; VERTS SANS MODULE : [campagne_cartes] sk271 Cloning Faux Pas : porte 1 icone ACCELERATION en jeu (desc, aucun script) || [campagne_cartes] sk271 Cloning Faux Pas, TEMOIN : montant 0 declare.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement : degats ; icone Acceleration native).

Carte terminée : OUI

### sk272 : Fickle Alliance

- [x] Etape 2 : carte(s) de reference : `60145`, `bw002`, `hd010` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk272.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "0", "RES": "G", "StartingThreat": "3", "Victory": "0", "Class": "Campaign;Leadership"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « k272 Fickle Alliance : vaincue, un sbire non Elite du deck rencontre devient un allie (MNG imprime -> CTR, traits gardes) » VERT; « k272 Fickle Alliance : un sbire ELITE du deck rencontre n'est PAS cherchable (seul Sandman reste : rien n'est mis en jeu) » VERT; « k272 Fickle Alliance : l'allie prend 1 degat consequent apres avoir attaque » VERT; « k272 Fickle Alliance : l'allie issu du sbire, vaincu, retourne en DEFAUSSE DE RENCONTRE (sa carte est une carte rencontre) » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 3/4 ; VERTS SANS MODULE : [campagne_cartes] sk272 Fickle Alliance : un sbire ELITE du deck rencontre n'est PAS cherchable (seul Sandman re.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (un sbire devient un ALLIE (face allie, image du sbire) ; le complot va en pile de victoire). Cas plateau : `ui-app/src/board/campagne-cartes-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk273 : Newbie Training

- [x] Etape 2 : carte(s) de reference : `hd011`, `dz009` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk273.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "0", "RES": "R", "StartingThreat": "3", "Victory": "0", "Class": "Campaign;Aggression"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k273 Newbie Training : vaincue, defait un sbire SKRULL non Elite et pioche 1 carte ; l'Elite SKRULL est epargne » VERT; « k273 Newbie Training, TEMOIN : aucun sbire SKRULL non Elite : rien n'est defait, aucune carte piochee » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 1/2 ; VERTS SANS MODULE : [campagne_cartes] sk273 Newbie Training, TEMOIN : aucun sbire SKRULL non Elite.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (sbire vaincu et carte piochee : rendus natifs).

Carte terminée : OUI

### sk274 : Searching for Powers

- [x] Etape 2 : carte(s) de reference : `hd010`, `bc004`, `dz031` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk274.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "0", "RES": "Y", "StartingThreat": "3", "Victory": "0", "Class": "Campaign;Basic"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k274 Searching for Powers : vaincue, cherche un SUPERPOWER dans le deck et le JOUE sans payer (01022 Ground Stomp : 1 degat a chaque ennemi) » VERT; « k274 Searching for Powers : l'amelioration SUPERPOWER trouvee dans la DEFAUSSE (sk044 Lazerfist, cout 3) est jouee gratuitement » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (carte jouee depuis le deck : rendu natif).

Carte terminée : OUI

### sk275 : Skrull Military Training

- [x] Etape 2 : carte(s) de reference : `hd010`, `40006`, `bc004` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk275.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "0", "RES": "R", "StartingThreat": "3", "Victory": "0", "Class": "Campaign;Basic"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 7/7 cas verts : « k275 Skrull Military Training : le CTR du heros ne retire AUCUNE menace (3 de depart) » VERT; « k275 Skrull Military Training : un allie NON Skrull (sk038 Human Torch) ne retire aucune menace » VERT; « k275 Skrull Military Training : un SOUTIEN (sk278 Cadre K) ne peut pas retirer la menace non plus » VERT; « k275 Skrull Military Training : un allie SKRULL (sk264 Jazinda, CTR 3) retire la menace, vainc le complot : pile de victoire » VERT; « k275 Skrull Military Training : en pile de victoire, le heros du proprietaire gagne +1 CTR, +1 ATQ, +1 DEF » VERT; « k275 Skrull Military Training, TEMOIN : tant que la carte est EN JEU (pas en vitrine), aucun bonus » VERT; « k275 Skrull Military Training : le bonus va au heros du PROPRIETAIRE seulement, pas a celui de l'autre joueur » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 5/7 ; VERTS SANS MODULE : [campagne_cartes] sk275 Skrull Military Training : un allie SKRULL (sk264 Jazinda, CTR 3) retire la menace, vainc le comp || [campagne_cartes] sk275 Skrull Military Training, TEMOIN : tant que la carte est EN JEU (pas en vitrine), aucun bonus.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte en pile de victoire + bonus de stats du heros). Cas plateau : `ui-app/src/board/campagne-cartes-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk276 : Stealing For Good

- [x] Etape 2 : carte(s) de reference : `hd010` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk276.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "0", "RES": "R", "StartingThreat": "2", "Victory": "0", "Class": "Campaign;Justice"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « k276 Stealing For Good : vaincue, ajoute une amelioration du deck a la main et retire sa valeur de menace (01065, cout 2) » VERT; « k276 Stealing For Good : une amelioration de cout 1 (01007 Spider-Tracer) retire 1 menace seulement » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (menace retiree et carte en main : rendus natifs).

Carte terminée : OUI

### sk277 : Antalya

- [x] Etape 2 : carte(s) de reference : `20029`, `ra001b` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk277.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Action »; « Hero Action »; « a FRIENDLY character ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "B", "Class": "Campaign;Protection"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k277 Antalya : Action -> soigne 1 degat de l'identite et s'incline » VERT; « k277 Antalya : peut soigner un ALLIE (personnage amical de n'importe quel type) » VERT; « k277 Antalya, TEMOIN : incline, elle n'offre plus son Action (les degats restent) » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 2/3 ; VERTS SANS MODULE : [campagne_cartes] sk277 Antalya, TEMOIN : incline, elle n'offre plus son Action (les degats restent).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (soin et inclinaison : rendus natifs).

Carte terminée : OUI

### sk278 : Cadre K

- [x] Etape 2 : carte(s) de reference : `20029` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk278.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « A scheme ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "G", "Class": "Campaign;Justice"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « k275 Skrull Military Training : un SOUTIEN (sk278 Cadre K) ne peut pas retirer la menace non plus » VERT; « k278 Cadre K : Action -> retire 1 menace d'une manigance (Bomb Scare 4 -> 3) et s'incline » VERT; « k278 Cadre K, TEMOIN : incline, aucune menace retiree » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 1/2 ; VERTS SANS MODULE : [campagne_cartes] sk278 Cadre K, TEMOIN : incline, aucune menace retiree.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (menace retiree et inclinaison : rendus natifs).

Carte terminée : OUI

### sk279 : Pool-O-Vision

- [x] Etape 2 : carte(s) de reference : `04047` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk279.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "0", "RES": "Y", "Class": "Campaign;'Pool"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « k279 Pool-O-Vision : apres la defaite d'un sbire SKRULL, pioche 1 carte par icone en jeu (Acceleration + Crise = 2) » VERT; « k279 Pool-O-Vision : quatre icones differentes (Crise, Acceleration, Amplification, Alea) : plafond de 3 cartes » VERT; « k279 Pool-O-Vision, TEMOIN : sans aucune icone en jeu, aucune carte piochee (mais le soutien s'incline) » VERT; « k279 Pool-O-Vision, TEMOIN : la defaite d'un sbire NON Skrull (Hydra Mercenary) ne declenche rien » VERT; « k279 Pool-O-Vision, TEMOIN : « Hero Response » : en alter ego (forme hors heros) rien n'est pioche » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 2/5 ; VERTS SANS MODULE : [campagne_cartes] sk279 Pool-O-Vision, TEMOIN : sans aucune icone en jeu, aucune carte piochee (mais le soutien s'incl || [campagne_cartes] sk279 Pool-O-Vision, TEMOIN : la defaite d'un sbire NON Skrull (Hydra Mercenary) ne declenche rien || [campagne_cartes] sk279 Pool-O-Vision, TEMOIN : « Hero Response ».
- [x] Etape 7 bis : limite imprimee ? NON de limite par round ; plafond « to a maximum of 3 » cartes (cas dedie).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (pioche et inclinaison : rendus natifs).

Carte terminée : OUI

### sk280 : Princess Anelle

- [x] Etape 2 : carte(s) de reference : `sk189a`, `sk270` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk280.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "0", "RES": "G", "Class": "Campaign;Basic"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 8/8 cas verts : « k280 Princess Anelle : cout X = joueurs + ennemis SKRULL en jeu : solo, aucun ennemi SKRULL = 1 » VERT; « k280 Princess Anelle : deux ennemis SKRULL en jeu (sbire Dard'van et General Kalamari) = 1 + 2 = 3 » VERT; « k280 Princess Anelle : le MECHANT SKRULL compte aussi (scenario Paibok) = 1 + 1 = 2 » VERT; « k280 Princess Anelle : un sbire non Skrull (Hydra Mercenary) ne compte pas = 1 » VERT; « k280 Princess Anelle : deux joueurs, aucun ennemi SKRULL = 2 » VERT; « k280 Princess Anelle : ALLIANCE (2 joueurs) : un cout de 4 qu'un joueur seul ne peut pas payer l'est a deux » VERT; « k280 Princess Anelle : apres la phase des joueurs, elle quitte la PARTIE (pas la defausse) et la phase du mechant est sautee » VERT; « k280 Princess Anelle, TEMOIN : sans Anelle, la phase du mechant n'est pas sautee » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 6/8 ; VERTS SANS MODULE : [campagne_cartes] sk280 Princess Anelle : ALLIANCE (2 joueurs) || [campagne_cartes] sk280 Princess Anelle, TEMOIN : sans Anelle, la phase du mechant n'est pas sautee.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (carte RETIREE DE LA PARTIE (zone « Retirees de la partie », pas la defausse)). Cas plateau : `ui-app/src/board/campagne-cartes-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk281 : Skrull Battleship

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk281.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "G", "Class": "Campaign;Leadership"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « k281 Skrull Battleship : jouable si on controle un allie SKRULL (Jazinda en jeu) » VERT; « k281 Skrull Battleship, TEMOIN : sans allie SKRULL (Human Torch, non Skrull), la carte reste en main » VERT; « k281 Skrull Battleship : Ressource de heros -> une ressource [wild] qui paie le cout manquant d'une carte (Jazinda, cout 3) » VERT; « k281 Skrull Battleship, TEMOIN : sans le Battleship, 2 ressources ne paient pas Jazinda (cout 3) : elle reste en main » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 2/4 ; VERTS SANS MODULE : [campagne_cartes] sk281 Skrull Battleship : jouable si on controle un allie SKRULL (Jazinda en jeu) || [campagne_cartes] sk281 Skrull Battleship, TEMOIN : sans le Battleship, 2 ressources ne paient pas Jazinda (cout 3).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (ressource generee et inclinaison : rendus natifs).

Carte terminée : OUI

### sk282 : Skrull Kill Krew

- [x] Etape 2 : carte(s) de reference : `ho004`, `an001a` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk282.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Hero Action »; « a SKRULL MINION ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "R", "Class": "Campaign;Aggression"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « k282 Skrull Kill Krew : Action de heros -> 1 degat a un sbire SKRULL, s'incline (sbire non vaincu) » VERT; « k282 Skrull Kill Krew : si le sbire est VAINCU par ce coup, le soutien se redresse » VERT; « k282 Skrull Kill Krew, TEMOIN : sans sbire SKRULL (Hydra Mercenary seul), aucune action offerte » VERT; « k282 Skrull Kill Krew, TEMOIN : « Hero Action » : en alter ego, rien ne se passe » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 2/4 ; VERTS SANS MODULE : [campagne_cartes] sk282 Skrull Kill Krew, TEMOIN : sans sbire SKRULL (Hydra Mercenary seul), aucune action offerte || [campagne_cartes] sk282 Skrull Kill Krew, TEMOIN : « Hero Action ».
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (degats et redressement : rendus natifs).

Carte terminée : OUI

### sk283 : 3-D Man's Goggles

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk283.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "B", "Class": "Campaign;Leadership"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « k283 3-D Man's Goggles : s'attache a un allie NON Skrull (Human Torch), jamais a un Skrull » VERT; « k283 3-D Man's Goggles, TEMOIN : avec SEULEMENT un allie Skrull (Jazinda), la carte n'est pas jouable (reste en main) » VERT; « k283 3-D Man's Goggles : l'allie qui attaque un ennemi SKRULL ne prend AUCUN degat consequent (Human Torch ATQ 2*) » VERT; « k283 3-D Man's Goggles, TEMOIN : contre un ennemi NON Skrull (Hydra Mercenary), l'allie prend son degat consequent » VERT; « k283 3-D Man's Goggles, TEMOIN : sans les lunettes, la meme attaque contre un Skrull coute 1 degat a l'allie » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 3/5 ; VERTS SANS MODULE : [campagne_cartes] sk283 3-D Man's Goggles, TEMOIN : contre un ennemi NON Skrull (Hydra Mercenary), l'allie prend son degat || [campagne_cartes] sk283 3-D Man's Goggles, TEMOIN : sans les lunettes, la meme attaque contre un Skrull coute 1 degat a l'.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (amelioration attachee a un allie). Cas plateau : `ui-app/src/board/campagne-cartes-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk284 : Inhibitor Mask

- [x] Etape 2 : carte(s) de reference : `33005` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk284.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "1", "RES": "R", "Temporary": "1", "Class": "Campaign;Basic"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « k284 Inhibitor Mask : s'attache a un ennemi SKRULL ; son texte imprime est ignore (Skrull Commander ne donne plus +1 ATQ) » VERT; « k284 Inhibitor Mask, TEMOIN : sans le masque, Skrull Commander donne bien +1 ATQ a sk184 » VERT; « k284 Inhibitor Mask, TEMOIN : avec SEULEMENT des ennemis non Skrull (Rhino), la carte n'est pas jouable » VERT; « k284 Inhibitor Mask : TEMPORARY : defaussee a la fin du round, le texte redevient actif » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 2/4 ; VERTS SANS MODULE : [campagne_cartes] sk284 Inhibitor Mask, TEMOIN : sans le masque, Skrull Commander donne bien +1 ATQ a sk184 || [campagne_cartes] sk284 Inhibitor Mask : TEMPORARY.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (amelioration attachee a un ennemi (sbire SKRULL)). Cas plateau : `ui-app/src/board/campagne-cartes-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk285 : Ultimate Nullifier

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk285.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "0", "RES": "R", "Temporary": "1", "Class": "Campaign;'Pool"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 6/6 cas verts : « k285 Ultimate Nullifier : l'ennemi porteur ne peut PAS s'activer (l'attaque de sk184 est annulee) » VERT; « k285 Ultimate Nullifier, TEMOIN : sans lui, l'attaque de sk184 inflige 2 degats a l'alter ego » VERT; « k285 Ultimate Nullifier : sur le MECHANT (Paibok SKRULL), il porte 1 icone Hazard (solo = 1 par joueur) » VERT; « k285 Ultimate Nullifier : a DEUX joueurs il porte 2 icones Hazard sur le mechant » VERT; « k285 Ultimate Nullifier, TEMOIN : sur un SBIRE (sk184), aucune icone Hazard » VERT; « k285 Ultimate Nullifier : TEMPORARY : defaussee a la fin du round » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 4/6 ; VERTS SANS MODULE : [campagne_cartes] sk285 Ultimate Nullifier, TEMOIN : sans lui, l'attaque de sk184 inflige 2 degats a l'alter ego || [campagne_cartes] sk285 Ultimate Nullifier : TEMPORARY.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (attachee a un ennemi : meme rendu que sk284 (teste) ; l'icone Hazard est un chiffre du moteur (cas `icones`)).

Carte terminée : OUI

### sk286 : Reverting Device

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk286.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "0", "RES": "Y", "Class": "Campaign;Justice"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « k286 Reverting Device : sous le controle du joueur, chaque sbire SKRULL engage avec lui perd 1 MNG (sk184 : 2 -> 1) » VERT; « k286 Reverting Device, TEMOIN : un sbire NON Skrull engage (Shocker, MNG 1) n'est pas touche » VERT; « k286 Reverting Device, TEMOIN : sans la carte, sk184 garde son MNG imprime » VERT; « k286 Reverting Device : un sbire SKRULL engage avec l'AUTRE joueur n'est pas touche » VERT; « k286 Reverting Device : le bonus se recalcule quand un sbire SKRULL s'engage APRES la pose de la carte » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 2/5 ; VERTS SANS MODULE : [campagne_cartes] sk286 Reverting Device, TEMOIN : un sbire NON Skrull engage (Shocker, MNG 1) n'est pas touche || [campagne_cartes] sk286 Reverting Device, TEMOIN : sans la carte, sk184 garde son MNG imprime || [campagne_cartes] sk286 Reverting Device : un sbire SKRULL engage avec l'AUTRE joueur n'est pas touche.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (amelioration attachee a l'identite). Cas plateau : `ui-app/src/board/campagne-cartes-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk287 : Skrull Shapeshifter

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk287.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "1", "RES": "G", "Class": "Campaign;Protection"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « k287 Skrull Shapeshifter : l'identite (alter ego) gagne le trait SKRULL » VERT; « k287 Skrull Shapeshifter : le trait vaut AUSSI en forme heros (contre-cas de l'autre forme) » VERT; « k287 Skrull Shapeshifter, TEMOIN : sans la carte, l'identite n'est pas SKRULL » VERT; « k287 Skrull Shapeshifter : quand le joueur serait vaincu, ses PV passent a 1 a la place, puis la carte est defaussee » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 3/4 ; VERTS SANS MODULE : [campagne_cartes] sk287 Skrull Shapeshifter, TEMOIN : sans la carte, l'identite n'est pas SKRULL.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (amelioration attachee a l'identite (trait SKRULL)). Cas plateau : `ui-app/src/board/campagne-cartes-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk288 : Sy-Torak Gem

- [x] Etape 2 : carte(s) de reference : `aa012` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_menace_campaign/sk288.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "Y", "Class": "Campaign;Aggression"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 6/6 cas verts : « k288 Sy-Torak Gem : +3 points de vie (alter ego : 13 PV max) » VERT; « k288 Sy-Torak Gem : le heros gagne +1 ATQ en forme heros » VERT; « k288 Sy-Torak Gem, TEMOIN : sans la carte, aucun bonus » VERT; « k288 Sy-Torak Gem : deck epuise, une ressource [energy] est depensee et la gemme reste en jeu » VERT; « k288 Sy-Torak Gem : la gemme defaussee en pleine pioche fait perdre ses +3 PV : l'identite (11 degats sur 13) tombe, sans planter » VERT; « k288 Sy-Torak Gem : deck epuise SANS ressource [energy] payable : la gemme est defaussee » VERT.
      Substitution (module remplace par `GetAbilities -> []`, empreinte du dossier identique avant/apres) : rouges 4/6 ; VERTS SANS MODULE : [campagne_cartes] sk288 Sy-Torak Gem, TEMOIN : sans la carte, aucun bonus || [campagne_cartes] sk288 Sy-Torak Gem : la gemme defaussee en pleine pioche fait perdre ses +3 PV.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (amelioration attachee a l'identite (+3 PV publies)). Cas plateau : `ui-app/src/board/campagne-cartes-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk289a : Cooperation Progress Reminder

- [x] Etape 2 : aucune capacite scriptee (type Insert : aucune capacite scriptee (regle du bloc Cooperation Area)).
- [x] Etape 5 : sans objet.
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « k289a / sk289b Cooperation Progress Reminder : les deux faces (type Insert) se creent sans erreur, rien n'est scripte » VERT.
      Substitution : sans objet.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (type Insert : zone `area_insert` ignoree par le plateau (aide-memoire de regles)).

Carte terminée : OUI

### sk289b : Cooperation Progress Reminder

- [x] Etape 2 : aucune capacite scriptee (type Insert : verso du rappel, aucun texte de regle).
- [x] Etape 5 : sans objet.
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « k289a / sk289b Cooperation Progress Reminder : les deux faces (type Insert) se creent sans erreur, rien n'est scripte » VERT.
      Substitution : sans objet.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (type Insert : zone `area_insert` ignoree par le plateau (aide-memoire de regles)).

Carte terminée : OUI
