# Paibok (scenario 3 de Skrull Menace, Kajislav) et New Revengers — gabarits PROCESSUS-CARTE

Pack `skrull_menace`, card_id sk141-sk160 (scenario Paibok : mechant I/II/III, complots principaux 1A/1B et 2A/2B,
attachements POWER SKRULL et conditions, sbires, complots annexes, traitrises) et sk161-sk169 (set modulaire New
Revengers : environnement, six sbires, complot annexe, traitrise). Fiches generees a partir des resultats REELS
(rapport test_capacites, sorties de substituer_pack.py, en-tetes des modules) par
`.planning/skrull-menace/defs/generer_gabarits_paibok.py`.

Rappels communs a toutes les cartes :
- **Etape 6 (nombres)** : stats, PV, menaces (depart / objectif / escalade), boosts et icones (Acceleration, Hazard) relus sur les SCANS de l'auteur (1500x2150, tous vus un par un) contre `data/cards.json` : conformes. Lectures corrigees par rapport a la transcription : Captain Paibok porte une icone HAZARD (sk146), The Revenge Time une icone ACCELERATION (sk168). Voir `defs/paibok_questions.md`.
- **Etape 7 (tests)** : cas `[paibok]` dans `tools/cas/paibok.py` (charge par `tools/test_capacites.py`). Chaque mesure part d'un plateau connu : `Puzzle.Remove` des quatre POWER SKRULL (celui que 1B revele au hasard a la mise en place compris), main fixee par `main_exclusive`, deck rencontre monte par `CreateEncounterDeck`. Pieges payes pendant les tests :
  - la main de depart de Spider-Man contient `01061` Great Responsibility, qui remplace tout `SetThreat` par des degats : `Puzzle.EmptyHand()` AVANT de poser la menace ;
  - `Puzzle.Reveal` sur un deck rencontre VIDE declenche l'epuisement du deck (la defausse entiere est remelangee et un pion Acceleration est pose) : toujours laisser une carte dans le deck ;
  - le pilote du harnais finance un cout « 1 ressource de n'importe quel type » avec la capacite de RESSOURCE de l'identite (Peter Parker, `[mental]`) plutot qu'avec la main : `payer_avec` impose la carte ;
  - l'alter ego de Spider-Man genere toujours une ressource : le cas « changement de forme refuse » prend T'Challa (aucune ressource).
- **Substitution (`substituer_pack.py`, trois passes sk14/sk15/sk16 puis sk157 et sk166 apres correctif, empreinte md5 du pack identique avant/apres, `git status` propre)** : chaque module est vide a tour de role, les cas filtres sur son card_id doivent tomber. Les cas « vert sans module » de chaque fiche sont TOUS des temoins d'ABSENCE d'effet (nom « TEMOIN », « sans l'attachement ») ou des mesures de comportement NATIF sans module (Hinder de sk157, Quickstrike de sk167, Toughness) ou de persistance du moteur (sk142 « jetons conserves au changement de stade ») : assumes comme le prevoit l'etape 7.
- **Mesure faible assumee** : la remise de la defausse dans le deck de `sk144b` (« Shuffle the encounter discard pile ») n'est mesuree qu'a la mise en place (defausse vide ensuite), le nombre de cartes defaussees avant le POWER SKRULL dependant de l'ordre du deck ; elle ne peut pas etre rejouee seule (`Puzzle.Reveal` d'un complot principal deplace la carte en jeu).
- **Etape 8 (autoplay)** : 64 parties `equilibre` contre `sk_paibok` (normal et expert, 8 graines chacun) : spider_man 2 x 16 (une premiere fournee de 16, une seconde apres correctif) et hulkling_kajislav 16, plus 16 parties spider_man contre Rhino comme TEMOIN. Grep exhaustif `NameError|AttributeError|TypeError|KeyError|AssertionError` sur les 32 journaux de la seconde fournee (spider_man 16 + hulkling_kajislav 16) : **0** (la premiere fournee en avait montre 2, voir ci-dessous). Journaux lus (defaite par les quatre POWER SKRULL « Players Lost » 8 fois sur 32, eliminations, Captain Paibok defaussee par son Action de heros, Surveillance Team qui retire la menace de 2B). 0 victoire : le profil `equilibre` ne ferait pas tomber un Paibok Robuste (le temoin Rhino : 0/16 aussi), ce n'est pas un signal d'equilibrage. **2 parties spider_man sur 16 « bloquees »** (graines 2 normal et 7 expert) : le pilote rejoue sans fin l'Action de heros de `01093` Tenacity (carte OFFICIELLE : « ready your hero » sans cible, le moteur la refuse, `Hero_Action(id=64) WhenPlayerInTurn failed`) : artefact du pilote, sans rapport avec le scenario (0 bloquee sur hulkling_kajislav, 0 sur le temoin Rhino).
  - **Defaut trouve PAR l'autoplay et corrige** : `Settling Scores` (sk157) rejouait un Boost par `ResolveAbility` direct, qui saute les conditions de la capacite ; Vermin (« if this activation is an attack ») plantait en `AttributeError: would_atk_message` quand le Boost venait d'une manigance. Les conditions de la capacite sont maintenant rejouees avec le message d'origine, et sk166 se garde (`getattr`). Aucun cas de la batterie ne le voyait.
