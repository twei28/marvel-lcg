# Backlog 12 : gabarits PROCESSUS-CARTE (pack Dazzler dz004 à dz038, im001b, wc014)

Reprise du 20/10/2026 de la vérification des cartes hors irefrixs
(`.planning/todos/2026-10-06-verification-cartes-hors-irefrixs.md`), arrêtée à
la carte 4/40 du pack Dazzler. Branche `backlog-12-dazzler`, partie de
`78ce4b85` (`sauvegarde-cle-usb-2026-10-14` au moment du départ).

Questions ouvertes, une par carte : `.planning/todos/2026-10-20-backlog-12-questions.md`
(Q1 dz012, Q2 dz016, Q3 dz021, Q4 dz031, Q5 dz035). Les cartes concernées
sont « Carte terminée : NON » tant que la réponse n'est pas codée.

## Preuves communes à tout le lot

- **Scans** : `Fusion/marvel-lcg-src/assets/pics/dz0xx.png` (40 scans
  présents), lus un par un ; texte imprimé comparé mot à mot à
  `data/cards.json` (`text`, `desc`, `traits`).
- **Icônes de ressource** : planche des coins des 31 cartes à ressource du
  pack, comparée à la valeur `desc.RES` (étoile verte = G, nœuds bleus = B,
  éclair jaune = Y, poing rouge = R) : 31/31 conformes, dont `dz018` « YY ».
- **Icône de complot** : `dz021` porte l'icône **Amplify** (comparée aux
  complots officiels 16054, 16144, 27173, 32027) ; `desc` ne l'avait pas :
  corrigé.
- **Cas** : `Fusion/marvel-lcg-src/tools/cas/dazzler.py` (préfixe
  `[dazzler] dzNNN`), vérificateur `dz_etat` (main de chaque joueur, Setlist,
  compteurs hors jeu, cartes de boost, jouabilité, face cachée).
- **Substitution** : `tools/substituer_pack.py` par carte (script
  `subst.sh`, empreinte md5 du pack identique avant/après à chaque passe).
  Un cas resté vert sans module est, sauf mention, un contre-cas d'ABSENCE
  d'effet (assumé, RECETTES §7duodecies).
- **Mutations ciblées** (le module corrigé remis à l'ancienne valeur, le cas
  doit rougir) : dz005, dz006, dz011 (distance), dz014 (réduction), dz017b,
  dz022, dz030, dz032, dz033, dz021 (donnée Amplify), im001b/wc014 (« Phase »).
- **Étape 8 (autoplay)** et **étape 8 bis (plateau)** : voir la fin du
  fichier, une fois pour tout le pack.

Crédits imprimés différents de `data/cards.json` (`custom: "Lord Havok"`) :
dz024, dz025, dz026, dz027, dz032, dz033, dz034 portent « MC Custom Content
By: jakxin » ; dz037 « Dharmatrails & Lord Havok ». Non modifié (donnée de
crédit, pas de règle) : signalé dans le rapport.

---

### im001b : * Tony Stark (Inventor)

- [x] Étape 2 : `dz003` (`in_this="Round"`, 06/10/2026), `16024` Deft Focus.
- [x] Étape 5 : « the next upgrade played **this round** » : le module prenait
      `"Phase"` (écart avoué) → `"Round"`. Résultat : corrigé.
- [x] Étape 6 : réduction de 1, limite une fois par round : conforme.
- [x] Étape 7 : cas « im001b Inventor — l'Action réduit la prochaine
      amélioration de TOUT LE ROUND », ROUGE sous `"Phase"`, VERT sous
      `"Round"` ; 4/4 cas im001b verts.
- [x] Étape 7 bis : limite « once per round » : témoin existant « TEMOIN
      D'EPUISEMENT » vert.
- [ ] Étape 8 : voir autoplay commun.
- [x] Étape 8 bis : NON (coût seulement).

Carte terminée : voir étape 8 en fin de fichier.

### wc014 : Warping Reality

- [x] Étape 2 : `dz003`, `01092` Helicarrier (même brique).
- [x] Étape 5 : « the next card played **this round** » : `"Phase"` →
      `"Round"`. Résultat : corrigé.
