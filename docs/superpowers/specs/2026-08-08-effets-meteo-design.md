# Effets météo — ouvrir la couche au-delà de Storm

Spec écrite le 08/08/2026.

## 1. L'existant

Le plateau a une couche météo, `ui-app/src/board/CoucheMeteo.tsx`, 64 lignes.
Elle superpose une iframe plein écran qui charge un effet HTML autonome depuis
`Fusion/marvel-lcg-src/public/effects/weather/`.

Trois effets existent :

| Fichier | Ce qu'il fait | Poids |
|---|---|---|
| `rain.html` | fond bleu-vert sombre en dégradé, gouttes de 1 par 89 pixels tombant en 0,63 s | 1,6 Ko |
| `storm.html` | canvas, éclairs ramifiés de 3 à 8 px doublés d'un halo, fond pulsant sur 6 s | 5,2 Ko |
| `snow.html` | 200 flocons, chacun avec sa propre animation CSS de 10 à 29 s | 79 Ko |

Ils ne se déclenchent que pour **Storm**, sur trois `card_id` en dur :
`36003` Hurricane, `36004` Thunderstorm, `36005` Blizzard. `36002` Clear Skies
n'a aucun visuel, il n'y a pas de `clear.html`.

La couche est activable dans les réglages, clé `marvel-board-meteo`, active par
défaut.

## 2. Les deux défauts de l'existant

**Elle ne lit que les joueurs.** `meteoDuMonde` fait
`for (const joueur of world.players ?? []) parcourir(joueur)`. Les 90 cartes
d'Environnement du jeu vivent dans `area_environment`, au niveau du monde :
aucune ne peut donc rien déclencher.

**Elle parcourt tout l'objet joueur**, y compris `hand_cards`, `player_deck` et
`additional_deck`, or c'est dans ce dernier que vit le deck météo de Storm avec
ses trois autres cartes. Le premier `card_id` trouvé gagne. Aujourd'hui le bon
effet l'emporte parce que `supports` précède `additional_deck` dans la
structure du descripteur, mais c'est un accident d'ordre des clés, pas une
garantie. Une carte météo en main déclencherait aussi son effet.

## 3. Ce qu'on livre à l'étape 1

**Lire des zones nommées** plutôt que l'objet entier :

- par joueur : `supports` et `environment_area`
- au niveau du monde : `area_environment`

Cela corrige les deux défauts et ouvre aux environnements d'un seul geste.

**Étendre la table** aux trois correspondances qui ne se discutent pas :

| `card_id` | Carte | Effet |
|---|---|---|
| `04081` | Snowy Hillside (Absorbing Man) | `snow` |
| `29039` | Air Static (Zzzax) | `storm` |
| `50131a` | Justice, Like Lightning (Thunderbolts) | `storm` |

**Un sélecteur d'aperçu** dans le panneau de réglages, à côté de
l'interrupteur météo : une liste qui force un effet à l'écran sans partie ni
carte. Visible par tous, pas réservé au bac à sable. C'est l'outil qui rendra
tenable la conception des sept filtres du Mojoverse à l'étape 2.

L'aperçu prime sur la météo dictée par les cartes tant qu'il est actif, et se
remet à « aucun » pour rendre la main au jeu.

## 4. Ce qu'on ne tranche pas seul

Trois cartes sont plausibles mais relèvent du goût, et seront proposées à
l'utilisateur une par une plutôt que décidées ici :

- `27065` City Streets (Sandman) : des rues de ville n'appellent pas la pluie
  d'elles-mêmes ;
- `27116b` Skies Over New York (Venom Goblin) : pluie ou orage, les deux se
  défendent ;
- `21079` Rubblestorm (Ebony Maw) : c'est une tempête de gravats, pas de pluie.

## 5. Le test

Rien de neuf à construire pour tester en jeu : `triche.ts` expose déjà
`mettreEnJeu`, et `CoucheTriche.tsx` la donne au joueur. Mettre `Snowy Hillside`
en jeu depuis le menu de triche suffit à voir la neige tomber.

Le sélecteur d'aperçu couvre le reste, sans partie.

