# Gabarits PROCESSUS-CARTE : The Warriors Three (Phenexian et Mysteltainn, `wt`)

Pack `warriors_three` (set 230) : 28 `card_id`. **Aucune carte n'est « terminee »** : il manque une partie reelle jouee par un humain (voir en fin de fichier). Cas : `tools/cas/warriors_three.py` (`[wt]`), plateau : `ui-app/src/board/warriors-three-plateau.test.ts`.

Ordre des cartes = ordre du pack. Les cas verts cites sont ceux du dernier passage complet.

### wt001a : Fandral (face HEROS)

- [x] Etape 2 : carte(s) de reference : wt001a (modele Wasp hp001a, Hero Resource hz004). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : capacite : Hero Resource (inclinaison de l'identite). « Active hero » : CORRECTIF player_setup.py. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 5/5 verts ; substitution : rouges 1/3
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt001b : The Warriors Three (alter ego)

- [x] Etape 2 : carte(s) de reference : hp001b (Wasp), cn001a-e (Conan : 4+ faces). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : aucun texte code : conception du pack (soutiens toujours en jeu, choix du heros par « Change To »).  Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 2/2 verts ; substitution : AUCUN CODE (module vide, conception du pack : rien a retirer)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt001c : Hogun (face HEROS)

- [x] Etape 2 : carte(s) de reference : wt001a. Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : Hero Resource mental. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 2/2 verts ; substitution : rouges 1/2
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt001d : Volstagg (face HEROS)

- [x] Etape 2 : carte(s) de reference : wt001a. Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : Hero Resource physique. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 2/2 verts ; substitution : rouges 1/2
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt002 : The Warriors Three (carte-titre, amelioration Permanent/Setup)

- [x] Etape 2 : carte(s) de reference : nt003a (Setup + Permanent), hz004 (restricted supplementaire), hp (`changer_de_forme`). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : Hero Action changer de heros ; synchronisation des etats ; registre « sbire vaincu ce round » pour Revelry. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 6/6 verts ; substitution : rouges 5/6
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt003 : Fandral (heros inactif, soutien PERSONA)

- [x] Etape 2 : carte(s) de reference : hz004 (CanGenerateResources HeroResource). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : Hero Resource conditionnee a « Fandral n'est pas le heros actif ». Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 1/1 verts ; substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt004 : Hogun (heros inactif)

- [x] Etape 2 : carte(s) de reference : wt003. Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : idem, mental. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 1/1 verts ; substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt005 : Volstagg (heros inactif)

- [x] Etape 2 : carte(s) de reference : wt003. Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : idem, physique. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 1/1 verts ; substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt006 : Hildegarde

- [x] Etape 2 : carte(s) de reference : 06002 (AfterCardEnterPlay Response). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : +1 ATQ/+1 CTR jusqu'a la fin de la phase sur l'identite (suit les changements : ignore_flip) et les allies WARRIORS THREE. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 1/1 verts ; substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt007 : Brandrheid Undrsigr

- [x] Etape 2 : carte(s) de reference : 01028 (GiveKeywordToAttached par nom), nt004 (AfterUnitChangeForm). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : +1 ATQ et Riposte 1 pour Volstagg ; Hero Response soin 1. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 3/3 verts ; substitution : rouges 2/3
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt008 : Fimbuldraugr

- [x] Etape 2 : carte(s) de reference : 32002/21191 (UnitIgnoreKeywordIcons). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : +1 CTR pour Fandral, ignore la crise, retire 1 menace. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 2/2 verts ; substitution : rouges 2/2
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt009 : Hridgandr

- [x] Etape 2 : carte(s) de reference : 14029 (UnitAttackGainKeyword piercing). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : +1 ATQ/+1 CTR pour Hogun, attaques de base perçantes, 1 degat. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 2/2 verts ; substitution : rouges 2/2
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt010 : Hildegund and Kin

- [x] Etape 2 : carte(s) de reference : 01006 (HealthUnits), bg011 (cible « personnage ami »). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : soigne 2 degats d'un personnage ami apres le passage en alter ego. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 1/1 verts ; substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt011 : Mighty Endurance

- [x] Etape 2 : carte(s) de reference : beta_ray_bill `MarteauAPaye` (effect.context.paid_this_res_effects). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : « if you used Volstagg to pay ». Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 2/2 verts ; substitution : rouges 1/2
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt012 : Artful Bladework

- [x] Etape 2 : carte(s) de reference : 01021 (DealDamage d'un evenement d'attaque). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : 4 degats, +2 si paye avec Fandral. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 2/2 verts ; substitution : rouges 2/2
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt013 : Hold the Line

- [x] Etape 2 : carte(s) de reference : 47029 (WhenThreatWouldBePlacedOn HeroInterrupt, PreventThreat All). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : empeche la menace ; Hogun : sonne un ennemi. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 1/1 verts ; substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt014 : Rally!

- [x] Etape 2 : carte(s) de reference : 06002 (Faces.ReadyAll). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : redresse les soutiens PERSONA (celui du heros actif exclu). Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 1/1 verts ; substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt015 : Leap into Action!

- [x] Etape 2 : carte(s) de reference : wt002. Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : change de heros actif (choix trie par nom). Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 1/1 verts ; substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt016 : A Questing We Shall Go!

- [x] Etape 2 : carte(s) de reference : 27025 (WhenThisObligationGiveToYou), 01163 (GiveKeywordToAttached sbire). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : cherche le sbire le plus bas, le revele, s'y attache (+5 PV, Solide, ELITE). Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 1/1 verts ; substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt017 : Fenris

- [x] Etape 2 : carte(s) de reference : 01136/16080b (UnitCannotTakeDamage, UnitCannotBeDefeatedWhile). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : indefaisable et sans degats ; manigance -> menace sur Countdown. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 2/2 verts ; substitution : rouges 2/2
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt018 : Countdown to Ragnarok

- [x] Etape 2 : carte(s) de reference : 10027 (ThreatCannotBeRemovedFromWhile), sk145b (SetGameOver). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : menace posee seulement par Fenris ; 5 menaces = defaite. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 3/3 verts ; substitution : rouges 2/3
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt019 : Gleipnir

- [x] Etape 2 : carte(s) de reference : 16085a (DealPlayerEncounterCard), 32188 (Cost('3')). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : distribue une carte rencontre ; Hero Action defausse Fenris ; Boost : se revele. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 2/2 verts ; substitution : rouges 2/2
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt020 : Skadihr

- [x] Etape 2 : carte(s) de reference : 40024 (WhenUnitWouldBeDefeated SetBeInstead), ah014 (Faces.TreatAsAlly). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : vaincue -> soignee et devenue alliee WARRIORS THREE, 2 degats consecutifs. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 1/1 verts ; substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt021 : Fated Clash

- [x] Etape 2 : carte(s) de reference : 16057 / 28031 (Choose one). Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : incline deux soutiens PERSONA ou Fenris manigance ; sinon cherche Fenris. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 1/1 verts ; substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt022 : Revelry in Asgard

- [x] Etape 2 : carte(s) de reference : hz (TeamUp) / ub019. Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : +2 (ou +3) taille de main jusqu'a la fin du round. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [x] Etape 7 : cas test_capacites : 1/1 verts ; substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt023 : Genius (reskin)

- [x] Etape 2 : carte(s) de reference : hz016. Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : carte a part (decision Hellcat) : sans module. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [ ] Etape 7 : cas test_capacites : 0/0 verts ; substitution : sans module
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.
- [x] **26/10/2026, arbitrage reskins** (RR « A copy of a card is defined by title » + GUIDE §12 bis) : ces trois ressources ne changent que l'image de `01088` / `01089` / `01090` : ART ALTERNATIF des ressources doubles. Traitement, comme Gwenpool / Beast / Binary : collection `warriors_three` dans `COLLECTIONS` (`ui-app/src/board/variantes.ts`) ET dans `COLLECTIONS_RESSOURCES` (`public/js/prepare/app.js`, proposée par défaut au héros « The Warriors Three » : `collectionDuHeros`). Les cartes restent dans `cards.json` (précédent TMNT / Gwenpool).
      « Max 1 per deck » par TITRE : `validerDeck` (`public/js/deckbuilder/regles.js`, `cleCopie` = titre|sous-titre) compte déjà `01088` + le reskin comme un même titre ; **aucun correctif nécessaire**, preuve : `tools/tests-lanceur/regles-ressources-doubles-par-titre.test.mjs` (4 verts : chaque reskin du dépôt + son officielle = « Trop d’exemplaires de « Energy » : 2/1 », deux mêmes reskins idem, un seul légal, trois titres différents sans gêne). Le moteur n'applique pas MaxPerDeck (seul le constructeur le juge).
      Collection : `ui-app/src/board/resources-art-packs-fanmade-2026-10.test.ts` (45 verts : ordre Energy/Genius/Strength, wizard aligné, images présentes ; ROUGE vu avant le câblage : 18 échecs sur 27, puis rouge à nouveau en retirant l'entrée du wizard).
      Carte terminée : NON (provisoire) : partie réelle humaine (voir la collection « The Warriors Three » dans la modale du héros et les trois ressources à l'écran).

### wt024 : Energy (reskin)

- [x] Etape 2 : carte(s) de reference : hz016. Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : idem. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [ ] Etape 7 : cas test_capacites : 0/0 verts ; substitution : sans module
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

### wt025 : Strength (reskin)

- [x] Etape 2 : carte(s) de reference : hz016. Comparable : meme declencheur / meme genre d'effet.
- [x] Etape 5 : texte-contre-code : idem. Mots-pieges verifies : each / your / unless / paid with / instead selon la carte.
- [x] Etape 6 : nombres texte <-> code : valeurs de `data/cards.json` relues sur le scan.
- [ ] Etape 7 : cas test_capacites : 0/0 verts ; substitution : sans module
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir rapport du pack (8 parties du heros + 8 d'un temoin).
- [x] Etape 8 bis : voir `warriors-three-plateau.test.ts` (cartes dessinees).

Carte terminee : NON (provisoire) : manque une partie reelle jouee par un humain.

---

## Resultats d'ensemble (26/10/2026)

- **Cas** `tools/cas/warriors_three.py` : 46 sur 46 verts (`[wt]`), aucune exception avalee. **Substitution** : 24 cartes sur 25 a script tombent au ROUGE sans leur module (`wt001b` n'a pas de code : conception du pack) ; le pack est restaure a l'identique apres chaque passe.
- **Autoplay** : 8 parties de `warriors_three` (0 victoire contre Rhino, deck d'aspect fourni par l'auteur mais pilote prudent ; 7,5 rounds en moyenne), **0 exception** dans les 8 journaux apres correction ; temoin She-Hulk : 8 parties, 0 exception, 1 partie bloquee (sans lien avec le pack).
- **Decks** : `warriors_three` et `warriors_three_aggression` montent une partie (« identite wt001a, main 5, deck 35 ») ; passe complete `verifier_tous_les_decks` : **175 sur 175** decks montent une partie.
- **Statique** : `test_cards` 7 712 modules, 0 erreur ; `verifier_prefixes`, `verifier_cibles`, `verifier_traductions_fr` OK ; `verifier_appels_modules warriors_three` OK et CALIBRE (un appel `this.InventeeParWt` ajoute exprès est bien refuse) ; tests FR (`vocabulaire-statuts`, `vocabulaire-evenements`, `textes-fr-fanmade`) verts ; plateau : 5 cas (`warriors-three-plateau.test.ts`).
- **Modification du MOTEUR** (une seule, `# CORRECTIF`) : `src/game/player/element/player_setup.py` : une face HEROS qui imprime « Active hero. » ne propose pas le « Change To » libre vers une AUTRE face heros. Prouvee par 3 cas (`wt001a Change To`, contre-cas, `wt001b Change To`).

## Defauts corriges pendant le travail

- `wt016` : une OBLIGATION ne s'attache pas a un sbire (`GetBindFace` plante, 3 parties d'autoplay sur 8) : bonus poses directement sur le sbire.
- `wt019` : `GetInitiator()` leve une AssertionError quand le boost est retourne par le vilain (1 partie sur 8).
- `wt020` : meme AssertionError sur `GetInitiator()` et `GetFirstPlayer` inexistant dans `Worlds`.
- `wt022` : `set_name` vide, donc module non charge ; `.SetTarget("TeamUp")` oublie.
- Cas faux : la main de depart jouait Hold the Line au pilote (empeche les `SetThreat`) ; `ChangeForm` bascule autrement que prevu ; `Puzzle.SetThreat` sur Countdown est empeche par la regle du pack.

## Arbitrages du 26/10/2026 : corrections appliquees (RR v1.8 + notice de l'auteur, voir `VERDICTS-REGLES-2026-10-26.md`)

Cas dans `tools/cas/warriors_three.py` (`[wt]`) ; rouge vu AVANT le correctif, vert apres ; substitution : `tools/substituer_pack.py .game-src-wt 9000 wt` (empreinte des sources identique avant / apres) ;
passe complete `[wt]` : **59/59** ; `[co]` : **61/61**. Verificateur de deck (`DECK_NOM=warriors_three`) : OK « identite wt001a, main 5, deck 35 » (et `chod` : OK). Autoplay (`tools/autoplay.py .game-src-wt --deck warriors_three --vilains rhino --parties 8`) : 8 parties terminees, 0 victoire / 8 defaites (5 manigance accomplie, 3 heros elimines), 0 incident ; temoin `spider_man` : 0 / 8 egalement ; grep NameError / AttributeError / TypeError / KeyError / AssertionError / Traceback dans les 8 journaux : **0**. Les journaux n'ont PAS ete lus ligne a ligne et on n'a pas verifie que wt016 / wt022 / wt008 y sont apparues. ⚠ CORRECTIF MOTEUR PARTAGE : `obligation.py` (`AttachTo2`, `bind_face`, `GetBindFace`) et `card_type/card_status.py` (garde `Unit2`) : la passe complete des decks (`verifier_tous_les_decks.py`) et la batterie complete n'ont PAS ete relancees ; seuls les cas des obligations ip018 et sl046 (9/9 verts) ont ete rejoues.

### wt002 : The Warriors Three (Q1 etats par heros ; Q15 « ce tour »)

- [x] Etape 2 : carte(s) de reference : `warriors_three/__init__.py::synchroniser_formes` (existant) ; `Deck2.Remove/Insert` (`game/deck/deck.py`) pour deplacer une carte d'etat ; `WhenPlayerTurnBegin` (`factory/turn_phase.py`).
- [x] Etape 5 : texte-contre-code : notice face B « Status cards on your inactive heroes will remain on them » ; « status cards ... on The Warriors Three card ... treated as if they were on your active hero » ; mots-pieges : « this turn » (tour, pas round), « inactive », « remain ». Resultat : les etats propres a un heros partent sur son soutien quand il devient inactif et reviennent avec lui ; ceux de la carte-titre (`wt_base_etats`, presents quand le heros devient actif) restent sur l'identite.
- [x] Etape 6 : nombres texte <-> code : aucun nombre imprime touche. Un personnage a au plus 1 Sonne / Desoriente / Etourdi et `tough_max` Tough : le surplus apres fusion est defausse (`LoseState`).
- [x] Etape 7 : cas : `wt002 Etats (Q1)` x4 (Fandral Sonne -> Hogun : pas Sonne, `wt_stash` sur wt003 : **ROUGE avant** ; retour a Fandral : de nouveau Sonne ; etat de l'alter ego suit Volstagg ; Tough de Fandral -> alter ego : **ROUGE avant**) ; substitution wt002 : rouges 8/10 (les deux gardes de non-regression restent verts sans module, assume).
- [x] Etape 7 bis : limite imprimee ? NON (la Hero Action n'a pas de limite imprimee).
- [x] Etape 8 : autoplay ciblé : non rejoue (voir fin de rapport).
- [x] Etape 8 bis : la carte d'etat d'un heros inactif est DESSINEE sur son soutien : `ui-app/src/board/warriors-three-plateau.test.ts` (« la carte d'etat d'un heros inactif est dessinee sur son soutien PERSONA »), **vert d'emblee** : le rendu generique lit `bind_object_id`, aucun correctif de plateau (pas de ROUGE a montrer).

Carte terminee : NON (provisoire) : partie reelle jouee par un humain non faite (un etat qui change de carte a l'ecran apres un changement de heros).

### wt011 : Mighty Endurance (Q2)

- [x] Etape 2 : carte(s) de reference : `donner_etat_a_un_heros` (nouveau, `__init__.py`) ; `StatusComponent.GiveStatusCard` (`component/status.py`).
- [x] Etape 5 : texte-contre-code : « Otherwise, give Volstagg a tough status card » : actif = l'identite ; inactif = son soutien (la carte attend, notice). Resultat : conforme.
- [x] Etape 6 : nombres : aucun.
- [x] Etape 7 : cas `wt011 (Q2)` x2 : la Tough est sur le soutien de Volstagg inactif (**ROUGE avant**) puis sur lui quand il devient actif (**ROUGE avant**) ; substitution wt011 : rouges 3/4.
- [x] Etape 7 bis : NON. Etape 8 : voir fin de rapport. Etape 8 bis : meme cas plateau que wt002.

Carte terminee : NON (provisoire) : partie humaine non faite.

### wt008 : Fimbuldraugr (Q6)

- [x] Etape 2 : carte(s) de reference : `UnitIgnoreKeywordIcons` (`factory/play.py`, 21191 Fandral pour le principe) ; RR « Crisis Icon ».
- [x] Etape 5 : texte-contre-code : « while he is your ACTIVE hero ignore ALL crisis icons in play » : toute source (alliés, evenements, autres joueurs) tant que la carte est attachee a la face HEROS de Fandral (`fandral_est_actif`). Resultat : conforme.
- [x] Etape 6 : nombres : +1 THW inchange.
- [x] Etape 7 : cas `wt008 Fimbuldraugr (Q6)` x2 : Vision (allie) retire de la menace du complot malgre Defense Network (Crise) : **ROUGE avant le correctif** (menace 5 au lieu de 4, vu en remettant l'ancienne ligne), vert apres ; contre-cas Hogun actif : la Crise bloque (reste vert sans module, assume : absence d'effet). Substitution wt008 : rouges 3/4. NB : le premier montage utilisait `01107`, qui n'a PAS d'icone Crise (cas vert pour rien) : corrige en `01125`.
- [x] Etape 7 bis : NON. Etape 8 : voir fin de rapport. Etape 8 bis : NON.

Carte terminee : NON (provisoire) : partie humaine non faite ; multijoueur (source = un AUTRE joueur) non mesure par un cas.

### wt016 : A Questing We Shall Go! (Q9)

- [x] Etape 2 : carte(s) de reference : `bl016` Embraced (`GiveKeywordToAttached` + `Reveal(if_entered_play=...)`).
- [x] Etape 5 : texte-contre-code : « Reveal it, then attach this card to it » : `Reveal(..., if_entered_play=attacher)` puis `this.AttachTo2(sbire)` ; les trois bonus (+5 PV, steady, ELITE) par `GiveKeywordToAttached(Minion, health=5, steady=1, trait="ELITE")`. CORRECTIF MOTEUR `obligation.py` (`AttachTo2`, `bind_face`, `GetBindFace`) : voir RECETTES-MOTEUR §38 ter. Sans sbire : surge (inchange).
- [x] Etape 6 : nombres : 5 PV (8 = 3 + 5 au cas), steady 1 : conforme.
- [x] Etape 7 : cas : le cas existant mesure `hotes` [wt016, 01101] : **ROUGE avant** (la carte etait accrochee a l'identite), vert apres ; le sbire vaincu emporte la carte (hors jeu) ; contre-cas sans sbire. Substitution wt016 : rouges 2/3 (le contre-cas sans sbire reste vert sans module : absence d'effet).
- [x] Etape 7 bis : NON. Etape 8 : voir fin de rapport.
- [x] Etape 8 bis : la carte est DESSINEE sous le sbire (`warriors-three-plateau.test.ts`, « A Questing We Shall Go! est dessinee attachee au sbire »), **vert d'emblee** (rendu generique).

Carte terminee : NON (provisoire) : partie humaine non faite ; verifier a l'ecran que l'obligation s'affiche sous le sbire et disparait avec lui. Les obligations officielles 46024 / 49027 (`this.GetBindFace()` sur l'identite) ne sont pas rejouees ici : a verifier si la batterie complete passe.

### wt022 : Revelry in Asgard (Q15)

- [x] Etape 2 : carte(s) de reference : `WhenPlayerTurnBegin` ; `Puzzle.EndPlayerTurn / BeginPlayerTurn`.
- [x] Etape 5 : texte-contre-code : « If a minion was defeated THIS TURN » : indicateur de tour (`world.stat.wt_sbire_vaincu_ce_tour`) pose par wt002, remis a faux au debut de chaque tour. Resultat : conforme.
- [x] Etape 6 : nombres : +2 / +3 de taille de main : conforme.
- [x] Etape 7 : cas `wt022 (Q15)` x2 : +3 apres un sbire vaincu ce tour (vert avant et apres) ; contre-cas sbire vaincu au tour PRECEDENT du meme round : **ROUGE avant** (8 au lieu de 7), vert apres. Substitution wt022 : rouges 3/3.
- [x] Etape 7 bis : NON. Etape 8 : voir fin de rapport. Etape 8 bis : NON.

Carte terminee : NON (provisoire) : partie humaine non faite ; le tour d'un AUTRE joueur (multijoueur) n'est pas rejoue par un cas : seul le remplacement tour-par-tour est mesure.

### wt014 Rally! et wt021 Fated Clash (Q3) : verifies, aucun correctif

Les deux utilisaient deja `soutiens_persona` (le soutien du heros actif n'est pas un soutien). Cas ajoute : `wt021 Fated Clash (Q3)` (Fandral actif : wt004 et wt005 s'inclinent, wt003 reste pret), vert d'emblee. ECART restant : un effet GENERIQUE « un soutien » d'une autre extension voit encore le soutien du heros actif (la carte reste en jeu).

## Questions en attente (option A = celle codee)

1. **[TRANCHE le 26/10/2026 : B, notice de l'auteur ; voir « Arbitrages du 26/10/2026 »]** **Etats (cartes d'etat) par heros** : A les cartes d'etat (stun, confused, tough) restent sur l'IDENTITE, partagees par les trois heros ; B chaque heros garde les siennes (FAQ : « status cards on your inactive heroes remain on them »). Le moteur n'a pas de cartes d'etat sur un soutien.
2. **[TRANCHE le 26/10/2026 : ni A ni B, la carte attend sur le soutien de Volstagg]** **wt011 Mighty Endurance, « Otherwise, give Volstagg a tough status card »** quand Volstagg est INACTIF : A le soutien ne peut pas porter de carte d'etat (effet perdu) ; B poser la carte sur l'identite.
3. **[VERIFIE le 26/10/2026 : Rally! et Fated Clash excluaient deja le soutien du heros actif ; cas ajoute, vert ; ecart generique note plus bas]** **Soutiens des heros** : A les trois soutiens PERSONA restent TOUJOURS en jeu, celui du heros actif est seulement inutilisable ; B celui du heros actif quitte le jeu (mis de cote) et revient quand il redevient inactif (plus fidele : les effets qui ciblent « un soutien » ne le voient pas).
4. **Etat de la carte-titre** : A la carte-titre (amelioration) et l'alter ego echangent leur etat pret/epuise a chaque passage (une carte physique qui se retourne) ; B les deux etats sont independants.
5. **wt006 Hildegarde** : A +1 ATQ/+1 CTR sur l'identite (suit les changements de heros) et sur chaque allie WARRIORS THREE ; B aussi sur chaque heros inactif separement (equivalent a l'ecran).
6. **[TRANCHE le 26/10/2026 : ni A ni B, toutes les sources]** **wt008 Fimbuldraugr** : A « ignore all crisis icons in play » = l'icone de crise est ignoree pour les contres de Fandral actif ; B pour toute action de Fandral.
7. **wt013 Hold the Line** : A empeche TOUTE la menace de l'evenement ; B seulement 1 (le texte dit « that threat » : A).
8. **wt014 Rally!** : A redresse les soutiens PERSONA, sauf celui du heros actif ; B tous, y compris celui du heros actif.
9. **[TRANCHE le 26/10/2026 : B, correctif moteur Obligation fait]** **wt016 A Questing We Shall Go!** : A bonus poses directement sur le sbire, la carte n'est pas attachee (limite moteur) ; B conserver l'attachement (necessite un correctif moteur sur `Obligation.GetBindFace`). « bottommost » = derniere carte du deck rencontre (A) ; sans sbire : surge.
10. **wt017 Fenris** : A PV 1 (le scan imprime « - ») et « can not take damage or be defeated » ; B autre valeur de PV.
11. **wt018 Countdown to Ragnarok** : A toute menace non posee par Fenris est empechee (y compris la regle de debogage) ; la carte est Permanent.
12. **wt019 Gleipnir** : A l'obligation distribue la carte rencontre face cachee quand elle est donnee, et RESTE en jeu avec son Hero Action ; B revelation « When Revealed ». Boost etoile : revelee au premier joueur.
13. **wt020 Skadihr** : A le joueur qui la vainc la reprend ; ATQ imprime (2) conserve en allie ; 2 degats consecutifs au contre et a l'attaque ; B ATQ 0.
14. **wt021 Fated Clash** : A les deux soutiens PERSONA a incliner incluent Hildegund and Kin ; sans option possible, cherche Fenris dans le deck et la defausse.
15. **[TRANCHE le 26/10/2026 : B, indicateur de TOUR]** **wt022 Revelry in Asgard** : A « ce tour » = ce round (registre de round ; ecart en multijoueur) ; Team-Up « Odinson » reconnait l'allie Odinson (`ra002`) et l'alter ego Odinson de Thor.
16. **wt023-wt025** : A cartes a part (decision Hellcat) ; B arts alternatifs des ressources officielles.
17. **Decklists imprimees** (precons Justice et Agression) : A noms ambigus resolus ainsi : Mutitasking = 15013 Multitasking (coquille de l'auteur) ; « Avenges Mansion » = 01091 ; Bootcamp = 13016 Boot Camp ; Mutitalented = 47021 Multitalented ; Lay Down the Law 12031 (ou 61018) ; Concussive Blow 05031 (ou 41014) ; Wolfsbane 40051 (ou 32092, Encounter) ; deux Thor = 13011 et 25013 ; B autres numeros.
18. **wt007 Brandrheid Undrsigr** : nom lu sur le scan (le fichier dit « Branderheid ») : A « Brandrheid ».
19. **Icones de ressource** des cartes (energie / mental / physique) lues a l'oeil sur le scan et comparees a des cartes officielles de meme glyphe, sans decoupe pixel par pixel.

## A verifier en partie reelle

- Une partie complete avec « The Warriors Three » choisi dans la liste Fan-made (decks Justice ET Agression, variante repliee sous la base).
- Les options « Change To » a l'ecran : depuis un heros, seulement l'alter ego ; depuis l'alter ego, les trois heros ; le choix du heros par la carte-titre et Leap into Action (liste triee).
- Le plateau : la carte-titre sur le heros actif, les trois soutiens PERSONA (celui du heros actif est a ignorer) et leurs etats incline/pret apres un changement de heros (non vu dans un navigateur).
- Plusieurs activations de heros dans un meme tour (Fandral attaque, changement, Hogun attaque).
- Les ressources de heros des soutiens (inactifs) pendant le paiement d'un evenement.
- Fenris / Countdown / Gleipnir / Skadihr dans une vraie partie (Fenris a PV « - » ; Skadihr alliee ; Gleipnir en jeu).
- La biographie au survol du heros dans l'assistant ; les 25 images a l'ecran (Countdown en paysage) ; le texte francais des cartes.
- Le Hero Response des armes « After <heros> becomes the active hero » en partie reelle (cas ChangeForm / titre seulement).


## wt020 Skadihr : mot-clé Quickstrike (26/10/2026, fin de batterie)

`tools/verifier_coherence_cartes.py` relevait « Quickstrike imprimé, clé `desc.Quickstrike` absente » : le moteur lit ce mot-clé directement dans `desc` (fiche `docs/reference/mots-cles/quickstrike.md`, modèle `01167`), donc **le mot-clé ne fonctionnait pas en jeu**. Corrigé : `"Quickstrike": "1"` ajouté dans `data/cards.json` (diff de 24 octets, JSON valide).
- Contrôle du pack : compare le texte imprimé de chaque carte wt avec sa `desc` (Quickstrike, Toughness, Guard, Retaliate, Surge, Overkill, Villainous, Piercing, Ranged, Stalwart, Steady, Permanent, Patrol, Hinder, Incite, Armored, Assault, Restricted, Uses, Tuck, Victory, Peril, Temporary, Ambush, Infiltrate…) : seule wt020 était en défaut (wt022 porte `TeamUp`, écrit autrement, conforme).
- Cas ajoutés à `tools/cas/warriors_three.py` : `[wt] wt020 « Quickstrike »` (forme héros, mise en jeu sous contrôle = engagée : ATQ 2 − DEF 1 de Fandral = 1 dégât à l'identité) et son témoin en ALTER EGO (0 dégât : Quickstrike ne vise qu'un héros). **Rouge sans la clé** (0 dégât au lieu de 1), **vert avec** ; substitution refaite le 26/10/2026 (clé retirée → rouge ; remise → vert, `cards.json` identique octet pour octet).
- Pack complet `[wt]` : 61/61 verts (PARALLELES=4). Autoplay `warriors_three` contre Rhino : 8 parties, 0 victoire / 8 défaites, 0 erreur dans les 8 journaux, 0 bloquée.
- Limite : la défense de Fandral est choisie par le pilote du harnais (le cas mesure 1 dégât, pas 2) ; l'attaque Quickstrike à l'engagement d'un sbire par un VRAI joueur n'est pas vue en partie réelle. Carte terminée : NON (provisoire) comme tout le pack.
