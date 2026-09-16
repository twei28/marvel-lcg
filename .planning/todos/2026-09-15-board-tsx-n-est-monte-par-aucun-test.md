# `board.tsx` n'est monté par aucun test, et trois défauts y sont passés

**Constat du 15/09/2026**, arrivé trois fois dans la même journée. Ce n'est plus
une coïncidence, c'est un trou.

## Ce que la batterie couvre, et ce qu'elle ne couvre pas

1596 cas verts, 141 fichiers. Les modules purs sont bien tenus : les règles de
zones, de placement, de glisser, de langue, d'interaction ont chacune leurs cas.

⚠ **`ui-app/src/board.tsx` (plus de 3600 lignes) n'est rendu par AUCUN test.**
Ni `PagePartie`, ni la barre du haut, ni le câblage entre les modules purs et
l'écran. Le typage est le seul filet, et il ne voit que les signatures.

## Les trois défauts du jour qui sont passés par ce trou

1. **La barre « Vue » était tombée dans le bouton « Partie »** lors de la refonte
   des onglets du 14/09, alors que la fiche de décision disait « la Vue reste
   dans la barre ». Aucun cas n'a rougi. Signalé en partie à plusieurs.
2. **Le glisser-déposer qui perd sa source** : la règle est corrigée et couverte
   par trois cas unitaires, mais le fait que `onDepot` PASSE bien la source au
   menu n'est prouvé que par le typage.
3. **Le montage du panneau de la manigance** (`{questionManigance ? <PanneauManigance/> : null}`) :
   le harnais `plateau-de-test.ts` court-circuite `board.tsx`, il ne sait même
   pas qu'un panneau existe. Relevé par la relecture de la tâche 10 du chantier
   de l'ouverture silencieuse.

## Les deux pistes, et ce qu'elles coûtent

**A. Monter `PagePartie` en vitest.** Le composant ouvre un socket et devient un
vrai client de jeu : il faudrait un faux moteur. Cher, mais c'est le seul niveau
qui prouve le câblage ET le rendu.

**B. Une spec `ui-check` qui compte les boutons de la barre** sur une partie à
deux joueurs. Beaucoup moins cher, attrape le défaut n°1 et ses cousins. ⚠ Mais
ces specs **créent une partie neuve et détruisent celle en cours** : elles ne
peuvent pas tourner à la demande, seulement sur décision.

⚠ Ne pas partir sur A sans avoir mesuré ce qu'un faux moteur exige : ce plateau
lit le monde, la demande, le siège, le catalogue et les scans. Un faux à
moitié juste donnerait des cas verts qui ne prouvent rien, ce qui est pire que
l'absence de cas.

## Ce qui a été fait, 16/09/2026 : la piste A

La mesure d'abord, comme l'avertissement l'exigeait : **le faux moteur coûte
100 lignes** (`ui-app/src/board/moteur-faux.ts`). Il ne remplace que le
TRANSPORT — l'écran reçoit exactement les mêmes trames (`EtatMoteur`) qu'en
partie réelle, et ses réponses sont enregistrées au lieu de partir. Aucune règle
de jeu n'y est simulée : le cas pose l'état complet qu'il veut voir dessiné.

Ce qui bloquait vraiment n'était pas le socket, c'était le module : `board.tsx`
n'exportait RIEN et montait la page à l'import. Deux changements minimes :
`PagePartie` est exporté, et le point d'entrée est passé sous
`if (!import.meta.env.VITEST)`. Le `throw` sur `#plateau` absent est maintenu
hors test, et la garde disparaît à la compilation (vérifié dans le bundle).

`ui-app/src/board/PagePartie.test.tsx`, 8 cas :

- le moteur est ouvert au montage et **fermé au démontage** ;
- la table est dessinée à la première trame ;
- **défaut n°1** : la barre offre « Vue » + Auto + un bouton par héros à
  plusieurs, rien en solo, et pas de bouton pour un joueur éliminé ;
- **défaut n°3** : le panneau de la manigance paraît sur la question du
  retournement, pas sur une demande ordinaire, et son bouton **répond
  vraiment** au moteur (une fois le retournement fini).

Les cinq cas des deux défauts ont été vérifiés par mutation : condition de la
Vue passée à `> 2`, montage du panneau forcé à `false` — trois rougissent, dont
les trois qui devaient. Batterie complète : 148 fichiers, 1658 cas, verts.

## Ce qui reste : le défaut n°2

Le glisser-déposer n'est toujours prouvé que par le typage. `onDepot` est
atteint par un geste de pointeur sur un plateau dimensionné (`ResizeObserver`,
rectangles) : jsdom ne donne ni l'un ni l'autre, et un faux geste prouverait le
faux geste, pas le dépôt. C'est le seul des trois qui reste ouvert.

## Statut

**Traité le 16/09/2026** pour les défauts n°1 et n°3 : l'écran de jeu est monté,
le trou est fermé. Le défaut n°2 reste à couvrir, voir ci-dessus.
