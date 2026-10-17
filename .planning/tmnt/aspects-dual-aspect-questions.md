# Aspects TMNT « Dual-Aspect » (`ud`) : questions ouvertes

16/10/2026, agent Dual-Aspect (branche `aspects-ud`). Scans : dossier zip « TMNT Aspect/Dual-Aspect »
(espace finale). Une question par carte, options multichoix, recommandation en premier.
Les cartes concernées sont codées selon l'option RECOMMANDÉE (cas verts sur cette lecture) mais
restent « Carte terminée : NON » tant que la réponse n'est pas donnée ; une autre réponse = une
retouche de quelques lignes dans le module indiqué.

---

## Q-UD1 : unicité par le SOUS-TITRE (les six cartes) — question transversale, non bloquante

- Cartes : ud001 ✦Rōnin « MIKEY », ud002 ✦Doomsayer « DONNIE », ud003 ✦Heavy Metal « JENNY »,
  ud004 ✦Stealth Fighter « RAPH », ud005 ✦Sōhei « LEO », ud006 ✦Nightwatcher « JENNY ».
- Constat : ces sous-titres sont EXACTEMENT les titres d'alter ego des héros TMNT (tm001b « Mikey »,
  td001b « Donnie », tj001b « Jenny », tr001b « Raph », tl001b « Leo »). Heavy Metal et Nightwatcher
  partagent le même sous-titre « Jenny » ; Doomsayer partage « Donnie » avec ua006 Bo-Wing.
- Les deux juges du projet ne disent PAS la même chose :
  - le **deck-builder** (`regles.js`, `correspondent`, Rules Reference v1.8) : un sous-titre égal au
    titre d'alter ego ou au sous-titre d'une autre carte unique = cartes qui « se correspondent » →
    Rōnin refusé dans un deck de Michelangelo, Heavy Metal + Nightwatcher refusés ensemble ;
  - le **moteur** (`CanCoexistWith`) : conflit seulement si TITRE commun ET même sous-titre → tout
    coexiste en jeu.
- Ce n'est pas un bandeau ✦ (décision Q-R1) : aucun `unique_also` posé.
- Question : Rōnin (Mikey) peut-il être joué par Michelangelo, et Heavy Metal (Jenny) cohabiter avec
  Nightwatcher (Jenny) ou Jennika ?
  1. **(recommandé)** Non : le sous-titre est le personnage ; ces alliés sont des « versions » de la
     tortue. Règle RR v1.8 du deck-builder ; aligner le moteur (`CanCoexistWith` : un sous-titre égal
     au titre d'alter ego / au sous-titre d'une autre unique = conflit). En jeu : Michelangelo ne
     peut pas inclure Rōnin ; un seul allié « Jenny » à la fois.
  2. Oui : seul le titre compte (comportement actuel du moteur) ; aligner le deck-builder sur le
     moteur pour ces packs. En jeu : Michelangelo + Rōnin, Heavy Metal + Nightwatcher ensemble.
  3. Autre (précise).

## Q-UD2 : ud003 Heavy Metal — « place a status card on a character » : quelles cartes d'état ?

- Scan : `TMNT Aspect/Dual-Aspect /AP Heavy Metal Jenny.png`.
- Le jeu connaît 7 cartes d'état : Stunned, Confused, Tough (officielles), Cloaked, Dazed,
  Intensified (TMNT, Inkwire), Exposed (pack custom sentinel).
- Options :
  1. **(recommandé, codé)** N'importe laquelle des cartes d'état que le jeu connaît, au choix du
     joueur, parmi celles que le personnage peut recevoir (plafonds du moteur). En jeu : 7 choix,
     dont Cloaked/Dazed/Intensified.
  2. Seulement les trois officielles (Stunned, Confused, Tough). En jeu : 3 choix.
  3. Les officielles + celles des scénarios TMNT (Cloaked, Dazed, Intensified), sans Exposed.
  4. Autre (précise).
- Module : `src/cards/pack/tmnt_aspect_dual/ud003.py`, liste `STATUTS`.

## Q-UD3 : ud004 Stealth Fighter — « Interrupt: AFTER Stealth Fighter is defeated »

- Scan : `TMNT Aspect/Dual-Aspect /JL Stealth Fighter Raph.png`.
- Texte contradictoire (même type que The Made Men) : « **Interrupt**: After Stealth Fighter is
  defeated by consequential damage, cloak a friendly character. »
- Options :
  1. **(recommandé, codé)** Interruption « When Stealth Fighter is defeated by consequential damage »
     (même tournure que Rōnin, Doomsayer, Sōhei du même pack). En jeu : l'effet part pendant qu'il
     tombe, un ami (identité ou allié, pas lui-même) devient Cloaked.
  2. Réponse « After ... is defeated » : même effet en jeu, un cran plus tard (après sa sortie).
     Le moteur doit alors porter la capacité depuis la défausse (pas de différence visible pour un
     joueur seul, différence de fenêtre pour d'autres interruptions).
  3. Autre (précise).

## Q-UD4 : ud005 Sōhei — « YOUR HERO gets +2 hand size » si l'on est en ALTER EGO

- Scan : `TMNT Aspect/Dual-Aspect /JP Sohei Leo.png`.
- Un allié peut attaquer/contrer (donc subir un dégât consécutif et tomber) quand le joueur est en
  forme alter ego.
- Options :
  1. **(recommandé, codé)** Le bonus ne vaut que si l'identité est en forme HÉROS quand Sōhei tombe ;
     en alter ego, rien. En jeu : pas de +2 si Sōhei tombe pendant un tour en alter ego.
  2. « Your hero » = votre identité quelle que soit sa forme : +2 aussi en alter ego.
  3. Le bonus est posé sur la face héros et ne s'applique que si l'on se retourne en héros avant la
     fin du round.
  4. Autre (précise).
