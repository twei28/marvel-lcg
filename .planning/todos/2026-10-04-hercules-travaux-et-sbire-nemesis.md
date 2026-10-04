# Hercules : Travaux/Dons jamais mélangés, sbire némésis en double (04/10/2026)

Signalements d'un joueur, relayés par l'utilisateur :
1. « Pour Hercules, je tire toujours les travaux et les dons dans le même
   ordre. Le mode aléatoire ne fonctionne pas ? »
2. « si je joue Faire face au passé, j'ai Arès et l'Hydre en jeu (et non le
   sbire némésis principal : Arès) »

## Causes

1. `59001b.py` posait les 3 Travaux et les 3 Dons dans le deck annexe sans
   mélanger. Encart officiel (mc59_rulesheet) : « shuffle the three gift cards
   together to form the gift deck and the three labor cards to form the labor
   deck ».
2. `IsNemesis` (card_encounter.py) : le marqueur `nemesis_of_player` du
   02/09/2026 rendait True pour TOUTE carte du set némésis, avant de regarder
   la mention « Nemesis » du sbire. Le second sbire du set passait pour le
   sbire némésis : Lernean Hydra (Hercules), Hydra Mercenary (Black Widow)…
   37 héros officiels touchés, via `49022` Face the Past et `01190` Shadow of
   the Past (set Standard, donc chaque partie).

## Décisions de l'utilisateur (questions une à une)

- Règle : si le set némésis du joueur contient un sbire MARQUÉ « Nemesis »,
  lui seul compte ; sinon le sbire du set compte (Zzzax emprunté par Viv
  Vision, sbire officiel de module sans mention, et les 6 sets maison à un
  seul sbire).
- Données : mention ajoutée aux 3 sets maison ambigus (deux sbires, aucune
  mention), d'après leur texte « (X's nemesis minion) » : bl013 Dracula,
  rs016 Ice Queen, 65012 The Reyna Sirena.

## Extensions du même chantier (questions une à une, 04/10/2026)

- Audit de TOUS les decks formés en début de partie (agent) : un bug réel,
  `39015a` Spiral (Cornered! toujours au-dessus du deck Show), et deux decks
  justes par effet de bord seulement, `04061a` Crossbones et `21129` Infinity
  Gauntlet (`SetAsideDeck.PushCards` ne mélange pas). Les trois mélangent
  maintenant explicitement. Une vingtaine d'autres decks vérifiés OK.
- Fouille d'un deck (Rules Reference v1.8, Search / Find), choix de
  l'utilisateur : remélange quand le deck a VRAIMENT été fouillé (carte sortie
  du deck, rien trouvé, fouille facultative refusée après avoir vu le deck) ;
  pas de mélange quand la carte vient d'une zone publique (défausse). Seul trou
  du moteur : la fouille facultative refusée (`search_internal.py`).

## Preuves communes

- Batterie complète finale (PARALLELES=4) : **2627/2633**. Les 6 rouges :
  `vv001a` vert rejoué seul (artefact du parallèle) ; `sg006`, `sg007`,
  `sg009`, `sg013` et `statistiques — dégâts séparés par siège` restent rouges
  SANS mes changements (fichiers moteur remis à leur version d'avant, puis
  restaurés) : défauts antérieurs, hors de ce chantier.
- Autoplay : Hercules 8 parties + témoin Spider-Man 8 parties (Rhino), puis
  Spider-Man contre Spiral, Crossbones, Thanos 8 parties chacun : 0 traceback
  sur 40 journaux. Premier Travail révélé variable selon la graine (Hydre,
  Protéger l'humanité, Pathos) ; premier Show de Spiral variable (Cornered! ou
  The Mojo Files). Spiral finit au round 1 : le pilote abuse de l'Action
  facultative de The Search for Spiral (2 dégâts à soi), sans lien.

## Gabarits PROCESSUS-CARTE

### 59001b : Hercules (alter ego)

- [x] Étape 2 : référence `sg001b` (`ShuffleAllTo` dans le deck annexe) et
      `Deck.Shuffle` ; le dessus se cherche par trait (`GetAdditionalDeckTop`).
- [x] Étape 5 : « begins the game with a Labor deck and a Gift deck (See
      insert) » ; encart mc59 : « shuffle the three gift cards … and the three
      labor cards ». Mélange ajouté après la pose.
- [x] Étape 6 : 3 Travaux, 3 Dons : vérifié par le cas (6 cartes).
- [x] Étape 7 : « 59001b Hercules — mise en place : … MELANGES », rouge avant
      (for_undo_shuffle = 0), vert après. Cas 59002 « le sbire marqué vaincu… »
      rendu indépendant du hasard (`PutOnAdditionalDeckTop('59007')`).
- [x] Étape 7 bis : limite imprimée ? NON (ici).
- [x] Étape 8 : 8 parties, témoin Spider-Man, 0 traceback.
- [x] Étape 8 bis : change ce qu'on voit ? NON (ordre seulement).

Carte terminée : OUI

### 49022 : Face the Past (et `IsNemesis`, `01190` Shadow of the Past)

- [x] Étape 2 : `01190` Shadow of the Past (même recherche `is_nemesis`).
- [x] Étape 5 : « your nemesis minion » = le sbire marqué Nemesis. Règle de
      l'utilisateur : si le set en a un marqué, lui seul ; sinon le sbire du
      set (Zzzax de Viv Vision).
- [x] Étape 6 : rien de chiffré touché.
- [x] Étape 7 : cas Face the Past Hercules, Shadow Hercules, Black Widow, Red
      Sonja, Wave : rouges avant, verts après ; témoins Viv Vision / Spider-Man
      verts avant et après.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : 8 parties Hercules, 0 traceback.
- [x] Étape 8 bis : NON (aucun nouveau dessin).

Carte terminée : OUI

### bl013 Dracula, rs016 Ice Queen, 65012 The Reyna Sirena (données)

- [x] Mention `"Nemesis"` ajoutée d'après le texte « (X's nemesis minion) ».
- [x] Cas rs016 et 65012 rouges avant / verts après. bl013 : Slayer mélange
      les Vampires au deck rencontre dès la mise en place, donc Shadow of the
      Past (pile mise de côté seulement) ne peut pas rougir ; c'est Face the
      Past, qui fouille aussi le deck rencontre, qui porte le cas : « 49022 Face
      the Past — Blade », vert avec la mention, ROUGE sans (bl014 en jeu).

Carte terminée : OUI

### 39015a Across the Mojoverse, 04061a Attack on Mount Athena, 21129 Infinity Gauntlet

- [x] Étape 2 : `50104a` MODOK, `04128a` Red Skull (`ShuffleAllTo`).
- [x] Étape 5 : « Shuffle each other SHOW … together with the Cornered! » ;
      « shuffle them together, and set them facedown » ; « shuffle the six
      Infinity Stone environment cards together ».
- [x] Étape 7 : trois cas « … est MELANGE », rouges avant (0 carte mélangée),
      verts après.
- [x] Étape 8 : 8 parties par scénario, 0 traceback.
- [x] Étape 8 bis : NON.

Cartes terminées : OUI

### Moteur : fouille facultative refusée (`search_internal.py`)

- [x] Cas Echo 60037b « fouille FACULTATIVE refusée » : rouge sans le
      correctif, vert avec (substitution faite). Kate Bishop : défausse (pas
      de mélange, contre-cas d'absence assumé), rien trouvé (mélange), carte
      dans le deck (mélange).
