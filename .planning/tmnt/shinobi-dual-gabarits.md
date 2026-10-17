# TMNT Shinobi, les 12 cartes DUAL (`sc001`-`sc012`) : gabarits PROCESSUS-CARTE (17/10/2026)

Pack `tmnt_shinobi_dual` (set « TMNT Shinobi Dual », Inkwire). Scans : `Dual Shinobi Cards/*.png`. Classement contre les officielles : **NOUVELLE** pour les 12
(aucun homonyme ni texte identique dans `data/cards.json`, vérifié par script le 17/10/2026 ; pas d'art alternatif possible). Crédit imprimé des 12 :
« TMNT Shinobi By: Inkwire ». Cas : `Fusion/marvel-lcg-src/tools/cas/tmnt_shinobi_dual.py` (filtre `[sc] scNNN`, 100 cas). Questions : `.planning/tmnt/shinobi-dual-questions.md`.

## Éléments communs aux 12

- **Une Dual compte comme LES DEUX types (livret p.7), construction ET jeu.** Preuves, pour chaque carte :
  - jeu, classes : cas `scNNN (classe DUAL a;b)` (verif `sc_classes`) : `IsClass`, `CardFinder(card_class=X)` et `card_classes=[X]` vrais pour CHACUN des deux types,
    faux pour les deux autres, faux pour Aspect, Basic et les quatre aspects ;
  - jeu, capacités des deux types : cas « avec JENNIKA » (Ninja Senpai = une Interruption par classe, une fois par round pour chacune) : +2/+2/+2 (deux classes = deux
    déclenchements) ; contre-épreuve : même cas avec `sc001` ramenée à la seule classe Bushido : +1/+1/+1, cas ROUGE (`attack=2 (attendu 3)`), restauré ensuite ;
  - construction : `tools/tests-lanceur/regles-shinobi-dual.test.mjs` (37 tests, sur les 12 cartes réelles de `data/cards.json`) : carte Shinobi, filtres des deux types et d'aucun
    autre, admise par un Path d'UN seul des deux types (Paths standard), refusée par un Path d'aucun des deux, refusée sans Path, jamais un aspect. Contre-épreuve : `sc001`
    ramenée à une classe : 3 tests rouges, restaurée ensuite.
- Aucune carte n'imprime « Limit once per round » : étape 7 bis = NON pour les 12. Les « limites » imprimées sont `Max 1 per player` (sc002, sc005, sc010, `desc.MaxPerUnit`, natif)
  et `Uses` (sc002, sc004, sc005, natif) : témoins ci-dessous.
- Preuve par substitution (module remplacé par `GetAbilities -> []`, cas relancés, restauré, ports 28600-28699 ; script jetable) : rouges / verts par carte au tableau final. Les
  cas qui restent VERTS sans module sont de quatre sortes, assumées : classes (moteur), `Uses`/`Max 1` natifs (`desc`), témoins d'ABSENCE (carte injouable, action non proposée,
  alter-ego), et le cas Jennika d'une amélioration (jouable sans module, le +2 vient des classes).
- Étape 8 (autoplay), commun : `deck` = Jennika + 36 Dual (3 exemplaires de chacune) contre Rhino normal, profil équilibré, **24 parties** (graines 1-24, 8 puis 16). Témoins : `spider_man`
  0/8 et `jennika` 0/8 (le pilote ne bat pas Rhino normal avec ces decks : 0 % partout, 0 % ici aussi). Grep exhaustif (NameError, AttributeError, TypeError, KeyError, AssertionError)
  sur les 40 journaux : **0**. Parties où le pilote a joué la carte : sc001 3 tentatives (voir ci-dessous), sc002 7, sc004 2, sc005 12 (21 Réponses), sc006 13, sc007 5, sc009 7,
  sc010 19, sc012 13 ; **sc003 Omawari, sc008 Naito Dansā, sc011 Kenbu : piochées et défaussées comme ressource, jamais jouées par le pilote** (pas prouvées en autoplay, seulement par cas).
  Journal lu pour Yomi : la carte remise au-dessus du deck est bien la prochaine carte de boost de Rhino ; Kusuri / Hitodama / Migatte : effets conformes au texte.
  ⚠ **Constat moteur (Nendō, aussi Omawari)** : quand l'arme est Jennika's Tekko-Kagi (WEAPON qui a AUSSI « exhaust → generate [wild] »), le pilote la compte parmi ses moyens de
  PAIEMENT ; le coût « Exhaust a WEAPON you control » est ensuite impayable, la carte revient en main et le paiement (cartes défaussées, Tekko-Kagi inclinée) est PERDU (sonde
  jetable, index 5645, journal : « Payé avec [...] » puis aucun effet). Paiement correct par la main : cas vert. Défaut du moteur (ordre ressources / coût de capacité), même schéma que
  `td005` ; non corrigé ici (hors périmètre), à signaler.
