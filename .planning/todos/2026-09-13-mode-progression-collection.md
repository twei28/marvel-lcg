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

## La grille de départ, pour se figurer le rythme

Set de base : 5 héros, 3 scénarios. Il faut donc 3 vilains battus et 5 héros
vainqueurs, soit **5 victoires bien réparties** pour ouvrir la vague 1. Et ces
cinq victoires rapportent cinq jetons fan-made, dix si elles sont prises en expert.

## Ce qui reste à trancher avant d'écrire

- **Ce que « verrouillé » veut dire à l'écran** : héros grisé avec sa condition
  affichée, ou simplement absent de la grille ?
- **Où vit la progression** : calculée à la volée depuis l'historique du compte, ou
  stockée ? Le choix « repartir de zéro » impose de stocker au moins une date de
  départ et la liste des jetons dépensés.
- **Les scénarios sans héros** (la boîte Bouffon Vert en a deux, zéro héros) et les
  **héros sans scénario** : la condition doit tolérer une liste vide des deux côtés.
- **Les sets modulaires et les défis**, hors vagues (`vague: null` au-delà de la
  boîte 61) : probablement toujours libres, à confirmer.
- **Le mode est-il un interrupteur** à côté du jeu libre, ou remplace-t-il la
  sélection ? Hypothèse de travail : un interrupteur, on ne verrouille pas le jeu
  de quelqu'un qui n'a rien demandé.

## Statut

Spec validée sur ses sept règles, nom arrêté, **non commencée**.