Côté automatique : `meteoDuMonde` devient testable seule, sur des descripteurs
fabriqués. Les cas qui comptent sont une carte météo **en jeu** qui déclenche,
une carte météo **en main** ou **dans le deck météo** qui ne déclenche pas, et
un environnement du monde qui déclenche.

## 6. Les étapes suivantes, pour mémoire

**Étape 2, le Mojoverse.** Sept environnements de genre télévisuel, `39035`
Crime, `39041` Fantasy, `39047` Horror, `39053` Sci-Fi, `39060` Sitcom, `39066`
Western, plus la Roue des Genres `39026a/b` qui en change en cours de partie.
C'est le seul cas où le visuel raconte la mécanique.

**Étape 3, le catalogue.** Recenser les 90 environnements et les 97 lieux,
proposer un effet pour chacun, chiffrer.

## 7. Risques

**Le poids.** `snow.html` fait 79 Ko pour 200 animations CSS simultanées. Multiplier
les effets sur ce modèle finira par se voir sur une machine modeste. À surveiller
dès l'étape 2.

**L'iframe est plein écran et sous le plateau.** Tout nouvel effet doit rester
lisible derrière les cartes, et ne jamais capter le pointeur.


## 8. Ce qui a réellement été construit — arrêté au 09/08/2026

Cette spec prévoyait trois étapes et parlait encore de « météo ». Le chantier
est allé beaucoup plus loin, et une bonne partie de ce qui suit contredit ce
qui précède. Le texte d'origine est conservé tel quel ; cette section dit
l'état réel.

**Quinze effets pour trente-six cartes**, tous côté rencontre sauf les trois
soutiens météo de Storm : pluie, orage, neige, brume, étoiles, braises,
poussière, néons, jungle, noir et blanc, horreur, cyber, sitcom, sépia,
tempête de sable. Les étapes 2 et 3 sont faites, Mojoverse compris.

**Les trois effets d'origine n'avaient JAMAIS rien affiché.** Trois causes
cumulées, chacune suffisante : la couche était en `z-index: 0`, donc derrière
la scène ; les documents laissaient le canevas blanc opaque par défaut d'une
iframe (commenter la ligne de fond ne rend pas transparent) ; et le plateau
déclare `color-scheme: dark` alors que les effets restaient en `normal`, ce
qui pousse Chrome à peindre un fond opaque sous l'iframe. Tout nouvel effet
doit déclarer `html { color-scheme: dark; }` ET un fond transparent.

**Les ambiances se superposent** au lieu de se disputer l'affichage : décor du
scénario en dessous, cartes des joueurs par-dessus. Mesuré, empiler ne coûte
rien jusqu'à trois couches. Ce qui coûtait, c'était `filter: blur()`, que cinq
effets utilisaient et qui divisait par deux le nombre d'images par seconde,
chacun tout seul. Le flou est désormais cuit dans `tache.png`, utilisée en
masque.

**Le réglage s'appelle « Ambiance »**, plus « Météo », et l'aperçu est une
grille de pastilles à cocher permettant d'en essayer plusieurs à la fois.
Trois états : Auto, Aucun, ou une liste d'effets.

**L'ambiance appartient au scénario**, jamais aux cartes du deck d'un joueur.
Seize Soutiens de héros ont été câblés puis retirés pour cette raison ; un cas
de test refuse désormais tout type Support, Event, Upgrade, Ally ou Resource.
Seule exception, le deck météo de Storm, dont le sujet EST la météo.

**Le noir et blanc a son propre document**, `2026-08-08-cadre-aspect-noir-et-blanc-design.md`,
qui traite du liseré d'aspect rendu nécessaire par la désaturation.

**Le risque du poids, annoncé au §7, s'est vérifié** — mais pas là où on
l'attendait. Ce n'est pas le nombre d'animations qui coûte, c'est le flou.

Restent sans ambiance, par choix explicite du joueur : les trois Manhattan
infestés `27117b`, `27118b`, `27119b`, et Skies Over New York `27116b`. Leurs
effets ont été écrits puis jugés illisibles et supprimés.
