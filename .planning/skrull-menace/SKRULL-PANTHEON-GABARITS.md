# Skrull Pantheon (scénario 4 de Skrull Menace, Kajislav) et Dard'van Sect — gabarits PROCESSUS-CARTE

Pack `skrull_menace`, card_id sk170-sk183 (scénario Skrull Pantheon : méchant double face Kly'bn / Sl'gur't par stade, complots
principaux 1A/1B et 2A/2B, environnement double face Stronghold / Destroyed, attachements Blessed by, Nogor, complots annexes,
traîtrises) et sk184-sk188 (set modulaire Dard'van Sect : deux sbires, complot annexe, deux traîtrises). Fiches générées à partir des
résultats RÉELS (rapport test_capacites, sorties de substituer_pack.py, en-têtes des modules) par
`.planning/skrull-menace/defs/generer_gabarits_pantheon.py`.

Rappels communs à toutes les cartes :
- **Numérotation** relue sur les 25 scans (pied de carte) : 170A/B, 171A/B, 172A/B (Kly'bn / Sl'gur't I, II, III), 173A/B (Protect the Pantheon),
  174A/B (Slaying the False Gods), 175A/B (Skrull Pantheon), 176-183 (rencontre), 184-188 (Dard'van Sect). Chaque face d'une carte double
  face a son card_id (`sk170a` = face Kly'bn, `sk170b` = face Sl'gur't ; `sk175a` Stronghold, `sk175b` Destroyed).
- **Règles du scénario** (insert p.14, lu par le coordinateur) : une SEULE carte double face par stade (PV partagés, le stade suivant arrive du
  même côté), jetons de foi (compteur maison `faith`), « Flip the villain » = défausse des attachements, cartes d'état, cartes de boost et autres
  éléments associés SAUF jetons de foi et dégâts, puis « When Revealed » de la face d'arrivée. Aucune carte de campagne n'est portée.
- **Étape 6 (nombres)** : stats, PV (15/18/20 par joueur, étoile = « par joueur »), menaces (9*/6*/+1* puis 12*/0/+1*), icônes de boost (Y = 1, ★ = pas d'icône
  chiffrée), SCH/ATK, relus sur les SCANS (1500x2150, tous vus un par un) contre `data/cards.json` : conformes. Lectures corrigées par rapport à
  la transcription : l'icône noire « boîte avec un plus » de sk186 est l'icône **HAZARD** (méthode du glyphe `H` de ChampionsIcons.ttf, rendu à côté
  du scan) ; Nogor : SCH/ATK/PV portent une ★ (renvoi au texte) et gardent leurs chiffres imprimés 1/1/4 ; Dard'van Priest : ATK ★ = `0*`.
  Voir `defs/pantheon_questions.md`.
- **Étape 7 (tests)** : 98 cas `[pantheon]` dans `tools/cas/pantheon.py` (chargé par `tools/test_capacites.py`), **98/98 verts**. Chaque mesure part d'un
  plateau connu : deck rencontre vidé (`EmptyEncounterDeck`) puis monté par `CreateEncounterDeck`, main fixée par `main_exclusive`, forme héros
  (`ChangeForm('01001b')`) quand on mesure une phase du méchant, deux joueurs par `heros2`. Pièges payés pendant les tests (détail :
  `defs/pantheon_moteur.md`) :
  - un deck de test rempli de cartes UNIQUES (Sandman) bouclait à l'infini (règle d'unicité + remélange + Renfort) : cartes de remplissage non uniques et inertes (`sk107`) ;
  - un deck qui s'épuise remélange sa défausse : cartes de remplissage SOUS les cartes mesurées ;
  - en alter ego le méchant manigance et atteint vite le seuil 9 du complot 1B (stade 1 accompli en pleine mesure) : mesurer une phase du méchant en forme héros ;
  - `carte_du_surge` exige UN SEUL exemplaire de la carte semée ; `passer_sur_option="Defense"` ne doit PAS figurer dans un cas dont la capacité remplace l'attaque (la question n'est jamais posée : c'est une preuve de plus que l'attaque est annulée).
- **Substitution (`substituer_pack.py`, deux passes sk17 / sk18, puis sk170a et sk174b rejouées après renommage de leurs cas ; empreinte md5 du pack identique avant/après, aucun stub restant)** :
  chaque module est vidé à tour de rôle, les cas filtrés sur son card_id doivent tomber. Les cas « vert sans module » de chaque fiche sont TOUS des
  témoins d'ABSENCE d'effet (« TEMOIN », « sans … », « NON offerte ») ou des mesures de comportement NATIF du moteur sans module : PV par stade lus dans `desc` (sk170a), Hinder (sk179) et menace de départ
  `2*` (sk180) lus dans `desc`, victoire quand le dernier stade du méchant est vaincu (sk171a, sk171b, sk172a), « si ce stade est achevé, les joueurs
  perdent » du complot 2B (texte en gras lu par le moteur, sk174b), environnement qui reste de côté tant que le stade 1 dure (sk175a) : assumés comme le prévoit l'étape 7.
- **Étape 8 (autoplay)** : 40 parties `equilibre`, graines 1-8 : spider_man contre `sk_skrull_pantheon` (8) et `sk_skrull_pantheon_expert` (8), hulkling_kajislav contre les deux (16),
  plus 8 parties spider_man contre Rhino comme TÉMOIN. Grep exhaustif `NameError|AttributeError|TypeError|KeyError|AssertionError|Traceback|<F>` sur les 32 journaux
  du scénario (copiés dès la fin de chaque fournée, `/tmp` étant nettoyé par d'autres sessions) : **0**. Journaux lus : retournements du méchant (44 + 56),
  jetons de foi (236 + 261 poses), environnement mis en jeu (18 + 42), stade 2 du complot, Nogor, Strengthen the Faith, Prayer (Kly'bn déplace bien les traîtrises défaussées vers la défausse sans les distribuer),
  Fanatic, Priest, Collective Prayers, Sectarian Practices, Blessed by : chaque carte a été jouée en partie. 0 victoire sur 32 (profil `equilibre`, 4-5 rounds avant l'élimination ou
  l'accomplissement de 2B : le témoin Rhino fait 0/8 aussi, ce n'est pas un signal d'équilibrage) ; 0 partie bloquée sur le scénario ; le témoin en a 2
  (artefact du pilote sur `01093` Tenacity, carte officielle, sans rapport).
- **Étape 8 bis (plateau)** : `ui-app/src/board/pantheon-plateau.test.ts` (12 cas, états CAPTURÉS sur le moteur par `tools/sonde_campagne.py` : jetons de foi, face Kly'bn puis Sl'gur't
  de la même carte, carte Tenace, carte de boost portée par le méchant, Blessed attaché au sbire, environnement Stronghold / Destroyed), vu ROUGE sur un état cassé (clé de compteur fausse, attachement détaché : plusieurs cas rouges),
  puis VERT ; `tsc --noEmit` propre. `compteurs-fr.test.ts` : `faith` → « foi ».
- **Outils statiques** : `verifier_appels_modules skrull_menace` OK (calibré : un appel inexistant glissé dans sk188 est bien vu) ; `verifier_api_cartes` sans faute dans skrull_menace (calibré de même).
- **Moteur partagé** : uniquement un compteur (`'faith'`) et un trait (`"GOD"`) déclarés dans `card_face.py` + traduction du trait et du compteur (`defs/pantheon_moteur.md`).
- **Limites connues et questions** : `defs/pantheon_questions.md` (icône Hazard de sk186, distribution « dans l'ordre des joueurs », jetons de foi conservés d'un stade à l'autre, « Advance to stage 2B »
  qui saute la face A, Action de l'environnement non offerte sans jeton, choix du Priest / de Sectarian Practices, retournement en pleine activation). À noter : l'Action de héros de l'environnement
  Stronghold est PROPOSÉE même sans deux ressources de même type en main (le moteur ne teste la couleur qu'au paiement, comme `40090`), mais le paiement mixte est refusé (cas dédié).
- **Ce qu'aucun outil ne voit** : une vraie partie jouée par un humain dans le navigateur (agrément du scénario, équilibrage du bot : profil `equilibre`), non faite ; l'équilibrage des deux
  chemins du stade 1 (Stronghold / Destroyed) en particulier ne se juge qu'à la main.

### sk170a : Kly'bn

- [x] Etape 2 : carte(s) de reference : `hunting_season/hs226` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk170a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « for each FAITH counter ON Kly'bn ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "15*", "ATK": "1", "SCH": "2", "Stage": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 6/6 cas verts : « ] sk170a Setup normal : Kly'bn I face visible, 1 jeton de foi, complot 1B, environnement mis de cote » VERT; « ] sk170a Changement de stade : Kly'bn I vaincu -> Kly'bn II du MEME cote (face Kly'bn), jeton de foi conserve + 1 » VERT; « ] sk170a PV par stade et par joueur : 15 / 18 / 20 (deux joueurs : 30 au stade I) » VERT; « ] sk170a Reponse forcee Kly'bn : 1 jeton de foi = 1 carte du dessus defaussee, distribuee si ce n'est PAS une traitrise » VERT; « ] sk170a Reponse forcee Kly'bn : une TRAITRISE defaussee n'est PAS distribuee (Exhaustion reste en defausse, le heros reste pret) » VERT; « ] sk170a Reponse forcee : « in player order » : 3 sbires, 2 joueurs -> le premier joueur en recoit 2, le second 1 » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 5/6 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (jetons de foi sur le mechant, face Kly'bn de la carte double face). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk170b : Sl'gur't

- [x] Etape 2 : carte(s) de reference : `hunting_season/hs226` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk170b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « for each FAITH counter ON Sl'gur't ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "15*", "ATK": "2", "SCH": "1", "Stage": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « ] sk170b Changement de stade : Sl'gur't I vaincu -> Sl'gur't II du MEME cote (face Sl'gur't) » VERT; « ] sk170b Retournement vers Kly'bn (aller-retour) : la face Kly'bn resout SON When Revealed » VERT; « ] sk170b Reponse forcee Sl'gur't : seules les TRAITRISES defaussees sont distribuees (Exhaustion distribuee, heros incline ; le sbire reste en defausse) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (face Sl'gur't de la meme carte, jetons de foi conserves). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk171a : Kly'bn

- [x] Etape 2 : carte(s) de reference : `hunting_season/hs226` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk171a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « for each FAITH counter ON Kly'bn ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "18*", "ATK": "1", "SCH": "3", "Stage": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « ] sk171a Setup EXPERT : Kly'bn II en jeu (stade II), 1 jeton de foi » VERT; « ] sk171a Dernier stade vaincu (face Kly'bn) : victoire des joueurs » VERT; « ] sk171a TEMOIN : stade II blesse mais pas vaincu : pas de victoire » VERT; « ] sk171a Reponse forcee Kly'bn II (expert) : 1 jeton de foi = 1 carte du dessus defaussee et distribuee (sbire) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (meme marque : jetons de foi, stade II face Kly'bn). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk171b : Sl'gur't

- [x] Etape 2 : carte(s) de reference : `hunting_season/hs226` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk171b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « for each FAITH counter ON Sl'gur't ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "18*", "ATK": "3", "SCH": "1", "Stage": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « ] sk171b En vaincre un suffit : Sl'gur't II vaincu (face visible) = victoire, sans avoir touche a Kly'bn » VERT; « ] sk171b Reponse forcee Sl'gur't II (expert) : seule la traitrise est distribuee (Exhaustion : heros incline), le sbire reste en defausse » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (meme marque : stade II face Sl'gur't). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk172a : Kly'bn

- [x] Etape 2 : carte(s) de reference : `hunting_season/hs226` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk172a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « for each FAITH counter ON Kly'bn ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "20*", "ATK": "2", "SCH": "3", "Stage": "3"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « ] sk172a Expert : stade II vaincu -> stade III (face Kly'bn), carte d'etat Robuste donnee a la revelation » VERT; « ] sk172a Expert : dernier stade (III) vaincu = victoire » VERT; « ] sk172a Retournement au stade III : Robuste defaussee puis REDONNEE par le When Revealed de la face d'arrivee » VERT; « ] sk172a Reponse forcee Kly'bn III (expert) : le sbire defausse est distribue ; la carte d'etat Robuste est en place » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (jetons de foi et carte d'etat Tenace portee par le mechant). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk172b : Sl'gur't

- [x] Etape 2 : carte(s) de reference : `hunting_season/hs226` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk172b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « for each FAITH counter ON Sl'gur't ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "20*", "ATK": "3", "SCH": "2", "Stage": "3"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « ] sk172b Expert : stade II vaincu face Sl'gur't -> stade III face Sl'gur't, Robuste donnee (« give HER a tough status card ») » VERT; « ] sk172b Reponse forcee Sl'gur't III (expert) : 3 jetons de foi = 3 cartes defaussees, seule la traitrise est distribuee » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (jetons de foi et carte d'etat Tenace, face Sl'gur't). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk173a : Protect the Pantheon

- [x] Etape 2 : aucune capacite scriptee.
- [x] Etape 5 : sans objet.
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « ] sk173a Setup : les ensembles obligatoires sont dans le deck rencontre (Dard'van Sect, Skrull Pantheon, Standard) » VERT.
      Substitution : sans objet.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (face A sans capacite en jeu (Contents / Setup : l'environnement est mis de cote par le scenario)).

Carte terminée : OUI

### sk173b : Protect the Pantheon

- [x] Etape 2 : carte(s) de reference : `web_of_deceit/wd055b` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk173b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the LAST threat is removed »; « complot a 0 au depart ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "1", "TargetThreat": "9*", "EscalationThreat": "1*", "StartingThreat": "6*"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « ] sk173b Derniere menace retiree : environnement DESTROYED en jeu, complot directement en 2B (sans 2A), mechant retourne » VERT; « ] sk173b Derniere menace retiree par un CONTRE reel (heros en forme heros, THW 1) : meme resultat » VERT; « ] sk173b TEMOIN : il reste de la menace -> rien ne se passe (environnement toujours de cote) » VERT; « ] sk173b When Completed : seuil atteint (9) -> environnement STRONGHOLD, stade 2A resolu (Strengthen the Faith revele +2 menace), puis 2B retourne le mechant » VERT; « ] sk173b TEMOIN : 8 menaces ne suffisent pas (seuil 9[per_hero]) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (met en jeu l'environnement (Stronghold ou Destroyed) a la fin du stade 1). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk174a : Slaying the False Gods

- [x] Etape 2 : carte(s) de reference : `01136`, `01180` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk174a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Search the encounter deck AND DISCARD PILE »; « reveal it ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « ] sk174a Revelation : Strengthen the Faith est cherchee aussi dans la DEFAUSSE rencontre » VERT; « ] sk174a Revelation, TEMOIN : aucune Strengthen the Faith nulle part -> rien n'est revele, le stade 2B s'installe quand meme » VERT; « ] sk174a Revelation : deux joueurs -> menace de Strengthen = 2*2 + 2*2 = 8 » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (revele Strengthen the Faith (complot annexe) avec 2[per_hero] menaces en plus). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk174b : Slaying the False Gods

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk174b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Flip the VILLAIN ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "2", "TargetThreat": "12*", "EscalationThreat": "1*", "StartingThreat": "0"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 11/11 cas verts : « ] sk174b PV partages : 4 degats subis face Kly'bn restent sur la face Sl'gur't apres le retournement » VERT; « ] sk174b Retournement (« Flip the villain » de 2B) : les attachements du mechant sont defausses » VERT; « ] sk174b TEMOIN : sans retournement l'attachement reste sur le mechant » VERT; « ] sk174b Retournement : les cartes d'etat (Sonne, Desoriente, Robuste) sont defaussees » VERT; « ] sk174b TEMOIN : sans retournement les trois cartes d'etat restent » VERT; « ] sk174b Retournement : les cartes de boost face cachee du mechant sont defaussees » VERT; « ] sk174b TEMOIN : sans retournement la carte de boost reste au mechant » VERT; « ] sk174b Retournement : les jetons de foi et les degats SURVIVENT, et la face d'arrivee pose son jeton (When Revealed) » VERT; « ] sk174b Revelation : le mechant sur la face Sl'gur't est retourne vers Kly'bn » VERT; « ] sk174b 2B accompli : les joueurs perdent la partie » VERT; « ] sk174b TEMOIN : 11 menaces ne perdent pas la partie » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 6/11 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (retourne le mechant (la face visible change)). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk175a : Skrull Pantheon

