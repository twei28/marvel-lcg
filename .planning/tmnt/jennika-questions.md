# Jennika (TMNT Heroes v3, Inkwire) : questions en attente

Écrites le 16/10/2026 pendant la création du héros (agent sans accès à l'utilisateur). Chaque lecture
provisoire est implémentée ET marquée `TODO-QUESTION` dans le script de la carte. Lecture recommandée en premier.
Scans : `.planning/tmnt/pics-jennika/<card_id>.jpg` (copie versionnée) ; originaux dans le zip
« TMNT Heroes-20261014T200300Z-1-001.zip », dossier « TMNT Heroes/Jennika v3/ ».

---

## Q1 : `tj001a` Jennika, Ninja Senpai : « Limit once per round for each Shinobi »

- Scan : `.planning/tmnt/pics-jennika/tj001a.jpg` (zip : `0 Jennika.png`).
- Texte anglais exact : « *Ninja Senpai* — **Interrupt**: When you play a Shinobi card, Jennika gets +1 THW,
  +1 ATK, and +1 DEF until the end of the round. *(Limit once per round for each Shinobi.)* »
- Lectures :
  1. **(recommandée, implémentée)** une fois par round **pour chacune des quatre classes Shinobi** (Bushido,
     Ninjutsu, Kuji-Kiri, Taijutsu) : quatre capacités, chacune `LimitOncePerRound`. Appui : le dos du Path dit
     « Dual Shinobi cards trigger both Shinobi types » (le mot « Shinobi » y désigne une classe) ;
  2. une fois par round **pour chaque carte Shinobi** (une 2e copie de la même carte ne redonne rien, mais une
     autre carte de la même classe redonne le bonus) ;
  3. une seule fois par round, toutes classes confondues.
- Ce que ça change en jeu : avec la lecture 1, jouer Moonlighting (Ninjutsu) puis Fearless Resolve (Bushido) dans
  le même round donne +2/+2/+2 ; avec la 3 seulement +1/+1/+1.
- Code : `cards/pack/jennika/jennika/tj001a.py`.

## Q2 : quelles cartes de Jennika sont des cartes « Shinobi » ?

- Scans : `tj003.jpg`, `tj004.jpg`, `tj005.jpg`, `tj006.jpg` (portent « This card is both a Jennika card and a
  Kuji-Kiri / Taijutsu / Ninjutsu / Bushido card ») ; `tj002.jpg` (Composure), `tj007.jpg` (Crib), `tj008.jpg`
  (Bow), `tj009.jpg`, `tj010.jpg` (Tekko-Kagi) n'impriment AUCUNE classe.
- Texte anglais exact du dos du Path (`Sosaiken Cardback.png`, non transcrit en carte) : « You may add **any
  combination** of Shinobi cards *(Bushido, Ninjutsu, Kuji-Kiri, or Taijutsu)* to your deck. »
- Lectures :
  1. **(recommandée, implémentée)** est Shinobi une carte qui porte l'une des quatre classes ; les cinq cartes
     sans classe (Composure, Crib, Bow, Tekko-Kagi x2) ne le sont pas ;
  2. toutes les cartes de Jennika sont Shinobi (le héros EST le Path Shinobi) : Composure, la Crib, l'arc et les
     Tekko-Kagi déclencheraient aussi Ninja Senpai et la Voie, et la ressource des Tekko-Kagi les paierait.
- Ce que ça change en jeu : avec la lecture 2, la ressource wild des Tekko-Kagi paie aussi Composure et la Crib, et
  Ninja Senpai se déclenche sur presque toutes les cartes jouées (il lui faudrait alors une limite par classe
  « sans classe »).
- Code : `desc.Class` (`data/cards.json`), `CarteShinobi()` dans `cards/pack/jennika/jennika/__init__.py`.

## Q3 : `tj011` Sōsaiken : type imprimé « PATH »

- Scan : `tj011.jpg` (zip : `Sosaiken.png`) ; dos : `Sosaiken Cardback.png`.
- Texte anglais exact : « Permanent. **Response**: After you play a Shinobi card, exhaust this card → draw 1 card. »
  Type imprimé : PATH ; trait : SENPAI ; « JENNIKA (16/16) ». Jenny : « **Setup**: Put the Sōsaiken Path into play
  under your control. »
- Lectures :
  1. **(recommandée, implémentée)** le moteur n'a pas de type « Path » : la carte est un **Support** (Permanent, sans
     coût, mise de côté et mise en jeu par le Setup de Jenny, modèle `58002` Ionic Physiology de Wonder Man). Rien
     dans le pack ne distingue un Path d'un Support ;
  2. créer un vrai type de carte « Path » dans le moteur (fichier partagé `card_type/`, plusieurs enregistrements) ;
     un effet qui parle de « soutien » ne toucherait plus la Voie.
