# Relecture et spectateur : voir 100 % de ce que le joueur voit (12/10/2026)

**RETIRÉ du backlog le 21/10/2026** (item 5), décision de l'utilisateur.

Constat de l'utilisateur : en revoyant une partie, « on ne voit pas tout » : le curseur du joueur passe SOUS
les fenêtres (couche `ui-app/src/board/CoucheCurseurs.tsx`), l'agrandissement d'une carte survolée n'apparaît
pas, etc. Existant : chaque client envoie sa souris normalisée 0..1 (`/set_cursor`, 150 ms) avec la carte
survolée et les clics ; relecture via `board/relecture/lecteur`.

## Décisions (questions une à une)

| # | Question | Réponse |
|---|---|---|
| 1 | Rendu du curseur | **Par-dessus tout** (fenêtres de phase, questions, aperçu) **+ courte traînée** des dernières positions |
| 2 | Carte survolée par le joueur | **Aperçu à droite comme chez lui + contour** de sa couleur autour de la carte sur la table |
| 3 | Autres gestes à rejouer | **Tous** : panneaux ouverts (journal, aide, réglages, défausse ouverte, loupe), menus de carte et option survolée, fenêtres déplacées / réduites, défilement et zoom |
| 4 | Taille d'écran différente | **Sa vue exacte mise à l'échelle** (taille de sa fenêtre enregistrée, mise à l'échelle avec bandes si les proportions diffèrent) |
| 5 | Ses réglages d'affichage | **Les siens** (sobre, mode de la phase du méchant, langue, animations) |
| 6 | Anciennes parties | **Rejouer ce qu'on a** avec le nouveau rendu + bandeau « enregistrement partiel » |
| 7 | Spectateur en direct | **Pareil en direct** |

## Ordre de travail

Après le lot 5 de la refonte de la phase du méchant (mêmes fichiers du plateau). Commencer par l'inventaire de ce
qui est déjà enregistré/émis, puis : curseur au premier plan + traînée, survol → aperçu + contour, enregistrement
des réglages et de la taille de vue, gestes (panneaux, menus, fenêtres, défilement), mise à l'échelle.
