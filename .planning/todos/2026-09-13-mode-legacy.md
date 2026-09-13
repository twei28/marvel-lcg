# À FAIRE : le mode Legacy

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
| **Nom** | **Legacy**, arrêté le 13/09/2026. « Archives du Collectionneur » avait été retenu quelques heures plus tôt, puis écarté : trop long pour une tuile, et le mot Legacy dit mieux ce qu'on fait, reprendre le jeu depuis son origine. |
| **Sous-titre de la tuile** | « Boîte par boîte ». La petite ligne sous le nom, comme « 1 héros » pour Solo et « Progression » pour Campagne : elle dit le rythme du mode. |
| **Phrase au survol** | « Tu commences avec la boîte de base et tu débloques la suite en gagnant. » Même ton que les cinq autres tuiles, voir `MODES` dans `public/js/prepare/app.js`. |
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
3. **Rétention : les 50 dernières parties de chaque joueur** (décision du
   13/09/2026). De quoi revoir une campagne entière et ses alentours. Le modèle
   existe déjà pour les journaux de moteur (`JOURNAUX_MOTEUR_GARDES`, les dix
   plus récents) : même forme, autre chiffre. ⚠ À confirmer une fois le poids
   d'un enregistrement mesuré — 50 parties par joueur, fois 20 places, fait 1000
   fichiers sur un serveur que personne ne surveille.
4. ⚠ **Attention à l'expiration des comptes.** `_nettoyer_emplacement` efface
   `replays/serveur-N/` quand une place est recyclée. Les parties d'un compte
   expiré partent donc avec sa place, et c'est cohérent, mais il faut le savoir.

## La grille réelle, mesurée le 13/09/2026

Douze paliers, relevés sur le vrai catalogue par `legacy-catalogue.js` :

| Vague | Scénarios | Héros |
|---|---|---|
| 0 · Set de base | 3 | 5 |
| 1 | 3 | 6 |
| 2 · The Rise of Red Skull | 6 | 6 |
| 3 · The Galaxy's Most Wanted | 5 | 6 |
| 4 · The Mad Titan's Shadow | 6 | 6 |
| 5 · Sinister Motives | 5 | 6 |
| 6 · Mutant Genesis | 8 | 8 |
| 7 · NeXt Evolution | 5 | 6 |
| 8 · Age of Apocalypse | 5 | 6 |
| 9 · Agents of S.H.I.E.L.D. | 7 | 6 |

La marche la plus lourde est la vague 6, huit et huit. Aucune ne dépasse ça :
la progression reste proportionnelle à la boîte, comme voulu.

Set de base : il faut 3 vilains battus et 5 héros vainqueurs, soit **5 victoires
bien réparties** pour ouvrir la vague 1. Et ces cinq victoires rapportent cinq
jetons fan-made, dix si elles sont prises en expert.

## Les sets modulaires et les défis

**Décision du 13/09/2026 : un set modulaire s'ouvre avec la boîte dont il
vient.** Cohérent avec l'idée de collection : on ne pioche pas dans un paquet
qu'on n'a pas encore.

Relevé fait le même jour, et il y a un piège. Sur **172 sets modulaires**, 156
sont rattachés à une extension par la clé `encounters` de `sets_info.json`, donc
à une vague. **Seize ne le sont pas :**

```
age_of_apocalypse_WIP, bodyguard, city_sewers, community_service, crime_wave,
electro, god_of_lies, kingpin, kraven_the_hunter, power_drain_ii, shocker,
snitches_get_stitches, the_lizard, the_spot, underling, vulture
```

Ils restent **libres**, faute de boîte à laquelle les rattacher. Inventer une
vague pour eux serait arbitraire, et les enfermer jusqu'à la fin du parcours les
rendrait invisibles pour toujours. À rattacher un par un si l'envie vient, mais
pas avant d'avoir écrit le reste.

## Ce qui reste à trancher avant d'écrire

Plus rien. Les douze règles sont arrêtées. Reste à mesurer le poids d'un
enregistrement de partie, ce qui est un chiffre à relever, pas une décision à
prendre.

## Décidé sans demander, parce que la réponse va de soi

- **Les scénarios sans héros** (la boîte Bouffon Vert en a deux, zéro héros) et les
  **héros sans scénario** : la condition tolère une liste vide des deux côtés. Une
  vague sans héros s'ouvre sur ses seuls vilains, et réciproquement. Sans cela,
  une boîte entière bloquerait la progression pour toujours.

## Le découpage, et où on en est

| # | Tranche | État |
|---|---|---|
| 1 | **Les règles**, pures et testées : `public/js/prepare/legacy.js`. Paliers, jetons, conditions, ordre des vagues, table rase. | ✅ **Faite le 13/09/2026.** 13 cas, `npm run legacy`. |
| 2 | **Les paliers depuis le catalogue** : `public/js/prepare/legacy-catalogue.js`. | ✅ **Faite le 13/09/2026.** 5 cas, `npm run legacy-paliers`. |
| 3 | **La fiche du compte** : `legacy-fiche.js`, routes `/get_legacy` et `/save_legacy`. | ✅ **Faite le 13/09/2026.** 10 cas, `npm run legacy-fiche`. |
| 4 | **L'écran** : la sixième tuile, la question à l'activation, la grille grisée avec l'étiquette de sa boîte et la condition en infobulle, le bandeau, l'achat d'un fan-made d'un clic. `legacy-verrou.js` + branchement dans `app.js`. | ✅ **Faite le 13/09/2026.** 7 cas `npm run legacy-verrou`, 8 cas `npm run legacy-ecran`. |
| 5 | **Garder les parties terminées** : `auto_save_after_game_over` allumé dans `config_serveur.py`, ménage à 50 dans `eteindre_jeu`, les trois emplacements du plateau jamais touchés. | ✅ **Faite le 13/09/2026.** |

⚠ La tranche 1 ne lit ni réseau, ni stockage, ni catalogue : on lui passe tout,
elle répond. Tout le reste s'y branche, rien ne s'y mélange.

## Statut

**Livré le 13/09/2026**, les cinq tranches. Non déployé à cette date.
Plus aucune question ouverte. Il reste un chiffre à relever, le poids d'un
enregistrement de partie, qui peut faire revoir la rétention.
