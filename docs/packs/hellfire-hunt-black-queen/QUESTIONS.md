# Hellfire Hunt, scénario 3 « Black Queen » (Selene) + module Darkhold : vrais doutes de règle

Écrit le 01/11/2026 par l'agent du scénario 3. L'utilisateur n'a PAS été interrogé (brief : trancher par les règles, le livret, le Rules Reference 1.8, puis ne garder
que ce qui reste ambigu). Chaque entrée : la carte, le scan, les lectures possibles, ce que chacune change EN JEU, la recommandation, et le **choix provisoire déjà codé**.

Scans : `/tmp/claude-29999/-home-oem-Desktop-Marvel-LCG/6c912ee0-c9ba-469c-a5ba-e4fc4b30f45a/scratchpad/hh/Hellfire Hunt Campaign/` (désigné `<ZIP>/` ci-dessous).

## Ce qui a été tranché SANS question (pour mémoire)

- **« basic power »** : le Rules Reference 1.8 (p.10, entrée BASIC POWER) en compte CINQ : ATK, THW, DEF, REC, SCH. Les héros, alliés, vilains et sbires en ont
  chacun leur part. DEF et REC sont donc bien des pouvoirs de base : un personnage ami qui contre, attaque, défend ou récupère fait perdre un compteur (voir n°2 pour
  la moitié « enemy »).
- **« Each identity gets +1 to each of its basic powers »** (Beneath the Sun) : ATK, THW, DEF et REC, héros ET alter ego (les alliés ne sont pas des identités).
- **Retournement = « entre en jeu »** : sans compteur, l'environnement se retourne ; la face qui apparaît « entre en jeu avec 3 compteurs par joueur » (sinon elle se
  retournerait aussitôt, à l'infini : Lunar Eclipse et hf404b posent d'ailleurs des compteurs sur un jour qu'on suppose rempli).
- **« Find »** (Darkhold, Immortal Moon Goddess, Blackheart) : deck de rencontre, défausse, zone mise de côté (Rules Reference 1.8 p.19, fiche `mots-cles/find.md`).
- **Blackheart et Immortal Moon Goddess restent DANS le deck de rencontre** dès le début (le Setup du 1A ne les met pas de côté ; même montage que Mutant Supremacy
  dans White Queen). Si l'un est pioché tôt, le 3A ne le trouve plus : c'est la règle de « find ».
- **Cartes mal orthographiées sur les scans** : « Rentless Pursuit » → nom `Relentless Pursuit`, « Hellfire Conjuratioion » → `Hellfire Conjuration`, « enviornment » →
  `environment` dans le texte de hf421. L'image garde la faute, le nom et le texte du jeu non.
- **Icônes de ressource** (Rules : jamais à vue) : poing = [physical] (vérifié contre `so002` par l'agent White Queen), nœuds reliés = [mental] (contre `rm004`, idem),
  éclair = [energy] (icône universelle du jeu). Aucune n'est « inconnue ».

## Vrais doutes

### 1. Eternal Night force le retournement alors qu'il reste des compteurs : que deviennent-ils ? (hf407a / hf407b / hf421)
Scans : `<ZIP>/Scenario/Black Queen/7a.png`, `7b.png`, `21.png`.
- Texte : « Beneath the Sun enters play with 3[per_hero] time counters. If there are no time counters here, flip this card. » et, sur Eternal Night, « When Revealed: Flip
  Beneath the Sun. » Le retournement NATUREL (0 compteur) est sans ambiguïté. Le retournement FORCÉ par Eternal Night peut avoir lieu avec des compteurs sur le jour.
- Lectures : (A) **la nuit arrive avec exactement 3 compteurs par joueur, les compteurs du jour disparaissent** ; (B) la nuit garde les compteurs du jour ET reçoit les 3
  par joueur ; (C) la nuit garde seulement les compteurs du jour (aucun nouveau).
- En jeu : (A) la nuit dure toujours le même temps, quelle que soit la carte qui l'a ramenée ; (B) un jour presque épuisé ramène une nuit LONGUE (jusqu'à 3 de plus) ;
  (C) un jour presque épuisé ramène une nuit courte.
- Recommandation : **(A)**. **Choix provisoire codé : (A)** (`RemplirLeTemps`, `__init__.py`).

### 2. « After a character uses a basic power OR an enemy activates » : qui compte ? (hf407a / hf407b)
Scans : `7a.png`, `7b.png`.
- Le Rules Reference 1.8 donne ATK et SCH aux vilains et sbires : un ennemi qui s'active « utilise » donc lui aussi un pouvoir de base, et « or an enemy activates » serait
  redondant si « a character » incluait les ennemis.
