# Cloak

**Texte imprimé / définition** : AUCUNE. Le mot est imprimé en verbe, sans
définition ni rappel entre parenthèses :
- `tl015` * Karai : « **When Revealed**: Cloak Karai. » et « **When Defeated**:
  Cloak the villain. » ;
- `tl016` Foot Soldiers : « **When Revealed**: Cloak Foot Soldiers. ».

Ni les scans du zip « TMNT Heroes / Leonardo v3 », ni l'insert de règles du pack
(« Katana Weapon Rules », qui ne traite que des katanas) ne le définissent.
Le mot n'existe pas dans le moteur (`grep Cloak src/` ne trouve que les cartes
Cloak & Dagger, sans rapport). **Mot-clé maison non défini** (pack `leonardo`,
auteur Inkwire, phase A du 15/10/2026).

**Mécanisme moteur** : aucun. `Cloak(effect, face)` est un STUB SANS EFFET dans
`src/cards/pack/leonardo/leonardo_nemesis/__init__.py` ; les trois appels y
passent, de sorte qu'une seule fonction sera à écrire quand la règle sera
donnée. Question prête : `.planning/tmnt/leonardo-phase-a.md`, Q1.

**Carte exemple** : `tl016` : Foot Soldiers (un seul effet, `Cloak`).

**Pièges connus** :
- Ne rien inventer : la question est posée, pas arbitrée. Hypothèses à
  proposer (non retenues) : statut « caché » rendant la carte intouchable
  jusqu'à son activation ; mot-clé de type Stalwart/Toughness ; état propre à
  la mini-série TMNT (à vérifier avec les 3 autres tortues, qui peuvent
  l'employer aussi).
- `Cloak the villain` (When Defeated de Karai) vise le VILAIN, pas Karai.

**Variantes maison** : à compléter après la réponse de l'utilisateur.
