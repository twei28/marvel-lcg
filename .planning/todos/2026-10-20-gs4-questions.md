# Galactic Storm, lot GS-4 (scénario 1 « Kree Sentry » gs076-gs090 et modulaire « Imperial Guard » gs091-gs113) : questions pour l'utilisateur (20/10/2026)

Une question par point, recommandation en premier, ce que chaque option change en jeu. La lecture recommandée est
celle qui est codée aujourd'hui ; rien d'autre n'a été tranché en silence. Scans : copies réduites dans
`Fusion/marvel-lcg-src/assets/pics/<card_id>.png` (dépôt principal), originaux dans
`sauvegardes-serveur/scans-originaux/<card_id>.png`.

## Décisions déjà prises (GS-0, briques communes), appliquées dans ce lot : closes

- **Conventions de lecture** (« ★ » devant une capacité et en exposant d'une statistique = renvoi au texte ; étoiles
  blanches à contour sous CTR/ATQ d'un allié = dégâts consécutifs ; pastille orange = points de vie ; silhouette après
  un nombre = « par joueur » ; Y rouge = une icône de boost) : appliquées telles quelles.
- **Livret 1.2 partout** : règles de Kree Sentry (p.9-10), d'Imperial Guard (p.8), FAQ p.22 (Intruder Elimination).
- **Attaque d'un ennemi contre un allié** : `ally_attack_is_against_player=False` (le livret p.4 s'applique, les
  capacités « attacks you » ne partent pas, le « vous » d'un Boost reste le contrôleur de l'allié) ; **contre un sbire**
  : `players_may_defend=True` (les joueurs peuvent défendre). Rick Jones (gs081) reprend la même règle pour le
  détournement de son Interruption forcée.
- **Ids** : `gs` + numéro imprimé sur trois chiffres ; Hobgoblin, imprimé « 99 », est `gs099` (Maelstrom de Quasar est
  `gs099q`) ; un card_id par numéro, exemplaires comptés dans les paquets.