- [x] Etape 2 : carte(s) de reference : `next_evol/40090`, `tt/55035` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk175a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « 2 resources of the SAME type ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « ] sk175a Stronghold : Action de heros OFFERTE avec 2 ressources de meme type (Energy YY) ; retire 1 jeton de foi » VERT; « ] sk175a Stronghold : deux ressources de types DIFFERENTS (1 mental + 1 energie) ne PAIENT PAS le cout : aucun jeton retire, main intacte » VERT; « ] sk175a Stronghold, TEMOIN : meme main, la carte Energy (YY) rend l'Action offerte » VERT; « ] sk175a Stronghold : Action NON offerte sans aucun jeton de foi » VERT; « ] sk175a Stade 1 : tant que le complot n'a pas avance, l'environnement reste hors jeu (les jetons ne peuvent pas etre retires) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (environnement dessine face Stronghold). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk175b : Skrull Pantheon

- [x] Etape 2 : carte(s) de reference : `sk175a`, `sk148` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk175b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « of ANY type ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « ] sk175b Destroyed : Action OFFERTE avec deux ressources de types DIFFERENTS ; retire 1 jeton de foi » VERT; « ] sk175b Destroyed : Action NON offerte sans aucun jeton de foi » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (environnement dessine face Destroyed). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk176 : Blessed by Kly'bn

