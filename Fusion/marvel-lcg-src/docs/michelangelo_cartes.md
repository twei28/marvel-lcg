# Pack Michelangelo (TMNT Heroes v3, Inkwire) : fiches PROCESSUS-CARTE.md, une par card_id

Préfixe `tm`, set 164. **17 card_id** (`tm001a` à `tm016`). Décisions de l'utilisateur :
`.planning/tmnt/decisions-phase-b.md`. Cas : `tools/cas/tmnt_michelangelo.py` (**92 cas**,
tous verts après fusion avec `sauvegarde-cle-usb-2026-10-14`).

## Preuves communes (16/10/2026)

- **Scans relus un par un** (17 cartes) : texte, coûts, PV, ATQ/CTR/DÉF, boosts, traits, ressources.
  Icônes de ressource **découpées et comparées** à des cartes officielles de ressource connue
  (01060 Y, 01061 B, 01074 R, 01062 G) : tm003 Y, tm004 Y, tm005 R, tm006 B, tm007 G, tm008 B, tm009 Y,
  tm010 R, tm011 Y, tm012 Y, conformes à `desc.RES`. Seul doute de lecture, non tranchable : le coût
  de tm009 est un cartouche **sans chiffre** (écrit `Cost 0`).
- **Substitution** (`tools/substituer_pack.py .game-src 42000 tm0`, module remplacé par un stub) :
  les 17 cartes ont au moins un cas rouge ; rouges/total : tm001a 11/14, tm001b 7/9, tm002 1/6,
  tm003 4/4, tm004 3/3, tm005 6/6, tm006 4/5, tm007 3/3, tm008 2/3, tm009 6/15, tm010 2/3,
  tm011 4/10, tm012 2/9, tm013 4/5, tm014 2/5, tm015 1/2, tm016 2/2. **Les cas qui restent verts sans
  module sont des témoins d'absence, des contrôles de BASE AUTOMATIQUE du moteur (Toughness,
  Retaliate, Restricted, Crisis, valeurs imprimées, conséquents) ou des vérifs du moteur lui-même
  (`MoveThreat`)** : assumés ici, pas maquillés. Détail tm002 : seul le cas Piercing dépend du module.
- **Mutations ciblées** (code modifié, cas vu ROUGE, code restauré) : tm006 `X = déclaré` rouge sur
  2 cas (Tough, Energy Barrier) ; tm001a sans `check_fn` de Crise rouge ; tm005 et tm006 sans
  `SetLabel` rouges (cas « héros Sonne »).
- **Deck** : `DECK_NOM=michelangelo verifier_tous_les_decks` : « identite tm001b, main 6, deck 8 ».
  `verifier_appels_modules michelangelo` : OK (non calibré par moi : confiance limitée).
- **Autoplay** : 8 parties `michelangelo` (rhino, normal, équilibre) en 59 s : 0 victoire, 4,9 rounds,
  **0 traceback** (grep exhaustif des 8 journaux). Témoin `spider_man` : 8 parties, 0 victoire,
  6,9 rounds. Le deck n'a que les 15 cartes signature (`player_deck` vide, consigne du 06/09) : le
  taux de victoire ne dit rien ; seule l'absence de plantage est mesurée. Journaux lus par grep, pas
  ligne à ligne.
- **Moteur partagé** : l'octroi `given_abilities` ne donnait RIEN (branche « Faceup seulement »,
  « Fix for 50070 »), donc les Nunchuck ne recevaient jamais l'aptitude. Corrigé par l'agent Leonardo
  (`abilities_en_continu`) ; ma version identique (`abilities_everywhere`) a été écartée à la fusion.
  Cas Nunchuck verts avec ce correctif.
