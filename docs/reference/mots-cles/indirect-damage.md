# Indirect damage (dégâts indirects)

**Texte imprimé / définition** : « [star] <carte>'s attacks deal indirect damage. » Les dégâts de l'attaque ne tombent plus sur la cible
désignée : le joueur attaqué les **répartit lui-même** entre les personnages qu'il contrôle (identité et alliés).

**Mécanisme moteur** : `AbilityFactory.UnitAttackGainKeyword("This", indirect_damage=True)` (`do_attack.py`) ; le message
`CheckIfAttackMessageHasKeyword` pose `property.deal_indirect_damage`, lu par `can_attack.py` (~l.480) qui appelle
`TakeIndirectDamage` -> `player.AssignDamage` : le joueur reçoit une question **« Assign N damage »** (`ChooseAbilities`, cibles avec
répétition, plage 0..N) puis chaque personnage reçoit ses points en un seul coup (`DamageProperty(.., is_indirect_damage=True)`).

**Carte exemple** : `16137` Starshark (script de référence) ; `hz014` The Vengeful Wing (pack Hepzibah, `[star]` permanent, cas `[hz]`).

**Pièges connus** :
- ⚠ **La défense s'applique AVANT** : `calculated_damage` est déjà réduit par la DÉF du défenseur (ATQ 3 contre DÉF 2 = 1 dégât
  indirect). Seule la répartition change, pas le calcul.
- ⚠ **Avec UN seul personnage, indirect et direct sont indiscernables** (« va subir 3 dégâts » dans les deux cas). Pour le prouver au
  harnais : un allié en jeu, **le héros ET l'allié inclinés** (sinon l'un défend), et `cibles=["<allié>", "<allié>", "<héros>"]` : les
  TROIS entrées sont nécessaires (une liste plus courte fait échouer la question « Assign N damage », sans erreur visible dans le
  résultat du cas, seulement `<E> ... WhenPlayerChooseAbility failed` au journal). Une attaque directe ne pose JAMAIS cette question.
- Robuste (`Tough`) ne distingue pas non plus les deux cas avec un seul personnage : il remplace l'événement « subir 3 dégâts » en bloc.

**Variantes maison** : `hz014` (Hepzibah) ; `nt015`, `sk166`, `sk224b` portent aussi `indirect_damage=True`.