- **Outils statiques** : `verifier_appels_modules skrull_menace` OK ; `verifier_api_cartes` sans faute dans skrull_menace.
- **Moteur partage** : uniquement 3 traits et 2 compteurs declares dans `card_face.py` (`defs/paibok_moteur.md`).
- **Limites connues et questions** : `defs/paibok_questions.md` (icone de Captain Paibok, portee de Distracted / Trapped in Ice sur les evenements, repli du premier joueur pour General Kalamari...).
- **Ce qu'aucun outil ne voit** : une vraie partie jouee par un humain dans le navigateur (agrement du scenario, equilibrage du bot : profil `equilibre`), non faite.


### sk141 : Paibok

- [x] Etape 2 : carte(s) de reference : `ih002`, `wd077b` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk141.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « attached TO PAIBOK ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "13*", "ATK": "2", "SCH": "1", "Toughness": "1", "Stage": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « sk141 pouvoirs VERROUILLES : 1 POWER SKRULL, 1 jeton -> impossible de le defausser » VERT; « sk141 pouvoirs verrouilles, TEMOIN : 2 POWER SKRULL pour 1 jeton -> on peut en defausser un » VERT; « sk141 pouvoirs verrouilles, TEMOIN : 0 jeton -> le POWER SKRULL se defausse » VERT; « sk141 la regle ne vise QUE les POWER SKRULL : Captain Paibok (TITLE) se defausse malgre le verrou » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (Paibok porte des jetons de maitrise et des attachements POWER SKRULL). Cas plateau : `ui-app/src/board/paibok-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk142 : Paibok

- [x] Etape 2 : carte(s) de reference : `sk141`, `01136` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk142.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Search the encounter deck AND DISCARD PILE ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "16*", "ATK": "2", "SCH": "2", "Toughness": "1", "Stage": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « sk142 Setup EXPERT : Paibok II, 1 jeton, DEUX POWER SKRULL (1B + « When Revealed » de Paibok II) » VERT; « sk142 Changement de stade : Paibok II garde ses jetons de maitrise ET ses attachements » VERT; « sk142 Paibok II revele : cherche un POWER SKRULL dans le DECK rencontre et le revele (il s'attache) » VERT; « sk142 Paibok II revele : un POWER SKRULL dans la DEFAUSSE rencontre est trouve aussi » VERT; « sk142 Paibok II revele, TEMOIN : aucun POWER SKRULL dans le deck ni la defausse -> rien n'est attache » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (meme marque : jetons de maitrise et attachements sur Paibok II). Cas plateau : `ui-app/src/board/paibok-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk143 : Paibok

- [x] Etape 2 : carte(s) de reference : `sk141`, `sk142` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk143.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "20*", "ATK": "3", "SCH": "3", "Toughness": "1", "Stage": "3"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk143 Paibok III (expert) revele : cherche un POWER SKRULL et le revele (stade II -> stade III) » VERT; « sk143 Paibok III : la regle des pouvoirs s'applique aussi au stade III (1 pouvoir, jetons >= 1 -> verrouille) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (meme marque : jetons de maitrise et attachements sur Paibok III). Cas plateau : `ui-app/src/board/paibok-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk144a : Power Skrull Engineering

