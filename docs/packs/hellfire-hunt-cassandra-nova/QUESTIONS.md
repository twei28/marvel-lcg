# Hellfire Hunt, scénario 5 « Cassandra Nova » : VRAIS doutes de règle (à poser à l'utilisateur, un par un, image à l'appui)

Contexte : l'agent qui a porté ce scénario ne pouvait pas interroger l'utilisateur. Chaque doute ci-dessous a reçu un **choix provisoire**, codé et testé,
documenté dans le script de la carte. Les scans sont dans `/tmp/claude-29999/-home-oem-Desktop-Marvel-LCG/6c912ee0-c9ba-469c-a5ba-e4fc4b30f45a/scratchpad/hh/Hellfire Hunt Campaign/`
(éphémère) ; les images du jeu (JPEG 615 px) sont dans `Fusion/marvel-lcg-src/assets/pics/<card_id>.jpg`.
FAQ du livret p.22 (scénario 5) déjà appliquée : options de Cassandra Domination qui DISPARAISSENT quand elles sont impossibles (voir hf607 ci-dessous).

## 1. hf608 / hf609 « Exploding Their Head » (obligation) : `Scenario/Cassandra Nova/8.png` et `9.png` ; `assets/pics/hf608.jpg`
Texte : « Each encounter card you revealed gains peril. **Forced Response** : After your turn ends, discard cards you control that the total resource cost of
cards is at least 2. Take 1 damage for each card you discarded. Then, discard this card. Otherwise, deal yourself 1 facedown encounter card. »
- Lectures possibles : (a) **retenue** : « cards you control » = alliés, améliorations et soutiens ; coût = coût IMPRIMÉ ; le joueur choisit les cartes une à une
  jusqu'à atteindre 2 ; il peut en défausser davantage (1 dégât chacune) ; si tout ce qu'il contrôle vaut moins de 2, « Otherwise » : 1 carte rencontre face cachée et
  l'obligation RESTE ; (b) « cards you control » inclut aussi l'identité ou les cartes de la zone de victoire (peu plausible) ; (c) « Otherwise » vise la phrase
  « Then, discard this card » seule : l'obligation serait toujours défaussée.
- Ce que ça change EN JEU : avec (a) un joueur sans alliés ni soutiens subit une carte rencontre par tour tant qu'il n'a rien à sacrifier (c'est la pression voulue) ; avec
  (c) l'obligation disparaîtrait au premier tour pour 0 dégât.
- Recommandation : (a). Le montage est testé (4 cas `hf608`/`hf609`).
- Sous-doute : « Each encounter card you revealed gains peril » : lu comme « chaque carte rencontre révélée PAR LE PORTEUR de l'obligation, tant qu'elle est en jeu » (Péril posé juste avant la résolution).

## 2. hf376 « Mind Shatter » (module Mind Control) : `Modules/Mind Control/6.png` ; `assets/pics/hf376.jpg`
Texte : « Peril. **When Revealed** : You are confused. You may discard any number of cards from your hand. Then, deal X damage to each identity in play, where X is equal to
half of the number of cards from your hand. »
- Lectures : (a) **retenue** : X = moitié du nombre de cartes qui RESTENT en main après la défausse facultative, arrondie au SUPÉRIEUR (c'est ce qui donne un sens à « you may discard » :
  on peut réduire les dégâts de tous les héros en se défaussant) ; (b) X = moitié des cartes défaussées (alors défausser serait toujours nuisible : absurde) ; (c) arrondi à l'inférieur.
- Ce que ça change EN JEU : main de 3 cartes : 2 dégâts (a, arrondi sup.) ou 1 (c) à CHAQUE identité ; en multijoueur c'est la main de celui qui révèle la carte qui fixe X pour tous.
- Recommandation : (a), arrondi supérieur (règle générale du jeu pour « half »).

## 3. hf607 « Cassandra Domination » (environnement) : `Scenario/Cassandra Nova/7.png` ; `assets/pics/hf607.jpg`
Texte : « ... remove 3 Cassandra Controls counter from it → you choose one : place 2 threat on each scheme, stun and confuse your identity, or deal 3 indirect damage to another friendly character. »
La FAQ p.22 tranche les exclusions, pas ces trois points :
- (a) « each scheme » : retenu = TOUTES les manigances en jeu (principale ET annexes). Alternative : manigances principales seulement.
- (b) « another friendly character » : retenu = alliés de tous les joueurs ET identités des AUTRES joueurs (jamais la sienne, FAQ « you cannot damage yourself ») ; l'option est offerte tant que les
  autres personnages peuvent absorber 3 dégâts AU TOTAL (somme de leurs PV restants ≥ 3). Un allié à exactement 3 PV compte (il est vaincu par les 3 dégâts, la FAQ ne parle que de « moins de 3 »).
  Alternative : un SEUL personnage doit pouvoir absorber les 3.
- (c) quand plusieurs autres personnages existent, le joueur répartit les 3 dégâts comme pour des dégâts indirects ordinaires (`AssignDamage`) entre eux.
- Ce que ça change EN JEU : à deux joueurs sans allié l'option « dégâts » reste offerte (l'autre héros les prend) ; sinon elle disparaît.
- Recommandation : garder les choix provisoires.