- [x] Etape 2 : carte(s) de reference : `sm/27181`, `brawn/bw016`, `sk113` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk176.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the MINION with the LOWEST SCH ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « ] sk176 Blessed by Kly'bn : s'attache au sbire de plus FAIBLE MNG (Hydra Mercenary 0, pas Skrull Scientist 3) et lui donne +X MNG (X = 1 jeton de foi) » VERT; « ] sk176 Blessed by Kly'bn : le bonus SUIT les jetons de foi (1 -> 3 -> 2) » VERT; « ] sk176 Blessed by Kly'bn : aucun sbire en jeu -> la carte gagne Renfort (revele la carte suivante) » VERT; « ] sk176 Boost (manigance) : +2 icones de boost : la manigance du mechant place 2 + 1 + 2 = 5 menaces (deux joueurs) » VERT; « ] sk176 Boost, TEMOIN : pendant une ATTAQUE les 2 icones ne s'ajoutent pas (1 + 1 = 2 degats au heros) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement dessine porte par le sbire ; MNG qui suit les jetons). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk177 : Blessed by Sl'gur't

- [x] Etape 2 : carte(s) de reference : `sk176`, `sk113` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk177.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the minion with the LOWEST ATK ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « ] sk177 Blessed by Sl'gur't : s'attache au sbire de plus FAIBLE ATQ (Skrull Scientist 0, pas Hydra Mercenary 1) et lui donne +X ATQ » VERT; « ] sk177 Blessed by Sl'gur't : le bonus SUIT les jetons de foi (1 -> 3) » VERT; « ] sk177 Blessed by Sl'gur't : aucun sbire en jeu -> Renfort » VERT; « ] sk177 Boost (attaque) : +2 icones : l'attaque du mechant inflige 1 + 1 + 2 = 4 degats » VERT; « ] sk177 Boost, TEMOIN : pendant une MANIGANCE les 2 icones ne s'ajoutent pas (2 + 1 = 3 menaces, deux joueurs) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement dessine porte par le sbire ; ATQ qui suit les jetons). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk178 : Nogor