- Lectures : (A) « a character » = personnage AMI (identité ou allié) ; chaque activation d'ennemi retire 1 compteur par l'autre moitié de la phrase ; (B) « a character » =
  n'importe quel personnage, ennemis compris : une activation d'ennemi retire alors 2 compteurs (une pour le pouvoir de base, une pour l'activation).
- En jeu : (B) double la vitesse du cycle jour / nuit pendant la phase du méchant (et le nombre de menaces de hf406b, qui se lit sur les compteurs).
- Recommandation : **(A)**. **Choix provisoire codé : (A)** (`AbilitesDuTemps`).

### 3. Le « + » étoilé de l'escalade du stade 3B (hf406b)
Scan : `<ZIP>/Scenario/Black Queen/6b.png` : la case d'escalade imprime « +2[per_hero]★ ».
- Lectures : (A) l'escalade imprimée (+2 par joueur) s'applique ET la Réponse forcée ajoute 1 menace par compteur de temps ; (B) l'étoile signifie que l'escalade est REMPLACÉE
  par le texte : seule la Réponse forcée ajoute de la menace.
- En jeu (cible 17 par joueur) : à 2 joueurs, (A) ≈ 4 + jusqu'à 6 = 10 par round (la partie est perdue en 4 rounds) ; (B) jusqu'à 6 par round (6 rounds).
- Recommandation : **(A)** (les deux imprimés sont appliqués, sans interprétation). **Choix provisoire codé : (A)**.

### 4. Le « +1★ ATK » du Darkhold (hf362)
Scan : `<ZIP>/Modules/darkhold/2.png` : la case porte « +1★ ATK ».
- Lectures : (A) +1 ATK permanent tant que le Darkhold est attaché à Selene ; (B) l'étoile renvoie au texte : le +1 ne vaut que pour l'attaque où l'Interruption forcée donne la carte de
  boost supplémentaire.
- En jeu : (B) rend le bonus conditionnel à un compteur Darkspell restant ; (A) le donne pendant les deux utilisations ET les activations de complot.
- Recommandation : **(A)** (valeur de `desc` lue par le moteur, comme `hf107`). **Choix provisoire codé : (A)**.

### 5. Eternal Manipulation (hf363) sans allié, ou avec Darkhold attaché : quel effet résout ?
Scan : `<ZIP>/Modules/darkhold/3.png` : « If Darkhold is attached to the villain, attached this to your ally with highest hit-point, Remove 1 darkspell counter from Darkhold. Otherwise, find Darkhold
attachment and reveal it. »
- Lectures sur « no ally » : (A) la carte ne s'attache pas, est défaussée, et le compteur Darkspell est retiré quand même (les deux instructions sont indépendantes) ; (B) sans allié
  le sort « rate » : pas de compteur retiré.
- Lectures sur « highest hit-point » : (A) PV RESTANTS (comme « highest remaining hit-point » de Hyponotic Trance) ; (B) PV imprimés.
- En jeu : (A) un sort fait toujours consommer le Darkhold ; (B) un joueur sans allié ne le fait pas consommer.
- Recommandation : **(A) pour les deux**. **Choix provisoire codé : (A)/(A)** (hf363.py).

### 6. Hyponotic Trance (hf413-hf415) : « the ally » est-il l'allié de TOUT joueur ?
Scan : `<ZIP>/Scenario/Black Queen/13.png` : « Attach to the ally with the highest remaining hit-point without Hyponotic Trance attached. »
- Lectures : (A) n'importe quel allié en jeu (aucun « your ») ; (B) un allié du joueur qui révèle la carte (le « you » de l'Action de héros).
- En jeu : identique en solo ; à plusieurs, (A) peut hypnotiser l'allié d'un autre joueur.
- Recommandation : **(A)** (le texte n'écrit pas « your », contrairement à hf363). **Choix provisoire codé : (A)**.

### 7. Immortal Moon Goddess (hf422) : que fait « cannot be defeated » avec des PV à 0 ?
Scan : `<ZIP>/Scenario/Black Queen/22.png`.
- Lectures : (A) Selene reste en jeu avec ses dégâts (elle peut en cumuler) ; quand la protection tombe (le jour revient, ou la manigance quitte le jeu) et qu'elle est à 0 PV ou moins,
  elle est vaincue tout de suite ; (B) la défaite est seulement ANNULÉE à chaque fois, et ne se relance pas quand la protection tombe (elle attend le prochain dégât).
- Recommandation : **(A)** (modèle Deathbird `gs115`). **Choix provisoire codé : (A)**.

## RÉPONSES DE L'UTILISATEUR (01/11/2026, une à une, cartes montrées)
Les 7 réponses retiennent la lecture recommandée = le choix provisoire déjà codé. Aucun changement de code.
1. Eternal Night : la nuit arrive avec exactement 3 par joueur. 2. « a character » = personnage ami seulement. 3. Escalade 3B ET Réponse forcée s'appliquent. 4. Darkhold +1 ATK permanent. 5. Eternal Manipulation sans allié : compteur Darkspell retiré quand même ; « highest hit-point » = PV restants. 6. Hyponotic Trance : n'importe quel allié en jeu. 7. Immortal Moon Goddess : vaincue tout de suite quand la protection tombe.
