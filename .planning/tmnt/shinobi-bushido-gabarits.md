# TMNT Shinobi Bushido (`sb001`-`sb020`) : gabarits PROCESSUS-CARTE (17/10/2026)

Pack `tmnt_shinobi_bushido` (set « TMNT Shinobi Bushido », Inkwire, classe Bushido). Scans : `.../zip-shinobi/TMNT Shinobi/Bushido/B1..B20`.
Classement contre les officielles : **NOUVELLE** pour les 20 (aucune officielle identique ; seul homonyme proche : `sb008` Self-Control vs `44026`
« Self Control », ressource de Deadpool, carte différente). Cas : `Fusion/marvel-lcg-src/tools/cas/tmnt_shinobi_bushido.py` (filtre `[sb] sbNNN`).
Questions ouvertes : `.planning/tmnt/shinobi-bushido-questions.md` (Q-B1 Mercy, Q-B2 Santōryū Ōgi). Helpers du pack : `src/cards/pack/tmnt_shinobi_bushido/__init__.py`
(`OathsSousControle`, `PlacerUnCompteurSamurai`).

**Étape 8 (autoplay ciblé) : NON faite sur ces 20 cartes** (consigne : pas de batterie ; aucun deck de test ne contient de carte Bushido portée). **Étape 8 bis** :
`sb014` (attachée à un allié), `sb013` (attachée à une amélioration, chaîne à deux étages), `sb018` (manigance de joueur) et les compteurs samouraï sur les
OATH changent ce qu'on voit ; aucun cas plateau nouveau écrit : les attachements à plusieurs étages sont couverts par le correctif générique de
`zones.ts` (cas `tmnt-shinobi-paths-plateau.test.ts`) et le compteur « samouraï » par `ScanCard.jetons.test.tsx` ; **non prouvé à l'œil pour Kōshō et Ōgi**.