- [x] Etape 2 : carte(s) de reference : `gorr/gb009`, `brawn/bw016` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk178.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « FOR EACH faith counter ON THE VILLAIN ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "SCH": "1", "ATK": "1", "Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « ] sk178 Nogor : +1 MNG, +1 ATQ et +1 PV par jeton de foi sur le mechant (1 jeton) » VERT; « ] sk178 Nogor : les bonus suivent les jetons (1 -> 4) et un Nogor blesse ne guerit pas » VERT; « ] sk178 Nogor revele : retourne le mechant (When Revealed) » VERT; « ] sk178 Nogor en Boost : retourne le mechant (face visible d'arrivee = Sl'gur't) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/4.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (sbire dont MNG, ATQ et PV suivent les jetons ; retourne le mechant). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk179 : Shapeless Wastes

- [x] Etape 2 : carte(s) de reference : `hunting_season/hs222` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk179.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « an ALLY OR a MINION ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "2", "Hinder": "2*", "Boost": "3"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 6/6 cas verts : « ] sk179 Shapeless Wastes : Hinder 2[per_hero] + menace fixe 2 = 4 menaces (un joueur) » VERT; « ] sk179 Shapeless Wastes : deux joueurs -> 2 + 2*2 = 6 menaces » VERT; « ] sk179 Reponse forcee : un sbire SKRULL vaincu -> le mechant est retourne » VERT; « ] sk179 Reponse forcee : un sbire NON-Skrull vaincu -> 1 jeton de foi (pas de retournement) » VERT; « ] sk179 Reponse forcee : un ALLIE non-Skrull vaincu -> 1 jeton de foi » VERT; « ] sk179 Reponse forcee, TEMOIN : sans la carte en jeu, un sbire vaincu ne pose aucun jeton » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/6 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (complot annexe ; retourne le mechant ou pose un jeton de foi). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk180 : Strengthen the Faith

