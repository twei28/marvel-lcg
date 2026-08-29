# Processus : une carte, du début à la fin

Fichier unique : construire ET vérifier une carte, dans l'ordre réel
d'exécution. Fusion de l'ancien §4 de `GUIDE-CREATION-CONTENU.md` et de
l'ancien `CHECKLIST-VALIDATION-CARTE.md` (29/08/2026). Une seule carte à la
fois (jamais un lot validé en bloc).

## Étape 1 : Entrée dans `data/cards.json`

Ajouter l'entrée dans le bon pack (tri par `card_id`). Renseigner `type`,
`name`, `desc`, `traits`, `set_name`, `text`. Format détaillé :
`GUIDE-CREATION-CONTENU.md` §2.

Pour une carte custom hors dépôt : voir `data/cards_custom.json` et le
mécanisme `cards/<id>.py.txt` (guide de l'éditeur).

## Étape 2 : Carte(s) de référence *(obligatoire, avant le script)*

Pour CHAQUE capacité distincte de la carte : quelle carte déjà scriptée est
comparable (même déclencheur, même genre d'effet), et pourquoi. Plus de
4 200 cartes sont déjà scriptées dans le dépôt : s'en inspirer plutôt que
réinventer. Ne pas écrire une ligne de script avant d'avoir rempli ce champ.

```
Capacité <nom> : carte de référence <card_id> (<nom>) : comparable parce que ...
```

## Étape 3 : Script

`src/cards/pack/<pack>/<set>/<card_id>.py`, `GetAbilities()`. Référence API :
`GUIDE-CREATION-CONTENU.md` §3. **Pour chaque mot-clé imprimé sur la carte**,
ouvrir sa fiche dans `mots-cles/` avant de coder son effet ; absente → la
créer d'abord (gabarit dans `mots-cles/README.md`).

### En cas de doute : DEMANDER, carte par carte

**Règle absolue.** Dès qu'une carte laisse place à plus d'une lecture, on ne
tranche pas tout seul : on pose la question à l'utilisateur.

- **Une question à la fois**, en **multichoix**, avec l'option recommandée en
  premier et « Autre (précise) » toujours disponible en dernier.
- **Une question par carte.** Ne jamais grouper « voici mes 8 arbitrages,
  valide en bloc » : chaque carte a son contexte, et un lot se valide à la
  légère.
- Chaque option doit dire **ce que ça change en jeu**, pas seulement ce que ça
  change dans le code.
- Poser la question **avant** d'écrire le script, pas après. Ce qui n'a
  pas été demandé au bon moment doit l'être quand même : mieux vaut une
  question tardive qu'un arbitrage silencieux.

Ce qui déclenche une question, sans exception :

| Situation | Exemple vécu |
|---|---|
| Mot-clé maison non défini sur les cartes fournies | `drain X` (Agent Anti-Venom) : introuvable sur les scans et en ligne |
| Texte imprimé contradictoire | The Made Men : « Forced **Interrupt** : **After** Maniac schemes or attacks » |
| Valeur imprimée que le moteur ne sait pas encoder | l'ATK « ★ » du Homme-Pourpre |
| Portée d'une phrase ambiguë | « Discard this obligation » : la dernière option seulement, ou les deux ? |
| Mot-clé officiel inapplicable tel quel | `TeamUp` de Power Couple, qui suppose DEUX héros en jeu |
| Contenu absent du matériel fourni | aucune decklist d'aspect livrée par l'auteur |
| Un effet que le moteur ne peut pas rendre fidèlement | « if this attack has ranged or piercing » sur un événement |
| Une icône imprimée qu'on ne reconnaît pas | l'icône « nœuds reliés » de Lockjaw, prise pour un os pendant cinq jours |

**Une icône de ressource ne se nomme jamais à vue.** Elle se vérifie contre
une carte du **même pack** dont la fiche déclare la ressource : `desc.RES`
vaut `R` physique, `B` mental, `Y` énergie, `G` wild. On découpe le coin
supérieur gauche des deux scans et on compare. Sur Lockjaw, 78005 Kamala's
Room porte `RES=B` et imprime la forme litigieuse ; 78002 Black Bolt porte
`RES=G` et imprime une ÉTOILE. Une lecture au jugé a inventé une « ressource
os » rendue par un wild, et quatre cartes n'ont pas rendu ce qu'elles
promettent jusqu'au 9/8/2026. **Aucun outil du projet ne peut attraper ça** :
tous comparent le code au texte saisi, et le texte était faux pareillement.
Seul un joueur l'a vu, en partie.

Ce qui ne déclenche PAS de question : les choix purement techniques sans effet
sur les règles (quelle fabrique employer, où ranger un helper, format
d'image). Ceux-là se documentent au §9 de `GUIDE-CREATION-CONTENU.md`, ils
ne se discutent pas.

À l'inverse, les points **non tranchables** (une capacité que le harnais ne
sait pas déclencher, un doute sur le comportement réel du moteur) ne sont
pas des questions : ils vont dans la liste « à vérifier en partie réelle »
du §9 de `GUIDE-CREATION-CONTENU.md`, et il faut le dire clairement en fin
de travail.

## Étape 4 : Image

`assets/pics/<card_id>.<jpg|png|webp>` (l'extension est obligatoire, le
chargeur `engine/file/cache.py` l'exige). Sans image déposée, le jeu tente
marvelcdb puis génère un repli.

## Étape 5 : Bloc texte-contre-code, ligne par ligne

Lire le texte imprimé phrase par phrase, puis le script Python, et vérifier
que chaque mot du texte a sa contrepartie exacte dans le code.

**Liste des mots-pièges à chercher explicitement sur CHAQUE carte** :

| Mot ou tournure | Piège concret déjà rencontré |
|---|---|
| `each`, `for each` | rendu par erreur « chaque joueur » au lieu de « chaque héros » (`wd001b`, `wd014`) |
| `against you`, `your` | portée oubliée ou élargie par erreur |
| `you control` | le coût ou la cible peut viser une carte hors du contrôle du joueur, y compris celle du vilain (`wd165`) |
| `unless`, `otherwise`, `without` | branche alternative non codée |
| `instead` | un déplacement écrit « instead » veut dire que la chose PART d'un endroit et ARRIVE ailleurs, pas qu'elle est dupliquée (leçon The Spot) |
| `once per round per player` | à ne pas coder comme une limite globale (`wd056b`) |
| `if you cannot` | vérifier que le cas testé est réellement atteignable (`wd028`) |
| `that <nom>` | vérifier que la cible visée est bien LA MÊME carte que celle nommée plus haut (`wd022`) |
| `equal number` | vérifier le sens exact du décompte (`wd037`) |
| `attacks` vs `attacks or engages` vs `attacks and damages` | trois déclencheurs différents (`wd006`, `41013` Cypher) |
| `and remove` (coût à plusieurs parties) | vérifier qu'AUCUNE partie n'est oubliée (`wd005`) |
| `defeated` vs `damaged` | ne jamais coder l'un pour l'autre (`45160` Scarab) |
| **Response**/**Interrupt** + `After` | déclencheur = vrai message du moteur avec fenêtre (`wd089`) |
| **Forced Interrupt** vs **Forced Response** | l'un résout AVANT l'événement, l'autre APRÈS (`40187` Reaper, `38031` Bonebreaker) |
| **Hero Response**/**Hero Action** | sous-type dédié, pas le type nu (`27009` Web-Bracelet) |
| un second Interrupt/Response/mot-clé annoncé | vérifier qu'il a vraiment un module (`wd077b`) |
| mot-clé cité mais pas imprimé sur CETTE carte | ne pas coder de capacité fantôme |
| icône de ressource | vérifier contre une carte du MÊME PACK, jamais à vue (leçon Lockjaw) |

**Bases automatiques à ne pas recoder inutilement** : `Toughness` et
`Restricted` sont lus par le moteur directement dans `desc`, aucun module
n'est nécessaire pour eux.

Si un mot ou une tournure ne figure pas dans la liste mais laisse un doute :
appliquer la règle « en cas de doute » ci-dessus.

## Étape 6 : Bloc nombres, texte ↔ code

Relever chaque valeur numérique imprimée (coûts, seuils, PV, compteurs,
« X fois », limites, distances) et vérifier qu'elle est identique dans
`data/cards.json` (`desc`) ET dans le script Python. Ce seul filet a trouvé
`wd077b` tout seul le 20/08/2026 : ne jamais le sauter.

## Étape 7 : Bloc tests par capacité, preuve par substitution

Pour CHAQUE capacité distincte (chaque bloc Action/Response/Interrupt/When
Revealed... séparé sur le texte imprimé) :

1. Écrire un cas dans `tools/test_capacites.py` qui monte une position réelle
   avec l'API Puzzle, déclenche la capacité, et vérifie l'état du monde.
2. Le cas doit être **sujet** : le `card_id` apparaît dans le NOM du cas.
3. **Preuve par substitution, obligatoire** : retirer/commenter le module,
   relancer le cas, constater ROUGE. Remettre le module, constater VERT.
4. Clés déterministes utiles : `main_exclusive`, `cibles`, `surpayer`,
   `payer_avec`, `accepter_choix`, `heros2`.
5. Pour une capacité de tour de jeu : `Puzzle.Attack`, `Puzzle.Scheme`,
   `Puzzle.Action` plutôt que « hors de portée du harnais ».

Aucune carte n'est « terminée » tant qu'il reste une capacité sans cas sujet
et sans preuve par substitution.

## Étape 8 : Bloc autoplay ciblé, grep exhaustif des erreurs

1. `tools/autoplay.py` sur le deck/scénario qui contient la carte, au moins
   8 parties, contre le même vilain qu'un héros TÉMOIN dans la même fournée.
2. Grep **exhaustif** de tous les logs, pas seulement le compteur d'incidents :
   ```bash
   for f in /tmp/autoplay_*.log; do
     grep -c "NameError\|AttributeError\|TypeError\|KeyError\|AssertionError" "$f"
   done
   ```
   Résultat attendu : 0 partout.
3. **Lire le journal ligne à ligne** pour les parties qui touchent
   directement la nouvelle carte, pas seulement grep les mots d'erreur.
4. Comparer le taux de blocage de la nouvelle carte à celui du témoin.

## Ce que ces blocs ne peuvent pas voir

Une vraie partie jouée par un humain dans le navigateur reste le seul juge
de « est-ce que la carte est agréable et fait ce qu'elle promet ». Si ce
point n'a pas été fait, l'écrire noir sur blanc dans le rapport de fin de
travail. Jamais « à vérifier en partie réelle » sans dire PRÉCISÉMENT quel
outil manque.

## Gabarit à copier, une fois par carte

```
### <card_id> : <nom de la carte>

- [ ] Étape 2 : carte(s) de référence : ...
- [ ] Étape 5 : texte-contre-code : mots-pièges vérifiés (lister) : ...
      Résultat : ...
- [ ] Étape 6 : nombres texte ↔ code : ...
      Résultat : ...
- [ ] Étape 7 : cas test_capacites par capacité, preuve par substitution :
      capacité 1 : cas <nom>, rouge sans module / vert avec : capacité 2 : ...
      Résultat : ...
- [ ] Étape 8 : autoplay ciblé : N parties, témoin <héros>, grep tracebacks : 0,
      lecture du journal : ...
      Résultat : ...

Carte terminée : OUI / NON : si NON, ce qui manque et pourquoi.
```