- [x] Etape 2 : carte(s) de reference : `an001b`, `ok001b`, `40123` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk144a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « on PAIBOK ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk144a Setup (puis 1B sk144b) : Paibok I en jeu, 1 jeton de maitrise, complot 1B, UN attachement POWER SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (le jeton de maitrise pose a la mise en place sur Paibok). Cas plateau : `ui-app/src/board/paibok-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk144b : Power Skrull Engineering

- [x] Etape 2 : carte(s) de reference : `01116b`, `sk102`, `sk083a`, `32113a` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk144b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Shuffle the encounter DISCARD PILE into the encounter deck ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "1", "TargetThreat": "5*", "EscalationThreat": "1*", "StartingThreat": "1*"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk144a Setup (puis 1B sk144b) : Paibok I en jeu, 1 jeton de maitrise, complot 1B, UN attachement POWER SKRULL » VERT; « sk144b Revelation a la mise en place : la defausse rencontre est REMELANGEE dans le deck (defausse vide) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (revele un attachement POWER SKRULL qui s'accroche a Paibok). Cas plateau : `ui-app/src/board/paibok-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk145a : Mastering Superpowers

- [x] Etape 2 : carte(s) de reference : `24017`, `01136` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk145a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « if Captain Paibok IS IN PLAY ... OTHERWISE ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk145a Revelation : jeton de maitrise +1 ET Captain Paibok (du deck) s'attache a Paibok » VERT; « sk145a Revelation, branche « Captain Paibok est en jeu » : son Boost soigne 2 degats de Paibok » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (jeton de maitrise et Captain Paibok qui s'accroche a Paibok). Cas plateau : `ui-app/src/board/paibok-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk145b : Mastering Superpowers

- [x] Etape 2 : carte(s) de reference : `39002b`, `21099b`, `21184b`, `27102b` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk145b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « remove all threat from here INSTEAD ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "2", "TargetThreat": "5*", "EscalationThreat": "1*", "StartingThreat": "0"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « sk145b Forced Interrupt : le complot « serait accompli » -> jeton +1, menace remise a 0, un POWER SKRULL revele du deck » VERT; « sk145b « discard until POWER SKRULL », bord du deck : le POWER SKRULL est la DERNIERE carte du deck » VERT; « sk145b « when the player phase ends, if all 4 POWER SKRULL are attached to Paibok, the players lose » » VERT; « sk145b defaite, TEMOIN : seulement 3 POWER SKRULL -> pas de defaite » VERT; « sk145b defaite, TEMOIN : quatre POWER SKRULL mais le complot 1B (pas 2B) est en jeu -> pas de defaite » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (jeton de maitrise, menace remise a 0, attachement POWER SKRULL revele). Cas plateau : `ui-app/src/board/paibok-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk146 : Captain Paibok

- [x] Etape 2 : carte(s) de reference : `01100`, `sk086`, `04136`, `sk107` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk146.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « → ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "2", "Hazard": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk146 Captain Paibok : s'attache a Paibok et porte une icone HAZARD » VERT; « sk146 Captain Paibok : Boost -> Paibok soigne 2 degats » VERT; « sk146 Captain Paibok : Action de heros -> resout le Boost de CHAQUE attachement du set (cout), puis se defausse » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement accroche a Paibok, avec son icone Hazard). Cas plateau : `ui-app/src/board/paibok-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk147 : Distracted

