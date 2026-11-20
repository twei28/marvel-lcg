# Absorb (mot-clé MAISON, scénario Black King de Hellfire Hunt)

**Texte imprimé / définition** : sur les trois stades de Sebastian Shaw (`hf201`-`hf203`) : « *Absorb* — **Forced Response** : After Sebastian Shaw takes damage from an attack, place energy counters on him equal to the damage taken. » (stade III : « Place 1 additional energy counter here. »). Ce n'est PAS un mot-clé du livret (p. 3) : c'est le NOM d'une capacité de la carte, que d'autres cartes citent : `hf207a` / `hf207b` Black King (« When Sebastian Shaw's *Absorb* ability triggers while there is an energy counter on him... »).

**Mécanisme moteur** : aucun mécanisme générique. `AbilitesDeShaw()` (`src/cards/pack/hellfire_hunt_black_king/__init__.py`) = `AbilityFactory.AfterUnitTookDamage(ForcedResponse, "This", ..., is_from_attack=True)` + `Faces.PlaceCountersOn([shaw], message.took_damage, 'energy', effect)`. Le compteur est le compteur nommé `energy` (déjà dans `CardFace.COUNTER`, libellé FR « énergie » dans `compteurs-fr.ts`).

**Carte exemple** : `hf201` Sebastian Shaw (I). L'« Absorb » est déclenché par des DÉGÂTS D'ATTAQUE seulement (un `Puzzle.Damage`, un effet de carte, ne place rien).

**Pièges connus** :
- **La Tactique du Roi (Black King) est une INTERRUPTION forcée sur le MÊME message** (`AfterUnitTookDamage`) que la Réponse forcée Absorb : le moteur résout les interruptions forcées AVANT les réponses forcées (`TimingPriority`, `ability_type.py`). Les compteurs déjà présents sont donc retirés (et convertis en menace) AVANT que l'Absorb n'en pose de nouveaux. Cas `[hf] hf207a King's Tactic ... AVANT l'Absorb`.
- « Max 1[per player] times per round » (face B) : `world.stat.AddRoundCounter` / `GetRoundCounter` (remis à zéro à la fin du round) ; la FAQ du livret p. 22 dit qu'au-delà de la limite la Tactique ne part pas et que les compteurs s'empilent sur Shaw ; les instances de la face A ne comptent pas.
- Shaw (stade I/II/III) perd ses compteurs à chaque changement de stade (nouvelle carte).

**Variantes maison** : tout le mot-clé est maison ; question ouverte de la limite « par joueur » : `docs/packs/hellfire-hunt-black-king/QUESTIONS.md`.
