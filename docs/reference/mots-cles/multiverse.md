# Multiverse

**Texte imprimé / définition** : le mot `Multiverse.` apparaît seul, en tête du
bloc de texte d'un **allié signature**, sans aucune parenthèse explicative.
Aucun des trois packs qui l'emploient ne le définit.

**Définition retenue** (glossaire fan-made de MC4DB, adoptée le 29/09/2026 ;
elle remplace l'arbitrage du 05/09/2026) :

> « Identity-specific cards with the multiverse keyword are optional
> **replacements** for the given card of the corresponding card number.
> During deckbuilding, you may choose to replace the identity-specific card
> sharing its card number with an identity-specific card with the multiverse
> keyword. Doing so satisfies your deckbuilding requirements. During a
> campaign, this choice cannot be unmade. »

Autrement dit : une carte Multiverse est **une autre version d'un numéro de
set déjà occupé**. Au deckbuilding, le joueur prend **l'une OU l'autre**,
jamais les deux. Choisir la version Multiverse satisfait l'obligation
d'emporter les cartes signature. En campagne, on ne revient pas dessus.

⚠ **Ce qui a changé le 29/09/2026.** La fiche disait jusque-là que le mot-clé
« n'interdit pas de les mettre toutes les deux dans le deck, seulement d'en
avoir deux en jeu ». C'était faux : trois decks de départ emportaient les deux
versions (16 signatures pour 15 numéros). Ils ne gardent plus que l'originale.

Les paires du dépôt, déclarées par la clé **`multiverse_of`** de `cards.json`
sur la carte Multiverse (même nom de clé que MC4DB) :

| Carte Multiverse | Remplace (même numéro de set) | Pack |
|---|---|---|
| `ra002` `* Odinson` | `ra003` `* Roz Solomon` | `rainy` (Thor, Jane Foster) |
| `bc003` `* Spider-Man` (AVENGER) | `bc002` `* Spider-Man` (SYMBIOTE, WEB-WARRIOR) | `blackcat` |
| `bw003` `* Ironheart` | `bw002` `* Silk` | `brawn` |

⚠ La paire `brawn` est **déduite**, pas lue : l'auteur n'imprime pas les
numéros dans `cards.json`, et le deck de départ de l'auteur emporte Silk sans
Ironheart. Les deux autres paires viennent des noms de fichiers du zip
(« 1 Spider-Man (black) / (red) ») et du deck de Rainy (16 entrées).

**Mécanisme moteur** : **AUCUN, zéro ligne de code**, comme avant. Le
remplacement est une règle de DECKBUILDING : elle vit dans les decks de départ
(une seule version) et dans l'éditeur, `validerDeck` de
`public/js/deckbuilder/regles.js`, qui refuse un deck contenant une carte
Multiverse ET la carte que désigne son `multiverse_of` (signatures du héros
comprises, donc aussi pour Stan Lee). Verrou :
`outils/verifier-regles-deck.mjs` (quatre cas). `PlayerSetup` n'a rien à
vérifier : un deck de départ ne porte plus qu'une version, et l'unicité native
(l'étoile `*`) reste le filet en jeu.

**Carte exemple** : `ra002` `* Odinson`. Son module ne fait rien pour le
mot-clé ; le commentaire qu'il porte sur « une seule version par deck » est
désormais exact au sens strict.

**Pièges connus** :

- ⚠ **`MULTIVERSE` est aussi un TRAIT**, et les deux notions n'ont rien à voir.
  `wd029` Multiverse Recruit (pack `web_of_deceit`) porte
  `"traits": ["MULTIVERSE"]` ; Blink (Earth-295) emploie le même mot comme
  trait. Un trait va dans `traits`, ce mot-clé-ci va dans `multiverse_of`.
- ⚠ **Ne pas croire que les deux versions sont deux illustrations d'une même
  carte.** `bc002` et `bc003` ont des statistiques, des traits et des
  capacités DIFFÉRENTS : ce sont deux `card_id` distincts qui se disputent un
  numéro.
- ⚠ **Un nouveau pack qui imprime `Multiverse`** doit recevoir sa clé
  `multiverse_of`, sans quoi l'éditeur laissera passer les deux versions.
- ⚠ **Campagne** : « this choice cannot be unmade » n'est appliqué nulle part
  (le carnet de campagne ne mémorise pas le choix). Écart connu, sans cas.

**Variantes maison** : aucune. Trois packs, trois auteurs (`rainy`, `brawn`,
`blackcat`), même écriture nue et même absence de définition.
