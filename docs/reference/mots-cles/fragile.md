# Fragile

**Texte imprimé / définition** : « Fragile. (Attacks against this character
gain overkill.) »

**Mécanisme moteur** : mot-clé maison, déjà défini dans le pack
`determination` (aspect fan-made, `src/cards/pack/determination/__init__.py`,
fonction `Fragile()`) avant même le pack `okoye`. Le crochet lui-même est
**officiel** : la carte 33032 (Marked) fait exactement ceci pour un sbire —
`message.GainOverKill(effect)` sur la fenêtre `WhenUnitWouldAttackUnit`. Il
suffit de changer la cible : `"This"` au lieu du sbire attaché par Marked.

```python
def Fragile() -> 'Ability':
    def fragile(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        message.GainOverKill(effect)

    return AbilityFactory.WhenUnitWouldAttackUnit(
        AbilityType.NonKeyword,
        None,
        "This",
        fragile,
    )
```

Le pack `okoye` réutilise CE mécanisme tel quel (`src/cards/pack/okoye/okoye/__init__.py`,
fonction `Fragile()`), avec une différence : Midnight Angel Armor (ok012/ok013)
retire ce mot-clé au personnage attaché (« loses the fragile keyword »). Le
moteur n'a pas de primitive générique pour désactiver une ability imprimée sur
une AUTRE carte : la condition est donc intégrée directement dans le handler
(pas d'overkill accordé si Midnight Angel Armor est attachée), ce qui produit
le même résultat observable que « perdre Fragile » sans modifier le mécanisme
partagé avec `determination`.

**Carte exemple** : `ok017` (jeton Dora Milaje) et `ok018` (jeton Midnight
Angel), les deux seuls porteurs du mot-clé dans ce pack — `GetAbilities()`
retourne simplement `[Fragile(), Legion()]`.

**Pièges connus** :
- `WhenUnitWouldAttackUnit` (et pas `WhenUnitWouldAttack`) est indispensable :
  la première fenêtre ne contient jamais de cible allié tant que le
  défenseur n'est pas choisi (voir §10 du guide, piège « la fenêtre du
  défenseur »).
- Overkill se réévalue par attaque, pas de façon permanente sur la carte :
  aucun état à nettoyer en fin de partie.

**Variantes maison** : `okoye` ajoute une clause de retrait conditionnelle
(Midnight Angel Armor) qui n'existe pas dans `determination`. Toute nouvelle
carte du pack `okoye` qui retirerait Fragile pour une autre raison devra
étendre cette même condition plutôt que d'écrire un second mécanisme.
