# Standard II et III étaient codés, et personne ne pouvait les choisir

**Question d'un joueur, 16/09/2026** : « is standard III implemented ». Puis
décision de l'utilisateur : « il faudrait proposer standard 1, standard 2 et
standard 3 à la place de juste standard ».

## Ce qui était vrai, et ce qui ne l'était pas

Les cartes étaient là, et elles marchaient :

| Set | Cartes | Scripts | Jouable avant le 16/09 |
|---|---|---|---|
| Standard I | 7 | ✅ | oui, partout |
| Standard II | 7 | ✅ | **jamais** : aucun scénario ne le déclare |
| Standard III | 7 | ✅ | oui, mais seulement dans les 12 scénarios de Web of Deceit |

**Le manque n'était pas le code, c'était l'écran.** La ligne de difficulté
n'offrait que « Standard » et « Expert », et `catalog.js:268`
(`encounterKind`) écarte de la liste des modulaires tout set dont le nom
commence par `standard`. Un joueur n'avait donc aucun moyen d'ajouter Standard
II ou III à un scénario qui ne les déclarait pas lui-même. Les 7 cartes de
Standard II n'avaient, à ce titre, **jamais été jouées une seule fois**.

⚠ **Fausse piste traversée en route, notée parce qu'elle peut resservir.** Le
set `standard_ii` référence la carte `24053`, qui semblait absente de
`cards.json` et sans script : de quoi conclure que le set était cassé. Elle est
en réalité déclarée comme RÉIMPRESSION :

```json
{ "card_id": "24053", "full_link": "01190" }
```

`full_link` (`src/cards/database.py`) copie le paper, lie l'image ET fait
résoudre le script de la carte d'origine. `24053` est « Shadow of the Past »,
la même carte que `01190` du Standard de base, au texte près. Un inventaire qui
ne lit que les entrées portant `name` et `set_name` ne voit aucune réimpression
et croit à un trou.

## Ce qui a été livré, le 16/09/2026

`public/js/prepare/niveau-standard.js` (nouveau). La règle, relevée dans
`data/scenarios/` plutôt que supposée :

```
rhino        -> ["standard"]
rhino_expert -> ["standard", "expert"]                    Expert S'AJOUTE
wd_kingpin   -> ["kingpin", "standard_iii", "bodyguard"]  III REMPLACE
```

D'où : **le niveau choisi remplace le set de la famille standard, et ne touche
à rien d'autre** — ni Expert, ni les modulaires, ni les sets propres au
scénario. Un scénario qui ne déclare aucun set standard n'en reçoit pas :
lui en ajouter un durcirait la partie sans que personne l'ait demandé.

- `app.js` : trois boutons « Standard I / II / III » à la place du bouton
  unique, Expert inchangé à côté. Le niveau est **présélectionné d'après le
  scénario** (ouvrir Web of Deceit montre Standard III, et non Standard I sur
  une partie qui n'en est pas une). Le récapitulatif de l'étape finale dit le
  niveau.
- `launcher.js` : le descripteur applique le niveau, **pour les deux tables** du
  mode Bataille.
- `d.standard` est un axe SÉPARÉ de `d.base` : dans le jeu, Expert s'ajoute au
  Standard, il ne le remplace pas. Passer en Expert garde donc le niveau choisi.

## Les preuves

`ui-check/tests/niveau-standard.spec.ts`, 8 cas (`npm run niveau-standard`) :
le remplacement qui épargne Expert, les sets du scénario intacts, le scénario
sans set standard qui n'en reçoit pas, le `standard_pvp` du mode Bataille qui
n'est PAS de la famille, l'absence de doublon, la présélection d'après le
scénario, la valeur inconnue qui retombe sur Standard I, et l'ordre des trois.

Vérifié par mutation : en faisant AJOUTER le set au lieu de le remplacer, ce
sont exactement les deux cas de garde qui rougissent (scénario sans set
standard, mode Bataille). Les 23 cas de l'assistant restent verts.

## Ce qui n'est PAS fait

- **Aucune partie n'a été jouée en Standard II ou III** depuis ce changement :
  la preuve est celle des tests, pas celle du jeu.
- Les 10 scénarios d'Age of Apocalypse ne déclarent toujours pas
  `standard_iii`, alors que le set appartient à cette boîte. Choix du jeu
  officiel ou oubli du portage : non tranché.
- `encounterKind` continue d'écarter les sets standard de la liste des
  modulaires, et c'est voulu : ils ont leur propre sélecteur maintenant.

## Statut

**Traité le 16/09/2026.** Non déployé au moment où cette fiche est écrite.
