# `ss012` Mark of Kaine : le déferlement ne part pas (CORRIGÉ le 11/09/2026, contrôle cassé, pas la carte)

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


## ✅ Corrigé le 11/09/2026 : c'était le CONTRÔLE, et c'était moi

La carte fonctionne. Le journal du cas dit, ligne 54 :
`Tigra gagne (overkill) de Mark of Kaine`. Le vérificateur cherchait la forme
**anglaise** `gains overkill`, et le journal est en **français** depuis
`272e1cb4`, **ce matin 11:49** (mon correctif « 66 clés de
translate_fr.json ne traduisaient rien »). J'ai donc cassé ce contrôle
quelques heures avant que la passe ciblée ne le voie rougir.

« Préexistant » était exact par rapport au verrou Crise (vérifié avec
`scheme_main.py` d'avant) mais faux dans l'absolu : la cause est un commit
du jour.

**Correctif** : le vérificateur accepte les deux langues et exige que le
mot-clé et la source soient sur la **même ligne**, ce que l'ancien test ne
faisait pas non plus. C'est la **deuxième** fois que ce contrôle casse pour
une raison étrangère à ss012 (le 01/09, un index codé en dur).

**Leçon** : un vérificateur qui relit un journal ne doit jamais dépendre de
la langue d'affichage. Les 3 autres lecteurs de journal du harnais ont été
vérifiés le même jour.
