# Spec : le mode manuel, ou le moteur réduit à un porte-cartes

**Date :** 18/09/2026
**Fiche d'origine :** `.planning/todos/2026-09-14-mode-manuel-sans-automatisation.md`
**Statut :** cadrée avec l'utilisateur, à relire avant le plan d'exécution.

## But

Offrir une partie où **rien n'est automatisé après la mise en place**. Le
moteur pose la table, puis se tait définitivement : il ne conduit plus, ne
demande plus rien, ne déclenche plus aucune capacité. Il ne sait plus que deux
choses, où est chaque carte et dans quel état. Tout le reste est au joueur,
comme sur Tabletop Simulator.

Deux gains visés, dans cet ordre :

1. **Jouer les cartes non implémentées.** Une carte sans script est déjà
   posable et inerte ; en manuel, c'est le joueur qui applique son texte.
2. **Corriger une erreur du moteur en pleine partie**, sans annuler dix coups.

## Ce que ce mode ne livre pas

**Les extensions non portées restent hors d'atteinte.** Leurs cartes ne sont
ni dans `data/cards.json` ni dans `assets/`. Le mode manuel n'aurait rien à
afficher. L'import de données est un chantier distinct, non cadré ici. La
fiche d'origine promettait le contraire, elle a été corrigée le 18/09/2026.

Également hors périmètre : le multijoueur en ligne, une console de commandes
brutes, et tout raccourci qui ferait exécuter une règle par le moteur.

## Décisions de cadrage

| Question | Décision |
|---|---|
| Forme du mode | Partie déclarée manuelle dès la mise en place |
| Mise en place | Automatique et **intégrale**, capacités de mise en place et mulligan compris |
| Après la mise en place | Silence total : ni phase, ni question, ni capacité, ni modificateur |
| Raccourcis « fais-le pour moi » | Aucun. Pas d'attaque assistée, pas de phase du vilain déroulée |
| Repère de tour et de phase | Aucun. Plateau nu |
| Vérification des placements | Aucune. Toute carte va sur toute pile |
| Manipulation | Calque Tabletop Simulator : glisser, clavier, clic droit |
| Statuts | Au clic droit, pas au clavier |
| Annulation | Ctrl+Z, geste par geste |
| Catalogue | Recherche par nom sur les 6217 cartes, pose directe sur la table |
| Table | Une personne, plusieurs héros, un écran |
| Fin de partie | Déclarée à la main, journal de campagne saisi à la main |

## Architecture

### 1. La règle

Une règle booléenne `mode_manuel`, sur le modèle exact de `mode_sandbox`
(`game/world/world_rule.py:71`) : posée par la liste `rules` du descripteur,
donc **conservée dans la sauvegarde**. On saura toujours qu'une partie était
manuelle. Les hauts faits ne sont pas enregistrés, au même endroit et pour la
même raison que le bac à sable (`ui-app/src/board/moteur.ts:986`), et le
rapport de bug porte la mention.

### 2. La boucle manuelle

`World.OnGameLoop` (`game/world/world.py:746`) est le seul endroit qui conduit
une partie. En mode manuel, il n'appelle pas `game_round()` mais une
`ManualLoop()` qui ne fait que trois choses en rond, jusqu'à la fin de partie :