- [x] Etape 2 : carte(s) de reference : `27166` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk147.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « When YOU thwart »; « by 1 ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 8/8 cas verts : « sk147 Distracted : s'attache a l'identite » VERT; « sk147 Distracted : Interruption forcee -> un contre retire 1 menace de MOINS (4 -> 4 au lieu de 3) » VERT; « sk147 Distracted, TEMOIN : sans l'attachement le meme contre retire 1 menace (4 -> 3) » VERT; « sk147 Distracted : Boost -> 1 menace sur le complot principal (en plus de la manigance de Paibok) » VERT; « sk147 Distracted, TEMOIN : une carte de boost sans effet ne pose que la manigance (1 + 1 = 2) » VERT; « sk147 Distracted : Action de heros [mental][mental] -> defaussee » VERT; « sk147 Distracted : un EVENEMENT de contre (Crisis Interdiction, 2 menaces) retire 1 menace de moins » VERT; « sk147 Distracted, TEMOIN : sans l'attachement Crisis Interdiction retire 2 menaces (4 -> 2) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 5/8 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (condition accrochee a l'identite du joueur). Cas plateau : `ui-app/src/board/paibok-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk148 : Electricity Projection

- [x] Etape 2 : carte(s) de reference : `24017` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk148.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Paibok gains retaliate 1 »; « a character YOU CONTROL ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1", "ATK+": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « sk148 Electricity Projection : Paibok gagne Riposte 1 et +1 ATQ » VERT; « sk148 Electricity Projection : Boost -> un personnage qu'on controle est etourdi » VERT; « sk148 Electricity Projection : Action de heros [mental][physical] -> la carte est defaussee (2 POWER SKRULL, 1 jeton) » VERT; « sk148 Action de heros NON OFFERTE quand les pouvoirs sont verrouilles (1 POWER SKRULL, 1 jeton) » VERT; « sk148 Action de heros OFFERTE des qu'il y a plus d'attachements que de jetons (TEMOIN) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 5/5.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement accroche a Paibok (Riposte, ATQ)). Cas plateau : `ui-app/src/board/paibok-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk149 : Hypnotized

- [x] Etape 2 : carte(s) de reference : `27166` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk149.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « to change FORM ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « sk149 Hypnotized : changer de forme coute 1 ressource de plus (Energy depensee, heros en forme heros) » VERT; « sk149 Hypnotized, TEMOIN : sans l'attachement le changement de forme ne coute rien » VERT; « sk149 Hypnotized : sans ressource a depenser, le changement de forme est REFUSE » VERT; « sk149 Hypnotized : Boost -> defausse 1 carte de la main » VERT; « sk149 Hypnotized : Action de heros [energy][energy] -> defaussee » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (condition accrochee a l'identite du joueur). Cas plateau : `ui-app/src/board/paibok-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk150 : Ice Control

- [x] Etape 2 : carte(s) de reference : `01100` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk150.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « After Paibok attacks YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1", "SCH+": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « sk150 Ice Control : Paibok gagne +1 MNG (le badge ATQ a etoile n'a pas de valeur) » VERT; « sk150 Ice Control : Reponse forcee -> apres que Paibok l'attaque, un de ses personnages s'incline » VERT; « sk150 Ice Control, TEMOIN : sans l'attachement, le heros attaque sans defense reste pret » VERT; « sk150 Ice Control : Boost -> un personnage qu'on controle s'incline » VERT; « sk150 Ice Control : Action de heros « 3 ressources de n'importe quel type » -> defaussee (2 POWER SKRULL, 1 jeton) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement accroche a Paibok (MNG)). Cas plateau : `ui-app/src/board/paibok-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk151 : Metallic Skin

- [x] Etape 2 : carte(s) de reference : `01100`, `04136` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk151.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « After PAIBOK takes damage ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1", "ATK+": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « sk151 Metallic Skin : Paibok gagne +1 ATQ » VERT; « sk151 Metallic Skin : Reponse forcee -> apres des degats, Paibok recoit une carte Robuste » VERT; « sk151 Metallic Skin, TEMOIN : sans l'attachement, apres des degats Paibok n'est PAS Robuste » VERT; « sk151 Metallic Skin : Boost -> Paibok recoit une carte Robuste » VERT; « sk151 Metallic Skin : Action de heros [energy][mental] -> defaussee (2 POWER SKRULL, 1 jeton) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement accroche a Paibok (ATQ) et carte d'etat Robuste). Cas plateau : `ui-app/src/board/paibok-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk152 : Shapeshifting

- [x] Etape 2 : carte(s) de reference : `40006`, `24017` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk152.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « gains stalwart AND the AERIAL trait ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1", "SCH+": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « sk152 Shapeshifting : Paibok gagne Solide, le trait AERIAL et +1 MNG » VERT; « sk152 Shapeshifting, TEMOIN : sans l'attachement, Paibok n'est ni Solide ni AERIAL » VERT; « sk152 Shapeshifting : Boost -> un personnage qu'on controle est desoriente » VERT; « sk152 Shapeshifting : Action de heros [energy][physical] -> defaussee (2 POWER SKRULL, 1 jeton) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement accroche a Paibok (MNG, trait AERIAL)). Cas plateau : `ui-app/src/board/paibok-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk153 : Trapped in Ice

