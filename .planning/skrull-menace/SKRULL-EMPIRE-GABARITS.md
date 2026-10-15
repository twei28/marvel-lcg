# Skrull Empire (scenario 1 de Skrull Menace, Kajislav) — gabarits PROCESSUS-CARTE

Pack `skrull_menace`, card_id sk070-sk116 : scenario Skrull Empire (sk070-106),
sets modulaires Skrull Society (sk107-112) et Army of Skrulls (sk113-116), plus
la carte technique `skrull_minion` (gabarit d'Impostor, comme `controlled_minion`).
Fiches generees le 15/10/2026 a partir des resultats REELS (rapport
test_capacites, sorties de substituer_pack.py, en-tetes des modules).

Rappels communs a toutes les cartes :
- **Etape 6 (nombres)** : stats, PV, menaces (depart / objectif / escalade), boosts et icones (Acceleration, Hazard, Crisis, Amplify) relus sur les SCANS de l'auteur contre `data/cards.json` : conformes.
- **Etape 7 (tests)** : 72 cas `[sk-e]` dans `tools/test_capacites.py`. Les planetes aleatoires sont retirees (`Puzzle.Remove` des 9) pour mesurer sur un plateau connu.
- **Etape 8 (autoplay)** : 16 parties spider_man contre Skrull Empire (8 normal + 8 expert) et 8 parties hulkling_kajislav : 0 traceback, 0 partie bloquee (24/24 finies). 0 victoire : le profil `equilibre` du bot ne frappe jamais un mechant a PV infinis (journal : Thwart, Defense, Incite Rebellion, jamais Attack), il ne mesure donc PAS l'equilibrage ; il prouve que le scenario se joue sans erreur du debut a l'elimination (5 rounds en moyenne).
- **Outils statiques** : `verifier_appels_modules skrull_menace` OK ; `verifier_api_cartes` sans faute sur le pack (13 fautes anciennes, dans d'autres packs).
- **Bugs trouves par les tests et corriges** :
  - Fin de stade : le premier mechant du stade suivant porte le MEME nom unique (« * Emperor Dorrek I ») ; revele avant le retrait de l'ancien, la regle d'unicite le defaussait. On retire d'abord, puis on installe (`FinDeStade`).
  - Tarnax II : `get_new_value` doit rendre une grandeur positive (le signe vient de `target_threat=-1`, modele hs224) ; une valeur negative etait lue comme un retrait.
  - Tarnax IV : `ThisGainKeywordWhileFaceIsInPlay` refuse un environnement (assertion interne) ; reecrit avec `WhileValid`.
- **Limite connue** : un soin « du mechant » venu d'un set qui ne passe pas par `SoignerLeMechant` ne soigne rien (le mechant a des PV infinis). Aucun set de ce scenario (Skrull Empire, Skrull Society, Army of Skrulls, Standard, Expert) n'en contient ; seul un set modulaire ajoute a la main pourrait le faire.

- **Etape 8 bis (plateau)** : `ui-app/src/board/skrull-empire-plateau.test.ts` (5 cas, etat CAPTURE sur le moteur le 15/10/2026), vus ROUGES sur un etat casse (4/5), puis VERTS ; `skrull-empire-cadran.test.ts` (6 cas : cadran de PV, pastille INF masquee, temoin Collector).
- **Point d'attention** : 4 cas Squirrel Girl (sg006/007/009/013) sont rouges AVANT et APRES mes changements de fichiers partages (verifie en les retablissant a HEAD) : regression anterieure, hors perimetre, a traiter a part. Un cas sr005/sr002 rouge dans la batterie complete etait un faux echec (processus mort sous charge), vert au second passage.


### sk070 : Emperor Dorrek I

- [x] Etape 2 : carte(s) de reference : `41002b`, `sk032` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk070.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « attacks gain ranged »; « basic ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "INF", "ATK": "1*", "SCH": "2", "Stage": "1", "Retaliate": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk070 Dorrek I — attaque a distance : la Riposte de l'allie defenseur est ignoree » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (mechant en jeu sans pastille INF : ses PV sont sur l'environnement). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk071 : Emperor Dorrek I

- [x] Etape 2 : carte(s) de reference : `41002b`, `sk032` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk071.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « attacks gain ranged »; « basic ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "INF", "ATK": "2*", "SCH": "2", "Stage": "2", "Retaliate": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk071 Dorrek I (II, expert) — attaque a distance : Riposte ignoree » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (mechant du stade II, meme marque). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk072 : Emperor Dorrek I

- [x] Etape 2 : carte(s) de reference : `41002b`, `sk032` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk072.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « attacks gain ranged »; « basic ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "INF", "ATK": "2*", "SCH": "3", "Stage": "3", "Retaliate": "2"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk072 / sk088 Stade III (expert) — Dorrek I III a distance, degats sur l'environnement III » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (mechant du stade III, meme marque). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk073 : Emperor Dorrek VII

- [x] Etape 2 : carte(s) de reference : `sk032`, `41002b` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk073.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun mot-piege dans un texte de mots-cles.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "INF", "ATK": "2*", "SCH": "1", "Stage": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk073 Dorrek VII — revele : Incite 1 par joueur sur le complot principal » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (mechant revele, meme marque). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk074 : Emperor Dorrek VII

- [x] Etape 2 : carte(s) de reference : `sk032`, `41002b` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk074.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun mot-piege dans un texte de mots-cles.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "INF", "ATK": "3*", "SCH": "1", "Stage": "2"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk074 Dorrek VII (II, expert) — revele : Incite 1 par joueur » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (meme marque). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk075 : Emperor Dorrek VII

- [x] Etape 2 : carte(s) de reference : `sk032`, `41002b` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk075.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun mot-piege dans un texte de mots-cles.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "INF", "ATK": "4*", "SCH": "2", "Stage": "3"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk075 Dorrek VII (III, expert) — revele au stade III : Incite 1 par joueur » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (meme marque). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk076 : Empress R'Klll

- [x] Etape 2 : carte(s) de reference : `sk032` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk076.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun mot-piege dans un texte de mots-cles.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "INF", "ATK": "1*", "SCH": "2", "Stage": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk076 R'Klll — revelee : elle attaque chaque heros » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (meme marque). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk077 : Empress R'Klll

- [x] Etape 2 : carte(s) de reference : `sk032` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk077.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun mot-piege dans un texte de mots-cles.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "INF", "ATK": "1*", "SCH": "3", "Stage": "2"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk077 R'Klll (II, expert) — revelee : elle attaque le heros » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (meme marque). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk078 : Empress R'Klll

- [x] Etape 2 : carte(s) de reference : `sk032` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk078.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun mot-piege dans un texte de mots-cles.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "INF", "ATK": "2*", "SCH": "4", "Stage": "3"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk078 R'Klll (III, expert) — revelee au stade III : elle attaque le heros » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (meme marque). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk079 : Empress S'Byll

- [x] Etape 2 : carte(s) de reference : aucune, PAS DE SCRIPT : texte = mots-cles natifs (Steady. Toughness.) portes par le desc.
- [x] Etape 5 : texte-contre-code : mots-cles du desc {"HP": "INF", "ATK": "2", "SCH": "2", "Stage": "1", "Steady": "1", "Toughness": "1"} relus contre le texte imprime.
      Resultat : conforme.
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "INF", "ATK": "2", "SCH": "2", "Stage": "1", "Steady": "1", "Toughness": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk079 S'Byll — Toughness : la premiere attaque ne blesse pas l'environnement » VERT.
      Substitution : sans objet (pas de module) ; le cas mesure le mot-cle natif.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (meme marque, carte Tough de Toughness). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk080 : Empress S'Byll

- [x] Etape 2 : carte(s) de reference : aucune, PAS DE SCRIPT : texte = mots-cles natifs (Steady. Toughness.) portes par le desc.
- [x] Etape 5 : texte-contre-code : mots-cles du desc {"HP": "INF", "ATK": "3", "SCH": "2", "Stage": "2", "Steady": "1", "Toughness": "1"} relus contre le texte imprime.
      Resultat : conforme.
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "INF", "ATK": "3", "SCH": "2", "Stage": "2", "Steady": "1", "Toughness": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk079 S'Byll — Toughness : la premiere attaque ne blesse pas l'environnement » VERT.
      Substitution : sans objet (pas de module) ; le cas mesure le mot-cle natif.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (meme marque). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk081 : Empress S'Byll

- [x] Etape 2 : carte(s) de reference : aucune, PAS DE SCRIPT : texte = mots-cles natifs (Stalwart. Toughness.) portes par le desc.
- [x] Etape 5 : texte-contre-code : mots-cles du desc {"HP": "INF", "ATK": "3", "SCH": "3", "Stage": "3", "Stalwart": "1", "Toughness": "1"} relus contre le texte imprime.
      Resultat : conforme.
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "INF", "ATK": "3", "SCH": "3", "Stage": "3", "Stalwart": "1", "Toughness": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk079 S'Byll — Toughness : la premiere attaque ne blesse pas l'environnement » VERT.
      Substitution : sans objet (pas de module) ; le cas mesure le mot-cle natif.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (meme marque). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk082a : Rise of the Skrull Empire

- [x] Etape 2 : carte(s) de reference : `55033a`, `hs107a` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk082a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun mot-piege dans un texte de mots-cles.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk082a Setup : Dorrek I, environnement Skrull Empire, complot 1B et 1 planete » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (mise en place : paquet PLANET, environnement, mechant). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk082b : Rise of the Skrull Empire

- [x] Etape 2 : carte(s) de reference : `21129` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk082b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Reveal »; « put into play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "1", "TargetThreat": "6*", "EscalationThreat": "2*", "StartingThreat": "0"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk082b Rise of the Skrull Empire 1B — revelee : une planete du paquet PLANET » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (une planete revelee dans la zone environnement). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk083a : Andromeda Galaxy Colonization

- [x] Etape 2 : carte(s) de reference : `01116b` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk083a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « a SKRULL minion ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "2"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk083a Andromeda Galaxy Colonization 2A — un sbire SKRULL entre en jeu » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (un sbire entre en jeu engage). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk083b : Andromeda Galaxy Colonization

- [x] Etape 2 : carte(s) de reference : `21129` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk083b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Reveal »; « put into play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "2", "TargetThreat": "7*", "EscalationThreat": "1*", "StartingThreat": "2*"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk083b Andromeda Galaxy Colonization 2B — revelee : une 2e planete » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (une planete revelee). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk084a : Further Empire Expansion

- [x] Etape 2 : carte(s) de reference : `01116b` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk084a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « a SKRULL minion ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "3"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk084a Further Empire Expansion 3A — un 2e sbire SKRULL entre en jeu » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (un sbire entre en jeu engage). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk084b : Further Empire Expansion

- [x] Etape 2 : carte(s) de reference : `21129` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk084b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Reveal »; « put into play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "3", "TargetThreat": "5*", "EscalationThreat": "1*", "StartingThreat": "0"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk084b Further Empire Expansion 3B — revelee : une 3e planete » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (une planete revelee). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk085a : Entire Universe Domination

- [x] Etape 2 : carte(s) de reference : `01116b` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk085a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « a SKRULL minion ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "4"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk085a Entire Universe Domination 4A — un 3e sbire SKRULL entre en jeu » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (un sbire entre en jeu engage). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk085b : Entire Universe Domination

- [x] Etape 2 : carte(s) de reference : `21129` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk085b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Reveal »; « put into play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "4", "TargetThreat": "9*", "EscalationThreat": "2*", "StartingThreat": "1*"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk085b Entire Universe Domination 4B — revelee : une 4e planete » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (une planete revelee). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk086 : Skrull Empire

- [x] Etape 2 : carte(s) de reference : `21100a`, `39031`, `16073b`, `40092` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk086.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Limit once per round PER PLAYER »; « its PRINTED text box ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk086 Skrull Empire — l'attaque sur le mechant blesse l'environnement » VERT; « sk086 Skrull Empire — a 0 PV : stade II (environnement II, Dorrek I stade II) » VERT; « sk086 Incite Rebellion — incliner son heros : la planete est vierge jusqu'a la fin du round » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? OUI (once per round per player) : cas « sk086 Incite Rebellion », `LimitOncePerRoundPerPlayer` (factory native).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (cadran de PV : pastille et jauge sur l'environnement). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk087 : Skrull Empire

