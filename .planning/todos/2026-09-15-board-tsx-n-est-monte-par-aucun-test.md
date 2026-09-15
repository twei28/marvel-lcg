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

## Statut

Constaté le 15/09/2026, **non traité**. À cadrer : c'est un choix d'outillage,
pas un correctif.
