# `ss012` Mark of Kaine : le déferlement ne part pas (défaut PRÉEXISTANT)

**Trouvé le 11/09/2026**, par la passe ciblée qui suivait le verrou Crise.
Le cas s'appelle « ss012 Mark of Kaine — attaques contre le sbire marqué
gagnent déferlement (déversement sur un autre ennemi) » et il échoue avec le
message :

```
aucune trace de 'gains overkill' dans le journal de la partie
```

## Ce n'est PAS une régression du verrou Crise

Mesuré, pas supposé : le fichier `scheme_main.py` a été remis dans sa version
d'avant (`git show 92cd218e~1`), le cas relancé, **et il échoue pareil**. Le
second cas de la même carte (« Hero Interrupt : +2 à l'excès ») passe, avant
comme après.

Mon filtre l'a simplement attrapé parce que son nom contient « attaques
**contre** le sbire marqué ».

## Depuis quand ?

Inconnu. La batterie complète n'avait pas été repassée depuis un moment, et
les passes filtrées ne visaient pas ce pack. À dater avec
`git log -S"Mark of Kaine"` et en rejouant le cas sur quelques commits.

## Par où commencer

1. Lire le module de la carte et le cas, et vérifier que le déferlement est
   bien posé par `UnitAttackGainKeyword(..., overkill=True)` (recette §3).
2. `TRACE_OPTIONS=1` sur ce cas seul, pour voir si la capacité est offerte.
3. Se méfier du piège connu : un filtre placé dans le corps de l'opération au
   lieu de `conditions` fait que la capacité est proposée mais n'agit pas.
