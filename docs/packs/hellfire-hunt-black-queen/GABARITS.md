# Hellfire Hunt, scénario 3 « Black Queen » + module Darkhold : gabarits PROCESSUS-CARTE

Généré par `generer_gabarits.py` à partir du dernier rapport de `test_capacites` (`/tmp/cas_hfq_A.json,/tmp/cas_hfq_B.json`) et de `SUBSTITUTION.txt` : les cas et les verdicts ne sont pas saisis à la main.

Pack `hellfire_hunt_black_queen` (set 243), module plat `src/cards/pack/hellfire_hunt_black_queen/`. Scénarios `hellfire_black_queen` (Selene I puis II) et `hellfire_black_queen_expert` (II puis III). Cas : `tools/cas/hellfire_black_queen.py`. Doutes de règle : `QUESTIONS.md`.

**Statut commun à TOUTES les cartes : « Carte terminée : NON : partie humaine à faire »** (aucune partie jouée par un humain dans le navigateur ; le reste est fait et prouvé ci-dessous).

### hf361 : Darkhold Dwarf

- [x] Étape 2 : cartes de référence : mots-cles/tuck.md (`PlaceCardHere(faces, True)` face visible, helper `Glisser` de gs119), `Deck.FindTopmost`
      Capacités : When Revealed : glisse sous lui le Spell of Darkhold du dessus de la defausse ; When Defeated : revele la carte glissee
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « topmost » ; tuck = FACE VISIBLE (livret p.4) ; « the card tucked here » : la revelation passe par le joueur engage ; piege de harnais : `CreateEncounterDiscardPile` AVANT `EmptyEncounterDeck` est remelangee dans le deck
- [x] Étape 6 : nombres texte ↔ code : PV 3, ATK 1, SCH 3, 2 icones de boost (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 4 cas, 4 verts avec le module.
      - OK  [hf] hf361 Darkhold Dwarf revele : glisse sous lui le Spell of Darkhold du DESSUS de la defausse (Soul Siphon, pose en dernier)
      - OK  [hf] hf361 Darkhold Dwarf revele : ordre inverse (Hellfire Conjuration au-dessus) -> c'est elle qui est glissee
      - OK  [hf] hf361 Darkhold Dwarf revele SANS Spell of Darkhold dans la defausse : rien n'est glisse
      - OK  [hf] hf361 Darkhold Dwarf vaincu : « Reveal the card tucked here » (Hellfire Conjuration, Darkhold sur le vilain : 3 degats indirects)
      Substitution (module remplacé par `GetAbilities -> []`) : hf361 : rouges 3/4   restent VERTS : 1
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : bloc plateau (sort glisse sous le sbire)

Carte terminée : NON : partie humaine à faire.

### hf362 : Darkhold

- [x] Étape 2 : cartes de référence : gs183 Induced Mutation (`AttachToFaceWhenPutIntoPlay(Villain)`, `GiveAdditionalBoostCardForThisActivation`), 02020 Hysteria (`WhenUnitWouldAttack`), fiche uses.md
      Capacités : Attache au vilain, +1 ATK, Uses (2 Darkspell) ; Interruption forcee : le vilain ATTAQUE -> -1 compteur et 1 carte de boost de plus
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « attacks » (pas un complot) ; le dernier compteur fait partir la carte AVEC son +1 ATK ; +1★ ATK (QUESTIONS.md n°4)
- [x] Étape 6 : nombres texte ↔ code : +1 ATK, 2 compteurs darkspell, 3 icones de boost (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 5 cas, 5 verts avec le module.
      - OK  [hf] hf362 Darkhold revele : s'attache au vilain, +1 ATK (Selene 2), 2 compteurs darkspell
      - OK  [hf] hf362 Interruption forcee : Selene ATTAQUE -> -1 compteur darkspell et 1 carte de boost de plus (nuit + Darkhold = 3 cartes de 2 icones : 2 + 6 = 8 degats)
      - OK  [hf] hf362 Uses : le DERNIER compteur retire fait quitter le Darkhold
      - OK  [hf] hf362 TEMOIN : une MANIGANCE de Selene ne consomme pas de compteur
      - OK  [hf] hf362 Uses : TEMOIN D'EPUISEMENT, DEUX attaques de Selene (2 compteurs) -> le Darkhold quitte le jeu a la 2e ; ATK 2 (avec le livre) puis 1 (sans) = 3 degats
      Substitution (module remplacé par `GetAbilities -> []`) : hf362 : rouges 5/5
- [x] Étape 7 bis : limite imprimée ? OUI : Uses (2) -> temoin d'epuisement
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : bloc plateau

Carte terminée : NON : partie humaine à faire.

### hf363 : Eternal Manipulation

- [x] Étape 2 : cartes de référence : hf324 Mind Manipulation (MEME texte : `TreatAttachedCardAsMinion(Ally, "Minion")`), hp017 Take Over Signal
      Capacités : Allie attache traite comme un sbire (texte vierge, SCH = THW imprime, pas de degats consecutifs) ; When Revealed : Darkhold sur le vilain -> s'attache a l'allie aux PV les plus hauts, -1 Darkspell ; sinon cherche Darkhold
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « highest hit-point » (QUESTIONS.md n°5) ; l'attachement est alors porte par la face `minion` (pic_id = l'allie) ; ⚠ Luke Cage (Tough) fausse la mesure des PV
- [x] Étape 6 : nombres texte ↔ code : +1 ATK, 1 icone de boost (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 2 cas, 2 verts avec le module.
      - OK  [hf] hf363 Eternal Manipulation, Darkhold sur le vilain : s'attache a l'allie qui a le plus de PV restants (Mockingbird), -1 darkspell ; l'allie devient un sbire (SCH = son THW imprime 1, ATK +1)
      - OK  [hf] hf363 Eternal Manipulation, SANS Darkhold sur le vilain : le Darkhold est cherche et revele (il s'attache a Selene), l'allie n'est pas touche
      Substitution (module remplacé par `GetAbilities -> []`) : hf363 : rouges 2/2
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : bloc plateau

Carte terminée : NON : partie humaine à faire.

### hf364 : Hellfire Conjuration

- [x] Étape 2 : cartes de référence : 27080 (`TakeIndirectDamage`), `ResolutionDeSort`
      Capacités : When Revealed : Darkhold sur le vilain -> 3 degats indirects, -1 Darkspell ; sinon cherche Darkhold
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « take 3 indirect damages » : le joueur qui revele
- [x] Étape 6 : nombres texte ↔ code : 3 degats indirects, 1 icone de boost (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 3 cas, 3 verts avec le module.
      - OK  [hf] hf364 Hellfire Conjuration, Darkhold sur le vilain : 3 degats indirects au joueur (heros seul : 3) et -1 darkspell
      - OK  [hf] hf364 Hellfire Conjuration, SANS Darkhold : il est cherche et revele (aucun degat)
      - OK  [hf] hf364 Hellfire Conjuration : le Darkhold est cherche aussi dans la DEFAUSSE de rencontre
      Substitution (module remplacé par `GetAbilities -> []`) : hf364 : rouges 3/3
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.

### hf365 : Soul Siphon

- [x] Étape 2 : cartes de référence : hf110 (`RevealThisCard`), 41029 (`GiveStatus`)
      Capacités : When Revealed : Darkhold sur le vilain -> sonne ET desoriente, -1 Darkspell ; sinon cherche Darkhold ; Boost : reveler cette carte
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : les DEUX statuts ; boost = revelation
- [x] Étape 6 : nombres texte ↔ code : etoile seule (pas d'icone numerique) (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 3 cas, 3 verts avec le module.
      - OK  [hf] hf365 Soul Siphon, Darkhold sur le vilain : le joueur est etourdi ET desoriente, -1 darkspell
      - OK  [hf] hf365 Soul Siphon, SANS Darkhold : il est cherche et revele, aucun statut
      - OK  [hf] hf365 Boost : Selene active avec Soul Siphon en boost -> la carte est revelee (Darkhold cherche et attache)
      Substitution (module remplacé par `GetAbilities -> []`) : hf365 : rouges 3/3
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.

### hf366 : Dimensional Portal

- [x] Étape 2 : cartes de référence : trors/zola (`DiscardEncounterCardsUntil(card_type=Minion)`)
      Capacités : When Revealed : Darkhold sur le vilain -> defausse jusqu'a un sbire, le revele, -1 Darkspell ; sinon cherche Darkhold
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : le sbire est REVELE (s'engage, resout son When Revealed)
- [x] Étape 6 : nombres texte ↔ code : 2 icones de boost (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 2 cas, 2 verts avec le module.
      - OK  [hf] hf366 Dimensional Portal, Darkhold sur le vilain : defausse jusqu'a un sbire (2 cartes defaussees), le REVELE (Little Demon en jeu), -1 darkspell
      - OK  [hf] hf366 Dimensional Portal, SANS Darkhold : il est cherche et revele (rien n'est defausse)
      Substitution (module remplacé par `GetAbilities -> []`) : hf366 : rouges 2/2
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.

### hf401 : Selene (I)

- [x] Étape 2 : cartes de référence : 01113 Klaw (`AfterUnitAttackEnd(..., "This")` en Reponse forcee) ; `AfterUnitAttackUnit.taken_damage / excess_damage` (can_attack.py)
      Capacités : Reponse forcee : vol de vie
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « non-excess » (l'exces ne vit que dans `AfterUnitAttackUnit.excess_damage`) ; « the defending player controlled » (la cible est controlee par le joueur ATTAQUE, un allie qui defend compte) ; « After Selene attacks » (pas une manigance) ; « heal damage from her » (borne par ses degats)
- [x] Étape 6 : nombres texte ↔ code : PV 12 par joueur, ATK 1, SCH 2 (desc) (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 4 cas, 4 verts avec le module.
      - OK  [hf] hf401 Reponse forcee : Selene (3 degats) attaque le heros incline (1 degat non excedentaire) -> elle se soigne de 1 (3 -> 2)
      - OK  [hf] hf401 Reponse forcee : TEMOIN, le heros DEFEND (0 degat) -> Selene ne se soigne pas
      - OK  [hf] hf401 Reponse forcee : l'EXCES n'est pas soigne (Black Cat 2 PV defend, subit 5 : 2 non excedentaires -> Selene 4 -> 2 degats)
      - OK  [hf] hf401 Reponse forcee : TEMOIN, sa manigance (alter-ego) ne la soigne pas
      Substitution (module remplacé par `GetAbilities -> []`) : hf401 : rouges 2/4   restent VERTS : 2
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON (aucune carte dessinee de plus)

Carte terminée : NON : partie humaine à faire.

### hf402 : Selene (II)

- [x] Étape 2 : cartes de référence : hf401 ; fiche mots-cles/toughness.md (base automatique, aucun script)
      Capacités : Toughness (natif, desc) ; Reponse forcee : vol de vie (meme fabrique que hf401)
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : Toughness est lu dans `desc` : ne jamais le recoder
- [x] Étape 6 : nombres texte ↔ code : PV 14 par joueur, ATK 2, SCH 2, Toughness 1 (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 2 cas, 2 verts avec le module.
      - OK  [hf] hf402 EXPERT : Selene (II) vaincue -> Selene (III), PV 17, Steady, Toughness ; ses attachements ne sont pas necessaires a la mesure
      - OK  [hf] hf402 Reponse forcee (EXPERT, Selene II) : elle se soigne des degats non excedentaires (3 degats, 2 de plus au heros incline : 3 -> 1)
      Substitution (module remplacé par `GetAbilities -> []`) : hf402 : rouges 1/2   restent VERTS : 1
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.

### hf403 : Selene (III)

- [x] Étape 2 : cartes de référence : hf401 ; fiches steady.md, toughness.md
      Capacités : Steady + Toughness (natifs, desc) ; Reponse forcee : vol de vie
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : Steady et Toughness lus dans `desc`
- [x] Étape 6 : nombres texte ↔ code : PV 17 par joueur, ATK 3, SCH 2, Steady 1, Toughness 1 (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 2 cas, 2 verts avec le module.
      - OK  [hf] hf403 stade III (expert) : PV 17, ATK 3, Steady + Toughness (carte Tough)
      - OK  [hf] hf403 Reponse forcee (EXPERT, Selene III) : meme vol de vie (ATK 3 : 3 degats au heros incline, 5 -> 2)
      Substitution (module remplacé par `GetAbilities -> []`) : hf403 : rouges 1/2   restent VERTS : 1
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.

### hf404a : Throne of the Hellfire Club (1A)

- [x] Étape 2 : cartes de référence : 50087a (Batroc : `SetupCards.PutIntoPlay` d'un environnement `set_aside`, `*CampaignSetup(n)`), skrull_menace/shaper_of_worlds (`Faces.SetAside` d'un set par `paper.set_name`)
      Capacités : Setup : la nuit en jeu, module Darkhold de cote sauf le Dwarf ; Campagne : `CampaignSetup(3)`
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « Set the Darkhold module aside » : la zone « mise de cote » contient AUSSI les allies Recruited de campagne, d'ou le filtre par `paper.set_name` ; « Shuffle the set-aside Darkhold Dwarf » : le Dwarf reste dans le deck (le deck est melange apres la mise en place)
- [x] Étape 6 : nombres texte ↔ code : environnement : 3 compteurs time par joueur ; complot 1B : menace 1 par joueur (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 2 cas, 2 verts avec le module.
      - OK  [hf] hf404a mise en place : Selene I, Throne of the Hellfire Club (menace 1), la NUIT en jeu avec 3 compteurs, Darkhold mis de cote sauf le Dwarf
      - OK  [hf] hf404a mise en place EXPERT : Selene II (PV 14, ATK 2, Toughness) puis la meme installation
      Substitution (module remplacé par `GetAbilities -> []`) : hf404a : rouges 2/2
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : bloc plateau (environnement a compteurs time)

Carte terminée : NON : partie humaine à faire.

### hf404b : Throne of the Hellfire Club (1B)

- [x] Étape 2 : cartes de référence : sk066 Paibok (`WhenCardWouldMoveToArea ... into_discard_pile`), 50087b (`Advance("2A")`), hf104b (`WhenMainSchemeStageCompleted`)
      Capacités : Interruption forcee : le Dwarf entre dans la defausse -> stade 2A ; When Completed : Tough sur Selene ; -2 compteurs du jour
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « enters the discard pile » = toute route (vaincu ou defausse du deck), pas seulement « defeated » ; « 2[per_hero] time counters » = 2 par joueur
- [x] Étape 6 : nombres texte ↔ code : cible 5 par joueur, escalade 2 par joueur, depart 1 par joueur (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 5 cas, 5 verts avec le module.
      - OK  [hf] hf404b Interruption forcee : le Darkhold Dwarf est vaincu (va a la defausse) -> avance au stade 2 ; hf405a melange le module Darkhold au deck
      - OK  [hf] hf404b Interruption forcee : TEMOIN, un AUTRE sbire defausse (Little Demon) -> le stade 1 reste
      - OK  [hf] hf404b When Completed (la NUIT) : Selene recoit une carte Tough ; les compteurs de la nuit ne bougent pas
      - OK  [hf] hf404b When Completed (le JOUR) : Selene recoit une carte Tough ET le jour perd 2 compteurs par joueur (3 -> 1)
      - OK  [hf] hf404b Interruption forcee : le Darkhold Dwarf est defausse du DESSUS du deck de rencontre (pas vaincu) -> le complot avance quand meme
      Substitution (module remplacé par `GetAbilities -> []`) : hf404b : rouges 4/5   restent VERTS : 1
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.

### hf405a : The Power of the Darkhold (2A)

- [x] Étape 2 : cartes de référence : skrull_menace/shaper_of_worlds (`Worlds.GetSetAsideAreaCards`) + `Faces.ShuffleAllTo`
      Capacités : When Revealed : melanger le set Darkhold mis de cote dans le deck
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : filtre par nom de set (zone mise de cote partagee avec les allies de campagne)
- [x] Étape 6 : nombres texte ↔ code : - (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 1 cas, 1 verts avec le module.
      - OK  [hf] hf405a When Revealed : le module Darkhold mis de cote est melange au deck de rencontre (le complot avance au stade 2)
      Substitution (module remplacé par `GetAbilities -> []`) : hf405a : rouges 1/1
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.

### hf405b : Get the Power (2B)

- [x] Étape 2 : cartes de référence : hf105b (`WhenMainSchemeStageCompleted`), 04119 (chercher puis attacher), mots-cles/find.md
      Capacités : When Completed : Tough sur Selene ; trouver Darkhold et l'attacher a Selene
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « find » : deck, defausse, mis de cote ET deja en jeu (s'il est deja attache a Selene : rien) ; « attach it to Selene » (pas au premier vilain venu)
- [x] Étape 6 : nombres texte ↔ code : cible 7 par joueur, escalade 1 par joueur, depart 2 par joueur (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 2 cas, 2 verts avec le module.
      - OK  [hf] hf405b When Completed : Selene recoit une carte Tough et le Darkhold est cherche puis ATTACHE a Selene
      - OK  [hf] hf405b When Completed : le Darkhold est DEJA attache a Selene (revele pendant le stade 2) -> il y reste, un seul exemplaire, la carte Tough est donnee
      Substitution (module remplacé par `GetAbilities -> []`) : hf405b : rouges 2/2
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.

### hf406a : Ascending to Godhood (3A)

- [x] Étape 2 : cartes de référence : hf105a / hf106a (`Search.EncounterCard` + `Reveal`), 04112b (`PutIntoPlay(first_player)`)
      Capacités : When Revealed : trouver et reveler Immortal Moon Goddess ; trouver Blackheart et le mettre en jeu engage avec le premier joueur
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « engaged with the first player » ; « (Shuffle.) » fait par `Search`
- [x] Étape 6 : nombres texte ↔ code : - (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 1 cas, 1 verts avec le module.
      - OK  [hf] hf406a When Revealed : Immortal Moon Goddess est cherchee et revelee, Blackheart mis en jeu engage avec le premier joueur
      Substitution (module remplacé par `GetAbilities -> []`) : hf406a : rouges 1/1
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.

### hf406b : Ascending to Godhood (3B)

- [x] Étape 2 : cartes de référence : trors/zola `TheMadDoctor` (`AfterResolveVillainPhaseStep(ForcedResponse, 1)`), hf106b (defaite lue dans le texte)
      Capacités : Reponse forcee : apres l'etape 1, 1 menace par compteur time ; Si cette etape est completee, les joueurs perdent (texte lu par le moteur)
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « for each time counter on Under the Moonlight OR Beneath the Sun » : la face VISIBLE ; l'escalade imprimee (+2 par joueur) reste (QUESTIONS.md n°3) ; l'icone d'acceleration d'Immortal Moon Goddess s'y ajoute
- [x] Étape 6 : nombres texte ↔ code : cible 17 par joueur, escalade 2 par joueur, depart 0 (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 2 cas, 2 verts avec le module.
      - OK  [hf] hf406b Reponse forcee : apres l'etape 1 de la phase du mechant, 1 menace par compteur time (3) + l'escalade imprimee (2) + la manigance de Selene a l'etape 3 (2) = 7
      - OK  [hf] hf406b Reponse forcee : le JOUR visible avec 1 compteur -> 1 + escalade 2 + manigance 2 = 5 menaces
      Substitution (module remplacé par `GetAbilities -> []`) : hf406b : rouges 2/2
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.

### hf407a : Under the Moonlight (la nuit)

- [x] Étape 2 : cartes de référence : gs183 (`WhenEnemyActivateAgainstYou` + `GiveAdditionalBoostCardForThisActivation`), 50090a Alert Level / 39026a (`card.Flip`), `AfterUnitUseBasicPower`, `AfterEnemyActivationEnd`, `IfThereIsNoCounterHere`
      Capacités : Entre en jeu avec 3 compteurs time par joueur ; sans compteur : se retourne ; Interruption forcee : Selene s'active -> 1 carte de boost de plus ; Reponse forcee : pouvoir de base d'un personnage ami ou activation ennemie -> -1 compteur
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « enters play with » rejoue a CHAQUE retournement (`AfterCardFlipToThisSide`) ; ⚠ vider la carte pour la remplir declenche le retournement a l'infini (RecursionError) : on ajuste par la difference ; « Black Queen » = Selene ; « character uses a basic power » (RR 1.8 : ATK THW DEF REC SCH) et « enemy activates » (QUESTIONS.md n°2) ; Eternal Night bloque le retrait sur la nuit
- [x] Étape 6 : nombres texte ↔ code : 3 par joueur ; -1 par evenement ; +1 carte de boost (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 11 cas, 11 verts avec le module.
      - OK  [hf] hf407a entre en jeu avec 3 compteurs time PAR JOUEUR : deux joueurs -> 6
      - OK  [hf] hf407a Reponse forcee : un ennemi s'active (Selene attaque) -> 1 compteur retire (3 -> 2)
      - OK  [hf] hf407a Reponse forcee : un personnage ami utilise un pouvoir de base (le heros attaque) -> 1 compteur retire (3 -> 2)
      - OK  [hf] hf407a Reponse forcee : le heros THWART la manigance -> 1 compteur retire
      - OK  [hf] hf407a Reponse forcee : l'alter-ego RECUPERE (pouvoir de base REC) -> 1 compteur retire
      - OK  [hf] hf407a Reponse forcee : le heros DEFEND contre Selene -> 2 compteurs retires (la defense + l'activation de Selene : 3 -> 1)
      - OK  [hf] hf407a Reponse forcee : TEMOIN, rien ne se passe -> 3 compteurs
      - OK  [hf] hf407a sans compteur : l'environnement se RETOURNE (Beneath the Sun, hf407b) et entre en jeu avec 3 compteurs
      - OK  [hf] hf407a Interruption forcee : la NUIT donne 1 carte de boost de plus a Selene (2 cartes de 2 icones : 1 + 4 = 5 degats)
      - OK  [hf] hf407a TEMOIN : la nuit, l'attaque du heros reste a 2
      - OK  [hf] hf407a Reponse forcee : un ALLIE (Luke Cage) attaque Selene -> 1 compteur retire (3 -> 2)
      Substitution (module remplacé par `GetAbilities -> []`) : hf407a : rouges 10/11   restent VERTS : 1
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « Limit ... » imprimee)
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : bloc plateau (compteurs time, face visible)

Carte terminée : NON : partie humaine à faire.

### hf407b : Beneath the Sun (le jour)

- [x] Étape 2 : cartes de référence : 06007 Asgard (`GiveKeywordToInPlayWhenApplyThis(Identity, ...)`), hf407a
      Capacités : Entre en jeu avec 3 compteurs time par joueur ; sans compteur : se retourne ; +1 a chaque pouvoir de base de chaque identite ; Reponse forcee : -1 compteur (meme montage que hf407a)
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « each identity » = heros ET alter ego ; « each of its basic powers » = ATK, THW, DEF, REC
- [x] Étape 6 : nombres texte ↔ code : +1 ATK/THW/DEF/REC (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 5 cas, 5 verts avec le module.
      - OK  [hf] hf407b sans compteur : il se retourne sur la NUIT (hf407a) avec 3 compteurs
      - OK  [hf] hf407b TEMOIN : le JOUR ne donne PAS de carte de boost de plus (1 carte de 2 icones : 1 + 2 = 3 degats)
      - OK  [hf] hf407b le JOUR : chaque identite a +1 a chaque pouvoir de base (l'attaque du heros passe de 2 a 3)
      - OK  [hf] hf407b le JOUR : le THW du heros passe de 1 a 2
      - OK  [hf] hf407b le JOUR : la RECUPERATION de l'alter-ego gagne +1 (3 -> 4)
      Substitution (module remplacé par `GetAbilities -> []`) : hf407b : rouges 4/5   restent VERTS : 1
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : bloc plateau

Carte terminée : NON : partie humaine à faire.

### hf408 : Blackheart

- [x] Étape 2 : cartes de référence : 27081 Tooth and Nail (`GainPiercing`), 27169 (`GainOverKill`), `GainRanged` (sender_damage.py)
      Capacités : Guard, Patrol, Steady (natifs) ; Boost : l'attaque gagne overkill, piercing, ranged
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « If this activation is an attack » (`during_attack=True`) ; Ranged n'a aucun effet MESURABLE contre un joueur (il ignore Riposte) : l'appel est pose, l'effet n'est pas prouve
- [x] Étape 6 : nombres texte ↔ code : PV 9, ATK 3, SCH 1, 3 icones de boost + etoile (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 5 cas, 5 verts avec le module.
      - OK  [hf] hf408 Boost : l'attaque de Selene gagne PERCANT : la carte Tough du heros est defaussee ET les 4 degats passent (1 + 3 icones)
      - OK  [hf] hf408 Boost : TEMOIN, une carte de boost sans effet (Little Demon, 2 icones) : la carte Tough absorbe TOUTE l'attaque (0 degat)
      - OK  [hf] hf408 Boost : l'attaque gagne OVERKILL : l'allie Black Cat (2 PV) defend, 4 degats -> l'exces (2) passe au heros
      - OK  [hf] hf408 Boost : TEMOIN, sans overkill (Little Demon, 3 degats) : l'exces (1) est perdu, le heros ne subit rien
      - OK  [hf] hf408 Blackheart en jeu : Guard (desc) : le heros ne peut pas attaquer Selene tant qu'il est la
      Substitution (module remplacé par `GetAbilities -> []`) : hf408 : rouges 2/5   restent VERTS : 3
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.

### hf409 : Little Demon (1/4) (+ hf410, hf411, hf412, même script)

- [x] Étape 2 : cartes de référence : hf124 (`AfterUnitAttackAndDamageUnit`), 41029 (`GiveStatus`), fiche teamwork.md
      Capacités : Patrol + Teamwork (DEMON) (natifs) ; Reponse forcee : apres avoir attaque et blesse vous, vous etes desoriente
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « damages YOU » (l'identite, pas un allie) ; ne JAMAIS recoder Teamwork (le sbire s'activerait deux fois)
- [x] Étape 6 : nombres texte ↔ code : PV 3, ATK 2, SCH 1, 2 icones de boost (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 7 cas, 7 verts avec le module.
      - OK  [hf] hf409 Reponse forcee : Little Demon attaque le heros incline (2 degats) -> le heros est desoriente
      - OK  [hf] hf409 Reponse forcee : TEMOIN, l'allie (Luke Cage) DEFEND : les degats vont a l'allie, le heros n'est PAS desoriente
      - OK  [hf] hf409 Teamwork (DEMON, natif) : un 2e Little Demon entre en jeu -> il s'active tout de suite (2 degats au heros incline, desoriente)
      - OK  [hf] hf409 Patrol (natif) : tant que Little Demon est la, le heros ne peut pas attaquer Selene sans Guard... TEMOIN de Patrol : Selene reste attaquable
      - OK  [hf] hf410 Little Demon (illustration 2) : meme Reponse forcee (desoriente apres avoir attaque et blesse)
      - OK  [hf] hf411 Little Demon (illustration 3) : meme Reponse forcee (desoriente apres avoir attaque et blesse)
      - OK  [hf] hf412 Little Demon (illustration 4) : meme Reponse forcee (desoriente apres avoir attaque et blesse)
      Substitution (module remplacé par `GetAbilities -> []`) : hf409 : rouges 1/4   restent VERTS : 3 ; hf410 : rouges 1/1 ; hf411 : rouges 1/1 ; hf412 : rouges 1/1
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.

### hf413 : Hyponotic Trance (1/3) (+ hf414, hf415, même script)

- [x] Étape 2 : cartes de référence : 04119 (`AttachToFaceWhenPutIntoPlay(most_remaining_hp, without_another_copy, if_cannot_gain_surge)`), hf304 (`UnitCannotDefend`), `UnitCannotAttackTarget`, 16095 (`CostFunc.Counter` sur une autre carte)
      Capacités : Ne peut pas attaquer Selene ni defendre contre elle ; When Revealed : s'attache a l'allie aux PV restants les plus hauts sans Trance, sinon surge ; Action de heros : [mental][mental] + -1 compteur du jour -> defausse
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « remaining » (PV restants, pas imprimes ; ⚠ Luke Cage a la carte Tough : `Puzzle.Damage` est absorbe) ; « the ally » (QUESTIONS.md n°6) ; le cout comprend le retrait du compteur du JOUR
- [x] Étape 6 : nombres texte ↔ code : -1 THW, 1 icone de boost (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 9 cas, 9 verts avec le module.
      - OK  [hf] hf413 revelee : s'attache a l'allie qui a le plus de PV RESTANTS (Mockingbird 3 PV intacts, pas Hulk 5 PV a 4 degats) ; THW -1
      - OK  [hf] hf414 revelee apres hf413 : l'allie qui a deja une Trance est exclu, la 2e va a l'AUTRE allie (Hulk)
      - OK  [hf] hf415 revelee quand le seul allie porte deja une Trance : « Otherwise, this card gains surge » (la carte suivante, Little Demon, est revelee)
      - OK  [hf] hf413 revelee sans aucun allie : elle gagne surge (la carte suivante est revelee)
      - OK  [hf] hf413 : l'allie hypnotise ne peut PAS attaquer Selene (Luke Cage ATK 2 : 0 degat)
      - OK  [hf] hf413 TEMOIN : sans Trance, Luke Cage attaque Selene (2 degats)
      - OK  [hf] hf413 : l'allie hypnotise ne peut PAS defendre contre Selene, mais defend contre un autre ennemi (Little Demon)
      - OK  [hf] hf413 Action de heros : le JOUR visible, depenser [mental][mental] (Genius) et retirer 1 compteur du jour -> la Trance est defaussee (compteurs 3 -> 2)
      - OK  [hf] hf413 Action de heros : TEMOIN, la NUIT (pas de jour a entamer) -> l'action n'est pas payable, la Trance reste
      Substitution (module remplacé par `GetAbilities -> []`) : hf413 : rouges 6/7   restent VERTS : 1 ; hf414 : rouges 1/1 ; hf415 : rouges 1/1
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.

### hf416 : Shining Shield (1/2) (+ hf417, même script)

- [x] Étape 2 : cartes de référence : 40091 Titanium Exoskeleton (`UnitCannotTakeDamageWhile`), `WhenThisBoostAttachTo`, hf413
      Capacités : Attachee a Selene : plafond de 2 degats par attaque ; Action de heros : [energy] + -1 compteur du jour -> defausse ; Boost : s'attache a Selene
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « from a SINGLE attack » (`is_from_attack=True`)
- [x] Étape 6 : nombres texte ↔ code : plafond 2 (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 5 cas, 5 verts avec le module.
      - OK  [hf] hf416 revele : s'attache a Selene
      - OK  [hf] hf416 : Selene ne peut pas subir plus de 2 degats d'UNE attaque (le JOUR, le heros attaque avec 3 -> 2 degats)
      - OK  [hf] hf416 TEMOIN : sans Shining Shield, le heros fait ses 3 degats le jour
      - OK  [hf] hf416 Action de heros : le JOUR visible, depenser [energy] (Energy) et retirer 1 compteur du jour -> le bouclier est defausse (compteurs 3 -> 2)
      - OK  [hf] hf417 Boost : Selene active avec Shining Shield en boost -> la carte s'attache a Selene
      Substitution (module remplacé par `GetAbilities -> []`) : hf416 : rouges 3/4   restent VERTS : 1 ; hf417 : rouges 1/1
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.

### hf418 : Relentless Pursuit

- [x] Étape 2 : cartes de référence : 60182 Cop (`WhenUnitWouldScheme` + `SetBeInstead`), hf120 (`DoAttackYou`)
      Capacités : Interruption forcee : Selene qui complote vous attaque a la place ; Action de heros : [physical] + -1 compteur du jour -> defausse
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « against YOU » : le joueur dont l'identite porte la carte ; « instead » = remplace la manigance
- [x] Étape 6 : nombres texte ↔ code : 3 icones de boost (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 3 cas, 3 verts avec le module.
      - OK  [hf] hf418 revelee : s'attache a l'identite ; Selene qui allait MANIGANCER ATTAQUE a la place (1 degat a l'alter-ego, menace inchangee a 1)
      - OK  [hf] hf418 TEMOIN : sans Pursuit, Selene manigance (+2 menace : 1 -> 3)
      - OK  [hf] hf418 Action de heros : le JOUR visible, depenser [physical] (Strength) et retirer 1 compteur du jour -> la carte est defaussee
      Substitution (module remplacé par `GetAbilities -> []`) : hf418 : rouges 2/3   restent VERTS : 1
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.

### hf419 : Dark Temptation

- [x] Étape 2 : cartes de référence : hf120 (`DoAttackYou`), 32069 Sabretooth Strikes (`IfThisAttackDefeats(Ally, ...)`)
      Capacités : When Revealed : Selene vous attaque ; Boost : si cette attaque vainc un allie, 2 menaces sur le complot principal
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « defeats an ally » (pas un autre personnage) ; piege paye : helper `MenaceSurLeComplotPrincipal` oublie dans le `__init__` du pack, NameError AVALE par le moteur
- [x] Étape 6 : nombres texte ↔ code : 1 icone de boost + etoile (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 3 cas, 3 verts avec le module.
      - OK  [hf] hf419 revelee : Selene attaque le joueur (heros incline : 1 degat)
      - OK  [hf] hf419 Boost : l'attaque DEFAIT une alliee (Black Cat 2 PV, 1 ATK + 1 icone = 2) -> 2 menaces sur le complot (1 -> 3)
      - OK  [hf] hf419 Boost : TEMOIN, l'alliee (Mockingbird 3 PV) survit -> pas de menace (reste 1)
      Substitution (module remplacé par `GetAbilities -> []`) : hf419 : rouges 2/3   restent VERTS : 1
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.

### hf420 : Lunar Eclipse

- [x] Étape 2 : cartes de référence : hf110 (`RevealThisCard`), hf407a/b
      Capacités : When Revealed : -1[per_hero] compteur du jour, sinon +1[per_hero] sur la nuit ; Boost : reveler cette carte
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « If you cannot » : le jour n'est pas visible ; retirer le dernier compteur du jour retourne l'environnement
- [x] Étape 6 : nombres texte ↔ code : 1 icone de boost + etoile (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 5 cas, 5 verts avec le module.
      - OK  [hf] hf420 revelee (JOUR) : retire 1 compteur du jour (3 -> 2)
      - OK  [hf] hf420 revelee (JOUR, 1 compteur) : le dernier est retire -> l'environnement se retourne sur la NUIT (3 compteurs)
      - OK  [hf] hf420 revelee (NUIT) : « If you cannot, place 1[per_hero] time counter on Under the Moonlight » (3 -> 4)
      - OK  [hf] hf420 Boost : Selene active avec Lunar Eclipse en boost -> la carte est REVELEE (+1 compteur la nuit, -1 pour l'activation : 3 -> 3)
      - OK  [hf] hf420 Boost : TEMOIN, meme activation avec une carte sans effet -> 3 -> 2
      Substitution (module remplacé par `GetAbilities -> []`) : hf420 : rouges 4/5   restent VERTS : 1
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.

### hf421 : Eternal Night

- [x] Étape 2 : cartes de référence : hf407a (`RetirerDuTemps`), 39026a (`card.Flip`)
      Capacités : Les compteurs de la nuit ne peuvent pas etre retires ; When Revealed : retourne le jour (la nuit revient)
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : « Flip Beneath the Sun » : sans effet si c'est deja la nuit ; la nuit revenue a EXACTEMENT 3 compteurs par joueur (QUESTIONS.md n°1)
- [x] Étape 6 : nombres texte ↔ code : menace 3, 3 icones de boost (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 4 cas, 4 verts avec le module.
      - OK  [hf] hf421 revelee quand le JOUR est visible : « Flip Beneath the Sun » -> la NUIT revient avec 3 compteurs
      - OK  [hf] hf421 revelee quand c'est deja la NUIT : rien ne se retourne (3 compteurs)
      - OK  [hf] hf421 : les compteurs de la NUIT ne peuvent pas etre retires (Selene s'active : 3 -> 3)
      - OK  [hf] hf421 TEMOIN : meme manigance en jeu, mais le JOUR est visible -> ses compteurs se retirent normalement (3 -> 2)
      Substitution (module remplacé par `GetAbilities -> []`) : hf421 : rouges 2/4   restent VERTS : 2
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.

### hf422 : Immortal Moon Goddess

- [x] Étape 2 : cartes de référence : gs115 Deathbird (`UnitCannotBeDefeatedWhile` + relance), 35029
      Capacités : Hinder 2[per_hero], Victory 1, acceleration (natifs) ; Tant que la nuit est en jeu, Selene ne peut pas etre vaincue
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : la relance de la defaite quand la protection tombe (la fabrique ne le fait pas quand la condition tombe : retournement du jour via `AfterCardFlip`, depart de la carte via `AfterCardLeavePlay`)
- [x] Étape 6 : nombres texte ↔ code : menace 7 + Hinder 2 par joueur, Victory 1, 1 icone de boost (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)
- [x] Étape 7 : cas `test_capacites`, preuve par substitution : 5 cas, 5 verts avec le module.
      - OK  [hf] hf422 revelee : menace 7 + Hinder 2 par joueur = 9 ; Victory 1 (desc)
      - OK  [hf] hf422 : la NUIT, Selene a 12 degats (mortels) mais n'est PAS vaincue (elle reste le stade I)
      - OK  [hf] hf422 : le JOUR venu (retournement), Selene a 12 degats est vaincue -> le stade II prend sa place
      - OK  [hf] hf422 : la manigance quitte le jeu -> Selene (a 12 degats) est vaincue aussi
      - OK  [hf] hf422 TEMOIN : sans la manigance, 12 degats vainquent Selene I (stade II)
      Substitution (module remplacé par `GetAbilities -> []`) : hf422 : rouges 1/5   restent VERTS : 4
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON

Carte terminée : NON : partie humaine à faire.


## Autoplay (étape 8), bilan commun aux 32 cartes

`tools/autoplay.py` (profil `equilibre`, graines 1 à 8, `.game-src-hfq`, ports 10150+), 8 parties chacune :

| Passe | Parties | Résultat | Rounds moyens | Causes de fin |
|---|---|---|---|---|
| Sunspot (`sunspot_hellfire`) / `hellfire_black_queen` standard | 8 | 0 victoires / 8 défaites | 4.9 | 7 × The Main Scheme was Completed ; 1 × All players were eliminated |
| Marvel Girl (`rachel_summers`) / `hellfire_black_queen` standard | 8 | 0 victoires / 8 défaites | 4.1 | 6 × All players were eliminated ; 2 × The Main Scheme was Completed |
| TÉMOIN : Sunspot / `hellfire_white_queen` standard | 8 | 0 victoires / 8 défaites | 4.2 | 5 × All players were eliminated ; 3 × The Main Scheme was Completed |
| Sunspot / `hellfire_black_queen_expert` | 8 | 0 victoires / 8 défaites | 4.9 | 5 × The Main Scheme was Completed ; 3 × All players were eliminated |

- **grep exhaustif des tracebacks** (`Traceback|NameError|AttributeError|TypeError|KeyError|AssertionError`) sur les 32 journaux : **0** partout.
- **Lecture du journal** : journal de la partie 1 de Sunspot (standard) lu par extraits (mise en place (nuit en jeu avec ses 3 compteurs, module Darkhold mis de côté), l'alternance nuit/jour (`Under the Moonlight perd 1 compteur` ... retournement sur `Beneath the Sun`, qui « entre en jeu » avec 3 compteurs, Sunspot « applique » le +1 aux pouvoirs de base puis « n'applique plus » au retour de la nuit), 2A (module Darkhold remélangé), Hellfire Conjuration en boost sur Selene, Dimensional Portal sans Darkhold (le livre est trouvé et attaché), Darkhold Dwarf révélé sans sort dans la défausse (rien de glissé)) puis événements `Darkhold` / sorts relevés par grep sur les 8 parties standard (Darkhold attaché par un sort, compteur `darkspell` retiré à l'attaque de Selene, Eternal Manipulation en boost).
- **Taux de victoire : 0/32, y compris le TÉMOIN (même héros contre White Queen, 0/8)** : ce n'est donc pas un signal de difficulté propre à Black Queen mais celui des decks de départ des deux héros de campagne (Sunspot incomplet : 4 cartes manquent au jeu, voir BACKLOG) et du pilote. Le scénario se termine par le complot principal (7 + 5 parties sur 24) ou par élimination.

## Portes statiques

- `tools/verifier_prefixes.py` : OK (aucun doublon, préfixe `hf` déclaré).
- `tools/verifier_desc_mots_cles.py hellfire_hunt_black_queen` : OK (32 cartes) après correction du texte de hf362 (`Uses (2 darkspell counters)`).
- `tools/verifier_noms_modules.py` : OK ; **calibrée** en lui donnant un nom inexistant (`hf999.py` jetable, supprimé) : elle tombe (« nom inconnu : NomQuiNExistePas »).
- `tools/verifier_appels_modules.py` : OK ; calibrée de même (`Faces.MethodeQuiNExistePas` : « n'existe pas »).
- `tools/test_cards.py` : 8103 cartes construites, 0 erreur.
- `ui-app` : `black-queen-plateau.test.ts` (5 cas, bloc plateau : aucun correctif d'affichage n'a été nécessaire, le plateau dessine déjà compteurs, attachements et cartes glissées sous un sbire), `textes-fr-fanmade.test.ts`, `traduction-public.test.ts`, `vocabulaire-statuts.test.ts`, `icones-ressources-fr.test.ts` : verts.
- Voile FR (Chromium via `ui-app/outils/export-voile/rendre-voile.mjs`, 11 cartes rendues : hf401, hf404a, hf404b, hf407a, hf407b, hf408, hf413, hf362, hf363, hf421, hf422) : le français se pose ; **défauts du voile (composant d'une autre session)** : hf404b garde deux traces d'anglais (« 2A », « it. ») hors de la zone effacée ; hf413 laisse « SIONI KIL » au-dessus de la ligne de traits traduite.

## Finitions du 01/11/2026 (session « finitions Hellfire Hunt »)

- Outil de preuve sur COPIE PRIVEE (jamais sur les sources partagees) : `docs/packs/hellfire-hunt/substituer_prive.py <pack> <port> <sortie.json>` (generalisation de celui de Torn ; `HFF_TAG='[hfc]'` pour les fondations). Mutations ponctuelles : un seul fragment du module retire, le cas doit tomber au rouge.
- **hf422 Immortal Moon Goddess : icone corrigee** (HAZARD, pas Acceleration : carte penchee sans barre, comparee a hf318/hf039/hf045 ; l'Acceleration de hf035 porte une barre dessous). `desc`, generateur et cas (`mots Hazard 1`) corriges.
- **hf422, preuve completee par MUTATIONS** (les deux cas « jour venu » et « la manigance quitte le jeu » restaient verts module vide car, sans protection, Selene est vaincue d'emblee : ils ne distinguaient rien) : (A) fabrique `UnitCannotBeDefeatedWhile(...)[:1]` (sans la relance a la sortie de la manigance) -> ROUGE sur « la manigance quitte le jeu » ; (B) sans la capacite `AfterCardFlip` (relance au retournement du jour) -> ROUGE sur « le jour venu ». Les deux moities sont donc PROUVEES.
