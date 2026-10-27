# Rupture X (maison, scénario `the_hunger_core`, préfixe `hg`)

**Texte imprimé** (livret officiel, page 4) : « Rupture X — Forced Response: After a Metazombie is defeated, The
Hunger Core takes X damage. This damage ignores [[shielded-by-the-horde]]. »

**Mécanisme moteur** : `AbilityFactory.WhenUnitBeDefeated(ForcedResponse, which_unit, op)`, modèle `defeated.py`.
`which_unit = CardFinder(traits=["METAZOMBIE"], card_type=Villain)` (accepté directement comme `CARD_TYPE`,
`condition/card_type.py:99` : `isinstance(check_rule, CardFinder)` → `Referential.Check`). `op` appelle
`LeCoeur(effect).DealDamage([LeCoeur(effect)], X, effect)` si le Cœur est encore en jeu.

« This damage ignores Shielded by the Horde » **n'exige aucun code de contournement** : la source de l'effet est
l'ability de `hg001`/`hg002`/`hg003` elle-même (une face `EncounterVillain`, pas `PlayerCard`), donc
`PlayerCardImmunity.IsPlayerCardEffect` renvoie déjà `False` et la brique ne l'aurait de toute façon pas bloquée
(voir le piège de [[shielded-by-the-horde]]). La phrase du livret est une clarification pour les joueurs, pas une
instruction de code.

**Carte exemple** : `hg001` Rupture 1, `hg002` Rupture 1, `hg003` Rupture 1 (texte identique sur les trois stades,
malgré « Just a Core 2 » qui, lui, change au stade III).

**Pièges connus** :

- **« After a Metazombie is defeated »** : TOUT Metazombie, pas seulement l'actif — `WhenUnitBeDefeated` n'a pas de
  condition sur le jeton actif.
- **Rupture peut vaincre le Cœur pendant qu'il reste des Metazombies en jeu** (FAQ, page 8 : « Can Rupture defeat
  the Core while Metazombies are in play? Yes. »). Les dégâts passent MÊME si `Shielded by the Horde` protège
  encore le Cœur à ce moment précis (d'où la clause « ignores »). La défaite du Cœur déclenche alors
  `Deeper Inside` ([[just-a-core-x]] ne s'en occupe pas, voir `hg004b`/`hg005b`).
- Le Metazombie vaincu qui déclenche Rupture n'est, lui, PAS retiré du jeu : il part dans la défausse du Horde deck
  (`commun.QuandMetazombieVaincu`), distincte de la défausse de rencontre.

**Variantes maison** : aucune à ce jour.
