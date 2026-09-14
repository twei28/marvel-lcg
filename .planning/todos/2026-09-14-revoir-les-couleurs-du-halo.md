# Revoir les couleurs du halo des héros — À REPRENDRE (les palettes actuelles sont gardées en l'état)

**Décision de l'utilisateur, 14/09/2026** : « ce qu'on va faire, c'est que tu
vas utiliser ce que tu as fait maintenant et mets dans le backlog, on va revoir
les couleurs ». Le halo part donc avec les palettes mesurées ce jour-là ; la
qualité des couleurs se reprend plus tard, à froid.

Son constat, après avoir regardé la planche des 145 héros : « pour certaines
cartes tu es parfait et d'autres complètement à côté. Par exemple Hulkling, une
grosse partie de la carte est verte et je ne vois rien de vert dans la palette
que tu proposes ».

## La cause, mesurée

Elle est identifiée, pas corrigée.

`outils/palettes-heros.py` range chaque pixel du contour dans un seau de
**20° de teinte** (18 seaux), puis garde les seaux qui pèsent au moins 10 %.
Une couleur FRANCHE tient dans un seau et survit ; une couleur ÉTALÉE se brise
en morceaux dont aucun n'atteint le seuil.

Hulkling, contour de ses 13 cartes :

| seau | part | couleur |
|------|------|---------|
| sombre | 39,1 % | `#080806` |
| terne | 17,0 % | `#6d6f67` |
| clair | 14,2 % | `#dddcdd` |
| **5** | 6,1 % | `#488035` vert |
| 1 | 3,9 % | `#a17045` |
| **4** | 3,7 % | `#6b914a` vert |
| **6** | 3,5 % | `#215d2e` vert |
| **3** | 3,1 % | `#787e41` vert |

Les quatre verts pèsent **16,4 % ensemble**, largement au-dessus du seuil, et
chacun passe dessous tout seul. D'où une palette noir + blanc, sans vert.

C'est exactement ce qui explique « parfait ici, à côté là » : Captain America a
un rouge et un bleu FRANCS (un seau chacun), Hulkling a un vert qui va du
kaki au sapin.

## La piste, non implémentée

Regrouper les seaux de teinte VOISINS avant de classer : prendre le seau le
plus lourd, absorber ses voisins à ±1 ou ±2 seaux (soit ±20° ou ±40°), le
sortir, recommencer. À vérifier sur des témoins avant de retenir la largeur :

- Captain America doit RESTER rouge / blanc / bleu (un regroupement trop large
  fondrait son rouge et son bleu dans le violet des seaux intermédiaires) ;
- Hulkling doit devenir vert ;
- Hulk, She-Hulk, Iron Man (rouge + or) et Thor sont les autres témoins utiles.

⚠ Deux corrections FAITES ce jour-là, à ne pas refaire :
- l'outil ne lisait que `cards.json` et laissait trois identités de
  `cards_custom.json` sans palette (Stan Lee, Hulk Rainy, Rescue Rainy) ;
- il jetait en bloc les seaux « sombre » et « terne », et onze héros dont le
  cadre est vraiment noir ou gris (Venom, Magneto, Storm, Gamora, Black
  Panther...) ressortaient en BLANC quasi pur. Il retranche maintenant la part
  commune à toutes les cartes (21 % de noir, 18 % de gris, mesurés sur les
  133 sets) et garde ce qui dépasse.

## Où regarder

- `outils/palettes-heros.py` : la mesure, `seau_de()` et `palette_du_set()`.
- `Fusion/marvel-lcg-src/data/palettes-heros.json` : 287 faces, 0 sans palette.
- `ui-app/src/board/halo-heros.ts` : la composition du fond, indépendante de la
  mesure. Rien à y changer pour ce sujet.
- La planche de contrôle des 145 héros (carte, halo rendu, pastilles) se
  regénère avec le script gardé dans le dossier de session ; elle est le moyen
  le plus rapide de juger un changement de mesure d'un coup d'œil.

## Statut

Noté le 14/09/2026, **à reprendre**. Les palettes actuelles partent en l'état,
sur décision de l'utilisateur.
