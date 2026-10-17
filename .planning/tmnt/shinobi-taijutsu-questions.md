# TMNT Shinobi Taijutsu (sh001-sh020) : questions ouvertes pour l'utilisateur (17/10/2026)

> Réponses rendues le 17/10/2026, voir shinobi-reponses.md (les mentions « NON terminée » / « provisoire » ci-dessous sont historiques : cartes levées).

Source : zip « TMNT Shinobi », dossier `Taijutsu` (T1-T20). Scans : `/tmp/claude-29999/-home-oem-Desktop-Marvel-LCG/2ed3e66d-9fcf-45e1-aa7f-2debf9a42af0/scratchpad/zip-shinobi/TMNT Shinobi/Taijutsu/`
(images importées dans `assets/pics/sh001.jpg`..`sh020.jpg` par `tools/importer_images_tmnt_shinobi.py`). Une question à la fois, scan à l'appui
(consigne : montrer l'image avant chaque question). Lecture PROVISOIRE retenue entre parenthèses ; chaque question dit ce qu'elle change EN JEU.
Les cartes concernées sont codées, testées, mais laissées **NON terminées** tant que la réponse n'est pas rendue.

## Q-T1 : sh003 Stiff Jab : crédit imprimé « MC Custom Content By: Inkwire »
- Scan : `Taijutsu/T3 Stiff Jab.png`. Les 19 autres cartes Taijutsu impriment « TMNT Shinobi By: Inkwire » ; celle-ci imprime
  « **MC** Custom Content By: Inkwire » (reste d'un autre gabarit, coquille probable).
- Options : (a) **laisser le scan tel quel** (recommandée : le scan fait foi, la ligne de crédit n'est pas du texte de jeu et le
  champ `custom` vaut « Inkwire » dans tous les cas) ; (b) retoucher l'image pour écrire « TMNT Shinobi By: Inkwire » ; (c) autre.
- Effet en jeu : AUCUN (une ligne de crédit sur l'image). Provisoire : (a). `sh003` : **NON terminée** (attend Q-T1, crédit seul).

## Q-T2 : sh017 Odyn : citation « I suggest you stand behnd me this time. »
- Scan : `Taijutsu/T17 Odyn.png`. La citation imprimée porte « **behnd** » (pour « behind »), sans nom d'auteur ; coquille probable.
- Options : (a) **corriger en « behind » dans `cards.json` et le texte français** (recommandée : lecture évidente, aucun effet de règle) ;
  (b) garder « behnd » tel quel (fidélité typographique au scan) ; (c) autre.
- Effet en jeu : AUCUN (texte d'ambiance en italique, sans règle). Provisoire : (b), la citation est transcrite comme imprimée
  dans `data/cards.json` ; le texte français la corrige déjà (« Je vous conseille de rester derrière moi cette fois »).
  `sh017` : **NON terminée** (attend Q-T2).

## Q-T3 : sh005 Double Kick : un événement qui porte DEFENSE et THWART satisfait-il les deux puces ?
- Scan : `Taijutsu/T5 Double Kick.png` : « If you paid for this card with: • A DEFENSE event, draw 1 card. • A THWART event, draw 1 card. »
  Trois événements du pack (Toss `sh009` DEFENSE/THWART, Countercross `sh018` ATTACK/DEFENSE/THWART, Trading Blows `sh007`
  ATTACK/DEFENSE pour la seule puce DEFENSE) portent plusieurs traits.
- Options : (a) **lecture littérale : chaque puce se teste séparément, Toss (DEFENSE + THWART) donne 2 cartes** (recommandée, c'est
  ce qui est codé : deux conditions indépendantes) ; (b) un même événement ne vaut qu'UNE puce, donc 1 carte au plus par événement ;
  (c) autre.
- Effet en jeu : (a) Double Kick payée par Toss ou Countercross pioche 2 ; (b) elle pioche 1. Plusieurs événements du MÊME trait ne
  repiochent pas dans les deux lectures (« A DEFENSE event », pas « each »). Provisoire : (a). `sh005` : **NON terminée** (attend Q-T3).

## Q-T4 : sh016 Jō : « After you damage an enemy » : quelles sources comptent ?
- Scan : `Taijutsu/T16 Jo.png` : « Hero Response: After you damage an enemy, remove 2 cudgel counters from this card → daze that enemy. »
  Même question que `.planning/tmnt/aspects-aggression-questions.md` Q-UA3 (ua033 Pete).
- Options : (a) **vos dégâts : votre identité ET les cartes que vous jouez** (recommandée, codée, comportement MESURÉ du moteur pour
  l'officielle `16032` Schadenfreude : un événement d'attaque comme Haymaker déclenche Jō, un allié non) ; (b) votre identité seulement
  (ses attaques et capacités) : un événement ne déclencherait pas Jō ; (c) tout ce que vous contrôlez, alliés compris ; (d) autre.
- Effet en jeu : (a) Haymaker + Jō = 3 dégâts puis un hébétement ; (b) pas d'hébétement après un événement ; (c) aussi après l'attaque d'un
  allié. Provisoire : (a). `sh016` : **NON terminée** (attend Q-T4).

## Notes sans question (relevées, aucune décision en jeu)
- **Homonyme confirmé sur le scan** : `sh008` Drop In (`Taijutsu/T8 Drop In.png`) n'a RIEN de commun avec `night_thrasher/nt004` Drop In
  (Hero Response de Night Thrasher : après un changement de forme, Battle Board). Ici : Action, redressez votre identité, retour d'un
  événement ATTACK/THWART si payée par un événement DEFENSE ; traits NYC. TACTIC. ; classe Taijutsu. Classement : NOUVELLE.
- **Classement contre les officielles** : les 20 cartes sont NOUVELLES (aucun texte identique à une officielle, aucun art alternatif) :
  les homonymes et quasi-homonymes (Crosscounter `18004` ~ Countercross, Wiggle Room `05005` ~ Raising Block, Bo Tobu `td003` ~ Toss...)
  ont un texte différent.
- **Cible « a scheme » = menace requise (convention du moteur)** : `Scheme2` ajoute `has_threat=True` aux cibles de manigance
  (`ability.py`, déjà vrai de l'officielle `18004` Crosscounter). Conséquence sur Toss `sh009`, Countercross `sh018`, Double Kick `sh005` :
  sans menace sur AUCUNE manigance, la carte n'est pas proposée, même si le reste de son effet (prévention, dégâts, pioche) serait
  possible. Non corrigé (comportement général du moteur, hors du périmètre d'une carte) ; mesuré par le cas
  `[sh] sh009 ... CONVENTION MOTEUR`.
- **Odyn `sh017` et les dégâts consécutifs** : le moteur résout la Réponse « After Odyn uses a basic power » AVANT les dégâts
  consécutifs (type d'aptitude `Consequential`, `ally.py`) : la carte Tough donnée par Odyn absorbe donc les dégâts consécutifs de CETTE
  attaque (Odyn n'a aucun dégât, la carte Tough est consommée). Mesuré par les deux premiers cas `sh017`. À confirmer en partie réelle si
  l'intention de l'auteur était autre.
- **Mutant Fight Club `sh012`** : « attach » = `PlaceCardHere(face cachée)` comme `ma004` / `26013`. Aucun plafond imprimé, aucun codé.
- **Martial Skill `sh010` / Jō `sh016`** : aucune cible de pose imprimée : amélioration posée sur VOTRE identité (défaut du moteur, comme
  `core/01057`), donc les Réponses de héros n'ont d'effet que sous la forme héros.
