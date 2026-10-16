# All-purpose counter (compteur polyvalent)

**Texte imprimé / définition** : « Place 1 all-purpose counter on ... » (tx004b Replicate,
tx006 Swarm Superiority). Terme OFFICIEL du jeu : un compteur dont le type est défini par la
carte qui le porte (FAQ officielle MC4DB du 29/09/2026 : « the card that an all-purpose counter
is on defines the type of that counter »).

**Mécanisme moteur** : `Faces.PlaceCountersOn(cibles, n, 'all-purpose', effect)` ; le moteur
convertit en `ConvertAllPurpose` (premier compteur nommé que la carte porte, sinon `counter`).
Le scénario Baxter Stockman force le nom par card_id (`COMPTEUR_DU_SBIRE`,
`baxter_stockman/__init__.py`) : voir `replicate.md`.

**Carte exemple** : `gmw/16034` Battery Pack (compteur déplacé sur un amélioration `ammo`),
`tx006` Swarm Superiority.

**Pièges connus** : sur une carte SANS compteur nommé, `'all-purpose'` devient le compteur
générique `counter`, sans effet : toute carte dont les valeurs suivent un compteur doit nommer
le sien.

**Variantes maison** : aucune.
