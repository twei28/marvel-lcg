# Deux défauts signalés en jeu le 12/09/2026, CORRIGÉS le jour même

## 1. « Quand je survole les cartes dans la modale, je ne vois pas la version agrandie »

Capture : la scène du déroulé (Klaw manigance sur Trafic Clandestin), rien
en grand au survol.

**Cause, mesurée** dans Chrome piloté : `document.elementFromPoint` au centre
d'une carte de la scène rendait `figure.deroule-carte`, jamais `.scan-card`,
à cause de `.deroule-carte .scan-card { pointer-events: none }` (« ni curseur,
ni survol », posé avec la case de bande dessinée du 07/09). Or la loupe
(`apercu-survol.ts`) cherche `closest('.scan-card')` sous la souris : elle ne
trouvait plus rien. Un `mouseover` envoyé directement à la carte ouvrait bien
la loupe : la logique était saine, la feuille la privait du pointeur.

**Correctif** : la carte garde le pointeur ; `cursor: default` et le
soulèvement au survol de `ScanCard` neutralisés dans la scène. Gate dans
`deroule-survol.test.ts` : `.deroule-carte .scan-card` ne doit plus porter
`pointer-events`.

## 2. « Sur la Policière en Patrouille on ne voit pas la quantité de menace prise »

Beat Cop (`10029`, « move 1 threat from a scheme to here ») : le moteur pose
des jetons `threat` sur le soutien, publiés en `info.k_threat` comme pour un
complot, mais `menaceAffichee` et `jetonMenace` (card-model.ts) ne
calculaient rien hors complot.

**Correctif** : toute carte qui porte de la menace la montre (compte seul, et
seulement s'il y a quelque chose : pas de « 0 » sur chaque soutien). Les
complots gardent leur rapport courant / cible.

**Les autres cartes du même genre**, relevées dans les modules
(`PlaceTokensOn([this], …, 'threat')` hors complots) : Stealth (`50035b`),
Alert Level (`50090a/b`), Beat Cop (`10029`), Iron Suit (`hd016`), Private
Investigator (`jj011`), Supporting Actor (`39029`, un sbire). Toutes couvertes
par la règle générique ; test `menace-hors-manigance.test.ts` (soutien,
sbire, complots inchangés).
