# HIDDEN (méchant caché, Hala Ultimatum)

**Texte imprimé / définition** : Galactic Storm 1.2 p.14, trait HIDDEN (scénario 3, Hala Ultimatum) :
« While the villain has the HIDDEN trait, players cannot affect the villain with player cards: no attacks by
heroes or allies, no damage through overkill when a minion is defeated with excess damage, no status card
placed on the villain, no upgrades or other player cards attached to it, no discarding of its tough status
cards (piercing or any player card ability). If a card ability has multiple targets and one is the villain,
players may only play that card or initiate that ability if at least one other valid target exists; if the
villain is the only target, the card cannot be played / ability cannot be initiated. **Conversely, the villain
cannot attack players while HIDDEN: whenever a player would be attacked by the villain, that player is dealt a
facedown encounter card.** After the villain flips to its DISCOVERED side, all attachments, status cards, boost
cards, damage and other elements remain. After a villain stage is defeated, the next stage enters play on the
same side as the just-defeated stage (in most situations DISCOVERED). »

Deux moitiés, deux briques moteur différentes :
1. **IMMUNITÉ** (déjà codée AVANT ce lot, briques communes du 20/10/2026) : documentée en entier dans
   `mots-cles/immunite-cartes-joueur.md` (fiche sœur, ne pas dupliquer ici).
2. **ATTAQUE** (codée dans CE lot, GS-6) : le méchant HIDDEN n'attaque jamais directement — chaque attaque
   qu'il ferait devient une distribution d'une carte de rencontre face cachée au joueur visé.

**Mécanisme moteur (moitié attaque)** : le message `Message.WhenUnitWouldAttack` (émis par
`CanAttack.AttackInternal`, `src/game/card/face/attribute/can_attack.py`) porte `against_player` (le joueur
visé par l'attaque de base) et hérite de `CanBeInstead` : tout gestionnaire qui appelle `message.SetBeInstead(effect)`
annule l'attaque entière avant qu'aucune cible ne soit choisie ni qu'aucun dégât ne soit calculé (`can_attack.py`,
test `if would_atk_message.is_be_instead: ... return None`). On compose :

```python
AbilityFactory.WhenUnitWouldAttack(
    AbilityType.ForcedInterrupt, "This", rediriger,
    conditions=[lambda effect, message: effect.this.HasTrait("HIDDEN")],
)
```

où `rediriger` distribue la carte puis annule :

```python
def rediriger(effect, message):
    joueur = message.against_player
    if joueur is not None:
        joueur.DealEncounterCards(1, effect)
    message.SetBeInstead(effect)
```

Exemples déjà en place dans le dépôt pour chaque brique : `AbilityFactoryEnemy.EnemyCannotActivate`
(`src/game/ability/factory/enemy.py`) pour le pattern `message.SetBeInstead(effect)` sur une attaque ; `Player.DealEncounterCard(s)`
(`src/game/player/action/player_action.py`) pour la distribution, utilisé entre autres par `ar012` (Ares), `sk248`
(Skrull Elite War Skrull), `sk065` (Lyja) pour « deal yourself 1 facedown encounter card ».

**Face DISCOVERED (retournement qui garde l'état) et avancée de stade** : le retournement d'un méchant à double
face (face a = HIDDEN, face b = DISCOVERED) se fait par `carte.Flip(effect)` (`this.card.Flip(effect)`) : MÊME
objet carte, donc attachements, cartes d'état, boosts et dégâts restent automatiquement (modèle Skrull Menace
`sk189/sk190/sk191` Spider-Woman/Queen Veranke, et `mojo 39012a/b` Spiral, et `60110/60111` Typhoid Mary). Après
la défaite d'un stade, `Scenario.AdvanceVillainStage` (`src/game/player/scenario.py`) choisit nativement, dans
la carte du stade suivant, la face dont le NOM est le même que celui de la face juste vaincue — c'est pour cela
que **toutes les faces HIDDEN doivent porter le même nom (« Kree Leader ») et toutes les faces DISCOVERED le
même nom (« Tanalth »)** à travers les trois stades : aucun code à écrire pour la règle « le stade suivant entre
du même côté », elle est native, à condition de nommer les faces correctement.

**Carte exemple** : `gs138a`/`gs139a`/`gs140a` (Kree Leader, HIDDEN, stades I/II/III) et `gs138b`/`gs139b`/
`gs140b` (Tanalth, DISCOVERED, stades I/II/III), `src/cards/pack/galactic_storm/hala_ultimatum/`.

**Pièges connus** :
- `against_player` peut être `None` si l'attaque de base ne vise pas directement un joueur (cible choisie par
  un autre mécanisme) : dans ce cas, aucune carte n'est distribuée mais l'attaque reste annulée (lecture
  recommandée, voir `.planning/todos/2026-10-20-gs6-hala-ultimatum-questions.md`).
- Le retournement HIDDEN→DISCOVERED est UNIQUE ET DÉFINITIF dans ce scénario (déclenché par la révélation de
  « Reckoning Begins » 2A→2B) : contrairement à Veranke, il n'y a pas de va-et-vient ; inutile de prévoir un
  retour à HIDDEN.
- Le flip ne doit s'exécuter que si le méchant est encore HIDDEN (`HasTrait("HIDDEN")`) au moment où
  « Reckoning Begins » se révèle, sinon un flip répété le renverrait par erreur vers HIDDEN.
- La moitié immunité continue de s'appliquer MÊME avec 0 PV restants tant que la face est HIDDEN (elle ne
  retombe jamais toute seule : seule la révélation de 2B la retire).

**Variantes maison** : aucune autre carte du dépôt ne porte HIDDEN à ce jour (20/10/2026) ; TARGETED est réservé
(Punisher MC×DC 2026 p183, non porté).