## 4. hf613-hf615 « Shatter Your Mind » : `Scenario/Cassandra Nova/13.png` ; `assets/pics/hf613.jpg`
Texte : « Each time a **Cassandra Nova card** is discarded this way, place 1 Cassandra Controls counter on your identity. »
- Retenu : « Cassandra Nova card » = carte de l'ENSEMBLE de rencontre Cassandra Nova (pied de carte « CASSANDRA NOVA (n/21) » : obligations, traîtrises, manigances annexes du scénario) ; le sbire homonyme du
  module Immensity est retiré du jeu au Setup. Alternative : seulement les cartes dont le NOM est « Cassandra Nova » (il n'y en a aucune dans le deck : la carte ne ferait jamais rien).
- Recommandation : l'ensemble (seule lecture qui rende la carte utile).

## 5. hf381 « Mutant Extinction Agenda » : `Modules/Mutant Extinction Agenda/1.png` ; `assets/pics/hf381.jpg`
Texte : « Victory 1. ... This card cannot be defeated while a SENTINEL minion is in play. »
- Retenu : la défaite est REMPLACÉE tant qu'une SENTINEL est en jeu ; la manigance reste à 0 menace ; quand la DERNIÈRE SENTINEL quitte le jeu, la manigance restée à 0 menace est vaincue
  (pile de victoire, Victory 1). Sans cet ajout (le moteur n'a pas de vérification d'état) elle resterait coincée à 0 menace, impossible à contrer. Alternative : elle reste en jeu jusqu'à ce qu'on lui
  remette de la menace (jamais en pratique).
- Recommandation : garder.

## 6. hf604b / hf605b / hf606b : coût « Discard N cards from the top of the encounter deck » quand le deck a moins de N cartes
Retenu : le coût ne peut pas être payé (l'Action n'est pas proposée) ; le moteur ne remélange pas la défausse en cours de défausse. À la fin d'une longue partie (deck de rencontre presque vide) on ne pourrait
donc plus retirer de compteur. Alternative RR : remélanger la défausse et continuer (avec le jeton d'accélération de la règle de remélange).
Recommandation : à trancher si l'on joue des parties très longues ; aucune partie d'autoplay n'a atteint ce cas (voir GABARITS.md).

## 7. hf621 « The Hate Machine » : `Scenario/Cassandra Nova/21.png` ; `assets/pics/hf621.jpg`
« While at least 1 Cassandra Control counter on your identity, you cannot attack Cassandra Nova or thwart the main scheme. »
Retenu : « you » = le joueur et son identité/héros ; ses ALLIÉS peuvent encore attaquer Cassandra Nova et contrer la manigance principale (cas testés). Alternative : ses alliés sont bloqués aussi.
Recommandation : garder (cohérent avec « you » partout ailleurs dans le jeu).