- Étape 8 bis, commun : les cartes dessinent des COMPTEURS de samouraï (sc002, sc004, sc005), des cartes d'ÉTAT (Cloaked, Dazed, Tough) et la carte révélée de sc008 : OUI, mais par des chemins
  déjà couverts. `ui-app/src/board/tmnt-shinobi-dual-plateau.test.ts` (10 tests) **verts d'emblée** : pas de « vu ROUGE sans correctif » possible (mécanismes déjà couverts par
  `tmnt-jennika-plateau.test.ts`), dit clairement. sc001, sc006, sc009, sc010, sc012 ne dessinent rien de nouveau.
- Texte FR : bloc « TMNT Shinobi Dual (sc) » de `textes-fr-fanmade.ts` + `generer-traduction-public.mjs` exécuté. Aucun mot-clé nouveau : fiches lues `shinobi`, `path`, `samurai-counter`,
  `uses`, `cloak`, `cloaked`, `daze`, `dazed`, `tuck` ; `Max 1 per player` = `desc.MaxPerUnit` (modèle `01018`).
- Gates : `verifier_appels_modules.py tmnt_shinobi_dual` OK (calibré : un appel bidon `PlaceThreatBidon` injecté dans sc001 est vu, puis retiré), `test_cards.py` 6717 OK / 0 erreur,
  `audit_cartes.py` aucune discordance sur `sc`, `verifier_prefixes.py` vert.

### Tableau final des cas

| carte | cas | rouges sans module | verts sans module (nature) |
|---|---|---|---|
| sc001 Nendō | 8 | 4 | classes, sans WEAPON, WEAPON non, WEAPON incliné (absences) |
| sc002 Shugorei | 9 | 4 | classes, Uses 4 natif, Max 1 x2, Jennika |
| sc003 Omawari | 6 | 3 | classes, sans WEAPON, alter-ego |
| sc004 Kuragari | 9 | 4 | classes, Uses 3 natif, témoin sans Action, 2 compteurs = 0 action, Jennika |
| sc005 Yoi-Dachi | 12 | 3 | classes, Uses natif, 5 absences (sans carte, Tenace, hors attaque, allié, Rhino hébété ATQ 0), Max 1, Jennika |
| sc006 Migatte | 8 | 5 | classes, témoin sans Migatte, alter-ego |
| sc007 Mizuki | 9 | 7 | classes, alter-ego |
| sc008 Naito Dansā | 8 | 5 | classes, deck sans cible (coût impayé), alter-ego |
| sc009 Yomi | 7 | 4 | classes, défausse vide, alter-ego |
| sc010 Kusuri | 10 | 6 | classes, non ATTACK, Max 1, Jennika |
| sc011 Kenbu | 8 | 5 | classes, sans Cloaked, alter-ego |
| sc012 Hitodama | 6 | 4 | classes, alter-ego |

(sc001 8 cas : le chiffre 4/4 est celui de la dernière substitution, après ajout du cas Tekko-Kagi ; les autres cartes ont été substituées avant ou après leur dernière modification, aucune
modification de cas depuis, sauf sc009 : vérificateur `Deck.GetTop` ajouté, substitution relancée 4/3.)

### sc001 : Nendō (Événement Bushido/Kuji-Kiri, ATTACK PSIONIC, 2, R)

- [x] Étape 2 : « Exhaust a WEAPON upgrade you control → » : `td005` Improvised Tactics (`CostFunc.Exhaust(card_type=Upgrade, trait=, from_where=["YouControlCards"])`) ; Hero Action (attack) +
      dégâts puis statut : `jennika/tj004` ; daze : `ShinobiDaze`.
