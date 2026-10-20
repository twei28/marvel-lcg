# Requirement

**Texte imprimé / définition** : « Requirement ([mental]). *(While paying for
this card, spend the listed resources.)* » Pour jouer la carte, le paiement
doit **comporter** les ressources listées, en plus d'en couvrir le coût. Ce
n'est pas un coût supplémentaire : les ressources listées sont **incluses**
dans le coût, elles en contraignent seulement la couleur.

Exemple : Web Binding (`27006`) coûte 2 avec `Requirement ([mental])`. Il faut
donc payer 2 ressources dont **au moins une** mentale, pas 3.

**Mécanisme moteur** : clé `desc.Requirement`, une chaîne de couleurs au même
format que `RES` (`"B"`, `"R"`, `"BB"`, `"YBR"`…). Lue nativement par
`HasCost.RegisterAttribute("Requirement", parse2)`
(`src/game/card/face/attribute/has_cost.py:24`), puis exposée par
`GetPrintedCostWithRequirement()`. **Aucun script requis** : c'est une des
« bases automatiques » du guide, au même titre que `Toughness` ou `Restricted`.

Le script d'une carte à Requirement ne le mentionne donc jamais. Vérifié sur
`27006.py` (Web Binding), qui ne code que son Hero Interrupt.

**Cartes exemples** (toutes officielles) :

| Carte | `desc.Requirement` | Imprimé |
|---|---|---|
| `27006` Web Binding | `"B"` | Requirement ([mental]) |
| `28013` No Quarter | `"R"` | Requirement ([physical]) |
| `29020` R&D Facility | `"BB"` | Requirement ([mental][mental]) |
| `27049` * Spider-Man | `"YBR"` | Requirement ([energy][mental][physical]) |

**Pièges connus** :

- **Ce n'est pas un coût en plus.** Lire « Requirement ([mental]) » sur une
  carte à 2 comme « 2 + 1 mental » est faux : c'est « 2, dont au moins 1
  mental ».
- **Ne pas le confondre avec « If you paid for this card using a [X]
  resource »**, qui est une CONDITION D'EFFET, pas une condition de jeu : la
  carte se joue dans tous les cas, seul le bonus dépend de la couleur payée.
  Le pack `doctor_doom` porte les deux tournures, parfois à une carte d'écart
  (`dd003` Doombot a un Requirement ; `dd004` « This World Is Mine! » a la
  condition d'effet).
- La chaîne se répète pour exiger plusieurs fois la même couleur (`"BB"` = deux
  mentales), exactement comme `RES`.

**Variantes maison** : aucune. Le pack fan-made `doctor_doom` (`dd003`
Doombot, `Requirement ([mental])`) l'emploie tel quel.

**Requirement ([wild])** : `"Requirement": "G"`. Le paiement doit COMPORTER au moins une icône
wild (une carte dont `desc.RES = "G"`, ou une ressource générée wild : Overswing de `tc001a`
génère `GGG`). Quatre icônes colorées sans wild (RR + YY) ne suffisent PAS. Précédent :
`dt084` Off the Cuff. Pack `casey_jones` : `tc005` Grand Slam (glyphe étoile du scan identique
à `04010` / `04033`, vérifié par découpe : `.planning/tmnt/pics-casey-icones/wild.png`). Cas :
`[casey] tc005` (wild + physique accepté, physique + énergie refusé).

**Exigence GAGNEE en cours de partie** (`gs239q` Entropy Ascendant, Galactic Storm, 20/10/2026 : « Each event card
gains requirement ([energy]) ») : pas de cle `desc`, une capacite constante sur `Message.WhenCalculateEffectCost`
(`message.is_play` et `Event.IsType(message.check_effect.this)`) qui convertit UNE ressource generique du cout en
[energy] (`ResRBYGA(a - 1, rbyg + Y)`), comme le moteur encode `desc.Requirement` (has_cost.py). Un evenement a 0
devient « [energy] » (question Q-GS2-3). Cas `[quasar] gs239q` (RR refuse, YY accepte, amelioration non touchee).
