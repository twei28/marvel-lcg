# À FAIRE : le mode Archives du Collectionneur

**Idée de l'utilisateur, 13/09/2026.** On commence avec la seule boîte de base et
ses cinq héros ; on ouvre la suite en jouant. Décisions prises le jour même, une
question à la fois.

⚠ **RIEN N'EST ÉCRIT.** Ce fichier est la spec, pas un rapport de livraison.

## Pourquoi ce mode a sa place

Le catalogue compte **69 héros officiels et 61 scénarios**, plus une soixantaine de
héros fan-made, et il n'offre aucun parcours : un nouveau venu ouvre le wizard et ne
sait pas par où commencer. Le mode donne un ordre, une raison de sortir les héros
qu'on ne choisirait jamais, et transforme le contenu fan-made en récompense.

Deux appuis déjà en place : `games_history*.json` enregistre par compte le scénario,
les héros (avec leur `card_id`), la victoire et la difficulté ; et les **vagues**
existent déjà dans `public/js/prepare/catalog.js` (`BORNES_VAGUES`), affichées comme
filtre dans le wizard.

## Les règles retenues

| Point | Décision |
|---|---|
| **Ce qui débloque la vague suivante** | Chaque vilain de la vague battu au moins une fois, ET chaque héros débloqué vainqueur au moins une fois. Deux listes à cocher, pas une grille : la marche reste proportionnelle à la boîte, jamais au catalogue entier. |
| **Taille d'un palier** | Les **vagues déjà en place** : le Set de base, puis les onze vagues, chacune ouverte par une grande boîte et suivie de ses paquets de héros. Douze paliers. |
| **Héros fan-made** | Ils ne sont ni libres ni verrouillés : ils s'**achètent**. Finir pour la première fois une victoire avec un héros OFFICIEL donne un jeton, à dépenser sur le héros fan-made de son choix. 69 jetons possibles, presque un pour un avec le catalogue fan-made. |
| **Difficulté** | Une victoire compte pareil en normal et en expert — personne n'est bloqué. Mais une victoire **en expert rapporte un jeton fan-made de plus**. |
| **Coop** | Une victoire à plusieurs coche **tous les héros de la table**, et le vilain. Fidèle au jeu de plateau, et ça récompense de jouer à plusieurs. |
| **Parties déjà jouées** | **Au choix, une fois, à l'activation** : « reprendre mes parties passées » ou « repartir de zéro ». Deux chemins à tenir, assumés. |
| **Nom** | **Archives du Collectionneur**, retenu le 13/09/2026. Référence au Collectionneur Marvel, et le mode consiste bien à compléter une collection. |
| **Où on entre** | Une **sixième tuile sur l'accueil**, à côté de Solo, Coop, Campagne, Bac à sable et Bataille. On y entre comme dans un mode, on en sort en revenant à l'accueil. Le jeu libre n'est jamais verrouillé. |
| **Ce qui est verrouillé** | **Grisé, avec sa condition affichée** : « Gagne une fois avec Thor pour ouvrir la vague 2 ». Le catalogue entier reste sous les yeux, ce qui donne envie, et on sait toujours ce qui reste à faire. |
| **Où vit la progression** | **Le plus complet et le plus sûr** : une fiche par compte, écrite noir sur blanc à chaque fin de partie (vilains battus, héros vainqueurs, vague atteinte, jetons gagnés et dépensés). Et, parce que deux sources de vérité finissent toujours par diverger, **elle doit pouvoir être reconstruite** à partir de `games_history` : un outil de reconstruction, pas une promesse. |

## Et tant qu'on y est : garder les parties terminées

**Demande de l'utilisateur, 13/09/2026 :** « garder les logs des parties
terminées, afin que je puisse les revoir comme si j'y étais ».

Ce qui est déjà là, et personne ne s'en sert :

- le moteur sait écrire un **replay complet** d'une partie (`game_session.SaveScene`),
  et il le fait tout seul à la sortie d'une partie **si `auto_save_after_game_over`
  vaut vrai**. Ce drapeau existe, il vaut `False` par défaut, et **rien ne le met
  à vrai** : aujourd'hui une partie finie ne laisse aucune trace jouable, sauf si
  quelqu'un a pensé à appuyer sur 💾 Save ;
- le bouton **« Revoir »** de l'assistant (`reprise.js`) rejoue déjà un replay pas
  à pas, par `/debug?/load <nom>:-1`. Il n'y a donc rien à écrire côté lecture.

Ce qu'il reste à faire, et à vérifier :

1. **Allumer `auto_save_after_game_over`** dans la configuration du serveur
   (`tools/config_serveur.py`). ⚠ Le crochet est `OnExitGameInternal`, la SORTIE
   de partie, pas la fin : à mesurer sur une vraie partie web avant d'y croire.
2. **Mesurer le poids d'un replay.** Inconnu à ce jour, mesure non faite : le
   pilote `autoplay` n'emprunte pas ce chemin. Il en faut un vrai avant de
   décider d'une politique de rétention.
3. **Décider de la rétention.** Le modèle existe déjà pour les journaux de
   moteur (`JOURNAUX_MOTEUR_GARDES`, les dix plus récents).
4. ⚠ **Attention à l'expiration des comptes.** `_nettoyer_emplacement` efface
   `replays/serveur-N/` quand une place est recyclée. Les parties d'un compte
   expiré partent donc avec sa place, et c'est cohérent, mais il faut le savoir.

## La grille de départ, pour se figurer le rythme

Set de base : 5 héros, 3 scénarios. Il faut donc 3 vilains battus et 5 héros
vainqueurs, soit **5 victoires bien réparties** pour ouvrir la vague 1. Et ces
cinq victoires rapportent cinq jetons fan-made, dix si elles sont prises en expert.

## Ce qui reste à trancher avant d'écrire

- **Combien de parties on garde**, et pour quel poids sur le disque. À mesurer
  d'abord, à décider ensuite.
- **Les sets modulaires et les défis**, hors vagues (`vague: null` au-delà de la
  boîte 61) : probablement toujours libres, à confirmer.

## Décidé sans demander, parce que la réponse va de soi

- **Les scénarios sans héros** (la boîte Bouffon Vert en a deux, zéro héros) et les
  **héros sans scénario** : la condition tolère une liste vide des deux côtés. Une
  vague sans héros s'ouvre sur ses seuls vilains, et réciproquement. Sans cela,
  une boîte entière bloquerait la progression pour toujours.

## Statut

Spec validée sur ses onze règles, nom arrêté, **non commencée**. Deux
points restent ouverts, tous les deux sur la rétention des parties gardées.
