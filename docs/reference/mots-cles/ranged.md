# Ranged

**Texte imprimé / définition** : « Ranged. *(This attack ignores retaliate.)* »
Une attaque à distance ignore la Riposte du défenseur. Le mot-clé se porte sur
l'ATTAQUE, jamais sur le personnage : un personnage « gains ranged » veut dire
« ses attaques gagnent ranged ».

**Mécanisme moteur** : propriété booléenne `ranged` de la dataclass
`AttackProperty` (`src/game/card/face/attribute/can_attack.py`, commentée
« ignore retaliate »). Elle n'est lue qu'à un seul endroit :
`src/game/card/face/attribute/can_retaliate.py` court-circuite `ResolveRetaliate`
si `atk_message.IsRanged()`. Trois chemins pour l'accorder :
- **permanent, sur les attaques d'un personnage** :
  `AbilityFactory.UnitAttackGainKeyword("This", ranged=True)`
  (`src/game/ability/factory/do_attack.py`) ;
- **ponctuel, sur une attaque que l'on déclenche soi-même** :
  `property=AttackProperty(ranged=True)` passé à `DealDamage` ;
- **ponctuel, sur l'attaque en cours** : `message.GainRanged(effect)`
  (`src/game/message/sender/sender_damage.py`).

⚠ **Aucune clé `desc`.** Contrairement à Guard, Patrol ou Retaliate, `Ranged`
n'existe pas dans la liste blanche `CardFace.KEY` : écrire `"Ranged": "1"` dans
`data/cards.json` fait planter le chargement de la carte. Ranged est toujours
scripté.

**Carte exemple** : `50107b` (* M.O.D.O.K., pack `aos`) :
`UnitAttackGainKeyword("This", overkill=True, ranged=True)`, permanent.
Ponctuel : `ag003` (pack `agent_13`), `AttackProperty(ranged=True)`.

**Pièges connus** :
- **Le sens s'inverse selon le message visé.** `ag005` (pack `agent_13`)
  documente le cas : appeler `message.GainRanged(effect)` sur le message de
  l'ATTAQUE ENNEMIE donne ranged à l'ennemi, l'exact contraire du texte
  « votre attaque gagne ranged ». Pour une attaque que la carte déclenche,
  passer `AttackProperty(ranged=True)` à `DealDamage`.
- Ranged n'annule que la Riposte. Il ne traverse ni la Robustesse (c'est
  [[piercing]]) ni le blocage d'un allié.
- Un `[star]` du genre « X's attacks gain ranged » est un effet PERMANENT de
  l'attachement ou du personnage : `UnitAttackGainKeyword`, pas une réponse.

**Variantes maison** : `gb014` (Vicious Tendrils, pack `gorr`) : attachement
posé sur le vilain qui donne à la fois `retaliate 1` (base automatique, sur le
porteur) et, par capacité étoilée, `ranged` aux attaques de Gorr — les deux
mots-clés se contredisent pour l'adversaire, ce qui est l'intention de la carte.
