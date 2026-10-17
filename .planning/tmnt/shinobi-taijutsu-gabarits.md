# Gabarits PROCESSUS-CARTE : pack tmnt_shinobi_taijutsu (sh001-sh020), 17/10/2026

Cas : `tools/cas/tmnt_shinobi_taijutsu.py` (113 cas `[sh]`, tous verts avec le module). Preuve par substitution : module remplace par un stub vide, cas du filtre `[sh] shNNN ` relances (port 28500), restaure ensuite (script jetable). Les cas restes verts sans module sont des TEMOINS D'ABSENCE d'effet (assumes) ou des mesures de mecanique native (Uses, soutien). Autoplay : `deck_taijutsu.json` (Spider-Man + Path Shihan `se004` + les 20 cartes), 8 parties contre Rhino, temoin `spider_man` (8 parties) : 0 traceback (NameError/AttributeError/TypeError/KeyError/AssertionError : 0 sur 8 logs), toutes les cartes jouees dans les journaux, 0 % de victoire dans les deux decks (deck de 25 cartes sans soutien de ressources : sans lien avec les cartes). Plateau : `ui-app/src/board/tmnt-shinobi-taijutsu-plateau.test.ts` (18 tests, rouge vu sans l'entree `cudgel` de `compteurs-fr.ts`). Etape 8 bis : voir par carte. Classement contre les officielles : NOUVELLE pour les 20 (homonyme sh008 / nt004 confirme different sur scan).

### sh001 : Raising Block

- [x] Etape 2 : cartes de reference : prevent 3 : 05005 Wiggle Room + td003 (is_from_attack) ; Reponse « after you spend this card to pay for a DEFENSE event » : 42008 Avian Anatomy.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : any amount FROM AN ATTACK (is_from_attack), prevent 3 OF THAT, spend THIS card, a DEFENSE event, Hero Interrupt/Response (forme heros).
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 0, prevent 3, draw 1 : cards.json = script. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 7 cas `[sh] sh001` verts ; substitution rouge : 3/7 (les 4 temoins d'absence restent verts).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (pioche, prevention).

Carte terminee : OUI

### sh002 : Foot Sweep

- [x] Etape 2 : cartes de reference : 04049 Clear the Area (Hero Action thwart) ; tj004 (paid_this_res_effects) ; 54003 (ReturnToHand).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : EACH ATTACK event used to pay (liste), pas DEFENSE/THWART, retour depuis la defausse, Hero Action.
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 2, remove 3 : cards.json = script. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 4 cas `[sh] sh002` verts ; substitution rouge : 4/4.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (retour en main).

Carte terminee : OUI

### sh003 : Stiff Jab

- [x] Etape 2 : cartes de reference : tj004 (deal then if paid ATTACK) ; tl006 (you MAY = Decline) ; tx016 (daze).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : paid WITH AN ATTACK EVENT, you MAY daze, daze THAT enemy (meme ennemi, vivant).
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 1, 2 degats : cards.json = script. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 4 cas `[sh] sh003` verts ; substitution rouge : 4/4.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (carte Dazed sur Rhino : plateau, dazed).

Carte terminee : NON : attend la reponse de l'utilisateur (Q-T1 (credit « MC Custom Content By: Inkwire »)), voir `.planning/tmnt/shinobi-taijutsu-questions.md`.

### sh004 : Straight Cross

- [x] Etape 2 : cartes de reference : tj004 (meme structure, 3 -> 5, Stunned).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : paid with an ATTACK event, stun THAT enemy, apres les degats, pas de « may ».
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 3, 5 degats. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 2 cas `[sh] sh004` verts ; substitution rouge : 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (Stunned).

Carte terminee : OUI

### sh005 : Double Kick

- [x] Etape 2 : cartes de reference : 18004 Crosscounter (deux cibles SetTarget/SetTarget2) ; ma015 (double libelle) ; tj004.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : deux puces INDEPENDANTES, « A DEFENSE event » (pas each), Toss/Countercross satisfont les deux, 2 effets sans fleche.
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 2, 2 degats, 2 menaces, draw 1 + 1. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 6 cas `[sh] sh005` verts ; substitution rouge : 6/6.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (pioche).

Carte terminee : NON : attend la reponse de l'utilisateur (Q-T3 (evenement DEFENSE+THWART : deux puces ou une ?)), voir `.planning/tmnt/shinobi-taijutsu-questions.md`.

### sh006 : Flying Kick

- [x] Etape 2 : cartes de reference : tj004 (paid_this_res_effects) ; 05005 (DrawUp).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : FOR EACH THWART event used to pay (nombre, distincts), Toss compte 1, Flying Kick n'est pas THWART.
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 2, 4 degats. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 5 cas `[sh] sh006` verts ; substitution rouge : 5/5.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (pioche).

Carte terminee : OUI

### sh007 : Trading Blows

- [x] Etape 2 : cartes de reference : 08030 Counterattack (AfterUnitTookDamage + Attacker) ; ma015 (stun or confuse) ; tj004.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : After you TAKE damage (reel), from an ENEMY attack, THAT enemy, stun OR confuse (option impossible non offerte), libelle attack/defense.
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 1, 2 degats. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 7 cas `[sh] sh007` verts ; substitution rouge : 5/7 (2 temoins verts).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (Stunned/Confused).

Carte terminee : OUI

### sh008 : Drop In (homonyme de nt004)

- [x] Etape 2 : cartes de reference : 27032 Double Life (Action, ready identity) ; 54003 Black Widow (retour) ; tj004.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : Action nu (alter-ego aussi), ready your IDENTITY, you MAY return, ATTACK OR THWART event, YOUR discard ; homonyme nt004 verifie sur scan : autre carte, NOUVELLE.
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 1. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 7 cas `[sh] sh008` verts ; substitution rouge : 7/7.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (redressement, retour en main).

Carte terminee : OUI

### sh009 : Toss

- [x] Etape 2 : cartes de reference : td003 Bo Tobu (prevent+thwart en Interruption) ; td004 (attaquant) ; tj004.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : FROM AN ATTACK, prevent 3 OF THAT, THAT enemy = attaquant, daze seulement si paye par un evenement ATTACK ; Scheme2 exige de la menace (convention moteur).
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 1, prevent 3, remove 1. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 6 cas `[sh] sh009` verts ; substitution rouge : 3/6 (temoins verts).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (Dazed).

Carte terminee : OUI

### sh010 : Martial Skill

- [x] Etape 2 : cartes de reference : 28002 Ms. Marvel (After you play an event) ; ua033 Pete (Exhaust + Counter) ; 01057 (MaxPerUnit).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : Max 1 per player natif, Uses (2 chi) natif (ne pas coder la sortie), cout double (incliner ET 1 chi), Response nu (alter-ego), After YOU play an EVENT.
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 1, 2 chi, draw 1. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 6 cas `[sh] sh010` verts ; substitution rouge : 4/6 (entree en jeu native, soutien : verts).
- [x] Etape 7 bis : limite imprimee ? OUI (inclinaison) : temoin d'epuisement `sh010 ... SECOND evenement`.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (compteurs chi, couchee).

Carte terminee : OUI

### sh011 : Elbow Strike

- [x] Etape 2 : cartes de reference : 41015 Upside the Head (meme declencheur) ; tx016 (daze).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : your HERO, BASIC attack, DAMAGES (Tough = pas de Reponse), daze THAT enemy.
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 0. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 4 cas `[sh] sh011` verts ; substitution rouge : 1/4 (3 temoins verts).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (Dazed).

Carte terminee : OUI

### sh012 : * Mutant Fight Club

- [x] Etape 2 : cartes de reference : ma004 Santana Family, 27007 George Stacy (AttachedCardCanPlayLikeInHand) ; 35022 Weapon X (TakeDamage + Exhaust) ; 26013 Jocasta (cible defausse + PlaceCardHere).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : Alter-Ego Action, cout = incliner ET subir 1 degat, ATTACK OR DEFENSE event de VOTRE defausse, FACEDOWN, AUCUN plafond, play seulement (comme en main).
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 1. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 7 cas `[sh] sh012` verts ; substitution rouge : 4/7 (temoins d'absence verts).
- [x] Etape 7 bis : limite imprimee ? NON (aucune limite imprimee).
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (evenements attaches face cachee sous un soutien).

Carte terminee : OUI

### sh013 : Roll With It

- [x] Etape 2 : cartes de reference : 01082 Indomitable (After your hero defends, ready) ; 32018 Defensive Energy (When you spend this card to play) ; bt011 (MoveAllToDeck Top).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : deux capacites distinctes, After your hero DEFENDS, ready your HERO (propose seulement si incline), spend THIS card for an ATTACK event, DEFENSE event de YOUR discard, DESSUS du deck.
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 0. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 5 cas `[sh] sh013` verts ; substitution rouge : 2/5 (temoins verts).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (deck, redressement).

Carte terminee : OUI

### sh014 : * Minarai

- [x] Etape 2 : cartes de reference : ua004 Attack Training (Attach to ally, Max 1 TRAINING natif) ; tl009 Taicho + ud006 (AfterAllyTakeConsequentialDamage).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : ally YOU CONTROL, attached ally (pas un autre), TAKES (Tough = rien), vaincu = rien a piocher.
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 1, draw 1. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 5 cas `[sh] sh014` verts ; substitution rouge : 2/5 (temoins verts).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (amelioration portee par l'allie).

Carte terminee : OUI

### sh015 : Keep the Momentum

- [x] Etape 2 : cartes de reference : 42008 Avian Anatomy (AfterYouSpendThisCard to_pay_card) ; se004 Shihan (choix dans la defausse, EstShinobi).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : spend ON AN EVENT (tout evenement), 1 TAIJUTSU EVENT (type + classe), YOUR discard, Response nu, Max 2 per deck natif.
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : ressource wild, Max 2. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 7 cas `[sh] sh015` verts ; substitution rouge : 3/7 (temoins verts).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (retour en main).

Carte terminee : OUI

### sh016 : * Jo

- [x] Etape 2 : cartes de reference : ua033 Pete (After you deal damage, cout Counter) ; 61017 / aspects (PlaceCountersInternal) ; 18010 (AfterPlayerPlayedCard).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : Restricted natif, Uses (3 cudgel) natif, TAIJUTSU EVENT, aucun plafond de compteurs, remove 2 (cout), THAT enemy, sortie de jeu par Uses sans perdre l'effet, After YOU damage = Q-T4.
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 2, 3 cudgel, +1, -2. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 9 cas `[sh] sh016` verts ; substitution rouge : 4/9 (temoins verts, dont 3 natifs/absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (compteurs cudgel, 'bâton' en FR).

Carte terminee : NON : attend la reponse de l'utilisateur (Q-T4 (portee de « After you damage an enemy »)), voir `.planning/tmnt/shinobi-taijutsu-questions.md`.

### sh017 : * Odyn

- [x] Etape 2 : cartes de reference : 14001a / tg001a (AfterUnitUseBasicPower) ; ud006 (Tough) ; ar010 (Discard YourHandCards trait).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : After ODYN (lui seul), basic power (ATK ou THW), discard a DEFENSE CARD (trait, cout), give Odyn Tough ; Tough avant les degats consecutifs (le moteur) ; ATK 3** THW 1* PV 3.
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 3, PV 3, ATK 3**, THW 1*. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 5 cas `[sh] sh017` verts ; substitution rouge : 2/5 (temoins verts).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (carte Tough sur un allie).

Carte terminee : NON : attend la reponse de l'utilisateur (Q-T2 (citation « behnd »)), voir `.planning/tmnt/shinobi-taijutsu-questions.md`.

### sh018 : Countercross

- [x] Etape 2 : cartes de reference : 18004 Crosscounter (meme structure) ; td003 (is_from_attack) ; 05005 (DrawUp).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : FROM AN ATTACK, prevent 1 OF THAT, trois effets sans fleche, deux cibles libres.
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 1, prevent 1, 1 degat, 1 menace, draw 1. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 4 cas `[sh] sh018` verts ; substitution rouge : 2/4 (temoins verts).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.

Carte terminee : OUI

### sh019 : Sideswipe

- [x] Etape 2 : cartes de reference : 04049 Clear the Area ; ma015 (if_this_remove_last_threat) ; 54003 (retour).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : If THIS removes the LAST threat on THAT scheme (annexe videe quitte le jeu), an ATTACK CARD (trait, tout type), YOUR discard.
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 0, remove 1. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 6 cas `[sh] sh019` verts ; substitution rouge : 6/6.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.

Carte terminee : OUI

### sh020 : Tough Nut

- [x] Etape 2 : cartes de reference : 27037 Power Within (AfterUnitUseBasicPower hero) ; ud006 (Tough) ; tj004 (DEFENSE or THWART).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies : your HERO basic power (ATK/THW/DEF), give IT a Tough, soin = phrase SEPAREE (a lieu meme si deja Tough), DEFENSE OR THWART (pas ATTACK).
      Resultat : chaque mot du scan a sa contrepartie dans le script (en-tete du `.py`).
- [x] Etape 6 : nombres texte <-> code : cout 1, heal 2. Resultat : identiques dans `data/cards.json` (desc, texte) et le script ; icone de ressource verifiee par la couleur du coin (R fist, Y bolt, B nodes, G star) contre tj004 / tj003 / tj005.
- [x] Etape 7 : 7 cas `[sh] sh020` verts ; substitution rouge : 6/7 (temoin allie vert).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay 8 parties (deck Taijutsu + temoin spider_man), tracebacks : 0, la carte est jouee dans les journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (meme dessin que sh017).

Carte terminee : OUI

## Limites non prouvees

- Aucune partie reelle jouee par un humain dans le navigateur (aucun outil du projet ne la remplace) ; l'affichage de la table n'est prouve que par des etats poses a la main (`plateau-de-test.ts`).
- Les cartes a cible « a scheme » ne sont pas proposees sans menace nulle part (convention du moteur, comme 18004).
- Odyn : l'ordre « Reponse puis degats consecutifs » est celui du moteur ; non confronte a une decision de l'auteur.