- [x] Etape 2 : carte(s) de reference : `hunting_season/hs222` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk180.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « a SKRULL MINION ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "2*", "Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « ] sk180 Strengthen the Faith : menace 2[per_hero] a la revelation (un joueur : 2 ; deux joueurs : 4) » VERT; « ] sk180 Reponse forcee : un sbire SKRULL entre en jeu -> 1 jeton de foi » VERT; « ] sk180 Reponse forcee, TEMOIN : un sbire NON-Skrull entre en jeu -> rien » VERT; « ] sk180 Reponse forcee, TEMOIN : un ALLIE ne declenche pas (« SKRULL minion ») » VERT; « ] sk180 Boost : place 1 jeton de foi (pendant l'attaque du mechant) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (complot annexe ; pose des jetons de foi). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk181 : Prayer to Kly'bn

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk181.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « if KLY'BN is in play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « ] sk181 Prayer to Kly'bn : Kly'bn en jeu -> il s'active contre le joueur (heros : ATQ 1 + 0 = 1 degat) » VERT; « ] sk181 Prayer to Kly'bn : Kly'bn PAS en jeu (face Sl'gur't visible) -> le mechant est retourne vers Kly'bn » VERT; « ] sk181 Boost : Kly'bn pas en jeu -> retourne le mechant (face visible Sl'gur't, attaque du mechant) » VERT; « ] sk181 Boost, TEMOIN : Kly'bn EN jeu -> pas de retournement » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (retourne le mechant (la face visible change)). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk182 : Prayer to Sl'gur't