**Preuve par substitution** (module remplacé par `GetAbilities -> []`, cas du pack relancés, rouges comptés ; script jetable, `PARALLELES=4`, ports 28200-28299) :
rouges / total : sb001 3/5, sb002 3/4, sb003 3/4, sb004 3/6, sb005 9/9, sb006 1/4, sb007 4/6, sb008 3/5, sb009 6/9, sb010 6/6, sb011 6/6, sb012 2/6,
sb013 3/7, sb014 6/7, sb015 2/4, sb016 4/8, sb017 3/6, sb018 4/8, sb019 6/9, sb020 6/9. Les cas qui restent VERTS sans module sont des témoins d'ABSENCE
(un autre pouvoir de base ne retire rien, allié qui n'agit pas pour le héros, forme alter-ego, cible illégale, arme déjà prête...), des mesures de valeurs
imprimées / de base automatique (Max 1 par joueur, Restricted, Victory, unicité, traits, PV, ATQ, CTR, menace de départ) ou des contre-cas « sans la carte »
(sb006, sb020) : assumé, listé dans `.planning/tmnt/shinobi-bushido-questions.md` et au rapport.

Éléments communs : `Uses (N samurai counters)` = base native (`desc.Uses = "N,samurai"`, fiche `uses.md`) ; trait OATH + compteur : `samurai-counter.md` ;
« Your hero gets +1 X » = `GiveKeywordToInPlayWhenApplyThis("YourHero", ...)` ; « you control » = `joueur.GetControlUpgrade(CardFinder(trait=...))`.

### sb001 Loyalty / sb002 Rectitude / sb003 Courage (Upgrade OATH, Uses 3)
- [x] Étape 2 : réf. `totally_awesome_hulk/ah005` (bonus de stat), `trors/spider_woman/04032` (`AfterUnitUseBasicPower`), `se003`/`jennika/tj006` (`RemoveCountersOn`).
- [x] Étape 5 : « Forced RESPONSE » ; « your HERO makes a basic DEF/THW/ATK » (un seul pouvoir, héros seul) ; « from THIS card » ; Uses défausse au dernier.
- [x] Étape 6 : +1 ; 3 compteurs ; coût 0/1/1. Conforme.
- [x] Étape 7 : 5/4/4 cas : bonus, Forced Response (3 -> 2), témoin d'un autre pouvoir, dernier compteur, (sb001) aucune défense déclarée. Rouges sans module : 3/3/3.
- [x] Étape 7 bis : limite imprimée ? NON.   - [ ] Étape 8 : non faite.   - [x] Étape 8 bis : NON (compteur déjà couvert).
Carte terminée : **OUI** (x3). Non prouvé : le bonus en alter-ego (l'attribut n'existe pas sur l'alter-ego).

### sb004 Glory (Upgrade OATH, Max 1 par joueur)
- [x] Réf. `se008` (`AfterUnitDefeatedScheme`), `nebu/22014` (coût `Discard("This")`), helper `PlacerUnCompteurSamurai` x4.
- [x] Mots-pièges : « your HERO defeats a SIDE scheme » ; « discard THIS card -> » (coût, Glory n'est plus cible) ; « a TOTAL of 4 among ANY NUMBER of OATH you control ».
- [x] Nombres : 4, 0. Conforme.   - [x] Étape 7 : 6 cas (4 compteurs posés, tout sur une autre OATH, sans OATH, témoin sbire, Max 1 x2). Rouges 3/6.
- [x] Limite : « Max 1 per player » : cas jouable / non jouable.   - [ ] Étape 8   - [x] 8 bis : NON.
Carte terminée : **OUI**.

### sb005 Gratitude (Upgrade OATH, Uses 2)
- [x] Réf. `tj006`, `wonder_man/58002` (`HealHealth`), `fne/daredevil/60016` (cartes d'état de l'identité).
- [x] Pièges : « Action » (deux formes) ; deux coûts ; « heal 1 from your IDENTITY » ; « You MAY discard 1 status card » (toute sorte, phrases indépendantes).
- [x] Étape 7 : 9 cas, rouges 9/9 ; témoin d'épuisement (0 action après usage, il reste 1 compteur).   - [x] Limite imprimée : NON (l'inclinaison).
Carte terminée : **OUI**.

### sb006 Mercy (Upgrade OATH, Max 1 par joueur) : lecture confirmée (Q-B1)
- [x] Réf. `drax/19011` (`WhenUnitWouldBeDefeated` + `SetBeInstead` + `SetHealth`), `nebu/22014`.
- [x] Pièges : « BY YOUR HERO » (pas un allié), « hit points to 1 » (PV restants), « Then, draw 3 ».   - [x] 4 cas, rouges 1/4 (3 témoins / base automatique).
Carte terminée : **OUI**. Q-B1 (réponse du 17/10/2026, `shinobi-reponses.md`) : option (a) confirmée (PV restants à 1, la défaite n'a pas lieu, on pioche 3).

### sb007 Integrity (Upgrade OATH)
- [x] Réf. `tj008`/`tm011` (`AfterPlayerPlayedCard`), helper. Pièges : « YOU play an OATH UPGRADE » (une amélioration OATH, pas autre chose) ; exhaust ; elle répond à sa propre pose.
- [x] 6 cas, rouges 4/6 (témoins non OATH et événement verts).  - [x] Limite : épuisement (2e OATH jouée : rien).   Carte terminée : **OUI**.

### sb008 Self-Control (Upgrade OATH, Uses 3)
- [x] Réf. `trors/hawkeye/04010` (`CanGenerateResources(Resource, Resources("G"))`), `tj006`. Icône du texte = étoile wild de `tj009` (découpes comparées).
- [x] Pièges : « Resource » (deux formes) ; UNE ressource ; dernier compteur retiré PENDANT le paiement.  - [x] 5 cas, rouges 3/5.  Carte terminée : **OUI**.

### sb009 Devotion (Upgrade OATH, Uses 3)
- [x] Réf. `nebu/22014` (`canbe_ready`), `se003`. Pièges : « ready A WEAPON upgrade YOU control » (celle d'un allié comprise ; arme prête = pas une cible).
- [x] 9 cas, rouges 6/9 (cibles illégales / alter-ego verts).  - [x] Épuisement : 0 action après usage.  Carte terminée : **OUI**.

### sb010 Tsujigiri (Event ATTACK)
- [x] Réf. `valk/25018` (dégâts = ATQ), `nova/28014` (`if_this_attack_defeats`). Pièges : « equal to YOUR ATK » courant (Courage +1) ; « If THIS attack defeats THAT enemy » ; « you MAY ».
- [x] 6 cas, rouges 6/6.  Carte terminée : **OUI**.

### sb011 Vow (Event THWART)
- [x] Réf. `cw/tigra/56009` (`if_this_remove_last_threat`), `ares/ar001b` (recherche + `GainCard`). Pièges : CTR courant ; « LAST threat ON THAT scheme » ; deck seulement, OATH seulement.
- [x] 6 cas, rouges 6/6.  Carte terminée : **OUI**.

### sb012 Kensei (Event SKILL)
- [x] Réf. `sm/27016` (`SetTarget("YourHero", canbe_ready=True)`), `sentinel/st011` (coût d'inclinaison à sélecteur maison). Pièges : arme prête sous son contrôle (allié compris) ; héros incliné.
- [x] 6 cas, rouges 2/6 (4 témoins d'impossibilité de jouer).  Carte terminée : **OUI**.

### sb013 Santōryū Ōgi (Upgrade SKILL, Max 1 par deck) : lecture confirmée (Q-B2)
- [x] Réf. `superior_iron_man/si008` (`Search` + `PlayACard(face, True)`), `CanAttach.AttachTo2`, `GiveKeywordToAttached(apply=...)` + `GainKeyword`.
- [x] 7 cas (arme ramenée payée et rattachée, Restricted perdu puis rendu au détachement, défausse, aucun / impayable, témoins), rouges 3/7.
Carte terminée : **OUI**. Q-B2 (réponse du 17/10/2026, `shinobi-reponses.md`) : option (a) confirmée (identité puis arme). Écart moteur : la limite « 2 Restricted » est contrôlée à l'entrée en jeu de l'arme, avant le rattachement ; contournement NON prouvé.

### sb014 ✦ Kōshō (Upgrade OATH. TITLE. TRAINING., Uses 2)
- [x] Réf. `mut_gen/32013` + `up027` (« Max 1 TRAINING per ally » = moteur), `patriot/pt016`. `SetTarget("Attached")` (porteur lu AVANT que Uses ne défausse la carte).
- [x] 7 cas, rouges 6/7 ; « you control » prouvé à deux joueurs.  Carte terminée : **OUI**. Non prouvé : plateau (attache à un allié).

### sb015 Oathbreaker (Event TACTIC)
- [x] Réf. `scw/15006` Warp Reality. Pièges : « revealed FROM THE ENCOUNTER DECK » ; coût = défausser une OATH choisie ; cancel ET discard.  - [x] 4 cas, rouges 2/4.  **OUI**.

### sb016 ✦ Wakizashi (Upgrade NINJA. WEAPON., Restricted)
- [x] Réf. `red_guardian/rg010` (`AfterCardDiscard` + « depuis le jeu » en `conditions`). Pièges : OATH de N'IMPORTE QUEL joueur ; depuis le JEU ; Uses en fait partie ; une pioche par redressement.
- [x] 8 cas, rouges 4/8.  Carte terminée : **OUI**. Note : citation « dashido » reproduite telle qu'imprimée.

### sb017 ✦ Uno (Ally NINJA. SAMURAI. TURTLE., ATQ 1* CTR 1* PV 3)  - [x] Réf. `04032`, `ul036`. 6 cas, rouges 3/6. **OUI**.

### sb018 ✦ Musha Shugyō (Manigance annexe de joueur, menace 5, coût 1)
- [x] Réf. `next_evol/cable/40006` (menace non retirable), `next_evol/40019`. Pièges : « other than THE OWNER » (identité du propriétaire et ce qu'elle joue seulement) ; « up to 2 » ; deck ET défausse.
- [x] 8 cas, rouges 4/8. Leçon : `Puzzle.SetThreat` négatif retire la menace PAR la manigance elle-même et est bloqué par la carte. **OUI** (lecture littérale confirmée par l'utilisateur le 17/10/2026 : seule l'identité du propriétaire, et ce qu'elle joue, retire de la menace).

### sb019 ✦ Gusoku (Upgrade ARMOR)  - [x] Réf. `04032`, `27016`, `CostFunc.Counter(Select.From(fn))`. 9 cas, rouges 6/9. **OUI**.

### sb020 Iaidō (Event SKILL)  - [x] Réf. `wsp/13005` Rapid Growth (`GainValue(+2)`). 9 cas, rouges 6/9. **OUI**.