- [x] Etape 2 : carte(s) de reference : `21100a`, `39031`, `16073b`, `40092` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk087.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Limit once per round PER PLAYER »; « its PRINTED text box ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk087 Skrull Empire II — a 0 PV en mode normal : dernier stade, les joueurs gagnent » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? OUI (once per round per player) : cas « sk086 Incite Rebellion », `LimitOncePerRoundPerPlayer` (factory native).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (cadran de PV du stade II). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk088 : Skrull Empire

- [x] Etape 2 : carte(s) de reference : `21100a`, `39031`, `16073b`, `40092` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk088.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Limit once per round PER PLAYER »; « its PRINTED text box ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk072 / sk088 Stade III (expert) — Dorrek I III a distance, degats sur l'environnement III » VERT; « sk088 Skrull Empire III — revele : les Overthrow mis de cote retournent dans le deck » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? OUI (once per round per player) : cas « sk086 Incite Rebellion », `LimitOncePerRoundPerPlayer` (factory native).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (cadran de PV du stade III). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk089 : Aks'Lo

- [x] Etape 2 : carte(s) de reference : `as012` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk089.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Each SKRULL **minion** ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk089 Aks'Lo — les sbires SKRULL ont +2 PV » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (planete en jeu (zone environnement)). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk090 : Hy'lt Minor

