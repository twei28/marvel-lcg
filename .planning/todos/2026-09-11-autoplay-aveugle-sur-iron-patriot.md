# L'autoplay est aveugle sur Iron Patriot, et la cause n'est pas le pack

**Constaté le 11/09/2026**, en vérifiant un chiffre laissé en suspens : Iron
Patriot perd **16 parties sur 16 au round 1,0**, là où le témoin `spider_man`
tient 3,6 rounds contre le même vilain, dans la même fournée.

## Ce n'est pas une régression, et ce n'est pas un défaut du pack

**Vérifié en remisant le correctif moteur du jour** (`git stash` des cinq
fichiers, autoplay relancé) : **chiffre identique sans lui**, 16/16 au round
1,0. Le canal des refus n'y est pour rien.

**Vérifié sur la carte** : l'Action *Enlistment* de `ip002a` Registration Act
n'a **aucune limite imprimée**, et une manigance-joueur ne peut pas s'incliner.
Elle est donc réellement répétable. C'est le texte de l'auteur, et le risque
qu'il a voulu : tu t'engages des sbires. Un humain la prend une ou deux fois.

## Ce qui se passe vraiment

Le pilote la prend **21 fois dans le round 1**. Les sbires REGISTERED entrent
en jeu par dizaines (33 cartes en jeu dans une partie d'un round), et leur
Incitation remplit le complot principal :

| Source de la menace | Occurrences |
|---|---|
| `ip025`, `ip022`, `ip032`, `ip031`, `ip029` (sbires REGISTERED) | 9 |
| deck Rencontre standard (`01130`, `01125`, `01121`, `01116b`) | 4 |

## La cause, mesurée et non supposée

`tools/autoplay.py:517`, branche par défaut du scorer : « une capacité proposée
et non forcée est presque toujours un gain » → **score fixe de 20**.

Première hypothèse, **fausse** : faire décroître ce score avec le nombre de
reprises dans le round. Essayée en `20/(1+n)` puis en `20/(1+n)²` : **21
reprises dans les deux cas**, 16/16 au round 1,0 inchangé.

Expérience discriminante : score forcé à **0,5 sans aucune condition**.
Résultat : **toujours 21 reprises**. Donc Attaque et Contre valent **moins de
0,5** au round 1.

**C'est là le vrai défaut.** `urgence(tours)` rend une valeur proche de zéro
tant que l'échéance est lointaine, et tous les gains pondérés
(`poids_menace * urgence * THW`, etc.) s'effondrent avec elle en début de
partie. N'importe quelle capacité à score fixe écrase donc les pouvoirs de
base. Le 20 ne créait pas le problème, il le masquait.

⚠ Le garde-fou de répétition existant (`etat["historique"]`) ne pouvait pas
l'attraper : il est indexé sur une **empreinte du contexte**, et chaque sbire
qui entre en jeu change le contexte. L'empreinte changeait à chaque coup.

## Ce que ça coûte, et pourquoi ça compte

**Les « 16 parties, 0 traceback » d'Iron Patriot ne valaient presque rien.**
Toutes finissaient avant la fin du premier round, sans exercer le pack. La gate
la plus chère du projet est aveugle sur ce pack, et le sera sur tout pack
offrant une capacité nommée répétable.

Les autres packs ne sont pas touchés de la même façon : Spider-Woman tient 3,9
et 5,8 rounds, Spider-Man 3,6 et 5,6. Le défaut ne se voit que quand une
capacité répétable est offerte en permanence.

## Ce qui n'a PAS été fait, et pourquoi

La correction du scorer a été **retirée** : elle n'apportait aucun bénéfice
mesuré, et garder une modification non probante dans l'instrument de mesure de
tout le projet aurait été pire que le défaut.

Le vrai chantier est ailleurs : **re-calibrer la courbe d'urgence pour que les
pouvoirs de base gardent une valeur en début de partie**. Le fichier montre que
ce modèle a été réglé par mesures successives (« essayée et retirée : elle
faisait tomber le bot de 6,3 à 4 rounds ») ; y toucher demande la même rigueur,
sur plusieurs decks témoins, et ce n'est pas un patch.

## ⚠ CORRECTION DU MÊME JOUR : la cause énoncée ci-dessus était incomplète

Le diagnostic initial attribuait tout à la courbe d'urgence. **Faux, ou plutôt
partiel.** Les scores réels, obtenus en instrumentant le scorer (ce que ce
document recommandait de faire, et qu'il fallait faire d'abord) :

```
retenues = [('Enlistment', 0.5), ('Attack', -5.0), ('Thwart', -5.0)]
```

Et l'instrumentation des faces a montré que ces Attaque et Contre à −5 ne sont
pas ceux du héros : ils sont liés au gabarit `registered_ally`, dont le `desc`
imprimé vaut `ATK: '0*'` et `THW: '0*'`, les vraies valeurs étant posées à
l'exécution par `Faces.TreatAsAlly`. **Le scorer lisait `paper.desc`, donc
l'imprimé.** Il voyait tous ces alliés comme nuls et refusait de s'en servir.

Il y avait donc **trois** défauts, pas un :

1. le score fixe de 20 des capacités nommées, qui écrase le calcul pondéré ;
2. la courbe d'urgence, qui rend exactement zéro au-delà de 6 tours d'échéance
   et fait tomber Contre à −5 avec le coût d'activation ;
3. **la lecture des statistiques imprimées au lieu des vivantes**, qui rend
   invisible toute carte dont les valeurs sont posées en jeu (`TreatAsAlly`,
   `TreatAsMinion`, bonus continus, améliorations).

## Ce qui a été corrigé, et mesuré

| Deck | Avant | Après |
|---|---|---|
| spider_man / rhino | 5,6 rounds | **7,5** |
| spider_man / klaw | 3,6 | **4,6** |
| spider_woman / rhino | 5,6 | **6,4** |
| spider_woman / klaw | 3,9 | **4,0** |
| iron_patriot | 1,0 | 1,0 |

Trois changements gardés : plancher d'urgence à 0,3, lecture de la statistique
vivante, décroissance des capacités répétées dans le round.

**Un changement REJETÉ** : faire passer cette décroissance en négatif. Elle
montait spider_man à 7,8 rounds, mais **Iron Patriot ne terminait plus** : le
bot déclinait, le moteur reposait la même question. Un gain sur un deck ne vaut
pas un blocage sur un autre.

**Iron Patriot reste à 1,0 round**, et c'est désormais une propriété connue et
non un mystère : le pack se noie lui-même dès que le pilote enlist librement.
La gate reste donc peu informative sur ce pack précis.

## Si on y revient

1. ~~Instrumenter le scorer pour **afficher les scores**~~ ✅ **FAIT le
   15/09/2026.** `--trace` imprime désormais `scores r1: [('Enlistment', 20.0),
   ('Play', 19.2), …]`, trié.
   ⚠ **Et il a fallu s'y reprendre à deux fois.** Posée après le choix, la trace
   affichait les scores D'APRÈS : le compteur du round venait d'être incrémenté,
   et la capacité s'y lisait déjà décotée. On lisait « Enlistment 6,67 » sur une
   décision prise à 10,0, de quoi conclure l'inverse de ce qui s'était passé.
   Elle se calcule maintenant AVANT `max(retenues, …)`.
2. Mesurer la courbe d'urgence sur 3 decks témoins AVANT de la changer.
3. Ne juger que sur les rounds tenus et les parties bloquées, jamais sur le taux
   de victoire seul.

## ✅ 15/09/2026 : le spam est corrigé, la cause restante est identifiée

**Ce que la trace des scores a montré**, et qu'aucun raisonnement n'aurait
donné. En fin de round il ne reste que DEUX options, et la seconde s'effondre
plus vite que la première :

```
scores r1: [('Enlistment', 6.67), ('Change_Form', 2.82)]   -> Enlistment
scores r1: [('Enlistment', 5.00), ('Change_Form', -2.64)]  -> Enlistment
scores r1: [('Enlistment', 3.33), ('Change_Form', -13.55)] -> Enlistment
scores r1: [('Enlistment', 2.86), ('Change_Form', -19.00)] -> Enlistment
```

Chaque enrôlement révèle des sbires que le joueur **ne contrôle pas** (Madame
Masque, Bullseye…). Les dégâts entrants montent, l'urgence de survie avec eux,
et passer en forme héros devient de plus en plus suicidaire aux yeux du scorer.
**Le pilote s'enterre, et plus il s'enterre, plus s'enterrer encore est ce
qu'il trouve de mieux.** Voilà pourquoi la décroissance `20/(1+n)` ne suffisait
pas : elle faisait bien baisser Enlistment, mais moins vite que son alternative.

**Le correctif : un PLAFOND par round sur les capacités nommées**
(`PLAFOND_CAPACITE_NOMMEE = 3`). L'option est **écartée** de la liste au-delà,
pas notée plus bas.
⚠ Écarter, pas annuler : noter négativement avait été essayé le 11/09 et
REJETÉ, parce que le bot déclinait alors et que le moteur reposait la même
question. Ici une AUTRE option est choisie, donc la partie avance. Si toutes
sont saturées, la liste entière est rendue : mieux vaut rejouer la même chose
qu'être bloqué.

**Mesures, 4 parties par ligne, profil équilibré :**

| Deck / vilain | Avant | Après | Parties sans verdict |
|---|---|---|---|
| spider_man / rhino | 7,5 | **7,5** | 0 |
| spider_man / klaw | 4,0 | **4,0** | 0 |
| spider_woman / rhino | 4,2 | **4,2** | 0 |
| iron_patriot / rhino | 1,5 | **1,5** | 0 |

Et sur le comportement, qui est l'objet du défaut : **« Enlistment » passe de
21 prises à 3** dans le round 1. Le tour se termine normalement, la phase du
méchant se joue, le pack est enfin exercé au lieu d'être noyé sous vingt
sbires.

**Le plafond a été balayé** : 1 et 2 donnent **1,2 round** contre 1,5 pour 3.
Serrer davantage ne rend pas le pilote meilleur, il le rend plus pauvre. La
valeur 3 est mesurée, pas choisie.

⚠ **CE QUI N'EST TOUJOURS PAS RÉGLÉ, et il faut le dire :** Iron Patriot perd
encore au round 1,5. Le spam n'était donc pas la seule cause. La suivante est
nommée et mesurée : **le bot ne repasse jamais en forme héros**, parce que
`Change_Form` est noté sur la seule survie (`g_survie = -1.0` pondéré par une
urgence qui monte avec les dégâts entrants) et jamais sur le coût de RESTER en
alter-ego, où il ne peut ni attaquer ni contrer pendant que le complot se
remplit. C'est le point 2 ci-dessus, et il demande la même rigueur : trois decks
témoins, avant et après.

Garde : `tools/test_autoplay_plafond.py` (11 cas, sans monter le moteur).