- [x] Etape 2 : carte(s) de reference : `27166`, `19018`, `55053` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk153.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « When YOU attack »; « by 1 ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 6/6 cas verts : « sk153 Trapped in Ice : Interruption forcee -> l'attaque de Spider-Man inflige 1 degat de moins (2 -> 1) » VERT; « sk153 Trapped in Ice, TEMOIN : sans l'attachement la meme attaque inflige 2 degats » VERT; « sk153 Trapped in Ice : Boost -> le joueur subit 1 degat » VERT; « sk153 Trapped in Ice : Action de heros [physical][physical] -> defaussee » VERT; « sk153 Trapped in Ice : un EVENEMENT d'attaque (Swinging Web Kick, 8 degats) est reduit lui aussi (7) » VERT; « sk153 Trapped in Ice, TEMOIN : sans l'attachement Swinging Web Kick inflige 8 » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/6 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (condition accrochee a l'identite du joueur). Cas plateau : `ui-app/src/board/paibok-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk154 : Devos the Devastator

- [x] Etape 2 : carte(s) de reference : `50144` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk154.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « FRIENDLY character ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "5", "SCH": "1", "ATK": "4", "Boost": "4"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk154 Devos : un statut sur un personnage AMI -> Devos s'active contre son joueur (attaque ATQ 4) » VERT; « sk154 Devos, TEMOIN : un statut sur un ENNEMI (Paibok) ne le declenche pas » VERT; « sk154 Devos : le joueur est en alter ego -> Devos MANIGANCE (menace +1 sur le complot principal) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (sbire ordinaire ; son activation passe par la phase du mechant deja couverte).

Carte terminée : OUI

### sk155 : General Kalamari

- [x] Etape 2 : carte(s) de reference : `32072`, `24017` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk155.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « The player WHO DEFEATED ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "SCH": "2", "ATK": "2", "Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk155 General Kalamari : vaincu -> le joueur resout le Boost de chaque attachement du set (Distracted : +1 menace) » VERT; « sk155 General Kalamari, TEMOIN : sans attachement du set, sa defaite ne change pas la menace » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (sbire ordinaire ; les Boost qu'il declenche se mesurent sur les attachements).

Carte terminée : OUI

### sk156 : Galactic Ambassador

- [x] Etape 2 : carte(s) de reference : `50134` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk156.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « FOR EACH friendly character WITH A STATUS CARD ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "2*", "Acceleration": "1", "Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk156 Galactic Ambassador : AUCUN personnage avec un statut -> menace de depart seule (2), icone Acceleration » VERT; « sk156 Galactic Ambassador : 2 personnages avec un statut (l'un en a deux) -> +2 par personnage = 2 + 4 » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (complot annexe ordinaire (menace chiffree)).

Carte terminée : OUI

### sk157 : Settling Scores

- [x] Etape 2 : carte(s) de reference : `sk111`, `sk087` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk157.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « ON EACH BOOST CARD ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "2", "Hinder": "2*", "Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk157 Settling Scores : Hinder 2[per_hero] natif -> 2 + 2 = 4 menaces » VERT; « sk157 Settling Scores : revelee -> seuls les POWER SKRULL de la DEFAUSSE rencontre retournent dans le deck » VERT; « sk157 Settling Scores : chaque Boost est resolu UNE FOIS DE PLUS (Distracted : 1 + 2 = 3 menaces ajoutees) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (complot annexe ordinaire (menace chiffree) ; cartes remises dans le deck, hors table).

Carte terminée : OUI

### sk158 : Council Manipulation

- [x] Etape 2 : carte(s) de reference : `sk098`, `01106`, `sk103` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk158.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « IF YOU are stunned or confused ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk158 Council Manipulation : Paibok manigance (1 + 1 = 2) ; joueur ni sonne ni desoriente -> PAS de surge » VERT; « sk158 Council Manipulation : joueur SONNE -> la carte gagne surge (le sbire du dessus est revele) » VERT; « sk158 Council Manipulation : joueur DESORIENTE -> surge aussi » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (traitrise : manigance et surge, chiffres seulement).

Carte terminée : OUI

### sk159 : Getting Ruthless

- [x] Etape 2 : carte(s) de reference : `01106`, `sk100`, `24017` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk159.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « (Alter-Ego) »; « (Hero) ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk159 Getting Ruthless (alter ego) : resout le Boost de chaque attachement du set (Distracted : +1 menace) » VERT; « sk159 Getting Ruthless (heros) : Paibok attaque le joueur (ATQ 2 + 1 carte de boost de 1 icone = 3) » VERT; « sk159 Getting Ruthless (heros) : joueur SONNE -> UNE carte de boost de plus (ATQ 2 + 2 icones = 4) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (traitrise : attaque, chiffres seulement).

Carte terminée : OUI

### sk160 : Power Demonstration

- [x] Etape 2 : carte(s) de reference : `24017` (detail et justification en tete de `src/cards/pack/skrull_menace/paibok/sk160.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « each attachment IN PLAY that belongs to the Paibok SET ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk160 Power Demonstration : resout le Boost de chaque attachement du set (Distracted : +1 menace) » VERT; « sk160 Power Demonstration : plusieurs attachements -> tous resolus (Distracted +1 menace ET Captain Paibok soigne 2) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (traitrise : Boost resolus, effets chiffres ou statuts).

Carte terminée : OUI

### sk161 : O.M.N.I.T.R.O.N.I.C.U.S.

- [x] Etape 2 : carte(s) de reference : `ah015` (detail et justification en tete de `src/cards/pack/skrull_menace/new_revengers/sk161.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « REVENGER MINION ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « sk161 O.M.N.I.T.R.O.N.I.C.U.S. : chaque sbire REVENGER gagne villainous » VERT; « sk161 O.M.N.I.T.R.O.N.I.C.U.S., TEMOIN : sans l'environnement, Angar n'est pas villainous » VERT; « sk161 O.M.N.I.T.R.O.N.I.C.U.S. : un sbire qui n'est PAS REVENGER n'est pas villainous » VERT; « sk161 O.M.N.I.T.R.O.N.I.C.U.S. : Action de heros [energy][energy] -> defaussee quand AUCUN ennemi REVENGER n'est en jeu » VERT; « sk161 O.M.N.I.T.R.O.N.I.C.U.S. : Action de heros NON OFFERTE tant qu'un ennemi REVENGER est en jeu » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (environnement ordinaire ; Vilenie est une propriete, aucune zone nouvelle).

Carte terminée : OUI

### sk162 : Angar the Screamer

- [x] Etape 2 : carte(s) de reference : `41002b`, `sk070` (detail et justification en tete de `src/cards/pack/skrull_menace/new_revengers/sk162.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « his ATTACKS gain ranged ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "SCH": "1", "ATK": "2*", "Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk162 Angar the Screamer : ses attaques gagnent RANGED -> la Riposte du heros (Black Panther) ne le touche pas » VERT; « sk162 Angar, TEMOIN : un sbire SANS ranged (Hydra Mercenary) subit la Riposte 1 de Black Panther » VERT; « sk162 Angar : quand il attaque un heros, son attaque est AUSSI resolue contre l'autre heros (2 joueurs) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (sbire ordinaire (attaque, degats)).

Carte terminée : OUI

### sk163 : Asti the All-Seeing

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/new_revengers/sk163.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « takes ANY AMOUNT of damage ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "SCH": "2", "ATK": "1", "Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk163 Asti the All-Seeing : chaque coup pose 1 jeton d'absorption (2 coups = 2 jetons) » VERT; « sk163 Asti : vaincu avec 1 jeton -> 2 degats INDIRECTS repartis entre les joueurs (1 joueur : 2) » VERT; « sk163 Asti : vaincu avec 3 jetons -> 6 degats indirects (2 par jeton) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (jetons d'absorption poses sur le sbire). Cas plateau : `ui-app/src/board/paibok-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk164 : Skar

- [x] Etape 2 : carte(s) de reference : `sk070` (detail et justification en tete de `src/cards/pack/skrull_menace/new_revengers/sk164.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « a character YOU control ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "SCH": "1", "ATK": "3*", "Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk164 Skar : ses attaques gagnent OVERKILL -> l'exces sur l'allie vaincu passe au heros (3 - 1 PV = 2) » VERT; « sk164 Skar, TEMOIN : Shocker (ATQ 2, sans overkill) vainc l'allie sans rien deverser sur le heros » VERT; « sk164 Skar : revele (heros) -> un personnage qu'on controle s'incline » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (sbire ordinaire (inclinaison)).

Carte terminée : OUI

### sk165 : The Maker

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/new_revengers/sk165.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « ANOTHER REVENGER enemy ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "SCH": "3", "ATK": "1", "Boost": "3"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 6/6 cas verts : « sk165 The Maker : ne subit AUCUN degat tant qu'un AUTRE ennemi REVENGER est en jeu » VERT; « sk165 The Maker, TEMOIN : seul Revenger en jeu, il subit les degats » VERT; « sk165 The Maker : le MECHANT devenu REVENGER (The Revenge Time) suffit a le rendre invulnerable » VERT; « sk165 The Maker : revele -> cherche The Revenge Time dans le deck et la defausse et la revele » VERT; « sk165 The Maker : The Revenge Time dans la DEFAUSSE rencontre est trouvee aussi » VERT; « sk165 The Maker dans le scenario Rhino : revele, il trouve The Revenge Time ; Rhino devenu REVENGER le rend invulnerable » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 5/6 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (sbire ordinaire (invulnerable : chiffres)).

Carte terminée : OUI

### sk166 : Vermin

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/new_revengers/sk166.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « ATTACKS ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "5", "SCH": "1", "ATK": "2*", "Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « sk166 Vermin : ses attaques sont INDIRECTES -> le joueur REPARTIT les degats : l'allie (Black Cat) les encaisse, le heros non » VERT; « sk166 Vermin, TEMOIN : Shocker (ATQ 2, direct) frappe le HEROS, l'allie est intact » VERT; « sk166 Vermin : Boost -> l'attaque de Paibok (ATQ 2 + 1 icone = 3) devient INDIRECTE : l'allie encaisse, le heros non » VERT; « sk166 Vermin, TEMOIN : une carte de boost de 1 icone sans effet -> attaque DIRECTE : le heros encaisse 3, l'allie est intact » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (sbire ordinaire (degats indirects : chiffres)).

Carte terminée : OUI

### sk167 : White Tiger

- [x] Etape 2 : carte(s) de reference : `30037` (detail et justification en tete de `src/cards/pack/skrull_menace/new_revengers/sk167.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the VILLAIN »; « FACEDOWN boost card ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "SCH": "2", "ATK": "2", "Boost": "2", "Quickstrike": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk167 White Tiger : Quickstrike (natif) -> elle attaque des son engagement avec le heros (ATQ 2) » VERT; « sk167 White Tiger : vaincue -> le mechant recoit 1 carte de boost face cachee » VERT; « sk167 White Tiger, TEMOIN : un autre sbire vaincu ne donne aucune carte de boost au mechant » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (sbire ordinaire (carte de boost face cachee : le plateau compte deja les boosts du mechant)).

Carte terminée : OUI

### sk168 : The Revenge Time

- [x] Etape 2 : carte(s) de reference : `sk156` (detail et justification en tete de `src/cards/pack/skrull_menace/new_revengers/sk168.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « The VILLAIN gains the trait »; « for each REVENGER ENEMY IN PLAY ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "2*", "Acceleration": "1", "Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « sk168 The Revenge Time : le MECHANT gagne le trait REVENGER ; icone Acceleration » VERT; « sk168 The Revenge Time, TEMOIN : sans la carte le mechant n'est pas REVENGER » VERT; « sk168 The Revenge Time : revelee -> +1 menace par ennemi REVENGER en jeu (2 sbires + le mechant = 3 : 2 + 3) » VERT; « sk168 The Revenge Time : aucun sbire REVENGER -> seul le mechant compte (2 + 1) » VERT; « sk168 The Revenge Time dans un AUTRE scenario (Rhino) : le mechant Rhino devient REVENGER (menace 2 + 1) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (complot annexe ordinaire ; le trait donne au mechant n'est pas dessine).

Carte terminée : OUI

### sk169 : Forming the Revengers

- [x] Etape 2 : carte(s) de reference : `sk102`, `01116b` (detail et justification en tete de `src/cards/pack/skrull_menace/new_revengers/sk169.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « a card WITH THE REVENGER TRAIT ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk169 Forming the Revengers : defausse jusqu'a une carte REVENGER (un sbire) et la revele » VERT; « sk169 Forming the Revengers : « a card WITH the REVENGER trait » : l'ENVIRONNEMENT O.M.N.I.T.R.O.N.I.C.U.S. convient » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (traitrise : revele une carte du deck, chiffres seulement).

Carte terminée : OUI