- [x] Etape 2 : carte(s) de reference : `st005b` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk090.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Each **identity** ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk090 Hy'lt Minor — chaque identite a -1 REC » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (planete en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk091 : Satriani

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk091.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « gains guard ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk091 Satriani — chaque sbire SKRULL gagne Garde » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (planete en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk092 : Skrell

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk092.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « **minion** ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk092 Skrell — chaque sbire SKRULL gagne +1 MNG » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (planete en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk093 : Skrullos

- [x] Etape 2 : carte(s) de reference : `st016`, `40109` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk093.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Each side scheme ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk093 Skrullos — chaque complot annexe gagne l'icone de crise » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (planete en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk094 : Tarnax II

- [x] Etape 2 : carte(s) de reference : `hs224` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk094.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « by 1[per_hero] »; « the main scheme ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk094 Tarnax II — menace cible du complot principal -1 par joueur » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (planete en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk095 : Tarnax IV

- [x] Etape 2 : carte(s) de reference : `40109` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk095.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « **a** side scheme »; « this card ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk095 Tarnax IV — complot annexe en jeu : elle gagne l'icone d'amplification » VERT; « sk095 Tarnax IV — CONTRE-CAS sans complot annexe : pas d'amplification » VERT; « sk095 Tarnax IV — le complot annexe quitte le jeu : l'icone d'amplification s'en va » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (planete en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk096 : Tarnax VII

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk096.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « **minion** ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk096 Tarnax VII — chaque sbire SKRULL gagne +1 ATQ » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (planete en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk097 : Zaragz'na

- [x] Etape 2 : carte(s) de reference : `40171` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk097.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Each ally and support ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk097 Zaragz'na — les allies entrent en jeu inclines » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (planete en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk098 : Impostor

- [x] Etape 2 : carte(s) de reference : `36038` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk098.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « NON-SKRULL ally »; « most REMAINING hit points ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk098 Impostor — l'allie devient un sbire SKRULL » VERT; « sk098 Impostor — CONTRE-CAS sans allie : le mechant manigance » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement : l'allie devient un sbire engage). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk099 : Intelligentsia

- [x] Etape 2 : carte(s) de reference : `40146`, `39012a` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk099.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « each OTHER »; « SKRULL ENEMY ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "5", "SCH": "2", "ATK": "0*", "Acceleration": "1", "Boost": "2"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk099 Intelligentsia — +1 SCH aux AUTRES ennemis SKRULL (mechant compris) » VERT; « sk099 Intelligentsia — elle manigance au lieu d'attaquer » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (sbire en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk100 : Emperor's Throne

- [x] Etape 2 : carte(s) de reference : `32072`, `60093` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk100.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the villain »; « even if ... alter-ego ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "2*", "Acceleration": "1", "Hazard": "1", "Boost": "3"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk100 Emperor's Throne — vaincu : le mechant attaque celui qui l'a vaincu » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (complot annexe en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk101 : Seeking a Suitable World

- [x] Etape 2 : carte(s) de reference : aucune, PAS DE SCRIPT : texte = mots-cles natifs (Incite 2.) portes par le desc.
- [x] Etape 5 : texte-contre-code : mots-cles du desc {"StartingThreat": "3*", "Incite": "2", "Acceleration": "1"} relus contre le texte imprime.
      Resultat : conforme.
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "3*", "Incite": "2", "Acceleration": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk101 Seeking a Suitable World — Incite 2 (mot-cle natif, sans module) : 2 menaces sur le complot principal » VERT.
      Substitution : sans objet (pas de module) ; le cas mesure le mot-cle natif.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (complot annexe en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk102 : A New Skrull Is Born

- [x] Etape 2 : carte(s) de reference : `01116b` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk102.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun mot-piege dans un texte de mots-cles.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk102 A New Skrull Is Born — defausse jusqu'a un sbire SKRULL et le revele » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (le sbire revele entre en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk103 : Giving Orders

- [x] Etape 2 : carte(s) de reference : `36039` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk103.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH SKRULL minion »; « activates ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk103 Giving Orders — CONTRE-CAS sans sbire SKRULL : surge » VERT; « sk103 Giving Orders — le sbire SKRULL engage s'active (attaque le heros) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (activation des sbires : degats et menace seulement).

Carte terminée : OUI

### sk104 : Long Live the Empire

- [x] Etape 2 : carte(s) de reference : `36039`, `mf016` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk104.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the villain ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk104 Long Live the Empire — soigne 2 x ennemis SKRULL sur l'environnement » VERT; « sk104 Long Live the Empire — CONTRE-CAS rien a soigner : surge » VERT; « sk104 Long Live the Empire — Boost : soigne 1 par ennemi SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (compteurs de degats de l'environnement seulement (cadran deja couvert par sk086)).

Carte terminée : OUI

### sk105 : Overthrow

- [x] Etape 2 : carte(s) de reference : `55051`, `44037`, `32167` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk105.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « REMOVE ... from the game ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk105 Overthrow — le mechant est remplace par le suivant du paquet (Dorrek VII) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (changement de mechant, Overthrow mis de cote). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk106 : Wrath of the Empire

- [x] Etape 2 : carte(s) de reference : `46028` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_empire/sk106.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « 2 cards FOR EACH planet »; « 1 acceleration token ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « sk106 Wrath of the Empire — 1 planete : 2 cartes defaussees, jeton d'acceleration » VERT; « sk106 Wrath of the Empire — CONTRE-CAS sans planete : rien n'est defausse » VERT; « sk106 Wrath of the Empire — Boost : +1 icone par planete (manigance 2 + 1) » VERT; « sk106 Wrath of the Empire — Boost TEMOIN sans planete : manigance 2 » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (defausse et jeton d'acceleration (chiffres)).

Carte terminée : OUI

### sk107 : Skrull Scientist

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_society/sk107.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « AFTER this activation ends ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "SCH": "3", "ATK": "0", "Acceleration": "1", "Boost": "2"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk107 Skrull Scientist — Boost : soigne 2 (l'environnement) apres l'activation » VERT; « sk107 Skrull Scientist — Boost hors Skrull Empire : soigne le mechant (Rhino) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (sbire en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk108 : Skrull Spy

- [x] Etape 2 : carte(s) de reference : `11044` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_society/sk108.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « RANDOM »; « YOUR hand ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "SCH": "2", "ATK": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk108 Skrull Spy — revele : 1 carte au hasard defaussee de la main » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (sbire en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk109 : Skrull Telepath

- [x] Etape 2 : carte(s) de reference : `40146`, `16140` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_society/sk109.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « If this activation is a SCHEME ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "SCH": "2", "ATK": "0*"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk109 Skrull Telepath — il manigance au lieu d'attaquer » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (sbire en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk110 : Skrull Warrior

- [x] Etape 2 : carte(s) de reference : `04145` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_society/sk110.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « YOU are stunned ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "SCH": "2", "ATK": "2", "Guard": "1", "Boost": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk110 Skrull Warrior — Boost sur attaque sans defense : tu es sonne » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (sbire en jeu, carte d'etat Stunned). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk111 : Plotting Revenge

- [x] Etape 2 : carte(s) de reference : aucune, PAS DE SCRIPT : texte = mots-cles natifs (Hinder 2[per_hero].) portes par le desc.
- [x] Etape 5 : texte-contre-code : mots-cles du desc {"StartingThreat": "2", "Hinder": "2*", "Acceleration": "1", "Boost": "2"} relus contre le texte imprime.
      Resultat : conforme.
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "2", "Hinder": "2*", "Acceleration": "1", "Boost": "2"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk111 Plotting Revenge — Hinder 2 (mot-cle natif, sans module) : 2 menaces de plus sur la carte » VERT.
      Substitution : sans objet (pas de module) ; le cas mesure le mot-cle natif.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (complot annexe en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk112 : Outnumbered

- [x] Etape 2 : carte(s) de reference : `27141`, `Reveal`, `46028` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_society/sk112.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH Skrull minion IN PLAY ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk112 Outnumbered — fouille deck et defausse : un sbire SKRULL revele » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (sbire revele en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk113 : Skrull Commander

- [x] Etape 2 : carte(s) de reference : `60075`, `46028` (detail et justification en tete de `src/cards/pack/skrull_menace/army_of_skrulls/sk113.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « each OTHER Skrull MINION ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "5", "SCH": "2", "ATK": "2", "Boost": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk113 Skrull Commander — +1 ATK aux AUTRES sbires SKRULL seulement » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (sbire en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk114 : Skrull Soldier

- [x] Etape 2 : carte(s) de reference : `ho015`, `46028` (detail et justification en tete de `src/cards/pack/skrull_menace/army_of_skrulls/sk114.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH side scheme »; « YOUR deck ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "SCH": "2", "ATK": "2", "Boost": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk114 Skrull Soldier — revele : 2 menaces sur chaque complot annexe » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (sbire en jeu). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk115 : Hijacked

- [x] Etape 2 : carte(s) de reference : `04122`, `16140` (detail et justification en tete de `src/cards/pack/skrull_menace/army_of_skrulls/sk115.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « YOUR deck, discard pile and HAND »; « an ally ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "4", "Hinder": "1*", "Crisis": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk115 Hijacked — revele : un allie de la main passe sous le complot » VERT; « sk115 Hijacked — vaincu : l'allie dessous entre en jeu sous le controle de son proprietaire » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (complot annexe, allie place dessous). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk116 : Skrull Assault

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/army_of_skrulls/sk116.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « attacks the HERO ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk116 Skrull Assault — CONTRE-CAS sans sbire SKRULL : surge » VERT; « sk116 Skrull Assault — le sbire SKRULL engage attaque le heros » VERT; « sk116 Skrull Assault — Boost : +1 icone par ennemi SKRULL (mechant + 2 sbires = +3) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (attaques des sbires : degats seulement).

Carte terminée : OUI
