# Aspects TMNT : socle commun et gabarits PROCESSUS-CARTE des trois cartes faites par le socle

16/10/2026. Socle posé AVANT le portage des 235 scans par cinq agents (un par aspect).

- Préfixes / packs / sets : `ua` tmnt_aspect_aggression (196), `ub` tmnt_aspect_basic (197),
  `uj` tmnt_aspect_justice (198), `ul` tmnt_aspect_leadership (199), `up` tmnt_aspect_protection (200),
  `ud` tmnt_aspect_dual (201). `max_id` = nombre de scans du dossier : NE PAS le modifier.
- Numérotation FIGÉE : `Fusion/marvel-lcg-src/tools/tmnt_aspects_numerotation.tsv`.
- Images : `Fusion/marvel-lcg-src/tools/importer_images_tmnt_aspects.py`.
- Recette reskin + Rampage : `docs/reference/RECETTES-MOTEUR.md` §11 ; fiche `mots-cles/rampage.md`.
- Cas : `Fusion/marvel-lcg-src/tools/cas/rampage.py`.

Les trois cartes ci-dessous sont FAITES (pack Aggression) : l'agent Aggression ne les refait pas.

### ua015 : Demolish

- [x] Étape 2 : cartes de référence : `nt006` Melon Grab (8 dégâts, piercing+overkill sous condition,
      événement d'attaque) ; `36007` / `27011` (soutien à trait contrôlé, `CardFinder2(trait, Support)`) ;
      `tr011` / `90107` (« take N damage » en coût). Rampage : coût neuf `CostFunc.Rampage`, fiche créée
      AVANT le code.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « As an additional cost » (coût, pas effet :
      un coût impayé annule tout), « take 3 damage » (identité), « YOUR deck », « an enemy » (vilain ou
      sbire), « you control a NYC SUPPORT » (soutien seulement, contrôlé par le joueur), « overkill AND
      piercing » (les deux), ★ = rappel sans effet.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût 3 (`desc.Cost "3*"`), Rampage 3 (`CostFunc.Rampage(3)`),
      8 dégâts (`DealDamage(..., 8)`), ressource [physical] (`RES R`, icône poing comparée à `ua009`
      Clobber = `18012` RES R, même pack).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution :
      capacité 1 (Rampage 3) : cas `[rampage] ua015 ... Rampage 3 paye`, `... deck de 2 cartes`,
      `... deck VIDE`, `... identite Tenace` ; rouges tous les quatre sans `SetCostFunc(CostFunc.Rampage(3))`
      (+ les deux cas NYC, qui mesurent aussi les 3 dégâts) : 0/6, verts avec : 6/6.
      capacité 2 (Hero Action, branche NYC) : cas `... soutien NYC controle -> percant ET deferlement`
      rouge quand la condition est forcée à faux ; contre-cas `... SANS soutien NYC` rouge quand elle est
      forcée à vrai ; verts avec le module.
      Résultat : 6/6 verts.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : 8 parties contre Rhino, profil équilibré, deck She-Hulk modifié (3
      Demolish, 2 Clobber, 1 Bo-Wing : `scratchpad/deck-she-hulk-tmnt.json`), témoin She-Hulk de départ
      dans la même configuration. Blocages : 1/8 et témoin 1/8 (même message de pilote sur l'Alter-Ego
      Action). Grep tracebacks (NameError, AttributeError, TypeError, KeyError, AssertionError,
      Traceback) : 0 sur les 16 journaux. Lecture du journal : Demolish JOUÉE dans 2 parties (journaux 6
      et 7) : 3 dégâts à She-Hulk, 3 cartes du dessus défaussées, puis 8 dégâts à Rhino ; ailleurs elle
      sert de ressource.
      Résultat : conforme.
- [x] Étape 8 bis : change ce qu'on VOIT ? NON : dégâts et défausse du dessus du deck vers la défausse,
      deux jauges et une pile déjà dessinées.
      Résultat : sans objet.

Carte terminée : OUI. Reste « en partie réelle » : le plateau n'annonce pas le coût Rampage avant le
paiement (rien dans le cartouche ne dit « vous allez subir 3 dégâts ») ; non mesuré, aucun outil ne le voit.

### ua009 : Clobber (reskin IDENTIQUE de 18012)

> **Converti en art alternatif de 18012 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ua009` n'existe plus dans `cards.json` (image `18012_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `18012` est conservé. Ce qui suit est l'historique.

- [x] Étape 2 : carte de référence : `18012` Clobber, branchée par `ability_link` (recette RECETTES §11) ;
      précédent joueur `45018` → `01070`.
- [x] Étape 5 : texte du scan relu mot à mot contre 18012 : identique (« first card you have played this
      round », « return this card to your hand »). Module 18012 relu : aucun nom ni card_id en dur.
      Résultat : conforme.
- [x] Étape 6 : coût 2, RES R (poing), 3 dégâts : identiques à 18012.
      Résultat : conforme.
- [x] Étape 7 : `[reskin] ua009 ... retour en main`, `... rejouee ... defausse (6 degats)` + TÉMOIN
      `18012` même montage ; sans `ability_link` : les 2 cas ua009 ROUGES (0 dégât), témoin vert.
      Résultat : 3/3 verts.
- [x] Étape 7 bis : limite imprimée ? NON (le « first card this round » n'est pas une limite).
- [x] Étape 8 : même fournée que ua015 : jouée dans 2 parties (journaux 6 et 8), 3 dégâts à Rhino ;
      0 traceback.
- [x] Étape 8 bis : NON.

Carte terminée : OUI, SAUF le deck-builder : homonyme de 18012, elle n'y a PAS de tuile (question Q-R2).

### ua006 : Bo-Wing (reskin IDENTIQUE de 53035 Winter Soldier)

- [x] Étape 2 : `53035` Winter Soldier par `ability_link`.
- [x] Étape 5 : texte du scan = texte de 53035 au nom près (« After Bo-Wing attacks and defeats an
      enemy, remove 2 threat from a scheme »). Module 53035 relu : `"This"`, aucun nom en dur. Traits du
      scan : NINJA. TURTLE. VIGILANTE. (ceux de 53035 : S.H.I.E.L.D, SOLDIER, NON repris). ⚠ Le scan
      imprime sous le titre un bandeau « ✦ WINTER SOLDIER » : question Q-R1.
      Résultat : conforme à la recette ; Q-R1 ouverte.
- [x] Étape 6 : coût 3, PV 3, ATK 2 (1 dégât consécutif) « 2* », THW 1 (1 dégât consécutif) « 1* »,
      RES B (icône « nœuds reliés » = mental, comme 53035), 2 menaces.
      Résultat : conforme.
- [x] Étape 7 : `[reskin] ua006 ... la Reponse de 53035 part sur Bo-Wing` (menace 5 → 3) + TÉMOIN 53035 ;
      sans `ability_link` : ROUGE (menace reste 5), témoin vert. Données : traits propres, unicité par
      son titre (coexiste avec 53035 ; un 2e Bo-Wing n'est pas jouable, témoin jouable) : verts avec et
      sans `ability_link` (ce sont des données, attendu).
      Résultat : 6/6 verts.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : même fournée : mis en jeu dans 4 parties (journaux 2, 6, 7, 8) ; sa Réponse n'a pas
      eu l'occasion de partir (aucun sbire tué par Bo-Wing) ; 0 traceback.
- [x] Étape 8 bis : NON (allié standard).

Carte terminée : OUI, sous réserve de Q-R1 (bandeau Winter Soldier).