- **Plateau (étape 8 bis)** : `ui-app/src/board/tmnt-michelangelo-plateau.test.ts` (22 cas verts).
  Sensibilité (16/10/2026) : `card-model.ts` `jetonMenace` renvoyant `undefined` + `zones.ts` sans
  attachement => 12 cas ROUGES, lignes restaurées. Couvre tm001b (Nunchuck inclinés, tm009 posée),
  tm001a/tm009 (jeton de menace), tm002/tm015 (carte Tough), tm005 (statut), tm013, tm011/tm012
  (Réponse octroyée : chaque Nunchuck est un porteur cliquable, l'incliné `indisponible`).
  **Rendu pixel et partie réelle : non faits** (les cas lisent le modèle de plateau, pas l'écran).
- **Cloak** : aucune carte Michelangelo ne l'emploie.

---

### tm001a : Michelangelo (Booyakasha)
- [x] Étape 2 : `ls001a`, `04032` (déclencheur), `34021` Storm (`MoveThreat`), `dt102` (nombre).
- [x] Étape 5 mots-pièges : « a basic power » (THW/ATQ/DÉF, pas REC), « from one scheme to another »,
      `5[per_hero]` testé sur la destination AVANT le déplacement, « up to 3 », Crise.
      Résultat : **corrigé** : Crise bloquait côté moteur (`MainScheme.RemoveThreatInternal`) mais le script
      proposait la principale ; `check_fn` ajouté. Annexe vidée = vaincue (moteur).
- [x] Étape 6 : THW 1 / ATQ 1 / DÉF 2 / PV 11 / main 5 : cas « valeurs imprimées » vert.
- [x] Étape 7 : ATQ, CTR, DÉF ; 1 sur 5 ; vaincue ; 5/1 joueur refusé, 4 accepté ; 9 accepté / 10 refusé à
      2 joueurs ; Crise active ET sans ; `MoveThreat` moteur avec le vrai effet Booyakasha (une `DebugRule`
      ignore la Crise d'office : piège noté). Rouge 11/14 sans module.
- [x] 7 bis : limite imprimée : NON.
- [x] 8 : voir preuves communes. [x] 8 bis : jeton de menace des deux manigances dessiné (`tmnt-michelangelo-plateau.test.ts`, rouge sans `jetonMenace`).
Carte terminée : **NON** (partie réelle non faite). Capacité et plateau prouvés.

### tm001b : Mikey (Setup, Action Nunchuck)
- [x] Étape 2 : `aa001b`, `jubilee/47001b` (Setup + fouille), `si001b`, `sf010` (coût), `40019`.
- [x] Étape 5 : « up to 2 », « deck AND discard pile », Setup. Résultat : **corrigé** : tm009 pouvait être dans
      la main de départ (6/15) ou en défausse (mulligan) et le Setup ne la posait alors pas ; recherche
      deck + défausse puis repli sur la main (cas rejoués par `Setup(False)`).
- [x] Étape 6 : REC 3 / PV 11 / main 6 vert.
- [x] Étape 7 : Setup en vraie partie, mulligan complet, tm009 en main, en défausse ; Action : 2 trouvés
      (deck + défausse, inclinés, coût payé), 1 trouvé, 0 trouvé, main vide refusée. Rouge 7/9.
      Mélange non mesuré (message du moteur par défaut de `Search`).
- [x] 7 bis : NON. [x] 8 bis : Nunchuck inclinés dessinés sur l'identité, tm009 posée au Setup avec 3 jetons (rouge sans attachement).
Carte terminée : **NON** (partie réelle non faite). Plateau prouvé.

### tm002 : Slash
- [x] Références : `50098` / `ho016` (Piercing), bases Toughness/Retaliate (fiches lues).
- [x] Étape 5-6 : ATQ 3 conséq. 2, CTR 0 conséq. 1, coût 3, PV 2 : `desc` conforme au scan.
- [x] Étape 7 : Toughness, Retaliate (Rhino subit 1), Piercing (Sandman Tough : Tough défaussé + 3 dégâts),
      conséquents (absorbés par Tough ; Slash vaincue sans Tough ; CTR 0 : 1 dégât). Rouge 1/6 (le reste = bases moteur).
- [x] 7 bis NON. [x] 8 bis : carte Tough dessinée sous Slash (rouge sans attachement).
Carte terminée : **NON** (partie réelle non faite). Plateau prouvé.

### tm003 : Call for Help
- [x] Réf. `ls005`, `20005`. Étape 5 : « ally OR the scheme » = UNE seule carte (cas deux disponibles).
- [x] Étape 7 : allié du deck, tm009 de la défausse, une seule carte, rien trouvé. Rouge 4/4.
- [x] 7 bis NON ; 8 bis NON (une carte en main). 8 : voir communs.
Carte terminée : **OUI**.

### tm004 : Impulsive
- [x] Réf. `mf013`, `20005`. Décision : jouable SANS WEAPON.
- [x] Étape 7 : avec arme (tm012 prête), sans arme, `CanPlayBy` vrai sans arme. Rouge 3/3.
- [x] 7 bis NON ; 8 bis NON.
Carte terminée : **OUI**.

### tm005 : Kaiten
- [x] Réf. `ls003`, `ls005`, `ra004`. Mots-pièges : « confuse OR stun » exclusives, « may » (Cancel offert).
- [x] Étape 7 : Sonne, Désoriente, Nunchuck incliné, aucun Nunchuck, refus (Cancel), libellé attaque (héros Sonne,
      mutation vue rouge). Rouge 6/6.
- [x] 7 bis NON ; 8 bis : statut Sonne/Désorienté standard.
Carte terminée : **OUI**.

### tm006 : Majime
- [x] Réf. `dt028`. **Corrigé** (décision) : X = dégâts RÉELLEMENT subis (PV perdus), plus le nombre déclaré.
- [x] Étape 7 : X=3, X=0, Tough (déclaré 3, subis 0 : aucun effet), 05017 Energy Barrier (déclaré 3, subis 2),
      libellé attaque/contre (héros Sonne). Mutation `X = déclaré` : 2 cas rouges. Rouge 4/5 (X=0 = absence).
- [x] 7 bis NON ; 8 bis NON.
Carte terminée : **OUI**.

### tm007 : Optimism
- [x] Réf. `12006`, `21058`. Étape 7 : soigne 1 + pioche 1, pleine santé (pioche quand même), en alter-ego
      (Réponse, pas Hero Response). Rouge 3/3. Icône wild vérifiée par découpe.
Carte terminée : **OUI**.

### tm008 : Mikey's Couch
- [x] Réf. `48003`, `ls007`. Étape 7 : +1 REC (alter-ego), Action (2 cartes de la défausse -> deck, incliné),
      Action refusée en forme héros. Rouge 2/3 (le témoin d'absence reste vert).
- [x] Pas de cas « +1 REC absent en forme héros » (la face héros n'a pas de REC mesurable).
Carte terminée : **OUI** (hors partie réelle, voir communs).

### tm009 : I'm Here to Help
- [x] Réf. `61007` (hors limite, **à l'entrée en jeu**), `50029`, `47003`.
- [x] Étape 5 : **deux défauts corrigés** : (1) le drapeau « hors limite » était posé au Setup seulement : jouée
      depuis la main elle était défaussée par la limite (cas rouge vu) ; (2) la condition « propriétaire » lisait
      `effect.GetInitiator()` (toujours le propriétaire), donc un AUTRE joueur qui la vainquait faisait piocher
      Michelangelo ; remplacée par `message.defeating_player`.
- [x] Étape 7 : hors limite (jouable), la limite mord sur les ordinaires, jouée de la main hors limite, Réponse
      forcée (-1), vaincue en forme héros (pioche 3), en alter-ego (rien), par un contre du héros (3), par un
      autre joueur (rien). Rouge 6/15 (témoins d'absence / vérifs de limite du moteur).
- [x] 7 bis NON. Coût imprimé : cartouche sans chiffre, écrit 0.
8 bis : jeton de menace et pioche de 3 cartes dessinés (`tmnt-michelangelo-plateau.test.ts`).
Carte terminée : **NON** (cartouche de coût vide non tranchable ; partie réelle).

### tm010 : Mikey's Skateboard
- [x] Réf. `01019a`, `bt001b`, `ls007`. Étape 7 : alter-ego -> héros, héros -> alter-ego, déjà incliné. Rouge 2/3.
Carte terminée : **OUI** (hors partie réelle).

### tm011 / tm012 : Nunchuck (octroi)
- [x] Réf. `50070` (octroi), `47004`, `ls004`, `62010`. Décision : vrai octroi à tous les NUNCHUCK.
- [x] Étape 5 : **le paramètre `given_abilities` ne donnait rien** (voir communs) ; corrigé dans le moteur.
- [x] Étape 7 : seul en jeu ; sans Nunchuck (témoin) ; l'autre seul ne reçoit pas la Réponse ; les deux en jeu
      = deux exemplaires indépendants (+2 ATQ, deux Interruptions de 1, deux dégâts à Rhino) ; l'un incliné ;
      disparition quand la donneuse part (dans les DEUX sens) ; ordre d'arrivée inversé ; alter-ego (Hero
      Response refusée) ; hors attaque (pas d'Interruption) ; Restricted (le plus ancien part au 3e).
      Risque de l'instance partagée (`is_initialized`) : **non observé**. Rouge tm011 4/10, tm012 2/9.
- [x] Ligne de base mesurée : l'attaque de Rhino vaut 4 dans ce montage (cas témoin).
8 bis : les deux Nunchuck dessinés et cliquables comme porteurs de la Réponse octroyée (`tmnt-michelangelo-plateau.test.ts`). Pas de ressource octroyée : l'octroi est une Réponse.
Cartes terminées : **NON** (partie réelle non faite). Plateau prouvé.

### tm013 : All Alone
- [x] Réf. `36030`, `sf010`. Étape 7 : révélation (alter-ego, allié et soutien inclinés), « cannot change
      forms », Action (coût identité + défausse -> retirée de la partie), coût impossible, 2 joueurs (allié de
      l'autre intact). Rouge 4/5.
Carte terminée : **OUI** (hors partie réelle).

### tm014 : Sewer Problems
- [x] Réf. `01149`, `01108`. Décision : Crise 1 (glyphe identique à 01108, vérifié par découpe).
- [x] Étape 7 : 3 cartes défaussées par joueur (1 et 2 joueurs), menace 4/8, Crise 1, Crise empêche de contrer la
      principale, Boost 3. Rouge 2/5 (Crise/Boost/menace = `desc`).
Carte terminée : **OUI** (hors partie réelle).

### tm015 : Wyrm
- [x] Réf. `ab016`, `50098`. Étape 7 : Toughness, vaincu -> deck Rencontre. Rouge 1/2 (Toughness = base).
Carte terminée : **OUI**.

### tm016 : Smash!
- [x] Réf. `ra027`. Étape 7 : 2 indirects sans allié ; avec allié (total 2). Rouge 2/2. Répartition
      choisie par le pilote (identité 2) : la répartition libre n'est pas explorée.
Carte terminée : **OUI**.

## Héros terminé ?

**NON.** Cartes toutes prouvées en capacité, mais : aucune partie complète jouée à la main, aucun cas plateau,
cartouche de coût de tm009 non tranchable, taux de victoire sans signification (deck de 15 cartes).