- [x] Étape 5 : mots-pièges : Exhaust devant la flèche (coût, pas défausse), « an enemy » puis « THAT enemy » (même cible, après les dégâts, pas un ennemi vaincu), Hero Action (forme héros).
      Résultat : conforme.
- [x] Étape 6 : 4 dégâts, coût 2 : `desc` = script. Conforme.
- [x] Étape 7 : 8 cas, capacité unique : nominal (rouge sans module), sbire vaincu, Tekko-Kagi payée par la main, sans WEAPON / WEAPON non / WEAPON incliné (témoins), Jennika.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : 24 parties communes, tentatives de Nendō par le pilote : constat moteur ci-dessus (paiement perdu quand l'arme paie aussi). Pas de résolution en autoplay.
- [x] Étape 8 bis : statut Dazed (déjà couvert).
Carte terminée : **OUI** (comportement prouvé par cas ; réserve moteur du paiement ci-dessus).

### sc002 : Shugorei (Amélioration Bushido/Kuji-Kiri, OATH SPELL, 2, B)

- [x] Étape 2 : coûts « Exhaust this + remove N counters » : `jennika/tj006` ; `Max 1 per player` : `01018` ; `DrawUp`.
- [x] Étape 5 : « from IT » (compteurs sur elle), les deux coûts, « Action » (deux formes), Max 1. Conforme.
- [x] Étape 6 : Uses 4, retrait 2, pioche 1. Conforme.
- [x] Étape 7 : 9 cas : 4 compteurs à l'entrée, Action (heros), alter-ego, **témoin d'épuisement** (2 usages puis la carte quitte le jeu : main +2), pas d'action une fois inclinée, Max 1 (+ témoin), Jennika.
- [x] Étape 7 bis : limites imprimées Uses / Max 1 : témoins ci-dessus. [x] Étape 8 : jouée 7 fois, 14 activations, 0 erreur. [x] Étape 8 bis : compteurs (couvert).
Carte terminée : **OUI**.

### sc003 : Omawari (Événement Bushido/Ninjutsu, SKILL, 1, R)

- [x] Étape 2 : `td005` (coût WEAPON) ; `tj005` / `se001` (cloak your hero) ; `Faces.GiveStatus(..., "Tough")`.
- [x] Étape 5 : les DEUX statuts sur LE HÉROS, « them » = le héros, un seul Cloaked par personnage (Tough posé quand même), Hero Action. Conforme.
- [x] Étape 6 : coût 1. [x] Étape 7 : 6 cas (nominal, sans WEAPON, déjà camouflé, alter-ego, Jennika) rouges sans module : 3/6. [x] 7 bis : NON.
- [ ] Étape 8 : jamais jouée par le pilote (drawn, utilisée comme ressource) : non prouvée en autoplay (voir commun). [x] 8 bis : statuts (couvert).
Carte terminée : **OUI** (autoplay sans partie jouant la carte, dit clairement).

### sc004 : Kuragari (Amélioration Bushido/Ninjutsu, OATH, 2, Y)

- [x] Étape 2 : `tj006` (coûts, `Faces.ReadyAll`), `tj005` (cloak). [x] Étape 5 : « 3 counters from it » (une seule utilisation, puis la carte part), cloak ET ready, « Action » + « your hero » : **Q-D1**.
- [x] Étape 6 : Uses 3, retrait 3. [x] Étape 7 : 9 cas : Uses, Action (cloak + ready + la carte part), témoins (sans Action, 2 compteurs = 0 action, 3 = 1 action), déjà camouflé, alter-ego provisoire, Jennika.
- [x] 7 bis : NON (Uses : témoins). [x] Étape 8 : 2 parties jouées, 0 erreur. [x] 8 bis : compteurs (couvert).
Carte terminée : **OUI**. Q-D1 (réponse du 17/10/2026, `shinobi-reponses.md`) : « Action » des deux formes ; en alter-ego « your hero » = l'identité camouflée et redressée (lecture littérale confirmée). 9 cas verts.

### sc005 : Yoi-Dachi (Amélioration Bushido/Taijutsu, OATH STANCE, 2, Y)

- [x] Étape 2 : `bkw/08030` Counterattack (`AfterUnitTookDamage(..., "You", is_from_attack=True, who_dealt_damage=Enemy)`, cible `"Attacker"`) ; `tj006` (compteur).
- [x] Étape 5 : « After YOU take damage FROM AN ENEMY ATTACK » (pas un allié, pas un dégât hors attaque, pas une attaque sans dégât), « Response » (deux formes), « THAT enemy » (l'attaquant),
      Uses, Max 1. Conforme.
- [x] Étape 6 : Uses 3, retrait 1. [x] Étape 7 : 12 cas : Réponse (héros, alter-ego), témoins (sans carte, Tenace, Puzzle.Damage, allié, Rhino hébété ATQ 2-2 = 0), **épuisement** (1 compteur : la Réponse
      part puis la carte quitte le jeu), Max 1, Jennika. [x] 7 bis : Uses / Max 1 témoins. [x] Étape 8 : 12 jouées, 21 Réponses, 0 erreur. [x] 8 bis : compteurs, Dazed (couvert).
Carte terminée : **OUI**.

### sc006 : Migatte (Événement Bushido/Taijutsu, DEFENSE, 1, R)

- [x] Étape 2 : `cap/03033` Expert Defense (`WhenUnitDefendAgainstAttack`, `GainDEFForThisAttack`) ; `jennika/tj004` (`paid_this_res_effects`) avec `EstShinobi` (helper local).
- [x] Étape 5 : « paid WITH A SHINOBI CARD » (autre carte, une Dual ou une carte à une classe, pas Basic/aspect), +2 DEF inconditionnel, ready seulement si payée ainsi, HeroInterrupt. Conforme.
- [x] Étape 6 : +2 DEF, coût 1. [x] Étape 7 : 8 cas (Capitaine Marvel DEF 1 contre Fin Fang Foom ATQ 4 : 3 dégâts sans Migatte, 1 avec ; payée Strength : reste inclinée ; payée Nendō / tj004 : redressée ;
      payée Haymaker : inclinée ; alter-ego : 4 dégâts, Migatte reste en main ; Jennika). [x] 7 bis : NON. [x] Étape 8 : 13 jouées, 0 erreur. [x] 8 bis : NON.
Carte terminée : **OUI**.

### sc007 : Mizuki (Événement Kuji-Kiri/Ninjutsu, PSIONIC THWART, 2, B)

- [x] Étape 2 : `04049` Clear the Area (« last threat on that scheme »), `ua002` (`ChooseAbilities`), `td005` (cloak), `se004` (`Faces.AddToHand`).
- [x] Étape 5 : « THE LAST threat ON THAT scheme » (avant > 0, après = 0), « choose » (une branche), « a FRIENDLY character », « an EVENT from YOUR discard » (pas une amélioration). Conforme.
- [x] Étape 6 : 2 menaces. [x] Étape 7 : 9 cas (2 -> 0, 1 -> 0, 3 -> 1 témoin, branche Return, amélioration non rendue, allié camouflé, alter-ego, Jennika) : 7 rouges. [x] 7 bis : NON.
- [x] Étape 8 : 5 jouées, 0 erreur. [x] 8 bis : statut (couvert).
Carte terminée : **OUI**.

### sc008 : Naito Dansā (Événement Kuji-Kiri/Ninjutsu, SPELL, 2, Y)

- [x] Étape 2 : `sm/27015` + `alopex/ta006` (même phrase « Reveal that card → », coût), `td005` (choix d'amis). [x] Étape 5 : union attachement OU manigance annexe, révélation avant la flèche,
      « up to 2 » (0 à 2), deux phrases indépendantes. Conforme. [x] Étape 6 : 2 et 2. [x] Étape 7 : 8 cas (attachement, manigance annexe, deck sans cible, « up to » moins que 2, exactement 2 sur 3,
      alter-ego, Jennika) : 5 rouges. [x] 7 bis : NON. [ ] Étape 8 : jamais jouée par le pilote. [x] 8 bis : carte révélée (couvert).
Carte terminée : **OUI** (autoplay sans partie jouant la carte).

### sc009 : Yomi (Événement Kuji-Kiri/Taijutsu, PSIONIC SPELL THWART, 1, Y)

- [x] Étape 2 : `04049` (effet), `valk/25001b` (`from_where=["EncounterDiscardPile"]`), `Faces.MoveAllToDeck`. [x] Étape 5 : coût devant la flèche (défausse vide = injouable), la carte CHOISIE va au DESSUS,
      « A scheme » (principale ou annexe). Conforme. [x] Étape 6 : 2 menaces. [x] Étape 7 : 7 cas, vérif `sc_dessus_rencontre` (deux lectures du dessus : `Deck.GetTop()` et l'ordre) : choisie au-dessus, l'autre
      reste, défausse vide, manigance annexe, alter-ego, Jennika : 4 rouges. [x] 7 bis : NON. [x] Étape 8 : 7 jouées, remise au-dessus lue au journal. [x] 8 bis : NON.
Carte terminée : **OUI**. (Libellé du journal « déplacée vers EncounterDiscardPile<0> top » trompeur : les mesures `Deck.GetTop` et la boost suivante de Rhino confirment le deck.)

### sc010 : Kusuri (Amélioration Kuji-Kiri/Taijutsu, ITEM MYSTIC, 2, R)

- [x] Étape 2 : `rainy/ra001b` Physician (`SetTarget(Friend, canbe_heal=True)`, `HealthUnits`), `CostFunc.Discard("YourHandCards", ...)`, `01018` (Max 1).
- [x] Étape 5 : « an ATTACK EVENT from your hand » (coût), « A FRIENDLY character » (allié inclus), « Action » (deux formes), Max 1. Conforme. [x] Étape 6 : 2 soignés. [x] Étape 7 : 10 cas (héros, alter-ego, allié, soin
      plafonné à 0, non ATTACK = 0 action, ATTACK = 1 action, **épuisement** (2 Haymaker, une seule défaussée), Max 1, Jennika) : 6 rouges. [x] 7 bis : Max 1 témoin. [x] Étape 8 : 19 jouées. [x] 8 bis : NON.
Carte terminée : **OUI**.

### sc011 : Kenbu (Événement Ninjutsu/Taijutsu, ATTACK, 2, B)

- [x] Étape 2 : `skrull_menace/lyja/sk049` (coût statut, `SetTarget(Enemy, range=(0, N))`), `tj004`. [x] Étape 5 : Cloaked du HÉROS défaussé en coût, « up to 3 », 1 dégât à CHACUN, « damaged this way » (Tenace = pas blessé),
      Hero Action. Conforme. [x] Étape 6 : 1 dégât, 3 ennemis. [x] Étape 7 : 8 cas (3 ennemis, sans Cloaked, 1 seul choisi, Rhino Tenace, sbire vaincu, alter-ego, Jennika) : 5 rouges. ⚠ Guard : un sbire Guard engagé
      interdit de viser le vilain (règle moteur) : cas montés avec Hydra Bomber (sans Guard). [x] 7 bis : NON. [ ] Étape 8 : jamais jouée par le pilote. [x] 8 bis : statuts (couvert).
Carte terminée : **OUI** (autoplay sans partie jouant la carte).

### sc012 : Hitodama (Événement Ninjutsu/Taijutsu, ATTACK, 2, B)

- [x] Étape 2 : `tj004` + `PayeAvecUnEvenement(effect, "THWART")`, `beast/bt005` (Hero Response sans déclencheur lue Hero Action). [x] Étape 5 : « paid with A THWART event », cloak LE HÉROS, **Hero Response sans « After » : Q-D2**.
- [x] Étape 6 : 3 dégâts. [x] Étape 7 : 6 cas (THWART : camouflé, ATTACK / ressources : pas camouflé, alter-ego, Jennika) : 4 rouges. [x] 7 bis : NON. [x] Étape 8 : 13 jouées, 0 erreur. [x] 8 bis : statut (couvert).
Carte terminée : **OUI**. Q-D2 (réponse du 17/10/2026, `shinobi-reponses.md`) : Hero Action (attack) confirmée (précédent `bt005`) ; le texte affiché de cards.json garde le « Hero Response » imprimé (comme sj020). 6 cas verts.