- **Icônes de ressource** (gabarit IMPERIAL-GUARD-GABARITS.md et KREE-SENTRY-GABARITS.md) : identifiées par découpe,
  jamais à vue. Éclair = [energy] (Electron), nœuds reliés = [mental] (Nightside), poing = [physical] (Pulsar et les deux
  poings de l'Optic Blast Cannon), étoile = [wild] (Fang) ; chaque forme comparée à une carte du même auteur dont la
  ressource est déclarée (sk148 et sk152 pour les trois premières, ab007 / rg011 / tt006 pour l'étoile). Icône « avion +
  croix » de Locking on Target = Amplify (identique à sk252 et gs133).

## Q1. gs080b : « If this stage is completes, the players lose the game »

Le mot imprimé est « completes » (coquille probable). Scan : `gs080b.png`. Même cas que Supreme Intelligence gs199b (Q4
du lot GS-8, tranché « forme officielle »).
1. **(Recommandé) « If this stage is completed »** : dernier stade du scénario, l'accomplir fait perdre les joueurs.
   Change en jeu : la partie se perd quand la menace de 2B atteint 10 par joueur (règle de base d'un dernier stade).
2. Lecture littérale impossible à jouer (« completes » n'est pas un événement) : rien d'autre ne serait codable.
3. Autre (préciser).

## Q2. gs096 Electron, gs105 Nightside, gs107 Pulsar : une carte WILD en main compte-t-elle comme ressource [energy] / [mental] / [physical] ?

Texte : « Discard a [energy|mental|physical] resource from your hand. If you cannot, resolve the Special ability... ».
Une carte à ressource wild (Spider-Woman, Genius wild...) peut payer n'importe quel coût, mais le moteur officiel ne
la compte pas comme une ressource d'un type précis quand une carte vérifie « a printed [x] resource »
(`convert_green_res=False`). Scans : `gs096.png`, `gs105.png`, `gs107.png`.
1. **(Recommandé) Une carte wild n'est PAS une ressource [energy] / [mental] / [physical] imprimée** (convention du
   moteur, déjà appliquée aux cartes de Binary). Change en jeu : un joueur dont la main n'a que des cartes wild subit le
   Special de l'environnement.
2. Une carte wild compte comme chaque type. Change en jeu : un joueur à main wild défausse toujours une carte et
   évite le Special, ce qui adoucit nettement les trois sbires.
3. Autre (préciser).

## Q3. gs079b / gs080b : « deal 1 damage to each character for each copy of Sentry's Grasp attached to it »

Un personnage portant deux Poignes (Rick Jones dans le scénario Expert, dès la mise en place). Scans : `gs079b.png`,
`gs080b.png`.
1. **(Recommandé) Une seule instance de dégâts égale au nombre de Poignes** (2 dégâts d'un coup). Change en jeu : une
   carte Tenace ou une prévention de dégâts annule les 2 dégâts d'un seul coup.
2. Une instance de 1 dégât PAR Poigne (deux instances). Change en jeu : une carte Tenace n'annule que le premier dégât,
   le second passe.
3. Autre (préciser).

## Q4. gs085 Death Grip : une Poigne qui porte 3 ou 4 dégâts quand Death Grip quitte le jeu

Texte : « Sentry's Grasp is set aside when there is 5 or more damage on it instead of 3. » La Poigne : « If there is 3 or
more damage here, set Sentry's Grasp aside. » Scan : `gs085.png`.
1. **(Recommandé) La condition « 3 dégâts ou plus » est un état : dès que Death Grip s'en va, une Poigne à 3 ou 4 dégâts
   est mise de côte aussitôt.** Change en jeu : vaincre Death Grip libère les héros d'une Poigne déjà bien abîmée.
2. La Poigne ne se met de côté qu'au prochain dégât (déclencheur, pas état). Change en jeu : une Poigne à 4 dégâts
   survit jusqu'à sa prochaine blessure.
3. Autre (préciser).

## Q5. gs090 Intruder Elimination : qui choisit « a non-KREE character », et parmi quoi ?

Texte : « When Revealed: Choose a non-KREE character. Kree Sentry attacks that character (even if that character is an
alter-ego). » Scan : `gs090.png`.
1. **(Recommandé) Le joueur qui révèle la carte choisit, parmi TOUS les personnages en jeu non KREE** (identités de tous
   les joueurs, alliés, Rick Jones compris, sbires ; ni la Poigne, qui n'est pas un personnage, ni Kree Sentry). Si le
   choix est l'identité du premier joueur, Kree Sentry attaque Rick Jones (FAQ p.22). Change en jeu : on peut diriger
   l'attaque vers un sbire pour gagner le surge (« If an enemy was attacked this way »), ou vers Rick Jones.
2. Le premier joueur choisit pour tout le groupe. Change en jeu : à plusieurs joueurs, un seul décide de la cible.
3. Seulement parmi les personnages du joueur qui révèle. Change en jeu : plus de choix d'un sbire.
4. Autre (préciser).

## Q6. gs097 Fang : « a card you control with a printed [wild] resource »

1. **(Recommandé) Les cartes EN JEU sous le contrôle du joueur** (alliés, améliorations, soutiens ; pas la main).
   Change en jeu : seules les cartes posées peuvent être défaussées.
2. Les cartes de la main aussi. Change en jeu : le sbire devient aussi sévère qu'Electron.
3. Autre (préciser).

## Q7. gs098 Gladiator : « a non-scenario specific ally you control »

1. **(Recommandé) Rick Jones et les autres alliés de rencontre (classe Encounter) ne comptent pas** : Gladiator ne peut
   défaire que les alliés de joueur (basic, aspect, propres à l'identité, de campagne). Change en jeu : Rick Jones n'est
   jamais sacrifié par Gladiator (la perte de partie ne vient pas de lui).
2. Seuls les alliés de CE scénario sont exclus ; un allié de rencontre d'un autre scénario compte. Change en jeu :
   identique ici (aucun autre allié de rencontre n'est jouable dans ce scénario).
3. Autre (préciser).

## Q8. Imperial Guard utilisé hors de la règle des neuf cartes

Le livret (p.8) : « whenever this modular set is chosen for a scenario, players only include nine cards from it »
et « Elsewhere it can be used like any encounter set ». Le moteur ne distingue pas « modulaire » et « ensemble de
rencontre » : le fichier `gs_imperial_guard.json` porte la règle des neuf cartes dans tous les cas.
1. **(Recommandé) Garder la règle des neuf cartes partout** (c'est ainsi que les scénarios 1, 2 et 4 l'emploient).
   Change en jeu : l'ensemble n'est jamais joué en entier.
2. Ajouter un second fichier `gs_imperial_guard_complet` (23 cartes, les trois environnements entrent par leur
   révélation) pour les parties « personnalisées ». Change en jeu : un choix de plus à l'écran de préparation ;
   besoin de dire quelle carte est « Elsewhere ».
3. Autre (préciser).

## Q9. Rick Jones dans une partie à plusieurs joueurs : qui contrôle Rick quand le premier joueur change ?

Texte : « The first player controls Rick Jones. » Mis en jeu sous le contrôle du premier joueur à la mise en place ;
le contrôle ne change pas si le jeton de premier joueur passe à un autre.
1. **(Recommandé) Le contrôle reste au joueur de départ** (le texte dit « the first player » au Setup). Change en jeu :
   « Kree Sentry attacks you » est détourné pour le joueur de départ seulement.
2. Le contrôle suit le jeton de premier joueur à chaque round. Change en jeu : la protection de Rick passe d'un joueur
   à l'autre ; nécessite un transfert de contrôle à chaque début de round (non codé).
3. Autre (préciser).