- [x] Etape 2 : carte(s) de reference : `sk181` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk182.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « if SL'GUR'T is in play »; « SHE activates against YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « ] sk182 Prayer to Sl'gur't : Sl'gur't en jeu -> elle s'active contre le joueur (heros : ATQ 2 = 2 degats) » VERT; « ] sk182 Prayer to Sl'gur't : Sl'gur't PAS en jeu (face Kly'bn visible) -> le mechant est retourne vers Sl'gur't » VERT; « ] sk182 Boost : Sl'gur't pas en jeu -> retourne le mechant (face visible Kly'bn) » VERT; « ] sk182 Boost, TEMOIN : Sl'gur't EN jeu -> pas de retournement » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/4.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (retourne le mechant (la face visible change)). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk183 : Talisman of the Skrulls

- [x] Etape 2 : carte(s) de reference : `01136`, `skrull_empire/sk103` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_pantheon/sk183.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Search the encounter deck AND DISCARD PILE »; « reveal HIM ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "3"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « ] sk183 Talisman of the Skrulls : Nogor est cherche dans le DECK et revele (il retourne le mechant), pas de Renfort » VERT; « ] sk183 Talisman : Nogor est cherche aussi dans la DEFAUSSE rencontre » VERT; « ] sk183 Talisman : Nogor introuvable -> la carte gagne Renfort (le sbire au-dessus du deck est revele) » VERT; « ] sk183 Talisman : Nogor deja EN JEU -> il n'entre pas en jeu : Renfort » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/4.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (revele Nogor, qui retourne le mechant). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk184 : Dard'van Fanatic

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/dardvan_sect/sk184.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EITHER ... OR »; « each character YOU CONTROL ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "SCH": "2", "ATK": "2", "Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « ] sk184 Dard'van Fanatic : 1 degat a chaque personnage qu'on controle (choix 1) » VERT; « ] sk184 Dard'van Fanatic : 1 menace sur chaque complot en jeu (choix 2), complot principal compris » VERT; « ] sk184 Dard'van Fanatic : le choix des degats touche aussi les allies que le joueur controle » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (degats ou menace chiffres (jauges deja couvertes)).