- [x] Étape 6 : 1+X : conforme (cas historique).
- [x] Étape 7 : cas « wc014 Warping Reality — Action : la réduction dure TOUT
      LE ROUND », ROUGE sous `"Phase"`, VERT sous `"Round"` ; 2/2 verts.
- [x] Étape 7 bis : pas de limite imprimée.
- [ ] Étape 8 : voir autoplay commun.
- [x] Étape 8 bis : NON.

Carte terminée : voir étape 8 en fin de fichier.

---

### dz004 : "Beautiful Dreamer"

- [x] Étape 2 : `04049` / `sh019` (« if this removes the last threat »).
- [x] Étape 5 : « a scheme », « the last threat from THAT scheme », « you
      MAY », « ANOTHER scheme » ; label (thwart). Conforme.
- [x] Étape 6 : coût 2, B ; 3, 2, 2 : conformes.
- [x] Étape 7 : 4 cas (dernière menace → bonus ; témoin sans bonus ; refus
      Cancel ; Showtime! 2 menaces). Substitution 4/4 rouges.
- [x] Étape 7 bis : pas de limite.
- [x] Étape 8 bis : NON.

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz005 : "Beauty and the Beast"

- [x] Étape 2 : `Search.PlayerCard` (an001b), `01080` First Aid (Friend).
- [x] Étape 5 : « a **friendly** character » : le Showtime! visait
      `YouControlUnit` → `Friend` (corrigé). « still in play at the end of
      the phase » : conforme.
