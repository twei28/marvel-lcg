# Predator (RyCoRan) : gabarits PROCESSUS-CARTE, 31 card_id

Pack `predator`, préfixe `pd`, set 214. Source : zip « Predator (5-25 Final) » déposé le 24/10/2026. Trois sets : `Predator` (pd001a-pd015,
pd021-pd025), `Predator Nemesis` (pd016-pd020), `Predator Alt Nemesis` (pd026-pd030, set némésis alternatif de l'auteur). Cas :
`Fusion/marvel-lcg-src/tools/cas/predator.py`, `predator_b.py`, `predator_c.py`, `predator_d.py` (filtre `[pd]`). Plateau :
`ui-app/src/board/predator-plateau.test.ts`. Recettes : `docs/reference/RECETTES-MOTEUR.md` §23. Questions à l'auteur : `QUESTIONS-AUTEUR.md`.

## Arbitrages utilisateur du 25/10/2026 (questions posées une à une, scan à l'appui)

1. **Savage Skewer (`pd007`)** : « discard a cloaked status card » = la carte Cloaked de **Predator seulement** (pas celle d'un ennemi ni d'un allié).
2. **Bio-Helmet (`pd014`)** : « for each icon, remove 1 threat from a scheme » = **une manigance au choix PAR icône** (répartition libre).
3. **Self Destruct (`pd011`)** : « (to a maximum of 10) » : l'utilisateur pose la question à l'auteur ; **provisoire** = plafond de 10 glyphes comptés, soit 10 dégâts au plus par cible.
4. **Hunted By the Hive (`pd019`)** : l'utilisateur pose la question à l'auteur ; **provisoire** = la Reine qui vient d'être trouvée attaque aussi.

## Décisions prises seules (règle de la Rules Reference ou texte sans ambiguïté), à signaler

- **Infralocked n'a pas d'état « libre »** : « return this card to your play area » = revenir sur l'**identité** du joueur (le moteur n'a pas d'amélioration libre).
  Si son sbire disparaît par une autre cause que Predator, la carte (Permanent) revient aussi sur l'identité (règle `NonKeyword` du script).
- **Find** (`pd008`, `pd009`, `pd019`, `pd020`, `pd029`) : règle « Find » du moteur, toutes les zones. Conséquence : le **Xenomorph de joueur** (`pd003`, un sbire) peut être trouvé par Jungle Stalk.
- **Xenomorph's Prey n'est PAS en jeu au départ** : tout le set némésis est mis de côté (comportement du moteur pour tous les héros).
- **Acid Blood / M134 Minigun** : l'icône imprimée « +1 ATQ » est écrite dans le texte (« gets +1 ATK »).
- **Decklist de l'auteur** : l'image « Predator starter deck » cite « 2 Targeted! » et « 15 Infralocked x3 » qui n'existent pas dans le zip (une seule Infralocked, 1/16, aucune « Targeted! ») ; les scans font foi.
  Les 22 cartes d'aspect (Aggression) et les 3 ressources + Razor Hunt sont recopiées dans `player_deck`.
- **Set némésis alternatif** : second deck de départ `predator_dutch` (`metadata.variante_de`).

## Points d'identification des cartes (pas des arbitrages)

- Ghost Protocol (3/16 et 4/16), Spine Rip (5/16 et 6/16), Savage Skewer (8/16 et 9/16) : impressions IDENTIQUES : un seul card_id chacune, deux exemplaires au deck.
- « Infrared Web » (`pd025`) est le fichier « Pred - Spidey Aspect - Event » ; « Razor Hunt » (`pd024`) le fichier « Predator-Wolverine TeamUp ».
- L'icône « Y » rouge du coin des cartes de rencontre est l'icône de BOOST ordinaire ; l'icône ronde à étoile est l'icône de boost à étoile. L'icône de la manigance annexe (boîte à croix) est **Hazard** (comparée à 01107 Breakin' & Takin').
- Icônes de ressource vérifiées contre les trois ressources du MÊME pack (Energy = éclair, Genius = nœuds, Strength = poing).
- Homonymes de NOM au dépôt : « Energy », « Genius », « Strength » (nombreuses versions) (aucun module ne cherche par nom : tout passe par card_id).

## Gates du héros

- [x] Étapes 1 à 8 de PROCESSUS-HEROS : cartes (`cards.json`, 31 card_id), scripts (3 sets), deck de départ (`deck/starter/predator.json` : 15 cartes de héros,
      `set_aside` = Infralocked, decklist d'aspect de l'auteur recopiée ; variante `predator_dutch.json` pour le set némésis alternatif), `sets_info.json`,
      images (`assets/pics/pd*.jpg`, non versionnées), biographie (`heros-info.js`, clé `pd001a`), textes FR (`textes-fr-fanmade.ts` + généré), compteurs FR (`skull`, `glyph`).
- [x] Étape 10 (aucune signature d'un autre héros) : les 15 cartes de `hero_deck` sont de classe `Hero`, set `Predator`.
- [x] `tools/verifier_tous_les_decks.py` : **157/157 decks montent une partie** (dont `predator` et `predator_dutch` : « identite pd001a, main 6, deck 35 »).
      Cette gate a attrapé DEUX défauts invisibles au harnais : le trait `XENOMORPH` absent de `CardFace.TRAITS` (assert `IsTrait` sur `desc.Teamwork`) et
      `AttachToFaceWhenPutIntoPlay` sur une AMÉLIORATION (assert `CastTo(Attachment)`, masqué par `RELEASE=1`).
- [x] `tools/test_cards.py` : 7375 modules OK, 0 erreur ; `verifier_prefixes.py`, `verifier_noms_modules.py`, `verifier_appels_modules.py`, `verifier_cibles.py`,
      `verifier_traductions_fr.py`, `verifier_desc_mots_cles.py predator` OK.
- [x] `tools/audit_cartes.py` : deux signalements, assumés. `pd003` « Interrupt » : écrit DANS le When Defeated (une vraie Interruption sortait la carte avant la
      défaite et muselait « Ready Predator », constaté au harnais ; `al002` Throg fait de même). `pd010` « exhaust sans coût » : l'inclinaison est payée dans
      un `CostFunc.Custom` (une seule inclinaison pour X compteurs retirés).
- [x] Cas : **108 cas `[pd]` verts sur 108** ; preuve par substitution : **27/28 modules** avec au moins un cas rouge sans eux, le 28e étant `pd009` dont le script est
      VIDE par construction (sa capacité « en vitrine » vit sur `pd001a`/`pd001b` : cas rouges mesurés en remplaçant `pd001a`). Les cas qui restent verts sans module sont des
      contre-cas d'absence d'effet, des valeurs imprimées ou des mots-clés natifs du moteur.
- [x] Plateau : `ui-app/src/board/predator-plateau.test.ts` 9/9 (calibré ROUGE en mutant deux assertions) ; `compteurs-fr.test.ts` et `textes-fr-fanmade.test.ts` verts.
- [x] Moteur / harnais touchés : `CardFace.COUNTER` (+`skull`, `glyph`), `CardFace.TRAITS` (+`XENOMORPH`, `YAUTJA`), `test_capacites.py` (`payer_avec` accepte un id
      répété pour une ressource à usages multiples). Batterie complète NON relancée (les trois changements sont additifs) : à faire au prochain gros regroupement.
- [ ] **Partie complète jouée par un humain** avec Predator (puis avec la variante Dutch) : NON FAIT, aucun outil du projet ne remplace le navigateur. À vérifier en jeu :
      la remise d'Infralocked sur l'identité, le paiement par Yautja Trophy Room (X usages), l'Action de Honor Hunt en vitrine pour un 2e joueur,
      l'affichage au survol de la biographie dans le wizard.
- [ ] **Questions en attente de l'auteur** : `QUESTIONS-AUTEUR.md` (Self Destruct, Hunted By the Hive, decklist, Razor Hunt, Infralocked, Find).

### pd001a : Predator (Hero)

```
* Predator (face HEROS) — SOLDIER. YAUTJA. PV 13, THW 0, ATK 3, DEF 2, main 5.
Response: After a minion enters play, attach Infralocked to it.
Camouflaged Hunter — Response: After you defeat a minion, give Predator a cloaked status card.

Cartes de reference :
 - `ar007` God of War (pack ares) : `AfterCardEnterPlay(.., Minion, op)` pour « after a minion enters play » et
   `AttachTo2(sbire, effect)`, seule voie pour DEPLACER une amelioration deja en jeu vers un autre hote ;
   `yd012` Yaka Arrow (pack yondu) : amelioration unique qui change d'hote (ennemi / identite).
 - `an001a` / `vp001a` : `AfterUnitDefeatedUnit(type, "You", Minion, op)` pour « after you defeat a minion ».
 - `ShinobiCloak` (cards/pack/__init__.py) : « give X a cloaked status card » (fiche mots-cles/cloaked.md).

⚠ Mots-pieges :
 - « Response » nu sur la face HEROS : optionnel (le moteur propose), muet en alter-ego.
 - « After A minion enters play » : n'importe quel sbire, de n'importe quel joueur, quel que soit le chemin (revelation,
   boost, Xenomorph joue par le joueur) ; Infralocked change alors d'hote (la carte n'a qu'UN exemplaire).
 - « After YOU defeat a minion » : un sbire vaincu par Predator lui-meme (jamais par un allie) ; Minion, pas Enemy.
 - « give PREDATOR a cloaked status card » : le HEROS ; une seule carte Cloaked par personnage, et Xenomorph's Prey
   (pd016) l'interdit tant qu'il est en jeu.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - pd001a Response : apres l'entree d'un sbire, Infralocked s'attache a lui
      - pd001a Response : un SECOND sbire reprend Infralocked (une seule carte, elle change d'hote)
      - pd001a Camouflaged Hunter : apres avoir vaincu un sbire, Predator recoit une carte Cloaked
      - pd001a Camouflaged Hunter : le sbire SURVIT (3 PV, ATK 3 = mort) -> choisir un sbire a 4 PV : pas de Cloaked
      - pd001a Predator : valeurs imprimees PV 13, THW 0, ATK 3, DEF 2, SOLDIER YAUTJA
      Preuve par substitution : **rouges 3/5** sans le module (les cas verts restants sont des contre-cas d'absence d'effet, des valeurs imprimées ou des mots-clés NATIFS du moteur, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : Infralocked change d'hote (identite <-> sbire), carte Cloaked sur le heros. Cas plateau : ui-app/src/board/predator-plateau.test.ts (9 cas verts ; calibre ROUGE le 25/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd001b : Yd'Nar (AlterEgo)

```
* Yd'Nar (face ALTER-EGO) — SOLDIER. YAUTJA. PV 13, REC 4, main 6.
Setup: Put Infralocked into play.
Future Trophy — Action: Discard cards from the top of your deck until you discard an upgrade, then add that card to
  your hand. (Limit once per round.)

Cartes de reference :
 - Setup d'une carte mise de cote : `ch001b` Shang-Chi / `36001b` * Ororo Munroe (storm) : `BeginGameWithSetAside([...])` +
   `WhenCardSetup("This", op)` puis `PutIntoPlay`. Infralocked est « Permanent » et n'est PAS une des 15 cartes du deck
   (les impressions vont de 1/16 a 16/16, Infralocked est la 1/16) : elle part de cote et entre en jeu au Setup.
 - « discard cards from the top of your deck until you discard X, then add that card to your hand » : le mot-cle `seek`
   (fiche mots-cles/seek.md), `br009` Oathbrother : `joueur.DiscardDeckUntil(effect, card_type=Upgrade)` puis `Faces.AddToHand`.
 - Action d'alter-ego limitee : `WhenInYourPlayTurn(AbilityType.AlterEgoAction, op).LimitOncePerRound()` (bt001b).

⚠ Mots-pieges :
 - « Put Infralocked INTO PLAY » : Infralocked s'attache a l'IDENTITE du joueur (le moteur n'a pas d'amelioration libre :
   « return this card to your play area » = revenir sur l'identite, voir pd002). Seule la face ALTER-EGO le fait.
 - « Action » nu sur l'alter-ego : `AlterEgoAction` ; « Limit once per round » (par carte).
 - « until you discard AN UPGRADE » : n'importe quelle amelioration (Upgrade), pas seulement TECH.
 - « then add THAT card to your hand » : la carte defaussee qui a arrete la boucle revient en main (et elle seule).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - pd001b Setup : Infralocked entre en jeu AU SETUP sur l'identite
      - pd001b Yd'Nar : valeurs imprimees PV 13, REC 4, SOLDIER YAUTJA
      - pd001b Future Trophy : defausse du deck jusqu'a une AMELIORATION, qui revient en main (Wrist Blades sous 2 Genius) ; 1 carte de fond reste
      - pd001b Future Trophy : « Limit once per round » -> une SECONDE Action dans le round ne fait rien (une seule amelioration en main)
      - pd001b Future Trophy : « Action » d'ALTER-EGO -> absente en forme HEROS (aucune carte en main)
      Preuve par substitution : **rouges 3/5** sans le module (les cas verts restants sont des contre-cas d'absence d'effet, des valeurs imprimées ou des mots-clés NATIFS du moteur, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? OUI (« Limit once per round »). Témoin d'épuisement : cas « Limit once per round » (deux déclenchements, le second ne fait rien, chiffre mesuré). Résultat : OK.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : Infralocked entre en jeu sur l'identite au Setup. Cas plateau : ui-app/src/board/predator-plateau.test.ts (9 cas verts ; calibre ROUGE le 25/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd002 : Infralocked (Upgrade)

```
* Infralocked — AMELIORATION, cout 0, Permanent. TACTIC. UNIQUE, un seul exemplaire (1/16), mise de cote puis mise en jeu
par le Setup de l'alter-ego (pd001b), deplacee de sbire en sbire par la Reponse du heros (pd001a).
Permanent.
Hero Interrupt: When Predator defeats attached minion, remove 2 threat from a scheme (3 threat instead from a side
  scheme). Then, return this card to your play area.

Cartes de reference :
 - `yd012` Yaka Arrow (pack yondu) : amelioration unique qui change d'hote (ennemi / identite) par `AttachTo2` ; son
   Interrupt part de l'ENNEMI porteur (`WhenUnitWouldBeDefeated`) ; `AttachToFaceWhenPutIntoPlay("YourIdentity")`
   (`sk147`, `mf016`) pour l'entree en jeu sur l'identite.
 - `WhenUnitBeDefeated(.., "AttachedCharacter", op, attacker=...)` (`pu092`, sl040) : « attached minion is defeated ».
 - `RetirerMenaceDUneManigance` (alligator_loki / web_of_deceit) : « remove N threat from a scheme », choix du joueur.

⚠ Mots-pieges :
 - « Permanent » : base automatique (`desc.Permanent`), AUCUN code. ⚠ L'amelioration ne quitte donc jamais le jeu par
   l'effet d'un AUTRE set : si son sbire hote disparait autrement que par Predator, elle reste en jeu (a verifier au harnais).
 - « Return this card TO YOUR PLAY AREA » : le moteur n'a pas d'amelioration libre ; la carte revient sur l'IDENTITE du
   joueur (decision d'implementation, signalee a l'utilisateur) : `AttachTo2(identite)`.
 - « 2 threat from a scheme (3 threat INSTEAD from a SIDE scheme) » : la valeur depend de la manigance CHOISIE ; le
   complot principal vaut 2, une manigance annexe 3 (pas 2+1).
 - « When PREDATOR defeats attached minion » : le heros Predator lui-meme (nom propre : face HEROS seulement), pas un
   allie ; l'Interrupt part AVANT la defaite (le sbire porte encore la carte).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - pd002 Infralocked : Predator vainc le sbire porteur -> 2 menaces retirees du complot principal, retour sur l'identite
      - pd002 Infralocked : sur une manigance ANNEXE, 3 menaces et non 2 (« 3 threat instead from a side scheme »)
      - pd002 Infralocked : le sbire porteur tombe par une AUTRE cause que Predator -> Infralocked ne disparait pas
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : une amelioration dessinee tantot sur l'identite, tantot sur un sbire engage. Cas plateau : ui-app/src/board/predator-plateau.test.ts (9 cas verts ; calibre ROUGE le 25/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd003 : Xenomorph (PlayerMinion)

```
Xenomorph (Warrior) — SBIRE DE JOUEUR, cout 0, [wild]. PV 4, MNG 0 / ATQ 2. XENOMORPH. Hero.
Teamwork (XENOMORPH).
When Defeated: Ready Predator.
Interrupt: When Xenomorph is defeated, shuffle it into your deck.

Cartes de reference :
 - `al002` * Throg (pack alligator_loki) : le SEUL autre sbire de joueur (type `PlayerMinion`, entete de
   `game/card/face/card_type/minion_player.py`) : joue depuis la main contre son cout, s'engage avec son proprietaire ;
   « When Defeated » par `WhenUnitBeDefeated(WhenDefeated, "This", op)` ; remelange dans le deck du PROPRIETAIRE par
   `Faces.ShuffleAllTo(.., joueur.player_deck, effect)`.
 - `32159` Fabian Cortez / `38029` Donald Pierce : `desc.Teamwork` natif (fiche mots-cles/teamwork.md), AUCUN script.
 - `Faces.ReadyAll([heros], effect)` (an001a, 31009) pour « ready Predator ».

⚠ Mots-pieges :
 - « Teamwork (XENOMORPH) » : natif, relu dans `desc` ; la Reine et les Drones du set nemesis portent le meme trait.
 - « When Defeated: Ready PREDATOR » : le HEROS Predator, sans condition « you defeated » (n'importe quel joueur ou carte
   peut vaincre le sbire).
 - « Interrupt: When Xenomorph is defeated, shuffle it into YOUR deck » : au deck du joueur PROPRIETAIRE, apres « Ready Predator » ;
   ecrit DANS le When Defeated (une vraie Interruption sortait la carte avant la defaite et muselait le Ready).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (6 cas sujets) :
      - pd003 Xenomorph : joue depuis la main (cout 0), il entre en jeu ENGAGE avec son proprietaire
      - pd003 Xenomorph : When Defeated -> Predator se redresse
      - pd003 Xenomorph : Interrupt, vaincu il est melange dans le deck du joueur (et plus en jeu)
      - pd003 Xenomorph : Teamwork (XENOMORPH) -> avec la Reine deja en jeu, il s'active a son arrivee (Predator se defend : incline)
      - pd003 Xenomorph : SANS autre XENOMORPH en jeu, aucune activation a l'arrivee (Predator reste pret)
      - pd003 Xenomorph : valeurs imprimees PV 4, ATQ 2, MNG 0, XENOMORPH
      Preuve par substitution : **rouges 2/6** sans le module (les cas verts restants sont des contre-cas d'absence d'effet, des valeurs imprimées ou des mots-clés NATIFS du moteur, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : sbire de JOUEUR engage avec son proprietaire. Cas plateau : ui-app/src/board/predator-plateau.test.ts (9 cas verts ; calibre ROUGE le 25/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd004 : Ghost Protocol (Event)

```
Ghost Protocol — EVENEMENT, cout 1, [energy]. THWART. x2.
Hero Action (thwart): Remove 2 threat from a scheme (4 threat instead if you are cloaked).

Cartes de reference :
 - `core/01052` Chase Them Down : `this.RemoveThreatFromSchemes(effect.targets, n, effect)` + `.SetPlay().SetLabel('thwart')`
   + `.SetTarget(Scheme2)` (la manigance est choisie par le selecteur de la carte).
 - `ShinobiCloak` / `IsCloaked` : la carte Cloaked (fiche mots-cles/cloaked.md).

⚠ Mots-pieges :
 - « 4 threat INSTEAD if YOU are cloaked » : 4 au lieu de 2 (pas 2 + 4) ; « you » = Predator (la face HEROS porte la carte
   Cloaked) ; la carte Cloaked n'est PAS consommee par cet evenement (il la lit seulement).
 - « from A scheme » : une manigance au choix, principale ou annexe.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - pd004 Ghost Protocol : retire 2 menaces d'une manigance (Predator non camoufle)
      - pd004 Ghost Protocol : Predator CAMOUFLE -> 4 menaces retirees
      - pd004 Ghost Protocol : la carte Cloaked n'est PAS consommee par l'evenement (elle est seulement lue)
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou agit sur des cartes déjà couvertes. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd005 : Spine Rip (Event)

```
Spine Rip — EVENEMENT, cout 3, [physical]. ATTACK. x2.
Hero Action (attack): Deal 7 damage to an enemy. If that enemy has Infralocked attached, this attack gains overkill.

Cartes de reference :
 - `core/01053` Relentless Assault : `hero.DealDamage(effect.targets, N, effect, property=AttackProperty(overkill=...))`
   (fiche mots-cles/overkill.md : l'outrepassement se donne a l'ATTAQUE) ; `.SetPlay().SetLabel('attack')`.
 - `Hote` / `GetAttachedUpgrades` (ares, yd012) : lire les ameliorations posees sur la cible.

⚠ Mots-pieges :
 - « an ENEMY » : sbire ou vilain (`Enemy`), pas seulement un sbire ; Infralocked ne s'attache qu'a un sbire.
 - « THAT enemy has Infralocked attached » : la carte nommee, lue sur la CIBLE avant les degats.
 - « this attack GAINS overkill » : le debordement va sur le vilain/le heros selon le mot-cle, pas des degats en plus.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - pd005 Spine Rip : 7 degats a un sbire de 4 PV sans Infralocked : il tombe, l'exces ne va PAS au vilain
      - pd005 Spine Rip : Infralocked sur la cible -> overkill, l'exces (7 - 2 PV = 5) frappe le vilain
      - pd005 Spine Rip : sans Infralocked sur la cible -> PAS d'overkill, le vilain ne prend rien
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou agit sur des cartes déjà couvertes. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd006 : Shadow Counter (Event)

```
Shadow Counter — EVENEMENT, cout 1, [mental]. DEFENSE.
Hero Interrupt (defense): When you would take any amount of damage, prevent 3 of that damage. Then, give Predator a cloaked
  status card.

Cartes de reference :
 - `core/spider_man/01003` Backflip : `WhenUnitWouldTakeDamage(Interrupt, "You", op).SetPlay().SetLabel('defense')` et
   `message.PreventDamage(n, effect)`.
 - `ShinobiCloak` (fiche cloaked.md) : « give X a cloaked status card ».

⚠ Mots-pieges :
 - « ANY amount of damage » : pas seulement une attaque (aucun `is_from_attack`), contrairement a Backflip ; at_least_damage=1.
 - « prevent 3 OF THAT damage » : au plus 3, pas toute l'attaque.
 - « THEN give Predator a cloaked status card » : apres la prevention ; la carte Cloaked posee ne reduit PAS ces degats-ci
   (elle ne vaut que pour les PROCHAINS). Predator deja camoufle : rien (une seule carte).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - pd006 Shadow Counter : attaque de Sandman (ATQ 3 - DEF 2 = 1 degat) -> tout est evite et Predator est camoufle
      - pd006 Shadow Counter : 5 degats directs -> 3 evites, 2 subis, puis camoufle (n'est PAS limite aux attaques)
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : pose une carte d'etat Cloaked. Cas plateau : ui-app/src/board/predator-plateau.test.ts (9 cas verts ; calibre ROUGE le 25/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd007 : Savage Skewer (Event)

```
Savage Skewer — EVENEMENT, cout 2, [physical]. ATTACK. TACTIC. x2.
Hero Action (attack): Deal 5 damage to an enemy. You may discard a cloaked status card to either stun and confuse that
  enemy or discard an attachment on that enemy with the text "Hero Action" or "Hero Response".

Cartes de reference :
 - `core/01053` Relentless Assault : degats d'attaque d'un evenement ; `rainy/rescue_rainy/90116` Magnetic Restraints :
   « stun » / « discard an attachment with Hero Action or Hero Response » (`Players.DiscardHeroActionAttachment`) ;
 - `Player.MayChooseOneAbility(effect, A, B)` : les deux branches + « Cancel » (« you MAY »).

⚠ Mots-pieges :
 - « discard A cloaked status card » : DECISION UTILISATEUR (25/10/2026) = celle de PREDATOR seulement. Pas de carte Cloaked
   sur Predator : l'option n'est pas offerte et seuls les 5 degats partent.
 - « to EITHER stun and confuse OR discard an attachment » : une seule des deux branches ; « stun AND confuse » = les deux statuts.
 - « that enemy » : celui qui vient de recevoir les degats ; il peut etre mort (aucune option alors).
 - « an attachment on that enemy with the text Hero Action or Hero Response » : attachement de RENCONTRE (type Attachment),
   pas une amelioration (Infralocked est une Upgrade) ; branche non offerte sans cible valide.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - pd007 Savage Skewer : 5 degats au vilain ; Predator NON camoufle -> aucune option, aucun statut
      - pd007 Savage Skewer : camoufle, branche « stun and confuse » -> le vilain est etourdi ET desoriente, Cloaked defaussee
      - pd007 Savage Skewer : camoufle, branche « attachement » -> l'attachement a Hero Action est defausse, pas d'etourdissement
      - pd007 Savage Skewer : camoufle mais le joueur REFUSE (Cancel) -> Cloaked conservee, rien d'autre
      Preuve par substitution : **rouges 4/4** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou agit sur des cartes déjà couvertes. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd008 : Jungle Stalk (Event)

```
Jungle Stalk — EVENEMENT, cout 0, [mental]. TACTIC.
Hero Action: Find a minion and put it into play engaged with you → heal damage from your hero for each icon (★ and Y) in
  that card's boost area and give Predator a cloaked status card.

Cartes de reference :
 - `br011` Hammer Time (pack beta_ray_bill) : « search ... for a minion and put it into play engaged with you → ... » : la
   carte convoque un sbire (COUT, fleche), puis agit sur lui ; ici `Find.Find` (regle « Find » du 23/10/2026).
 - `core/01051` : `this.HealthUnits(unites, n, effect)` pour soigner.
 - `FacesCounter.CountTotalBoostIcons` / `CountTotalBoostStar` (15004, ho014) : les icones du cadre de boost.

⚠ Mots-pieges :
 - « each icon (★ AND Y) in THAT card's boost area » : icones de boost ordinaires + icone a etoile du sbire convoque.
 - « heal damage FROM YOUR HERO » : le HEROS du joueur (pas un allie, pas l'identite alter-ego) : 1 PV par icone.
 - « AND give Predator a cloaked status card » : meme si 0 PV soigne ; une seule Cloaked par personnage.
 - « Find a minion » est un COUT (fleche) : sans sbire a trouver, rien ne se passe (pas de Cloaked).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - pd008 Jungle Stalk : trouve un sbire a 2 icones de boost (Shocker) -> 2 PV soignes, Predator camoufle, sbire engage
      - pd008 Jungle Stalk : sbire a ETOILE seulement (Weapons Runner : 0 icone + l'etoile) -> 1 PV soigne
      - pd008 Jungle Stalk : Drone (1 icone + etoile) -> 2 PV soignes (etoile ET icone comptees)
      - pd008 Jungle Stalk : AUCUN sbire a trouver -> rien (ni soin, ni Cloaked) : « Find » est un COUT
      - pd008 Jungle Stalk : « Find » balaie TOUTES les zones, y compris le deck du joueur : son propre Xenomorph (sbire de joueur) est trouve
      Preuve par substitution : **rouges 4/5** sans le module (les cas verts restants sont des contre-cas d'absence d'effet, des valeurs imprimées ou des mots-clés NATIFS du moteur, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : pose une carte d'etat Cloaked et met un sbire en jeu. Cas plateau : ui-app/src/board/predator-plateau.test.ts (9 cas verts ; calibre ROUGE le 25/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd009 : Honor Hunt (PlayerSideScheme)

```
* Honor Hunt — MANIGANCE ANNEXE DE JOUEUR, cout 0, [wild]. Menace 5. Victory 0. Assault.
While Honor Hunt is in the victory display, it gains "Action: Find a minion and put it into play engaged with you. Any player
  may trigger this ability. (Limit once per round)."

Cartes de reference :
 - `40006` Technovirus Purge / `40018` Call for Backup : le type `PlayerSideScheme` (cout, `StartingThreat`, `Victory 0`),
   SANS script ; `Assault` et `Victory` sont des bases automatiques (`desc`, fiches mots-cles/assault.md, victory.md).
 - la capacite « en vitrine » : RECETTES §3bis, `rs009` Queen of Sogaria (pack red_sonja) : posee sur L'IDENTITE (pd001a ET
   pd001b), `ActionHonorHuntEnVitrine` dans `__init__.py` ; `pu141` pour `AnyPlayerCanDoThis` + limite.

⚠ Mots-pieges :
 - « Assault » : les contres de BASE contre cette manigance utilisent l'ATQ au lieu de la MNG (base automatique du moteur).
 - « Victory 0 » : la manigance va a la vitrine quand elle est vaincue (`desc.Victory`).
 - « While it is in the victory display, IT GAINS » : l'Action n'existe qu'en vitrine ; elle est portee par l'identite de
   Predator (une carte en vitrine est hors jeu), declenchable par N'IMPORTE QUEL joueur, une fois par round.
 - « Find a minion and put it into play engaged WITH YOU » : « you » = le joueur qui declenche, pas Predator.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - pd009 Honor Hunt : jouee depuis la main (cout 0), elle entre en jeu avec 5 menaces
      - pd009 Honor Hunt : Assault -> un contre de BASE utilise l'ATQ (3) et non la MNG (0 pour Predator) : 5 -> 2
      - pd009 Honor Hunt : EN VITRINE, l'Action « find a minion ... engaged with you » est offerte : le Shocker entre en jeu
      - pd009 Honor Hunt : PAS en vitrine -> l'Action n'est pas offerte (aucun sbire ne bouge)
      - pd009 Honor Hunt : « Limit once per round » -> une SECONDE tentative dans le round ne fait rien (un seul sbire arrive)
      Preuve par substitution : le script de pd009 est VIDE (Assault, Victory, menace sont natifs) ; sa capacité « en vitrine » vit sur l'identité : **cas « EN VITRINE » et « Limit once per round » rouges** quand `pd001a` est remplacé par un module vide (mesuré le 25/10). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? OUI (« Limit once per round »). Témoin d'épuisement : cas « Limit once per round » (deux déclenchements, le second ne fait rien, chiffre mesuré). Résultat : OK.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : manigance annexe de joueur, puis en vitrine de victoire. Cas plateau : ui-app/src/board/predator-plateau.test.ts (9 cas verts ; calibre ROUGE le 25/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd010 : Yautja Trophy Room (Support)

```
* Yautja Trophy Room — SOUTIEN, cout 2, [mental]. LOCATION.
Response: After you defeat a minion, place 1 skull counter here.
Resource: Exhaust Yautja Trophy Room and remove X skull counters from it → generate X [wild] resources.

Cartes de reference :
 - `an001a` / `vp001a` : `AfterUnitDefeatedUnit(Response, "You", Minion, op)` ; `Faces.PlaceCountersOn([this], 1, 'skull', effect)`
   (compteur `skull` ajoute a l'enum `COUNTER`, card_face.py, 25/10/2026).
 - `sm011` Spinnerets (« Remove X web counters → generate X [wild] ») : « retire 1 pion → 1 ressource, autant de fois que de
   pions », equivalent en jeu (les ressources s'additionnent sur le meme paiement), `SetToAvailableTimesFn` ;
   `ze011` Mount Olympus : `CostFunc.Custom` pour un cout arbitraire ; `conditions=[...]` OBLIGATOIRE sur `CanGenerateResources`.

⚠ Mots-pieges :
 - « EXHAUST ... and remove X counters » : l'inclinaison n'est payee QU'UNE FOIS par paiement, X pions sont retires pour X
   ressources. Montage : chaque utilisation retire 1 pion ; la premiere incline la carte, les suivantes (meme paiement) la
   trouvent deja inclinee PAR CE PAIEMENT (marque `_pd_paiement` posee sur l'effet paye, lue par la condition de disponibilite).
   Une carte inclinee par autre chose reste inutilisable.
 - « After YOU defeat a minion » : Predator lui-meme, un SBIRE (Minion), pas un allie.
 - « a Resource: » sans « Hero » : utilisable aux deux formes ; ressource wild (`Resources("G")`).
 - UNE SEULE `CanGenerateResources` par carte (assert du moteur).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (6 cas sujets) :
      - pd010 Trophy Room : Predator vainc un sbire -> 1 compteur skull
      - pd010 Trophy Room : un sbire vaincu par une AUTRE cause que Predator -> aucun compteur
      - pd010 Trophy Room : Resource -> 2 compteurs retires, UNE seule inclinaison, 2 ressources wild paient Spine Rip... (cout 3 : + Energy)
      - pd010 Trophy Room : 3 compteurs, cout 2 pays par la salle seule -> X = 2 : il en reste 1
      - pd010 Trophy Room : 2 compteurs paient Ghost Protocol (cout 1) avec UNE seule utilisation : 1 compteur retire
      - pd010 Trophy Room : sans compteur, la ressource n'est pas offerte : l'evenement n'est PAS joue
      Preuve par substitution : **rouges 4/6** sans le module (les cas verts restants sont des contre-cas d'absence d'effet, des valeurs imprimées ou des mots-clés NATIFS du moteur, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : compteurs « skull ». Cas plateau : ui-app/src/board/predator-plateau.test.ts (9 cas verts ; calibre ROUGE le 25/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd011 : Self Destruct (Upgrade)

```
* Self Destruct — AMELIORATION, cout 2, [energy][energy]. TECH. WEAPON.
Hero Action: Exhaust this card → place 2 glyph counters here.
Hero Action: Remove this card from the game → deal 1 damage to the villain and each minion engaged with you (to a maximum
  of 10) for each glyph counter here.

Cartes de reference :
 - `Faces.PlaceCountersOn([this], n, 'glyph', effect)` (compteur `glyph` ajoute a l'enum `COUNTER`, 25/10/2026) ;
   `CostFunc.Exhaust("This")` pour « Exhaust this card → » (`core/01051`, tr009 Raphael pour un cout qui lit un compteur).
 - `CostFunc.RemoveFromGame("This")` : « Remove this card from the game → ». ⚠ Il retire la carte AVANT l'effet : le nombre de
   glyphes doit etre lu dans le cout, donc un `CostFunc.Custom` qui memorise le compteur sur l'effet PUIS retire la carte.
 - `this.DealDamage(unites, n, effect)` (`core/01051`), `player.GetEngagedMinions()` (ra002).

⚠ Mots-pieges :
 - « each minion engaged WITH YOU » : les sbires engages avec le joueur qui joue, pas ceux des autres joueurs.
 - « (to a maximum of 10) » : ARBITRAGE PROVISOIRE (25/10/2026) = plafond de 10 glyphes comptes, soit 10 degats au plus par
   cible (1 degat par glyphe). Question posee a l'auteur (QUESTIONS-AUTEUR.md) : ces lectures donnent le meme resultat par cible.
 - « for EACH glyph counter » : 1 degat par glyphe, au vilain ET a chaque sbire engage.
 - Les deux Actions sont distinctes : l'une incline (chargement), l'autre detruit l'objet ; aucune limite imprimee.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - pd011 Self Destruct : 1re Action -> incline, 2 compteurs glyph
      - pd011 Self Destruct : 2e Action avec 3 glyphes -> 3 degats au vilain ET au sbire engage (vaincu), la carte quitte la partie
      - pd011 Self Destruct : 12 glyphes -> plafond de 10 degats (vilain)
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : compteurs « glyph », amelioration inclinee. Cas plateau : ui-app/src/board/predator-plateau.test.ts (9 cas verts ; calibre ROUGE le 25/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd012 : Yautja Wrist Blades (Upgrade)

```
Yautja Wrist Blades — AMELIORATION, cout 1, [physical]. TECH. WEAPON.
Predator gains retaliate 1 and his basic attacks gain piercing.

Cartes de reference :
 - `core/captain_america/03009` Captain America's Shield : `*GiveKeywordToAttached(CardFinder(name="..."), retaliate=1)`
   (fiche mots-cles/retaliate.md) ;
 - `UnitAttackGainKeyword(attacker, target, is_basic_attack=True, piercing=True)` (do_attack.py) : « his basic attacks gain
   piercing » (fiche mots-cles/piercing.md ; `27078`, ho016).

⚠ Mots-pieges :
 - « PREDATOR gains » : NOM PROPRE, la face HEROS seulement ; ni Yd'Nar (l'alter-ego ne combat pas), ni un allie.
 - « his BASIC attacks » : l'attaque de base (pouvoir ATK) ; PAS les attaques d'evenement ni d'amelioration (Plasmacaster,
   Spine Rip). `is_basic_attack=True`.
 - Retaliate 1 sans condition (« gains » = tant que la carte est en jeu), et la carte ne se retire qu'a la defausse.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - pd012 Wrist Blades : Predator gagne retaliate 1 -> l'attaquant (Shocker) subit 1 degat
      - pd012 Wrist Blades : son attaque de BASE est perforante -> elle defausse la carte Tough et blesse quand meme (Shocker 3 PV tombe)
      - pd012 Wrist Blades : SANS les lames, la meme attaque est absorbee par Tough (le Shocker survit, Tough defaussee)
      - pd012 Wrist Blades : Spine Rip (attaque d'EVENEMENT, pas de base) n'est PAS perforante : Tough absorbe, le Shocker survit
      Preuve par substitution : **rouges 2/4** sans le module (les cas verts restants sont des contre-cas d'absence d'effet, des valeurs imprimées ou des mots-clés NATIFS du moteur, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou agit sur des cartes déjà couvertes. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd013 : Plasmacaster (Upgrade)

```
* Plasmacaster — AMELIORATION, cout 2, [energy]. TECH. WEAPON.
Hero Action (attack): Exhaust Plasmacaster → deal 2 damage to an enemy (3 damage instead if that enemy has an upgrade
  attached). This attack gains ranged.

Cartes de reference :
 - `core/01053` : `hero.DealDamage(effect.targets, n, effect, property=AttackProperty(ranged=True))` ;
   `CostFunc.Exhaust("This")` ; `.SetLabel('attack')` + `.SetTarget(Enemy)` ; fiche mots-cles/ranged.md.
 - `GetAttachedUpgrades()` (ares, yd012) : ameliorations posees sur la cible (Infralocked en est une).

⚠ Mots-pieges :
 - « 3 damage INSTEAD if that enemy has AN upgrade attached » : 3 au lieu de 2, quelle que soit l'amelioration (Infralocked
   compte) ; ATTACHEE a l'ennemi, pas posee a cote.
 - « This attack gains ranged » : ignore la riposte (`ranged=True`) ; ce n'est pas une attaque de BASE (Wrist Blades ne donne rien).
 - « Exhaust Plasmacaster → » : l'inclinaison est le COUT (payee avant le choix de cible).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - pd013 Plasmacaster : 2 degats a un ennemi SANS amelioration attachee, la carte s'incline
      - pd013 Plasmacaster : l'ennemi porte Infralocked (une amelioration) -> 3 degats
      - pd013 Plasmacaster : « ranged » -> pas de riposte (Rhino avec Concussion Blasters, retaliate 1 : Predator ne subit rien)
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou agit sur des cartes déjà couvertes. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd014 : Bio-Helmet (Upgrade)

```
* Bio-Helmet — AMELIORATION, cout 2, [mental]. ARMOR. TECH.
Hero Action: Exhaust Bio-Helmet → look at the top card of the encounter deck. For each icon (★ and Y) in that card's boost
  area, remove 1 threat from a scheme.

Cartes de reference :
 - `CostFunc.LookAtDeck("EncounterDeck", 1)` (cost_func.py) / `player.LookAtDeck(deck, n, effect)` : « look at the top card » ;
 - `FacesCounter.CountTotalBoostIcons` + `CountTotalBoostStar` (15004, ho014) : les icones du cadre de boost ;
 - `RetirerMenaceDUneManigance` (alligator_loki, web_of_deceit) : « remove N threat from a scheme », choix du joueur.

⚠ Mots-pieges :
 - « FOR EACH icon (★ and Y) ... remove 1 threat from A scheme » : DECISION UTILISATEUR (25/10/2026) = UNE manigance AU CHOIX
   PAR ICONE (repartition libre entre complot principal et annexes).
 - « look at the top card » : la carte reste sur le deck (aucun mouvement), meme sans icone.
 - « Exhaust Bio-Helmet → » : l'inclinaison est le COUT ; deck de rencontre vide : rien a regarder, rien ne part.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - pd014 Bio-Helmet : dessus du deck rencontre = Shocker (2 icones) -> 2 menaces retirees du complot principal, carte laissee sur le deck
      - pd014 Bio-Helmet : DEUX manigances differentes, une par icone (decision utilisateur du 25/10) : le complot principal n'a qu'1 menace, la 2e icone va sur l'annexe
      - pd014 Bio-Helmet : carte a ETOILE seule (Weapons Runner) -> 1 menace
      - pd014 Bio-Helmet : carte sans icone (traitrise sans Boost) -> aucune menace retiree, le casque est quand meme incline
      Preuve par substitution : **rouges 4/4** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou agit sur des cartes déjà couvertes. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd015 : Exposed Target (Obligation)

```
Exposed Target — Obligation (set « Predator »), Boost 2, « Give to the Yd'Nar player ».
You may flip to alter-ego form. Choose:
 • Exhaust Yd'Nar → remove Exposed Target from the game.
 • Discard each cloaked status card from your identity and 1 TECH upgrade you control. If no cards were discarded this way,
   this card gains surge. Discard this obligation.

Cartes de reference :
 - `sv011` Silver Down (silver_surfer) / `ch018` Family Ties (shang_chi) : MEME squelette — `WhenThisObligationGiveToYou`,
   `YouMayFlipToYourAlterEgoForm`, puis `joueur.ChooseAbilities` avec `condition=` par branche ;
 - `ThisCardGainSurge(effect)` (nt015, mf017) pour « this card gains surge » ;
 - `face.DiscardCloaked(effect, rule="All")` (can_status.py) pour « discard each cloaked status card ».

⚠ Mots-pieges :
 - 1re branche : « → remove FROM THE GAME » ; 2e branche : « DISCARD this obligation » : deux sorties DIFFERENTES (hc013 : une
   obligation reste en jeu tant qu'on ne la deplace pas) ;
 - « Exhaust Yd'Nar » : l'alter-ego, donc seulement apres le retournement et s'il est pret ; la fleche en fait un COUT ;
 - « discard each cloaked status card FROM YOUR IDENTITY AND 1 TECH upgrade YOU CONTROL » : les deux defausses, la carte
   Cloaked de Predator ET UNE amelioration TECH de ce joueur (au choix) ; « if NO cards were discarded this way » : ni Cloaked
   ni TECH defaussee -> surge (puis la carte est defaussee comme le texte l'ordonne).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - pd015 Exposed Target : forme alter-ego, branche 1 -> Yd'Nar s'incline et l'obligation est RETIREE de la partie
      - pd015 Exposed Target : branche 2 -> la carte Cloaked ET une amelioration TECH (Wrist Blades) sont defaussees, l'obligation aussi (pas de surge)
      - pd015 Exposed Target : branche 2 SANS Cloaked ni TECH -> « this card gains surge » : la carte du dessus (Shocker) est revelee, l'obligation defaussee
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou agit sur des cartes déjà couvertes. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd016 : Xenomorph's Prey (SideScheme)

```
Xenomorph's Prey — MANIGANCE ANNEXE (set « Predator Nemesis »), menace 3 par joueur, Boost 2. Hazard.
Once the hunter, now the hunted. The Xenomorph's Queen has marked her prey.
While this card is in play, Predator cannot gain cloaked status cards.
When Revealed: Place 1 additional threat here for each status card in play.

Cartes de reference :
 - `mf015` Hubris (mister_fantastic_nemesis) : `WhenThisRevealed(None, op)` + `this.PlaceThreatOnSchemes([this], n, effect)` ;
 - `ah006` Gamma Barrier (totally_awesome_hulk) : `WhenUnitWouldBeStatus(type, unite, [statuts], op)` puis
   `message.SetBeInstead(effect)` pour REFUSER la pose d'une carte d'etat ;
 - `Hazard` et `StartingThreat "3*"` : bases automatiques (`desc`, fiches mots-cles/hazard.md).

⚠ Mots-pieges :
 - « Predator CANNOT gain cloaked status cards » : NOM PROPRE, la face HEROS ; tant que la manigance est en jeu ; une carte Cloaked
   deja posee RESTE (« cannot gain », pas « loses »). Regle continue (`AbilityType.NonKeyword` : une `Rule` resterait active apres le retrait de la carte).
 - « for EACH status card IN PLAY » : toutes les cartes d'etat en jeu, de n'importe quel personnage (Sonne, Desoriente, Coriace,
   Camoufle...), ennemis compris ; comptees a la revelation.
 - « 1 ADDITIONAL threat » en plus de la menace imprimee (3 par joueur).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - pd016 Xenomorph's Prey : revelee, elle porte 3 menaces (3 par joueur, 1 joueur) et aucune de plus sans carte d'etat
      - pd016 Xenomorph's Prey : tant qu'elle est en jeu, Predator ne peut PAS recevoir de carte Cloaked
      - pd016 Xenomorph's Prey : une carte Cloaked DEJA posee RESTE quand la manigance arrive (« cannot gain », pas « loses »)
      - pd016 Xenomorph's Prey : SANS la manigance en jeu, Predator recoit bien sa carte Cloaked (temoin de la regle)
      - pd016 Xenomorph's Prey : When Revealed -> 1 menace de plus par carte d'etat EN JEU (Stunned sur le vilain + Tough sur un sbire = 2) : 3 + 2 = 5
      Preuve par substitution : **rouges 2/5** sans le module (les cas verts restants sont des contre-cas d'absence d'effet, des valeurs imprimées ou des mots-clés NATIFS du moteur, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : manigance annexe qui interdit les cartes Cloaked. Cas plateau : ui-app/src/board/predator-plateau.test.ts (9 cas verts ; calibre ROUGE le 25/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd017 : Xenomorph Queen (Minion)

```
* Xenomorph Queen — SBIRE nemesis de Predator (set « Predator Nemesis »). ELITE. XENOMORPH. PV 9, MNG 1, ATQ 3★, Boost 2.
Toughness.
★ Xenomorph Queen's attacks gain piercing and overkill.
(Predator's nemesis minion.)

Cartes de reference :
 - `UnitAttackGainKeyword("This", piercing=True, overkill=True)` (27078, ho016 ; Throg al002 pour overkill) : « X's attacks
   gain ... » ; fiches mots-cles/piercing.md, overkill.md ;
 - `Toughness` : base automatique (`desc.Toughness`, fiche toughness.md), AUCUN code ; `desc.Nemesis` : base automatique.

⚠ Mots-pieges :
 - « ★ » devant la phrase = icone etoile imprimee, PAS un « Boost: » : la capacite est CONSTANTE (convention moteur,
   RECETTES §3), pas liee a une carte de boost ; l'ATQ imprimee « 3★ » porte la meme etoile.
 - « Xenomorph Queen's attacks » : ses attaques a elle (`attacker="This"`), pas celles des autres Xenomorphes.
 - « piercing AND overkill » : les deux ; la Reine est ELITE (pas de limite en jeu, une seule carte).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - pd017 Xenomorph Queen : Toughness -> entre en jeu avec une carte Tough
      - pd017 Xenomorph Queen : valeurs imprimees PV 9, ELITE XENOMORPH
      - pd017 Xenomorph Queen : ses attaques sont PERFORANTES -> elles defaussent la carte Tough de Predator ET le blessent (ATQ 3 - DEF 2 = 1)
      - pd017 Xenomorph Queen : ses attaques ont l'OUTREPASSEMENT -> contre un sbire de 2 PV (Weapons Runner), l'exces de 1 va a Predator
      Preuve par substitution : **rouges 2/4** sans le module (les cas verts restants sont des contre-cas d'absence d'effet, des valeurs imprimées ou des mots-clés NATIFS du moteur, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : sbire nemesis a carte Tough. Cas plateau : ui-app/src/board/predator-plateau.test.ts (9 cas verts ; calibre ROUGE le 25/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd018 : Xenomorph Drone (Minion)

```
* Xenomorph Drone — SBIRE (set « Predator Nemesis »). XENOMORPH. PV 3, MNG 1, ATQ 2, Boost ★ + 1. Guard. Teamwork (XENOMORPH).
Forced Response: After Xenomorph Drone engages you, if there are no other minions engaged with you, deal yourself 1
  facedown encounter card.
★ Boost: Put Xenomorph Drone into play engaged with you.

Cartes de reference :
 - `38029` Donald Pierce : `AfterMinionEngagePlayer(ForcedResponse, "This", "You", op)` ;
 - `01121` Weapons Runner : `WhenCardBecomeBoost("This", PutThisIntoPlay)` (helper de `cards/pack/__init__.py`) ;
 - `ar012` / `16118` Badoon Grunt : `player.DealEncounterCards(1, effect)` pour « deal yourself 1 facedown encounter card » ;
 - `Guard` et `Teamwork` : bases automatiques (`desc`, fiches guard.md, teamwork.md), AUCUN script.

⚠ Mots-pieges :
 - « If there are NO OTHER minions engaged with you » : les AUTRES sbires engages avec CE joueur (le Drone ne compte pas).
 - « After Drone engages YOU » : « you » = le joueur auquel il vient de s'engager.
 - « ★ Boost » : icone etoile du cadre de boost (`desc.Boost "1**"` = 1 icone + l'etoile) ; une carte de boost entre en jeu
   engagee avec le joueur vise.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - pd018 Xenomorph Drone : valeurs imprimees PV 3, XENOMORPH, Guard
      - pd018 Xenomorph Drone : Forced Response, SEUL sbire engage -> 1 carte rencontre face cachee (revelee ensuite : le Shocker du dessus arrive)
      - pd018 Xenomorph Drone : un AUTRE sbire est deja engage -> aucune carte distribuee (le Shocker reste dans le deck)
      - pd018 Xenomorph Drone : [star] Boost -> il entre en jeu engage avec le joueur
      Preuve par substitution : **rouges 2/4** sans le module (les cas verts restants sont des contre-cas d'absence d'effet, des valeurs imprimées ou des mots-clés NATIFS du moteur, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou agit sur des cartes déjà couvertes. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd019 : Hunted By the Hive (Treachery)

```
Hunted By the Hive — TRAITRISE (set « Predator Nemesis »), Boost 2.
When Revealed: Xenomorph Queen attacks you. If it's not in play, find Xenomorph Queen and put it into play engaged with you.

Cartes de reference :
 - `27168` Symbiotic Strength (sm) : `villain.DoAttackYou(player, effect)` pour « X attacks you » ;
 - `Find.Find` (game/operate/find.py, regle « Find » du 23/10/2026) pour « find Xenomorph Queen », comme `AmenerLaReine`
   (helper du set) ; `br011` / `Search.SearchForCard` pour « put it into play engaged with you ».

⚠ Mots-pieges :
 - « If it's not in play » : la Reine ABSENTE est trouvee (deck de rencontre, defausse, cartes mises de cote) ; deja en jeu elle attaque.
 - ARBITRAGE PROVISOIRE (25/10/2026, question posee a l'auteur, QUESTIONS-AUTEUR.md) : la Reine qui vient d'arriver ATTAQUE aussi
   (la 1re phrase est resolue apres son arrivee). Si l'auteur dit le contraire : retirer l'appel a `DoAttackYou` apres `AmenerLaReine`.
 - Reine introuvable (vaincue puis retiree, deja engagee ailleurs...) : rien ne se passe.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - pd019 Hunted By the Hive : Reine ABSENTE (mise de cote) -> trouvee et mise en jeu engagee, puis elle attaque (Predator se defend : incline)
      - pd019 Hunted By the Hive : Reine DEJA en jeu -> elle attaque (elle ne revient pas)
      - pd019 Hunted By the Hive : Reine INTROUVABLE -> rien ne se passe (Predator reste pret)
      Preuve par substitution : **rouges 2/3** sans le module (les cas verts restants sont des contre-cas d'absence d'effet, des valeurs imprimées ou des mots-clés NATIFS du moteur, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou agit sur des cartes déjà couvertes. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd020 : Acid Blood (Attachment)

```
Acid Blood — ATTACHEMENT (set « Predator Nemesis »), CONDITION, +1 ATQ, Boost 1.
Attached minion gains retaliate 1.
When Revealed: Find the Xenomorph Queen and put it into play engaged with you and attach this card to it.

Cartes de reference :
 - `GiveKeywordToAttached("AttachedCharacter"...)` : `core/captain_america/03009` (retaliate pour un personnage porteur),
   `ts007` (`this.AttachTo2(villain, effect)`) pour attacher une carte de rencontre a un sbire ;
 - `AmenerLaReine` (helper du set) : « find the Xenomorph Queen and put it into play engaged with you ».

⚠ Mots-pieges :
 - « +1 ATK » : l'icone imprimee a gauche (« +1 ATQ ») est un bonus du sbire PORTEUR : `GiveKeywordToAttached(..., attack=1)`.
 - « Attached minion gains retaliate 1 » : constant, tant que l'attachement est en place.
 - « Find the Xenomorph Queen ... AND attach this card to it » : si la Reine est DEJA en jeu, elle ne peut pas « entrer en jeu »
   mais la carte s'attache quand meme a elle (sinon l'attachement n'a pas d'hote) ; Reine introuvable : la carte s'attache
   au sbire engage de son choix, a defaut elle est defaussee.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - pd020 Acid Blood : When Revealed -> la Reine est trouvee, mise en jeu engagee et l'attachement s'accroche a elle
      - pd020 Acid Blood : la Reine est DEJA en jeu -> l'attachement s'accroche a elle
      - pd020 Acid Blood : « +1 ATK » -> la Reine frappe a 4 (ATQ 3 + 1 - DEF 2 = 2 degats)
      - pd020 Acid Blood : « retaliate 1 » -> Predator attaque la Reine et subit 1 degat de riposte
      Preuve par substitution : **rouges 4/4** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : attachement pose sur la Reine. Cas plateau : ui-app/src/board/predator-plateau.test.ts (9 cas verts ; calibre ROUGE le 25/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd021 : Energy (Resource)

```
Ressource de base : aucun script (comme hc024 / ht015). Texte : « Max 1 per deck. » (desc.MaxPerDeck, natif).
```

- [x] Étape 2 : cartes de référence : `hc024` / `ht015` (ressources de base à l'art d'un héros).
- [x] Étape 5 : texte-contre-code : « Max 1 per deck » = `desc.MaxPerDeck`, `RES` lu sur le scan. Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - pd021 Energy : deux ressources energie (YY) paient Ghost Protocol (cout 1) -- Max 1 par deck
      Preuve par substitution : sans objet (aucun module).
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou agit sur des cartes déjà couvertes. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd022 : Genius (Resource)

```
Ressource de base : aucun script (comme hc024 / ht015). Texte : « Max 1 per deck. » (desc.MaxPerDeck, natif).
```

- [x] Étape 2 : cartes de référence : `hc024` / `ht015` (ressources de base à l'art d'un héros).
- [x] Étape 5 : texte-contre-code : « Max 1 per deck » = `desc.MaxPerDeck`, `RES` lu sur le scan. Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - pd022 Genius : deux ressources mentales (BB) paient Shadow Counter (cout 1)
      Preuve par substitution : sans objet (aucun module).
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou agit sur des cartes déjà couvertes. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd023 : Strength (Resource)

```
Ressource de base : aucun script (comme hc024 / ht015). Texte : « Max 1 per deck. » (desc.MaxPerDeck, natif).
```

- [x] Étape 2 : cartes de référence : `hc024` / `ht015` (ressources de base à l'art d'un héros).
- [x] Étape 5 : texte-contre-code : « Max 1 per deck » = `desc.MaxPerDeck`, `RES` lu sur le scan. Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - pd023 Strength : deux ressources physiques (RR) paient Spine Rip (cout 3) avec une Energy
      Preuve par substitution : sans objet (aucun module).
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou agit sur des cartes déjà couvertes. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd024 : Razor Hunt (Event)

```
Razor Hunt — EVENEMENT BASIC, cout 1, [physical]. ATTACK. Team-Up (Wolverine and Predator). Max 1 per deck.
Hero Action (attack): Deal 1 damage each to Wolverine and Predator. Deal 3 damage to an enemy. Deal 3 damage to an enemy.

Cartes de reference :
 - `br011` Hammer Time / `al023` Little Rascals / `12020` Swarm Tactics : UN EVENEMENT TEAM-UP PORTE `.SetTarget("TeamUp")`
   (assert de `database.py:223`) ; `desc.TeamUp "Wolverine;Predator"` et `desc.MaxPerDeck` sont des bases automatiques
   (fiche mots-cles/teamup.md : les allies comptent) ;
 - `Worlds.GetOnFieldFriendlyCharacters(effect)` (al023) pour retrouver Wolverine et Predator ; `core/01053` pour l'attaque.

⚠ Mots-pieges :
 - « 1 damage EACH to Wolverine AND Predator » : 1 degat a CHACUN des deux (ils se blessent eux-memes : cout de la carte) ;
 - « Deal 3 damage to AN enemy. Deal 3 damage to AN enemy. » : DEUX applications independantes, chacune CHOISIT son ennemi
   (le meme deux fois ou deux differents) ; texte litteral, question posee a l'auteur (QUESTIONS-AUTEUR.md) ;
 - « Wolverine » : tout personnage ami de ce nom (allie 32041, ou heros) ; ce n'est pas une carte du deck de Predator seule.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - pd024 Razor Hunt : Team-Up (Wolverine et Predator en jeu) -> 1 degat a CHACUN d'eux et 3 + 3 degats a l'ennemi
      - pd024 Razor Hunt : SANS Wolverine en jeu -> la carte n'est pas jouable (reste en main, rien ne bouge)
      Preuve par substitution : **rouges 1/2** sans le module (les cas verts restants sont des contre-cas d'absence d'effet, des valeurs imprimées ou des mots-clés NATIFS du moteur, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou agit sur des cartes déjà couvertes. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd025 : Infrared Web (Event)

```
Infrared Web — EVENEMENT BASIC, cout 1, [energy]. ATTACK. DEFENSE. Team-Up (Spider-Man and Predator). Max 1 per deck.
Hero Interrupt (attack/defense): When an enemy attack would deal damage to you, prevent 3 of that damage. Deal 3 damage to an enemy.

Cartes de reference :
 - `core/spider_man/01003` Backflip : `WhenUnitWouldTakeDamage(Interrupt, "You", op, is_from_attack=True)` et
   `message.PreventDamage(n, effect)` ; `.SetTarget("TeamUp")` obligatoire pour un evenement Team-Up (br011, al023).

⚠ Mots-pieges :
 - « When an enemy ATTACK would deal damage to YOU » : une attaque ennemie contre toi (`is_from_attack=True`), pas les degats
   indirects ni ceux d'une traitrise ; « prevent 3 OF THAT damage » : au plus 3 ;
 - « Deal 3 damage to an enemy » : un ennemi au choix, EN PLUS de la prevention (fiche mots-cles/teamup.md : Spider-Man doit
   etre en jeu, heros ou allie) ; coquille du scan : « damge » (lu « damage »).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - pd025 Infrared Web : Team-Up (Spider-Man et Predator) -> evite 3 degats d'une attaque et inflige 3 degats a un ennemi
      - pd025 Infrared Web : SANS Spider-Man en jeu -> la carte n'est pas jouee (Predator encaisse l'attaque, le vilain n'est pas touche)
      Preuve par substitution : **rouges 1/2** sans le module (les cas verts restants sont des contre-cas d'absence d'effet, des valeurs imprimées ou des mots-clés NATIFS du moteur, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou agit sur des cartes déjà couvertes. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd026 : Chopper (SideScheme)

```
Chopper — MANIGANCE ANNEXE (set « Predator Alt Nemesis »), menace 3 (fixe), Boost 2. Permanent. Hazard.
Permanent.
While there is no threat here, this scheme loses the [hazard] icon.
Forced Response: After threat is placed here, if there is at least 8 threat here, the players lose the game.

Cartes de reference :
 - `sk285` Ultimate Nullifier / `27144` : `ThisGainKeyword(fn, hazard=N, change_on_event=...)` (l'icone Hazard portee par la carte) ;
   `sk138` : `change_on_event=OnEvent.Threat("This")` (un bonus qui suit la MENACE de la carte) ;
 - `AfterSchemePlaceThreat(type, "This", op, has_at_least_threat=N)` (scheme.py) ; `Worlds.SetGameOver(False, effect)` (27102b,
   sk145b) pour « the players lose the game » ;
 - `Permanent` et `Hazard` : bases automatiques (`desc`), AUCUN script (fiches permanent.md, hazard.md).

⚠ Mots-pieges :
 - « WHILE there is NO threat here, loses the hazard icon » : l'icone (imprimee, `desc.Hazard 1`) disparait a 0 menace et
   REVIENT des qu'il y en a de nouveau (bonus -1 dynamique, pas une suppression definitive).
 - « AFTER threat is placed here » : la menace POSEE (pas l'escalade des autres cartes) ; « at least 8 » = 8 ou plus, comptee
   sur la carte entiere.
 - « Permanent » : elle ne quitte pas le jeu (meme vaincue : a verifier au harnais) ; « the PLAYERS lose » : defaite collective.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (6 cas sujets) :
      - pd026 Chopper : revelee, 3 menaces (fixes) et l'icone Hazard
      - pd026 Chopper : « While there is no threat here, this scheme loses the hazard icon » -> a 0 menace, plus d'icone
      - pd026 Chopper : la menace REVIENT -> l'icone Hazard aussi
      - pd026 Chopper : 8 menaces -> les joueurs PERDENT la partie
      - pd026 Chopper : 7 menaces -> la partie continue
      - pd026 Chopper : Permanent -> un effet d'un AUTRE set ne peut pas la defausser
      Preuve par substitution : **rouges 2/6** sans le module (les cas verts restants sont des contre-cas d'absence d'effet, des valeurs imprimées ou des mots-clés NATIFS du moteur, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : manigance annexe Permanent a icone Hazard dynamique. Cas plateau : ui-app/src/board/predator-plateau.test.ts (9 cas verts ; calibre ROUGE le 25/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd027 : Dutch Schaefer (Minion)

```
* Dutch Schaefer — SBIRE nemesis de Predator (set « Predator Alt Nemesis »). ELITE. SOLDIER. PV 6, MNG 2★, ATQ 2★, Boost 2.
Toughness.
★ Forced Response: After Dutch Schaefer activates, place 1 threat on each scheme.
(Predator's nemesis minion.)

Cartes de reference :
 - `nt013` : `AfterEnemyActivationEnd(ForcedResponse, "This", op)` pour « after X activates » (toute activation, pas seulement
   contre toi) ; `27094` / `27158` : `this.PlaceThreatOnSchemes("EachScheme", 1, effect)` ;
 - `Toughness` et `Nemesis` : bases automatiques (`desc`).

⚠ Mots-pieges :
 - « After Dutch Schaefer ACTIVATES » : attaque OU manigance, contre n'importe quel joueur (pas « activates against you ») ;
 - « on EACH scheme » : le complot principal ET chaque manigance annexe, 1 menace chacune ;
 - « ★ » = etoile imprimee devant la phrase, capacite constante (convention RECETTES §3).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - pd027 Dutch Schaefer : Toughness -> entre en jeu avec une carte Tough ; valeurs imprimees PV 6, ELITE SOLDIER
      - pd027 Dutch Schaefer : apres son activation, 1 menace sur CHAQUE manigance (complot principal 4 -> 5, Chopper 3 -> 4)
      Preuve par substitution : **rouges 1/2** sans le module (les cas verts restants sont des contre-cas d'absence d'effet, des valeurs imprimées ou des mots-clés NATIFS du moteur, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou agit sur des cartes déjà couvertes. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd028 : Colonel Dillon (Minion)

```
* Colonel Dillon — SBIRE (set « Predator Alt Nemesis »). SOLDIER. PV 4, MNG 1, ATQ 2★, Boost 2. Patrol. Teamwork (SOLDIER).
★ Forced Response: After Colonel Dillon attacks you, place 1 threat on each scheme.

Cartes de reference :
 - `AfterUnitAttackEnd(ForcedResponse, "This", op, against_who="You")` (do_attack.py) pour « after X attacks you » ;
   `27094` : `this.PlaceThreatOnSchemes("EachScheme", 1, effect)` ;
 - `Patrol` et `Teamwork` : bases automatiques (`desc`, fiches patrol.md, teamwork.md).

⚠ Mots-pieges :
 - « After Dillon ATTACKS YOU » : une ATTAQUE contre le joueur (pas une manigance, pas une attaque contre un allie) ;
 - « on EACH scheme » : principal + annexes, 1 menace chacune ; « Teamwork (SOLDIER) » : le trait de Dutch Schaefer / Dillon.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - pd028 Colonel Dillon : une ATTAQUE contre le joueur -> 1 menace sur chaque manigance
      - pd028 Colonel Dillon : Teamwork (SOLDIER) -> avec Dutch deja en jeu il s'active a son arrivee (Predator se defend : incline)
      - pd028 Colonel Dillon : valeurs imprimees PV 4, SOLDIER, Patrol
      Preuve par substitution : **rouges 1/3** sans le module (les cas verts restants sont des contre-cas d'absence d'effet, des valeurs imprimées ou des mots-clés NATIFS du moteur, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou agit sur des cartes déjà couvertes. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd029 : M134 Minigun (Attachment)

```
M134 Minigun — ATTACHEMENT (set « Predator Alt Nemesis »), WEAPON, +1 ATQ, Boost 1.
Attach to Dutch Schaefer. If he is not in play, search the encounter deck and discard pile for him, reveal him and attach
  this card to him.
★ Forced Response: After Dutch Schaefer attacks you, place 1 threat on the Chopper side scheme.

Cartes de reference :
 - `Find.FindAndReveal` (game/operate/find.py) pour « search ... for him, reveal him » ; `this.AttachTo2(face, effect)` (ts007) ;
 - `GiveKeywordToAttached("Character", attack=1)` (retaliate/ATQ pour l'hote) ;
 - `AfterUnitAttackEnd(.., against_who="You")` (pd028) ; `PoserDeLaMenaceSurLeChopper` (helper du set).

⚠ Mots-pieges :
 - « +1 ATK » : l'icone imprimee : bonus d'ATQ de l'hote (Dutch) ;
 - « Attach to Dutch Schaefer. IF HE IS NOT IN PLAY, search ... » : Dutch en jeu = on s'attache a lui ; sinon on le cherche,
   on le REVELE (il s'engage) et on s'attache ; introuvable : defaussee ;
 - « After Dutch Schaefer attacks you » : le PORTEUR, contre le joueur ; « the Chopper side scheme » : le nom propre
   (`pd026`), rien si Chopper n'est pas en jeu.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - pd029 M134 Minigun : Dutch en jeu -> l'arme s'attache a lui
      - pd029 M134 Minigun : Dutch ABSENT (mis de cote) -> il est cherche, revele et l'arme s'attache a lui
      - pd029 M134 Minigun : « +1 ATK » -> Dutch frappe a 3 (ATQ 2 + 1 - DEF 2 = 1 degat)
      - pd029 M134 Minigun : apres l'attaque de Dutch contre le joueur -> 1 menace sur Chopper
      Preuve par substitution : **rouges 4/4** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : attachement pose sur Dutch. Cas plateau : ui-app/src/board/predator-plateau.test.ts (9 cas verts ; calibre ROUGE le 25/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### pd030 : Get To The... (Treachery)

```
Get To The... — TRAITRISE (set « Predator Alt Nemesis »), Boost 2.
When Revealed: The villain schemes. Place 2 threat on The Chopper side scheme.

Cartes de reference :
 - `27113` / `27082` (sm) : `villain.DoActivate(player, effect)` ; `enemy.DoSchemes(player, effect)` (enemy.py:46) pour « the
   villain schemes » ; `PoserDeLaMenaceSurLeChopper` (helper du set).

⚠ Mots-pieges :
 - « The villain SCHEMES » : une MANIGANCE du vilain contre le joueur qui revele (pas une activation au choix) ;
 - « Place 2 threat ON THE CHOPPER side scheme » : le nom propre, 2 menaces, rien si elle n'est pas en jeu.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - pd030 Get To The... : le vilain MANIGANCE et Chopper recoit 2 menaces (3 -> 5)
      - pd030 Get To The... : SANS Chopper en jeu -> le vilain manigance, aucune menace ailleurs
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON. Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (predator × rhino × équilibré/agressif × 8 graines), 16 parties de la variante predator_dutch, témoin spider_man (16 parties, mêmes réglages) : 0 victoire pour les trois (le pilote ne gagne pas contre Rhino, y compris avec le témoin), 5,5 à 6,1 rounds pour predator contre 6,1 à 6,9 pour le témoin, 0 incident ; grep tracebacks : 0 sur les 48 journaux. Journal lu : Infralocked suit les sbires et retire de la menace (3 sur une annexe), Jungle Stalk pose Cloaked, Honor Hunt est contrée à l'ATQ (Assault). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou agit sur des cartes déjà couvertes. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).