Carte terminée : OUI

### sk185 : Dard'van Priest

- [x] Etape 2 : carte(s) de reference : `jessica_jones/jj019`, `sk046`, `27083` (detail et justification en tete de `src/cards/pack/skrull_menace/dardvan_sect/sk185.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « INSTEAD ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "SCH": "2", "ATK": "0*", "Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « ] sk185 Dard'van Priest : « When Revealed » : il comploter (menace sur le complot principal) » VERT; « ] sk185 Dard'van Priest : Interruption forcee : il N'ATTAQUE PAS, il resout le When Revealed d'une carte en jeu (Fanatic : 1 degat au heros) » VERT; « ] sk185 Dard'van Priest : le choix peut viser le MECHANT : +1 jeton de foi » VERT; « ] sk185 Dard'van Priest, TEMOIN : sans l'Interruption, une attaque ordinaire n'a aucun effet de revelation (foi inchangee) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (comploter ou resoudre le When Revealed d'une autre carte : effets chiffres deja couverts).

Carte terminée : OUI

### sk186 : Dard'van Sect

- [x] Etape 2 : carte(s) de reference : `30037` (detail et justification en tete de `src/cards/pack/skrull_menace/dardvan_sect/sk186.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the VILLAIN »; « FACEDOWN boost card ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "2*", "Hazard": "1", "Boost": "3"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « ] sk186 Dard'van Sect : le mechant recoit 1 carte de boost face cachee ; menace 2[per_hero] ; icone Hazard » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (donne une carte de boost face cachee au mechant ; icone Hazard). Cas plateau : `ui-app/src/board/pantheon-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk187 : Collective Prayers

- [x] Etape 2 : carte(s) de reference : `texas_twister/tt015` (detail et justification en tete de `src/cards/pack/skrull_menace/dardvan_sect/sk187.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the top card ... FOR EACH character in play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « ] sk187 Collective Prayers : defausse 1 carte par personnage en jeu (identite + mechant = 2) et revele celles du set Dard'van Sect » VERT; « ] sk187 Collective Prayers : le nombre de cartes suit le nombre de personnages (identite + allie + mechant = 3) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (defausse et revele des cartes du set : effets deja couverts).

Carte terminée : OUI

### sk188 : Sectarian Practices

- [x] Etape 2 : carte(s) de reference : `sk046`, `27083`, `skrull_empire/sk103` (detail et justification en tete de `src/cards/pack/skrull_menace/dardvan_sect/sk188.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « a card IN PLAY »; « that ability ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « ] sk188 Sectarian Practices : resout le When Revealed d'une carte en jeu (choix force : le mechant, +1 jeton de foi), pas de Renfort » VERT; « ] sk188 Sectarian Practices : le When Revealed du complot 2B (« flip the villain ») peut etre choisi » VERT; « ] sk188 Sectarian Practices (autre scenario, Rhino) : aucune carte en jeu avec un When Revealed -> Renfort (la carte suivante est revelee) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (resout le When Revealed d'une autre carte : effets deja couverts).

Carte terminée : OUI