- [x] Étape 6 : coût 2, B, +2 THW : conformes.
- [x] Étape 7 : 6 cas (allié en jeu ; retour en main ; allié vaincu ;
      Showtime! +2 ; durée ; personnage d'un autre joueur). Substitution 5/6
      (le cas de durée est un contre-cas) ; mutation `YouControlUnit` → rouge.
- [x] Étape 7 bis : pas de limite.
- [x] Étape 8 bis : NON (l'allié entre en jeu par le chemin normal).

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz006 : "Doll"

- [x] Étape 2 : `27006` Web Binding.
- [x] Étape 5 : « the **villain** would activate **against you** » : la
      fabrique n'a aucun filtre de joueur (son `against_you` est commenté) →
      condition `contre_ce_joueur` ajoutée (corrigé). « your identity » : conforme.
- [x] Étape 6 : coût 2, B : conforme.
- [x] Étape 7 : 4 cas (vilain contre le joueur annulé ; sbire non annulé ;
      vilain contre un autre joueur non annulé ; Showtime! Tough).
      Substitution 2/4 (deux contre-cas d'absence) ; mutation sans la
      condition → rouge.
- [x] Étape 8 bis : NON.

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz007 : "Hush Now Baby"

- [x] Étape 2 : `04036` Pheromones (même texte, carte officielle).
- [x] Étape 5 : « stun **and** confuse an enemy » : la cible exigeait
      `canbe_stunned` (un ennemi déjà étourdi était exclu) →
      `canbe_status=["Stunned", "Confused"]` comme 04036 (corrigé).
      « **Each** player draws 1 » : conforme.
- [x] Étape 6 : coût 3, Y : conforme.
- [x] Étape 7 : 3 cas (Rhino ; ennemi déjà étourdi ; chaque joueur pioche,
      partie à deux). Substitution 3/3.
- [x] Étape 8 bis : NON.

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz008 : "In the Darkest Light"

- [x] Étape 5 : « each enemy », « non-ELITE » : conformes.
- [x] Étape 6 : coût 2, B, 2 dégâts : conformes.
- [x] Étape 7 : 3 cas (chaque ennemi ; Showtime! sur un sbire choisi ; ELITE
      exclu). Substitution 3/3.

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz009 : "Out and Proud"

- [x] Étape 2 : `44016` (Defeat a non-ELITE minion).
- [x] Étape 5 : « non-ELITE minion », « each ally in play » : conformes.
- [x] Étape 6 : coût 3, Y, 1 : conformes.
- [x] Étape 7 : 4 cas (sbire vaincu ; ELITE seul → injouable ; témoin
      jouable ; Showtime! chaque allié). Substitution 3/4 (contre-cas ELITE).

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz010 : "Rich Angel"

- [x] Étape 2 : `03005` Shield Block (`is_from_attack=True`).
- [x] Étape 5 : « when **you** would take [...] from an **attack** », « an
      identity » : conformes.
- [x] Étape 6 : coût 1, Y, 2 : conformes.
- [x] Étape 7 : 4 cas (attaque prévenue ; dégâts hors attaque non prévenus ;
      Showtime! soigne ; identité d'un autre joueur en forme héros).
      Substitution 3/4 (contre-cas hors attaque).
- ⚠ Observation moteur, non tranchée : l'**alter ego** d'un autre joueur
  (Peter Parker) n'apparaît pas parmi les cibles légales du Showtime!
  (`Identity` comme `Friend`) ; en forme héros, si. Cause non trouvée
  (sélecteur), à creuser à part : elle touche toute carte « an identity ».

Carte terminée : OUI pour le texte ; réserve multijoueur ci-dessus.

### dz011 : "The Serpent is Coming"

- [x] Étape 5 : « This attack gains **ranged** » : `AttackProperty(ranged=True)`.
- [x] Étape 6 : coût 3, Y, 6 et 2 : conformes.
- [x] Étape 7 : 3 cas (6 dégâts ; Riposte ignorée — Tracksuit Mafioso
      60202, Tough consommée ; Showtime! 2). Substitution 3/3 ; mutation
      `ranged=False` → rouge (2 dégâts de riposte).

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz012 : "Too Good to be True"

- [x] Étape 5 : « Draw 3. Choose and discard 1 » : conforme. Showtime!
      « Shuffle 3 cards from your discard pile » : **qui choisit ?** → Q1.
- [x] Étape 6 : coût 1, B, 3/1/3 : conformes.
- [x] Étape 7 : 2 cas (pioche/défausse ; défausse de 3 exactement). 2/2.

Carte terminée : NON — question Q1 (choix des 3 cartes du Showtime!).

### dz013 : "Velvet Sky"

- [x] Étape 2 : `09007` Protective Ward (même phrase), `RetirerUneCarteDeStatut`
      (pack donatello) pour le choix du statut.
- [x] Étape 5 : « a **friendly** character » → `Friend` (corrigé) ; « a status
      card » : l'ancien helper ne connaissait que Stunned/Confused/Tough et
      choisissait à la place du joueur → toutes les cartes d'état, choix du
      joueur (corrigé, `RetirerUnStatut`, partagé avec dz028).
- [x] Étape 6 : coût 1, Y : conforme.
- [x] Étape 7 : 5 cas (traîtrise annulée ; statut retiré ; personnage d'un
      autre joueur ; choix entre deux statuts ; carte Dazed). 5/5.

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz014 : * Lightbringr

- [x] Étape 2 : `53021` Resource Reserve.
- [x] Étape 5 : « Events attached », « played this way by 1 », « facedown »,
      « (to a maximum of 3) », « Alter-Ego Action » : conformes.
- [x] Étape 6 : coût 1, Y, 1, 3 : conformes.
- [x] Étape 7 : 5 cas (glisser face cachée ; plafond 3 ; non-SONG refusé ;
      jouer dessous avec réduction ; témoin depuis la main). Clé de harnais
      ajoutée : `jouer_sous`. Substitution 2/5 (trois contre-cas d'absence) ;
      mutation réduction 0 → rouge.
- [ ] Étape 8 bis : OUI (cartes glissées face cachée sous un soutien) : voir
      fin de fichier.

Carte terminée : voir étape 8 bis.

### dz015 : Dazzler's Rollerskates

- [x] Étape 5 : « Exhaust [...] → ready Dazzler », Hero Action : conformes.
- [x] Étape 6 : coût 2, Y : conforme.
- [x] Étape 7 : 4 cas (jouée ; redresse ; inclinée = pas d'action ; pas en
      alter ego). Substitution 1/4 (jeu depuis la main = valeur native ; deux
      absences).

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz016 : Sound Collector Suit

- [x] Étape 2 : `58008` Jet Belt (ressource bornée à un type de carte).
- [x] Étape 5 : « Dazzler gets +1 DEF » codé « You » (identité) : sans effet
      observable (l'alter ego n'a pas de DEF). « Resource: [...] **or** remove
      1 sound counter » : fenêtre de la seconde branche → Q2.
- [x] Étape 6 : coût 2, Y, +1 : conformes.
- [x] Étape 7 : 3 cas + 1 historique (+1 DEF). Substitution 3/4.

Carte terminée : NON — question Q2.

### dz017a : Live Concert

- [x] Étape 5 : « After you resolve a SONG **event** », « (to a maximum of
      4) », « Hero Action: Flip [...] and reveal it » : conformes.
- [x] Étape 7 : 4 cas + Setup historique. Substitution 2/5 (absences, Setup
      porté par dz001b).
- [ ] Étape 8 bis : OUI (Setlist posée face visible) : voir fin de fichier.

Carte terminée : voir étape 8 bis.

### dz017b : Showtime!

- [x] Étape 5 : « in **any order** » : l'ordre était imposé → choix du joueur
      (corrigé). « discard all cards from the Setlist » : les compteurs sound
      restaient sur les chansons défaussées (`OublierLaSetlist` jamais
      appelé) → corrigé. « If 4 cards », « you may either » : conformes.
- [x] Étape 6 : 4, 4, 4 : conformes.
- [x] Étape 7 : 6 cas. Substitution 6/6.

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz018 : Sound Absorption

- [x] Étape 5 : « After you **spend** this card » : conforme.
- [x] Étape 6 : YY (planche des coins), 2 compteurs : conformes.
- [x] Étape 7 : 2 cas. Substitution 1/2 (témoin).
- Note : le scan est numéroté « 12/16 » comme Velvet Sky, et la carte
  n'est pas dans le deck de départ `deck/starter/dazzler.json`.

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz019 : Performance Anxiety

- [x] Étape 2 : `rg012` Caged Bird.
- [x] Étape 5 : « You **may** flip », les deux interdits, « Exhaust your
      identity **and** discard a support or upgrade » : conformes.
- [x] Étape 6 : Boost 2 (scan) : conforme.
- [x] Étape 7 : 7 cas. Substitution 4/7 (témoin ; interdits portés par
      dz001b et dz017a).

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz020 : * Klaw (némésis)

- [x] Étape 2 : `01118` Sonic Converter.
- [x] Étape 5 : « attacks **and damages** » : conforme.
- [x] Étape 6 : SCH 2, ATK 1, PV 6, Boost 3, ELITE : conformes.
- [x] Étape 7 : 2 cas. Substitution 1/2 (absence).

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz021 : Solid Sound Body (némésis)

- [x] Étape 5 : « Klaw gets +10 », « When Defeated: Give Klaw » : quel
      Klaw contre le scénario Klaw → Q3.
- [x] Étape 6 : menace 4, Hinder 1 par héros, Boost 2, **Amplify** (icône
      imprimée, absente de `desc` → corrigé, checksum recalculé).
- [x] Étape 7 : 3 cas. Substitution 2/3 (le cas de données reste vert) ;
      mutation de données (Amplify retiré) → rouge.

Carte terminée : NON — question Q3.

### dz022 : Stealing Sound (némésis)

- [x] Étape 5 : « **Dazzler's** Setlist » : le module lisait le joueur qui
      révèle et ne tombait juste que parce que `Concert` ignorait son filtre
      → `JoueurDeDazzler` (corrigé) ; le filtre de `Concert` / `AngoisseEnJeu`
      (passé en `check_effect_fn` à `FindCardOnField`, jamais appelé) est
      désormais fait à la main.
- [x] Étape 7 : 4 cas. Substitution 4/4 ; mutation → rouge.

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz023 : Taunting Light (némésis)

- [x] Étape 5 : « If you are Dazzler » = nom de la forme en cours (précédents
      officiels 01015, 10025) ; « If **no attack was made** » : un vilain
      étourdi n'attaque pas → `if_no_attack_was_made` (corrigé).
- [x] Étape 7 : 3 cas. Substitution 3/3.

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz024 à dz027 : Song of Aggression / Justice / Leadership / Protection

- [x] Étape 5 : « for each SONG card in your discard pile (to a maximum of
      4) » : conforme ; dz026 « Exhaust an ally » = allié contrôlé (Rules
      Reference v1.8, COST) ; dz027 « a **friendly** character » :
      `YouControlCharacter` → `Friend` (corrigé).
- [x] Étape 6 : coûts 1, ressources Y / R / R / B, plafond 4 : conformes.
- [x] Étape 7 : dz024 2/2, dz025 2/2, dz026 2/3 (injouable = absence),
      dz027 2/2 (dont le cas à deux joueurs, rouge avant correction).

Cartes terminées : OUI (sous réserve de l'autoplay commun).

### dz028 : "Doom and Gloom" ; dz029 : Love Song ; dz030 : Power Ballad

- [x] Étape 5 : « **Choose**: » est obligatoire : `MayChooseOneAbility`
      offrait « Cancel » → `ChooseAbilities` (corrigé, trois cartes) ;
      « a **friendly** character » → `Friend` (dz028, dz029, corrigé) ;
      dz030 « if your identity is Dazzler [...] » : conforme.
- [x] Étape 6 : coûts 1 / 1 / 3 (−2), X = ennemis avec statut : conformes.
- [x] Étape 7 : dz028 3/3, dz029 3/3, dz030 2/3 (témoin Spider-Man) ;
      mutation dz030 → rouge.

Cartes terminées : OUI (sous réserve de l'autoplay commun).

### dz031 : Tribute

- [x] Étape 5 : « Tribute **becomes a copy** of that card [...] until it is
      placed in the discard pile » : non rendu (le module joue une carte
      fabriquée ; une Response choisie reste en MAIN) → Q4.
- [x] Étape 7 : 1 cas (comportement actuel). 1/1.

Carte terminée : NON — question Q4 (et extension du moteur probable).

### dz032 : Captivating Performance

- [x] Étape 5 : « the next card you play **this turn** » : la promesse
      n'avait aucune durée → `until_turn_end` (corrigé ; `Puzzle.EndPlayerTurn`
      ajouté pour le prouver).
- [x] Étape 7 : 3 cas. Substitution 1/3 (absences) ; mutation → rouge.

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz033 : Duet

- [x] Étape 5 : « ready **your hero** and **another friendly** character » :
      `YouControlUnit` → `Friend`, minimum dynamique, alter ego non redressé
      au titre de « your hero » ; le filtre « pas ton héros » passait par
      `check_fn`, que le sélecteur ne transmet pas → `check_effect_fn` (corrigé).
- [x] Étape 7 : 2 cas. 2/2 ; mutation → rouge.

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz034 : Encore

- [x] Étape 5 : « Search your discard pile for a SONG card » : conforme.
- [x] Étape 7 : 2 cas. 1/2 (absence).

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz035 : * Karaoke Night

- [x] Étape 5 : « choose a SONG in the Setlist → resolve the 'Hero Action' » :
      la cible de la Hero Action était prise d'office par le moteur → choix du
      joueur (corrigé). Coût avant la flèche d'une Hero Action résolue → Q5.
- [x] Étape 7 : 3 cas. 2/3 (absence).

Carte terminée : NON — question Q5.

### dz036 : * DJ

- [x] Étape 5 : « for each SONG card used to pay », « a scheme », « an
      enemy » : manigance et ennemi pris d'office → choix du joueur (corrigé).
- [x] Étape 6 : coût 3, Y, PV 2, ATK 1*, THW 1* : conformes.
- [x] Étape 7 : 3 cas. 2/3 (témoin sans SONG).

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz037 : Coolest Team-Up Ever!

- [x] Étape 5 : Team-Up (fiche `teamup.md`), « cancel its When Revealed »,
      « up to 2 » : conformes.
- [x] Étape 7 : 2 cas (partie à deux avec Jubilee ; sans Jubilee). 1/2.

Carte terminée : OUI (sous réserve de l'autoplay commun).

### dz038 : Love from Beyond the Stars

- [x] Étape 5 : « Choose: » → `ChooseAbilities` (corrigé) ; « Then » : conforme.
- [x] Étape 7 : 2 cas. 1/2 (injouable sans Longshot).

Carte terminée : OUI (sous réserve de l'autoplay commun).

---

## Étape 8 : autoplay ciblé (commun au lot), 20/10/2026

`tools/autoplay.py .game-src --deck <deck> --vilains rhino --parties 8`
(profil équilibré, graines 1 à 8). Grep `NameError|AttributeError|TypeError|
KeyError|AssertionError|Traceback` sur chaque `/tmp/autoplay_<deck>_rhino_*.log`.

| Deck | Parties | Victoires | Défaites | Bloquées | Erreurs Python | Cartes du lot vues |
|---|---|---|---|---|---|---|
| dazzler (1er passage) | 8 | 0 | 2 | **6** | 0 | — |
| dazzler (après correctif dz017a) | 8 | 0 | 8 | 0 | 0 | Live Concert 65, Showtime! 31, Rehearsal 23, Power Ballad 12, Too Good 10, Serpent 7, Hush 7, Rich Angel 6, Beauty 4, Lightbringr 3, Dreamer 3, Performance Anxiety 2, Darkest Light 2, Song of Justice 1, Rollerskates 1 |
| spider_man (témoin) | 8 | 0 | 8 | 0 | 0 | — |
| iron_man_model_42 (im001b) | 8 | 0 | 7 | 1 | 0 | Inventor 25 activations |
| wiccan (wc014) | 8 | 0 | 8 | 0 | 0 | wc014 seulement dépensée comme ressource, jamais jouée |

- **Défaut trouvé par l'autoplay, corrigé** : les 6 blocages du premier
  passage venaient tous de la Hero Action de Live Concert (`dz017a`) offerte
  avec une Setlist VIDE : retourner, ne rien résoudre, retourner encore ne
  change rien, et le pilote la reprenait sans fin. Condition « Setlist non
  vide » ajoutée (même garde que Rehearsal et Karaoke Night). Second passage :
  0 blocage, même profil que le témoin.
- Blocage Iron Man (graine 7) : « Remove 1 threat from a scheme » offert sur
  le complot principal sous Crise (Crowd Control) ; sans lien avec `im001b`
  (réduction de coût), hors périmètre, signalé.
- Non vues en autoplay (absentes du deck de départ ou du set némésis, qui
  n'entre pas contre Rhino sans avancer) : dz006, dz009, dz013, dz016,
  dz018, dz020-dz024, dz026-dz029, dz031-dz038 ; wc014 n'a jamais été jouée.
  Pour elles, seule la preuve du harnais vaut.
- Aucune vraie partie jouée à la main dans le navigateur : non fait.

## Étape 8 bis : ce que le plateau dessine (dz014, dz017a)

- Côté moteur : vérificateur `dz_rendu` (`ToDescriptor.Player`), cas
  « dz017a Live Concert : rendu » (la chanson est émise dans `area_hero`, liée
  à Live Concert, face visible) et « dz014 Lightbringr : rendu » (émise dans
  `supports`, liée à Lightbringr, face cachée) : verts.
- Côté plateau : `ui-app/src/board/dazzler-setlist-lightbringr.test.ts`
  (5 cas, verts). Calibré : avec un `bind_object_id` orphelin, les deux cas
  « portée par » tombent au rouge (2 échecs sur 5). Pas de correctif ici,
  donc pas de rouge « avant correctif » au sens strict.
- Limite connue, inchangée : le compteur `sound` d'une chanson de la Setlist
  n'a pas de badge à l'écran (`dazzler/__init__.py`, zone hors jeu).

## Bilan

- Carte terminée : **OUI** pour dz004 à dz011, dz013, dz014, dz015, dz017a,
  dz017b, dz018, dz019, dz020, dz022 à dz030, dz032 à dz034, dz036 à dz038,
  im001b, wc014 (wc014 : Action jamais jouée par le pilote, preuve du harnais
  seulement ; dz010 : réserve multijoueur sur l'alter ego d'un autre joueur).
- Carte terminée : **NON** pour dz012 (Q1), dz016 (Q2), dz021 (Q3), dz031
  (Q4, extension du moteur probable), dz035 (Q5).