1. attendre sur `device_manager.notify.input` ;
2. exécuter les commandes déposées (`DrainSandboxCommands`) ;
3. redessiner (`WorldRender.PresentForceNoWait`, qui existe déjà et ne sert
   qu'à ça).

Le moteur n'interroge personne : `asking_players` reste vide, donc le plateau
n'a aucune question à afficher et n'a rien à filtrer.

La mise en place n'est pas touchée : elle se déroule dans `World.Initialize`,
en amont de cette boucle.

### 3. La porte du silence

Toute capacité de toute carte, et tout effet de règle, passe par
`EventManager.BroadcastMessage` (`game/event/manager.py:650`). Une porte posée
là, plus une sur `BroadcastStackMessage`, suffit à couper la totalité des
déclenchements.

**Le récit à l'écran survit**, et ce n'est pas un hasard : les messages
appellent `Present` dans leur **constructeur**, avant l'envoi. Le plateau
continuera donc d'annoncer « carte défaussée » et le journal de le noter,
sans qu'aucune capacité ne parte.

La porte s'ouvre sur un attribut explicite, `world.manuel_actif`, mis à vrai
juste avant d'entrer dans `ManualLoop`. Surtout pas déduit de la règle seule :
la mise en place, elle, a besoin que tout fonctionne.

**Conséquence assumée, à écrire noir sur blanc dans l'aide du mode :** les
effets de règle passent par la même porte. Un sbire à zéro point de vie n'est
plus défaussé tout seul, c'est voulu ; mais les **modificateurs de
caractéristiques disparaissent aussi**. Une amélioration « +1 ATQ »
n'augmentera plus l'attaque affichée. Le plateau montre les valeurs
imprimées, le joueur compte.

### 4. Le canal des gestes

Inchangé : `/sandbox_command`, qui n'accepte que des appels `Puzzle.<methode>`
et rejette tout le reste à l'analyse syntaxique
(`engine/device/web/server/server_get.py:94`). Aucun code arbitraire ne
circule, et le mode manuel n'ouvre aucune surface nouvelle.

Les cartes sont visées **par identifiant d'objet**, jamais par nom, pour la
raison déjà documentée dans `ui-app/src/board/triche.ts`.

## Le vocabulaire de manipulation

Calqué sur Tabletop Simulator, dont les conventions ont été vérifiées.

| Geste | Effet |
|---|---|
| Glisser une carte | La déplace vers la pile ou la zone visée, sans aucune vérification |
| Lâcher sur une pile | Dessus par défaut, dessous avec Maj |
| Survol d'une pile + chiffre | Prend N cartes (une seconde de délai, pour taper 12) |
| Survol d'une carte + chiffre | Pose N jetons **naturels** : dégâts sur un personnage, menace sur une manigance |
| Maj + chiffre | Retire autant |
| F | Retourne la carte, ou la pile survolée |
| R | Mélange la pile survolée |
| Q | Incline ou redresse |
| Alt | Agrandit |
| Ctrl+Z | Annule le dernier geste |
| Clic droit | Menu complet : statuts, jetons nommés, déplacement explicite, consultation d'une pile |

Les quatre statuts (assommé, désorienté, coriace, exposé) sont au clic droit,
sur décision de l'utilisateur. Aucune lettre à mémoriser.

Quand le jeton naturel d'une carte est douteux, le chiffre ne fait rien et le
plateau renvoie au clic droit, qui nomme chaque jeton. Mieux vaut ne rien
poser que poser la mauvaise chose sur une carte qu'on ne relira pas.

## Les gestes, côté moteur

L'API `Puzzle` couvre déjà l'essentiel : `Discard`, `Gain`, `Draw`,
`PutIntoPlay`, `Reveal`, `Damage`, `Heal`, `PlaceThreat`, `SetThreat`,
`Exhaust`, `Ready`, `Flip`, `Remove`, `PutIntoDeck`, `Counter`, `Token`,
`Confuse`, `Stun`, `Tough`, `Expose`, `CreateCard`.

Il manque quatre choses, toutes courtes :

- `MoveTo(carte, zone, position)` : le déplacement libre vers n'importe quelle
  zone, dessus ou dessous. C'est l'échappatoire retenue contre le risque
  « une zone oubliée bloque la partie ».
- `Attach(carte, cible)` : poser une amélioration ou un soutien sur une carte
  précise.
- `Engage(carte, joueur)` : engager ou désengager un sbire.
- `Shuffle(zone)` : mélanger une pile.

Aucun de ces quatre n'a besoin de vérifier quoi que ce soit : le déplacement
réel se fait dans `card.MoveToArea`, et le message qui suit ne sert qu'à
notifier, donc la porte du silence ne le casse pas.

## La sauvegarde, le rechargement, l'annulation

Le mécanisme existe : une partie Puzzle garde ses commandes dans
`Scene.puzzle`, rejouées à la mise en place (`game_session.py:133`).

**Décision : un champ séparé**, `Scene.manuel_commands`, et non une
réutilisation de `Scene.puzzle`. Les deux usages ne doivent pas se mélanger,
et un champ à défaut vide laisse les sauvegardes existantes se recharger sans
changer de sens.

- Chaque commande acceptée y est ajoutée.
- Recharger, c'est refaire la mise en place avec la même graine, puis rejouer
  les commandes dans l'ordre.
- Ctrl+Z, c'est retirer la dernière et recharger. Compter une à deux secondes
  sur une longue partie, ce qui est acceptable pour un geste rare.

## La fin de partie et la campagne

Deux boutons, victoire et défaite. Rien d'automatique, puisque le moteur ne
surveille plus rien. À l'écran de fin de scénario, **toutes** les cases du
journal de campagne deviennent saisissables, y compris celles marquées `auto`
dans les fiches de campagne : le moteur n'est plus en mesure de les constater.

## Le plateau

On masque tout ce qui parlait au nom du moteur : `BandeauPhase`,
`DeroulePhase`, `AssistantAction`, `CoucheCoach`, `DemandeCentrale`,
`CouchePasAPas`, `RecapPhaseMechant`, et la barre des actions légales.

`MenuTriche` et `CoucheTriche` deviennent le menu normal du mode, sans bandeau
« Bac à sable ». Le regroupement en une seule couche, déjà délibéré, est
conservé : le mode doit pouvoir être retiré sans laisser de traces.

Toutes les mains sont visibles en même temps, puisqu'il n'y a qu'un opérateur.

Le journal de partie note chaque geste, comme il note déjà les interventions
du bac à sable.

## Ce qui est déjà mesuré, et qu'il ne faut pas re-supposer

Trois faits établis le 18/09/2026, par lecture du code :

1. **Exécuter des commandes hors de `DoGetInput` fonctionne.**
   `PuzzleHelper.Exec` est appelé dans `GameSetup`
   (`game/game_run/game_session.py:133`), sur le fil du jeu, hors de toute
   attente d'entrée, à chaque partie Puzzle.
2. **Les identifiants d'objets sont un compteur de création**
   (`game/object/manager.py:59`), sans lien avec le tirage. Tout le corpus de
   cas Puzzle vise déjà les cartes par `c1`, `c2`, `c5` d'une exécution à
   l'autre, et l'annulation actuelle du moteur fonctionne déjà par rejeu.
3. **Le récit à l'écran ne passe pas par la diffusion des messages** : les
   messages texte appellent `Present` dans leur constructeur
   (`game/message/sender/sender_deck.py:13` et suivants), pas depuis
   `BroadcastMessage`.

## Les témoins qui comptent

Un mode vert ne prouve rien tant que ces cinq-là ne sont pas passés.

1. **Le moteur se tait.** Après la mise en place, zéro appel à `DoGetInput`
   pendant toute une partie, et ni le tour ni la phase ne changent seuls.
2. **Aucune capacité ne part.** Défausser à la main un allié portant une
   réponse « après avoir été défaussé » ne produit rien dans le journal.
   Le témoin qui compte est le **refus**, pas l'absence de plantage.
3. **La table reste manipulable.** Une carte de chaque type peut aller dans
   chaque zone, y compris là où les règles l'interdisent.
4. **L'aller-retour de sauvegarde.** Un geste, une sauvegarde, un
   rechargement, et l'état est identique carte par carte. C'est ce test qui
   lève définitivement le point 2 ci-dessus.
5. **Le plateau dessine bien.** Capture du plateau manuel réel, étape 8 bis de
   `PROCESSUS-CARTE.md` : le moteur vert ne prouve rien sur le rendu.

## Découpage proposé pour le plan

1. La règle `mode_manuel`, la boucle manuelle, la porte du silence. Témoins 1
   et 2. C'est le cœur, et c'est ce qui dit si l'idée tient.
2. Les quatre ajouts à l'API `Puzzle`. Témoin 3.
3. La sauvegarde, le rechargement, Ctrl+Z. Témoin 4.
4. Le plateau manuel : masquage, menu promu, glisser-déposer, clavier,
   recherche catalogue. Témoin 5.
5. La fin de partie et le journal de campagne.

---

# Avenant du 18/09/2026 : la pause manuelle en cours de partie

**Demande de l'utilisateur.** Pouvoir basculer une partie automatique en
manuel au milieu, et revenir. Motif : quand le moteur se trompe, ou qu'une
carte est mal paramétrée, le joueur corrige à la main et finit sa partie au
lieu de la perdre. Et au moment où il envoie son rapport de bug, on doit voir
ce qu'il a fait de ses mains, pour trancher entre un défaut du moteur et une
erreur de jeu.

## Ce que c'est, et ce que ce n'est pas

Ce n'est **pas** la bascule vers le mode manuel déclaré, qui reste ce que la
spec décrit plus haut. C'est une **pause sur place** : le moteur ne quitte pas
son déroulé, il reste garé exactement là où il en était, sur la question qu'il
venait de poser. Le mécanisme existe déjà : quand le moteur attend une réponse,
il exécute les commandes qu'on lui dépose, puis il repose sa question avec des
options recalculées. Une intervention à la main est donc naturellement suivie
d'une question à jour.

## Décisions

| Question | Décision |
|---|---|
| Forme de la bascule | Pause sur place, le moteur reste garé sur sa question |
| Si la question elle-même est fautive | Un bouton « passer cette question », l'échappatoire |
| Pendant la pause | La porte du silence se ferme : aucune capacité ne part |
| Reprise | Le moteur repose sa question, options recalculées |
| Traces | Les gestes s'insèrent au journal à leur place chronologique, marqués comme manuels, ET le rapport de bug reprend la liste seule en fin de document |
| Hauts faits | Ils continuent de compter. La partie porte une marque « corrigée à la main », visible au journal et au rapport |

## Ce que ça change à l'architecture décrite plus haut

`world.manuel_actif` cesse d'être « posé juste avant d'entrer dans la boucle
manuelle » pour devenir « vrai chaque fois que le mode manuel est actif, quelle
qu'en soit la raison ». Le mode déclaré le pose une fois pour toutes après la
mise en place ; la pause le pose et le retire à la demande. La porte du silence,
elle, ne change pas d'une ligne.

Aucune boucle manuelle n'est nécessaire pour la pause : le moteur est déjà garé
dans `DoGetInput`, qui draine déjà les commandes.

## Reste à cadrer

Qui peut déclencher la pause en multijoueur, et ce que voient les autres
joueurs pendant ce temps. Sans objet tant que le mode manuel vise un seul
écran, mais la pause, elle, a vocation à servir sur les tables en ligne.
