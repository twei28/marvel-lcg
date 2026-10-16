# Piercing

**Texte imprimé / définition** : « Piercing. *(This attack discards a tough
status card instead of being blocked by it.)* » Une attaque perçante défausse
les cartes de statut Robustesse (tough) de la cible au lieu d'être absorbée
par elles.

**Mécanisme moteur** : propriété booléenne `piercing` de la dataclass des
propriétés d'attaque (`src/game/card/face/attribute/can_attack.py`, commentée
« discard tough » ; le pendant `lost_piercing` sert aux retraits). Deux
chemins pour l'accorder :
- statiquement, via `piercing=True` des fabriques d'attaque
  (`src/game/ability/factory/do_attack.py`, ex. `ab008` du pack `albert`) ;
- dynamiquement via `message.GainPiercing(effect)` sur le message d'attaque
  (`src/game/message/sender/sender_damage.py`, `sender.py`) — chemin des
  textes « this attack gains piercing ».
Les conditions « if this attack has piercing » se testent via
`with_piercing` (`src/game/ability/factory/damage.py`,
`WhenRecalculateAttackDamage`).

**Carte exemple** : `ab008` (pack `albert`) : attaque déclarée avec
`piercing=True` dans la fabrique.

**Pièges connus** :
- Piercing ne retire la Robustesse que dans le cadre d'une ATTAQUE. Un effet
  de dégâts directs hors attaque reste bloqué par tough.
- Un événement qui « gains piercing » selon une condition doit brancher la
  condition sur le paiement ou l'état AU MOMENT de l'attaque, pas à celui du
  jeu de la carte (même piège que « if this attack has ranged or piercing »,
  listé dans PROCESSUS-CARTE.md comme non rendable fidèlement sur certains
  événements).

**Cas `tc012` Persuader (pack `casey_jones`)** : « When you make a basic attack, exhaust Persuader
→ you get +1 ATK for that attack. This attack gains piercing » = `WhenUnitWouldAttack(HeroInterrupt,
"You", op, is_basic_attack=True)` + `message.GainATKForThisAttack(1)` + `message.GainPiercing(effect)` sur
le message d'ATTAQUE (pas `WhenUnitUseBasicPower`, qui couvre aussi la défense et le contre). Cas
`[casey] tc012` : Rhino Tough, 4 dégâts passent et le Tough est défaussé, contre 0 dégât (Tough absorbe)
sans la carte.

**Variantes maison** : `ho016` (* Bullseye, pack `harry_osborn`) : « [star]
Bullseye's attack gains piercing and overkill » — capacité étoile (Expert)
posée par `GainPiercing`/`GainOverKill` sur l'attaque en cours.