- Ce que ça change en jeu : avec la lecture 1, un effet « défaussez / inclinez / redressez un soutien » pourrait
  viser la Voie (Permanent la protège de la défausse par un autre set, mais pas de l'inclinaison).
- Code : `data/cards.json` (`tj011`, type `Support`).

## Q4 : `tj011` : mise de côté ou dans le deck ?

- Scan : `tj011.jpg` ; Jenny : voir Q3.
- Lectures :
  1. **(recommandée, implémentée)** la Voie est **mise de côté** (hors des 15 cartes du deck, `set_aside`, créée par
     `BeginGameWithSetAside`) : la main de départ n'est pas amputée ;
  2. la Voie est dans le deck (16 cartes) et le Setup la cherche (décision utilisateur du 15/10/2026 pour
     `tm009` I'm Here to Help de Michelangelo, « 12/15 »).
- Ce que ça change en jeu : avec la lecture 2, la Voie occupe une place de la main de départ avec probabilité
  5/16 (elle est ensuite posée par le Setup) et le deck compte 16 cartes.
- Code : `deck/starter/jennika.json` (`set_aside`), `cards/pack/jennika/jennika/tj001b.py`.

## Q5 : `tj003` Apparition : « Remove 2 threat from a scheme **and** confuse an enemy »

- Scan : `tj003.jpg`.
- Texte anglais exact : « **Action** *(thwart)*: Remove 2 threat from a scheme and confuse an enemy. »
- Lectures :
  1. **(recommandée, implémentée)** les deux moitiés sont indépendantes : sans manigance contrable (Crise sur la
     principale, plus de menace), l'ennemi est quand même désorienté, et inversement (modèle `tm006` Majime) ;
  2. les deux cibles sont obligatoires : la carte est injouable s'il manque l'une des deux.
- Ce que ça change en jeu : avec la lecture 2, Apparition ne se joue pas quand la seule manigance restante est un
  complot principal verrouillé par une Crise.
- Code : `cards/pack/jennika/jennika/tj003.py`.

## Notes sans question (lectures évidentes, consignées pour mémoire)

- **Paire 14/15 `tj009` + `tj010`** (Tekko-Kagi, « Other Tekko-Kagi flipped ») : illustration continue d'une carte à
  l'autre ; NON déclarée au registre des panoramas (consigne : la signaler seulement).
- **`tj014` Phantasm** : « Cloak each PHANTOMS minion in play » : Phantasm est encore en jeu pendant sa résolution
  et reçoit lui-même une carte Cloaked qui disparaît avec lui.
- **`tj008` Jennika's Bow** : « deal 1 damage to an enemy **or** remove 1 threat » : un seul des deux, au choix.
- **`tj012` Personality Adjustment** : « You may flip... Choose: » : la bascule est facultative, puis le choix est
  obligatoire ; l'option « Exhaust Jenny » n'existe qu'en forme alter ego, Jenny redressée.
- **Dos du Path** (`Sosaiken Cardback.png`) : insert de règles (construction de deck), aucune carte créée.
