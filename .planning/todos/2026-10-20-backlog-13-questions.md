# Questions ouvertes, backlog 13 (réserves de gabarits, 20/10/2026)

Rien ci-dessous n'a été tranché ni codé. Une question par carte (ou par
groupe de cartes au texte identique), à poser une à la fois, en montrant
d'abord le scan indiqué (règle de `PROCESSUS-CARTE.md` étape 3 et mémoire
« questions une à une, avec image »).

## Q1. 60040a / 60040b / 60040c Photographic Reflexes : l'action doit-elle être offerte quand aucun événement glissé n'est payable ?

**Scan à montrer** : `Fusion/marvel-lcg-src/assets/pics/60040a.jpg` (les trois
variantes ont le même texte, seule l'icône de ressource change).

**Texte imprimé** : « If you are in hero form, you can discard Photographic
Reflexes from your hand to play an event tucked under Echo as if it were in
your hand. Reduce the cost to play that event by 2. You cannot trigger Echo's
"Watch and Learn" ability for that event. »

**Ce qui a été constaté (20/10/2026)** :

- En autoplay (deck `echo` contre Rhino, graine 4, journal
  `/tmp/autoplay_echo_rhino_normal_equilibre_4.log`, lignes 297 à 305) : In
  Harm's Way est glissé sous Echo, le pilote clique Photographic Reflexes
  (60040b) en main, la carte est **défaussée**, puis le paiement de
  l'événement est annulé faute de ressources : **la carte est perdue, rien
  n'est joué**.
- Reproduit au harnais (cas d'observation non conservé) : Hit and Run (18020,
  coût 3, donc 1 après réduction) glissé, une seule Photographic Reflexes en
  main et rien d'autre pour payer. Le **chemin A** (cliquer la carte en main)
  est offert, Photographic Reflexes part en défausse, Hit and Run reste glissé.
- Dans la même position, le **chemin B** (cliquer l'événement glissé) est
  REFUSÉ par le moteur (cas « SEULE en main, elle ne peut PAS payer la carte
  qu'elle vient d'autoriser », correctif du 25/09/2026). Les deux chemins se
  comportent donc différemment.

Le code actuel (`fne/echo/__init__.py`, condition `il_y_a_un_evenement_glisse`)
ne vérifie que la PRÉSENCE d'un événement glissé, pas qu'il puisse être joué.

**Question** : quand aucun événement glissé ne peut être joué (pas de quoi
payer même après la réduction de 2, ou aucune cible légale), que doit faire
Photographic Reflexes en main ?

- **Option A (recommandée) : l'action n'est pas offerte.** Elle n'apparaît
  que si au moins un événement glissé peut réellement être joué (coût réduit
  payable avec ce qui reste, cible légale présente). En jeu : impossible de
  perdre la carte pour rien ; les chemins A et B se comportent pareil dans
  cette position.
- **Option B : on garde le comportement actuel.** L'action est offerte dès
  qu'un événement est glissé ; si le paiement échoue ou est annulé, la carte
  est quand même défaussée. En jeu : un joueur peut gaspiller sa carte (et le
  pilote automatique le fait) ; le choix reste au joueur.
- **Option C : offerte, mais annulable sans perte.** Si l'événement n'est
  finalement pas joué, Photographic Reflexes revient en main. En jeu : pas de
  perte, mais le joueur peut « essayer » puis renoncer, ce qu'aucune autre
  carte du moteur ne permet aujourd'hui.
- **Autre (préciser).**

**Ce qui dépend de la réponse** : le statut « Carte terminée » des trois
gabarits (`2026-09-21-echo-gabarits-processus-carte.md`) ; un cas sujet et un
témoin seront écrits pour l'option retenue.

## Q2. dt087, dt100, dt105, dt106, dt107 (Fleeting et Alias) : peut-on monter un deck de TEST pour l'autoplay ?

**Scans à montrer** : `Fusion/marvel-lcg-src/assets/pics/dt087.jpg`, puis
`dt105.jpg` (les quatre porteurs d'Alias ont la même mécanique ; `dt100`,
`dt106`, `dt107` sont à côté).

Question de MÉTHODE, pas de lecture de carte : elle est identique pour les
cinq cartes, d'où une seule question. La séparer en cinq si l'utilisateur le
préfère.

**État** : les cinq cartes ont tous leurs cas au harnais (10/10 au filtre
`[dt]` le 20/10/2026) et leur preuve par substitution (29/09). Seule l'étape 8
(autoplay, 8 parties) manque : aucun deck ne contient ces cartes. Les decks de
départ du pack `determination` ont été supprimés le 05/09/2026 ; le seul deck
qui cite `dt105`, `deck/starter/venompool.json`, l'exclut explicitement
(`collision_note`). La règle « pas de deck inventé »
(`KIT-CHATGPT-CREATION.md`) interdit d'écrire un deck de héros sans liste
d'auteur. Or les cartes restent dans `cards.json` et dans l'éditeur de deck :
un joueur peut donc les mettre dans un deck.

**Question** : comment fermer l'étape 8 de ces cinq gabarits ?

- **Option A (recommandée) : un deck de TEST, jamais distribué.** Un fichier
  de deck rangé hors de `deck/starter` (par exemple sous `tools/`), donné à
  `autoplay.py --deck <chemin>` seulement : un héros déjà en base, l'aspect
  Determination, les cinq cartes et des homonymes (Deadpool `dt016`) pour que
  l'Alias puisse partir. En jeu : rien ne change pour les joueurs (le deck
  n'apparaît nulle part) ; on obtient la preuve qu'aucune exception avalée ne
  sort de ces cartes dans une vraie boucle de partie.
- **Option B : déclarer l'étape 8 hors périmètre** pour ces cartes, tant
  qu'aucune decklist n'existe, et clore les gabarits sur « OUI, autoplay hors
  périmètre ». En jeu : rien ne change ; le risque d'une exception avalée en
  partie réelle (deck construit par un joueur) reste non mesuré.
- **Option C : attendre une decklist de l'auteur** de l'aspect Determination.
  En jeu : rien ne change ; la réserve reste ouverte sans date.
- **Autre (préciser).**
