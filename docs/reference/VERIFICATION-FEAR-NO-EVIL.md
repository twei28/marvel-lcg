# Vérification du portage de la campagne Fear No Evil (Peur de Rien)

Ce fichier rassemble TOUT le portage de la boîte **Fear No Evil** (pack 60) dans le moteur Marvel Champions décrit par `KIT-CHATGPT-CREATION.md` (et `MOTS-CLES-TOUS.md` pour les mots-clés). Il est figé au 08/10/2026, puis mis à jour le 11/10/2026 pour les cartes revérifiées sur scan (`60001a`, `60003`, `60009`, `60012`, `60018`, `60032`, `60095`, `60161a`, `60191`, `daredevil/__init__.py` ; voir la fin de la section 5).

## Ta mission

Vérifier, carte par carte, que le portage est **fidèle aux vraies cartes et aux règles de la boîte** (livret `mc60_fear_no_evil_rulebook.pdf` et carnet `mc60_fear_no_evil_campaign_log.pdf`, fournis à part). Tu ne réécris rien : tu **signales**.

Pour chaque carte, compare :
1. **La fiche** (`cards.json`) à la vraie carte : nom, sous-titre, type, coût, PV, ATK/THW/SCH/DEF, ressource, traits, icônes de boost, mots-clés, texte imprimé. Tu connais peut-être la carte : dis d'où vient ta certitude (livret, carte connue, déduction) et marque « incertain » si tu n'es pas sûr.
2. **Le script** (`.py`) au texte imprimé : bon type de capacité (Action, Interrupt, Response, Forced), bon déclencheur et bon moment, bonnes cibles, bons coûts, limites (« once per round »), conditions. Une carte sans script est normale si tout son texte est porté par la fiche (mots-clés lus dans `desc`) ; signale-la seulement si son texte demande un effet.
3. **Les scénarios** (section 3) au livret : vilain et ses étapes, manigances, sets de rencontre et modulaires, mise en place, mode expert.
4. **La campagne** (section 4) au livret et au carnet : ordre des affaires, progression, récompenses, conséquences, ce qui passe d'un scénario à l'autre.

**Ne signale PAS comme erreur** un choix listé en section 5 (arbitrages déjà tranchés avec l'auteur du projet), sauf si tu as une preuve qu'il contredit le livret.

## Format de ton rapport

Un tableau par section, une ligne par écart, du plus grave au moins grave :

| Carte (`card_id`, nom) | Gravité | Ce qui est écrit | Ce que dit la vraie carte / le livret | Source de ta certitude |
|---|---|---|---|---|

Gravité : **BLOQUANT** (la partie se joue mal : mauvais nombre, effet absent ou inversé), **ÉCART** (effet proche mais pas exact), **COSMÉTIQUE** (orthographe, sous-titre, trait). À la fin : la liste des cartes que tu n'as PAS pu vérifier, et pourquoi. Pas d'écart sur une carte : ne la cite pas.

Travaille par lots (un set à la fois, dans l'ordre du sommaire) et attends que l'utilisateur dise « suite » entre deux lots.

## Sommaire

1. Les cartes, par set (fiche + script)
2. Le code partagé du pack (`__init__.py`)
3. Les scénarios et les sets de rencontre
4. La campagne
5. Les arbitrages déjà tranchés

## 1. Les cartes, par set

### Set : Daredevil (15 cartes)

#### `60001a` * Daredevil

```json
{
 "card_id": "60001a",
 "type": "Hero",
 "name": "* Daredevil",
 "subtitle": "",
 "desc": {
  "HP": "10",
  "ATK": "2",
  "THW": "2",
  "DEF": "2",
  "HS": "5"
 },
 "traits": [
  "DEFENDER",
  "MARTIAL ARTIST"
 ],
 "set_name": "Daredevil",
 "text": "<i>Superhuman Senses</i> — <b>Action</b>: Play the top card of the [[Sense]] deck as if it were in your hand <i>(paying its cost)</i>.\n<b>Forced Interrupt</b>: When a [[Sense]] upgrade would leave play, place it on the bottom of the [[Sense]] deck instead."
}
```

Script `src/cards/pack/fne/daredevil/60001a.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def check_sense_top(effect: 'Effect', message: 'Message.CheckIfFaceIsLikeInHand') -> bool:
        initiator = effect.GetInitiator()
        if not initiator:
            return False
        return (message.which_face == initiator.additional_deck.GetTop())
    return [*AbilityFactory.YouMayPlayCardLikeInHand(AbilityType.NonKeyword, None, conditions=[check_sense_top]),
            # Rafraichissement du cache `is_like_in_hand` (voir
            # `RafraichirDessusDeckAnnexe`, __init__.py). `AbilityType.Rule`,
            # comme sur Echo (60037a.py) : c'est lui qui garde l'aptitude en
            # ecoute meme quand cette face HEROS part dans `aside_deck`.
            AbilityFactory.WhenCardWouldMoveToArea(
                AbilityType.Rule, CardFinder(card_ids=list(SENSE_DECK_IDS)),
                RafraichirDessusDeckAnnexe)]
```

#### `60001b` * Matt Murdock

```json
{
 "card_id": "60001b",
 "type": "AlterEgo",
 "name": "* Matt Murdock",
 "subtitle": "",
 "desc": {
  "HP": "10",
  "REC": "3",
  "HS": "6"
 },
 "traits": [
  "ATTORNEY"
 ],
 "set_name": "Daredevil",
 "text": "Matt Murdock begins the game with a [[Sense]] deck. <i>(See rulebook p. 26.)</i>\n<b>Forced Interrupt</b>: When a [[Sense]] upgrade would leave play, place it on the bottom of the [[Sense]] deck instead."
}
```

Script `src/cards/pack/fne/daredevil/60001b.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def flip_top_card(player: 'Player', by_effect: 'Effect'):
        if (player.additional_deck.GetSize() == 0):
            player.additional_deck.ShuffleWithDiscardPile(False, by_effect)
        faces = player.additional_deck.Get()
        if not faces:
            return
        Faces.FlipAllTo(faces[:-1], False, by_effect)
        face = faces[-1]
        face.FlipTo(by_effect, face_up=True)
    def move_to_sense_deck(effect: 'Effect', message: 'Message.WhenCardWouldMoveToArea') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        message.ChangeToArea(player.additional_deck, effect)
        def to_bottom():
            if (this.card.area == player.additional_deck):
                this.card.MoveToBottom(player.additional_deck, effect)
            flip_top_card(player, effect)
        RunAt.AfterEventEnd(effect, message, to_bottom)
    def with_sense_deck(effect: 'Effect', message: 'Message.WhenPlayerSelectHero') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)
        initiator = effect.GetInitiator()
        def register_effect(face: 'CardFace'):
            face.effect.Registers(AbilityFactory.WhenCardWouldMoveToArea(AbilityType.Temp0, 'This', move_to_sense_deck, conditions=[lambda effect, message: message.into_area.flags.is_discards]).NoOutOfPlayLimit())
        for face in initiator.set_aside_deck.Get():
            register_effect(face)
        this.effect.Registers(AbilityFactory.AfterCardsMoved(AbilityType.Temp0,
            initiator.set_aside_deck.Get(),
            lambda effect, message: flip_top_card(initiator, effect),
            by_shuffle=False))
        flip_top_card(initiator, effect)
    return [AbilityFactory.BeginGameWithSetAside([*SENSE_DECK_IDS], with_sense_deck)]
```

#### `60007` * Elektra (Elektra Natchios)

```json
{
 "card_id": "60007",
 "type": "Ally",
 "name": "* Elektra",
 "subtitle": "Elektra Natchios",
 "desc": {
  "Cost": "3",
  "HP": "3",
  "ATK": "2*",
  "THW": "1*",
  "RES": "G",
  "Class": "Hero"
 },
 "traits": [
  "DEFENDER",
  "MARTIAL ARTIST"
 ],
 "set_name": "Daredevil",
 "text": "[star] <b>Forced Interrupt (Hero)</b>: When Elektra would take consequential damage, Daredevil takes that damage instead."
}
```

Script `src/cards/pack/fne/daredevil/60007.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def check_this(effect: 'Effect', message: 'Message.WhenAllyWouldTakeConsequentialDamage') -> bool:
        return (effect.this == message.trigger)
    def check_hero_form(effect: 'Effect', message: 'Message.WhenAllyWouldTakeConsequentialDamage') -> bool:
        this = effect.this.CastTo(Ally)
        return this.GetControlByPlayer().IsInHeroForm()
    def elektra(effect: 'Effect', message: 'Message.WhenAllyWouldTakeConsequentialDamage') -> None:
        this = effect.this.CastTo(Ally)
        message.SetBeInstead(effect)
        identity = this.GetControlByPlayer().GetIdentity()
        identity.CastTo(Unit2).TakeDamage(this, message.will_take_damage, effect)
    return [Ability(AbilityType.ForcedInterrupt, Message.WhenAllyWouldTakeConsequentialDamage, [check_this, check_hero_form], elektra, is_local=True)]
```

#### `60008` Cross-Examination

```json
{
 "card_id": "60008",
 "type": "Event",
 "name": "Cross-Examination",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "RES": "R",
  "Class": "Hero"
 },
 "traits": [
  "ATTACK"
 ],
 "set_name": "Daredevil",
 "text": "<b>Hero Action</b> <i>(attack)</i>: Deal 3 damage to an enemy. For each upgrade attached to that enemy, you may deal 1 additional damage to it."
}
```

Script `src/cards/pack/fne/daredevil/60008.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def cross_examination(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        for target in effect.targets:
            damage = 3 + len(target.GetAttachedUpgrades())
            this.DealDamage([target], damage, effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, cross_examination).SetPlay().SetLabel('attack').SetTarget(Enemy)]
```

#### `60009` Deposition

```json
{
 "card_id": "60009",
 "type": "Event",
 "name": "Deposition",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "RES": "B",
  "Class": "Hero"
 },
 "traits": [
  "THWART"
 ],
 "set_name": "Daredevil",
 "text": "<b>Alter-Ego Action</b> <i>(thwart)</i>: You may choose any upgrade from the [[Sense]] deck and play it, ignoring its resource cost. <i>(Do not shuffle.)</i> Remove 2 threat from a scheme."
}
```

Script `src/cards/pack/fne/daredevil/60009.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def deposition(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()
        PlaySenseUpgradeFree(initiator, effect, optional=True)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, deposition).SetPlay().SetLabel('thwart').SetTarget(Scheme2, has_threat=True)]
```

#### `60010` Living Lie Detector

```json
{
 "card_id": "60010",
 "type": "Event",
 "name": "Living Lie Detector",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "RES": "Y",
  "Class": "Hero"
 },
 "traits": [
  "THWART"
 ],
 "set_name": "Daredevil",
 "text": "<b>Action</b> <i>(thwart)</i>: Remove 2 threat from a scheme. For each upgrade attached to that scheme, you may remove 1 additional threat from it."
}
```

Script `src/cards/pack/fne/daredevil/60010.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def living_lie_detector(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        for target in effect.targets:
            amount = 2 + len(target.GetAttachedUpgrades())
            this.RemoveThreatFromSchemes([target], amount, effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, living_lie_detector).SetPlay().SetLabel('thwart').SetTarget(Scheme2, has_threat=True)]
```

#### `60011` Raising Hell

```json
{
 "card_id": "60011",
 "type": "Event",
 "name": "Raising Hell",
 "subtitle": "",
 "desc": {
  "Cost": "2",
  "RES": "R",
  "Class": "Hero"
 },
 "traits": [
  "ATTACK"
 ],
 "set_name": "Daredevil",
 "text": "<b>Hero Action</b> <i>(attack)</i>: Deal 2 damage to each enemy for each upgrade attached to that enemy (3 damage instead if Daredevil has the [[Aerial]] trait)."
}
```

Script `src/cards/pack/fne/daredevil/60011.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def raising_hell(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()
        per_upgrade = 3 if initiator.GetIdentity().HasTrait('AERIAL') else 2
        for enemy in Worlds.FindCardsOnField(effect, card_type=Enemy):
            n = len(enemy.GetAttachedUpgrades())
            if n > 0:
                this.DealDamage([enemy], per_upgrade * n, effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, raising_hell).SetPlay().SetLabel('attack')]
```

#### `60012` * Focus the Senses

```json
{
 "card_id": "60012",
 "type": "PlayerSideScheme",
 "name": "* Focus the Senses",
 "subtitle": "",
 "desc": {
  "Cost": "0",
  "StartingThreat": "4",
  "RES": "B",
  "Class": "Hero"
 },
 "traits": [],
 "set_name": "Daredevil",
 "text": "Threat cannot be removed from this scheme except by Daredevil or Matt Murdock.\n<b>When Defeated</b>: You may move any number of [[Sense]] upgrades in play to other cards they can attach to. Choose any number of upgrades from the [[Sense]] deck and put them into play. <i>(Do not shuffle.)</i>"
}
```

Script `src/cards/pack/fne/daredevil/60012.py` :

```python
from . import *
SENSE_ATTACH_TARGETS = {
    '60002': (Enemy, Scheme2), '60003': (Enemy, Scheme2),
    '60004': (Enemy,), '60005': (Enemy,), '60006': (Scheme2,)}
def MoveSenseUpgrades(player: 'Player', effect: 'Effect') -> None:
    mine = [u for u in Worlds.FindCardsOnField(effect, card_type=Upgrade)
            if u.paper.card_id in SENSE_ATTACH_TARGETS and u.GetControlByPlayer() == player]
    if not mine:
        return
    def choose_upgrades(chosen: Sequence['CardFace']):
        for face in list(chosen):
            upgrade = face.CastTo(Upgrade)
            dests = [t for kind in SENSE_ATTACH_TARGETS[upgrade.paper.card_id]
                     for t in Worlds.FindCardsOnField(effect, card_type=kind)
                     if t != upgrade.bind_face and t != effect.this]
            if not dests:
                continue
            def move(to: Sequence['CardFace'], upgrade=upgrade):
                if to:
                    upgrade.AttachTo2(to[0], effect)
            player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Move ' + upgrade.paper.name + ' to another card', move).SetTarget(dests, range=(0, 1), not_move=True, not_shuffle=True))
    player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Move any number of Sense upgrades in play to other cards they can attach to', choose_upgrades).SetTarget(mine, range=(0, len(mine)), not_move=True, not_shuffle=True))
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)
        player = message.GetDefeatingPlayer()
        if not player:
            player = effect.GetInitiator()
        MoveSenseUpgrades(player, effect)
        PlaySenseUpgradeFree(player, effect, any_number=True)
    def check_remover(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        remover = message.by_effect.GetInitiator() if message.by_effect else None
        if remover and Player.IsType(remover):
            for face in remover.GetAllIdentityFace():
                if (face.paper.name in ('Daredevil', 'Matt Murdock')):
                    return False
        return True
    def cannot_remove(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
        message.SetBeInstead(effect)
    return [AbilityFactory.CanPlayThisSchemeCard(),
            AbilityFactory.WhenSchemeWouldRemoveThreat(AbilityType.NonKeyword, 'This', cannot_remove, conditions=[check_remover]),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated, has_defeating_player=True)]
```

#### `60013` * Foggy Nelson

```json
{
 "card_id": "60013",
 "type": "Support",
 "name": "* Foggy Nelson",
 "subtitle": "",
 "desc": {
  "Cost": "2",
  "RES": "B",
  "Class": "Hero"
 },
 "traits": [
  "ATTORNEY",
  "PERSONA"
 ],
 "set_name": "Daredevil",
 "text": "<b>Alter-Ego Action</b>: Exhaust Foggy Nelson → remove 2 threat from a scheme."
}
```

Script `src/cards/pack/fne/daredevil/60013.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def foggy_nelson(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)
    return [AbilityFactory.CanPlayThisSupportCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, foggy_nelson).SetCostFunc(CostFunc.Exhaust('This')).SetTarget(Scheme2, has_threat=True)]
```

#### `60014` * Karen Page

```json
{
 "card_id": "60014",
 "type": "Support",
 "name": "* Karen Page",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "RES": "Y",
  "Class": "Hero"
 },
 "traits": [
  "PERSONA"
 ],
 "set_name": "Daredevil",
 "text": "<b>Action</b>: Exhaust Karen Page → shuffle 1 Daredevil card from your discard pile into your deck. If you are in alter-ego form, draw 1 card."
}
```

Script `src/cards/pack/fne/daredevil/60014.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def karen_page(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        initiator = effect.GetInitiator()
        Faces.ShuffleAllTo(effect.targets, initiator.player_deck, effect)
        if initiator.IsAlterEgo():
            initiator.DrawUp(1, effect)
    return [AbilityFactory.CanPlayThisSupportCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, karen_page).SetCostFunc(CostFunc.Exhaust('This')).SetTarget(finder=CardFinder(set_name='Daredevil'), from_where=['YourDiscardPile'], range=(1, 1))]
```

#### `60015` * Nelson and Murdock

```json
{
 "card_id": "60015",
 "type": "Support",
 "name": "* Nelson and Murdock",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "RES": "Y",
  "Class": "Hero"
 },
 "traits": [
  "LOCATION"
 ],
 "set_name": "Daredevil",
 "text": "<b>Response</b>: After an [[Attorney]] character or support defeats a side scheme, confuse an enemy."
}
```

Script `src/cards/pack/fne/daredevil/60015.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def nelson_and_murdock(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        def action(targets: Sequence['CardFace']):
            Faces.GiveStatus(targets, 'Confused', effect)
        player = effect.GetInitiator()
        player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Confuse an enemy', action).SetTarget(Enemy, canbe_confused=True))
    def check_attorney(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> bool:
        src = message.by_effect.this if message.by_effect else None
        if src and src.HasTrait('ATTORNEY'):
            return True
        player = message.GetDefeatingPlayer()
        if not player:
            return False
        identity = player.GetIdentity()
        return bool(identity and identity.HasTrait('ATTORNEY'))
    return [AbilityFactory.CanPlayThisSupportCard(),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.Response, SchemeSide2, nelson_and_murdock, has_defeating_player=True, conditions=[check_attorney])]
```

#### `60016` * Sister Maggie

```json
{
 "card_id": "60016",
 "type": "Support",
 "name": "* Sister Maggie",
 "subtitle": "",
 "desc": {
  "Cost": "2",
  "RES": "B",
  "Class": "Hero"
 },
 "traits": [
  "PERSONA"
 ],
 "set_name": "Daredevil",
 "text": "Matt Murdock gets +3 REC.\n<b>Response</b>: After you recover, discard a status card from your identity."
}
```

Script `src/cards/pack/fne/daredevil/60016.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def sister_maggie(effect: 'Effect', message: 'Message.AfterUnitRecovery') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()
        def action(targets: Sequence['CardFace']):
            Faces.DiscardAll(targets, effect)
        status_cards = list(identity.components.status.GetDeck().Get(True))
        if status_cards:
            initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard a status card from your identity', action).SetTarget(status_cards))
    return [AbilityFactory.CanPlayThisSupportCard(),
            *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(name='Matt Murdock'), recover=3),
            AbilityFactory.AfterUnitRecovery(AbilityType.Response, 'YourIdentity', sister_maggie)]
```

#### `60017` * Daredevil's Billy Club

```json
{
 "card_id": "60017",
 "type": "Upgrade",
 "name": "* Daredevil's Billy Club",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "RES": "R",
  "Restricted": "1",
  "Class": "Hero"
 },
 "traits": [
  "ITEM",
  "WEAPON"
 ],
 "set_name": "Daredevil",
 "text": "Restricted. Daredevil gets +1 ATK.\n<b>Hero Action</b>: Return this card to your hand <i>(from play)</i> → choose:\n• Deal 1 damage to an enemy.\n• Daredevil gains the [[Aerial]] trait until the end of the round."
}
```

Script `src/cards/pack/fne/daredevil/60017.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def billy_club(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        Faces.AddToHand([this], initiator, effect)
        def deal_damage(targets: Sequence['CardFace']):
            this.DealDamage(targets, 1, effect)
        def gain_aerial(targets: Sequence['CardFace']):
            identity = initiator.GetIdentity()
            # CORRECTIF : `GainTraitsUntilEndOfRound` n'existe pas. Le moteur
            # expose `GainUntilRoundEnd(by_effect, trait=...)`. L'option
            # « gagne AERIAL » plantait donc a chaque choix, silencieusement.
            identity.GainUntilRoundEnd(effect, trait=['AERIAL'])
        initiator.ChooseAbilities(effect,
            AbilityFactory.ForChoiceAbility('Deal 1 damage to an enemy', deal_damage).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility('Daredevil gains the AERIAL trait until the end of the round', gain_aerial))
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            *AbilityFactory.GiveKeywordToAttached('You', attack=1),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, billy_club)]
```

#### `60018` * The Man Without Fear

```json
{
 "card_id": "60018",
 "type": "Upgrade",
 "name": "* The Man Without Fear",
 "subtitle": "",
 "desc": {
  "Cost": "2",
  "RES": "R",
  "Class": "Hero"
 },
 "traits": [
  "TITLE"
 ],
 "set_name": "Daredevil",
 "text": "<b>Hero Action</b>: Exhaust this card and deal 1 damage to Daredevil → choose:\n• Choose any upgrade from the [[Sense]] deck and play it, ignoring its resource cost. <i>(Do not shuffle.)</i>\n• Ready Daredevil."
}
```

Script `src/cards/pack/fne/daredevil/60018.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def man_without_fear(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()
        identity.CastTo(Unit2).TakeDamage(this, 1, effect)
        def play_sense(targets: Sequence['CardFace']):
            PlaySenseUpgradeFree(initiator, effect)
        def ready_dd(targets: Sequence['CardFace']):
            Faces.ReadyAll([initiator.GetIdentity()], effect)
        initiator.ChooseAbilities(effect,
            AbilityFactory.ForChoiceAbility('Choose any upgrade from the Sense deck and play it, ignoring its resource cost', play_sense),
            AbilityFactory.ForChoiceAbility('Ready Daredevil', ready_dd))
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, man_without_fear).SetCostFunc(CostFunc.Exhaust('This'))]
```

#### `60032` Sensory Overload

```json
{
 "card_id": "60032",
 "type": "Obligation",
 "name": "Sensory Overload",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "GiveTo": "Matt Murdock"
 },
 "traits": [],
 "set_name": "Daredevil",
 "text": "<b><i>Give to the Matt Murdock player.</i></b>\n<b>Forced Response</b>: After a [[Sense]] upgrade enters play, take 1 damage.\n<b>Alter-Ego Response</b>: After you recover, discard this card."
}
```

Script `src/cards/pack/fne/daredevil/60032.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def sensory_overload(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        this = effect.this.CastTo(Obligation)
        player = this.GetGaveToPlayer()
        player.GetIdentity().CastTo(Unit2).TakeDamage(this, 1, effect)
    def after_recover(effect: 'Effect', message: 'Message.AfterUnitRecovery') -> None:
        this = effect.this.CastTo(Obligation)
        Faces.DiscardAll([this], effect)
    def check_sense(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> bool:
        return message.trigger.HasTrait('SENSE')
    return [AbilityFactory.WhenCardEnterPlay(AbilityType.ForcedResponse, Upgrade, sensory_overload, conditions=[check_sense]),
            AbilityFactory.AfterUnitRecovery(AbilityType.Response, 'YourIdentity', after_recover)]
```

### Set : Sense Deck (5 cartes)

#### `60002` Acute Tactility

```json
{
 "card_id": "60002",
 "type": "Upgrade",
 "name": "Acute Tactility",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "Class": "Hero",
  "RES": "R"
 },
 "traits": [
  "SENSE",
  "SUPERPOWER"
 ],
 "set_name": "Sense Deck",
 "text": "Attach to an enemy or scheme.\n<b>Interrupt</b>: When you defeat attached enemy or remove the last threat from attached scheme, discard this card → ready your identity."
}
```

Script `src/cards/pack/fne/sense_deck/60002.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def defeat_enemy(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        SenseDiscard(this, effect)
        Faces.ReadyAll([initiator.GetIdentity()], effect)
    def defeat_scheme(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        SenseDiscard(this, effect)
        Faces.ReadyAll([initiator.GetIdentity()], effect)
    def check_enemy_you(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> bool:
        this = effect.this
        if (message.trigger != this.bind_face):
            return False
        killer = message.killer
        return bool(killer) and (killer.GetControlByPlayer() == this.GetControlByPlayer())
    def check_scheme_you(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> bool:
        this = effect.this
        if (message.trigger != this.bind_face):
            return False
        return (message.GetDefeatingPlayer() == this.GetControlByPlayer())
    return [AbilityFactory.CanPlayThisUpgradeCard(ENEMY_OR_SCHEME),
            AbilityFactory.WhenUnitBeDefeated(AbilityType.Interrupt, None, defeat_enemy, conditions=[check_enemy_you]),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.Interrupt, None, defeat_scheme, has_defeating_player=True, conditions=[check_scheme_you])]
```

#### `60003` Enhanced Olfaction

```json
{
 "card_id": "60003",
 "type": "Upgrade",
 "name": "Enhanced Olfaction",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "Class": "Hero",
  "RES": "Y"
 },
 "traits": [
  "SENSE",
  "SUPERPOWER"
 ],
 "set_name": "Sense Deck",
 "text": "Attach to an enemy or scheme.\n<b>Interrupt</b>: When you defeat attached enemy or remove the last threat from attached scheme, discard this card → reduce the cost of the next card you play this phase by 2."
}
```

Script `src/cards/pack/fne/sense_deck/60003.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def give_discount(effect: 'Effect') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        identity = player.GetIdentity()
        Unused(identity)
        # Rapport n°79 : une CanGenerateResources temporaire sur l'identite plantait (IndexError, pas de DoGenerateResources).
        Worlds.UpdateNextCardPlayCost(player, -2, effect, in_this="Phase")
    def defeat_enemy(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        SenseDiscard(this, effect)
        give_discount(effect)
    def defeat_scheme(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        SenseDiscard(this, effect)
        give_discount(effect)
    def check_enemy_you(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> bool:
        this = effect.this
        if (message.trigger != this.bind_face):
            return False
        killer = message.killer
        return bool(killer) and (killer.GetControlByPlayer() == this.GetControlByPlayer())
    def check_scheme_you(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> bool:
        this = effect.this
        if (message.trigger != this.bind_face):
            return False
        return (message.GetDefeatingPlayer() == this.GetControlByPlayer())
    return [AbilityFactory.CanPlayThisUpgradeCard(ENEMY_OR_SCHEME),
            AbilityFactory.WhenUnitBeDefeated(AbilityType.Interrupt, None, defeat_enemy, conditions=[check_enemy_you]),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.Interrupt, None, defeat_scheme, has_defeating_player=True, conditions=[check_scheme_you])]
```

#### `60004` Heightened Hearing

```json
{
 "card_id": "60004",
 "type": "Upgrade",
 "name": "Heightened Hearing",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "Class": "Hero",
  "RES": "B"
 },
 "traits": [
  "SENSE",
  "SUPERPOWER"
 ],
 "set_name": "Sense Deck",
 "text": "Attach to an enemy.\n<b>Hero Interrupt</b> <i>(defense)</i>: When attached enemy attacks, discard this card → that enemy gets -3 ATK for that attack. <i>(You become the target of that attack.)</i>"
}
```

Script `src/cards/pack/fne/sense_deck/60004.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def reduce_attack(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        attacker = message.trigger
        SenseDiscard(this, effect)
        attacker.CastTo(Unit2).GainForThisActive(effect, message, attack=-3)
        player = this.GetControlByPlayer()
        identity = player.GetIdentity() if player else None
        if identity:
            def redirect(e2: 'Effect', m2: 'Message.WhenUnitWouldTakeDamage') -> None:
                if (message.GetDefender() == None) and (m2.trigger != identity):
                    m2.ChangeDealtToTarget(identity, e2)
            this.effect.RegisterTemp(AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.Temp0, None, redirect, is_from_attack=message), unregister_after_exec=True, until_event_end=message)
    return [AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Enemy)),
            AbilityFactory.WhenUnitWouldAttack(AbilityType.HeroInterrupt, None, reduce_attack, conditions=[lambda effect, message: (message.trigger == effect.this.bind_face)])]
```

#### `60005` Radar Sense

```json
{
 "card_id": "60005",
 "type": "Upgrade",
 "name": "Radar Sense",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "Class": "Hero",
  "RES": "Y"
 },
 "traits": [
  "SENSE",
  "SUPERPOWER"
 ],
 "set_name": "Sense Deck",
 "text": "Attach to an enemy.\n<b>Response</b> <i>(attack)</i>: After you attack attached enemy, discard this card → deal 3 damage to that enemy."
}
```

Script `src/cards/pack/fne/sense_deck/60005.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def radar_sense(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Upgrade)
        target = effect.this.bind_face
        SenseDiscard(this, effect)
        if target:
            this.DealDamage([target], 3, effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Enemy)),
            AbilityFactory.AfterUnitAttackUnit(AbilityType.Response, 'YourIdentity', None, radar_sense, conditions=[lambda effect, message: (effect.this.bind_face == message.attacked)])]
```

#### `60006` Superior Taste

```json
{
 "card_id": "60006",
 "type": "Upgrade",
 "name": "Superior Taste",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "Class": "Hero",
  "RES": "B"
 },
 "traits": [
  "SENSE",
  "SUPERPOWER"
 ],
 "set_name": "Sense Deck",
 "text": "Attach to a scheme.\n<b>Response</b> <i>(thwart)</i>: After you thwart attached scheme, discard this card → remove 2 threat from that scheme."
}
```

Script `src/cards/pack/fne/sense_deck/60006.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def superior_taste(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> None:
        this = effect.this.CastTo(Upgrade)
        target = effect.this.bind_face
        SenseDiscard(this, effect)
        if target:
            this.RemoveThreatFromSchemes([target], 2, effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Scheme2)),
            AbilityFactory.AfterUnitThwartScheme(AbilityType.Response, 'YourIdentity', None, superior_taste, conditions=[lambda effect, message: (effect.this.bind_face == message.scheme)])]
```

### Set : (sans set) (26 cartes)

#### `60019` * Blindspot (Sam Chung)

```json
{
 "card_id": "60019",
 "type": "Ally",
 "name": "* Blindspot",
 "subtitle": "Sam Chung",
 "desc": {
  "Cost": "4",
  "HP": "3",
  "ATK": "2*",
  "THW": "2*",
  "RES": "Y",
  "Class": "Justice"
 },
 "traits": [
  "GENIUS",
  "MARTIAL ARTIST"
 ],
 "set_name": "",
 "text": "[star] <b>Response</b>: After Blindspot thwarts, confuse an enemy with an upgrade attached."
}
```

Script `src/cards/pack/fne/60019.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def blindspot(effect: 'Effect', message: 'Message.AfterUnitThwartEnd') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        Faces.GiveStatus(effect.targets, 'Confused', effect)
    return [AbilityFactory.AfterUnitThwartEnd(AbilityType.Response, 'This', blindspot).SetTarget(Enemy, with_attach=Upgrade, canbe_confused=True)]
```

#### `60020` * Cloak (Tyrone Johnson)

```json
{
 "card_id": "60020",
 "type": "Ally",
 "name": "* Cloak",
 "subtitle": "Tyrone Johnson",
 "desc": {
  "Cost": "3",
  "HP": "2",
  "ATK": "1",
  "THW": "2",
  "RES": "B",
  "Class": "Justice",
  "Acceleration": "1"
 },
 "traits": [
  "DEFENDER"
 ],
 "set_name": "",
 "text": "<b>Action</b>: Exhaust Cloak and spend [energy] [energy] resources → find Dagger and put her into play."
}
```

Script `src/cards/pack/fne/60020.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def cloak(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        initiator = effect.GetInitiator()
        face = Search.PlayerCard(effect, initiator, include_player_deck=True, include_discard_pile=True, include_player_hand_cards=True, name='Dagger')
        if face:
            face.CastTo(Ally).PutIntoPlay(initiator, effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, cloak).SetCostFunc(CostFunc.Exhaust('This')).SetCostFunc(CostFunc.Spend(Cost('YY')))]
```

#### `60021` * Dagger (Tandy Bowen)

```json
{
 "card_id": "60021",
 "type": "Ally",
 "name": "* Dagger",
 "subtitle": "Tandy Bowen",
 "desc": {
  "Cost": "3",
  "HP": "3",
  "ATK": "2**",
  "THW": "1**",
  "RES": "Y",
  "Class": "Justice"
 },
 "traits": [
  "DEFENDER"
 ],
 "set_name": "",
 "text": "Cloak loses each [acceleration] icon.\n[star] If Cloak is in play, Dagger takes -1 consequential damage after she uses a basic power."
}
```

Script `src/cards/pack/fne/60021.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def cloak_in_play(effect: 'Effect') -> int:
        face = Worlds.FindCardOnField(effect, CardFinder(name='Cloak', card_type=Ally))
        return (-1 if face else 0)
    return [*AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(name='Cloak', card_type=Ally), acceleration_icon=-1),
            AbilityFactory.WhenAllyWouldTakeConsequentialDamage('This', update_damage=cloak_in_play)]
```

#### `60022` * Ghost Rider (Johnny Blaze)

```json
{
 "card_id": "60022",
 "type": "Ally",
 "name": "* Ghost Rider",
 "subtitle": "Johnny Blaze",
 "desc": {
  "Cost": "3",
  "HP": "3",
  "ATK": "2*",
  "THW": "1*",
  "RES": "Y",
  "Class": "Justice"
 },
 "traits": [
  "MIDNIGHT SUN"
 ],
 "set_name": "",
 "text": "[star] <b>Interrupt</b>: When Ghost Rider attacks an enemy, spend a [energy] resource ([energy] [energy] resources instead if that enemy is the villain) → confuse that enemy."
}
```

Script `src/cards/pack/fne/60022.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def ghost_rider(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        Faces.GiveStatus(list(message.targets), 'Confused', effect)
    def check_villain(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        return any(Villain.IsType(t) for t in message.targets)
    def check_not_villain(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        return not any(Villain.IsType(t) for t in message.targets)
    return [AbilityFactory.WhenUnitMakeAttack(AbilityType.Interrupt, 'This', ghost_rider, conditions=[check_not_villain]).SetCost(Cost('Y')),
            AbilityFactory.WhenUnitMakeAttack(AbilityType.Interrupt, 'This', ghost_rider, conditions=[check_villain]).SetCost(Cost('YY'))]
```

#### `60023` Know Your Enemy

```json
{
 "card_id": "60023",
 "type": "Event",
 "name": "Know Your Enemy",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "RES": "B",
  "Class": "Justice"
 },
 "traits": [
  "THWART"
 ],
 "set_name": "",
 "text": "[star] Discount 1 ([[Martial Artist]]).\n<b>Hero Action</b> <i>(thwart)</i>: Remove 1 threat from a scheme. Remove 1 threat from a scheme."
}
```

Script `src/cards/pack/fne/60023.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def know_your_enemy(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()
        for _ in range(2):
            schemes = [s for s in Worlds.FindCardsOnField(effect, card_type=Scheme2) if (s.threat > 0)]
            if not schemes:
                return
            def action(targets: Sequence['CardFace']):
                this.RemoveThreatFromSchemes(list(targets), 1, effect)
            initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Remove 1 threat from a scheme', action).SetTarget(schemes, range=(1, 1), not_move=True))
    return [DiscountAbility(1, ['MARTIAL ARTIST']),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, know_your_enemy).SetPlay().SetLabel('thwart')]
```

#### `60024` * De-escalation

```json
{
 "card_id": "60024",
 "type": "PlayerSideScheme",
 "name": "* De-escalation",
 "subtitle": "",
 "desc": {
  "Cost": "0",
  "StartingThreat": "4",
  "Victory": "0",
  "RES": "R",
  "Class": "Justice"
 },
 "traits": [],
 "set_name": "",
 "text": "Victory 0.\n<b>When Defeated</b>: Remove an acceleration token from play."
}
```

Script `src/cards/pack/fne/60024.py` :

```python
from . import *

# * De-escalation
# Victory 0.
# When Defeated: Remove an acceleration token from play.
#
# CORRECTIF 4/8/2026 : `Worlds.RemoveAccelerationToken` n'existe pas, la
# capacite plantait a chaque fois que la manigance etait vaincue. On passe par
# les faces qui PORTENT un jeton (`GetAccelerationTokenFaces`) et par le
# retrait de jeton standard.

def GetAbilities() -> Sequence['Ability']:

    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)

        porteurs = [x for x in Worlds.GetAccelerationTokenFaces(effect)
                    if x.acceleration_token > 0]
        if porteurs:
            Faces.RemoveTokensOn(porteurs[:1], 1, 'acceleration_token', effect)

    return [
        AbilityFactory.CanPlayThisSchemeCard(),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated),
    ]
```

#### `60025` Chance Encounter

```json
{
 "card_id": "60025",
 "type": "Upgrade",
 "name": "Chance Encounter",
 "subtitle": "",
 "desc": {
  "Cost": "0",
  "RES": "Y",
  "Class": "Justice",
  "MaxPerUnit": "1"
 },
 "traits": [
  "CONDITION"
 ],
 "set_name": "",
 "text": "Attach to a side scheme. Max 1 per scheme.\n<b>Interrupt:</b> When attached side scheme is defeated, search your deck and discard pile for an ally and add it to your hand. Shuffle your deck."
}
```

Script `src/cards/pack/fne/60025.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def chance_encounter(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        initiator = effect.GetInitiator()
        face = Search.PlayerCard(effect, initiator, include_player_deck=True, include_discard_pile=True, card_type=Ally)
        if face:
            Faces.AddToHand([face], initiator, effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=SchemeSide2)),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.Interrupt, None, chance_encounter, conditions=[lambda effect, message: (message.trigger == effect.this.bind_face)])]
```

#### `60026` Legal Trouble

```json
{
 "card_id": "60026",
 "type": "Upgrade",
 "name": "Legal Trouble",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "RES": "B",
  "Class": "Justice",
  "MaxPerUnit": "1"
 },
 "traits": [
  "CONDITION"
 ],
 "set_name": "",
 "text": "[star] Discount 1 ([[Attorney]] or [[Police]]).\nAttach to a minion. Max 1 per minion.\nAttached minion gets -2 SCH."
}
```

Script `src/cards/pack/fne/60026.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    return [DiscountAbility(1, ['ATTORNEY', 'POLICE']),
            AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Minion)),
            *AbilityFactory.GiveKeywordToAttached(Minion, scheme=-2)]
```

#### `60027` Move in Shadow

```json
{
 "card_id": "60027",
 "type": "Upgrade",
 "name": "Move in Shadow",
 "subtitle": "",
 "desc": {
  "Cost": "2",
  "RES": "Y",
  "MaxPerUnit": "1",
  "Class": "Justice",
  "Temporary": "1"
 },
 "traits": [
  "SKILL"
 ],
 "set_name": "",
 "text": "[star] Discount 1 ([[Martial Artist]] or [[Spy]]).\nTemporary. Max 1 per player.\n<b>Response</b> <i>(thwart)</i>: After you play a card <i>(including this one)</i>, remove 1 threat from a scheme."
}
```

Script `src/cards/pack/fne/60027.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def move_in_shadow(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        def action(targets: Sequence['CardFace']):
            this.RemoveThreatFromSchemes(targets, 1, effect)
        initiator = effect.GetInitiator()
        initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Remove 1 threat from a scheme', action).SetTarget(Scheme2, has_threat=True))
    return [DiscountAbility(1, ['MARTIAL ARTIST', 'SPY']),
            AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.AfterPlayerPlayedCard(AbilityType.Response, 'You', None, move_in_shadow)]
```

#### `60028` Stealth Training

```json
{
 "card_id": "60028",
 "type": "Upgrade",
 "name": "Stealth Training",
 "subtitle": "",
 "desc": {
  "Cost": "2",
  "RES": "R",
  "MaxPerUnit": "1",
  "Class": "Justice"
 },
 "traits": [
  "SKILL"
 ],
 "set_name": "",
 "text": "Play under any player's control. Max 1 per player.\n<b>Response</b>: After you thwart and exactly defeat a side scheme, exhaust Stealth Training → stun an enemy."
}
```

Script `src/cards/pack/fne/60028.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def stealth_training(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        Faces.GiveStatus(effect.targets, 'Stunned', effect)
    def check_you(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> bool:
        this = effect.this
        return (message.GetDefeatingPlayer() == this.GetControlByPlayer())
    return [AbilityFactory.CanPlayThisUpgradeCard('Players'),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.Response, EncounterSideScheme, stealth_training, has_defeating_player=True, conditions=[check_you]).SetCostFunc(CostFunc.Exhaust('This')).SetTarget(Enemy, canbe_stunned=True)]
```

#### `60029` * Stick

```json
{
 "card_id": "60029",
 "type": "Support",
 "name": "* Stick",
 "subtitle": "",
 "desc": {
  "Cost": "2",
  "RES": "R",
  "Class": "Basic"
 },
 "traits": [
  "MARTIAL ARTIST",
  "PERSONA"
 ],
 "set_name": "",
 "text": "<b>Interrupt</b>: When a friendly [[Martial Artist]] character uses a basic power, choose:\n• Exhaust Stick → that character gets +1 to that basic power for this use.\n• That character gets -1 to that basic power for this use. Ready Stick."
}
```

Script `src/cards/pack/fne/60029.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def plus_one(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        message.GainValue(1, effect)
    def minus_one(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Support)
        message.GainValue(-1, effect)
        Faces.ReadyAll([this], effect)
    finder = CardFinder2('MARTIAL ARTIST', Friend)
    return [AbilityFactory.CanPlayThisSupportCard(),
            AbilityFactory.WhenUnitUseBasicPower(AbilityType.Interrupt, finder, plus_one).SetTarget('Trigger').SetCostFunc(CostFunc.Exhaust('This')),
            AbilityFactory.WhenUnitUseBasicPower(AbilityType.Interrupt, finder, minus_one).SetTarget('Trigger')]
```

#### `60030` Contingency Planning

```json
{
 "card_id": "60030",
 "type": "Upgrade",
 "name": "Contingency Planning",
 "subtitle": "",
 "desc": {
  "Cost": "0",
  "RES": "R",
  "MaxPerUnit": "1",
  "Class": "Basic"
 },
 "traits": [
  "SKILL"
 ],
 "set_name": "",
 "text": "Max 1 per player.\nYou may play the upgrade tucked here as if it were in your hand.\n<b>Action</b>: Choose 1 upgrade in your hand that can attach to a minion or side scheme. Tuck that upgrade under here (to a maximum of 1)."
}
```

Script `src/cards/pack/fne/60030.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def contingency_planning(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        for face in effect.targets:
            this.TuckCardUnderHere(face, effect)
    def check_no_tucked(effect: 'Effect') -> bool:
        this = effect.this
        return (len(this.GetPlacedCardArea().Get()) == 0)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            *AbilityFactory.AttachedCardCanPlayLikeInHand(CardFinder(card_type=Upgrade)),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, contingency_planning, conditions=[lambda effect, message: check_no_tucked(effect)]).SetTarget(finder=CardFinder(card_type=Upgrade), from_where=['YourHandCards'], range=(1, 1))]
```

#### `60031` Dance with the Devil

```json
{
 "card_id": "60031",
 "type": "Upgrade",
 "name": "Dance with the Devil",
 "subtitle": "",
 "desc": {
  "Cost": "0",
  "RES": "G",
  "Class": "Basic",
  "MaxPerDeck": "1"
 },
 "traits": [
  "DANCE"
 ],
 "set_name": "",
 "text": "Team-Up (Daredevil and Elektra). Max 1 per deck.\nAttach to an enemy.\n<b>Hero Action</b> <i>(attack)</i>: Discard this card → deal 3 damage to attached enemy."
}
```

Script `src/cards/pack/fne/60031.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def dance_with_the_devil(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        target = this.bind_face
        Faces.DiscardAll([this], effect)
        if target:
            this.DealDamage([target], 3, effect)
    def check_team_up(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        units = Worlds.GetOnFieldFriendlyCharacters(effect.this.card.game_area)
        for name in ('Daredevil', 'Elektra'):
            if not any((u.IsName(name) or u.IsSubName(name)) for u in units):
                return False
        return True
    return [AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Enemy), conditions=[check_team_up]),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, dance_with_the_devil).SetLabel('attack')]
```

#### `60038` Innate Reflexes

```json
{
 "card_id": "60038",
 "type": "Upgrade",
 "name": "Innate Reflexes",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "Class": "Protection"
 },
 "traits": [
  "CONDITION"
 ],
 "set_name": "",
 "text": "Starting. <i>(You may add this card to your hand before drawing your starting hand.)</i>\nYour hero gets +1 DEF."
}
```

Script `src/cards/pack/fne/60038.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def starting(effect: 'Effect', message: 'Message.WhenGameBeginSetup') -> None:
        this = effect.this.CastTo(Upgrade)
        if not this.card.area.flags.is_player_deck:
            return
        player = this.GetControlByOrOwner()
        Faces.AddToHand([this], player, effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            *AbilityFactory.GiveKeywordToAttached(Hero, defense=1),
            AbilityFactory.WhenGameBeginSetup(starting).NoOutOfPlayLimit()]
```

#### `60048` Army of One

```json
{
 "card_id": "60048",
 "type": "Event",
 "name": "Army of One",
 "subtitle": "",
 "desc": {
  "Cost": "1*",
  "RES": "Y",
  "Class": "Protection"
 },
 "traits": [],
 "set_name": "",
 "text": "[star] Increase the cost to play this card by 1 for each ally you control.\n<b>Hero Action</b>: Ready your hero."
}
```

Script `src/cards/pack/fne/60048.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def army_of_one(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        Faces.ReadyAll(effect.targets, effect)
    def increase_cost(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> None:
        player = effect.this.GetControlByOrOwner()
        value = len(player.allies.Get())
        if (value > 0):
            message.UpdateCost(value, effect)
    def check_this_cost(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        if (message.check_effect.this != effect.this):
            return False
        return message.check_effect.ability.is_play
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, army_of_one).SetPlay().SetLabel().SetTarget('YourHero'),
            AbilityFactory.WhenCalculateEffectCost(AbilityType.NonKeywordStar, increase_cost, conditions=[check_this_cost]).CanWorkOnlyInHand()]
```

#### `60049` Get Their Attention

```json
{
 "card_id": "60049",
 "type": "Event",
 "name": "Get Their Attention",
 "subtitle": "",
 "desc": {
  "Cost": "2",
  "RES": "B",
  "Class": "Protection"
 },
 "traits": [
  "DEFENSE",
  "THWART"
 ],
 "set_name": "",
 "text": "<b>Hero Interrupt</b> <i>(defense/thwart)</i>: When an enemy initiates an attack, remove 3 threat from a scheme."
}
```

Script `src/cards/pack/fne/60049.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def get_their_attention(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Event)
        this.RemoveThreatFromSchemes(effect.targets, 3, effect)
    return [AbilityFactory.WhenUnitWouldAttack(AbilityType.HeroInterrupt, Enemy, get_their_attention).SetPlay().SetLabel('defense', 'thwart').SetTarget(Scheme2, has_threat=True)]
```

#### `60050` In Harm's Way

```json
{
 "card_id": "60050",
 "type": "Event",
 "name": "In Harm's Way",
 "subtitle": "",
 "desc": {
  "Cost": "3*",
  "RES": "R",
  "Class": "Protection"
 },
 "traits": [
  "ATTACK",
  "THWART"
 ],
 "set_name": "",
 "text": "[star] Increase the cost to play this card by 1 for each ally you control.\n<b>Hero Action</b> <i>(attack/thwart)</i>: Deal X damage to an enemy and remove X threat from a scheme, where X is your DEF."
}
```

Script `src/cards/pack/fne/60050.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def in_harms_way(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()
        value = initiator.GetHero().defense
        if (value <= 0):
            return
        this.DealDamage(effect.targets, value, effect)
        def remove_threat(targets: Sequence['CardFace']):
            this.RemoveThreatFromSchemes(targets, value, effect)
        initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Remove X threat from a scheme', remove_threat).SetTarget(Scheme2, has_threat=True))
    def increase_cost(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> None:
        player = effect.this.GetControlByOrOwner()
        value = len(player.allies.Get())
        if (value > 0):
            message.UpdateCost(value, effect)
    def check_this_cost(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        if (message.check_effect.this != effect.this):
            return False
        return message.check_effect.ability.is_play
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, in_harms_way).SetPlay().SetLabel('attack', 'thwart').SetTarget(Enemy),
            AbilityFactory.WhenCalculateEffectCost(AbilityType.NonKeywordStar, increase_cost, conditions=[check_this_cost]).CanWorkOnlyInHand()]
```

#### `60051` 

```json
{
 "card_id": "60051",
 "full_link": "32014"
}
```

*Pas de script : tout passe par la fiche.*

#### `60052` The Best Offense...

```json
{
 "card_id": "60052",
 "type": "Upgrade",
 "name": "The Best Offense...",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "RES": "B",
  "Temporary": "1",
  "Class": "Protection"
 },
 "traits": [
  "CONDITION"
 ],
 "set_name": "",
 "text": "Temporary.\nYour hero gets +1 DEF.\nUse your DEF in place of your THW and ATK. <i>(Ignore any modifiers to your THW and ATK.)</i>"
}
```

Script `src/cards/pack/fne/60052.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def the_best_offense(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        hero = message.trigger.CastTo(Hero)
        current = (hero.attack if (message.power == 'ATK') else hero.thwart)
        value = (hero.defense - current)
        if value:
            message.GainValue(value, effect)
    def check_attached(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> bool:
        return (effect.this.GetBindFace() == message.trigger)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            *AbilityFactory.GiveKeywordToAttached(Hero, defense=1),
            AbilityFactory.WhenUnitUseBasicPower(AbilityType.ForcedInterrupt, Hero, the_best_offense, powers=['ATK', 'THW'], conditions=[check_attached])]
```

#### `60053` * Ronin

```json
{
 "card_id": "60053",
 "type": "Upgrade",
 "name": "* Ronin",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "RES": "B",
  "Class": "Protection"
 },
 "traits": [
  "TITLE"
 ],
 "set_name": "",
 "text": "While you do not control any allies, your hero gets +1 DEF and gains retaliate 1."
}
```

Script `src/cards/pack/fne/60053.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def no_allies(effect: 'Effect', attach: 'CardFace', ui: List['CardFace']) -> int:
        player = attach.GetControlByPlayer()
        return (player.allies.FindCard(card_type=Ally) == None)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            *AbilityFactory.GiveKeywordToAttached(Hero, get_new_value=no_allies, defense=1, retaliate=1, ex_change_on_event=OnEvent.CardInPlay(Ally))]
```

#### `60054` Stand Alone

```json
{
 "card_id": "60054",
 "type": "Upgrade",
 "name": "Stand Alone",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "RES": "Y",
  "MaxPerUnit": "1",
  "Class": "Protection"
 },
 "traits": [
  "CONDITION"
 ],
 "set_name": "",
 "text": "Max 1 per player.\n<b>Hero Interrupt</b>: When an enemy attacks you <i>(before any defender is declared)</i>, if you do not control any allies, exhaust Stand Alone → ready your hero."
}
```

Script `src/cards/pack/fne/60054.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def stand_alone(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        Faces.ReadyAll([player.GetIdentity()], effect)
    def check_no_allies(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        player = effect.this.GetControlByPlayer()
        if (message.GetAgainstPlayer() != player):
            return False
        return (player.allies.FindCard(card_type=Ally) == None)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenUnitAttackYou(AbilityType.HeroInterrupt, Enemy, stand_alone, conditions=[check_no_allies]).SetCostFunc(CostFunc.Exhaust('This'))]
```

#### `60055` See No Evil, Hear No Evil

```json
{
 "card_id": "60055",
 "type": "Event",
 "name": "See No Evil, Hear No Evil",
 "subtitle": "",
 "desc": {
  "Cost": "2",
  "RES": "G",
  "MaxPerDeck": "1",
  "TeamUp": "Daredevil;Echo",
  "Class": "Basic"
 },
 "traits": [
  "ATTACK",
  "THWART"
 ],
 "set_name": "",
 "text": "Team-Up (Daredevil and Echo). Max 1 per deck.\n<b>Hero Action</b> <i>(attack/thwart)</i>: Choose 2 of the following (you may choose the same option twice):\n• Deal 3 damage to an enemy.\n• Remove 3 threat from a scheme."
}
```

Script `src/cards/pack/fne/60055.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def see_no_evil_hear_no_evil(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()
        def deal_damage(targets: Sequence['CardFace']):
            this.DealDamage(targets, 3, effect)
        def remove_threat(targets: Sequence['CardFace']):
            this.RemoveThreatFromSchemes(targets, 3, effect)
        initiator.ChooseAbilities(effect,
            AbilityFactory.ForChoiceAbility('Deal 3 damage to an enemy', deal_damage).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility('Remove 3 threat from a scheme', remove_threat).SetTarget(Scheme2, has_threat=True),
            repeat=2)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, see_no_evil_hear_no_evil).SetPlay().SetLabel('attack', 'thwart').SetTarget('TeamUp')]
```

#### `60056` 

```json
{
 "card_id": "60056",
 "full_link": "40059"
}
```

*Pas de script : tout passe par la fiche.*

#### `60057` 

```json
{
 "card_id": "60057",
 "full_link": "01088"
}
```

*Pas de script : tout passe par la fiche.*

#### `60058` 

```json
{
 "card_id": "60058",
 "full_link": "01089"
}
```

*Pas de script : tout passe par la fiche.*

#### `60059` 

```json
{
 "card_id": "60059",
 "full_link": "01090"
}
```

*Pas de script : tout passe par la fiche.*

### Set : Daredevil Nemesis (4 cartes)

#### `60033` * Bullseye

```json
{
 "card_id": "60033",
 "type": "Minion",
 "name": "* Bullseye",
 "subtitle": "",
 "desc": {
  "HP": "5",
  "ATK": "3",
  "SCH": "1",
  "Boost": "3",
  "Nemesis": "Matt Murdock"
 },
 "traits": [
  "ASSASSIN"
 ],
 "set_name": "Daredevil Nemesis",
 "text": "<b>When Revealed</b>: Choose:\n• Discard a [[Persona]] support you control.\n• Bullseye attacks you <i>(even in alter-ego form)</i>."
}
```

Script `src/cards/pack/fne/daredevil_nemesis/60033.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def bullseye_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        player = message.GetToPlayer()
        persona_supports = [x for x in Worlds.FindCardsOnField(effect, card_type=Support, trait='PERSONA') if (x.GetControlBy() == player)]
        def discard_persona(targets: Sequence['CardFace']):
            Faces.DiscardAll(targets, effect)
        def attack_you(targets: Sequence['CardFace']):
            this.DoAttackYou(player, effect)
        choices = []
        if persona_supports:
            choices.append(AbilityFactory.ForChoiceAbility('Discard a PERSONA support you control', discard_persona).SetTarget(persona_supports))
        choices.append(AbilityFactory.ForChoiceAbility('Bullseye attacks you', attack_you))
        player.ChooseAbilities(effect, *choices)
    return [AbilityFactory.WhenThisRevealed(None, bullseye_revealed)]
```

#### `60034` Deadliest Man Alive

```json
{
 "card_id": "60034",
 "type": "SideScheme",
 "name": "Deadliest Man Alive",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "StartingThreat": "5"
 },
 "traits": [],
 "set_name": "Daredevil Nemesis",
 "text": "<b>Forced Interrupt</b>: When Bullseye attacks, give him a facedown boost card."
}
```

Script `src/cards/pack/fne/daredevil_nemesis/60034.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def deadliest_man_alive(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        message.GiveAdditionalBoostCardForThisActivation(1, effect)
    return [AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, CardFinder(name='Bullseye'), deadliest_man_alive)]
```

#### `60035` Stolen Sai

```json
{
 "card_id": "60035",
 "type": "Attachment",
 "name": "Stolen Sai",
 "subtitle": "",
 "desc": {
  "Boost": "1",
  "ATK+": "1"
 },
 "traits": [
  "WEAPON"
 ],
 "set_name": "Daredevil Nemesis",
 "text": "Attach to the enemy with the highest ATK.\n[star] Attached character's attacks gain piercing.\n<b>Hero Action</b>: Spend [physical] [physical] resources → choose to either attach this card to Elektra or discard it.\n<hr />\n[star] <b>Boost</b>: If this activation is an attack, it gains piercing."
}
```

Script `src/cards/pack/fne/daredevil_nemesis/60035.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def discard_this(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        initiator = effect.GetInitiator()
        elektra = Worlds.FindCardOnField(effect, name='Elektra', card_type=Ally)
        if not elektra:
            Faces.DiscardAll([this], effect)
            return
        def attach(targets: Sequence['CardFace']):
            this.AttachTo2(elektra, effect)
        def discard(targets: Sequence['CardFace']):
            Faces.DiscardAll([this], effect)
        initiator.ChooseAbilities(effect,
            AbilityFactory.ForChoiceAbility('Attach this card to Elektra', attach),
            AbilityFactory.ForChoiceAbility('Discard this card', discard))
    def sai_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « Boost: If this activation is an attack, it gains piercing. »
        # Modele officiel : Crossfire 04027 (during_attack filtre les attaques).
        message.would_atk_message.GainPiercing(effect)
    return [AbilityFactory.AttachToFaceWhenPutIntoPlay(Enemy, highest_atk=True),
            AbilityFactory.UnitAttackGainKeyword(CardFinder(with_attach=True), piercing=True, conditions=[lambda effect, message: (message.trigger == effect.this.bind_face)]),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, discard_this).SetCostFunc(CostFunc.Spend(Cost('RR'))),
            AbilityFactory.WhenCardBecomeBoost('This', sai_boost, during_attack=True)]
```

#### `60036` Eye on the Target

```json
{
 "card_id": "60036",
 "type": "Treachery",
 "name": "Eye on the Target",
 "subtitle": "",
 "desc": {
  "Boost": "2"
 },
 "traits": [],
 "set_name": "Daredevil Nemesis",
 "text": "<b>When Revealed</b>: Choose:\n• Remove an ally or [[Persona]] support you control from the game.\n• Bullseye attacks you <i>(even in alter-ego form)</i>. If he is not in play, find him and reveal him."
}
```

Script `src/cards/pack/fne/daredevil_nemesis/60036.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def eye_on_the_target(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()
        candidates = [x for x in Worlds.FindCardsOnField(effect, card_type=Ally) if (x.GetControlBy() == player)]
        candidates += [x for x in Worlds.FindCardsOnField(effect, card_type=Support, trait='PERSONA') if (x.GetControlBy() == player)]
        def remove_from_game(targets: Sequence['CardFace']):
            Faces.RemoveAllFromGame(targets, effect)
        def attack_you(targets: Sequence['CardFace']):
            bullseye = Worlds.FindCardOnField(effect, name='Bullseye', card_type=Minion)
            if bullseye:
                bullseye.DoAttackYou(player, effect)
            else:
                face = Search.EncounterCard(effect, player, include_discard_pile=True, name='Bullseye')
                if face:
                    face.Reveal(player, effect)
        choices = []
        if candidates:
            choices.append(AbilityFactory.ForChoiceAbility('Remove an ally or PERSONA support you control from the game', remove_from_game).SetTarget(candidates))
        choices.append(AbilityFactory.ForChoiceAbility('Bullseye attacks you', attack_you))
        player.ChooseAbilities(effect, *choices)
    return [AbilityFactory.WhenThisRevealed(None, eye_on_the_target)]
```

### Set : Echo (14 cartes)

#### `60037a` * Echo

```json
{
 "card_id": "60037a",
 "type": "Hero",
 "name": "* Echo",
 "subtitle": "",
 "desc": {
  "HP": "9",
  "ATK": "2",
  "THW": "2",
  "DEF": "2",
  "HS": "5"
 },
 "traits": [
  "DEFENDER",
  "MARTIAL ARTIST"
 ],
 "set_name": "Echo",
 "text": "<i>Watch and Learn</i> — <b>Response</b>: After a player plays an aspect or basic event, tuck that event under here from that player's discard pile. Then, if there are more than 3 tucked cards here, discard all but 3 of those cards."
}
```

Script `src/cards/pack/fne/echo/60037a.py` :

```python
from . import *

# * Echo (Maya Lopez), face heros.
#
# Watch and Learn — Response: After a player plays an aspect or basic event,
#   tuck that event under here from that player's discard pile. Then, if there
#   are more than 3 tucked cards here, discard all but 3 of those cards.
#
# Le reste du texte d'Echo est porte par Photographic Reflexes (60040a/b/c) :
#   « If you are in hero form, you can discard Photographic Reflexes from your
#     hand to play an event tucked under Echo as if it were in your hand.
#     Reduce the cost to play that event by 2. You cannot trigger Echo's
#     "Watch and Learn" ability for that event. »
#
# DEUX CHEMINS mènent au même état de jeu, et les deux sont voulus :
#  - chemin A : on clique sur Photographic Reflexes EN MAIN, le moteur demande
#    quel evenement glisse rejouer. C'est la lecture litterale du texte, et
#    c'est le module 60040a/b/c qui le porte (voir `__init__.py`).
#  - chemin B : on clique directement sur la carte glissee, qui est rendue
#    « comme en main » par `YouMayPlayCardLikeInHand` ci-dessous, et
#    Photographic Reflexes se defausse toute seule en consequence.
# La reduction de 2 vit a UN SEUL endroit (`reduire_le_cout_des_glissees`),
# pour que les deux chemins paient exactement la meme chose.


def GetAbilities() -> Sequence['Ability']:
    def watch_and_learn(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Hero)
        controller = this.GetControlByPlayer()
        face = message.played_face
        if not (face.card.area.flags.is_discards or face.IsInProcessingArea()):
            return
        this.TuckCardUnderHere(face, effect)
        placed = this.GetPlacedCardArea().Get()
        excess = (len(placed) - 3)
        if (excess > 0):
            def action(targets: Sequence['CardFace']):
                Faces.DiscardAll(list(targets), effect)
            controller.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard tucked cards down to 3', action).SetTarget(list(placed), range=(excess, excess), not_move=True))

    def check_aspect_event(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> bool:
        face = message.played_face
        if not IsAspectOrBasicEvent(face):
            return False
        # « You cannot trigger Echo's Watch and Learn ability for THAT event » :
        # l'evenement joue DEPUIS la zone glissee ne s'y remet pas. C'est la
        # seule facon de jouer une carte de cette zone, donc la clause de
        # Photographic Reflexes est tenue ici, pour les deux chemins.
        return (message.from_area != effect.this.GetPlacedCardArea())

    def check_tucked_playable(effect: 'Effect', message: 'Message.CheckIfFaceIsLikeInHand') -> bool:
        this = effect.this
        face = message.which_face
        if (face.card.area != this.GetPlacedCardArea()):
            return False
        initiator = effect.GetInitiator()
        if not initiator:
            return False
        if (initiator != this.GetControlByPlayer()):
            return False
        if not initiator.IsInHeroForm():
            return False
        return (initiator.hand_cards.FindCard(name='Photographic Reflexes') != None)

    def rafraichir_les_glissees(effect: 'Effect', message: 'Message2') -> None:
        """Vide le cache « cette carte est comme en main » des cartes glissees.

        ⚠ DEFAUT MESURE LE 21/09/2026, signalement n°17 (Yarro). La reponse de
        `check_tucked_playable` depend de DEUX choses qui bougent sans que la
        carte glissee ne bouge : la FORME du joueur, et la presence de
        Photographic Reflexes dans sa main. Or `card.can_state.is_like_in_hand`
        n'est remis a zero qu'au DEPLACEMENT de la carte (`card.py`, MoveToArea)
        : la toute premiere reponse etait donc figee pour toute la vie de la
        carte sous Echo.

        Mesure, sur une carte glissee en forme heros (harnais test_capacites) :
          forme heros   -> IsLikeInHand() = True   (juste)
          forme CIVILE  -> IsLikeInHand() = True   (FAUX : la carte reste offerte)
          retour heros  -> IsLikeInHand() = False  (FAUX : elle ne l'est plus)
        Le cache vide a la main rendait bien True / False / True.

        Meme piege, meme remede que Magik (`aoa/magik/45030a.py`, qui remet
        `is_like_in_hand` a None sur les cartes du dessus de son deck).

        On ne rafraichit que les cartes ENCORE dans la zone glissee : celle
        qu'on est en train de jouer l'a deja quittee pour la zone de
        resolution, et son drapeau force par `PlayCardsLikeInTurn` ne doit pas
        etre efface en plein vol.
        """
        zone = effect.this.GetPlacedCardArea()
        if zone is None:
            return
        for face in zone.Get(True):
            if face is not None:
                face.card.can_state.is_like_in_hand = None

    def check_reflexes_quitte_la_main(effect: 'Effect', message: 'Message.WhenCardWouldMoveToArea') -> bool:
        return message.from_area.flags.is_in_hand

    def discard_photographic_reflexes(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        """Chemin B : la carte glissee est cliquee, Photographic Reflexes part seule.

        ⚠ Rien a faire sur le chemin A : la carte y a deja ete defaussee comme
        COUT, et Echo en defausserait une SECONDE (voir `REFLEXES_DEJA_PAYEES`).
        """
        this = effect.this
        player = this.GetControlByPlayer()
        if player.flag.Get(REFLEXES_DEJA_PAYEES):
            return
        prs = [x for x in player.hand_cards.Get() if x.IsName('Photographic Reflexes')]
        if not prs:
            return
        if (len({x.paper.card_id for x in prs}) <= 1):
            Faces.DiscardAll([prs[0]], effect)
            return
        def action(targets: Sequence['CardFace']):
            Faces.DiscardAll(list(targets), effect)
        player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard a Photographic Reflexes', action).SetTarget(prs, range=(1, 1), not_move=True))

    def check_played_from_tuck(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> bool:
        return (message.from_area == effect.this.GetPlacedCardArea())

    def reduire_le_cout_des_glissees(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> None:
        message.UpdateCost(-2, effect)

    def check_cout_d_une_glissee(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        """« Reduce the cost to play that event by 2 ».

        ⚠ CORRIGE LE 21/09/2026. C'etait `CanGenerateResources(Resources('GG'))`
        : Echo offrait DEUX RESSOURCES WILD au lieu de reduire le cout. Le
        montant paye par la main est le meme dans le cas ordinaire, mais ce
        n'est pas la meme regle — deux wild couvrent une exigence de couleur
        (`Requirement`) qu'une reduction de cout laisse a payer, et elles
        comptent comme des ressources DEPENSEES pour toute carte qui lit le
        paiement. L'idiome du depot pour cette tournure exacte est
        `WhenCalculateEffectCost` + `UpdateCost` (dz014 Lightbringr, aa002
        Scarlet Witch, meme phrase imprimee).

        La condition est « la carte payee est dans la zone glissee », sans
        regarder la main : jouer une carte de cette zone n'est possible QUE par
        Photographic Reflexes (chemin A, ou PR est deja defaussee au moment du
        paiement ; chemin B, ou elle est encore en main). Une condition « PR en
        main » ferait donc sauter la reduction sur le chemin A, et la
        DOUBLERAIT sur le chemin A si le joueur tenait une seconde copie.

        ⚠ LE CONTROLE DU PAYEUR EST RESTE, et c'est volontaire. L'ancienne
        `check_pay_for_tucked` verifiait `message.GetToPlayer()` ; le perdre
        aurait offert la reduction a un AUTRE joueur qui aide a payer (les
        cartes `Alliance`, « the players can pay this card's costs as a
        group »). La zone seule ne suffit donc pas.
        """
        if not message.is_play:
            return False
        if message.check_effect is None:
            return False
        zone = effect.this.GetPlacedCardArea()
        paying_face = message.check_effect.this
        if zone is None or paying_face is None or paying_face.card.area != zone:
            return False
        return message.GetToPlayer() == effect.this.GetControlByPlayer()

    return [AbilityFactory.AfterPlayerPlayedCard(AbilityType.Response, 'AnyPlayer', None, watch_and_learn, conditions=[check_aspect_event]).SetName('Watch and Learn'),
            *AbilityFactory.YouMayPlayCardLikeInHand(AbilityType.NonKeyword, None, conditions=[check_tucked_playable]),
            AbilityFactory.WhenPlayerPlayCard(AbilityType.Rule, 'You', None, discard_photographic_reflexes, conditions=[check_played_from_tuck]),
            AbilityFactory.WhenCalculateEffectCost(AbilityType.NonKeyword, reduire_le_cout_des_glissees, conditions=[check_cout_d_une_glissee]).NoOutOfPlayLimit(),
            # Les trois rafraichissements du cache (voir `rafraichir_les_glissees`).
            # ⚠ `AbilityType.Rule` N'EST PAS DECORATIF ICI : c'est lui qui pose
            # `is_ignore_game_area` (ability_type.py), donc `is_ignore_out_of_play`.
            # Sans lui, une aptitude `NonKeyword` portee par la face HEROS cesserait
            # d'ecouter des que cette face part dans `aside_deck` — c'est-a-dire
            # PILE au moment de la bascule vers la forme civile. Le rafraichissement
            # ne marcherait que dans un sens, en silence.
            AbilityFactory.AfterUnitChangeForm(AbilityType.Rule, 'You', rafraichir_les_glissees),
            AbilityFactory.AfterCardEnterHand(AbilityType.Rule, CardFinder(name='Photographic Reflexes'), rafraichir_les_glissees),
            AbilityFactory.WhenCardWouldMoveToArea(AbilityType.Rule, CardFinder(name='Photographic Reflexes'), rafraichir_les_glissees, conditions=[check_reflexes_quitte_la_main])]
```

#### `60037b` * Maya Lopez

```json
{
 "card_id": "60037b",
 "type": "AlterEgo",
 "name": "* Maya Lopez",
 "subtitle": "",
 "desc": {
  "HP": "9",
  "REC": "3",
  "HS": "6"
 },
 "traits": [
  "CIVILIAN"
 ],
 "set_name": "Echo",
 "text": "<i>Practice Makes Perfect</i> — <b>Interrupt</b>: When you change to hero form, search your deck for an aspect or basic event and add it to your hand. <i>(Shuffle.)</i>"
}
```

Script `src/cards/pack/fne/echo/60037b.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def practice_makes_perfect(effect: 'Effect', message: 'Message.WhenUnitWouldChangeForm') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)
        initiator = effect.GetInitiator()
        face = Search.PlayerCard(effect, initiator, include_player_deck=True, may=True, finder=CardFinder(card_type=Event, card_classes=[*ASPECT_OR_BASIC_CLASSES]))
        if face:
            Faces.AddToHand([face], initiator, effect)
    return [AbilityFactory.WhenUnitWouldChangeForm(AbilityType.Interrupt, 'You', practice_makes_perfect, to_form=Hero).SetName('Practice Makes Perfect')]
```

#### `60039` * Daredevil (Matt Murdock)

```json
{
 "card_id": "60039",
 "type": "Ally",
 "name": "* Daredevil",
 "subtitle": "Matt Murdock",
 "desc": {
  "Cost": "3",
  "HP": "3",
  "ATK": "2*",
  "THW": "2*",
  "RES": "G",
  "Class": "Hero"
 },
 "traits": [
  "DEFENDER",
  "MARTIAL ARTIST"
 ],
 "set_name": "Echo",
 "text": "[star] <b>Response</b>: After Daredevil uses a basic power, reduce the cost of the next event you play this round by 1."
}
```

Script `src/cards/pack/fne/echo/60039.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def follow_my_lead(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        player = this.GetControlByPlayer()
        finder = CardFinder(card_type=Event)
        def check_cost_card(e2: 'Effect', m2: 'Message.WhenCalculateEffectCost') -> bool:
            return finder.Check(m2.check_effect.this)
        def check_play_card(e2: 'Effect', m2: 'Message.WhenPlayerWouldPlayCard') -> bool:
            return finder.Check(m2.play_face)
        def check_player(e2: 'Effect', m2: 'TriggerNonePlayerMessage') -> bool:
            return (player == m2.to_player)
        def update_cost(e2: 'Effect', m2: 'Message.WhenCalculateEffectCost') -> None:
            m2.UpdateCost(-1, e2)
        modify_effects = this.effect.RegisterTemp(AbilityFactory.WhenCalculateEffectCost(AbilityType.Temp0, update_cost, conditions=[check_cost_card, check_player, lambda e2, m2: m2.check_effect.ability.is_play]), unregister_after_exec=False, until_round_end=True)
        def unregister(e2: 'Effect', m2: 'Message2') -> None:
            Effects.UnRegister(modify_effects)
        this.effect.RegisterTemp(Ability(AbilityType.Temp0, Message.WhenPlayerWouldPlayCard, [check_play_card, check_player], unregister), unregister_after_exec=True, until_round_end=True)
    return [AbilityFactory.AfterUnitUseBasicPower(AbilityType.Response, 'This', follow_my_lead)]
```

#### `60040a` Photographic Reflexes

```json
{
 "card_id": "60040a",
 "type": "Event",
 "name": "Photographic Reflexes",
 "subtitle": "",
 "desc": {
  "Cost": "-1",
  "RES": "Y",
  "Class": "Hero"
 },
 "traits": [],
 "set_name": "Echo",
 "text": "[star] If you are in hero form, you can discard Photographic Reflexes from your hand to play an event tucked under Echo as if it were in your hand. Reduce the cost to play that event by 2. You cannot trigger Echo's <i>\"Watch and Learn\"</i> ability for that event."
}
```

Script `src/cards/pack/fne/echo/60040a.py` :

```python
from . import *

# Photographic Reflexes (variante A) — meme texte que les deux autres,
# seule l'icone de ressource change. Tout le module est en commun :
# `AbilitesPhotographicReflexes` dans le `__init__.py` du set.
def GetAbilities() -> Sequence['Ability']:
    return list(AbilitesPhotographicReflexes())
```

#### `60040b` Photographic Reflexes

```json
{
 "card_id": "60040b",
 "type": "Event",
 "name": "Photographic Reflexes",
 "subtitle": "",
 "desc": {
  "Cost": "-1",
  "RES": "B",
  "Class": "Hero"
 },
 "traits": [],
 "set_name": "Echo",
 "text": "[star] If you are in hero form, you can discard Photographic Reflexes from your hand to play an event tucked under Echo as if it were in your hand. Reduce the cost to play that event by 2. You cannot trigger Echo's <i>\"Watch and Learn\"</i> ability for that event."
}
```

Script `src/cards/pack/fne/echo/60040b.py` :

```python
from . import *

# Photographic Reflexes (variante B) — meme texte que les deux autres,
# seule l'icone de ressource change. Tout le module est en commun :
# `AbilitesPhotographicReflexes` dans le `__init__.py` du set.
def GetAbilities() -> Sequence['Ability']:
    return list(AbilitesPhotographicReflexes())
```

#### `60040c` Photographic Reflexes

```json
{
 "card_id": "60040c",
 "type": "Event",
 "name": "Photographic Reflexes",
 "subtitle": "",
 "desc": {
  "Cost": "-1",
  "RES": "R",
  "Class": "Hero"
 },
 "traits": [],
 "set_name": "Echo",
 "text": "[star] If you are in hero form, you can discard Photographic Reflexes from your hand to play an event tucked under Echo as if it were in your hand. Reduce the cost to play that event by 2. You cannot trigger Echo's <i>\"Watch and Learn\"</i> ability for that event."
}
```

Script `src/cards/pack/fne/echo/60040c.py` :

```python
from . import *

# Photographic Reflexes (variante C) — meme texte que les deux autres,
# seule l'icone de ressource change. Tout le module est en commun :
# `AbilitesPhotographicReflexes` dans le `__init__.py` du set.
def GetAbilities() -> Sequence['Ability']:
    return list(AbilitesPhotographicReflexes())
```

#### `60041` Study the Tape

```json
{
 "card_id": "60041",
 "type": "Event",
 "name": "Study the Tape",
 "subtitle": "",
 "desc": {
  "Cost": "0",
  "RES": "B",
  "Class": "Hero"
 },
 "traits": [
  "TACTIC"
 ],
 "set_name": "Echo",
 "text": "<b>Action</b>: Search any player's discard pile for 1 aspect event, 1 basic event, or 1 copy of Photographic Reflexes and add that card to your hand."
}
```

Script `src/cards/pack/fne/echo/60041.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def study_the_tape(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()
        faces = []
        def collect(player: 'Player'):
            for face in player.discard_pile.Get():
                if IsAspectOrBasicEvent(face) or (face.paper.name == 'Photographic Reflexes'):
                    faces.append(face)
        Players.ForEachPlayer(effect, collect)
        if not faces:
            return
        def action(targets: Sequence['CardFace']):
            Faces.AddToHand(list(targets), initiator, effect)
        initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Add that card to your hand', action).SetTarget(faces, range=(1, 1)))
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, study_the_tape).SetPlay().SetLabel()]
```

#### `60042` * The Rez

```json
{
 "card_id": "60042",
 "type": "Support",
 "name": "* The Rez",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "RES": "Y",
  "Class": "Hero"
 },
 "traits": [
  "LOCATION"
 ],
 "set_name": "Echo",
 "text": "<b>Alter-Ego Action</b>: Exhaust The Rez → heal X damage from Maya Lopez, where X is the highest cost among cards tucked under her."
}
```

Script `src/cards/pack/fne/echo/60042.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def the_rez(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()
        value = 0
        for face in identity.GetPlacedCardArea().Get():
            value = max(value, GetPrintedCostValue(face))
        if (value > 0):
            identity.HealHealth(value, effect)
    return [AbilityFactory.CanPlayThisSupportCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, the_rez).SetCostFunc(CostFunc.Exhaust('This'))]
```

#### `60043` American Sign Language

```json
{
 "card_id": "60043",
 "type": "Upgrade",
 "name": "American Sign Language",
 "subtitle": "",
 "desc": {
  "Cost": "2",
  "RES": "B",
  "Class": "Hero"
 },
 "traits": [
  "SKILL"
 ],
 "set_name": "Echo",
 "text": "<b>Hero Resource</b>: Exhaust this card → generate a [wild] resource for an event being played by any player."
}
```

Script `src/cards/pack/fne/echo/60043.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.CanGenerateResources(AbilityType.HeroResource, Resources('G'), for_card=CardFinder(card_type=Event), is_play_card=True).SetCostFunc(CostFunc.Exhaust('This')).AnyPlayerCanDoThis()]
```

#### `60044` Choreography

```json
{
 "card_id": "60044",
 "type": "Upgrade",
 "name": "Choreography",
 "subtitle": "",
 "desc": {
  "Cost": "1",
  "RES": "B",
  "Class": "Hero"
 },
 "traits": [
  "SKILL"
 ],
 "set_name": "Echo",
 "text": "<b>Action</b>: Exhaust this card → shuffle 1 aspect or basic event from your discard pile into your deck. If you are in alter-ego form, draw 1 card."
}
```

Script `src/cards/pack/fne/echo/60044.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def choreography(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        initiator = effect.GetInitiator()
        faces = [face for face in initiator.discard_pile.Get() if IsAspectOrBasicEvent(face)]
        if not faces:
            if not initiator.IsInHeroForm():
                initiator.DrawUp(1, effect)
            return
        def action(targets: Sequence['CardFace']):
            Faces.ShuffleAllTo(list(targets), initiator.player_deck, effect)
            if not initiator.IsInHeroForm():
                initiator.DrawUp(1, effect)
        initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Shuffle 1 aspect or basic event into your deck', action).SetTarget(faces, range=(1, 1)))
    def check_has_event(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        initiator = effect.GetInitiator()
        if not initiator:
            return False
        if not initiator.IsInHeroForm():
            return True
        for face in initiator.discard_pile.Get():
            if IsAspectOrBasicEvent(face):
                return True
        return False
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, choreography, conditions=[check_has_event]).SetCostFunc(CostFunc.Exhaust('This'))]
```

#### `60045` * Echo's Katana

```json
{
 "card_id": "60045",
 "type": "Upgrade",
 "name": "* Echo's Katana",
 "subtitle": "",
 "desc": {
  "Cost": "2",
  "RES": "R",
  "Restricted": "1",
  "Class": "Hero"
 },
 "traits": [
  "WEAPON"
 ],
 "set_name": "Echo",
 "text": "Restricted.\n<b>Hero Response</b> <i>(attack)</i>: After you play an event, exhaust Echo's Katana → deal damage to an enemy equal to that event's printed cost. This attack gains piercing."
}
```

Script `src/cards/pack/fne/echo/60045.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def echos_katana(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        value = GetPrintedCostValue(message.played_face)
        if (value <= 0):
            return
        this.DealDamage(effect.targets, value, effect, property=AttackProperty(piercing=True))
    def check_printed_cost(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> bool:
        return (GetPrintedCostValue(message.played_face) > 0)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.AfterPlayerPlayedCard(AbilityType.HeroResponse, 'You', CardFinder(card_type=Event), echos_katana, conditions=[check_printed_cost]).SetCostFunc(CostFunc.Exhaust('This')).SetLabel('attack').SetTarget(Enemy)]
```

#### `60046` Improvisation

```json
{
 "card_id": "60046",
 "type": "Upgrade",
 "name": "Improvisation",
 "subtitle": "",
 "desc": {
  "Cost": "3",
  "RES": "Y",
  "Class": "Hero"
 },
 "traits": [
  "SKILL"
 ],
 "set_name": "Echo",
 "text": "<b>Hero Response</b>: After you play an event, if it has the following traits:\n• [[Attack]] — heal 1 damage from Echo.\n• [[Defense]] — remove 1 threat from a scheme.\n• [[Thwart]] — deal 1 damage to an enemy."
}
```

Script `src/cards/pack/fne/echo/60046.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def improvisation(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()
        face = message.played_face
        if face.HasTrait('ATTACK'):
            identity.HealHealth(1, effect)
        if face.HasTrait('DEFENSE'):
            def remove_threat(targets: Sequence['CardFace']):
                this.RemoveThreatFromSchemes(targets, 1, effect)
            initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Remove 1 threat from a scheme', remove_threat).SetTarget(Scheme2, has_threat=True))
        if face.HasTrait('THWART'):
            def deal_damage(targets: Sequence['CardFace']):
                this.DealDamage(targets, 1, effect)
            initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Deal 1 damage to an enemy', deal_damage).SetTarget(Enemy))
    def check_traits(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> bool:
        face = message.played_face
        return (face.HasTrait('ATTACK') or (face.HasTrait('DEFENSE') or face.HasTrait('THWART')))
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.AfterPlayerPlayedCard(AbilityType.HeroResponse, 'You', CardFinder(card_type=Event), improvisation, conditions=[check_traits])]
```

#### `60047` Muscle Memory

```json
{
 "card_id": "60047",
 "type": "Upgrade",
 "name": "Muscle Memory",
 "subtitle": "",
 "desc": {
  "Cost": "2",
  "RES": "R",
  "Class": "Hero"
 },
 "traits": [
  "SKILL"
 ],
 "set_name": "Echo",
 "text": "<b>Hero Action</b>: Exhaust this card → add an event tucked under Echo to your hand."
}
```

Script `src/cards/pack/fne/echo/60047.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def muscle_memory(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        initiator = effect.GetInitiator()
        placed = initiator.GetIdentity().GetPlacedCardArea().Get()
        if not placed:
            return
        def action(targets: Sequence['CardFace']):
            Faces.AddToHand(list(targets), initiator, effect)
        initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Add a tucked event to your hand', action).SetTarget(list(placed), range=(1, 1)))
    def check_has_tucked(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        initiator = effect.GetInitiator()
        if not initiator:
            return False
        return (len(initiator.GetIdentity().GetPlacedCardArea().Get()) > 0)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, muscle_memory, conditions=[check_has_tucked]).SetCostFunc(CostFunc.Exhaust('This'))]
```

#### `60060` Raised by the Kingpin

```json
{
 "card_id": "60060",
 "type": "Obligation",
 "name": "Raised by the Kingpin",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "GiveTo": "Maya Lopez"
 },
 "traits": [],
 "set_name": "Echo",
 "text": "<b><i>Give to the Maya Lopez player.</i></b>\nYou cannot deal damage to Kingpin.\n<b>When Revealed</b>: Find Kingpin and put him into play engaged with you.\n<b>Response</b>: After you thwart, place that threat here. If there is 4 or more threat here, remove this card from the game."
}
```

Script `src/cards/pack/fne/echo/60060.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def raised_by_the_kingpin(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)
        player = this.GetGaveToPlayer() or message.GetToPlayer()
        face = Worlds.FindCardOnField(effect, name='Kingpin', card_type=Minion)
        if not face:
            face = Search.EncounterCard(effect, include_discard_pile=True, include_set_aside=True, name='Kingpin', card_type=Minion)
            if face:
                face.PutIntoPlay(player, effect)
                return
    def after_thwart(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> None:
        this = effect.this.CastTo(Obligation)
        num = message.remove_threat
        if (num > 0):
            this.PlaceCountersInternal(num, 'all-purpose', effect)
        if (this.GetAllCounters() >= 4):
            Faces.RemoveAllFromGame([this], effect)
    def check_you(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> bool:
        this = effect.this.CastTo(Obligation)
        return (message.trigger.GetControlBy() == this.GetGaveToPlayer())
    def check_source_yours(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this.CastTo(Obligation)
        source = message.source
        if (source == None):
            return False
        return (source.GetControlBy() == this.GetGaveToPlayer())
    return [AbilityFactory.WhenThisRevealed(None, raised_by_the_kingpin),
            AbilityFactory.AfterUnitThwartScheme(AbilityType.Response, None, None, after_thwart, remove_threat=True, conditions=[check_you]),
            AbilityFactory.UnitCannotTakeDamageWhile(AbilityType.NonKeyword, CardFinder(name='Kingpin', card_type=Minion), conditions=[check_source_yours])]
```

### Set : Echo Nemesis (4 cartes)

#### `60061` * Kingpin

```json
{
 "card_id": "60061",
 "type": "Minion",
 "name": "* Kingpin",
 "subtitle": "",
 "desc": {
  "HP": "6",
  "ATK": "2*",
  "SCH": "3",
  "Boost": "3",
  "Nemesis": "Maya Lopez"
 },
 "traits": [
  "CRIMINAL"
 ],
 "set_name": "Echo Nemesis",
 "text": "[star] <b>Forced Interrupt</b>: When Kingpin would attack the Maya Lopez player, he schemes instead.\n<i>(Echo's nemesis minion.)</i>"
}
```

Script `src/cards/pack/fne/echo_nemesis/60061.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    def kingpin_schemes_instead(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        message.DoSchemeInstead(effect)
    def check_maya_player(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        player = message.GetAgainstPlayer()
        if not Player.IsType(player):
            return False
        identity = player.GetIdentity()
        if (identity.paper.name == 'Maya Lopez'):
            return True
        for face in identity.card.back_faces:
            if (face.paper.name == 'Maya Lopez'):
                return True
        return False
    return [AbilityFactory.WhenUnitAttackYou(AbilityType.ForcedInterrupt, 'This', kingpin_schemes_instead, conditions=[check_maya_player])]
```

#### `60062` Master Manipulator

```json
{
 "card_id": "60062",
 "type": "SideScheme",
 "name": "Master Manipulator",
 "subtitle": "",
 "desc": {
  "StartingThreat": "2*"
 },
 "traits": [],
 "set_name": "Echo Nemesis",
 "text": "Kingpin cannot take damage.\n<b>When Revealed</b>: Find Kingpin and put him into play engaged with you.\n<hr />\n[star] <b>Boost</b>: If Kingpin is in play, reveal this scheme."
}
```

Script `src/cards/pack/fne/echo_nemesis/60062.py` :

```python
from . import *
from cards.pack.fne import KingpinEnJeu
def GetAbilities() -> Sequence['Ability']:
    def find_kingpin(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        player = message.GetToPlayer()
        face = Worlds.FindCardOnField(effect, name='Kingpin', card_type=Minion)
        if not face:
            face = Search.EncounterCard(effect, include_discard_pile=True, include_set_aside=True, name='Kingpin', card_type=Minion)
            if face:
                face.PutIntoPlay(player, effect)
                return
    def boost_reveal(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        player = message.GetToPlayer()
        this.Reveal(player, effect)
    def check_kingpin_in_play(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> bool:
        return (KingpinEnJeu(effect) is not None)
    return [AbilityFactory.UnitCannotTakeDamageWhile(AbilityType.NonKeyword, CardFinder(name='Kingpin')),
            AbilityFactory.WhenThisRevealed(None, find_kingpin),
            AbilityFactory.WhenBoostCardTurnedFaceUp(AbilityType.Boost, None, boost_reveal, conditions=[check_kingpin_in_play])]
```

#### `60063` Kingpin's Henchman

```json
{
 "card_id": "60063",
 "type": "Minion",
 "name": "Kingpin's Henchman",
 "subtitle": "",
 "desc": {
  "HP": "4",
  "ATK": "2",
  "SCH": "1",
  "Boost": "1",
  "Guard": "1"
 },
 "traits": [
  "CRIMINAL"
 ],
 "set_name": "Echo Nemesis",
 "text": "Guard.\nKingpin cannot take damage."
}
```

Script `src/cards/pack/fne/echo_nemesis/60063.py` :

```python
from . import *
def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.UnitCannotTakeDamageWhile(AbilityType.NonKeyword, CardFinder(name='Kingpin'))]
```

#### `60064` Pawn of the Kingpin

```json
{
 "card_id": "60064",
 "type": "Treachery",
 "name": "Pawn of the Kingpin",
 "subtitle": "",
 "desc": {
  "Boost": "2"
 },
 "traits": [],
 "set_name": "Echo Nemesis",
 "text": "<b>When Revealed (Alter-Ego)</b>: If Kingpin is in play, he schemes. Otherwise, this card gains surge.\n<b>When Revealed (Hero)</b>: Deal damage to a hero equal to your hero's ATK."
}
```

Script `src/cards/pack/fne/echo_nemesis/60064.py` :

```python
from . import *
from cards.pack.fne import KingpinEnJeu
def GetAbilities() -> Sequence['Ability']:
    def pawn_alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        kingpin = KingpinEnJeu(effect)
        if kingpin:
            kingpin.DoSchemes(player, effect)
            return
        ThisCardGainSurge(effect, message)
    def pawn_hero(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()
        value = player.GetHero().attack
        if (value <= 0):
            return
        heroes = [p.GetIdentity() for p in Worlds.GetPlayers(effect) if Hero.IsType(p.GetIdentity())]
        if not heroes:
            return
        if (len(heroes) == 1):
            this.DealDamage(heroes, value, effect)
            return
        def act(chosen: Sequence['CardFace']):
            this.DealDamage(list(chosen), value, effect)
        player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Deal the damage to a hero', act).SetTarget(heroes, range=(1, 1), not_move=True))
    return [AbilityFactory.WhenThisRevealed('Alter-Ego', pawn_alter_ego),
            AbilityFactory.WhenThisRevealed('Hero', pawn_hero)]
```

### Set : Bullseye (12 cartes)

#### `60065` * Bullseye

```json
{
 "card_id": "60065",
 "type": "Villain",
 "name": "* Bullseye",
 "subtitle": "",
 "desc": {
  "HP": "14*",
  "ATK": "1",
  "SCH": "0",
  "Stage": "1"
 },
 "traits": [
  "ASSASSIN",
  "UNDERLING"
 ],
 "set_name": "Bullseye",
 "text": "<b>When Revealed</b>: Set aside Adamantium-Laced Spine (68A).\n[star] <b>Forced Interrupt</b>: When Bullseye activates, each of his boost cards gains [boost]. If this activation is an attack, it gains ranged."
}
```

Script `src/cards/pack/fne/bullseye/60065.py` :

```python
from . import *

# * Bullseye (I) — SCH 0 / ATK 1 / 14[per_hero]
# When Revealed: Set aside Adamantium-Laced Spine (68A).
# [star] Forced Interrupt : voir CapacitesDeBullseye.
# La colonne est dans le deck de rencontre (set Bullseye) ; on la met de cote
# pour que le stade II la « Find » (la recherche couvre la mise de cote).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        SetupCards.SetAsideCards(effect, name="Adamantium-Laced Spine", card_type=Attachment)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        *CapacitesDeBullseye(),
    ]
```

#### `60066` * Bullseye

```json
{
 "card_id": "60066",
 "type": "Villain",
 "name": "* Bullseye",
 "subtitle": "",
 "desc": {
  "HP": "16*",
  "ATK": "2",
  "SCH": "1",
  "Stage": "2"
 },
 "traits": [
  "ASSASSIN",
  "UNDERLING"
 ],
 "set_name": "Bullseye",
 "text": "<b>When Revealed</b>: Find Adamantium-Laced Spine and attach it to Bullseye.\n[star] <b>Forced Interrupt</b>: When Bullseye activates, each of his boost cards gains [boost]. If this activation is an attack, it gains ranged."
}
```

Script `src/cards/pack/fne/bullseye/60066.py` :

```python
from . import *

# * Bullseye (II) — SCH 1 / ATK 2 / 16[per_hero]
# When Revealed: Find Adamantium-Laced Spine and attach it to Bullseye.
# « Find » fouille toutes les zones (mise de cote, deck, defausse) :
# Find.FindAndAttachTo (find.py:74).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Villain)
        Find.FindAndAttachTo(effect, this, who_perform=message.GetToPlayer(), name="Adamantium-Laced Spine", card_type=Attachment)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        *CapacitesDeBullseye(),
    ]
```

#### `60067` * Bullseye

```json
{
 "card_id": "60067",
 "type": "Villain",
 "name": "* Bullseye",
 "subtitle": "",
 "desc": {
  "HP": "18*",
  "ATK": "3",
  "SCH": "1",
  "Stage": "3"
 },
 "traits": [
  "ASSASSIN",
  "UNDERLING"
 ],
 "set_name": "Bullseye",
 "text": "<b>When Revealed</b>: Find Deranged Bloodlust and reveal it.\n[star] <b>Forced Interrupt</b>: When Bullseye activates, each of his boost cards gains [boost]. If this activation is an attack, it gains ranged."
}
```

Script `src/cards/pack/fne/bullseye/60067.py` :

```python
from . import *

# * Bullseye (III) — SCH 1 / ATK 3 / 18[per_hero]
# When Revealed: Find Deranged Bloodlust and reveal it.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Find.FindAndReveal(effect, message.GetToPlayer(), name="Deranged Bloodlust", card_type=SchemeSide2)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        *CapacitesDeBullseye(),
    ]
```

#### `60068a` * Adamantium-Laced Spine

```json
{
 "card_id": "60068a",
 "type": "Attachment",
 "name": "* Adamantium-Laced Spine",
 "subtitle": "",
 "desc": {
  "Permanent": "1"
 },
 "traits": [
  "TECH"
 ],
 "set_name": "Bullseye",
 "text": "Permanent.\n<b>Forced Interrupt</b>: When Bullseye would take damage, prevent all but 3 of that damage. Place the prevented damage here. Then, if there is 6 or more damage here, flip this card."
}
```

Script `src/cards/pack/fne/bullseye/60068a.py` :

```python
from . import *

# * Adamantium-Laced Spine (TECH) — Permanent.
# Forced Interrupt: When Bullseye would take damage, prevent all but 3 of that
#   damage. Place the prevented damage here. Then, if there is 6 or more damage
#   here, flip this card.
# Le « damage here » est un compteur nomme 'damage' sur l'attachement ; le
# recto-verso passe par RetournerLaColonne (card.Flip + raccrochage, voir __init__).
# Attache a Bullseye a l'entree en jeu (stade II le « Find and attach »).

def GetAbilities() -> Sequence['Ability']:

    def colonne(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)
        total = message.will_take_damage
        evite = max(0, total - 3)
        if evite > 0:
            message.PreventDamage(evite, effect)
            Faces.PlaceCountersOn([this], evite, 'damage', effect)
        if this.GetCounters('damage') >= 6:
            RetournerLaColonne(this, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Bullseye")),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            CardFinder(name="Bullseye"),
            colonne,
        ),
    ]
```

#### `60068b` * Damaged Spine

```json
{
 "card_id": "60068b",
 "type": "Attachment",
 "name": "* Damaged Spine",
 "subtitle": "",
 "desc": {
  "Permanent": "1"
 },
 "traits": [
  "TECH"
 ],
 "set_name": "Bullseye",
 "text": "Permanent.\n[star] <b>Forced Response</b>: After Bullseye schemes, remove 3 damage from here. Then, if there is no damage here, flip this card."
}
```

Script `src/cards/pack/fne/bullseye/60068b.py` :

```python
from . import *

# * Damaged Spine (TECH) — Permanent.
# [star] Forced Response: After Bullseye schemes, remove 3 damage from here.
#   Then, if there is no damage here, flip this card.

def GetAbilities() -> Sequence['Ability']:

    def repare(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.RemoveCountersOn([this], 3, 'damage', effect)
        if this.GetCounters('damage') <= 0:
            RetournerLaColonne(this, effect)

    return [
        # Le retournement DETACHE la carte (« Bullseye perd l'amelioration »,
        # constate au harnais) : comme 55007b, la face B porte son propre
        # AttachToFaceWhenPutIntoPlay pour se raccrocher.
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Bullseye")),
        AbilityFactory.AfterUnitSchemeEnd(
            AbilityType.ForcedResponse,
            CardFinder(name="Bullseye"),
            repare,
        ),
    ]
```

#### `60069` Raise the Stakes

```json
{
 "card_id": "60069",
 "type": "Attachment",
 "name": "Raise the Stakes",
 "subtitle": "",
 "desc": {
  "Boost": "3"
 },
 "traits": [
  "CONDITION"
 ],
 "set_name": "Bullseye",
 "text": "Attach to Bullseye.\n[star] <b>Forced Interrupt</b>: When Bullseye attacks, give him 1 additional boost card for this attack. If this attack defeats a friendly character, remove them and this card from the game. Otherwise, shuffle this card into the encounter deck."
}
```

Script `src/cards/pack/fne/bullseye/60069.py` :

```python
from . import *

# Raise the Stakes (CONDITION) — Attach to Bullseye.
# [star] Forced Interrupt: When Bullseye attacks, give him 1 additional boost
#   card for this attack. If this attack defeats a friendly character, remove
#   them and this card from the game. Otherwise, shuffle this card into the
#   encounter deck.
# Modeles : 02020 Hysteria (boost supplementaire), 01099 Charge
# (RunAt.AfterEnemyActivationEnd), 24023 Out for Blood (temp WhenUnitBeDefeated
# borne a l'attaque en cours pour SAVOIR qui a ete vaincu).

def GetAbilities() -> Sequence['Ability']:

    def mise(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Attachment)
        message.GiveAdditionalBoostCardForThisActivation(1, effect)
        vaincus: List['CardFace'] = []

        def noter(e: 'Effect', m: 'Message.WhenUnitBeDefeated') -> None:
            vaincus.append(m.trigger)

        temps = this.effect.Registers(
            AbilityFactory.WhenUnitBeDefeated(
                AbilityType.Temp0,
                Friend,
                noter,
                conditions=[lambda e, m: getattr(m, 'would_atk_message', None) is message],
            )
        )

        def fin() -> None:
            Effects.UnRegister(temps)
            if vaincus:
                Faces.RemoveAllFromGame(vaincus + [this], effect)
            elif this.IsInPlay():
                Faces.ShuffleAllTo([this], "EncounterDeck", effect)

        RunAt.AfterEnemyActivationEnd(effect, message, fin)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Bullseye")),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            CardFinder(name="Bullseye"),
            mise,
        ),
    ]
```

#### `60070` Deadly Sai

```json
{
 "card_id": "60070",
 "type": "Attachment",
 "name": "Deadly Sai",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "ATK+": "2"
 },
 "traits": [
  "WEAPON"
 ],
 "set_name": "Bullseye",
 "text": "Attach to Bullseye.\n[star] Bullseye's attacks lose ranged and gain piercing.\n<b>Hero Response</b>: After your hero defends against an attack from Bullseye, spend 2 different resources → discard this card."
}
```

Script `src/cards/pack/fne/bullseye/60070.py` :

```python
from . import *

# Deadly Sai (WEAPON) — Attach to Bullseye. +2 ATK (cle desc ATK+).
# [star] Bullseye's attacks lose ranged and gain piercing.
#   (piercing : UnitAttackGainKeyword ; « lose ranged » : lu par la capacite
#   etoilee de Bullseye, DeadlySaiAttache.)
# Hero Response: After your hero defends against an attack from Bullseye,
#   spend 2 different resources -> discard this card.
#   (AfterUnitDefendAgainstAttack("You", attacker=Bullseye) + Cost("2",
#   different_type=True), modele 05002 Red Dagger.)

def GetAbilities() -> Sequence['Ability']:

    def defausser(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Bullseye")),
        AbilityFactory.UnitAttackGainKeyword(CardFinder(name="Bullseye"), piercing=True),
        AbilityFactory.AfterUnitDefendAgainstAttack(
            AbilityType.HeroResponse,
            "You",
            defausser,
            attacker=CardFinder(name="Bullseye"),
        ).SetCost(Cost("2", different_type=True)),
    ]
```

#### `60071` Incessant Pursuit

```json
{
 "card_id": "60071",
 "type": "Attachment",
 "name": "Incessant Pursuit",
 "subtitle": "",
 "desc": {
  "Boost": "1"
 },
 "traits": [
  "CONDITION"
 ],
 "set_name": "Bullseye",
 "text": "Attach to an ally without Incessant Pursuit attached. Otherwise, this card gains surge.\n<b>Forced Interrupt</b>: When the villain would attack you, it attacks attached ally instead and the attack gains overkill. If this attack defeats attached ally, remove them from the game."
}
```

Script `src/cards/pack/fne/bullseye/60071.py` :

```python
from . import *

# Incessant Pursuit (CONDITION)
# Attach to an ally without Incessant Pursuit attached. Otherwise, surge.
# Forced Interrupt: When the villain would attack you, it attacks attached
#   ally instead and the attack gains overkill. If this attack defeats
#   attached ally, remove them from the game.
# Modeles : 21178 Beguiled (finder not_with_attach), 50096 Leaping Kick
# (BasicAttack([allie], overkill)), RECETTES §2 « instead ».
# « you » = le joueur qui controle l'allie attache.

def GetAbilities() -> Sequence['Ability']:

    def contre_moi(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        this = effect.this.CastTo(Attachment)
        allie = this.GetBindFace()
        joueur = message.GetAgainstPlayer()
        # ⚠ L'attaque de remplacement (BasicAttack sur l'allie) repasse ici :
        # sans ce garde, recursion infinie (constate au harnais).
        cibles = list(getattr(message, 'targets', None) or getattr(message, 'attacked_targets', None) or [])
        if allie is None or allie in cibles:
            return False
        return joueur is not None and allie.GetControlByPlayer() is joueur

    def poursuite(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Attachment)
        allie = this.GetBindFace()
        vilain = message.trigger.CastTo(Villain)
        if allie is None:
            return
        message.SetBeInstead(effect)
        vilain.BasicAttack(
            [allie], effect,
            property=AttackProperty(overkill=True),
            if_this_defeat_unit=lambda unite: Faces.RemoveAllFromGame([unite], effect),
        )

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_type=Ally, not_with_attach=CardFinder(name="Incessant Pursuit")),
            if_cannot_gain_surge=True,
        ),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            Villain,
            poursuite,
            conditions=[contre_moi],
        ),
    ]
```

#### `60072` * Lady Bullseye

```json
{
 "card_id": "60072",
 "type": "Minion",
 "name": "* Lady Bullseye",
 "subtitle": "",
 "desc": {
  "HP": "6",
  "ATK": "1",
  "SCH": "2",
  "Boost": "3",
  "Villainous": "1"
 },
 "traits": [
  "ASSASSIN",
  "HAND"
 ],
 "set_name": "Bullseye",
 "text": "Villainous.\n[star] <b>Forced Interrupt</b>: When resolving boost cards during Lady Bullseye's attack, if that attack is undefended, give her 1 additional boost card for this attack."
}
```

Script `src/cards/pack/fne/bullseye/60072.py` :

```python
from . import *
from game.card.face.attribute.can_boost import CanBoost

# * Lady Bullseye (ASSASSIN, HAND) — Villainous : base automatique.
# [star] Forced Interrupt: When resolving boost cards during Lady Bullseye's
#   attack, if that attack is undefended, give her 1 additional boost card
#   for this attack.
# « When resolving boost cards » = WhenBoostCardWouldTurnedFaceUp (envoye par
# ResolveBoostCards, defenseur connu) ; `boost_for_card="This"` borne a SES
# boosts ; une seule fois par attaque (drapeau sur le message d'attaque).

def GetAbilities() -> Sequence['Ability']:

    def sans_defense(effect: 'Effect', message: 'Message.WhenBoostCardWouldTurnedFaceUp') -> bool:
        attaque = message.would_atk_message
        if attaque is None or getattr(attaque, '_lady_bullseye_bonus', False):
            return False
        return getattr(message.being_message, 'defender', None) is None

    def bonus(effect: 'Effect', message: 'Message.WhenBoostCardWouldTurnedFaceUp') -> None:
        attaque = message.would_atk_message
        setattr(attaque, '_lady_bullseye_bonus', True)
        # Pas `GiveAdditionalBoostCardForThisActivation` : sur le message
        # d'attaque il enregistre une capacite Temp pour la PROCHAINE
        # activation (sender_damage.py:276), donc rien pour celle-ci. On pose
        # la carte face cachee tout de suite : la boucle de ResolveBoostCards
        # la retourne dans la foulee (meme primitive que sender_card.py:751).
        effect.this.CastTo(CanBoost).GiveFacedownBoostCardsInternal(1, effect, attaque)

    return [
        AbilityFactory.WhenBoostCardWouldTurnedFaceUp(
            AbilityType.ForcedInterrupt,
            bonus,
            while_attack=True,
            boost_for_card="This",
            conditions=[sans_defense],
        ),
    ]
```

#### `60073` Deranged Bloodlust

```json
{
 "card_id": "60073",
 "type": "SideScheme",
 "name": "Deranged Bloodlust",
 "subtitle": "",
 "desc": {
  "Boost": "1",
  "StartingThreat": "4",
  "Hazard": "1"
 },
 "traits": [],
 "set_name": "Bullseye",
 "text": "<b>When Revealed</b>: Place additional threat here equal to Bullseye's stage number.\n<hr />\n[star] <b>Boost</b>: After this activation, reveal this card."
}
```

Script `src/cards/pack/fne/bullseye/60073.py` :

```python
from . import *

# Deranged Bloodlust (side scheme, 4, aléa : base)
# When Revealed: Place additional threat here equal to Bullseye's stage number.
# [star] Boost: After this activation, reveal this card.
# Modeles : 01109 Bomb Scare (menace additionnelle), 07009 Escaped Convict
# (message.AfterThisActivation).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        bullseye = TrouverBullseye(effect)
        if bullseye:
            this.PlaceThreatOnSchemes([this], bullseye.printed_stage, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        joueur = message.GetToPlayer()
        message.AfterThisActivation(effect, lambda: this.Reveal(joueur, effect))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

#### `60074` Everything is a Weapon

```json
{
 "card_id": "60074",
 "type": "Treachery",
 "name": "Everything is a Weapon",
 "subtitle": "",
 "desc": {
  "Boost": "1"
 },
 "traits": [],
 "set_name": "Bullseye",
 "text": "<b>When Revealed (Alter-Ego)</b>: Take 2 indirect damage.\n<b>When Revealed (Hero)</b>: Choose: Either Bullseye activates against you, or remove an ally you control from the game.\n<hr />\n[star] <b>Boost</b>: If Bullseye is attacking, give him an additional boost card and this attack gains piercing."
}
```

Script `src/cards/pack/fne/bullseye/60074.py` :

```python
from . import *

# Everything is a Weapon
# When Revealed (Alter-Ego): Take 2 indirect damage.
# When Revealed (Hero): Choose: Either Bullseye activates against you, or
#   remove an ally you control from the game.
# [star] Boost: If Bullseye is attacking, give him an additional boost card
#   and this attack gains piercing.
# Modeles : 27080 (indirect), 08013 (ChooseAbilities a deux branches), 11041
# Deathunt (GiveBoostCardForThisActivation en contexte de boost).

def GetAbilities() -> Sequence['Ability']:

    def alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        message.GetToPlayer().GetIdentity().TakeIndirectDamage(this, 2, effect)

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        bullseye = TrouverBullseye(effect)

        def active(targets: Sequence['CardFace']) -> None:
            if bullseye:
                bullseye.DoActivate(joueur, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Bullseye activates against you", active),
            AbilityFactory.ForChoiceAbility(
                "Remove an ally you control from the game",
                lambda targets: Faces.RemoveAllFromGame(targets, effect),
            ).SetTarget("YourAlly"),
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        attaque = getattr(message, 'would_atk_message', None)
        if attaque is None:
            return
        message.GiveBoostCardForThisActivation(Enemy, 1, effect)
        attaque.GainPiercing(effect)

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", heros),
        AbilityFactory.WhenCardBecomeBoost(
            "This", boost,
            during_attack=True,
            activating_enemy=CardFinder(name="Bullseye"),
        ),
    ]
```

#### `60075` Unerring Desire

```json
{
 "card_id": "60075",
 "type": "Treachery",
 "name": "Unerring Desire",
 "subtitle": "",
 "desc": {
  "Boost": "3"
 },
 "traits": [],
 "set_name": "Bullseye",
 "text": "<b>When Revealed</b>: Choose to either give this card to the villain as a facedown boost card, or remove a [[Persona]] support you control from the game.\n<hr />\n[star] <b>Boost</b>: If this activation is an attack, it gains overkill."
}
```

Script `src/cards/pack/fne/bullseye/60075.py` :

```python
from . import *

# Unerring Desire
# When Revealed: Choose to either give this card to the villain as a facedown
#   boost card, or remove a PERSONA support you control from the game.
# [star] Boost: If this activation is an attack, it gains overkill.
# Modeles : 56091 (GiveBoostCard), an013 Hel-Wolf (GainOverKill en boost).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        vilain = Worlds.FindVillain(effect)

        def au_vilain(targets: Sequence['CardFace']) -> None:
            if vilain:
                vilain.GiveBoostCard(this, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Give this card to the villain as a facedown boost card", au_vilain),
            AbilityFactory.ForChoiceAbility(
                "Remove a Persona support you control from the game",
                lambda targets: Faces.RemoveAllFromGame(targets, effect),
            ).SetTarget(CardFinder(card_type=Support, trait="PERSONA"), from_where=["YouControlCards"]),
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.would_atk_message.GainOverKill(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost, during_attack=True),
    ]
```

### Set : Electro (10 cartes)

#### `60076` * Electro

```json
{
 "card_id": "60076",
 "type": "Villain",
 "name": "* Electro",
 "subtitle": "",
 "desc": {
  "HP": "15*",
  "ATK": "1",
  "SCH": "1",
  "Stage": "1"
 },
 "traits": [
  "CRIMINAL",
  "UNDERLING"
 ],
 "set_name": "Electro",
 "text": "<b>When Revealed</b>: Find Electric Charge, attach it to Electro, and place 2[per_hero] charge counters on it.\n[star] <b>Forced Response</b>: After Electro schemes, place 1 charge counter on Electric Charge."
}
```

Script `src/cards/pack/fne/electro/60076.py` :

```python
from . import *

# * Electro (60076) : voir CapacitesDElectro (charges par manigance = 1).

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDElectro(1, None),
    ]
```

#### `60077` * Electro

```json
{
 "card_id": "60077",
 "type": "Villain",
 "name": "* Electro",
 "subtitle": "",
 "desc": {
  "HP": "17*",
  "ATK": "2",
  "SCH": "1",
  "Stage": "2"
 },
 "traits": [
  "CRIMINAL",
  "UNDERLING"
 ],
 "set_name": "Electro",
 "text": "<b>When Revealed</b>: Find Electric Charge, attach it to Electro, and place 2[per_hero] charge counters on it.\n[star] <b>Forced Response</b>: After Electro schemes, place 1 charge counter on Electric Charge."
}
```

Script `src/cards/pack/fne/electro/60077.py` :

```python
from . import *

# * Electro (60077) : voir CapacitesDElectro (charges par manigance = 1).

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDElectro(1, None),
    ]
```

#### `60078` * Electro

```json
{
 "card_id": "60078",
 "type": "Villain",
 "name": "* Electro",
 "subtitle": "",
 "desc": {
  "HP": "20*",
  "ATK": "2",
  "SCH": "2",
  "Stage": "3",
  "Hazard": "1"
 },
 "traits": [
  "CRIMINAL",
  "UNDERLING"
 ],
 "set_name": "Electro",
 "text": "<b>When Revealed</b>: Place 3[per_hero] charge counters on Electric Charge.\n[star] <b>Forced Response</b>: After Electro schemes, place 2 charge counters on Electric Charge."
}
```

Script `src/cards/pack/fne/electro/60078.py` :

```python
from . import *

# * Electro (60078) : voir CapacitesDElectro (charges par manigance = 2, 3[per_hero] charges a la revelation, alea : base).

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDElectro(2, '3*'),
    ]
```

#### `60079` * Electric Charge

```json
{
 "card_id": "60079",
 "type": "Attachment",
 "name": "* Electric Charge",
 "subtitle": "",
 "desc": {
  "Permanent": "1"
 },
 "traits": [
  "CONDITION"
 ],
 "set_name": "Electro",
 "text": "Permanent.\n[star] <b>Forced Interrupt</b>: When Electro attacks, remove 1 charge counter from here → give Electro an additional boost card for this attack. This attack gains overkill.\n<b>Hero Action</b>: Spend a [energy] resource or 2 resources of any type → remove 1 charge counter from here."
}
```

Script `src/cards/pack/fne/electro/60079.py` :

```python
from . import *

# * Electric Charge (CONDITION) — Permanent. Attache a Electro.
# [star] Forced Interrupt: When Electro attacks, remove 1 charge counter from
#   here -> give Electro an additional boost card for this attack. This attack
#   gains overkill.  (CostFunc.Counter("This", 1, 'charge') = COUT, la fleche.)
# Hero Action: Spend a [energy] resource or 2 resources of any type -> remove
#   1 charge counter from here. (deux capacites, RECETTES §5 « or ».)

def GetAbilities() -> Sequence['Ability']:

    def decharge(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GiveAdditionalBoostCardForThisActivation(1, effect)
        message.GainOverKill(effect)

    def retirer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.RemoveCountersOn([this], 1, 'charge', effect)

    def a_des_charges(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        return effect.this.GetCounters('charge') > 0

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Electro")),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            CardFinder(name="Electro"),
            decharge,
        ).SetCostFunc(CostFunc.Counter("This", 1, 'charge')),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, retirer, conditions=[a_des_charges])
            .SetName("Spend [energy]: remove 1 charge counter").SetCost(Cost("Y")),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, retirer, conditions=[a_des_charges])
            .SetName("Spend 2 resources: remove 1 charge counter").SetCost(Cost("2")),
    ]
```

#### `60080` Drained of Power

```json
{
 "card_id": "60080",
 "type": "Attachment",
 "name": "Drained of Power",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "Uses": "3,drain"
 },
 "traits": [
  "CONDITION"
 ],
 "set_name": "Electro",
 "text": "Uses (3 drain counters).\n<b>When Revealed</b>: Attach to your identity and exhaust each upgrade you control.\n<b>Forced Interrupt</b>: When an upgrade you control would ready, you may spend a [energy] resource or 2 resources of any type. If you do, remove 1 drain counter from here <i>(and ready that upgrade)</i>. Otherwise, that upgrade does not ready."
}
```

Script `src/cards/pack/fne/electro/60080.py` :

```python
from . import *

# Drained of Power (CONDITION) — Uses (3 drain counters) : base desc.
# When Revealed: Attach to your identity and exhaust each upgrade you control.
# Forced Interrupt: When an upgrade you control would ready, you may spend a
#   [energy] resource or 2 resources of any type. If you do, remove 1 drain
#   counter from here (and ready that upgrade). Otherwise, that upgrade does
#   not ready.
# Modeles : 50153 (AttachToFaceWhenPutIntoPlay("YourIdentity")), WhenCardWouldReady
# (control_by="You") + SetBeInstead pour « does not ready », Otherwise.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        ameliorations = [f for f in Worlds.FindCardsOnField(effect, card_type=Upgrade) if f.GetControlByPlayer() is joueur]
        if ameliorations:
            Faces.ExhaustAll(ameliorations, effect)

    def redressement(effect: 'Effect', message: 'Message.WhenCardWouldReady') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.trigger.GetControlByPlayer()
        if joueur is None:
            return

        def payer() -> None:
            Faces.RemoveCountersOn([this], 1, 'drain', effect)

        def sinon(targets: Sequence['CardFace']) -> None:
            message.SetBeInstead(effect)

        joueur.ChooseAbilities(
            effect,
            *ChoixPayerEnergieOuDeux(joueur, effect, "ready that upgrade", payer),
            AbilityFactory.Otherwise(sinon),
        )

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardWouldReady(
            AbilityType.ForcedInterrupt,
            CardFinder(card_type=Upgrade),
            redressement,
            control_by="You",
        ),
    ]
```

#### `60081` * Whiplash

```json
{
 "card_id": "60081",
 "type": "Minion",
 "name": "* Whiplash",
 "subtitle": "",
 "desc": {
  "HP": "5",
  "ATK": "2",
  "SCH": "2",
  "Boost": "3"
 },
 "traits": [
  "CRIMINAL"
 ],
 "set_name": "Electro",
 "text": "<b>Forced Interrupt</b>: When Whiplash is attacked, remove 1 charge counter from Electric Charge → discard the top card of the encounter deck. Deal 1 damage to the attacker for each boost icon ([boost]) on the discarded card."
}
```

Script `src/cards/pack/fne/electro/60081.py` :

```python
from . import *

# * Whiplash (CRIMINAL)
# Forced Interrupt: When Whiplash is attacked, remove 1 charge counter from
#   Electric Charge -> discard the top card of the encounter deck. Deal 1
#   damage to the attacker for each boost icon on the discarded card.
# Le retrait de charge est un COUT (la fleche) : CostFunc.Counter sur
# Electric Charge. `message.trigger` = l'attaquant (WhenUnitWouldAttack).
# Icones : FacesCounter.CountTotalBoostIcons (chiffrees ; « each boost icon »).

def GetAbilities() -> Sequence['Ability']:

    def contre_coup(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)
        face = Worlds.DiscardEncounterTopCard(effect)
        if face is None:
            return
        n = FacesCounter.CountTotalBoostIcons([face])
        if n > 0:
            this.DealDamage([message.trigger], n, effect)

    return [
        AbilityFactory.WhenUnitWouldBeAttacked(
            AbilityType.ForcedInterrupt,
            "This",
            contre_coup,
        ).SetCostFunc(CostFunc.Counter(CardFinder(name="Electric Charge"), 1, 'charge')),
    ]
```

#### `60082` Charging Up

```json
{
 "card_id": "60082",
 "type": "SideScheme",
 "name": "Charging Up",
 "subtitle": "",
 "desc": {
  "Boost": "3",
  "StartingThreat": "6",
  "Hazard": "1"
 },
 "traits": [],
 "set_name": "Electro",
 "text": "<b>When Defeated</b>: Place 3 charge counters on Electric Charge."
}
```

Script `src/cards/pack/fne/electro/60082.py` :

```python
from . import *

# Charging Up (side scheme, 6, alea : base)
# When Defeated: Place 3 charge counters on Electric Charge.

def GetAbilities() -> Sequence['Ability']:

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        PoserCharges(effect, 3)

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
```

#### `60083` Chain Lightning

```json
{
 "card_id": "60083",
 "type": "Treachery",
 "name": "Chain Lightning",
 "subtitle": "",
 "desc": {
  "Boost": "1"
 },
 "traits": [],
 "set_name": "Electro",
 "text": "<b>When Revealed</b>: For each character you control, choose:\n• Exhaust that character.\n• Deal 1 damage to that character <i>(3 damage instead if there are any charge counters on Electric Charge)</i>. Remove 1 charge counter from Electric Charge."
}
```

Script `src/cards/pack/fne/electro/60083.py` :

```python
from . import *

# Chain Lightning
# When Revealed: For each character you control, choose:
#   - Exhaust that character.
#   - Deal 1 damage to that character (3 damage instead if there are any charge
#     counters on Electric Charge). Remove 1 charge counter from Electric Charge.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        for personnage in list(joueur.GetControlCharacters()):
            if not personnage.IsInPlay():
                continue

            def frapper(targets: Sequence['CardFace'], cible=personnage) -> None:
                degats = 3 if Charges(effect) > 0 else 1
                this.DealDamage([cible], degats, effect)
                RetirerCharges(effect, 1)

            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(f"Exhaust {personnage.name}", lambda targets, cible=personnage: Faces.ExhaustAll([cible], effect)),
                AbilityFactory.ForChoiceAbility(f"Deal damage to {personnage.name}", frapper),
            )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
```

#### `60084` Energy Overload

```json
{
 "card_id": "60084",
 "type": "Treachery",
 "name": "Energy Overload",
 "subtitle": "",
 "desc": {
  "Boost": "2"
 },
 "traits": [],
 "set_name": "Electro",
 "text": "<b>When Revealed</b>: If you have no cards with a printed [energy] resource in your hand, this card gains surge. Otherwise, for each card with a printed [energy] resource in your hand, choose:\n• Discard that card.\n• Stun a character you control."
}
```

Script `src/cards/pack/fne/electro/60084.py` :

```python
from . import *

# Energy Overload
# When Revealed: If you have no cards with a printed [energy] resource in your
#   hand, this card gains surge. Otherwise, for each card with a printed
#   [energy] resource in your hand, choose:
#   - Discard that card.  - Stun a character you control.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        energies = [f for f in joueur.hand_cards.Get() if ClassCard.IsType(f) and f.printed_resource.HasColorPrinted("Y")]
        if not energies:
            ThisCardGainSurge(effect)
            return
        for carte in energies:
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(f"Discard {carte.name}", lambda targets, c=carte: Faces.DiscardAll([c], effect)),
                AbilityFactory.ForChoiceAbility(
                    "Stun a character you control",
                    lambda targets: Faces.GiveStatus(targets, "Stunned", effect),
                ).SetTarget("YouControlUnit", canbe_stunned=True),
            )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
```

#### `60085` Shocking Revelation

```json
{
 "card_id": "60085",
 "type": "Treachery",
 "name": "Shocking Revelation",
 "subtitle": "",
 "desc": {
  "Boost": "2"
 },
 "traits": [],
 "set_name": "Electro",
 "text": "<b>When Revealed</b>: Discard the top card of your deck for each card you control. For each card with a printed [energy] resource discarded this way, choose:\n• Take 1 indirect damage.\n• Place 1 charge counter on Electric Charge."
}
```

Script `src/cards/pack/fne/electro/60085.py` :

```python
from . import *

# Shocking Revelation
# When Revealed: Discard the top card of your deck for each card you control.
#   For each card with a printed [energy] resource discarded this way, choose:
#   - Take 1 indirect damage.  - Place 1 charge counter on Electric Charge.
# « each card you control » : tout ce qui est en jeu sous ton controle,
# identite comprise.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        # GetControlByOrOwner : `GetControlByPlayer` leve un assert sur les cartes
        # du scenario (lecon si012, 18/09/2026).
        n = len([f for f in Worlds.FindCardsOnField(effect) if f.GetControlByOrOwner() is joueur])
        if n <= 0:
            return
        defaussees = joueur.DiscardDeckTopCards(n, effect)
        for carte in defaussees:
            if not (ClassCard.IsType(carte) and carte.printed_resource.HasColorPrinted("Y")):
                continue
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility("Take 1 indirect damage", lambda targets: joueur.GetIdentity().TakeIndirectDamage(this, 1, effect)),
                AbilityFactory.ForChoiceAbility("Place 1 charge counter on Electric Charge", lambda targets: PoserCharges(effect, 1)),
            )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
```

### Set : Hammerhead (11 cartes)

#### `60086` * Hammerhead

```json
{
 "card_id": "60086",
 "type": "Villain",
 "name": "* Hammerhead",
 "subtitle": "",
 "desc": {
  "HP": "14*",
  "ATK": "1",
  "SCH": "2",
  "Stage": "1"
 },
 "traits": [
  "CRIMINAL",
  "MAGGIA",
  "UNDERLING"
 ],
 "set_name": "Hammerhead",
 "text": "[star] <b>Forced Response</b>: After Hammerhead attacks and damages a character, stun that character. If that character was already stunned, deal 1 damage to them."
}
```

Script `src/cards/pack/fne/hammerhead/60086.py` :

```python
from . import *

# * Hammerhead (60086) : [star] Forced Response, 1 degat(s) sur un personnage deja etourdi.
# Toughness / Retaliate sont des bases automatiques lues dans desc.

def GetAbilities() -> Sequence['Ability']:
    return [
        ReponseForceeCoupDeBoule(1),
    ]
```

#### `60087` * Hammerhead

```json
{
 "card_id": "60087",
 "type": "Villain",
 "name": "* Hammerhead",
 "subtitle": "",
 "desc": {
  "HP": "15*",
  "ATK": "2",
  "SCH": "2",
  "Toughness": "1",
  "Retaliate": "1",
  "Stage": "2"
 },
 "traits": [
  "CRIMINAL",
  "MAGGIA",
  "UNDERLING"
 ],
 "set_name": "Hammerhead",
 "text": "Toughness. Retaliate 1.\n[star] <b>Forced Response</b>: After Hammerhead attacks and damages a character, stun that character. If that character was already stunned, deal 1 damage to them."
}
```

Script `src/cards/pack/fne/hammerhead/60087.py` :

```python
from . import *

# * Hammerhead (60087) : [star] Forced Response, 1 degat(s) sur un personnage deja etourdi.
# Toughness / Retaliate sont des bases automatiques lues dans desc.

def GetAbilities() -> Sequence['Ability']:
    return [
        ReponseForceeCoupDeBoule(1),
    ]
```

#### `60088` * Hammerhead

```json
{
 "card_id": "60088",
 "type": "Villain",
 "name": "* Hammerhead",
 "subtitle": "",
 "desc": {
  "HP": "16*",
  "ATK": "3",
  "SCH": "3",
  "Toughness": "1",
  "Retaliate": "2",
  "Stage": "3"
 },
 "traits": [
  "CRIMINAL",
  "MAGGIA",
  "UNDERLING"
 ],
 "set_name": "Hammerhead",
 "text": "Toughness. Retaliate 2.\n[star] <b>Forced Response</b>: After Hammerhead attacks and damages a character, stun that character. If that character was already stunned, deal 2 damage to them."
}
```

Script `src/cards/pack/fne/hammerhead/60088.py` :

```python
from . import *

# * Hammerhead (60088) : [star] Forced Response, 2 degat(s) sur un personnage deja etourdi.
# Toughness / Retaliate sont des bases automatiques lues dans desc.

def GetAbilities() -> Sequence['Ability']:
    return [
        ReponseForceeCoupDeBoule(2),
    ]
```

#### `60089` Energy Gatling Gun

```json
{
 "card_id": "60089",
 "type": "Attachment",
 "name": "Energy Gatling Gun",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "ATK+": "1"
 },
 "traits": [
  "TECH"
 ],
 "set_name": "Hammerhead",
 "text": "Attach to Hammerhead.\n<b>Forced Response</b>: After Hammerhead attacks, if the attacked character was not defeated, discard this card → Hammerhead attacks that character again."
}
```

Script `src/cards/pack/fne/hammerhead/60089.py` :

```python
from . import *

# Energy Gatling Gun
# Attach to Hammerhead. (+1 ATK : cle desc "ATK+", base automatique.)
# Forced Response: After Hammerhead attacks, if the attacked character was not
#   defeated, discard this card -> Hammerhead attacks that character again.
#
# La fleche fait de la defausse un COUT (al014, 42030 : CostFunc.Discard("This")).
# « that character » : l'unite qui a subi l'attaque (defenseur ou identite).
# Un allie se re-attaque par BasicAttack([allie]) (modele 50096 Leaping Kick),
# une identite par DoAttackYou. La carte etant defaussee en cout, la seconde
# attaque ne peut pas relancer la reponse : pas de boucle.

def GetAbilities() -> Sequence['Ability']:

    def personnage_attaque(message: 'Message.AfterUnitAttackEnd') -> 'Unit2|None':
        cibles = [u for u in message.attacked_targets if u.IsInPlay() and not u.IsDefeated()]
        return cibles[0] if cibles else None

    def survivant(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        return personnage_attaque(message) is not None

    def re_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(this)
        hammerhead = TrouverHammerhead(effect)
        cible = personnage_attaque(message)
        if hammerhead is None or cible is None:
            return
        if Identity.IsType(cible):
            joueur = cible.GetControlByPlayer()
            hammerhead.DoAttackYou(joueur, effect)
        else:
            hammerhead.BasicAttack([cible], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name="Hammerhead")
        ),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            CardFinder(name="Hammerhead"),
            re_attaque,
            conditions=[survivant],
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
```

#### `60090` Hardheaded

```json
{
 "card_id": "60090",
 "type": "Attachment",
 "name": "Hardheaded",
 "subtitle": "",
 "desc": {
  "Boost": "1",
  "SCH+": "1"
 },
 "traits": [
  "CONDITION"
 ],
 "set_name": "Hammerhead",
 "text": "Attach to Hammerhead.\nHammerhead gains stalwart.\n<b>Hero Action</b>: Spend [energy] [mental] [physical] resources → discard this card.\n<hr />\n[star] <b>Boost</b>: Give the activating enemy a tough status card."
}
```

Script `src/cards/pack/fne/hammerhead/60090.py` :

```python
from . import *

# Hardheaded (CONDITION)
# Attach to Hammerhead. (+1 SCH : cle desc "SCH+", base automatique.)
# Hammerhead gains stalwart.
# Hero Action: Spend [energy] [mental] [physical] resources -> discard this card.
# [star] Boost: Give the activating enemy a tough status card.
#
# Modeles : 16064 Drang's Spear (stalwart attache + action a cout), 01118 Sonic
# Converter (Cost("YBR")), 52037 Growing Strong (boost -> tough a l'ennemi actif).

def GetAbilities() -> Sequence['Ability']:

    def robuste(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Faces.GiveStatus([message.activating_enemy], "Tough", effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name="Hammerhead")
        ),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Hammerhead"),
            stalwart=1,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("YBR")),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            robuste,
        ),
    ]
```

#### `60091` * Chameleon

```json
{
 "card_id": "60091",
 "type": "Minion",
 "name": "* Chameleon",
 "subtitle": "",
 "desc": {
  "HP": "5",
  "ATK": "1",
  "SCH": "1",
  "Boost": "3"
 },
 "traits": [
  "CRIMINAL",
  "MAGGIA"
 ],
 "set_name": "Hammerhead",
 "text": "[star] Chameleon gets +X SCH, where X is the highest THW value among characters in play.\n<b>When Revealed</b>: Chameleon schemes."
}
```

Script `src/cards/pack/fne/hammerhead/60091.py` :

```python
from . import *

# * Chameleon (CRIMINAL, MAGGIA)
# [star] Chameleon gets +X SCH, where X is the highest THW value among
#   characters in play.
# When Revealed: Chameleon schemes.
#
# Modeles : 27067 Sand Clone (ThisGainKeyword avec fonction de valeur),
# 32117 Master Mold's Children (DoSchemes). Le THW n'existe que sur les
# personnages amis (heros, allies) : un alter-ego ou un ennemi vaut 0. La
# valeur se recalcule a chaque entree/sortie d'un personnage ami en jeu et a
# chaque changement de forme (OnEvent.Form ecoute aussi Enter/LeavePlay).
# ⚠ `OnEvent.Form` refuse une UNION de types (AttributeError 'UnionType' has
# no attribute 'IsType') : on passe la classe mere Friend (identites + allies).

def GetAbilities() -> Sequence['Ability']:

    def plus_haut_thw(effect: 'Effect', ui: List['CardFace']) -> int:
        meilleur = 0
        for unite in Worlds.GetOnFieldFriendlyCharacters(effect):
            if HasThwart.IsType(unite):
                meilleur = max(meilleur, unite.thwart)
        return meilleur

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        this.DoSchemes(message.GetToPlayer(), effect)

    return [
        AbilityFactory.ThisGainKeyword(
            plus_haut_thw,
            scheme=1,
            change_on_event=OnEvent.Form(Friend),
        ),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
```

#### `60092` Maggia Enforcers

```json
{
 "card_id": "60092",
 "type": "Minion",
 "name": "Maggia Enforcers",
 "subtitle": "",
 "desc": {
  "HP": "3",
  "ATK": "2",
  "SCH": "0",
  "Boost": "0",
  "Guard": "1"
 },
 "traits": [
  "CRIMINAL",
  "MAGGIA"
 ],
 "set_name": "Hammerhead",
 "text": "Guard.\n[star] Maggia Enforcers's SCH is equal to the number of [[Maggia]] enemies in play <i>(including this one)</i>."
}
```

Script `src/cards/pack/fne/hammerhead/60092.py` :

```python
from . import *

# Maggia Enforcers (CRIMINAL, MAGGIA) — Guard : base automatique.
# [star] Maggia Enforcers's SCH is equal to the number of MAGGIA enemies in
#   play (including this one).
#
# SCH imprime = 0 (etoile), +1 par ennemi MAGGIA en jeu, lui compris. Modele :
# 24016 Mandrill (ThisGainKeywordForEachFaceInPlay), rafraichi par defaut a
# chaque entree/sortie d'une carte du filtre (OnEvent.CardInPlay).

def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.ThisGainKeywordForEachFaceInPlay(
            CardFinder(trait="MAGGIA", card_type=Enemy),
            scheme=1,
        ),
    ]
```

#### `60093` Maggia Underboss

```json
{
 "card_id": "60093",
 "type": "Minion",
 "name": "Maggia Underboss",
 "subtitle": "",
 "desc": {
  "HP": "4",
  "ATK": "1",
  "SCH": "1",
  "Boost": "1",
  "Villainous": "1"
 },
 "traits": [
  "CRIMINAL",
  "MAGGIA"
 ],
 "set_name": "Hammerhead",
 "text": "Villainous.\n[star] <b>Forced Interrupt</b>: When Maggia Underboss activates against you, if you are stunned, give it an additional boost card for this activation."
}
```

Script `src/cards/pack/fne/hammerhead/60093.py` :

```python
from . import *

# Maggia Underboss (Villainous : base automatique)
# [star] Forced Interrupt: When Maggia Underboss activates against you, if you
#   are stunned, give it an additional boost card for this activation.
#
# Modele : 02020 Hysteria (WhenUnitWouldAttack + WhenUnitWouldScheme, meme
# handler, GiveAdditionalBoostCardForThisActivation). « you are stunned » = ton
# identite porte le statut, teste dans `conditions` (un filtre ne va jamais
# dans le corps, RECETTES §1).

def GetAbilities() -> Sequence['Ability']:

    def joueur_etourdi(effect: 'Effect', message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldScheme') -> bool:
        joueur = message.GetAgainstPlayer()
        return joueur is not None and joueur.GetIdentity().IsStunned()

    def boost_en_plus(effect: 'Effect', message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldScheme') -> None:
        message.GiveAdditionalBoostCardForThisActivation(1, effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            "This",
            boost_en_plus,
            conditions=[joueur_etourdi],
        ),
        AbilityFactory.WhenUnitWouldScheme(
            AbilityType.ForcedInterrupt,
            "This",
            boost_en_plus,
            conditions=[joueur_etourdi],
        ),
    ]
```

#### `60094` Consolidate Power

```json
{
 "card_id": "60094",
 "type": "SideScheme",
 "name": "Consolidate Power",
 "subtitle": "",
 "desc": {
  "Boost": "1",
  "StartingThreat": "6"
 },
 "traits": [],
 "set_name": "Hammerhead",
 "text": "<b>Forced Response</b>: After a minion is defeated, give it to the villain as a facedown boost card."
}
```

Script `src/cards/pack/fne/hammerhead/60094.py` :

```python
from . import *

# Consolidate Power (side scheme)
# Forced Response: After a minion is defeated, give it to the villain as a
#   facedown boost card.
#
# Modele : 56091 Dangerous Recruits (GiveBoostCard sur le leader ennemi) ; ici
# le vilain actif (Worlds.FindVillain). Le texte dit Forced RESPONSE, on
# s'accroche donc a AfterUnitBeDefeated et non a l'interruption du modele.

def GetAbilities() -> Sequence['Ability']:

    def au_vilain(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        vilain = Worlds.FindVillain(effect)
        if vilain:
            vilain.GiveBoostCard(message.trigger, effect)

    return [
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.ForcedResponse,
            Minion,
            au_vilain,
        ),
    ]
```

#### `60095` Power Struggle

```json
{
 "card_id": "60095",
 "type": "SideScheme",
 "name": "Power Struggle",
 "subtitle": "",
 "desc": {
  "Boost": "1",
  "StartingThreat": "5",
  "Amplify": "1"
 },
 "traits": [],
 "set_name": "Hammerhead",
 "text": "<b>When Revealed</b>: Defeat the minion with the fewest remaining hit points in play. Discard cards from the encounter deck until you discard a minion. Reveal that minion."
}
```

Script `src/cards/pack/fne/hammerhead/60095.py` :

```python
from . import *

# Power Struggle (side scheme, Amplify 1 : base automatique lue dans desc)
# When Revealed: Defeat the minion with the fewest remaining hit points in
#   play. Discard cards from the encounter deck until you discard a minion.
#   Reveal that minion.
#
# Modeles : 24023 Out for Blood (Filter.One fewest_remaining_hp), 01116b
# Underground Distribution (DiscardEncounterCardsUntil), 01095 Rhino (Reveal).
# Sans sbire en jeu, la premiere phrase ne fait rien et la suite se resout.

def GetAbilities() -> Sequence['Ability']:

    def lutte(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        joueur = message.GetToPlayer()
        sbire = Filter.One(Worlds.GetOnFieldMinions(effect), effect, fewest_remaining_hp=True)
        if sbire:
            Faces.DefeatUnits([sbire], this, effect)
        face = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
        if face:
            face.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            lutte,
        ),
    ]
```

#### `60096` "Head First!"

```json
{
 "card_id": "60096",
 "type": "Treachery",
 "name": "\"Head First!\"",
 "subtitle": "",
 "desc": {
  "Boost": "2"
 },
 "traits": [],
 "set_name": "Hammerhead",
 "text": "<b>When Revealed (Alter-Ego)</b>: This card gains surge.\n<b>When Revealed (Hero)</b>: Hammerhead attacks you. If you are stunned, Hammerhead gets +2 ATK for this attack and this attack gains overkill."
}
```

Script `src/cards/pack/fne/hammerhead/60096.py` :

```python
from . import *

# "Head First!"
# When Revealed (Alter-Ego): This card gains surge.
# When Revealed (Hero): Hammerhead attacks you. If you are stunned, Hammerhead
#   gets +2 ATK for this attack and this attack gains overkill.
#
# Modele : 04086 Swinging Stone (AttackProperty(additional_value=...)), 01106
# Stampede (surge en alter-ego). L'overkill se declare dans la meme propriete.

def GetAbilities() -> Sequence['Ability']:

    def tete_la_premiere(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        hammerhead = TrouverHammerhead(effect)
        if hammerhead is None:
            return
        if joueur.GetIdentity().IsStunned():
            propriete = AttackProperty(additional_value=2, overkill=True)
        else:
            propriete = AttackProperty()
        hammerhead.DoAttackYou(joueur, effect, property=propriete)

    return [
        AbilityFactory.WhenThisRevealed(
            "Alter-Ego",
            ThisCardGainSurge,
        ),
        AbilityFactory.WhenThisRevealed(
            "Hero",
            tete_la_premiere,
        ),
    ]
```

### Set : Purple Man (13 cartes)

#### `60097` * Purple Man

```json
{
 "card_id": "60097",
 "type": "Villain",
 "name": "* Purple Man",
 "subtitle": "",
 "desc": {
  "HP": "13*",
  "ATK": "0",
  "SCH": "1",
  "Stage": "1"
 },
 "traits": [
  "PSIONIC",
  "UNDERLING"
 ],
 "set_name": "Purple Man",
 "text": "Each [[Influenced]] minion gains guard.\nEach boost card from the Purple Man encounter set gains: \"[star] <b>Boost</b>: After this activation, deal this card to yourself as a facedown encounter card.\""
}
```

Script `src/cards/pack/fne/purple_man/60097.py` :

```python
from . import *

# * Purple Man (60097) : voir CapacitesDePurpleMan (guard=True, villainous=False, patrol=False).

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDePurpleMan(guard=True, villainous=False, patrol=False),
    ]
```

#### `60098` * Purple Man

```json
{
 "card_id": "60098",
 "type": "Villain",
 "name": "* Purple Man",
 "subtitle": "",
 "desc": {
  "HP": "15*",
  "ATK": "1",
  "SCH": "2",
  "Stage": "2"
 },
 "traits": [
  "PSIONIC",
  "UNDERLING"
 ],
 "set_name": "Purple Man",
 "text": "Each [[Influenced]] minion gains guard and villainous.\nEach boost card from the Purple Man encounter set gains: \"[star] <b>Boost</b>: After this activation, deal this card to yourself as a facedown encounter card.\""
}
```

Script `src/cards/pack/fne/purple_man/60098.py` :

```python
from . import *

# * Purple Man (60098) : voir CapacitesDePurpleMan (guard=True, villainous=True, patrol=False).

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDePurpleMan(guard=True, villainous=True, patrol=False),
    ]
```

#### `60099` * Purple Man

```json
{
 "card_id": "60099",
 "type": "Villain",
 "name": "* Purple Man",
 "subtitle": "",
 "desc": {
  "HP": "17*",
  "ATK": "1",
  "SCH": "3",
  "Stage": "3"
 },
 "traits": [
  "PSIONIC",
  "UNDERLING"
 ],
 "set_name": "Purple Man",
 "text": "Each [[Influenced]] minion gains guard, patrol, and villainous.\nEach boost card from the Purple Man encounter set gains: \"[star] <b>Boost</b>: After this activation, deal this card to yourself as a facedown encounter card.\""
}
```

Script `src/cards/pack/fne/purple_man/60099.py` :

```python
from . import *

# * Purple Man (60099) : voir CapacitesDePurpleMan (guard=True, villainous=True, patrol=True).

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDePurpleMan(guard=True, villainous=True, patrol=True),
    ]
```

#### `60100` Converted

```json
{
 "card_id": "60100",
 "type": "Attachment",
 "name": "Converted",
 "subtitle": "",
 "desc": {
  "Boost": "3"
 },
 "traits": [
  "CONDITION"
 ],
 "set_name": "Purple Man",
 "text": "Treat attached ally as an [[Influenced]] minion with a blank text box. Attached minion's SCH is equal to its base THW and it does not take consequential damage.\n<b>When Revealed</b>: Attach to the highest-cost ally you control and engage it. Otherwise, this card gains surge."
}
```

Script `src/cards/pack/fne/purple_man/60100.py` :

```python
from . import *

# Converted (CONDITION)
# Treat attached ally as an INFLUENCED minion with a blank text box. Attached
#   minion's SCH is equal to its base THW and it does not take consequential
#   damage.
# When Revealed: Attach to the highest-cost ally you control and engage it.
#   Otherwise, this card gains surge.
# Modele exact : 21178 Beguiled (TreatAttachedCardAsMinion sur le gabarit
# « Influenced Minion », qui porte le trait et un texte vide ; la fabrique
# copie ATK et pose SCH = THW imprime, sans degats consecutifs).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        allies = [a for a in Worlds.GetOnFieldAllies(effect) if a.GetControlByPlayer() is joueur]
        allie = Filter.One(allies, effect, highest_cost=True)
        if allie:
            this.AttachTo2(allie, effect)
        else:
            ThisCardGainSurge(effect)

    def engager(minion: 'Minion', face: 'CardFace', effect: 'Effect') -> None:
        joueur = face.GetControlByPlayer()
        if joueur is not None:
            minion.EngagePlayer(joueur, effect)

    return [
        AbilityFactory.TreatAttachedCardAsMinion(Ally, "Influenced Minion", engager),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
```

#### `60101` Firefighter

```json
{
 "card_id": "60101",
 "type": "Minion",
 "name": "Firefighter",
 "subtitle": "",
 "desc": {
  "HP": "3",
  "ATK": "1",
  "SCH": "1",
  "Boost": "0",
  "Vulnerable": "1"
 },
 "traits": [
  "CIVILIAN",
  "INFLUENCED"
 ],
 "set_name": "Purple Man",
 "text": "Vulnerable.\n[star] Firefighter's attacks gain piercing.\n<b>When Defeated</b>: Discard the highest-cost support or upgrade from play."
}
```

Script `src/cards/pack/fne/purple_man/60101.py` :

```python
from . import *

# Firefighter (CIVILIAN, INFLUENCED) — Vulnerable : base.
# [star] Firefighter's attacks gain piercing.
# When Defeated: Discard the highest-cost support or upgrade from play.

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        cartes = Worlds.FindCardsOnField(effect, card_type=Support|Upgrade)
        cible = Filter.One(cartes, effect, highest_cost=True)
        if cible:
            Faces.DiscardAll([cible], effect)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", piercing=True),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
```

#### `60102` Judge

```json
{
 "card_id": "60102",
 "type": "Minion",
 "name": "Judge",
 "subtitle": "",
 "desc": {
  "HP": "2",
  "ATK": "0",
  "SCH": "3",
  "Boost": "2",
  "Vulnerable": "1"
 },
 "traits": [
  "CIVILIAN",
  "INFLUENCED"
 ],
 "set_name": "Purple Man",
 "text": "Vulnerable.\n<b>When Defeated</b>: Place 3 threat on the main scheme."
}
```

Script `src/cards/pack/fne/purple_man/60102.py` :

```python
from . import *

# Judge (CIVILIAN, INFLUENCED) — Vulnerable : base.
# When Defeated: Place 3 threat on the main scheme.

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        this.PlaceThreatOnSchemes("MainScheme", 3, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
```

#### `60103` Security Guard

```json
{
 "card_id": "60103",
 "type": "Minion",
 "name": "Security Guard",
 "subtitle": "",
 "desc": {
  "HP": "4",
  "ATK": "2",
  "SCH": "0",
  "Boost": "1",
  "Patrol": "1",
  "Vulnerable": "1"
 },
 "traits": [
  "CIVILIAN",
  "INFLUENCED"
 ],
 "set_name": "Purple Man",
 "text": "Patrol. Vulnerable.\n<b>When Defeated</b>: Discard the ally with the highest ATK <i>(among allies)</i> in play."
}
```

Script `src/cards/pack/fne/purple_man/60103.py` :

```python
from . import *

# Security Guard (CIVILIAN, INFLUENCED) — Patrol, Vulnerable : bases.
# When Defeated: Discard the ally with the highest ATK (among allies) in play.

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        allie = Filter.One(Worlds.GetOnFieldAllies(effect), effect, highest_atk=True)
        if allie:
            Faces.DiscardAll([allie], effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
```

#### `60104` Skater Punk

```json
{
 "card_id": "60104",
 "type": "Minion",
 "name": "Skater Punk",
 "subtitle": "",
 "desc": {
  "HP": "2",
  "ATK": "2",
  "SCH": "1",
  "Boost": "0",
  "Vulnerable": "1"
 },
 "traits": [
  "CIVILIAN",
  "INFLUENCED"
 ],
 "set_name": "Purple Man",
 "text": "Vulnerable.\n<b>When Defeated</b>: Deal 3 damage to the defeating player's identity."
}
```

Script `src/cards/pack/fne/purple_man/60104.py` :

```python
from . import *

# Skater Punk (CIVILIAN, INFLUENCED) — Vulnerable : base.
# When Defeated: Deal 3 damage to the defeating player's identity.

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetDefeatingPlayer()
        if joueur is not None:
            this.DealDamage([joueur.GetIdentity()], 3, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
```

#### `60105` "Fight."

```json
{
 "card_id": "60105",
 "type": "Obligation",
 "name": "\"Fight.\"",
 "subtitle": "",
 "desc": {
  "Boost": "1",
  "Uses": "3,command"
 },
 "traits": [],
 "set_name": "Purple Man",
 "text": "Uses (3 command counters).\n<b>Forced Action</b>: Exhaust this card and remove 1 command counter from it → deal 2 damage to a hero or ally."
}
```

Script `src/cards/pack/fne/purple_man/60105.py` :

```python
from . import *

# "Fight." (obligation, Uses 3 command) — Forced Action: Exhaust this card and
# remove 1 command counter from it -> deal 2 damage to a hero or ally.

def GetAbilities() -> Sequence['Ability']:

    def frapper(effect: 'Effect', joueur: 'Player', this: 'Obligation') -> None:
        this.DealDamage(effect.targets, 2, effect)

    return [
        ObligationCommandee("Fight.", frapper)[0].SetTarget(CardFinder(card_type=Hero|Ally)),
    ]
```

#### `60106` "Protect."

```json
{
 "card_id": "60106",
 "type": "Obligation",
 "name": "\"Protect.\"",
 "subtitle": "",
 "desc": {
  "Boost": "1",
  "Uses": "3,command"
 },
 "traits": [],
 "set_name": "Purple Man",
 "text": "Uses (3 command counters).\n<b>Forced Action</b>: Exhaust this card and remove 1 command counter from it → give the villain a tough status card."
}
```

Script `src/cards/pack/fne/purple_man/60106.py` :

```python
from . import *

# "Protect." (obligation, Uses 3 command) — Forced Action: ... -> give the
# villain a tough status card.

def GetAbilities() -> Sequence['Ability']:

    def proteger(effect: 'Effect', joueur: 'Player', this: 'Obligation') -> None:
        vilain = Worlds.FindVillain(effect)
        if vilain:
            Faces.GiveStatus([vilain], "Tough", effect)

    return [
        *ObligationCommandee("Protect.", proteger),
    ]
```

#### `60107` "Serve."

```json
{
 "card_id": "60107",
 "type": "Obligation",
 "name": "\"Serve.\"",
 "subtitle": "",
 "desc": {
  "Boost": "1",
  "Uses": "3,command"
 },
 "traits": [],
 "set_name": "Purple Man",
 "text": "Uses (3 command counters).\n<b>Forced Action</b>: Exhaust this card and remove 1 command counter from it → place 2 threat on the main scheme."
}
```

Script `src/cards/pack/fne/purple_man/60107.py` :

```python
from . import *

# "Serve." (obligation, Uses 3 command) — Forced Action: ... -> place 2
# threat on the main scheme.

def GetAbilities() -> Sequence['Ability']:

    def servir(effect: 'Effect', joueur: 'Player', this: 'Obligation') -> None:
        this.PlaceThreatOnSchemes("MainScheme", 2, effect)

    return [
        *ObligationCommandee("Serve.", servir),
    ]
```

#### `60108` Power of Suggestion

```json
{
 "card_id": "60108",
 "type": "SideScheme",
 "name": "Power of Suggestion",
 "subtitle": "",
 "desc": {
  "Boost": "3",
  "StartingThreat": "2",
  "Hinder": "3*",
  "Hazard": "1"
 },
 "traits": [],
 "set_name": "Purple Man",
 "text": "[star] Hinder 3[per_hero].\nEach minion gains the [[Influenced]] trait."
}
```

Script `src/cards/pack/fne/purple_man/60108.py` :

```python
from . import *

# Power of Suggestion (side scheme 2) — [star] Hinder 3[per_hero] et alea : bases desc.
# Each minion gains the INFLUENCED trait.

def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Minion),
            trait="INFLUENCED",
        ),
    ]
```

#### `60109` Sway the Masses

```json
{
 "card_id": "60109",
 "type": "Treachery",
 "name": "Sway the Masses",
 "subtitle": "",
 "desc": {
  "Boost": "2"
 },
 "traits": [],
 "set_name": "Purple Man",
 "text": "<b>When Revealed</b>: Choose an [[Influenced]] minion from the encounter discard pile and reveal it. Otherwise, this card gains surge."
}
```

Script `src/cards/pack/fne/purple_man/60109.py` :

```python
from . import *

# Sway the Masses
# When Revealed: Choose an INFLUENCED minion from the encounter discard pile
#   and reveal it. Otherwise, this card gains surge.
# Search.SearchForCard limite a la DEFAUSSE de rencontre (01095 fouille deck
# + defausse ; ici seulement la defausse).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        face = Search.SearchForCard(
            effect, joueur,
            include_encounter_discard_pile=True,
            trait="INFLUENCED", card_type=Minion,
        )
        if face:
            face.Reveal(joueur, effect)
        else:
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
```

### Set : Typhoid Mary (14 cartes)

#### `60110a` * Typhoid Mary

```json
{
 "card_id": "60110a",
 "type": "Villain",
 "name": "* Typhoid Mary",
 "subtitle": "",
 "desc": {
  "HP": "10*",
  "ATK": "1",
  "SCH": "2",
  "Stage": "A"
 },
 "traits": [
  "MUTANT",
  "PSIONIC",
  "UNDERLING"
 ],
 "set_name": "Typhoid Mary",
 "text": "<b>Forced Interrupt</b>: When Typhoid Mary would be defeated, place 1 damage token on Disturbed Psyche instead and reset her hit points to 10[per_hero]."
}
```

Script `src/cards/pack/fne/typhoid_mary/60110a.py` :

```python
from . import *

# * Typhoid Mary (A) — SCH 2 / ATK 1 / 10[per_hero]. Voir CapacitesDeMary.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDeMary("10*")]
```

#### `60110b` * Bloody Mary

```json
{
 "card_id": "60110b",
 "type": "Villain",
 "name": "* Bloody Mary",
 "subtitle": "",
 "desc": {
  "HP": "10*",
  "ATK": "2",
  "SCH": "1",
  "Stage": "A"
 },
 "traits": [
  "MUTANT",
  "PSIONIC",
  "UNDERLING"
 ],
 "set_name": "Typhoid Mary",
 "text": "<b>Forced Interrupt</b>: When Bloody Mary would be defeated, place 1 damage token on Disturbed Psyche instead and reset her hit points to 10[per_hero]."
}
```

Script `src/cards/pack/fne/typhoid_mary/60110b.py` :

```python
from . import *

# * Bloody Mary (A) — SCH 1 / ATK 2 / 10[per_hero]. Voir CapacitesDeMary.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDeMary("10*")]
```

#### `60111a` * Typhoid Mary

```json
{
 "card_id": "60111a",
 "type": "Villain",
 "name": "* Typhoid Mary",
 "subtitle": "",
 "desc": {
  "HP": "13*",
  "ATK": "1",
  "SCH": "3",
  "Toughness": "1",
  "Stage": "B"
 },
 "traits": [
  "MUTANT",
  "PSIONIC",
  "UNDERLING"
 ],
 "set_name": "Typhoid Mary",
 "text": "Toughness.\n<b>Forced Interrupt</b>: When Typhoid Mary would be defeated, place 1 damage token on Disturbed Psyche instead and reset her hit points to 13[per_hero]."
}
```

Script `src/cards/pack/fne/typhoid_mary/60111a.py` :

```python
from . import *

# * Typhoid Mary (B) — SCH 3 / ATK 1 / 13[per_hero], Toughness (base).

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDeMary("13*")]
```

#### `60111b` * Bloody Mary

```json
{
 "card_id": "60111b",
 "type": "Villain",
 "name": "* Bloody Mary",
 "subtitle": "",
 "desc": {
  "HP": "13*",
  "ATK": "3",
  "SCH": "1",
  "Stage": "B"
 },
 "traits": [
  "MUTANT",
  "PSIONIC",
  "UNDERLING"
 ],
 "set_name": "Typhoid Mary",
 "text": "<b>When Revealed</b>: Deal 1 damage to each identity.\n<b>Forced Interrupt</b>: When Bloody Mary would be defeated, place 1 damage token on Disturbed Psyche instead and reset her hit points to 13[per_hero]."
}
```

Script `src/cards/pack/fne/typhoid_mary/60111b.py` :

```python
from . import *

# * Bloody Mary (B) — SCH 1 / ATK 3 / 13[per_hero].
# When Revealed: Deal 1 damage to each identity. (La FAQ du livret : le When
# Revealed de la face qui apparait se resout aussi au retournement.)

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterVillain)
        identites = [j.GetIdentity() for j in effect.world.const_players if j.GetIdentity() is not None]
        if identites:
            this.DealDamage(identites, 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        *CapacitesDeMary("13*"),
    ]
```

#### `60112` Disturbed Psyche

```json
{
 "card_id": "60112",
 "type": "Environment",
 "name": "Disturbed Psyche",
 "subtitle": "",
 "desc": {
  "Setup": "1"
 },
 "traits": [],
 "set_name": "Typhoid Mary",
 "text": "Setup.\n<b>Setup</b>: Put the villain into play on a random side <i>(and reveal it)</i>.\n<b>Forced Interrupt</b>: When the villain phase ends, flip the villain.\n<b>If there are 3 or more tokens here, the players win the game!</b>"
}
```

Script `src/cards/pack/fne/typhoid_mary/60112.py` :

```python
from . import *

# Disturbed Psyche (environment) — Setup (base desc : commence en jeu).
# Setup: Put the villain into play on a random side (and reveal it).
# Forced Interrupt: When the villain phase ends, flip the villain.
# If there are 3 or more tokens here, the players win the game!
#
# Le scenario met deja le vilain en jeu (stade unique 60110a / 60111a) : le
# Setup se contente de le retourner une fois sur deux (Rand), la revelation
# etant celle de la mise en place. ⚠ Hors de portee du harnais (WhenGameWouldBegin
# part une fois, avant lui) : verificateur dedie `fne_setup_psyche`.
# Retournement : card.Flip (modele 45101a),
# a la fin de la phase du mechant (WhenPhaseEnd "Villain"). Victoire :
# Worlds.SetGameOver(True) (32130), verifiee a chaque jeton pose ici.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        vilain = TrouverMary(effect)
        if vilain and Rand.RandomChoice([True, False], effect):
            vilain.card.Flip(effect)

    def fin_de_phase(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        vilain = TrouverMary(effect)
        if vilain:
            vilain.card.Flip(effect)

    def jeton(effect: 'Effect', message: 'Message.AfterCardPlacedToken') -> None:
        VerifierVictoire(effect)

    return [
        # Une carte Setup (desc) n'a PAS de message WhenCardSetup (envoye pour
        # les complots) : sa capacite Setup vit sur AfterGameSetup (cc001, 58031).
        AbilityFactory.AfterGameSetup(mise_en_place),
        AbilityFactory.WhenPhaseEnd(AbilityType.ForcedInterrupt, "Villain", fin_de_phase),
        AbilityFactory.AfterCardPlacedToken(AbilityType.ForcedResponse, "This", None, jeton),
    ]
```

#### `60113a` Establish Trust

```json
{
 "card_id": "60113a",
 "type": "SideScheme",
 "name": "Establish Trust",
 "subtitle": "",
 "desc": {
  "StartingThreat": "8*",
  "Permanent": "1",
  "Setup": "1"
 },
 "traits": [],
 "set_name": "Typhoid Mary",
 "text": "Permanent. Setup.\n[star] In expert mode, this card gains hinder 3[per_hero].\n<b>When Defeated</b>: Place 1 threat token on Disturbed Psyche. Flip this card."
}
```

Script `src/cards/pack/fne/typhoid_mary/60113a.py` :

```python
from . import *

# Establish Trust (side scheme 8[per_hero]) — Permanent, Setup : bases desc.
# [star] In expert mode, this card gains hinder 3[per_hero].
# When Defeated: Place 1 threat token on Disturbed Psyche. Flip this card.
# (Une manigance Permanente ne quitte pas le jeu : elle se RETOURNE en
# attachement Mary Walker, qui s'accroche au vilain.)

def GetAbilities() -> Sequence['Ability']:

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        env = TrouverDisturbedPsyche(effect)
        if env:
            Faces.PlaceTokensOn([env], 1, 'threat', effect)
        VerifierVictoire(effect)
        if Worlds.IsGameOver(effect):
            return
        this.card.Flip(effect, call_reveal=False)
        mw = this.card.face
        vilain = TrouverMary(effect)
        if vilain is not None and CanAttach.IsType(mw):
            mw.AttachTo2(vilain, effect)

    return [
        AbilityFactory.IfExpertModeThisGainKeyword(hinder="3*"),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
```

#### `60113b` * Mary Walker

```json
{
 "card_id": "60113b",
 "type": "Attachment",
 "name": "* Mary Walker",
 "subtitle": "",
 "desc": {
  "Permanent": "1"
 },
 "traits": [
  "PERSONA"
 ],
 "set_name": "Typhoid Mary",
 "text": "Attach to the villain. Permanent.\n[star] Attached villain cannot activate.\n<b>Forced Response</b>: After the villain takes damage or the round ends, deal each player 1 facedown encounter card and flip this card."
}
```

Script `src/cards/pack/fne/typhoid_mary/60113b.py` :

```python
from . import *

# * Mary Walker (PERSONA) — Attach to the villain. Permanent.
# [star] Attached villain cannot activate.
# Forced Response: After the villain takes damage or the round ends, deal each
#   player 1 facedown encounter card and flip this card.
# (Le retour vers Establish Trust : FlipMaryWalkerVersEstablishTrust.)

def GetAbilities() -> Sequence['Ability']:

    def rechute(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Attachment)
        premier = Worlds.GetFirstPlayer(effect)

        def action(joueur: 'Player') -> None:
            joueur.DealEncounterCards(1, effect)

        Players.ForEachPlayer(effect, action)
        FlipMaryWalkerVersEstablishTrust(effect, premier)

    def le_vilain(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> bool:
        this = effect.this.CastTo(Attachment)
        return message.trigger is this.GetBindFace()

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.EnemyCannotActivate(AbilityType.NonKeywordStar, "AttachedEnemy"),
        AbilityFactory.AfterUnitTookDamage(AbilityType.ForcedResponse, Villain, rechute, conditions=[le_vilain]),
        AbilityFactory.WhenRoundEnd(AbilityType.ForcedResponse, None, rechute),
    ]
```

#### `60114` Telekinesis

```json
{
 "card_id": "60114",
 "type": "Attachment",
 "name": "Telekinesis",
 "subtitle": "",
 "desc": {
  "Boost": "1",
  "SCH+": "2"
 },
 "traits": [
  "PSIONIC",
  "SUPERPOWER"
 ],
 "set_name": "Typhoid Mary",
 "text": "Attach to the villain.\n<b>Hero Action</b>: Spend [mental] [mental] resources → discard this card.\n<hr />\n[star] <b>Boost</b>: If Typhoid Mary is activating, take 3 indirect damage. Exhaust each character damaged this way."
}
```

Script `src/cards/pack/fne/typhoid_mary/60114.py` :

```python
from . import *

# Telekinesis (PSIONIC, SUPERPOWER) — Attach to the villain. +2 SCH (SCH+).
# Hero Action: Spend [mental] [mental] resources -> discard this card.
# [star] Boost: If Typhoid Mary is activating, take 3 indirect damage. Exhaust
#   each character damaged this way.

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Attachment)
        if not MaryActive(effect, "Typhoid Mary"):
            return
        joueur = message.GetToPlayer()
        touches: List['CardFace'] = []

        def noter(m: 'Message.AfterUnitTookDamage') -> None:
            touches.append(m.trigger)

        joueur.GetIdentity().TakeIndirectDamage(this, 3, effect, operation=noter)
        vivants = [u for u in touches if u.IsInPlay()]
        if vivants:
            Faces.ExhaustAll(vivants, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("BB")),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

#### `60115` Psionic Slash

```json
{
 "card_id": "60115",
 "type": "Treachery",
 "name": "Psionic Slash",
 "subtitle": "",
 "desc": {
  "Boost": "0"
 },
 "traits": [],
 "set_name": "Typhoid Mary",
 "text": "<b>When Revealed</b>: If the Mary Walker attachment is in play, flip it and reveal Establish Trust. The villain schemes.\n<hr />\n[star] <b>Boost</b>: If Typhoid Mary is activating, deal 3 damage to an ally you control."
}
```

Script `src/cards/pack/fne/typhoid_mary/60115.py` :

```python
from . import *

# Psionic Slash
# When Revealed: If the Mary Walker attachment is in play, flip it and reveal
#   Establish Trust. The villain schemes.
# [star] Boost: If Typhoid Mary is activating, deal 3 damage to an ally you control.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        FlipMaryWalkerVersEstablishTrust(effect, joueur)
        vilain = TrouverMary(effect)
        if vilain:
            vilain.DoSchemes(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        if not MaryActive(effect, "Typhoid Mary"):
            return
        joueur = message.GetToPlayer()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Deal 3 damage to an ally you control", lambda targets: this.DealDamage(targets, 3, effect)).SetTarget("YourAlly"),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

#### `60116` Psi Nova

```json
{
 "card_id": "60116",
 "type": "Treachery",
 "name": "Psi Nova",
 "subtitle": "",
 "desc": {
  "Boost": "2"
 },
 "traits": [],
 "set_name": "Typhoid Mary",
 "text": "<b>When Revealed</b>: Deal 1 damage to each character you control. You are stunned.\n<hr />\n[star] <b>Boost</b>: If Typhoid Mary is activating, you are stunned."
}
```

Script `src/cards/pack/fne/typhoid_mary/60116.py` :

```python
from . import *

# Psi Nova
# When Revealed: Deal 1 damage to each character you control. You are stunned.
# [star] Boost: If Typhoid Mary is activating, you are stunned.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        this.DealDamage(list(joueur.GetControlCharacters()), 1, effect)
        Faces.GiveStatus([joueur.GetIdentity()], "Stunned", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if MaryActive(effect, "Typhoid Mary"):
            Faces.GiveStatus([message.GetToPlayer().GetIdentity()], "Stunned", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

#### `60117` Assembled Armor

```json
{
 "card_id": "60117",
 "type": "Attachment",
 "name": "Assembled Armor",
 "subtitle": "",
 "desc": {
  "Boost": "1",
  "ATK+": "2"
 },
 "traits": [
  "ARMOR"
 ],
 "set_name": "Typhoid Mary",
 "text": "Attach to the villain.\n<b>Forced Interrupt</b>: When the villain would take any amount of damage, place it here instead. Then, if there is 5 or more damage here <i>(8 or more in expert mode)</i>, discard this attachment.\n<hr />\n[star] <b>Boost</b>: If Bloody Mary is activating, you are confused."
}
```

Script `src/cards/pack/fne/typhoid_mary/60117.py` :

```python
from . import *

# Assembled Armor (ARMOR) — Attach to the villain. +2 ATK (ATK+).
# Forced Interrupt: When the villain would take any amount of damage, place
#   it here instead. Then, if there is 5 or more damage here (8 or more in
#   expert mode), discard this attachment.
# [star] Boost: If Bloody Mary is activating, you are confused.
# Modele : 60068a (PreventDamage + compteur 'damage').

def GetAbilities() -> Sequence['Ability']:

    def armure(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)
        total = message.will_take_damage
        if total <= 0:
            return
        message.PreventDamage("All", effect)
        Faces.PlaceCountersOn([this], total, 'damage', effect)
        seuil = 8 if Worlds.IsExpert(effect) else 5
        if this.GetCounters('damage') >= seuil:
            Faces.DiscardAll([this], effect)

    def le_vilain_attache(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this.CastTo(Attachment)
        return message.trigger is this.GetBindFace()

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if MaryActive(effect, "Bloody Mary"):
            Faces.GiveStatus([message.GetToPlayer().GetIdentity()], "Confused", effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, Villain, armure, conditions=[le_vilain_attache]),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

#### `60118` Hail of Blades

```json
{
 "card_id": "60118",
 "type": "Treachery",
 "name": "Hail of Blades",
 "subtitle": "",
 "desc": {
  "Boost": "0"
 },
 "traits": [],
 "set_name": "Typhoid Mary",
 "text": "<b>When Revealed</b>: If the Mary Walker attachment is in play, flip it and reveal Establish Trust. The villain attacks you <i>(even if you are in alter-ego form)</i>.\n<hr />\n[star] <b>Boost</b>: If Bloody Mary is activating, take 2 damage."
}
```

Script `src/cards/pack/fne/typhoid_mary/60118.py` :

```python
from . import *

# Hail of Blades
# When Revealed: If the Mary Walker attachment is in play, flip it and reveal
#   Establish Trust. The villain attacks you (even if you are in alter-ego form).
# [star] Boost: If Bloody Mary is activating, take 2 damage.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        FlipMaryWalkerVersEstablishTrust(effect, joueur)
        vilain = TrouverMary(effect)
        if vilain:
            vilain.DoAttackYou(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        if MaryActive(effect, "Bloody Mary"):
            this.DealDamage([message.GetToPlayer().GetIdentity()], 2, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

#### `60119` Scavenged Bulwark

```json
{
 "card_id": "60119",
 "type": "Treachery",
 "name": "Scavenged Bulwark",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "Surge": "1"
 },
 "traits": [],
 "set_name": "Typhoid Mary",
 "text": "Surge.\n<b>When Revealed</b>: Give the villain a tough status card.\n<hr />\n[star] <b>Boost</b>: If Bloody Mary is activating, give her a tough status card."
}
```

Script `src/cards/pack/fne/typhoid_mary/60119.py` :

```python
from . import *

# Scavenged Bulwark — Surge (base).
# When Revealed: Give the villain a tough status card.
# [star] Boost: If Bloody Mary is activating, give her a tough status card.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        vilain = Worlds.FindVillain(effect)
        if vilain:
            Faces.GiveStatus([vilain], "Tough", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if MaryActive(effect, "Bloody Mary"):
            Faces.GiveStatus([message.activating_enemy], "Tough", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

#### `60120` Hand Lookout

```json
{
 "card_id": "60120",
 "type": "Minion",
 "name": "Hand Lookout",
 "subtitle": "",
 "desc": {
  "HP": "4",
  "ATK": "2",
  "SCH": "0",
  "Boost": "1",
  "Guard": "1",
  "Toughness": "1"
 },
 "traits": [
  "HAND",
  "NINJA"
 ],
 "set_name": "Typhoid Mary",
 "text": "Guard. Toughness.\n<hr />\n[star] <b>Boost</b>: Give the activating enemy an additional boost card."
}
```

Script `src/cards/pack/fne/typhoid_mary/60120.py` :

```python
from . import *

# Hand Lookout (HAND, NINJA) — Guard, Toughness : bases.
# [star] Boost: Give the activating enemy an additional boost card. (11041)

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.GiveBoostCardForThisActivation(Enemy, 1, effect)

    return [
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

### Set : Art Museum Heist (8 cartes)

#### `60121a` Art Museum Heist

```json
{
 "card_id": "60121a",
 "type": "MainScheme",
 "name": "Art Museum Heist",
 "subtitle": "",
 "desc": {
  "Stage": "1A"
 },
 "traits": [],
 "set_name": "Art Museum Heist",
 "text": "<b>Contents</b>: Chosen [[Underling]] villain <i>(see rulebook p. 5)</i>. Chosen villain's set, Art Museum Heist set, and Standard set. Two modular encounter sets <i>(Cops and The Owl)</i>.\n<b>Setup</b>: Find this encounter set's 4 [[Art]] attachments and attach 1 at random to the villain. Shuffle the other 3 into the encounter deck."
}
```

Script `src/cards/pack/fne/art_museum_heist/60121a.py` :

```python
from . import *
from cards.pack.fne.campaign import CapacitesDeCampagne

# Art Museum Heist (1A)
# Setup: Find this encounter set's 4 ART attachments and attach 1 at random to
#   the villain. Shuffle the other 3 into the encounter deck.
#
# Les 4 oeuvres sont mises de cote par le scenario (set_aside). Modele : 55004a
# Prime Real Estate (SetupCards.AttachTo choose="Random", include_in_play=False),
# puis Faces.ShuffleAllTo(..., "EncounterDeck") pour les trois autres.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        vilain = Worlds.FindVillain(effect)
        if vilain is None:
            return
        SetupCards.AttachTo(
            effect,
            attach_to=vilain,
            finder=CardFinder(trait="ART", card_type=Attachment),
            include_in_play=False,
            choose="Random",
        )
        restantes = Worlds.GetSetAsideAreaCards(effect, CardFinder(trait="ART", card_type=Attachment))
        if restantes:
            Faces.ShuffleAllTo(restantes, "EncounterDeck", effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place,
        ),
        *CapacitesDeCampagne("art_museum_heist"),
    ]
```

#### `60121b` Art Museum Heist

```json
{
 "card_id": "60121b",
 "type": "MainScheme",
 "name": "Art Museum Heist",
 "subtitle": "",
 "desc": {
  "StartingThreat": "1*",
  "TargetThreat": "9*",
  "EscalationThreat": "0",
  "Stage": "1B"
 },
 "traits": [],
 "set_name": "Art Museum Heist",
 "text": "[star] X is 1 more than the number of [[Art]] attachments on the villain.\n<b>Forced Response</b>: After an enemy makes an undefended attack against an identity, attach 1 [[Art]] attachment on that identity to the villain.\n<b>If this stage is completed, the players lose the game.</b>"
}
```

Script `src/cards/pack/fne/art_museum_heist/60121b.py` :

```python
from . import *

# Art Museum Heist (1B)  — 1[per_hero] de depart, 9[per_hero] cible.
# [star] X is 1 more than the number of ART attachments on the villain.
#   (escalade +X[per_hero] : EscalationThreat "0" + WhenCalcThisSchemeEscalation,
#   modele 16091b The Art of Evasion, avec Worlds.GetPlayerNumIcon.)
# Forced Response: After an enemy makes an undefended attack against an
#   identity, attach 1 ART attachment on that identity to the villain.
#   (AfterUnitAttackUnit is_undefended_attack=True, modele Dense Forest 04080.)
# If this stage is completed, the players lose the game.

def GetAbilities() -> Sequence['Ability']:

    def escalade(effect: 'Effect') -> int:
        vilain = Worlds.FindVillain(effect)
        nb = len(OeuvresSur(vilain)) if vilain else 0
        return Worlds.GetPlayerNumIcon(effect) * (1 + nb)

    def vol_apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        identite = message.attacked
        vilain = Worlds.FindVillain(effect)
        oeuvres = OeuvresSur(identite)
        if vilain is None or not oeuvres:
            return
        joueur = identite.GetControlByPlayer()
        oeuvre = joueur.AskChooseFace(oeuvres, effect, prompt="Choose an Art attachment to give to the villain") if len(oeuvres) > 1 else oeuvres[0]
        if oeuvre is not None:
            oeuvre.AttachTo2(vilain, effect)

    return [
        AbilityFactory.WhenCalcThisSchemeEscalation(escalade),
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            Enemy,
            Identity,
            vol_apres_attaque,
            is_undefended_attack=True,
        ),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
```

#### `60122` * Impossible Object

```json
{
 "card_id": "60122",
 "type": "Attachment",
 "name": "* Impossible Object",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "Surge": "1",
  "SCH+": "1",
  "THW+": "1"
 },
 "traits": [
  "ART"
 ],
 "set_name": "Art Museum Heist",
 "text": "Surge.\nAttach to the villain.\n<b>Forced Response</b>: After this card attaches to a character, confuse that character.\n<b>Hero Action</b>: Spend a [mental] resource or exhaust your hero → attach this card to your hero."
}
```

Script `src/cards/pack/fne/art_museum_heist/60122.py` :

```python
from . import *

# * Impossible Object (ART) : confuse a l'attache ; Hero Action [mental] ou incliner.

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDUneOeuvre(
            Cost("B"),
            lambda effect, unite: Faces.GiveStatus([unite], "Confused", effect),
        ),
    ]
```

#### `60123` * Inspiring Pottery

```json
{
 "card_id": "60123",
 "type": "Attachment",
 "name": "* Inspiring Pottery",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "Surge": "1",
  "SCH+": "1",
  "THW+": "1"
 },
 "traits": [
  "ART"
 ],
 "set_name": "Art Museum Heist",
 "text": "Surge.\nAttach to the villain.\nAttached character gains stalwart.\n<b>Hero Action</b>: Spend a [wild] resource or exhaust your hero → attach this card to your hero."
}
```

Script `src/cards/pack/fne/art_museum_heist/60123.py` :

```python
from . import *

# * Inspiring Pottery (ART) : le porteur gagne stalwart ; Hero Action [wild] ou incliner.
# Modele du stalwart attache : 16064 Drang's Spear, sur "Character" (le porteur,
# vilain ou heros).

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDUneOeuvre(Cost("G"), None),
        *AbilityFactory.GiveKeywordToAttached(
            "Character",
            stalwart=1,
        ),
    ]
```

#### `60124` * Replica Shield

```json
{
 "card_id": "60124",
 "type": "Attachment",
 "name": "* Replica Shield",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "Surge": "1",
  "SCH+": "1",
  "THW+": "1"
 },
 "traits": [
  "ART"
 ],
 "set_name": "Art Museum Heist",
 "text": "Surge.\nAttach to the villain.\n<b>Forced Response</b>: After this card attaches to a character, give that character a tough status card.\n<b>Hero Action</b>: Spend a [physical] resource or exhaust your hero → attach this card to your hero."
}
```

Script `src/cards/pack/fne/art_museum_heist/60124.py` :

```python
from . import *

# * Replica Shield (ART) : tough a l'attache ; Hero Action [physical] ou incliner.

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDUneOeuvre(
            Cost("R"),
            lambda effect, unite: Faces.GiveStatus([unite], "Tough", effect),
        ),
    ]
```

#### `60125` * Stunning Landscape

```json
{
 "card_id": "60125",
 "type": "Attachment",
 "name": "* Stunning Landscape",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "Surge": "1",
  "SCH+": "1",
  "THW+": "1"
 },
 "traits": [
  "ART"
 ],
 "set_name": "Art Museum Heist",
 "text": "Surge.\nAttach to the villain.\n<b>Forced Response</b>: After this card attaches to a character, stun that character.\n<b>Hero Action</b>: Spend an [energy] resource or exhaust your hero → attach this card to your hero."
}
```

Script `src/cards/pack/fne/art_museum_heist/60125.py` :

```python
from . import *

# * Stunning Landscape (ART) : stun a l'attache ; Hero Action [energy] ou incliner.

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDUneOeuvre(
            Cost("Y"),
            lambda effect, unite: Faces.GiveStatus([unite], "Stunned", effect),
        ),
    ]
```

#### `60126` Art Thief

```json
{
 "card_id": "60126",
 "type": "Minion",
 "name": "Art Thief",
 "subtitle": "",
 "desc": {
  "HP": "3",
  "ATK": "2",
  "SCH": "2",
  "Boost": "0"
 },
 "traits": [
  "THIEF"
 ],
 "set_name": "Art Museum Heist",
 "text": "<b>When Revealed</b>: Search the encounter deck and discard pile for an [[Art]] attachment and attach it to the villain. If you cannot, move an [[Art]] attachment from an identity to the villain.\n<hr />\n[star] <b>Boost</b>: Move an [[Art]] attachment from an identity to the villain."
}
```

Script `src/cards/pack/fne/art_museum_heist/60126.py` :

```python
from . import *

# Art Thief (THIEF)
# When Revealed: Search the encounter deck and discard pile for an ART
#   attachment and attach it to the villain. If you cannot, move an ART
#   attachment from an identity to the villain.
# [star] Boost: Move an ART attachment from an identity to the villain.
#
# Modeles : 01095 Rhino (Search.EncounterCard include_discard_pile), l'attache
# passe par PutIntoPlay : l'oeuvre s'accroche elle-meme au vilain
# (AttachToFaceWhenPutIntoPlay), sans declencher son Surge (pas de Reveal).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        face = Search.EncounterCard(
            effect,
            include_discard_pile=True,
            trait="ART",
            card_type=Attachment,
        )
        if face:
            face.PutIntoPlay(joueur, effect)
        else:
            DeplacerUneOeuvreVersLeVilain(effect, joueur)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        DeplacerUneOeuvreVersLeVilain(effect, message.GetToPlayer())

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

#### `60127` Tug of War

```json
{
 "card_id": "60127",
 "type": "Treachery",
 "name": "Tug of War",
 "subtitle": "",
 "desc": {
  "Boost": "1"
 },
 "traits": [],
 "set_name": "Art Museum Heist",
 "text": "<b>When Revealed</b>: You may spend [physical] [physical] [physical] resources to move an [[Art]] attachment from the villain to your identity. Otherwise, move an [[Art]] attachment from an identity to the villain and this card gains surge."
}
```

Script `src/cards/pack/fne/art_museum_heist/60127.py` :

```python
from . import *

# Tug of War
# When Revealed: You may spend [physical] x3 resources to move an ART
#   attachment from the villain to your identity. Otherwise, move an ART
#   attachment from an identity to the villain and this card gains surge.
#
# Modele : 50134 Innocent Bystanders (ForChoiceAbilityWithCost) + Otherwise.
# La branche payante n'est offerte que si le vilain porte une oeuvre ET que
# le joueur peut payer (PeutCouvrirLeCout, helper du pack).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()

        def branche_payante_possible(effet_choix: 'Effect', message_choix: 'Message.WhenPlayerChooseAbility') -> bool:
            # Offerte seulement si le vilain porte une oeuvre ET si les trois
            # [physical] sont couvrables : sinon le moteur ne proposerait
            # qu'elle (Otherwise est masquee tant qu'une autre option existe),
            # le paiement echouerait et rien ne se passerait (constate au
            # harnais, 18/09/2026). ⚠ Le joueur vient de la CLOTURE : le message
            # de choix n'expose pas GetToPlayer (exception avalee -> condition
            # fausse, branche jamais offerte, constate le meme jour).
            vilain = Worlds.FindVillain(effet_choix)
            if vilain is None or not OeuvresSur(vilain):
                return False
            return PeutCouvrirLeCout(joueur, effet_choix, Cost("RRR"))

        def reprendre(targets: Sequence['CardFace'], res: 'Resources') -> None:
            DeplacerUneOeuvreDuVilainVers(effect, joueur, joueur.GetIdentity())

        def sinon(targets: Sequence['CardFace']) -> None:
            DeplacerUneOeuvreVersLeVilain(effect, joueur)
            ThisCardGainSurge(effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("RRR"),
                "Spend [physical][physical][physical]: move an Art attachment from the villain to your identity",
                reprendre,
                conditions=[branche_payante_possible],
            ),
            AbilityFactory.Otherwise(sinon),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
```

### Set : The Getaway (8 cartes)

#### `60128a` The Getaway

```json
{
 "card_id": "60128a",
 "type": "MainScheme",
 "name": "The Getaway",
 "subtitle": "",
 "desc": {
  "Stage": "1A"
 },
 "traits": [],
 "set_name": "The Getaway",
 "text": "<b>Contents</b>: Chosen [[Underling]] villain <i>(see rulebook p. 5)</i>. Chosen villain's set, The Getaway set, and Standard set. Two modular encounter sets <i>(Cops and Drive)</i>.\n<b>Setup</b>: Place 1 speed counter here <i>(2 counters instead in expert mode)</i>. Attach the Out Front attachment (129A) to the villain."
}
```

Script `src/cards/pack/fne/the_getaway/60128a.py` :

```python
from . import *
from cards.pack.fne.campaign import CapacitesDeCampagne

# The Getaway 1A
# Setup: Place 1 speed counter here (2 counters instead in expert mode).
#   Attach the Out Front attachment (129A) to the villain.
# Modele : 60121a (WhenCardSetup du complot 1A), Find.FindAndAttachTo (60066)
# pour aller chercher Out Front dans la mise de cote du scenario.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Faces.PlaceCountersOn([this], 2 if Worlds.IsExpert(effect) else 1, 'speed', effect)
        vilain = Worlds.FindVillain(effect)
        if vilain is not None:
            Find.FindAndAttachTo(effect, vilain, who_perform=Worlds.GetFirstPlayer(effect), name="Out Front", card_type=Attachment)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        # Mode campagne (livret p. 9 et encarts CAMPAIGN INSTRUCTIONS) : inerte
        # hors campagne (`Worlds.IsCampaign`), voir cards/pack/fne/campaign.py.
        *CapacitesDeCampagne("the_getaway"),
    ]
```

#### `60128b` The Getaway

```json
{
 "card_id": "60128b",
 "type": "MainScheme",
 "name": "The Getaway",
 "subtitle": "",
 "desc": {
  "StartingThreat": "2*",
  "TargetThreat": "9*",
  "EscalationThreat": "2*",
  "Stage": "1B"
 },
 "traits": [],
 "set_name": "The Getaway",
 "text": "<b>Forced Interrupt</b>: When the round ends, if there is threat here, do each of the following:\n1. Place 1 speed counter here.\n2. If Alongside is in play, flip it to Out Front. Otherwise, place 1 additional speed counter here.\nIf this stage is completed, the players lose the game."
}
```

Script `src/cards/pack/fne/the_getaway/60128b.py` :

```python
from . import *

# The Getaway 1B — 2[per_hero] de depart, cible 9[per_hero], escalade
#   +2[per_hero] : bases desc.
# Forced Interrupt: When the round ends, if there is threat here, do each of
#   the following: 1. Place 1 speed counter here. 2. If Alongside is in play,
#   flip it to Out Front. Otherwise, place 1 additional speed counter here.
# If this stage is completed, the players lose the game.
# ⚠ « if there is threat here » lu AVANT toute action ; Alongside -> Out Front
# passe par RetournerLAttachement (le Flip nu detache, RECETTES §7quater).

def GetAbilities() -> Sequence['Ability']:

    def fin_de_round(effect: 'Effect', message: 'Message.WhenRoundEnd') -> None:
        this = effect.this.CastTo(MainScheme)
        if this.threat <= 0:
            return
        Faces.PlaceCountersOn([this], 1, 'speed', effect)
        alongside = Worlds.FindCardOnField(effect, name="Alongside", card_type=Attachment)
        if alongside is not None:
            RetournerLAttachement(alongside, effect)
        else:
            Faces.PlaceCountersOn([this], 1, 'speed', effect)

    return [
        AbilityFactory.WhenRoundEnd(AbilityType.ForcedInterrupt, None, fin_de_round),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
```

#### `60129a` Out Front

```json
{
 "card_id": "60129a",
 "type": "Attachment",
 "name": "Out Front",
 "subtitle": "",
 "desc": {
  "Permanent": "1"
 },
 "traits": [],
 "set_name": "The Getaway",
 "text": "Permanent.\nAttach to the villain.\nIf there is no threat on the main scheme, flip this card.\n[star] Attached villain's attacks gain ranged.\n<b>Forced Interrupt</b>: When the villain would be dealt any amount of damage, remove that amount of threat from the main scheme instead <i>(ignoring crisis icons)</i>."
}
```

Script `src/cards/pack/fne/the_getaway/60129a.py` :

```python
from . import *

# Out Front — Permanent (base). Attach to the villain.
# If there is no threat on the main scheme, flip this card.
# [star] Attached villain's attacks gain ranged.
# Forced Interrupt: When the villain would be dealt any amount of damage,
#   remove that amount of threat from the main scheme instead (ignoring
#   crisis icons).
# « no threat on the main scheme » : verifie apres chaque retrait de menace du
# complot principal (AfterSchemeRemoveThreat(MainScheme, last_threat=True) ;
# ⚠ which_scheme est un TYPE, la chaine "MainScheme" leve un AssertionError
# avale dans CheckWhichCard, harnais du 18/09/2026). Le retrait ignore
# la crise : RemoveThreatFromSchemes(ignore_crisis=True). Alongside ->
# Out Front = fin de round (60128b) ; Out Front -> Alongside = ici.

def GetAbilities() -> Sequence['Ability']:

    def plus_de_menace(effect: 'Effect', message: 'Message.AfterSchemeRemoveThreat') -> None:
        this = effect.this.CastTo(Attachment)
        scheme = message.trigger
        if scheme.threat <= 0 and this.IsInPlay():
            RetournerLAttachement(this, effect)

    def encaisse(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)
        total = message.will_take_damage
        if total <= 0:
            return
        message.PreventDamage("All", effect)
        this.RemoveThreatFromSchemes("MainScheme", total, effect, ignore_crisis=True)

    def le_vilain_attache(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this.CastTo(Attachment)
        return message.trigger is this.GetBindFace()

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.UnitAttackGainKeyword("AttachedEnemy", ranged=True),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, Villain, encaisse, conditions=[le_vilain_attache]),
        AbilityFactory.AfterSchemeRemoveThreat(AbilityType.ForcedInterrupt, MainScheme, plus_de_menace, last_threat=True),
    ]
```

#### `60129b` Alongside

```json
{
 "card_id": "60129b",
 "type": "Attachment",
 "name": "Alongside",
 "subtitle": "",
 "desc": {
  "Permanent": "1"
 },
 "traits": [],
 "set_name": "The Getaway",
 "text": "Permanent.\n<b>When Revealed</b>: Each player takes 1 indirect damage. The villain takes 2[per_hero] damage."
}
```

Script `src/cards/pack/fne/the_getaway/60129b.py` :

```python
from . import *

# Alongside — Permanent (base).
# When Revealed: Each player takes 1 indirect damage. The villain takes
#   2[per_hero] damage.
# La face apparait par retournement (RetournerLAttachement, call_reveal) : le
# When Revealed se resout alors (FAQ du livret sur Bloody Mary (B)).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)

        def un_indirect(player: 'Player') -> None:
            player.GetIdentity().TakeIndirectDamage(this, 1, effect)

        Players.ForEachPlayer(effect, un_indirect)
        vilain = Worlds.FindVillain(effect)
        if vilain is not None:
            this.DealDamage([vilain], 2 * Worlds.GetPlayerNumIcon(effect), effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
```

#### `60130` Escort Vehicle

```json
{
 "card_id": "60130",
 "type": "Minion",
 "name": "Escort Vehicle",
 "subtitle": "",
 "desc": {
  "HP": "5",
  "ATK": "2",
  "SCH": "2",
  "Boost": "3",
  "Guard": "1",
  "Patrol": "1"
 },
 "traits": [
  "VEHICLE"
 ],
 "set_name": "The Getaway",
 "text": "Guard. Patrol.\nIf the number of speed counters on the main scheme is at least:\n• 3 – This minion gains toughness.\n• 6 – This minion also gains quickstrike.\n• 9 – This minion also gains surge."
}
```

Script `src/cards/pack/fne/the_getaway/60130.py` :

```python
from . import *

# Escort Vehicle (VEHICLE) — Guard, Patrol : bases desc.
# If the number of speed counters on the main scheme is at least:
#   • 3 – This minion gains toughness.  • 6 – ...also quickstrike.
#   • 9 – ...also surge.
# ThisGainKeyword(check_fn) recalcule sur OnEvent.Counter(MainScheme, 'speed')
# (modele 60091 Chameleon pour le recalcul sur evenement).

def GetAbilities() -> Sequence['Ability']:

    def seuil(n: int):
        def check(effect: 'Effect', ui: List['CardFace']) -> int:
            return 1 if CompteursDeVitesse(effect) >= n else 0
        return check

    # ⚠ OnEvent.Counter prend un TYPE : la chaine "MainScheme" est une
    # Sequence et leve `assert not isinstance(check_rule, Sequence)`
    # (card_type.py:247) a CHAQUE compteur pose pendant que le sbire est en
    # jeu (15 tracebacks par partie d'autoplay, vus par l'agent B le 18/09).
    evenement = OnEvent.Counter(MainScheme, 'speed')
    return [
        AbilityFactory.ThisGainKeyword(seuil(3), toughness=1, change_on_event=evenement),
        AbilityFactory.ThisGainKeyword(seuil(6), quickstrike=1, change_on_event=evenement),
        AbilityFactory.ThisGainKeyword(seuil(9), surge=1, change_on_event=evenement),
    ]
```

#### `60131` Jackknifed Tanker Truck

```json
{
 "card_id": "60131",
 "type": "SideScheme",
 "name": "Jackknifed Tanker Truck",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "StartingThreat": "2",
  "Hinder": "1*",
  "Crisis": "1"
 },
 "traits": [],
 "set_name": "The Getaway",
 "text": "[star] Hinder 1[per_hero].\nThe villain cannot be dealt damage."
}
```

Script `src/cards/pack/fne/the_getaway/60131.py` :

```python
from . import *

# Jackknifed Tanker Truck (side scheme 2, crisis) — [star] Hinder 1[per_hero] : base.
# The villain cannot be dealt damage.  (UnitCannotTakeDamage(Villain), fabrique
# corrigee le 30/08/2026, rend une liste.)

def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.UnitCannotTakeDamage(Villain),
    ]
```

#### `60132` Burning Rubber

```json
{
 "card_id": "60132",
 "type": "Treachery",
 "name": "Burning Rubber",
 "subtitle": "",
 "desc": {
  "Boost": "1"
 },
 "traits": [],
 "set_name": "The Getaway",
 "text": "<b>When Revealed</b>: For each speed counter on the main scheme, choose:\n• Spend 1 resource of any type.\n• Place 1 threat on the main scheme."
}
```

Script `src/cards/pack/fne/the_getaway/60132.py` :

```python
from . import *

# Burning Rubber
# When Revealed: For each speed counter on the main scheme, choose:
#   • Spend 1 resource of any type.  • Place 1 threat on the main scheme.
# Branche payante offerte seulement si payable (PeutCouvrirLeCout, 60127) ;
# sinon la seconde branche s'impose.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()

        def payable(effet_choix: 'Effect', message_choix: 'Message.WhenPlayerChooseAbility') -> bool:
            return PeutCouvrirLeCout(joueur, effet_choix, Cost("1"))

        def branches() -> Sequence['Ability']:
            return [
                AbilityFactory.ForChoiceAbilityWithCost(Cost("1"), "Spend 1 resource of any type", lambda targets, res: None, conditions=[payable]),
                AbilityFactory.ForChoiceAbility("Place 1 threat on the main scheme", lambda targets: this.PlaceThreatOnSchemes("MainScheme", 1, effect)),
            ]

        PourChaqueCompteurDeVitesse(effect, joueur, branches)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
```

#### `60133` Pedestrians

```json
{
 "card_id": "60133",
 "type": "Treachery",
 "name": "Pedestrians",
 "subtitle": "",
 "desc": {
  "Boost": "1"
 },
 "traits": [],
 "set_name": "The Getaway",
 "text": "<b>When Revealed</b>: For each speed counter on the main scheme, choose:\n• Exhaust a character you control.\n• Take 1 indirect damage."
}
```

Script `src/cards/pack/fne/the_getaway/60133.py` :

```python
from . import *

# Pedestrians
# When Revealed: For each speed counter on the main scheme, choose:
#   • Exhaust a character you control.  • Take 1 indirect damage.
# « a character you control » : un personnage PRET (sinon la branche ne fait
# rien) ; le choix du personnage passe par la cible de la branche.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()

        def incliner(targets: Sequence['CardFace']) -> None:
            prets = [c for c in joueur.GetControlCharacters() if c.IsReady()]
            if not prets:
                return
            cible = prets[0] if len(prets) == 1 else joueur.AskChooseFace(prets, effect)
            if cible is not None:
                Faces.ExhaustAll([cible], effect)

        def branches() -> Sequence['Ability']:
            # ⚠ ForChoiceAbility n'a pas de `conditions` (seule la variante
            # WithCost en a) : `condition` est un BOOLEEN evalue a la
            # construction, et branches() est rappelee a chaque compteur.
            un_pret_existe = any(c.IsReady() for c in joueur.GetControlCharacters())
            return [
                AbilityFactory.ForChoiceAbility("Exhaust a character you control", incliner, condition=un_pret_existe),
                AbilityFactory.ForChoiceAbility("Take 1 indirect damage", lambda targets: joueur.GetIdentity().TakeIndirectDamage(this, 1, effect)),
            ]

        PourChaqueCompteurDeVitesse(effect, joueur, branches)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
```

### Set : Protection Racket (13 cartes)

#### `60134a` Protection Racket

```json
{
 "card_id": "60134a",
 "type": "MainScheme",
 "name": "Protection Racket",
 "subtitle": "",
 "desc": {
  "Stage": "1A"
 },
 "traits": [],
 "set_name": "Protection Racket",
 "text": "<b>Contents</b>: Chosen [[Underling]] villain <i>(see rulebook p. 5)</i>. Chosen villain's set, Protection Racket set, and Standard set. Two modular encounter sets <i>(Disasters and Tracksuit Mafia)</i>.\n<b>Setup</b>: Each player chooses a single Protection Racket main scheme <i>(at random in expert mode)</i>, places it in their play area, and flips it to its 1B side. Set each unused main scheme aside, out of play."
}
```

Script `src/cards/pack/fne/protection_racket/60134a.py` :

```python
from . import *

# Protection Racket 1A (face commune aux cinq complots) : voir CapacitesDe1A.

from cards.pack.fne.campaign import CapacitesDeCampagne


def _premier_complot(effect: 'Effect', message: 'Message2') -> bool:
    """Un complot principal PAR JOUEUR : seul le premier en jeu porte les
    capacites de campagne (voir CapacitesDeCampagne, `garde`)."""
    # ⚠ Par la CARTE, pas par la face : a la mise en place de campagne le
    # complot est deja retourne cote 1B, `effect.this` est la face 1A.
    complots = ComplotsRacket(effect)
    return bool(complots) and complots[0].card is effect.this.card


def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDe1A(),
        # Mode campagne (livret p. 9 et p. 13) : inerte hors campagne.
        *CapacitesDeCampagne("protection_racket", garde=_premier_complot),
    ]
```

#### `60134b` Battle in the Bodega

```json
{
 "card_id": "60134b",
 "type": "MainScheme",
 "name": "Battle in the Bodega",
 "subtitle": "",
 "desc": {
  "StartingThreat": "0",
  "TargetThreat": "10",
  "EscalationThreat": "1",
  "Stage": "1B"
 },
 "traits": [],
 "set_name": "Protection Racket",
 "text": "<b>Forced Response</b>: After a character in this play area is attacked, deal 1 damage to the attacker and place 1 threat here. <i>(Limit once per phase in standard mode.)</i>\nIf any main scheme is completed or any player is eliminated, the players lose the game."
}
```

Script `src/cards/pack/fne/protection_racket/60134b.py` :

```python
from . import *

# Battle in the Bodega 1B — 10 menaces, +1 : bases desc.
# Forced Response: After a character in this play area is attacked, deal 1
#   damage to the attacker and place 1 threat here. (Limit once per phase in
#   standard mode.)
# If any main scheme is completed or any player is eliminated, the players
#   lose the game.  (CapacitesCommunes1B)
# « in this play area » = DansCetteAire ; la limite ne vaut qu'en mode normal
# (deux capacites, l'une limitee et l'autre non, selon Worlds.IsExpert).

def GetAbilities() -> Sequence['Ability']:

    def riposte(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(MainScheme)
        attaquant = message.attacker
        if attaquant is not None and attaquant.IsInPlay():
            this.DealDamage([attaquant], 1, effect)
        this.PlaceThreatOnSchemes([this], 1, effect)

    def dans_cette_aire(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> bool:
        return DansCetteAire(message.attacked, effect.this)

    normal = AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, Enemy, "YouControlCharacter", riposte,
                                               conditions=[dans_cette_aire, lambda e, m: not Worlds.IsExpert(e)]).LimitOncePerPhase()
    expert = AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, Enemy, "YouControlCharacter", riposte,
                                               conditions=[dans_cette_aire, lambda e, m: Worlds.IsExpert(e)])
    return [normal, expert, *CapacitesCommunes1B()]
```

#### `60135a` Protection Racket

```json
{
 "card_id": "60135a",
 "type": "MainScheme",
 "name": "Protection Racket",
 "subtitle": "",
 "desc": {
  "Stage": "1A"
 },
 "traits": [],
 "set_name": "Protection Racket",
 "text": "<b>Contents</b>: Chosen [[Underling]] villain <i>(see rulebook p. 5)</i>. Chosen villain's set, Protection Racket set, and Standard set. Two modular encounter sets <i>(Disasters and Tracksuit Mafia)</i>.\n<b>Setup</b>: Each player chooses a single Protection Racket main scheme <i>(at random in expert mode)</i>, places it in their play area, and flips it to its 1B side. Set each unused main scheme aside, out of play."
}
```

Script `src/cards/pack/fne/protection_racket/60135a.py` :

```python
from . import *

# Protection Racket 1A (face commune aux cinq complots) : voir CapacitesDe1A.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDe1A()]
```

#### `60135b` Bull in a China Shop

```json
{
 "card_id": "60135b",
 "type": "MainScheme",
 "name": "Bull in a China Shop",
 "subtitle": "",
 "desc": {
  "StartingThreat": "0",
  "TargetThreat": "10",
  "EscalationThreat": "1",
  "Stage": "1B"
 },
 "traits": [],
 "set_name": "Protection Racket",
 "text": "<b>Forced Interrupt</b>: When excess damage is dealt to an ally <i>(in expert mode, an ally or a minion)</i> in this play area, place an equal amount of threat on this scheme.\nIf any main scheme is completed or any player is eliminated, the players lose the game."
}
```

Script `src/cards/pack/fne/protection_racket/60135b.py` :

```python
from . import *

# Bull in a China Shop 1B — 10, +1 : bases desc.
# Forced Interrupt: When excess damage is dealt to an ally (in expert mode, an
#   ally or a minion) in this play area, place an equal amount of threat on
#   this scheme.
# WhenUnitBeDefeated.excess_damage (sender_unit.py:70) : l'exces n'existe qu'a la defaite.

def GetAbilities() -> Sequence['Ability']:

    def casse(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(MainScheme)
        exces = int(getattr(message, "excess_damage", 0) or 0)
        if exces > 0:
            this.PlaceThreatOnSchemes([this], exces, effect)

    def concerne(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> bool:
        unite = message.trigger
        if not DansCetteAire(unite, effect.this):
            return False
        if Ally.IsType(unite):
            return True
        return Minion.IsType(unite) and Worlds.IsExpert(effect)

    return [
        # L'exces n'existe qu'a la defaite : WhenUnitBeDefeated.excess_damage
        # (= -PV restants, sender_unit.py:70) ; AfterUnitTookDamage ne part pas
        # pour le coup fatal (mesure du 18/09/2026).
        AbilityFactory.WhenUnitBeDefeated(AbilityType.ForcedInterrupt, Unit2, casse, conditions=[concerne]),
        *CapacitesCommunes1B(),
    ]
```

#### `60136a` Protection Racket

```json
{
 "card_id": "60136a",
 "type": "MainScheme",
 "name": "Protection Racket",
 "subtitle": "",
 "desc": {
  "Stage": "1A"
 },
 "traits": [],
 "set_name": "Protection Racket",
 "text": "<b>Contents</b>: Chosen [[Underling]] villain <i>(see rulebook p. 5)</i>. Chosen villain's set, Protection Racket set, and Standard set. Two modular encounter sets <i>(Disasters and Tracksuit Mafia)</i>.\n<b>Setup</b>: Each player chooses a single Protection Racket main scheme <i>(at random in expert mode)</i>, places it in their play area, and flips it to its 1B side. Set each unused main scheme aside, out of play."
}
```

Script `src/cards/pack/fne/protection_racket/60136a.py` :

```python
from . import *

# Protection Racket 1A (face commune aux cinq complots) : voir CapacitesDe1A.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDe1A()]
```

#### `60136b` Hung Out to Dry

```json
{
 "card_id": "60136b",
 "type": "MainScheme",
 "name": "Hung Out to Dry",
 "subtitle": "",
 "desc": {
  "StartingThreat": "0",
  "TargetThreat": "10",
  "EscalationThreat": "1",
  "Stage": "1B"
 },
 "traits": [],
 "set_name": "Protection Racket",
 "text": "<b>Forced Response</b>: After a character enters play in this play area, deal 1 damage to it and place 1 threat here.\nIf any main scheme is completed or any player is eliminated, the players lose the game."
}
```

Script `src/cards/pack/fne/protection_racket/60136b.py` :

```python
from . import *

# Hung Out to Dry 1B — 10, +1 : bases desc.
# Forced Response: After a character enters play in this play area, deal 1
#   damage to it and place 1 threat here.
# AfterCardEnterPlay(Character) filtre par DansCetteAire (sbire engage avec le
# proprietaire compris).

def GetAbilities() -> Sequence['Ability']:

    def serre(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(MainScheme)
        unite = message.trigger
        if unite.IsInPlay():
            this.DealDamage([unite], 1, effect)
        this.PlaceThreatOnSchemes([this], 1, effect)

    def concerne(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> bool:
        unite = message.trigger
        return Unit2.IsType(unite) and DansCetteAire(unite, effect.this)

    return [
        AbilityFactory.AfterCardEnterPlay(AbilityType.ForcedResponse, None, serre, conditions=[concerne]),
        *CapacitesCommunes1B(),
    ]
```

#### `60137a` Protection Racket

```json
{
 "card_id": "60137a",
 "type": "MainScheme",
 "name": "Protection Racket",
 "subtitle": "",
 "desc": {
  "Stage": "1A"
 },
 "traits": [],
 "set_name": "Protection Racket",
 "text": "<b>Contents</b>: Chosen [[Underling]] villain <i>(see rulebook p. 5)</i>. Chosen villain's set, Protection Racket set, and Standard set. Two modular encounter sets <i>(Disasters and Tracksuit Mafia)</i>.\n<b>Setup</b>: Each player chooses a single Protection Racket main scheme <i>(at random in expert mode)</i>, places it in their play area, and flips it to its 1B side. Set each unused main scheme aside, out of play."
}
```

Script `src/cards/pack/fne/protection_racket/60137a.py` :

```python
from . import *

# Protection Racket 1A (face commune aux cinq complots) : voir CapacitesDe1A.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDe1A()]
```

#### `60137b` Pawn Shop Showdown

```json
{
 "card_id": "60137b",
 "type": "MainScheme",
 "name": "Pawn Shop Showdown",
 "subtitle": "",
 "desc": {
  "StartingThreat": "0",
  "TargetThreat": "10",
  "EscalationThreat": "1",
  "Stage": "1B"
 },
 "traits": [],
 "set_name": "Protection Racket",
 "text": "Reduce the cost of the first upgrade played into this play area each round by 1.\n<b>Forced Response</b>: After an attachment or upgrade enters play in this play area, place 1 threat here.\nIf any main scheme is completed or any player is eliminated, the players lose the game."
}
```

Script `src/cards/pack/fne/protection_racket/60137b.py` :

```python
from . import *

# Pawn Shop Showdown 1B — 10, +1 : bases desc.
# Reduce the cost of the first upgrade played into this play area each round by 1.
# Forced Response: After an attachment or upgrade enters play in this play
#   area, place 1 threat here.
# La reduction : ReduceCostToPlayFaceWhen(Upgrade) pour le proprietaire, une
# fois par round (drapeau remis a zero en fin de round).

def GetAbilities() -> Sequence['Ability']:
    etat = {"round": -1}

    def premiere_du_round(effect: 'Effect', message: 'Message') -> bool:
        return etat["round"] != effect.world.round_id

    def apres_entree(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(MainScheme)
        carte = message.trigger
        if Upgrade.IsType(carte) and carte.GetControlByPlayer() is Proprietaire(this):
            etat["round"] = effect.world.round_id
        this.PlaceThreatOnSchemes([this], 1, effect)

    def concerne(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> bool:
        carte = message.trigger
        this = effect.this
        if Upgrade.IsType(carte):
            return carte.GetControlByPlayer() is Proprietaire(this)
        if Attachment.IsType(carte):
            porteur = carte.GetBindFace()
            return porteur is not None and DansCetteAire(porteur, this)
        return False

    def du_proprietaire(effect: 'Effect', message: 'Message') -> bool:
        joueur = effect.world.current_player
        return joueur is not None and joueur is Proprietaire(effect.this)

    return [
        AbilityFactory.ReduceCostToPlayFaceWhen(Upgrade, 1, "AnyPlayer", conditions=[premiere_du_round, du_proprietaire]),
        AbilityFactory.AfterCardEnterPlay(AbilityType.ForcedResponse, None, apres_entree, conditions=[concerne]),
        *CapacitesCommunes1B(),
    ]
```

#### `60138a` Protection Racket

```json
{
 "card_id": "60138a",
 "type": "MainScheme",
 "name": "Protection Racket",
 "subtitle": "",
 "desc": {
  "Stage": "1A"
 },
 "traits": [],
 "set_name": "Protection Racket",
 "text": "<b>Contents</b>: Chosen [[Underling]] villain <i>(see rulebook p. 5)</i>. Chosen villain's set, Protection Racket set, and Standard set. Two modular encounter sets <i>(Disasters and Tracksuit Mafia)</i>.\n<b>Setup</b>: Each player chooses a single Protection Racket main scheme <i>(at random in expert mode)</i>, places it in their play area, and flips it to its 1B side. Set each unused main scheme aside, out of play."
}
```

Script `src/cards/pack/fne/protection_racket/60138a.py` :

```python
from . import *

# Protection Racket 1A (face commune aux cinq complots) : voir CapacitesDe1A.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDe1A()]
```

#### `60138b` A Slice of the Pizza Dough

```json
{
 "card_id": "60138b",
 "type": "MainScheme",
 "name": "A Slice of the Pizza Dough",
 "subtitle": "",
 "desc": {
  "StartingThreat": "0",
  "TargetThreat": "10",
  "EscalationThreat": "1",
  "Stage": "1B"
 },
 "traits": [],
 "set_name": "Protection Racket",
 "text": "<b>Forced Response</b>: After a character in this play area defeats another character or a side scheme <i>(in any play area)</i>, heal 1 damage from the defeating character and place 1 threat here.\nIf any main scheme is completed or any player is eliminated, the players lose the game."
}
```

Script `src/cards/pack/fne/protection_racket/60138b.py` :

```python
from . import *

# A Slice of the Pizza Dough 1B — 10, +1 : bases desc.
# Forced Response: After a character in this play area defeats another
#   character or a side scheme (in any play area), heal 1 damage from the
#   defeating character and place 1 threat here.

def GetAbilities() -> Sequence['Ability']:

    def recompense(effect: 'Effect', message: 'Message') -> None:
        this = effect.this.CastTo(MainScheme)
        tueur = getattr(message, "killer", None) or getattr(message, "trigger", None)
        if tueur is not None and tueur.IsInPlay():
            tueur.HealHealth(1, effect)
        this.PlaceThreatOnSchemes([this], 1, effect)

    def tueur_de_cette_aire(effect: 'Effect', message: 'Message') -> bool:
        tueur = getattr(message, "killer", None) or getattr(message, "trigger", None)
        return tueur is not None and Unit2.IsType(tueur) and DansCetteAire(tueur, effect.this)

    return [
        AbilityFactory.AfterUnitDefeatedUnit(AbilityType.ForcedResponse, None, None, recompense, conditions=[tueur_de_cette_aire]),
        AbilityFactory.AfterUnitDefeatedScheme(AbilityType.ForcedResponse, None, EncounterSideScheme, recompense, conditions=[tueur_de_cette_aire]),
        *CapacitesCommunes1B(),
    ]
```

#### `60139` Shop Proprietor

```json
{
 "card_id": "60139",
 "type": "Ally",
 "name": "Shop Proprietor",
 "subtitle": "",
 "desc": {
  "Cost": "0",
  "HP": "3",
  "ATK": "1**",
  "THW": "1**",
  "Class": "Encounter"
 },
 "traits": [
  "CIVILIAN"
 ],
 "set_name": "Protection Racket",
 "text": "<b>When Revealed</b>: Put Shop Proprietor into play under your control. This card gains surge.\n<b>Forced Interrupt</b>: When this ally leaves play, place 4 threat on the main scheme in your play area."
}
```

Script `src/cards/pack/fne/protection_racket/60139.py` :

```python
from . import *

# Shop Proprietor (allie de rencontre, CIVILIAN, cout 0, THW 1, ATK 1, 3 PV)
# When Revealed: Put Shop Proprietor into play under your control. This card
#   gains surge.
# Forced Interrupt: When this ally leaves play, place 4 threat on the main
#   scheme in your play area.
# « your play area » = le complot du controleur de l'allie (ComplotDuJoueur).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Ally)
        joueur = message.GetToPlayer()
        this.PutIntoPlay(joueur, effect, under_control=True)
        ThisCardGainSurge(effect)

    def part(effect: 'Effect', message: 'Message.WhenCardLeavePlay') -> None:
        this = effect.this.CastTo(Ally)
        joueur = this.GetControlByPlayer()
        if joueur is None:
            return
        scheme = ComplotDuJoueur(effect, joueur) or Worlds.FindMainScheme(effect)
        if scheme is not None:
            this.PlaceThreatOnSchemes([scheme], 4, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardLeavePlay(AbilityType.ForcedInterrupt, "This", part),
    ]
```

#### `60140` * Man-Bull

```json
{
 "card_id": "60140",
 "type": "Minion",
 "name": "* Man-Bull",
 "subtitle": "",
 "desc": {
  "HP": "6",
  "ATK": "4",
  "SCH": "2",
  "Boost": "2"
 },
 "traits": [
  "BRUTE"
 ],
 "set_name": "Protection Racket",
 "text": "[star] <b>Forced Response</b>: After Man-Bull attacks, place threat on the main scheme equal to the excess damage dealt by this attack.\n<hr />\n[star] <b>Boost</b>: If this activation is an attack, place threat on the main scheme equal to the excess damage dealt by this attack."
}
```

Script `src/cards/pack/fne/protection_racket/60140.py` :

```python
from . import *

# * Man-Bull (BRUTE) — SCH 2, ATK 4, 6 PV, boost 2.
# [star] Forced Response: After Man-Bull attacks, place threat on the main
#   scheme equal to the excess damage dealt by this attack.
# [star] Boost: If this activation is an attack, place threat on the main
#   scheme equal to the excess damage dealt by this attack.
#
# ⚠ REECRITE LE 18/09/2026 : LA CARTE ETAIT INERTE, ET SES DEUX CAS PASSAIENT.
# La version precedente lisait `AfterUnitAttackEnd.excess_damage`, qui
# N'EXISTE PAS (sender_damage.py:558 : le message porte `total_dealt_damage`,
# `damaged_targets`, `atk_messages`). `getattr(..., 0)` rendait donc toujours
# 0, aucune menace n'etait posee — et les deux cas restaient verts parce que
# Battle in the Bodega (60134b) pose 1 menace de son cote sur la meme attaque.
# C'est la preuve par SUBSTITUTION qui l'a montre : « SUBST 60140 : rouges
# 0/2 », les deux cas verts sans le module.
#
# L'exces n'existe qu'A LA DEFAITE (`WhenUnitBeDefeated.excess_damage`,
# sender_unit.py:70 = `-health` apres coup), comme pour 60135b Bull in a China
# Shop. On ecoute donc la defaite, filtree sur « vaincu par CETTE carte, au
# cours d'une attaque, avec de l'exces » : `by_attack=True`, `attacker="This"`,
# `took_excess_damage=True`. Un personnage vaincu par autre chose, ou sans
# exces, ne declenche rien.
#
# ⚠ « the main scheme » DANS CE SET : il y en a un PAR JOUEUR. La menace tombe
# sur le complot du joueur qui controlait le personnage vaincu (meme regle que
# la manigance de base du vilain, voir __init__.py), et sur « MainScheme » en
# dernier recours.


def PoserLExces(porteur: 'CardFace', message: 'Message.WhenUnitBeDefeated',
                effect: 'Effect') -> None:
    exces = int(message.excess_damage or 0)
    if exces <= 0:
        return
    vaincu = message.trigger
    complot = None
    proprietaire = vaincu.GetControlByOrOwner() if vaincu is not None else None
    if Player.IsType(proprietaire):
        complot = ComplotDuJoueur(effect, proprietaire)
    porteur.PlaceThreatOnSchemes([complot] if complot is not None else "MainScheme",
                                 exces, effect)


def GetAbilities() -> Sequence['Ability']:

    def poser(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        PoserLExces(effect.this, message, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        being = message.being_message
        ennemi = message.activating_enemy
        if being is None or not being.IsAttack() or ennemi is None:
            return
        # ⚠ `unregister_after_exec` est OBLIGATOIRE (mot-cle sans defaut) :
        # sans lui, TypeError avale a chaque boost (autoplay du 18/09/2026).
        # La capacite est posee sur l'ENNEMI QUI S'ACTIVE (« this activation »),
        # pas sur Man-Bull, qui n'est qu'une carte de boost ici.
        ennemi.effect.RegisterTemp(
            AbilityFactory.WhenUnitBeDefeated(
                AbilityType.Temp0,
                Unit2,
                poser,
                by_attack=True,
                attacker="This",
                took_excess_damage=True,
            ),
            unregister_after_exec=True,
            until_phase_end=True,
        )

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.ForcedResponse,
            Unit2,
            poser,
            by_attack=True,
            attacker="This",
            took_excess_damage=True,
        ),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

#### `60141` Change of Venue

```json
{
 "card_id": "60141",
 "type": "Treachery",
 "name": "Change of Venue",
 "subtitle": "",
 "desc": {
  "Boost": "1",
  "Surge": "1"
 },
 "traits": [],
 "set_name": "Protection Racket",
 "text": "Surge.\n<b>When Revealed</b>: Swap your main scheme with a random set-aside main scheme. Place the threat from the previous scheme on the new scheme.\n<hr />\n[star] <b>Boost</b>: Resolve this card's \"When Revealed\" ability."
}
```

Script `src/cards/pack/fne/protection_racket/60141.py` :

```python
from . import *

# Change of Venue — Surge : base desc.
# When Revealed: Swap your main scheme with a random set-aside main scheme.
#   Place the threat from the previous scheme on the new scheme.
# [star] Boost: Resolve this card's "When Revealed" ability.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        EchangerLeComplot(effect, message.GetToPlayer())

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        EchangerLeComplot(effect, message.GetToPlayer())

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

### Set : The Raft Breakout (10 cartes)

#### `60142a` The Raft Breakout

```json
{
 "card_id": "60142a",
 "type": "MainScheme",
 "name": "The Raft Breakout",
 "subtitle": "",
 "desc": {
  "Stage": "1A"
 },
 "traits": [],
 "set_name": "The Raft Breakout",
 "text": "<b>Contents</b>: Chosen [[Underling]] villain <i>(see rulebook p. 5)</i>. Chosen villain's set, The Raft Breakout set, and Standard set. Two modular encounter sets <i>(The Owl and Tombstone)</i>.\n<b>Setup</b>: Attach Master Key to the villain. Each player discards cards from the encounter deck until they discard a [[Prisoner]] minion and reveal that minion."
}
```

Script `src/cards/pack/fne/the_raft_breakout/60142a.py` :

```python
from . import *
from cards.pack.fne.campaign import CapacitesDeCampagne

# The Raft Breakout 1A
# Setup: Attach Master Key to the villain. Each player discards cards from
#   the encounter deck until they discard a PRISONER minion and reveal that
#   minion.
# Master Key est dans la mise de cote du scenario (Find.FindAndAttachTo).

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        vilain = Worlds.FindVillain(effect)
        premier = Worlds.GetFirstPlayer(effect)
        if vilain is not None:
            Find.FindAndAttachTo(effect, vilain, who_perform=premier, name="Master Key", card_type=Attachment)

        def evasion(player: 'Player') -> None:
            face = Worlds.DiscardEncounterCardsUntil(effect, trait="PRISONER", card_type=Minion)
            if face is not None:
                face.Reveal(player, effect)

        Players.ForEachPlayer(effect, evasion)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        # Mode campagne (livret p. 9 et encarts CAMPAIGN INSTRUCTIONS) : inerte
        # hors campagne (`Worlds.IsCampaign`), voir cards/pack/fne/campaign.py.
        *CapacitesDeCampagne("the_raft_breakout"),
    ]
```

#### `60142b` The Raft Breakout

```json
{
 "card_id": "60142b",
 "type": "MainScheme",
 "name": "The Raft Breakout",
 "subtitle": "",
 "desc": {
  "StartingThreat": "2*",
  "TargetThreat": "11*",
  "EscalationThreat": "1*",
  "Stage": "1B"
 },
 "traits": [],
 "set_name": "The Raft Breakout",
 "text": "Each minion gains: \"<b>When Defeated</b>: Remove 1 threat from the main scheme <i>(2 threat instead if this minion has the [[Elite]] trait)</i>.\"\nIf this stage is completed, the players lose the game."
}
```

Script `src/cards/pack/fne/the_raft_breakout/60142b.py` :

```python
from . import *

# The Raft Breakout 1B — 2[per_hero], cible 11[per_hero], +1[per_hero] : bases.
# Each minion gains: "When Defeated: Remove 1 threat from the main scheme
#   (2 threat instead if this minion has the ELITE trait)."
# If this stage is completed, the players lose the game.
# ⚠ GiveAbilityToInPlayWhenApplyThis(Minion, abilities=[...]) ne donne la
# capacite QUE sur un evenement Faceup (environment_helper2.py:213,
# « Fix for 50070 ») : un sbire mis en jeu sans etre retourne (PutIntoPlay,
# Zemo qui convertit un allie...) ne la recoit jamais (harnais 18/09/2026).
# Le complot ecoute donc lui-meme la defaite de chaque sbire : meme resultat,
# et un sbire au texte vide (DECEIVED) garde la capacite, comme le veulent
# les regles (un texte vide n'efface que le texte IMPRIME).

def GetAbilities() -> Sequence['Ability']:

    def evade(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(MainScheme)
        sbire = message.trigger
        n = 2 if sbire.HasTrait("ELITE") else 1
        this.RemoveThreatFromSchemes([this], n, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.ForcedResponse, Minion, evade),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
```

#### `60143` * Master Key

```json
{
 "card_id": "60143",
 "type": "Attachment",
 "name": "* Master Key",
 "subtitle": "",
 "desc": {
  "Permanent": "1"
 },
 "traits": [
  "ITEM"
 ],
 "set_name": "The Raft Breakout",
 "text": "Attach to the villain.\nPermanent.\n[star] <b>Forced Response</b>: After the villain schemes against you, deal each of that activation's boost cards that is a minion to yourself as a facedown encounter card."
}
```

Script `src/cards/pack/fne/the_raft_breakout/60143.py` :

```python
from . import *

# * Master Key (ITEM) — Attach to the villain. Permanent (base).
# [star] Forced Response: After the villain schemes against you, deal each of
#   that activation's boost cards that is a minion to yourself as a facedown
#   encounter card.

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        DistribuerLesBoostsDeCeType(effect, message, Minion, attaque=False, vilain_seulement=True)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.WhenCardBecomeBoost(None, boost),
    ]
```

#### `60144` * Absorbing Man

```json
{
 "card_id": "60144",
 "type": "Minion",
 "name": "* Absorbing Man",
 "subtitle": "",
 "desc": {
  "HP": "6",
  "ATK": "1",
  "SCH": "1",
  "Boost": "3",
  "Villainous": "1"
 },
 "traits": [
  "BRUTE",
  "ELITE",
  "PRISONER"
 ],
 "set_name": "The Raft Breakout",
 "text": "Villainous.\n[star] <b>Forced Interrupt</b>: When Absorbing Man attacks you, tuck the top card of your deck under him. Absorbing Man gets +1 ATK for this attack for each different resource type <i>([energy], [mental], [physical], and [wild])</i> on cards tucked under him."
}
```

Script `src/cards/pack/fne/the_raft_breakout/60144.py` :

```python
from . import *

# * Absorbing Man (BRUTE, ELITE, PRISONER) — Villainous : base.
# [star] Forced Interrupt: When Absorbing Man attacks you, tuck the top card
#   of your deck under him. Absorbing Man gets +1 ATK for this attack for each
#   different resource type ([energy], [mental], [physical], and [wild]) on
#   cards tucked under him.
# FacesCounter.GetPrintedResourcesTypes = nombre de types differents
# (["YY","B","B"] -> 2), le joker compte pour un type.

def GetAbilities() -> Sequence['Ability']:

    def attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetAgainstPlayer()
        if joueur is None:
            return
        dessus = joueur.player_deck.GetTop()
        if dessus is not None:
            this.TuckCardUnderHere(dessus, effect)
        cachees = list(this.GetPlacedCardArea().Get())
        bonus = FacesCounter.GetPrintedResourcesTypes(cachees) if cachees else 0
        if bonus > 0:
            message.GainATKForThisAttack(bonus, effect)

    return [
        AbilityFactory.WhenUnitAttackYou(AbilityType.ForcedInterrupt, "This", attaque),
    ]
```

#### `60145` * Baron Zemo

```json
{
 "card_id": "60145",
 "type": "Minion",
 "name": "* Baron Zemo",
 "subtitle": "",
 "desc": {
  "HP": "6",
  "ATK": "1",
  "SCH": "2",
  "Boost": "3",
  "Villainous": "1"
 },
 "traits": [
  "ELITE",
  "HYDRA",
  "PRISONER"
 ],
 "set_name": "The Raft Breakout",
 "text": "Villainous.\nTreat each ally with threat on it as a [[Deceived]] minion with a blank text box. Its SCH is equal to its base THW and it does not take consequential damage.\n<b>When Revealed</b>: Place 1 threat on an ally without threat on it. It engages its controller."
}
```

Script `src/cards/pack/fne/the_raft_breakout/60145.py` :

```python
from . import *

# * Baron Zemo (ELITE, HYDRA, PRISONER) — Villainous : base.
# Treat each ally with threat on it as a DECEIVED minion with a blank text
#   box. Its SCH is equal to its base THW and it does not take consequential
#   damage.
# When Revealed: Place 1 threat on an ally without threat on it. It engages
#   its controller.
# Gabarit `deceived_minion` (pack "") comme `influenced_minion` (60100).
# ⚠ Harnais du 18/09/2026 : le cadre GiveKeywordToInPlayWhenApplyThis(apply=)
# ne sait pas DEFAIRE la conversion sur retrait du jeton (la face alliee,
# echangee, est ignoree par `is_setting_as` et l'evenement Token(Ally) ne voit
# plus qu'un sbire) ; et TreatAsMinion pose sur Zemo des temporaires qu'on ne
# peut pas retirer. Trois ecouteurs explicites, conversion inline
# (ConvertirEnDeceived / RendreLAllie, __init__.py) :
#   1. jeton threat pose sur un allie -> conversion (et Zemo entre en jeu ->
#      les allies qui en portent deja) ;
#   2. dernier jeton retire d'un sbire DECEIVED -> il redevient allie ;
#   3. Zemo quitte le jeu -> chaque sbire DECEIVED redevient allie, jetons
#      conserves (FAQ du livret) ;
#   4. sbire DECEIVED vaincu -> `Card.CheckIfCanDiscard` remet la face
#      imprimee, l'allie va dans la defausse de son proprietaire (natif).

def GetAbilities() -> Sequence['Ability']:

    def jeton_pose(effect: 'Effect', message: 'Message.AfterCardPlacedToken') -> None:
        ConvertirEnDeceived(message.trigger, effect)

    def allie_avec_menace(effect: 'Effect', message: 'Message.AfterCardPlacedToken') -> bool:
        face = message.trigger
        return message.token_name == 'threat' and Ally.IsType(face) and face.IsInPlay() \
            and face.GetTokens('threat') > 0 and not face.card.IsAsOtherCard()

    def jeton_retire(effect: 'Effect', message: 'Message.AfterCardRemovedToken') -> None:
        RendreLAllie(message.trigger, effect)

    def deceived_sans_menace(effect: 'Effect', message: 'Message.AfterCardRemovedToken') -> bool:
        face = message.trigger
        return message.token_name == 'threat' and EstUnDeceived(face) and face.GetTokens('threat') <= 0

    def entre_en_jeu(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        for allie in list(Worlds.GetOnFieldAllies(effect)):
            if allie.GetTokens('threat') > 0 and not allie.card.IsAsOtherCard():
                ConvertirEnDeceived(allie, effect)

    def quitte_le_jeu(effect: 'Effect', message: 'Message.WhenCardLeavePlay') -> None:
        for sbire in list(Worlds.GetOnFieldMinions(effect)):
            if EstUnDeceived(sbire):
                RendreLAllie(sbire, effect)

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        allies = [a for a in Worlds.GetOnFieldAllies(effect) if a.GetTokens('threat') <= 0]
        if not allies:
            return
        cible = allies[0] if len(allies) == 1 else joueur.AskChooseFace(allies, effect)
        if cible is not None:
            Faces.PlaceTokensOn([cible], 1, 'threat', effect)

    return [
        Ability(AbilityType.NonKeyword, Message.AfterCardPlacedToken, [allie_avec_menace], jeton_pose),
        Ability(AbilityType.NonKeyword, Message.AfterCardRemovedToken, [deceived_sans_menace], jeton_retire),
        AbilityFactory.AfterCardEnterPlay(AbilityType.NonKeyword, "This", entre_en_jeu),
        AbilityFactory.WhenCardLeavePlay(AbilityType.NonKeyword, "This", quitte_le_jeu),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
```

#### `60146` * Drang

```json
{
 "card_id": "60146",
 "type": "Minion",
 "name": "* Drang",
 "subtitle": "",
 "desc": {
  "HP": "6",
  "ATK": "1",
  "SCH": "1",
  "Boost": "3",
  "Villainous": "1"
 },
 "traits": [
  "BADOON",
  "ELITE",
  "PRISONER"
 ],
 "set_name": "The Raft Breakout",
 "text": "Villainous.\n[star] <b>Forced Response</b>: After Drang attacks you, place 1 barrage counter on him. Then, take 1 indirect damage for each barrage counter on Drang."
}
```

Script `src/cards/pack/fne/the_raft_breakout/60146.py` :

```python
from . import *

# * Drang (BADOON, ELITE, PRISONER) — Villainous : base.
# [star] Forced Response: After Drang attacks you, place 1 barrage counter on
#   him. Then, take 1 indirect damage for each barrage counter on Drang.

def GetAbilities() -> Sequence['Ability']:

    def barrage(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Minion)
        Faces.PlaceCountersOn([this], 1, 'barrage', effect)
        joueur = message.GetAgainstPlayer()  # ⚠ pas d'attribut `attacked_you` sur AfterUnitAttackEnd
        if joueur is not None:
            joueur.GetIdentity().TakeIndirectDamage(this, this.GetCounters('barrage'), effect)

    return [
        AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, "This", barrage),
    ]
```

#### `60147` * Mysterio

```json
{
 "card_id": "60147",
 "type": "Minion",
 "name": "* Mysterio",
 "subtitle": "",
 "desc": {
  "HP": "6",
  "ATK": "1",
  "SCH": "2",
  "Boost": "3",
  "Villainous": "1"
 },
 "traits": [
  "CRIMINAL",
  "ELITE",
  "PRISONER"
 ],
 "set_name": "The Raft Breakout",
 "text": "Villainous.\n[star] <b>Forced Response</b>: After Mysterio attacks you, deal each of that activation's boost cards that is a treachery to yourself as a facedown encounter card."
}
```

Script `src/cards/pack/fne/the_raft_breakout/60147.py` :

```python
from . import *

# * Mysterio (CRIMINAL, ELITE, PRISONER) — Villainous : base.
# [star] Forced Response: After Mysterio attacks you, deal each of that
#   activation's boost cards that is a treachery to yourself as a facedown
#   encounter card.

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        DistribuerLesBoostsDeCeType(effect, message, Treachery, attaque=True, vilain_seulement=False)

    return [
        AbilityFactory.WhenCardBecomeBoost(None, boost),
    ]
```

#### `60148` * Proxima Midnight

```json
{
 "card_id": "60148",
 "type": "Minion",
 "name": "* Proxima Midnight",
 "subtitle": "",
 "desc": {
  "HP": "7",
  "ATK": "2",
  "SCH": "1",
  "Boost": "3",
  "Villainous": "1"
 },
 "traits": [
  "BLACK ORDER",
  "ELITE",
  "PRISONER"
 ],
 "set_name": "The Raft Breakout",
 "text": "Villainous.\n[star] <b>Forced Interrupt</b>: When Proxima Midnight attacks you, choose to either place 1 threat on the main scheme, or Proxima Midnight gets +2 ATK for this attack."
}
```

Script `src/cards/pack/fne/the_raft_breakout/60148.py` :

```python
from . import *

# * Proxima Midnight (BLACK ORDER, ELITE, PRISONER) — Villainous : base.
# [star] Forced Interrupt: When Proxima Midnight attacks you, choose to either
#   place 1 threat on the main scheme, or Proxima Midnight gets +2 ATK for
#   this attack.

def GetAbilities() -> Sequence['Ability']:

    def attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetAgainstPlayer()
        if joueur is None:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Place 1 threat on the main scheme", lambda targets: this.PlaceThreatOnSchemes("MainScheme", 1, effect)),
            AbilityFactory.ForChoiceAbility("Proxima Midnight gets +2 ATK for this attack", lambda targets: message.GainATKForThisAttack(2, effect)),
        )

    return [
        AbilityFactory.WhenUnitAttackYou(AbilityType.ForcedInterrupt, "This", attaque),
    ]
```

#### `60149` * Rhino

```json
{
 "card_id": "60149",
 "type": "Minion",
 "name": "* Rhino",
 "subtitle": "",
 "desc": {
  "HP": "7",
  "ATK": "3",
  "SCH": "1",
  "Boost": "3",
  "Toughness": "1",
  "Villainous": "1"
 },
 "traits": [
  "BRUTE",
  "ELITE",
  "PRISONER"
 ],
 "set_name": "The Raft Breakout",
 "text": "Toughness. Villainous.\n[star] Rhino's attacks gain overkill.\n<hr />\n[star] <b>Boost</b>: Give the activating enemy a tough status card."
}
```

Script `src/cards/pack/fne/the_raft_breakout/60149.py` :

```python
from . import *

# * Rhino (BRUTE, ELITE, PRISONER) — Toughness, Villainous : bases.
# [star] Rhino's attacks gain overkill.
# [star] Boost: Give the activating enemy a tough status card.

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Faces.GiveStatus([message.activating_enemy], "Tough", effect)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", overkill=True),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

#### `60150` Imprisoned

```json
{
 "card_id": "60150",
 "type": "Obligation",
 "name": "Imprisoned",
 "subtitle": "",
 "desc": {
  "Boost": "0"
 },
 "traits": [],
 "set_name": "The Raft Breakout",
 "text": "You cannot thwart, attack, or change to alter-ego form.\n<b>Hero Action</b>: Spend 3 resources of any type or exhaust characters you control with a total THW of 3 or more → discard this card.\n<hr />\n[star] <b>Boost</b>: Reveal this card."
}
```

Script `src/cards/pack/fne/the_raft_breakout/60150.py` :

```python
from . import *

# Imprisoned (obligation de rencontre)
# You cannot thwart, attack, or change to alter-ego form.
# Hero Action: Spend 3 resources of any type or exhaust characters you control
#   with a total THW of 3 or more -> discard this card.
# [star] Boost: Reveal this card.
# Modeles : 27133 (PlayersCannotThwartWhile), 11049 (PlayersCannotAttackWhile),
# PlayersCannotChangeForms(to_form=AlterEgo) ; la seconde branche de cout est
# un CostFunc.Custom qui fait choisir des personnages prets jusqu'a 3 THW.

def GetAbilities() -> Sequence['Ability']:

    def defausser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Faces.DiscardAll([effect.this], effect)

    def incliner_pour_trois_thw(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        joueur = effect.GetInitiator()
        prets = [c for c in joueur.GetControlCharacters() if c.IsReady()]
        if sum(c.thwart for c in prets) < 3:
            return False
        choisis: List['CardFace'] = []
        while sum(c.thwart for c in choisis) < 3:
            restants = [c for c in prets if c not in choisis]
            if not restants:
                return False
            c = restants[0] if len(restants) == 1 else joueur.AskChooseFace(restants, effect)
            if c is None:
                return False
            choisis.append(c)
        Faces.ExhaustAll(choisis, effect)
        return True

    def revele(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        if joueur is not None:
            this.Reveal(joueur, effect)

    return [
        AbilityFactory.PlayersCannotThwartWhile("You", None),
        AbilityFactory.PlayersCannotAttackWhile("You", None),
        AbilityFactory.PlayersCannotChangeForms(AbilityType.NonKeyword, "You", to_form=AlterEgo),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, defausser)
            .SetName("Spend 3 resources of any type: discard Imprisoned")
            .SetCost(Cost("3")),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, defausser)
            .SetName("Exhaust characters with a total THW of 3 or more: discard Imprisoned")
            .SetCostFunc(CostFunc.Custom(None, incliner_pour_trois_thw)),
        AbilityFactory.WhenCardBecomeBoost("This", revele),
    ]
```

### Set : Stop the Presses! (9 cartes)

#### `60151a` Stop the Presses!

```json
{
 "card_id": "60151a",
 "type": "MainScheme",
 "name": "Stop the Presses!",
 "subtitle": "",
 "desc": {
  "Stage": "1A"
 },
 "traits": [],
 "set_name": "Stop the Presses!",
 "text": "<b>Contents</b>: Chosen [[Underling]] villain <i>(see rulebook p. 5)</i>. Chosen villain's set, Stop the Presses! set, and Standard set. Two modular encounter sets <i>(Tombstone and Tracksuit Mafia)</i>.\n<b>Setup</b>: Put the Daily Bugle environment into play. Each player puts a random [[Daily Bugle]] support from this encounter set into play under their control. Remove each remaining [[Daily Bugle]] support from the game."
}
```

Script `src/cards/pack/fne/stop_the_presses/60151a.py` :

```python
from . import *
from cards.pack.fne.campaign import CapacitesDeCampagne
import random

# Stop the Presses! 1A
# Setup: Put the Daily Bugle environment into play. Each player puts a random
#   DAILY BUGLE support from this encounter set into play under their
#   control. Remove each remaining DAILY BUGLE support from the game.
# L'environnement et les 4 soutiens sont dans la mise de cote du scenario.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        premier = Worlds.GetFirstPlayer(effect)
        de_cote = list(Worlds.GetSetAsideAreaCards(effect))
        bugle = [f for f in de_cote if f.IsName("Daily Bugle") and Environment.IsType(f)]
        if bugle:
            bugle[0].PutIntoPlay(premier, effect)
        soutiens = [f for f in de_cote if Support.IsType(f) and f.HasTrait("DAILY BUGLE")]

        def distribuer(player: 'Player') -> None:
            if not soutiens:
                return
            choisi = Rand.RandomChoice(soutiens, effect)
            soutiens.remove(choisi)
            choisi.PutIntoPlay(player, effect, under_control=True)

        Players.ForEachPlayer(effect, distribuer)
        if soutiens:
            Faces.RemoveAllFromGame(list(soutiens), effect)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        # Mode campagne (livret p. 9 et encarts CAMPAIGN INSTRUCTIONS) : inerte
        # hors campagne (`Worlds.IsCampaign`), voir cards/pack/fne/campaign.py.
        *CapacitesDeCampagne("stop_the_presses"),
    ]
```

#### `60151b` Stop the Presses!

```json
{
 "card_id": "60151b",
 "type": "MainScheme",
 "name": "Stop the Presses!",
 "subtitle": "",
 "desc": {
  "StartingThreat": "1*",
  "TargetThreat": "9*",
  "EscalationThreat": "1*",
  "Stage": "1B"
 },
 "traits": [],
 "set_name": "Stop the Presses!",
 "text": "<b>Forced Response</b>: After an enemy makes an undefended attack against you, choose:\n• Place 2 threat here <i>(3 threat instead in expert mode)</i>.\n• Remove 1 stamina counter from a [[Daily Bugle]] support you control.\nIf a [[Daily Bugle]] support leaves play or this stage is completed, the players lose the game."
}
```

Script `src/cards/pack/fne/stop_the_presses/60151b.py` :

```python
from . import *

# Stop the Presses! 1B — 1[per_hero], cible 9[per_hero], +1[per_hero] : bases.
# Forced Response: After an enemy makes an undefended attack against you,
#   choose: • Place 2 threat here (3 threat instead in expert mode).
#   • Remove 1 stamina counter from a DAILY BUGLE support you control.
# If a DAILY BUGLE support leaves play or this stage is completed, the
#   players lose the game.
# AfterUnitAttackUnit(Enemy, Identity, is_undefended_attack=True) (60121b) ;
# la seconde branche n'est offerte que si le joueur controle un tel soutien.

def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(MainScheme)
        identite = message.attacked
        joueur = identite.GetControlByPlayer()
        if joueur is None:
            return
        n = 3 if Worlds.IsExpert(effect) else 2

        def menace(targets: Sequence['CardFace']) -> None:
            this.PlaceThreatOnSchemes([this], n, effect)

        def endurance(targets: Sequence['CardFace']) -> None:
            soutiens = SoutiensDailyBugle(effect, joueur)
            if not soutiens:
                return
            cible = soutiens[0] if len(soutiens) == 1 else joueur.AskChooseFace(soutiens, effect)
            if cible is not None:
                RetirerUneEndurance(cible, effect)

        # ⚠ ForChoiceAbility n'a pas de `conditions` : `condition` est un booleen
        # evalue a la construction (juste avant le choix, ce qui suffit ici).
        a_un_soutien = bool(SoutiensDailyBugle(effect, joueur))
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(f"Place {n} threat on Stop the Presses!", menace),
            AbilityFactory.ForChoiceAbility("Remove 1 stamina counter from a Daily Bugle support you control", endurance, condition=a_un_soutien),
        )

    def perdu(effect: 'Effect', message: 'Message.WhenCardLeavePlay') -> None:
        Worlds.SetGameOver(False, effect)

    return [
        AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, Enemy, Identity, apres_attaque, is_undefended_attack=True),
        AbilityFactory.WhenCardLeavePlay(AbilityType.ForcedInterrupt, CardFinder(trait="DAILY BUGLE", card_type=Support), perdu),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
```

#### `60152` Daily Bugle

```json
{
 "card_id": "60152",
 "type": "Environment",
 "name": "Daily Bugle",
 "subtitle": "",
 "desc": {},
 "traits": [],
 "set_name": "Stop the Presses!",
 "text": "<b>Alter-Ego Action</b>: Exhaust a [[Daily Bugle]] support you control → place 1 stamina counter on that support. <i>(Any player can do this.)</i>"
}
```

Script `src/cards/pack/fne/stop_the_presses/60152.py` :

```python
from . import *

# Daily Bugle (environment)
# Alter-Ego Action: Exhaust a DAILY BUGLE support you control -> place 1
#   stamina counter on that support. (Any player can do this.)
# CostFunc.Exhaust(finder) puis `return_exhausted_cards` pour viser CE soutien.

def GetAbilities() -> Sequence['Ability']:
    inclinaison = CostFunc.Exhaust(CardFinder(trait="DAILY BUGLE", card_type=Support))

    def recharge(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        for face in inclinaison.return_exhausted_cards:
            Faces.PlaceCountersOn([face], 1, 'stamina', effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, recharge)
            .SetName("Exhaust a Daily Bugle support you control: place 1 stamina counter on it")
            .SetCostFunc(inclinaison),
    ]
```

#### `60153` * Ben Urich

```json
{
 "card_id": "60153",
 "type": "Support",
 "name": "* Ben Urich",
 "subtitle": "",
 "desc": {
  "Cost": "2",
  "RES": "B",
  "Class": "Encounter",
  "Uses": "3,stamina"
 },
 "traits": [
  "DAILY BUGLE",
  "PERSONA"
 ],
 "set_name": "Stop the Presses!",
 "text": "Uses (3 stamina counters).\n<b>Action</b>: Exhaust Ben Urich and remove 1 stamina counter from him → look at the top 2 cards of the encounter deck. You may discard 1 of those cards. <i>(Put the rest back in the same order.)</i>"
}
```

Script `src/cards/pack/fne/stop_the_presses/60153.py` :

```python
from . import *

# * Ben Urich (DAILY BUGLE, PERSONA, soutien de rencontre) — Uses (3 stamina) : base.
# Action: Exhaust Ben Urich and remove 1 stamina counter from him -> look at
#   the top 2 cards of the encounter deck. You may discard 1 of those cards.
#   (Put the rest back in the same order.)
# joueur.LookAtDeck("EncounterDeck", 2) (bc006 Cat Burglary), choix facultatif.

def GetAbilities() -> Sequence['Ability']:

    def enquete(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        vues = joueur.LookAtDeck("EncounterDeck", 2, effect)
        if not vues:
            return
        # ⚠ L'INTITULE EST OBLIGATOIRE (signalement Yarro n43, 03/10/2026). Sans
        # `prompt`, l'option du choix reprenait le NOM DE LA CAPACITE (« Ben
        # Urich: look at the top 2 cards... ») : le joueur croyait devoir la
        # relancer et ne voyait jamais qu'il s'agissait de defausser. « Discard
        # one » est l'intitule deja employe par 45036 (Magik).
        choisie = joueur.AskChooseFace(list(vues), effect, forced=False, prompt="Discard one")  # « You may » = forced=False (pas de `may`)
        if choisie is not None:
            Faces.DiscardAll([choisie], effect)

    a = AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, enquete).SetName("Ben Urich: look at the top 2 cards of the encounter deck")
    for c in CoutDeReporter():
        a = a.SetCostFunc(c)
    return [a]
```

#### `60154` * Betty Brant

```json
{
 "card_id": "60154",
 "type": "Support",
 "name": "* Betty Brant",
 "subtitle": "",
 "desc": {
  "Cost": "2",
  "RES": "B",
  "Class": "Encounter",
  "Uses": "3,stamina"
 },
 "traits": [
  "DAILY BUGLE",
  "PERSONA"
 ],
 "set_name": "Stop the Presses!",
 "text": "Uses (3 stamina counters).\n<b>Interrupt</b>: When a boost card is turned faceup, exhaust Betty Brant and remove 1 stamina counter from her → cancel that card's boost icons and \"Boost\" ability. Give the activating enemy another boost card for this activation."
}
```

Script `src/cards/pack/fne/stop_the_presses/60154.py` :

```python
from . import *
from game.card.face.attribute.can_boost import CanBoost

# * Betty Brant (DAILY BUGLE, PERSONA) — Uses (3 stamina) : base.
# Interrupt: When a boost card is turned faceup, exhaust Betty Brant and
#   remove 1 stamina counter from her -> cancel that card's boost icons and
#   "Boost" ability. Give the activating enemy another boost card for this
#   activation.
# WhenBoostCardWouldTurnedFaceUp + SetBeInstead : la carte DOIT quitter le
# paquet de boost (defausse), sinon boucle infinie (bc007 Misfortune) ; la
# carte de remplacement est posee face cachee (GiveFacedownBoostCardsInternal,
# 60072 Lady Bullseye).

def GetAbilities() -> Sequence['Ability']:

    def annule(effect: 'Effect', message: 'Message.WhenBoostCardWouldTurnedFaceUp') -> None:
        carte = message.trigger
        message.SetBeInstead(effect)
        if carte is not None:
            Faces.DiscardAll([carte], effect)
        ennemi = message.being_message.by_face if message.being_message is not None else None
        if ennemi is not None and CanBoost.IsType(ennemi):
            ennemi.GiveFacedownBoostCardsInternal(1, effect, message.would_message)

    a = AbilityFactory.WhenBoostCardWouldTurnedFaceUp(AbilityType.Interrupt, annule).SetName("Betty Brant: cancel this boost card, give another")
    for c in CoutDeReporter():
        a = a.SetCostFunc(c)
    return [a]
```

#### `60155` * J. Jonah Jameson

```json
{
 "card_id": "60155",
 "type": "Support",
 "name": "* J. Jonah Jameson",
 "subtitle": "",
 "desc": {
  "Cost": "2",
  "RES": "B",
  "Class": "Encounter",
  "Uses": "3,stamina"
 },
 "traits": [
  "DAILY BUGLE",
  "PERSONA"
 ],
 "set_name": "Stop the Presses!",
 "text": "Uses (3 stamina counters).\n<b>Action</b>: Exhaust J. Jonah Jameson, remove 1 stamina counter from him, and deal yourself 1 facedown encounter card → draw 2 cards."
}
```

Script `src/cards/pack/fne/stop_the_presses/60155.py` :

```python
from . import *

# * J. Jonah Jameson (DAILY BUGLE, PERSONA) — Uses (3 stamina) : base.
# Action: Exhaust J. Jonah Jameson, remove 1 stamina counter from him, and
#   deal yourself 1 facedown encounter card -> draw 2 cards.
# Trois couts : Exhaust, Counter, DealPlayerEncounterCard(1, "Initiator").

def GetAbilities() -> Sequence['Ability']:

    def piocher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        effect.GetInitiator().DrawUp(2, effect)

    a = AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, piocher).SetName("J. Jonah Jameson: deal yourself 1 encounter card, draw 2 cards")
    for c in CoutDeReporter() + [CostFunc.DealPlayerEncounterCard(1, "Initiator")]:
        a = a.SetCostFunc(c)
    return [a]
```

#### `60156` * Robbie Robertson

```json
{
 "card_id": "60156",
 "type": "Support",
 "name": "* Robbie Robertson",
 "subtitle": "",
 "desc": {
  "Cost": "2",
  "RES": "B",
  "Class": "Encounter",
  "Uses": "3,stamina"
 },
 "traits": [
  "DAILY BUGLE",
  "PERSONA"
 ],
 "set_name": "Stop the Presses!",
 "text": "Uses (3 stamina counters).\n<b>Response</b>: After a player is dealt a facedown encounter card, exhaust Robbie Robertson and remove 1 stamina counter from him → look at that encounter card. You may discard it and deal that player another facedown encounter card."
}
```

Script `src/cards/pack/fne/stop_the_presses/60156.py` :

```python
from . import *

# * Robbie Robertson (DAILY BUGLE, PERSONA) — Uses (3 stamina) : base.
# Response: After a player is dealt a facedown encounter card, exhaust Robbie
#   Robertson and remove 1 stamina counter from him -> look at that encounter
#   card. You may discard it and deal that player another facedown encounter
#   card.
# AfterPlayerDealEncounterCard ; la carte = message.would_message.face.

def GetAbilities() -> Sequence['Ability']:

    def relire(effect: 'Effect', message: 'Message.AfterPlayerDealEncounterCard') -> None:
        joueur_vise = message.GetToPlayer()  # TriggerPlayerMessage : pas de `trigger`
        carte = message.would_message.face
        controleur = effect.this.GetControlByPlayer() or joueur_vise
        if carte is None or controleur is None:
            return
        # ⚠ L'INTITULE EST OBLIGATOIRE (meme defaut que Ben Urich 60153,
        # signalement Yarro n43). Sans `prompt`, le choix reprenait le NOM DE LA
        # CAPACITE : rien ne disait qu'on defausse la carte pour en recevoir une autre.
        choix = controleur.AskChooseFace([carte], effect, forced=False, prompt="Discard it and deal another")  # « You may » = forced=False
        if choix is not None:
            Faces.DiscardAll([carte], effect)
            joueur_vise.DealEncounterCards(1, effect)

    a = AbilityFactory.AfterPlayerDealEncounterCard(AbilityType.Response, relire).SetName("Robbie Robertson: look at that encounter card, you may discard it")
    for c in CoutDeReporter():
        a = a.SetCostFunc(c)
    return [a]
```

#### `60157` Exclusive Interview

```json
{
 "card_id": "60157",
 "type": "SideScheme",
 "name": "Exclusive Interview",
 "subtitle": "",
 "desc": {
  "Boost": "1",
  "StartingThreat": "6"
 },
 "traits": [],
 "set_name": "Stop the Presses!",
 "text": "[[Daily Bugle]] supports cannot ready.\n<b>When Revealed</b>: Exhaust each [[Daily Bugle]] support."
}
```

Script `src/cards/pack/fne/stop_the_presses/60157.py` :

```python
from . import *

# Exclusive Interview (side scheme 6)
# DAILY BUGLE supports cannot ready.
# When Revealed: Exhaust each DAILY BUGLE support.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        soutiens = SoutiensDailyBugle(effect)
        if soutiens:
            Faces.ExhaustAll(soutiens, effect)

    return [
        *AbilityFactory.CardCannotReady(CardFinder(trait="DAILY BUGLE", card_type=Support)),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
```

#### `60158` Breaking News

```json
{
 "card_id": "60158",
 "type": "Treachery",
 "name": "Breaking News",
 "subtitle": "",
 "desc": {
  "Boost": "0"
 },
 "traits": [],
 "set_name": "Stop the Presses!",
 "text": "<b>When Revealed</b>: Choose:\n• Exhaust a [[Daily Bugle]] support <i>(under any player's control)</i> and remove 1 stamina counter from it.\n• Place 2 threat on the main scheme.\n<hr />\n[star] <b>Boost</b>: Exhaust a [[Daily Bugle]] support <i>(under any player's control)</i>."
}
```

Script `src/cards/pack/fne/stop_the_presses/60158.py` :

```python
from . import *

# Breaking News
# When Revealed: Choose: • Exhaust a DAILY BUGLE support (under any player's
#   control) and remove 1 stamina counter from it. • Place 2 threat on the
#   main scheme.
# [star] Boost: Exhaust a DAILY BUGLE support (under any player's control).

def ChoisirUnSoutien(effect: 'Effect', joueur: 'Player') -> 'CardFace|None':
    soutiens = SoutiensDailyBugle(effect)
    if not soutiens:
        return None
    return soutiens[0] if len(soutiens) == 1 else joueur.AskChooseFace(soutiens, effect)


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()

        def epuiser(targets: Sequence['CardFace']) -> None:
            cible = ChoisirUnSoutien(effect, joueur)
            if cible is not None:
                Faces.ExhaustAll([cible], effect)
                RetirerUneEndurance(cible, effect)

        # ⚠ ForChoiceAbility n'a pas de `conditions` : booleen a la construction.
        existe = bool(SoutiensDailyBugle(effect))
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Exhaust a Daily Bugle support and remove 1 stamina counter from it", epuiser, condition=existe),
            AbilityFactory.ForChoiceAbility("Place 2 threat on the main scheme", lambda targets: this.PlaceThreatOnSchemes("MainScheme", 2, effect)),
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        cible = ChoisirUnSoutien(effect, message.GetToPlayer())
        if cible is not None:
            Faces.ExhaustAll([cible], effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

### Set : Kingpin (23 cartes)

#### `60159a` * Kingpin

```json
{
 "card_id": "60159a",
 "type": "Villain",
 "name": "* Kingpin",
 "subtitle": "",
 "desc": {
  "HP": "25*",
  "ATK": "0",
  "SCH": "2",
  "Stalwart": "1",
  "Stage": "1"
 },
 "traits": [
  "CRIMINAL"
 ],
 "set_name": "Kingpin",
 "text": "Stalwart.\nKingpin cannot be dealt damage or have upgrades attached. <i>(The players must garner Public Support to face him directly.)</i>\n[star] <b>Forced Interrupt</b>: When Kingpin would attack you, he schemes instead."
}
```

Script `src/cards/pack/fne/kingpin/60159a.py` :

```python
from . import *

# * Kingpin (A1) — SCH 2 / ATK [star] / 25[per_hero], CRIMINAL. Stalwart : base desc.
# Kingpin cannot be dealt damage or have upgrades attached.
# [star] Forced Interrupt: When Kingpin would attack you, he schemes instead.
# Voir CapacitesDeKingpin1.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDeKingpin1()]
```

#### `60159b` * Kingpin

```json
{
 "card_id": "60159b",
 "type": "Villain",
 "name": "* Kingpin",
 "subtitle": "",
 "desc": {
  "HP": "25*",
  "ATK": "2",
  "SCH": "2",
  "Steady": "1",
  "Stage": "2"
 },
 "traits": [
  "CRIMINAL",
  "MARTIAL ARTIST"
 ],
 "set_name": "Kingpin",
 "text": "Steady.\n[star] <b>Forced Interrupt</b>: When Kingpin activates against you, if you are not engaged with a minion, give Kingpin 1 additional boost card for this activation."
}
```

Script `src/cards/pack/fne/kingpin/60159b.py` :

```python
from . import *

# * Kingpin (A2) — SCH 2 / ATK 2 / 25[per_hero], CRIMINAL MARTIAL ARTIST. Steady : base desc.
# [star] Forced Interrupt: When Kingpin activates against you, if you are not
#   engaged with a minion, give Kingpin 1 additional boost card for this activation.
# Voir CapacitesDeKingpin2.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDeKingpin2(overkill=False)]
```

#### `60160a` * Kingpin

```json
{
 "card_id": "60160a",
 "type": "Villain",
 "name": "* Kingpin",
 "subtitle": "",
 "desc": {
  "HP": "28*",
  "ATK": "0",
  "SCH": "3",
  "Stalwart": "1",
  "Stage": "1"
 },
 "traits": [
  "CRIMINAL"
 ],
 "set_name": "Kingpin",
 "text": "Stalwart.\nKingpin cannot be dealt damage or have upgrades attached. <i>(The players must garner Public Support to face him directly.)</i>\n[star] <b>Forced Interrupt</b>: When Kingpin would attack you, he schemes instead."
}
```

Script `src/cards/pack/fne/kingpin/60160a.py` :

```python
from . import *

# * Kingpin (B1, expert) — SCH 3 / ATK [star] / 28[per_hero]. Voir CapacitesDeKingpin1.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDeKingpin1()]
```

#### `60160b` * Kingpin

```json
{
 "card_id": "60160b",
 "type": "Villain",
 "name": "* Kingpin",
 "subtitle": "",
 "desc": {
  "HP": "28*",
  "ATK": "3",
  "SCH": "3",
  "Steady": "1",
  "Stage": "2"
 },
 "traits": [
  "CRIMINAL",
  "MARTIAL ARTIST"
 ],
 "set_name": "Kingpin",
 "text": "Steady.\n[star] <b>Forced Interrupt</b>: When Kingpin activates against you, if you are not engaged with a minion, give Kingpin 1 additional boost card for this activation and this activation gains overkill if it is an attack."
}
```

Script `src/cards/pack/fne/kingpin/60160b.py` :

```python
from . import *

# * Kingpin (B2, expert) — SCH 3 / ATK 3 / 28[per_hero]. Steady : base desc.
# [star] Forced Interrupt: ... give Kingpin 1 additional boost card for this
#   activation and this activation gains overkill if it is an attack.
# Voir CapacitesDeKingpin2(overkill=True).

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDeKingpin2(overkill=True)]
```

#### `60161a` The King's Gambit

```json
{
 "card_id": "60161a",
 "type": "MainScheme",
 "name": "The King's Gambit",
 "subtitle": "",
 "desc": {
  "Stage": "1A"
 },
 "traits": [],
 "set_name": "Kingpin",
 "text": "<b>Contents</b>: Kingpin (A1) <i>(Kingpin (B1) instead for expert mode.)</i> Kingpin encounter set. Two modular encounter sets <i>(Tombstone and Tracksuit Mafia)</i>.\n<b>Setup</b>: Each player reveals their set-aside nemesis minion. Each player whose nemesis minion shares a title with a character in play instead removes their nemesis minion from the game, then finds an [[Underling]] minion that is not in play and reveals it."
}
```

Script `src/cards/pack/fne/kingpin/60161a.py` :

```python
from . import *
from cards.pack.fne.campaign import CapacitesDeCampagneKingpin

# The King's Gambit (1A)
# Setup: Each player reveals their set-aside nemesis minion. Each player whose
#   nemesis minion shares a title with a character in play instead removes
#   their nemesis minion from the game, then finds an UNDERLING minion that is
#   not in play and reveals it.
# Modele : 60121a (WhenCardSetup("This")). « shares a title » = meme nom
# qu'un personnage (Unit2) en jeu, par ex. le sbire Kingpin, nemesis d'Echo.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:

        def par_joueur(joueur: 'Player') -> None:
            for sbire in SbiresNemesisMisDeCote(joueur):
                noms = {c.name for c in Worlds.GetOnFieldCharacters(effect)}
                if sbire.name in noms:
                    Faces.RemoveAllFromGame([sbire], effect)
                    TrouverEtRevelerUnderling(effect, joueur)
                else:
                    sbire.Reveal(joueur, effect)

        Players.ForEachPlayer(effect, par_joueur)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        # Mode campagne (livret p. 9 et encarts CAMPAIGN INSTRUCTIONS) : inerte
        # hors campagne (`Worlds.IsCampaign`), voir cards/pack/fne/campaign.py.
        *CapacitesDeCampagneKingpin(),
    ]
```

#### `60161b` The King's Gambit

```json
{
 "card_id": "60161b",
 "type": "MainScheme",
 "name": "The King's Gambit",
 "subtitle": "",
 "desc": {
  "StartingThreat": "3*",
  "TargetThreat": "11*",
  "EscalationThreat": "1*",
  "Stage": "1B"
 },
 "traits": [],
 "set_name": "Kingpin",
 "text": "<b>When Revealed</b>: Put Public Support into play, LOW side faceup.\n<b>Hero Action</b>: Remove 5 threat from here <i>(4 threat instead in expert mode)</i>. Shuffle the encounter discard pile into the encounter deck, then discard cards from the top of the encounter deck until a minion is discarded and reveal that minion.\nIf this stage is completed, the players lose the game."
}
```

Script `src/cards/pack/fne/kingpin/60161b.py` :

```python
from . import *

# The King's Gambit (1B) — 3[per_hero] depart, 11[per_hero] cible, +1[per_hero].
# When Revealed: Put Public Support into play, LOW side faceup.
# Hero Action: Remove 5 threat from here (4 threat instead in expert mode).
#   Shuffle the encounter discard pile into the encounter deck, then discard
#   cards from the top of the encounter deck until a minion is discarded and
#   reveal that minion.
# If this stage is completed, the players lose the game.
# Modeles : 56096b (When Revealed d'une face 1B), 16073b (Hero Action sur un
# complot principal + IfThisSchemeStageIsCompletedPlayersLoseTheGame), 60095
# (DiscardEncounterCardsUntil + Reveal). Le cout « Remove N threat from here »
# depend du mode : CostFunc.Custom + condition (RECETTES §5).

def GetAbilities() -> Sequence['Ability']:

    def seuil(effect: 'Effect') -> int:
        return 4 if Worlds.IsExpert(effect) else 5

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        face = SetupCards.PutIntoPlay(effect, joueur, name="Public Support", card_type=Environment)
        if face is not None and face.card.face is not face.card.printed_faces[0]:
            face.card.Flip(effect, call_reveal=False)

    def assez_de_menace(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        return effect.this.threat >= seuil(effect)

    def retirer_la_menace(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        this = effect.this.CastTo(MainScheme)
        n = seuil(effect)
        if this.threat < n:
            return False
        retire = this.RemoveThreatFromSchemes([this], n, effect)
        return retire is not None and retire >= n

    def gambit(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        defausse = Worlds.GetEncounterDiscardPileCards(effect)
        if defausse:
            Faces.ShuffleAllTo(defausse, "EncounterDeck", effect)
        sbire = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
        if sbire is not None:
            sbire.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, gambit, conditions=[assez_de_menace])
            .SetName("Remove threat from here: shuffle the discard pile in and reveal a minion")
            .SetCostFunc(CostFunc.Custom(None, retirer_la_menace)),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
```

#### `60162a` Endgame

```json
{
 "card_id": "60162a",
 "type": "MainScheme",
 "name": "Endgame",
 "subtitle": "",
 "desc": {
  "Stage": "2A"
 },
 "traits": [],
 "set_name": "Kingpin",
 "text": "<b>When Revealed</b>: Each player finds their nemesis minion and reveals it. Each player whose nemesis minion did not enter play this way finds an [[Underling]] minion that is not in play and reveals it. In expert mode, the first player finds and reveals the Organized Crime side scheme."
}
```

Script `src/cards/pack/fne/kingpin/60162a.py` :

```python
from . import *

# Endgame (2A)
# When Revealed: Each player finds their nemesis minion and reveals it. Each
#   player whose nemesis minion did not enter play this way finds an UNDERLING
#   minion that is not in play and reveals it. In expert mode, the first player
#   finds and reveals the Organized Crime side scheme.
# Modeles : 01190 Shadow of the Past (nemesis par joueur), Find.FindAndReveal
# (if_no_entered_play : le sbire deja en jeu est « revele » sans entrer en jeu,
# un sbire retire du jeu n'est pas trouve : les deux menent a l'UNDERLING).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:

        def par_joueur(joueur: 'Player') -> None:
            entre = True

            def pas_entre() -> None:
                nonlocal entre
                entre = False

            sbire = Find.FindAndReveal(
                effect, joueur,
                finder=CardFinder(card_type=Minion, is_nemesis=joueur),
                if_no_entered_play=pas_entre,
            )
            if sbire is None or not entre:
                TrouverEtRevelerUnderling(effect, joueur)

        Players.ForEachPlayer(effect, par_joueur)
        if Worlds.IsExpert(effect):
            Find.FindAndReveal(effect, Worlds.GetFirstPlayer(effect),
                               name="Organized Crime", card_type=EncounterSideScheme)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
```

#### `60162b` Endgame

```json
{
 "card_id": "60162b",
 "type": "MainScheme",
 "name": "Endgame",
 "subtitle": "",
 "desc": {
  "StartingThreat": "0*",
  "TargetThreat": "7*",
  "EscalationThreat": "1*",
  "Stage": "2B"
 },
 "traits": [],
 "set_name": "Kingpin",
 "text": "Each minion gains guard.\nIf this stage is completed, the players lose the game."
}
```

Script `src/cards/pack/fne/kingpin/60162b.py` :

```python
from . import *

# Endgame (2B) — 0[per_hero] depart, 7[per_hero] cible, +1[per_hero].
# Each minion gains guard.
# If this stage is completed, the players lose the game.
# Modele : 60097 Purple Man (GiveKeywordToInPlayWhenApplyThis, liste).

def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(card_type=Minion), guard=1),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
```

#### `60163a` Public Support (LOW)

```json
{
 "card_id": "60163a",
 "type": "Environment",
 "name": "Public Support",
 "subtitle": "LOW",
 "desc": {},
 "traits": [],
 "set_name": "Kingpin",
 "text": "<b>Forced Response</b>: After a minion is defeated, place 1 support counter here.\n<b>Forced Interrupt</b>: When the villain phase begins, if there are at least 2[per_hero]+2 support counters here, flip Kingpin and advance the main scheme to stage 2A. Then, flip this card."
}
```

Script `src/cards/pack/fne/kingpin/60163a.py` :

```python
from . import *

# Public Support (LOW) — environnement recto-verso (60163a,60163b), mis en jeu
# par le When Revealed de The King's Gambit 1B.
# Forced Response: After a minion is defeated, place 1 support counter here.
# Forced Interrupt: When the villain phase begins, if there are at least
#   2[per_hero]+2 support counters here, flip Kingpin and advance the main
#   scheme to stage 2A. Then, flip this card.
# Modeles : 60094 (AfterUnitBeDefeated Minion), 60112 Disturbed Psyche
# (card.Flip du vilain), WhenVillainPhaseBegin (nt011), MainScheme.Advance("2A")
# (scheme_main.py:175 -> world.AdvanceMainScheme). Le retournement de
# l'environnement lui-meme : card.Flip (il n'est pas attache, pas de
# RetournerLAttachement) ; les compteurs restent sur la carte (60068a/b).

def GetAbilities() -> Sequence['Ability']:

    def seuil_atteint(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> bool:
        return effect.this.GetCounters('support') >= 2 * Worlds.GetPlayerNumIcon(effect) + 2

    def bascule(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        this = effect.this
        kingpin = TrouverKingpin(effect)
        if kingpin is not None:
            kingpin.card.Flip(effect)
        complot = Worlds.FindMainScheme(effect)
        if complot is not None and complot.printed_stage == 1:
            complot.Advance("2A", effect)
        this.card.Flip(effect, call_reveal=False)

    return [
        ReponseForceeSoutien(),
        AbilityFactory.WhenVillainPhaseBegin(AbilityType.ForcedInterrupt, bascule, conditions=[seuil_atteint]),
    ]
```

#### `60163b` Public Support (HIGH)

```json
{
 "card_id": "60163b",
 "type": "Environment",
 "name": "Public Support",
 "subtitle": "HIGH",
 "desc": {},
 "traits": [],
 "set_name": "Kingpin",
 "text": "<b>Interrupt</b>: When an enemy would be given a facedown boost card, remove 1[per_hero] support counters from here instead.\n<b>Forced Response</b>: After a minion is defeated, place 1 support counter here."
}
```

Script `src/cards/pack/fne/kingpin/60163b.py` :

```python
from . import *

# Public Support (HIGH)
# Interrupt: When an enemy would be given a facedown boost card, remove
#   1[per_hero] support counters from here instead.
# Forced Response: After a minion is defeated, place 1 support counter here.
#
# Fenetre moteur ajoutee le 18/09/2026 pour cette carte :
# Message.WhenEnemyWouldBeGivenBoostCards, envoye par
# CanBoost.GiveFacedownBoostCardsInternal AVANT la pioche, pour TOUTES les
# sources (activation, James Wesley, Bag of Tricks). Fabrique
# AbilityFactory.WhenEnemyWouldBeGivenBoostCards (activate.py) ; l'operation
# retire UNE carte du compte (message.SetNum(num - 1)) et les compteurs.

def GetAbilities() -> Sequence['Ability']:

    def remplacable(effect: 'Effect', message: 'Message.WhenEnemyWouldBeGivenBoostCards') -> bool:
        return message.num > 0 and \
            effect.this.GetCounters('support') >= Worlds.GetPlayerNumIcon(effect)

    def remplacer(effect: 'Effect', message: 'Message.WhenEnemyWouldBeGivenBoostCards') -> None:
        message.SetNum(message.num - 1)
        Faces.RemoveCountersOn([effect.this], Worlds.GetPlayerNumIcon(effect), 'support', effect)

    return [
        AbilityFactory.WhenEnemyWouldBeGivenBoostCards(AbilityType.Interrupt, Enemy, remplacer, conditions=[remplacable]),
        ReponseForceeSoutien(),
    ]
```

#### `60164` Bear Hug

```json
{
 "card_id": "60164",
 "type": "Attachment",
 "name": "Bear Hug",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "Uses": "3,grip"
 },
 "traits": [
  "CONDITION"
 ],
 "set_name": "Kingpin",
 "text": "If Kingpin has the [[Martial Artist]] trait, attach to your hero. Otherwise, this card gains surge.\nUses (3 grip counters).\nYou cannot change to alter-ego form.\n<b>Forced Interrupt</b>: When you would thwart or attack, remove 1 grip counter from here instead."
}
```

Script `src/cards/pack/fne/kingpin/60164.py` :

```python
from . import *

# Bear Hug (CONDITION) — boost 2, Uses (3 grip counters) : base desc.
# If Kingpin has the MARTIAL ARTIST trait, attach to your hero. Otherwise,
#   this card gains surge.
# You cannot change to alter-ego form.
# Forced Interrupt: When you would thwart or attack, remove 1 grip counter
#   from here instead.
# Modeles : 60080 (AttachToFaceWhenPutIntoPlay sur l'identite), 60150
# Imprisoned (PlayersCannotChangeForms to_form=AlterEgo), 60182 Cop
# (WhenUnitWouldScheme + SetBeInstead) transpose a WhenUnitWouldAttack /
# WhenUnitWouldThwart("You"). La condition « Kingpin MARTIAL ARTIST » va sur
# le selecteur (check_effect_fn), pour que le « cannot » declenche le surge.

def GetAbilities() -> Sequence['Ability']:

    def kingpin_arts_martiaux(effect: 'Effect', face: 'CardFace') -> bool:
        return KingpinArtMartial(effect)

    def au_lieu(effect: 'Effect', message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldThwart') -> None:
        message.SetBeInstead(effect)
        Faces.RemoveCountersOn([effect.this], 1, 'grip', effect)

    selecteur = Select.From("YourHero")
    selecteur.selector_filter.AddParameter(check_effect_fn=kingpin_arts_martiaux)
    selecteur.selector_range.SetRange("All")

    def surge(effect: 'Effect', joueur: 'Player') -> None:
        ThisCardGainSurge(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlayInternal(
            selecteur,
            conditions=[lambda effect, message: not effect.this.card.area.flags.is_upgrades],
            if_cannot_operation=surge,
        ),
        AbilityFactory.PlayersCannotChangeForms(AbilityType.NonKeyword, "You", to_form=AlterEgo),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "You", au_lieu),
        AbilityFactory.WhenUnitWouldThwart(AbilityType.ForcedInterrupt, "You", au_lieu),
    ]
```

#### `60165` * James Wesley

```json
{
 "card_id": "60165",
 "type": "Attachment",
 "name": "* James Wesley",
 "subtitle": "",
 "desc": {
  "Boost": "0",
  "SCH+": "1"
 },
 "traits": [
  "PERSONA"
 ],
 "set_name": "Kingpin",
 "text": "<b>When Revealed</b>: Attach to Kingpin and give him a facedown boost card.\n<b>Hero Action</b>: Discard a [[Thwart]] event from your hand → discard James Wesley. Kingpin schemes.\n<hr />\n[star] <b>Boost</b>: Attach this card to Kingpin."
}
```

Script `src/cards/pack/fne/kingpin/60165.py` :

```python
from . import *

# * James Wesley (PERSONA) — +1 SCH (desc SCH+), boost [star] seule.
# When Revealed: Attach to Kingpin and give him a facedown boost card.
# Hero Action: Discard a THWART event from your hand -> discard James Wesley.
#   Kingpin schemes.
# [star] Boost: Attach this card to Kingpin.
# Voir CapacitesDUnePersona. « give him a facedown boost card » hors activation :
# GiveFacedownBoostCardsInternal(1, effect, None) (la carte attend sa prochaine
# activation dans sa pile de boost, comme 56091 / 60094).

def GetAbilities() -> Sequence['Ability']:

    def carte_boost(effect: 'Effect', joueur: 'Player', kingpin: 'Villain') -> None:
        kingpin.CastTo(CanBoost).GiveFacedownBoostCardsInternal(1, effect, None)

    def manigance(effect: 'Effect', joueur: 'Player', kingpin: 'Villain') -> None:
        kingpin.DoSchemes(joueur, effect)

    return [
        *CapacitesDUnePersona("THWART", "Discard a Thwart event: discard James Wesley, Kingpin schemes",
                              carte_boost, manigance),
    ]
```

#### `60166` * Kingpin's Cane

```json
{
 "card_id": "60166",
 "type": "Attachment",
 "name": "* Kingpin's Cane",
 "subtitle": "",
 "desc": {
  "Boost": "1",
  "ATK+": "1"
 },
 "traits": [
  "WEAPON"
 ],
 "set_name": "Kingpin",
 "text": "<b>When Revealed</b>: Attach to Kingpin. You are stunned.\n<b>Forced Response</b>: After Kingpin attacks and damages a hero, stun that hero. If a hero is stunned this way, discard this card.\n<hr />\n[star] <b>Boost</b>: You are stunned. If you were already stunned, take 1 damage."
}
```

Script `src/cards/pack/fne/kingpin/60166.py` :

```python
from . import *

# * Kingpin's Cane (WEAPON) — +1 ATK (desc ATK+), boost [star]+1.
# When Revealed: Attach to Kingpin. You are stunned.
# Forced Response: After Kingpin attacks and damages a hero, stun that hero.
#   If a hero is stunned this way, discard this card.
# [star] Boost: You are stunned. If you were already stunned, take 1 damage.
# Modeles : ReponseForceeCoupDeBoule (60086, AfterUnitAttackAndDamageUnit),
# retour de Faces.GiveStatus (19001a : compte les unites servies, un Stalwart
# refuse en silence), 08029 (identity.TakeDamage(this, 1, effect)).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Faces.GiveStatus([message.GetToPlayer().GetIdentity()], "Stunned", effect)

    def coup_de_canne(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this
        cible = message.attacked
        if Faces.GiveStatus([cible], "Stunned", effect) > 0:
            Faces.DiscardAll([this], effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        identite = message.GetToPlayer().GetIdentity()
        deja = identite.IsStunned()
        Faces.GiveStatus([identite], "Stunned", effect)
        if deja:
            identite.TakeDamage(this, 1, effect)

    return [
        AttacheAKingpin(),
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            CardFinder(name="Kingpin", card_type=Villain),
            Hero,
            coup_de_canne,
            target_in_play=True,
        ),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

#### `60167` Mountain of Muscle

```json
{
 "card_id": "60167",
 "type": "Attachment",
 "name": "Mountain of Muscle",
 "subtitle": "",
 "desc": {
  "Boost": "2"
 },
 "traits": [
  "CONDITION"
 ],
 "set_name": "Kingpin",
 "text": "If Kingpin has the [[Martial Artist]] trait, attach to Kingpin. Otherwise, this card gains surge.\nKingpin gains retaliate 1.\n<b>Forced Interrupt</b>: When Kingpin would take any amount of damage, place it here instead. Then, if there is 8 or more damage here, discard this card."
}
```

Script `src/cards/pack/fne/kingpin/60167.py` :

```python
from . import *

# Mountain of Muscle (CONDITION) — boost 2.
# If Kingpin has the MARTIAL ARTIST trait, attach to Kingpin. Otherwise, this
#   card gains surge.
# Kingpin gains retaliate 1.
# Forced Interrupt: When Kingpin would take any amount of damage, place it
#   here instead. Then, if there is 8 or more damage here, discard this card.
# Modeles : CapacitesDUnVehicule (drive, seuil + if_cannot_gain_surge), 03009
# (GiveKeywordToAttached retaliate).

def GetAbilities() -> Sequence['Ability']:

    def encaisse(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)
        total = message.will_take_damage
        if total <= 0:
            return
        message.PreventDamage("All", effect)
        Faces.PlaceCountersOn([this], total, 'damage', effect)
        if this.GetCounters('damage') >= 8:
            Faces.DiscardAll([this], effect)

    def le_porteur(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this.CastTo(Attachment)
        return message.trigger is this.GetBindFace()

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name="Kingpin", card_type=Villain, trait=TRAIT_ARTS_MARTIAUX),
            if_cannot_gain_surge=True,
        ),
        *AbilityFactory.GiveKeywordToAttached("Character", retaliate=1),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, Villain, encaisse, conditions=[le_porteur]),
    ]
```

#### `60168` * Vanessa Fisk

```json
{
 "card_id": "60168",
 "type": "Attachment",
 "name": "* Vanessa Fisk",
 "subtitle": "",
 "desc": {
  "Boost": "0",
  "SCH+": "1"
 },
 "traits": [
  "PERSONA"
 ],
 "set_name": "Kingpin",
 "text": "<b>When Revealed</b>: Attach to Kingpin. You are confused.\n<b>Hero Action</b>: Discard an [[Attack]] event from your hand → discard Vanessa Fisk. Kingpin attacks you.\n<hr />\n[star] <b>Boost</b>: You are confused. If you were already confused, place 1 threat on the main scheme."
}
```

Script `src/cards/pack/fne/kingpin/60168.py` :

```python
from . import *

# * Vanessa Fisk (PERSONA) — +1 SCH (desc SCH+), boost [star] seule.
# When Revealed: Attach to Kingpin. You are confused.
# Hero Action: Discard an ATTACK event from your hand -> discard Vanessa Fisk.
#   Kingpin attacks you.
# [star] Boost: You are confused. If you were already confused, place 1 threat
#   on the main scheme.
# Voir CapacitesDUnePersona ; « Kingpin attacks you » = DoAttackYou (60118).

def GetAbilities() -> Sequence['Ability']:

    def confus(effect: 'Effect', joueur: 'Player', kingpin: 'Villain') -> None:
        Faces.GiveStatus([joueur.GetIdentity()], "Confused", effect)

    def attaque(effect: 'Effect', joueur: 'Player', kingpin: 'Villain') -> None:
        kingpin.DoAttackYou(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        identite = message.GetToPlayer().GetIdentity()
        deja = identite.IsConfused()
        Faces.GiveStatus([identite], "Confused", effect)
        if deja:
            this.PlaceThreatOnSchemes("MainScheme", 1, effect)

    return [
        *CapacitesDUnePersona("ATTACK", "Discard an Attack event: discard Vanessa Fisk, Kingpin attacks you",
                              confus, attaque),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

#### `60169` * Black Cat

```json
{
 "card_id": "60169",
 "type": "Minion",
 "name": "* Black Cat",
 "subtitle": "",
 "desc": {
  "HP": "6",
  "ATK": "1",
  "SCH": "1",
  "Boost": "2",
  "Villainous": "1"
 },
 "traits": [
  "THIEF",
  "UNDERLING"
 ],
 "set_name": "Kingpin",
 "text": "Villainous.\nWhile there is 4 threat here, treat Black Cat as an ally that takes 2 consequential damage after she attacks or thwarts.\n<b>Hero Action</b>: Spend a [mental] resource → place 1 threat here. If there is 4 threat here, take control of Black Cat as an ally."
}
```

Script `src/cards/pack/fne/kingpin/60169.py` :

```python
from . import *

# * Black Cat (THIEF UNDERLING) — SCH 1 / ATK 1 / 6 PV, boost 2. Villainous : base.
# While there is 4 threat here, treat Black Cat as an ally that takes 2
#   consequential damage after she attacks or thwarts.
# Hero Action: Spend a [mental] resource -> place 1 threat here. If there is 4
#   threat here, take control of Black Cat as an ally.
# La menace sur un sbire est un JETON 'threat' (60145 Baron Zemo, jetons sur
# un allie ; harnais : cle `jetons`). La seule source de menace « here » est
# l'action : la conversion se fait a ce moment (ConvertirBlackCatEnAlliee).
# Alliee, elle garde Villainous (FAQ du livret) : le gabarit fne_black_cat_ally
# le porte, et un allie villainous recoit une carte boost a chaque attaque.

def GetAbilities() -> Sequence['Ability']:

    def placer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Minion)
        joueur = effect.GetInitiator()
        Faces.PlaceTokensOn([this], 1, 'threat', effect)
        if this.GetTokens('threat') >= 4:
            ConvertirBlackCatEnAlliee(this, joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, placer)
            .SetName("Spend a mental resource: place 1 threat on Black Cat")
            .SetCost(Cost("B")),
    ]
```

#### `60170` * Diamondback

```json
{
 "card_id": "60170",
 "type": "Minion",
 "name": "* Diamondback",
 "subtitle": "",
 "desc": {
  "HP": "6",
  "ATK": "1",
  "SCH": "1",
  "Boost": "2",
  "Villainous": "1"
 },
 "traits": [
  "CRIMINAL",
  "UNDERLING"
 ],
 "set_name": "Kingpin",
 "text": "Villainous.\n[star] <b>Forced Interrupt</b>: When Diamondback attacks you, take 1 damage.\n<hr />\n[star] <b>Boost</b>: Take 1 damage."
}
```

Script `src/cards/pack/fne/kingpin/60170.py` :

```python
from . import *

# * Diamondback (CRIMINAL UNDERLING) — SCH 1 / ATK 1 / 6 PV, boost [star]+2. Villainous : base.
# [star] Forced Interrupt: When Diamondback attacks you, take 1 damage.
# [star] Boost: Take 1 damage.
# Modeles : 60144 (« When X attacks you » = WhenUnitWouldAttack "This"), 08029
# (identity.TakeDamage(this, 1, effect)) ; en boost, le joueur est
# message.GetToPlayer().

def GetAbilities() -> Sequence['Ability']:

    def un_degat(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this
        joueur = message.GetAgainstPlayer()
        if joueur is not None:
            joueur.GetIdentity().TakeDamage(this, 1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        message.GetToPlayer().GetIdentity().TakeDamage(this, 1, effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", un_degat),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

#### `60171` * Spot

```json
{
 "card_id": "60171",
 "type": "Minion",
 "name": "* Spot",
 "subtitle": "",
 "desc": {
  "HP": "5",
  "ATK": "2",
  "SCH": "2",
  "Boost": "3"
 },
 "traits": [
  "CRIMINAL",
  "UNDERLING"
 ],
 "set_name": "Kingpin",
 "text": "Enters play with 1 spot counter on him.\n<b>Forced Interrupt</b>: When Spot would be dealt damage from an attack, if there is at least 1 spot counter here, remove 1 spot counter from here and deal that damage to the attacker instead. Otherwise, place 1 spot counter here."
}
```

Script `src/cards/pack/fne/kingpin/60171.py` :

```python
from . import *

# * Spot (CRIMINAL UNDERLING) — SCH 2 / ATK 2 / 5 PV, boost 3.
# Enters play with 1 spot counter on him.
# Forced Interrupt: When Spot would be dealt damage from an attack, if there is
#   at least 1 spot counter here, remove 1 spot counter from here and deal that
#   damage to the attacker instead. Otherwise, place 1 spot counter here.
# Modeles : sr015 Mysterio (ThisEnterPlayWithCounters + WhenUnitWouldTakeDamage
# "This" + PreventDamage("All")), l'attaquant = message.would_atk_message.attacker.

def GetAbilities() -> Sequence['Ability']:

    def portail(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Minion)
        if this.GetCounters('spot') >= 1:
            total = message.will_take_damage
            message.PreventDamage("All", effect)
            Faces.RemoveCountersOn([this], 1, 'spot', effect)
            attaque = message.would_atk_message
            attaquant = attaque.attacker if attaque is not None else None
            if attaquant is not None and total > 0:
                this.DealDamage([attaquant], total, effect)
        else:
            Faces.PlaceCountersOn([this], 1, 'spot', effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(1, 'spot'),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, "This", portail, is_from_attack=True),
    ]
```

#### `60172` * Stilt-Man

```json
{
 "card_id": "60172",
 "type": "Minion",
 "name": "* Stilt-Man",
 "subtitle": "",
 "desc": {
  "HP": "4",
  "ATK": "1",
  "SCH": "1",
  "Boost": "3"
 },
 "traits": [
  "CRIMINAL",
  "UNDERLING"
 ],
 "set_name": "Kingpin",
 "text": "Enters play with 2 stilt counters on him.\n[star] Stilt-Man gets +1 SCH and +1 ATK for each stilt counter on him.\n<b>Forced Interrupt</b>: When Stilt-Man would take any amount of damage, remove 1 stilt counter from him instead."
}
```

Script `src/cards/pack/fne/kingpin/60172.py` :

```python
from . import *

# * Stilt-Man (CRIMINAL UNDERLING) — SCH 1 / ATK 1 / 4 PV, boost 3.
# Enters play with 2 stilt counters on him.
# [star] Stilt-Man gets +1 SCH and +1 ATK for each stilt counter on him.
# Forced Interrupt: When Stilt-Man would take any amount of damage, remove 1
#   stilt counter from him instead.
# Modeles : sr015 Mysterio (compteurs a l'entree, degats remplaces tant qu'il
# reste un pion), dt133 (ThisGainKeyword dynamique, rafraichi par
# OnEvent.Counter("This", 'stilt')).

def GetAbilities() -> Sequence['Ability']:

    def pions(effect: 'Effect', ui: List['CardFace']) -> int:
        return effect.this.GetCounters('stilt')

    def a_un_pion(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        return effect.this.GetCounters('stilt') > 0

    def un_pion_au_lieu(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage("All", effect)
        Faces.RemoveCountersOn([effect.this], 1, 'stilt', effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(2, 'stilt'),
        AbilityFactory.ThisGainKeyword(pions, attack=1, scheme=1, change_on_event=OnEvent.Counter("This", 'stilt')),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, "This", un_pion_au_lieu, conditions=[a_un_pion]),
    ]
```

#### `60173` Kingpin's Influence

```json
{
 "card_id": "60173",
 "type": "SideScheme",
 "name": "Kingpin's Influence",
 "subtitle": "",
 "desc": {
  "Boost": "3",
  "StartingThreat": "2*",
  "Hazard": "1"
 },
 "traits": [],
 "set_name": "Kingpin",
 "text": "<b>When Defeated</b>: The player who defeated this scheme places 3 threat on their nemesis side scheme. If it is not in play, they find it and reveal it."
}
```

Script `src/cards/pack/fne/kingpin/60173.py` :

```python
from . import *

# Kingpin's Influence (side scheme) — 2[per_hero], boost 3, Hazard : base desc.
# When Defeated: The player who defeated this scheme places 3 threat on their
#   nemesis side scheme. If it is not in play, they find it and reveal it.
# Modeles : 60113a (WhenSchemeBeDefeated WhenDefeated), message.GetDefeatingPlayer,
# CardFinder(card_type=EncounterSideScheme, is_nemesis=joueur) (checker.py:304),
# Find.FindAndReveal (fouille la reserve nemesis). Lecture litterale : en jeu ->
# 3 menaces ; sinon -> trouvee et revelee (sa menace de depart), sans les 3.

def GetAbilities() -> Sequence['Ability']:

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this
        joueur = message.GetDefeatingPlayer()
        finder = CardFinder(card_type=EncounterSideScheme, is_nemesis=joueur)
        complot = Worlds.FindCardOnField(effect, finder=finder)
        if complot is not None:
            this.PlaceThreatOnSchemes([complot], 3, effect)
        else:
            Find.FindAndReveal(effect, joueur, finder=finder)

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
```

#### `60174` Organized Crime

```json
{
 "card_id": "60174",
 "type": "SideScheme",
 "name": "Organized Crime",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "StartingThreat": "3*"
 },
 "traits": [],
 "set_name": "Kingpin",
 "text": "Each minion gets +2 hit points."
}
```

Script `src/cards/pack/fne/kingpin/60174.py` :

```python
from . import *

# Organized Crime (side scheme) — 3[per_hero], boost 2.
# Each minion gets +2 hit points.
# Modele : 60097 Purple Man (GiveKeywordToInPlayWhenApplyThis, liste), health=2.

def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(card_type=Minion), health=2),
    ]
```

#### `60175` Bag of Tricks

```json
{
 "card_id": "60175",
 "type": "Treachery",
 "name": "Bag of Tricks",
 "subtitle": "",
 "desc": {
  "Boost": "0"
 },
 "traits": [],
 "set_name": "Kingpin",
 "text": "<b>When Revealed</b>: Reveal a random card from your set-aside nemesis set. If no card is revealed this way, this card gains surge.\n<hr />\n[star] <b>Boost</b>: Give this character a random card from your set-aside nemesis set as an additional boost card."
}
```

Script `src/cards/pack/fne/kingpin/60175.py` :

```python
from . import *

# Bag of Tricks (treachery) — boost [star] seule.
# When Revealed: Reveal a random card from your set-aside nemesis set. If no
#   card is revealed this way, this card gains surge.
# [star] Boost: Give this character a random card from your set-aside nemesis
#   set as an additional boost card.
# Modeles : 01190 Shadow of the Past (player.set_aside_nemesis_sets),
# Rand.RandomChoice (60112), CanBoost.GiveBoostCard (60094 : la carte rejoint la
# pile de boost, la boucle de ResolveBoostCards la retourne dans la foulee).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        cartes = CartesNemesisMisesDeCote(joueur)
        if not cartes:
            ThisCardGainSurge(effect)
            return
        carte = Rand.RandomChoice(cartes, effect)
        if carte.Reveal(joueur, effect) is None:
            ThisCardGainSurge(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        ennemi = message.activating_enemy
        cartes = CartesNemesisMisesDeCote(joueur)
        if not cartes or ennemi is None or not CanBoost.IsType(ennemi):
            return
        carte = Rand.RandomChoice(cartes, effect)
        ennemi.GiveBoostCard(carte, effect, getattr(message, 'would_atk_message', None))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

#### `60176` Unrelenting Hate

```json
{
 "card_id": "60176",
 "type": "Treachery",
 "name": "Unrelenting Hate",
 "subtitle": "",
 "desc": {
  "Boost": "1"
 },
 "traits": [],
 "set_name": "Kingpin",
 "text": "<b>When Revealed</b>: Your nemesis minion activates against you. If your nemesis minion is not in play, find it and reveal it. If you cannot find it, find an [[Underling]] minion that is not in play and reveal it.\n<hr />\n[star] <b>Boost</b>: If this activation is an attack, it gains overkill."
}
```

Script `src/cards/pack/fne/kingpin/60176.py` :

```python
from . import *

# Unrelenting Hate (treachery) — boost [star]+1.
# When Revealed: Your nemesis minion activates against you. If your nemesis
#   minion is not in play, find it and reveal it. If you cannot find it, find an
#   UNDERLING minion that is not in play and reveal it.
# [star] Boost: If this activation is an attack, it gains overkill.
# Modeles : 60074 (DoActivate), Find.FindAndReveal (fouille deck, defausse,
# mise de cote, jamais la zone retiree), an013 (GainOverKill en boost).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        sbire = SbireNemesisEnJeu(joueur, effect)
        if sbire is not None:
            sbire.DoActivate(joueur, effect)
            return
        trouve = Find.FindAndReveal(effect, joueur, finder=CardFinder(card_type=Minion, is_nemesis=joueur))
        if trouve is None:
            TrouverEtRevelerUnderling(effect, joueur)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        attaque = getattr(message, 'would_atk_message', None)
        if attaque is not None:
            attaque.GainOverKill(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

### Set : Disasters (5 cartes)

#### `60177` Mystic Incursion

```json
{
 "card_id": "60177",
 "type": "Environment",
 "name": "Mystic Incursion",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "Crisis": "1",
  "Uses": "2,civilian"
 },
 "traits": [
  "DISASTER"
 ],
 "set_name": "Disasters",
 "text": "Uses (2 civilian counters).\n<b>Hero Action</b>: Spend [mental] [mental] resources or exhaust a hero or ally you control → remove 1 civilian counter from here <i>(2 counters instead if you exhausted a [[Mystic]] character)</i>."
}
```

Script `src/cards/pack/fne/disasters/60177.py` :

```python
from . import *

# Mystic Incursion (DISASTER, environment, crisis) — Uses (2 civilian counters).
# Hero Action: Spend [mental][mental] resources or exhaust a hero or ally you
#   control -> remove 1 civilian counter from here (2 counters instead if you
#   exhausted a MYSTIC character).

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDeCatastrophe("BB", "[mental][mental]", lambda f: f.HasTrait("MYSTIC"))]
```

#### `60178` Sinking Ferry

```json
{
 "card_id": "60178",
 "type": "Environment",
 "name": "Sinking Ferry",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "Crisis": "1",
  "Uses": "2,civilian"
 },
 "traits": [
  "DISASTER"
 ],
 "set_name": "Disasters",
 "text": "Uses (2 civilian counters).\n<b>Hero Action</b>: Spend [energy] [energy] resources or exhaust a hero or ally you control → remove 1 civilian counter from here <i>(2 counters instead if you exhausted an [[Aerial]] character)</i>."
}
```

Script `src/cards/pack/fne/disasters/60178.py` :

```python
from . import *

# Sinking Ferry (DISASTER) — Uses (2 civilian counters).
# Hero Action: Spend [energy][energy] resources or exhaust a hero or ally you
#   control -> remove 1 civilian counter (2 instead if you exhausted an AERIAL
#   character).

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDeCatastrophe("YY", "[energy][energy]", lambda f: f.HasTrait("AERIAL"))]
```

#### `60179` Towering Inferno

```json
{
 "card_id": "60179",
 "type": "Environment",
 "name": "Towering Inferno",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "Crisis": "1",
  "Uses": "2,civilian"
 },
 "traits": [
  "DISASTER"
 ],
 "set_name": "Disasters",
 "text": "Uses (2 civilian counters).\n<b>Hero Action</b>: Spend [physical] [physical] resources or exhaust a hero or ally you control → remove 1 civilian counter from here <i>(2 counters instead if you exhausted a character that has a tough status card)</i>."
}
```

Script `src/cards/pack/fne/disasters/60179.py` :

```python
from . import *

# Towering Inferno (DISASTER) — Uses (2 civilian counters).
# Hero Action: Spend [physical][physical] resources or exhaust a hero or ally
#   you control -> remove 1 civilian counter (2 instead if you exhausted a
#   character that has a tough status card).
# ⚠ « has a tough status card » lu AU MOMENT du cout : incliner ne retire pas
# la robustesse, la lecture apres inclinaison est donc fidele.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDeCatastrophe("RR", "[physical][physical]", lambda f: f.IsTough())]
```

#### `60180` Collapsing Bridge

```json
{
 "card_id": "60180",
 "type": "SideScheme",
 "name": "Collapsing Bridge",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "StartingThreat": "1",
  "Hinder": "2*",
  "Hazard": "1"
 },
 "traits": [],
 "set_name": "Disasters",
 "text": "[star] Hinder 2[per_hero].\n<b>Forced Response</b>: After any amount of threat is removed from Collapsing Bridge, place 1 threat here."
}
```

Script `src/cards/pack/fne/disasters/60180.py` :

```python
from . import *

# Collapsing Bridge (side scheme, 1, hazard) — [star] Hinder 2[per_hero] : base.
# Forced Response: After any amount of threat is removed from Collapsing
#   Bridge, place 1 threat here.
# AfterSchemeRemoveThreat("This") ; « any amount » : la valeur retiree > 0.
# ⚠ Le moteur envoie AfterSchemeRemoveThreat AVANT de constater la defaite
# (scheme.py:145-150) : sans garde, un pont ramene a 0 recevait 1 menace et
# n'etait JAMAIS vaincu (harnais du 18/09/2026). Un complot annexe est vaincu
# des que sa derniere menace part (RRG « Defeated ») : la reponse ne resout
# que s'il reste de la menace, donc si le pont est encore en jeu.

def GetAbilities() -> Sequence['Ability']:

    def rechute(effect: 'Effect', message: 'Message.AfterSchemeRemoveThreat') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        this.PlaceThreatOnSchemes([this], 1, effect)

    def au_moins_une(effect: 'Effect', message: 'Message.AfterSchemeRemoveThreat') -> bool:
        return getattr(message, "value", 1) > 0

    def encore_de_la_menace(effect: 'Effect', message: 'Message.AfterSchemeRemoveThreat') -> bool:
        return effect.this.CastTo(EncounterSideScheme).threat > 0

    return [
        AbilityFactory.AfterSchemeRemoveThreat(AbilityType.ForcedResponse, "This", rechute, conditions=[au_moins_une, encore_de_la_menace]),
    ]
```

#### `60181` Bystanders in Peril

```json
{
 "card_id": "60181",
 "type": "Treachery",
 "name": "Bystanders in Peril",
 "subtitle": "",
 "desc": {
  "Boost": "1",
  "Peril": "1"
 },
 "traits": [],
 "set_name": "Disasters",
 "text": "Peril.\n<b>When Revealed</b>: Place 1 civilian counter on a [[Disaster]] environment. If no counter was placed this way, search the encounter deck and discard pile for a [[Disaster]] environment and reveal it.\n<hr />\n[star] <b>Boost</b>: Place 1 civilian counter on a [[Disaster]] environment."
}
```

Script `src/cards/pack/fne/disasters/60181.py` :

```python
from . import *

# Bystanders in Peril — Peril : base desc.
# When Revealed: Place 1 civilian counter on a DISASTER environment. If no
#   counter was placed this way, search the encounter deck and discard pile
#   for a DISASTER environment and reveal it.
# [star] Boost: Place 1 civilian counter on a DISASTER environment.
# Modeles : 60109 (Search.SearchForCard deck + defausse), choix du joueur par
# AskChooseFace quand plusieurs catastrophes sont en jeu.

def PoserUnCivil(effect: 'Effect', joueur: 'Player') -> bool:
    envs = Worlds.FindCardsOnField(effect, trait="DISASTER", card_type=Environment)
    if not envs:
        return False
    cible = envs[0] if len(envs) == 1 else joueur.AskChooseFace(list(envs), effect)
    if cible is None:
        return False
    Faces.PlaceCountersOn([cible], 1, 'civilian', effect)
    return True


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if PoserUnCivil(effect, joueur):
            return
        face = Search.SearchForCard(
            effect, joueur,
            include_encounter_deck=True, include_encounter_discard_pile=True,
            trait="DISASTER", card_type=Environment,
        )
        if face:
            face.Reveal(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        PoserUnCivil(effect, message.GetToPlayer())

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

### Set : Cops (4 cartes)

#### `60182` Cop

```json
{
 "card_id": "60182",
 "type": "Minion",
 "name": "Cop",
 "subtitle": "",
 "desc": {
  "HP": "3",
  "ATK": "2",
  "SCH": "0",
  "Boost": "0",
  "Quickstrike": "1",
  "Vulnerable": "1"
 },
 "traits": [
  "POLICE"
 ],
 "set_name": "Cops",
 "text": "Quickstrike. Vulnerable.\n[star] <b>Forced Interrupt</b>: When Cop would scheme, it attacks the villain instead.\n<b>When Defeated</b>: Place 2 threat on the main scheme."
}
```

Script `src/cards/pack/fne/cops/60182.py` :

```python
from . import *

# Cop (POLICE) — Quickstrike, Vulnerable : bases automatiques.
# [star] Forced Interrupt: When Cop would scheme, it attacks the villain instead.
# When Defeated: Place 2 threat on the main scheme.
#
# « instead » = message.SetBeInstead sur WhenUnitWouldScheme (RECETTES §2),
# puis une attaque de base contre le vilain (BasicAttack, modele 50096 Leaping
# Kick pour un ennemi qui frappe une unite precise).

def GetAbilities() -> Sequence['Ability']:

    def attaque_le_vilain(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        this = effect.this.CastTo(Minion)
        message.SetBeInstead(effect)
        vilain = Worlds.FindVillain(effect)
        if vilain:
            this.BasicAttack([vilain], effect)

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        this.PlaceThreatOnSchemes("MainScheme", 2, effect)

    return [
        AbilityFactory.WhenUnitWouldScheme(
            AbilityType.ForcedInterrupt,
            "This",
            attaque_le_vilain,
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            vaincu,
        ),
    ]
```

#### `60183` Crooked Cop

```json
{
 "card_id": "60183",
 "type": "Minion",
 "name": "Crooked Cop",
 "subtitle": "",
 "desc": {
  "HP": "4",
  "ATK": "2",
  "SCH": "1",
  "Boost": "0",
  "Quickstrike": "1",
  "Vulnerable": "1"
 },
 "traits": [
  "CRIMINAL",
  "POLICE"
 ],
 "set_name": "Cops",
 "text": "Quickstrike. Vulnerable.\n<b>When Defeated</b>: The defeating player deals themself 1 facedown encounter card.\n<hr />\n[star] <b>Boost</b>: Take 2 indirect damage."
}
```

Script `src/cards/pack/fne/cops/60183.py` :

```python
from . import *

# Crooked Cop (CRIMINAL, POLICE) — Quickstrike, Vulnerable : bases automatiques.
# When Defeated: The defeating player deals themself 1 facedown encounter card.
# [star] Boost: Take 2 indirect damage.
#
# Modeles : 27080 Lashing Out (TakeIndirectDamage en boost), message
# WhenUnitBeDefeated.GetDefeatingPlayer().

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        joueur = message.GetDefeatingPlayer()
        if joueur:
            joueur.DealEncounterCards(1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        message.GetToPlayer().GetIdentity().TakeIndirectDamage(this, 2, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            vaincu,
        ),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

#### `60184` Wanted

```json
{
 "card_id": "60184",
 "type": "Obligation",
 "name": "Wanted",
 "subtitle": "",
 "desc": {
  "Boost": "2"
 },
 "traits": [],
 "set_name": "Cops",
 "text": "<b>Hero Action</b>: Discard cards from the encounter deck until a [[Police]] minion is discarded and put it into play engaged with you. Discard this card."
}
```

Script `src/cards/pack/fne/cops/60184.py` :

```python
from . import *

# Wanted (obligation du set modulaire Cops, sans « Give to »)
# Hero Action: Discard cards from the encounter deck until a POLICE minion is
#   discarded and put it into play engaged with you. Discard this card.
#
# Modeles : dz019 Performance Anxiety (obligation qui reste en jeu et se
# retire par une action), 11025 Rampage (DiscardEncounterCardsUntil +
# PutIntoPlay : un sbire pose par un joueur s'engage avec lui).

def GetAbilities() -> Sequence['Ability']:

    def recherche(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = effect.GetInitiator()
        face = Worlds.DiscardEncounterCardsUntil(effect, trait="POLICE", card_type=Minion)
        if face:
            face.PutIntoPlay(joueur, effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            recherche,
        ),
    ]
```

#### `60185` Police Cordon

```json
{
 "card_id": "60185",
 "type": "SideScheme",
 "name": "Police Cordon",
 "subtitle": "",
 "desc": {
  "Boost": "3",
  "StartingThreat": "3",
  "Hinder": "1*"
 },
 "traits": [],
 "set_name": "Cops",
 "text": "[star] Hinder 1[per_hero].\nEach [[Police]] minion gains guard and patrol.\n<b>When Revealed</b>: Search the encounter deck and discard pile for a [[Police]] minion and reveal it."
}
```

Script `src/cards/pack/fne/cops/60185.py` :

```python
from . import *

# Police Cordon (side scheme) — Hinder 1[per_hero] : base automatique.
# Each POLICE minion gains guard and patrol.
# When Revealed: Search the encounter deck and discard pile for a POLICE minion
#   and reveal it.
#
# Modeles : GiveKeywordToInPlayWhenApplyThis (rend une LISTE, deballage *),
# 01095 Rhino pour la recherche + Reveal.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        face = Search.EncounterCard(
            effect,
            include_discard_pile=True,
            trait="POLICE",
            card_type=Minion,
        )
        if face:
            face.Reveal(joueur, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(trait="POLICE", card_type=Minion),
            guard=1,
            patrol=1,
        ),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
```

### Set : Drive (5 cartes)

#### `60186` Sports Car

```json
{
 "card_id": "60186",
 "type": "Attachment",
 "name": "Sports Car",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "ATK+": "1"
 },
 "traits": [
  "VEHICLE"
 ],
 "set_name": "Drive",
 "text": "Attach to the enemy with the highest ATK without a [[Vehicle]] attachment. Otherwise, this card gains surge.\n<b>Forced Interrupt</b>: When attached character would take any amount of damage, place it here instead. If there is 4 or more damage here, discard this card."
}
```

Script `src/cards/pack/fne/drive/60186.py` :

```python
from . import *

# Sports Car (VEHICLE) — +1 ATK (cle desc ATK+).
# Attach to the enemy with the highest ATK without a VEHICLE attachment.
#   Otherwise, this card gains surge.
# Forced Interrupt: When attached character would take any amount of damage,
#   place it here instead. If there is 4 or more damage here, discard this card.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDUnVehicule(4, highest_atk=True)]
```

#### `60187` Motorcycle

```json
{
 "card_id": "60187",
 "type": "Attachment",
 "name": "Motorcycle",
 "subtitle": "",
 "desc": {
  "Boost": "1",
  "SCH+": "1",
  "THW+": "1"
 },
 "traits": [
  "VEHICLE"
 ],
 "set_name": "Drive",
 "text": "Attach to the enemy with the highest SCH without a [[Vehicle]] attachment. Otherwise, this card gains surge.\n<b>Forced Interrupt</b>: When attached character would take any amount of damage, place it here instead. If there is 3 or more damage here, discard this card."
}
```

Script `src/cards/pack/fne/drive/60187.py` :

```python
from . import *

# Motorcycle (VEHICLE) — +1 SCH/THW (cles desc SCH+ et THW+).
# Attach to the enemy with the highest SCH without a VEHICLE attachment.
#   Otherwise, this card gains surge.
# Forced Interrupt : ... 3 or more damage here, discard this card.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDUnVehicule(3, highest_sch=True)]
```

#### `60188` Utility Van

```json
{
 "card_id": "60188",
 "type": "Attachment",
 "name": "Utility Van",
 "subtitle": "",
 "desc": {
  "Boost": "1"
 },
 "traits": [
  "VEHICLE"
 ],
 "set_name": "Drive",
 "text": "Attach to the enemy with the fewest remaining hit points without a [[Vehicle]] attachment. Otherwise, this card gains surge.\n<b>Forced Interrupt</b>: When attached character would take any amount of damage, place it here instead. If there is 6 or more damage here, discard this card."
}
```

Script `src/cards/pack/fne/drive/60188.py` :

```python
from . import *

# Utility Van (VEHICLE)
# Attach to the enemy with the fewest remaining hit points without a VEHICLE
#   attachment. Otherwise, this card gains surge.
# Forced Interrupt : ... 6 or more damage here, discard this card.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDUnVehicule(6, fewest_remaining_hp=True)]
```

#### `60189` Traffic Jam

```json
{
 "card_id": "60189",
 "type": "SideScheme",
 "name": "Traffic Jam",
 "subtitle": "",
 "desc": {
  "Boost": "3",
  "StartingThreat": "2",
  "Hinder": "2*",
  "Crisis": "1"
 },
 "traits": [],
 "set_name": "Drive",
 "text": "[star] Hinder 2[per_hero].\n<b>Forced Interrupt</b>: When a character with a [[Vehicle]] attachment would:\n• Add threat to a scheme, that threat is added here instead.\n• Remove threat from a scheme, that threat is removed from here instead."
}
```

Script `src/cards/pack/fne/drive/60189.py` :

```python
from . import *

# Traffic Jam (side scheme, 2, crisis) — [star] Hinder 2[per_hero] : base desc.
# Forced Interrupt: When a character with a VEHICLE attachment would:
#   • Add threat to a scheme, that threat is added here instead.
#   • Remove threat from a scheme, that threat is removed from here instead.
# WhenSchemeWouldPlaceThreat : PreventThreat("All") + pose ici ;
# WhenSchemeWouldRemoveThreat : SetCannotBeRemoved + retrait ici. Le personnage
# qui pose = `sch_message.trigger` (manigance) sinon `by_effect.this` ; celui
# qui retire = `by_face` (contre).

def GetAbilities() -> Sequence['Ability']:

    def pose_ici(effect: 'Effect', message: 'Message.WhenSchemeWouldPlaceThreat') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        valeur = message.value
        if valeur <= 0:
            return
        message.PreventThreat("All", effect)
        this.PlaceThreatOnSchemes([this], valeur, effect)

    def pose_par_un_vehicule(effect: 'Effect', message: 'Message.WhenSchemeWouldPlaceThreat') -> bool:
        this = effect.this
        if message.trigger is this:
            return False
        auteur = message.sch_message.trigger if message.sch_message is not None else message.by_effect.this
        return auteur is not None and AUnVehicule(auteur)

    def retire_ici(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        valeur = message.value
        message.SetCannotBeRemoved(effect)
        if valeur > 0:
            this.RemoveThreatFromSchemes([this], valeur, effect)

    def retrait_par_un_vehicule(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        this = effect.this
        if message.trigger is this:
            return False
        return message.by_face is not None and AUnVehicule(message.by_face)

    return [
        AbilityFactory.WhenSchemeWouldPlaceThreat(AbilityType.ForcedInterrupt, None, pose_ici, conditions=[pose_par_un_vehicule]),
        AbilityFactory.WhenSchemeWouldRemoveThreat(AbilityType.ForcedInterrupt, None, retire_ici, conditions=[retrait_par_un_vehicule]),
    ]
```

#### `60190` Carjacking

```json
{
 "card_id": "60190",
 "type": "Treachery",
 "name": "Carjacking",
 "subtitle": "",
 "desc": {
  "Boost": "2"
 },
 "traits": [],
 "set_name": "Drive",
 "text": "<b>When Revealed</b>: Discard cards from the encounter deck until a [[Vehicle]] attachment is discarded and reveal it. If your identity does not have a [[Vehicle]] attachment, you may spend 3 resources of the same type to attach the discarded attachment to your identity instead."
}
```

Script `src/cards/pack/fne/drive/60190.py` :

```python
from . import *

# Carjacking
# When Revealed: Discard cards from the encounter deck until a VEHICLE
#   attachment is discarded and reveal it. If your identity does not have a
#   VEHICLE attachment, you may spend 3 resources of the same type to attach
#   the discarded attachment to your identity instead.
# Modeles : 60184 Wanted (DiscardEncounterCardsUntil), 60127 Tug of War (branche
# payante offerte seulement si payable, PeutCouvrirLeCout), 40122a
# (Cost("3", same_type=True)).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        face = Worlds.DiscardEncounterCardsUntil(effect, trait="VEHICLE", card_type=Attachment)
        if face is None:
            return
        identite = joueur.GetIdentity()
        if AUnVehicule(identite):
            face.Reveal(joueur, effect)
            return

        def payable(effet_choix: 'Effect', message_choix: 'Message.WhenPlayerChooseAbility') -> bool:
            return PeutCouvrirLeCout(joueur, effet_choix, Cost("3", same_type=True))

        def attacher(targets: Sequence['CardFace'], res: 'Resources') -> None:
            face.CastTo(Attachment).AttachTo2(identite, effect)

        def sinon(targets: Sequence['CardFace']) -> None:
            face.Reveal(joueur, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("3", same_type=True),
                "Spend 3 resources of the same type: attach the discarded attachment to your identity instead",
                attacher, conditions=[payable]),
            AbilityFactory.Otherwise(sinon),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
```

### Set : The Owl (4 cartes)

#### `60191` Flight Serum

```json
{
 "card_id": "60191",
 "type": "Attachment",
 "name": "Flight Serum",
 "subtitle": "",
 "desc": {
  "Boost": "0",
  "SCH+": "1",
  "ATK+": "1"
 },
 "traits": [
  "SUPERPOWER"
 ],
 "set_name": "The Owl",
 "text": "Attach to a non-[[Aerial]] enemy. Otherwise, this card gains surge.\nAttached enemy gains [[Aerial]].\n<b>Hero Action</b>: Discard an [[Attack]] event from your hand → discard this card."
}
```

Script `src/cards/pack/fne/the_owl/60191.py` :

```python
from . import *

# Flight Serum (SUPERPOWER) — +1 SCH / +1 ATK : cles desc "SCH+"/"ATK+".
# Attach to a non-AERIAL enemy. Otherwise, this card gains surge.
# Attached enemy gains AERIAL.
# Hero Action: Discard an ATTACK event from your hand -> discard this card.
#
# Modeles : AttachToFaceWhenPutIntoPlay(if_cannot_gain_surge=True), 18027 In A
# Bind (CostFunc.Discard("YourHandCards", trait="ATTACK", card_type=Event)).

def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(non_trait="AERIAL", card_type=Enemy),
            if_cannot_gain_surge=True,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            "Character",
            trait="AERIAL",
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCostFunc(CostFunc.Discard("YourHandCards", trait="ATTACK", card_type=Event)),
    ]
```

#### `60192` * Mister Fish

```json
{
 "card_id": "60192",
 "type": "Minion",
 "name": "* Mister Fish",
 "subtitle": "",
 "desc": {
  "HP": "4",
  "ATK": "2",
  "SCH": "1",
  "Boost": "2"
 },
 "traits": [
  "CRIMINAL",
  "MAGGIA"
 ],
 "set_name": "The Owl",
 "text": "[star] Mister Fish's attacks gain piercing and ranged.\n<b>When Revealed</b>: Mister Fish engages the player whose identity has the fewest remaining hit points."
}
```

Script `src/cards/pack/fne/the_owl/60192.py` :

```python
from . import *

# * Mister Fish (CRIMINAL, MAGGIA)
# [star] Mister Fish's attacks gain piercing and ranged.
# When Revealed: Mister Fish engages the player whose identity has the fewest
#   remaining hit points.
#
# Modeles : 04027 Crossfire (UnitAttackGainKeyword), 45135 Armored Unibike
# (EngagePlayer). PlayerFinder ne sait pas trier par PV : on choisit a la main.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        joueurs = [j for j in effect.world.const_players if j.GetIdentity() is not None]
        if not joueurs:
            return
        cible = min(joueurs, key=lambda j: j.GetIdentity().health)
        this.EngagePlayer(cible, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
            ranged=True,
        ),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
```

#### `60193` * The Owl

```json
{
 "card_id": "60193",
 "type": "Minion",
 "name": "* The Owl",
 "subtitle": "",
 "desc": {
  "HP": "5",
  "ATK": "2",
  "SCH": "3",
  "Boost": "0",
  "Quickstrike": "1"
 },
 "traits": [
  "AERIAL",
  "CRIMINAL"
 ],
 "set_name": "The Owl",
 "text": "Quickstrike.\n[star] The Owl's attacks gain piercing.\n<hr />\n[star] <b>Boost</b>: If this activation is an attack, it gains piercing."
}
```

Script `src/cards/pack/fne/the_owl/60193.py` :

```python
from . import *

# * The Owl (AERIAL, CRIMINAL) — Quickstrike : base automatique.
# [star] The Owl's attacks gain piercing.
# [star] Boost: If this activation is an attack, it gains piercing.
#
# Modele exact : 04027 Crossfire.

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.would_atk_message.GainPiercing(effect)

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
            during_attack=True,
        ),
    ]
```

#### `60194` Swoop Down

```json
{
 "card_id": "60194",
 "type": "Treachery",
 "name": "Swoop Down",
 "subtitle": "",
 "desc": {
  "Boost": "3"
 },
 "traits": [],
 "set_name": "The Owl",
 "text": "<b>When Revealed (Alter-Ego)</b>: The villain and each minion engaged with you schemes. Each [[Aerial]] enemy gets +2 SCH for its activation.\n<b>When Revealed (Hero)</b>: The villain and each minion engaged with you attacks you. Each [[Aerial]] enemy gets +2 ATK for its activation."
}
```

Script `src/cards/pack/fne/the_owl/60194.py` :

```python
from . import *

# Swoop Down
# When Revealed (Alter-Ego): The villain and each minion engaged with you
#   schemes. Each AERIAL enemy gets +2 SCH for its activation.
# When Revealed (Hero): The villain and each minion engaged with you attacks
#   you. Each AERIAL enemy gets +2 ATK for its activation.
#
# Modeles : 32117 Master Mold's Children (vilain puis sbires engages), 04086
# Swinging Stone (additional_value dans la propriete). On deroule a la main
# plutot que par Worlds.Enemies.* pour porter le +2 propre a chaque ennemi.

def GetAbilities() -> Sequence['Ability']:

    def ennemis(effect: 'Effect', joueur: 'Player') -> List['Enemy']:
        liste: List['Enemy'] = []
        vilain = Worlds.FindVillain(effect)
        if vilain:
            liste.append(vilain)
        liste.extend(list(joueur.GetEngagedMinions()))
        return liste

    def bonus(ennemi: 'Enemy') -> int:
        return 2 if ennemi.HasTrait("AERIAL") else 0

    def alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        for ennemi in ennemis(effect, joueur):
            if ennemi.IsInPlay():
                ennemi.DoSchemes(joueur, effect, property=SchemeProperty(additional_value=bonus(ennemi)))

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        for ennemi in ennemis(effect, joueur):
            if ennemi.IsInPlay():
                ennemi.DoAttackYou(joueur, effect, property=AttackProperty(additional_value=bonus(ennemi)))

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", heros),
    ]
```

### Set : Tombstone (5 cartes)

#### `60195` Cold as Ice

```json
{
 "card_id": "60195",
 "type": "Attachment",
 "name": "Cold as Ice",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "SCH+": "2"
 },
 "traits": [],
 "set_name": "Tombstone",
 "text": "Attach to the minion with the highest base hit points and give that minion a tough status card. Otherwise, this card gains surge.\n[star] <b>Forced Response</b>: After attached minion schemes, confuse the first player's identity and discard Cold as Ice."
}
```

Script `src/cards/pack/fne/tombstone/60195.py` :

```python
from . import *

# Cold as Ice — +2 SCH (cle desc SCH+).
# Attach to the minion with the highest base hit points and give that minion a
#   tough status card. Otherwise, this card gains surge.
# [star] Forced Response: After attached minion schemes, confuse the first
#   player's identity and discard Cold as Ice.

def GetAbilities() -> Sequence['Ability']:

    def apres_manigance(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        this = effect.this.CastTo(Attachment)
        premier = Worlds.GetFirstPlayer(effect)
        Faces.GiveStatus([premier.GetIdentity()], "Confused", effect)
        Faces.DiscardAll([this], effect)

    return [
        AttacheAuSbireLePlusSolide(),
        AbilityFactory.AfterUnitSchemeEnd(AbilityType.ForcedResponse, "AttachedEnemy", apres_manigance),
    ]
```

#### `60196` Hard as Marble

```json
{
 "card_id": "60196",
 "type": "Attachment",
 "name": "Hard as Marble",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "ATK+": "2"
 },
 "traits": [],
 "set_name": "Tombstone",
 "text": "Attach to the minion with the highest base hit points and give that minion a tough status card. Otherwise, this card gains surge.\n[star] <b>Forced Response</b>: After attached minion attacks, stun the attacked character and discard Hard as Marble."
}
```

Script `src/cards/pack/fne/tombstone/60196.py` :

```python
from . import *

# Hard as Marble — +2 ATK (cle desc ATK+).
# Attach to the minion with the highest base hit points and give that minion a
#   tough status card. Otherwise, this card gains surge.
# [star] Forced Response: After attached minion attacks, stun the attacked
#   character and discard Hard as Marble.
# « the attacked character » = message.attacked_targets (60089 Gatling Gun).

def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Attachment)
        cibles = [u for u in message.attacked_targets if u.IsInPlay() and not u.IsDefeated()]
        if cibles:
            Faces.GiveStatus(cibles, "Stunned", effect)
        Faces.DiscardAll([this], effect)

    return [
        AttacheAuSbireLePlusSolide(),
        AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, "AttachedEnemy", apres_attaque),
    ]
```

#### `60197` * Beetle

```json
{
 "card_id": "60197",
 "type": "Minion",
 "name": "* Beetle",
 "subtitle": "",
 "desc": {
  "HP": "5",
  "ATK": "1",
  "SCH": "1",
  "Boost": "2",
  "Villainous": "1"
 },
 "traits": [
  "AERIAL",
  "CRIMINAL"
 ],
 "set_name": "Tombstone",
 "text": "Villainous.\n<b>When Revealed</b>: Search the encounter deck and discard pile for an attachment that can attach to a minion and attach it to Beetle."
}
```

Script `src/cards/pack/fne/tombstone/60197.py` :

```python
from . import *

# * Beetle (AERIAL, CRIMINAL) — Villainous : base desc.
# When Revealed: Search the encounter deck and discard pile for an attachment
#   that can attach to a minion and attach it to Beetle.
# « can attach to a minion » : PeutSAccrocherAUnSbire (tombstone/__init__.py),
# qui relit la phrase imprimee « Attach to ... » : la regle moteur
# `Asset2.CanAttachTo` ne connait que MaxPerUnit et acceptait Gatling Gun
# (« Attach to the villain ») sur Beetle. La fouille passe par
# Search.SearchForCard sur cette liste filtree (faces=...).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetToPlayer()
        candidates = [f for f in Worlds.GetEncounterDeckCards(effect.world) + Worlds.GetEncounterDiscardPileCards(effect.world)
                      if PeutSAccrocherAUnSbire(f, this)]
        if not candidates:
            return
        face = Search.SearchForCard(effect, joueur, faces=candidates, card_type=Attachment)
        if face:
            face.CastTo(Attachment).AttachTo2(this, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
```

#### `60198` * Tombstone

```json
{
 "card_id": "60198",
 "type": "Minion",
 "name": "* Tombstone",
 "subtitle": "",
 "desc": {
  "HP": "8",
  "ATK": "2",
  "SCH": "2",
  "Boost": "0",
  "Quickstrike": "1"
 },
 "traits": [
  "CRIMINAL"
 ],
 "set_name": "Tombstone",
 "text": "Quickstrike.\n<hr />\n[star] <b>Boost</b>: Give the villain a tough status card."
}
```

Script `src/cards/pack/fne/tombstone/60198.py` :

```python
from . import *

# * Tombstone (CRIMINAL) — Quickstrike : base desc.
# [star] Boost: Give the villain a tough status card.

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        vilain = Worlds.FindVillain(effect)
        if vilain:
            Faces.GiveStatus([vilain], "Tough", effect)

    return [
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
```

#### `60199` Hit List

```json
{
 "card_id": "60199",
 "type": "SideScheme",
 "name": "Hit List",
 "subtitle": "",
 "desc": {
  "Boost": "3",
  "StartingThreat": "3*"
 },
 "traits": [],
 "set_name": "Tombstone",
 "text": "<b>Forced Response</b>: After the villain phase begins, deal 3 indirect damage to the first player. For each ally defeated this way, remove 1[per_hero] threat from Hit List."
}
```

Script `src/cards/pack/fne/tombstone/60199.py` :

```python
from . import *

# Hit List (side scheme, 3[per_hero])
# Forced Response: After the villain phase begins, deal 3 indirect damage to
#   the first player. For each ally defeated this way, remove 1[per_hero]
#   threat from Hit List.
# AfterPhaseBegin("Villain") ; TakeIndirectDamage.
# ⚠ `operation=` de TakeIndirectDamage ne voit PAS les unites vaincues :
# can_health.py:288 n'envoie AfterUnitTookDamage (et n'appelle l'operation)
# que `if unit.IsInPlay()`, or l'allie vaincu est deja defausse. Mesure au
# harnais du 18/09/2026 (Spider-Woman vaincue, menace inchangee). On compare
# donc les allies en jeu avant et apres les degats.

def GetAbilities() -> Sequence['Ability']:

    def liste(effect: 'Effect', message: 'Message.AfterPhaseBegin') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        premier = Worlds.GetFirstPlayer(effect)
        identite = premier.GetIdentity()
        allies_avant = [a for a in premier.GetControlAllies() if a.IsInPlay()]
        identite.TakeIndirectDamage(this, 3, effect)
        vaincus = [a for a in allies_avant if not a.IsInPlay() or a.IsDefeated()]
        if vaincus:
            this.RemoveThreatFromSchemes([this], Worlds.GetPlayerNumIcon(effect) * len(vaincus), effect)

    return [
        AbilityFactory.AfterPhaseBegin(AbilityType.ForcedResponse, "Villain", liste),
    ]
```

### Set : Tracksuit Mafia (5 cartes)

#### `60200` * Ivan Banionis

```json
{
 "card_id": "60200",
 "type": "Minion",
 "name": "* Ivan Banionis",
 "subtitle": "",
 "desc": {
  "HP": "5",
  "ATK": "2",
  "SCH": "0",
  "Boost": "2",
  "Teamwork": "TRACKSUIT"
 },
 "traits": [
  "CRIMINAL",
  "TRACKSUIT"
 ],
 "set_name": "Tracksuit Mafia",
 "text": "Teamwork ([[Tracksuit]]).\n<b>When Revealed</b>: Place 1 acceleration token here.\n[star] <b>Forced Response</b>: After Ivan Banionis schemes, place 1 acceleration token here."
}
```

Script `src/cards/pack/fne/tracksuit_mafia/60200.py` :

```python
from . import *

# * Ivan Banionis (CRIMINAL, TRACKSUIT) — Teamwork (TRACKSUIT) : base desc.
# When Revealed: Place 1 acceleration token here.
# [star] Forced Response: After Ivan Banionis schemes, place 1 acceleration
#   token here.
# PlaceAccelerationToken (50081 Abduct Superhumans).

def GetAbilities() -> Sequence['Ability']:

    def accelere(effect: 'Effect', message: 'Message') -> None:
        this = effect.this.CastTo(Minion)
        this.PlaceAccelerationToken(1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, accelere),
        AbilityFactory.AfterUnitSchemeEnd(AbilityType.ForcedResponse, "This", accelere),
    ]
```

#### `60201` * The Clown

```json
{
 "card_id": "60201",
 "type": "Minion",
 "name": "* The Clown",
 "subtitle": "",
 "desc": {
  "HP": "6",
  "ATK": "1",
  "SCH": "0",
  "Boost": "2",
  "Teamwork": "TRACKSUIT",
  "Villainous": "1"
 },
 "traits": [
  "ASSASSIN",
  "TRACKSUIT"
 ],
 "set_name": "Tracksuit Mafia",
 "text": "Teamwork ([[Tracksuit]]). Villainous.\n[star] <b>Forced Response</b>: After The Clown schemes, give him 1 facedown boost card."
}
```

Script `src/cards/pack/fne/tracksuit_mafia/60201.py` :

```python
from . import *

# * The Clown (ASSASSIN, TRACKSUIT) — Teamwork (TRACKSUIT), Villainous : bases.
# [star] Forced Response: After The Clown schemes, give him 1 facedown boost
#   card.  (Faces.GiveFacedownBoostCards, 55007b)

def GetAbilities() -> Sequence['Ability']:

    def apres_manigance(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        this = effect.this.CastTo(Minion)
        Faces.GiveFacedownBoostCards([this], 1, effect)

    return [
        AbilityFactory.AfterUnitSchemeEnd(AbilityType.ForcedResponse, "This", apres_manigance),
    ]
```

#### `60202` * Tracksuit Mafioso

```json
{
 "card_id": "60202",
 "type": "Minion",
 "name": "* Tracksuit Mafioso",
 "subtitle": "",
 "desc": {
  "HP": "7",
  "ATK": "0",
  "SCH": "3",
  "Boost": "3",
  "Retaliate": "2",
  "Teamwork": "TRACKSUIT",
  "Vulnerable": "1"
 },
 "traits": [
  "CRIMINAL",
  "TRACKSUIT"
 ],
 "set_name": "Tracksuit Mafia",
 "text": "Retaliate 2. Teamwork ([[Tracksuit]]). Vulnerable.\n<b>When Defeated</b>: Tuck this card under the Tracksuit Mafia side scheme. Otherwise, stun and confuse the character that defeated Tracksuit Mafioso."
}
```

Script `src/cards/pack/fne/tracksuit_mafia/60202.py` :

```python
from . import *

# * Tracksuit Mafioso (CRIMINAL, TRACKSUIT) — Retaliate 2, Teamwork (TRACKSUIT),
#   Vulnerable : bases desc.
# When Defeated: Tuck this card under the Tracksuit Mafia side scheme.
#   Otherwise, stun and confuse the character that defeated Tracksuit Mafioso.
# « the character that defeated » = message.killer.

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        manigance = TrouverTracksuitMafia(effect)
        if manigance is not None:
            manigance.TuckCardUnderHere(this, effect)
            return
        tueur = message.killer
        if tueur is not None and Unit2.IsType(tueur) and tueur.IsInPlay():
            Faces.GiveStatus([tueur], "Stunned", effect)
            Faces.GiveStatus([tueur], "Confused", effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
```

#### `60203` Tracksuit Bro

```json
{
 "card_id": "60203",
 "type": "Minion",
 "name": "Tracksuit Bro",
 "subtitle": "",
 "desc": {
  "HP": "3",
  "ATK": "2",
  "SCH": "1",
  "Boost": "2",
  "Teamwork": "TRACKSUIT",
  "Vulnerable": "1"
 },
 "traits": [
  "CRIMINAL",
  "TRACKSUIT"
 ],
 "set_name": "Tracksuit Mafia",
 "text": "Teamwork ([[Tracksuit]]). Vulnerable.\n<b>When Defeated</b>: Tuck this card under the Tracksuit Mafia side scheme. Otherwise, shuffle this card into the encounter deck."
}
```

Script `src/cards/pack/fne/tracksuit_mafia/60203.py` :

```python
from . import *

# Tracksuit Bro (CRIMINAL, TRACKSUIT) — Teamwork (TRACKSUIT), Vulnerable : bases.
# When Defeated: Tuck this card under the Tracksuit Mafia side scheme.
#   Otherwise, shuffle this card into the encounter deck.

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        manigance = TrouverTracksuitMafia(effect)
        if manigance is not None:
            manigance.TuckCardUnderHere(this, effect)
        else:
            Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
```

#### `60204` Tracksuit Mafia

```json
{
 "card_id": "60204",
 "type": "SideScheme",
 "name": "Tracksuit Mafia",
 "subtitle": "",
 "desc": {
  "Boost": "2",
  "StartingThreat": "3*"
 },
 "traits": [],
 "set_name": "Tracksuit Mafia",
 "text": "<b>When Revealed</b>: Discard cards from the top of the encounter deck until a [[Tracksuit]] minion is discarded and tuck that minion here.\n<b>Forced Response</b>: After a player reveals a [[Tracksuit]] minion from the encounter deck, that player reveals 1 minion tucked here."
}
```

Script `src/cards/pack/fne/tracksuit_mafia/60204.py` :

```python
from . import *

# Tracksuit Mafia (side scheme, 3[per_hero])
# When Revealed: Discard cards from the top of the encounter deck until a
#   TRACKSUIT minion is discarded and tuck that minion here.
# Forced Response: After a player reveals a TRACKSUIT minion from the
#   encounter deck, that player reveals 1 minion tucked here.
# ⚠ Le sbire sorti d'ici est lui-meme « revele » : le drapeau `en_cours`
# empeche la reponse de se rappeler elle-meme (le texte dit « from the
# encounter deck », pas « from here »).

def GetAbilities() -> Sequence['Ability']:
    etat = {"en_cours": False}

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        face = Worlds.DiscardEncounterCardsUntil(effect, trait="TRACKSUIT", card_type=Minion)
        if face is not None:
            this.TuckCardUnderHere(face, effect)

    def sortie(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        if etat["en_cours"]:
            return
        joueur = message.GetToPlayer()
        caches = [f for f in this.GetPlacedCardArea().Get() if Minion.IsType(f)]
        if not caches or joueur is None:
            return
        choisi = caches[0] if len(caches) == 1 else joueur.AskChooseFace(caches, effect)
        if choisi is None:
            return
        etat["en_cours"] = True
        try:
            choisi.Reveal(joueur, effect)
        finally:
            etat["en_cours"] = False

    def un_tracksuit_du_deck(effect: 'Effect', message: 'Message.WhenCardRevealed') -> bool:
        return not etat["en_cours"] and message.trigger is not effect.this

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardRevealed(AbilityType.ForcedResponse, CardFinder(trait="TRACKSUIT", card_type=Minion), sortie, conditions=[un_tracksuit_du_deck]),
    ]
```

### Set : Fear No Evil Campaign (12 cartes)

#### `60205a` Art Museum Heist (Completed)

```json
{
 "card_id": "60205a",
 "type": "Environment",
 "name": "Art Museum Heist",
 "subtitle": "Completed",
 "desc": {},
 "traits": [
  "COMPLETED"
 ],
 "set_name": "Fear No Evil Campaign",
 "text": "<b>Setup</b>: Give each identity a tough status card."
}
```

Script `src/cards/pack/fne/fear_no_evil_campaign/60205a.py` :

```python
from . import *

# Art Museum Heist (COMPLETED) — Setup: Give each identity a tough status card.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        identites = [p.GetIdentity() for p in Worlds.GetPlayers(effect)]
        Faces.GiveStatus(identites, "Tough", effect)

    return [AbilityFactory.AfterGameSetup(mise_en_place)]
```

#### `60205b` Art Museum Heist (Failed)

```json
{
 "card_id": "60205b",
 "type": "Environment",
 "name": "Art Museum Heist",
 "subtitle": "Failed",
 "desc": {},
 "traits": [
  "FAILED"
 ],
 "set_name": "Fear No Evil Campaign",
 "text": "<b>Setup</b>: Each player chooses to stun or confuse their identity <i>(in expert mode, do both instead)</i>."
}
```

Script `src/cards/pack/fne/fear_no_evil_campaign/60205b.py` :

```python
from . import *

# Art Museum Heist (FAILED) — Setup: Each player chooses to stun or confuse
#   their identity (in expert mode, do both instead).

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        def chacun(player: 'Player') -> None:
            identite = player.GetIdentity()
            if Worlds.IsExpert(effect):
                Faces.GiveStatus([identite], "Stunned", effect)
                Faces.GiveStatus([identite], "Confused", effect)
                return
            player.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility("Stun your identity", lambda targets: Faces.GiveStatus([identite], "Stunned", effect)),
                AbilityFactory.ForChoiceAbility("Confuse your identity", lambda targets: Faces.GiveStatus([identite], "Confused", effect)),
            )
        Players.ForEachPlayer(effect, chacun)

    return [AbilityFactory.AfterGameSetup(mise_en_place)]
```

#### `60206a` The Getaway (Completed)

```json
{
 "card_id": "60206a",
 "type": "Environment",
 "name": "The Getaway",
 "subtitle": "Completed",
 "desc": {},
 "traits": [
  "COMPLETED"
 ],
 "set_name": "Fear No Evil Campaign",
 "text": "<b>Setup</b>: After resolving mulligans, each player may search their deck and discard pile for an upgrade and add it to their hand. In expert mode, each player who did so discards 1 card from their hand."
}
```

Script `src/cards/pack/fne/fear_no_evil_campaign/60206a.py` :

```python
from . import *

# The Getaway (COMPLETED) — Setup: After resolving mulligans, each player may search
#   their deck and discard pile for an upgrade and add it to their hand. In expert
#   mode, each player who did so discards 1 card from their hand.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        Players.ForEachPlayer(effect, lambda player: ChercherEnMain(effect, player, Upgrade))

    return [AbilityFactory.AfterGameSetup(mise_en_place)]
```

#### `60206b` The Getaway (Failed)

```json
{
 "card_id": "60206b",
 "type": "Environment",
 "name": "The Getaway",
 "subtitle": "Failed",
 "desc": {},
 "traits": [
  "FAILED"
 ],
 "set_name": "Fear No Evil Campaign",
 "text": "In expert mode, attachments cannot be discarded from play during the first round.\n<b>Setup</b>: Each player searches the encounter deck for an attachment and reveals it. Deal a facedown encounter card to each player who could not."
}
```

Script `src/cards/pack/fne/fear_no_evil_campaign/60206b.py` :

```python
from . import *

# The Getaway (FAILED)
# In expert mode, attachments cannot be discarded from play during the first round.
# Setup: Each player searches the encounter deck for an attachment and reveals
#   it. Deal a facedown encounter card to each player who could not.
# ⚠ « cannot be discarded » : WhenCardLeavePlay(Attachment) + SetBeInstead au
# round 1 en expert ; si le message ne se laisse pas remplacer, l'ecart est
# signale au journal (ecart assume, a mesurer).

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        def chacun(player: 'Player') -> None:
            face = Search.SearchForCard(effect, player, include_encounter_deck=True, card_type=Attachment)
            if face is not None:
                face.Reveal(player, effect)
            else:
                player.DealEncounterCards(1, effect)
        Players.ForEachPlayer(effect, chacun)

    def garde(effect: 'Effect', message: 'Message.WhenCardLeavePlay') -> None:
        if hasattr(message, "SetBeInstead"):
            message.SetBeInstead(effect)

    def premier_round_expert(effect: 'Effect', message: 'Message.WhenCardLeavePlay') -> bool:
        return Worlds.IsExpert(effect) and effect.world.round_id <= 1 and getattr(message.into_area.flags, "is_discard_pile", False)

    return [
        AbilityFactory.AfterGameSetup(mise_en_place),
        AbilityFactory.WhenCardLeavePlay(AbilityType.ForcedInterrupt, Attachment, garde, conditions=[premier_round_expert]),
    ]
```

#### `60207a` Protection Racket (Completed)

```json
{
 "card_id": "60207a",
 "type": "Environment",
 "name": "Protection Racket",
 "subtitle": "Completed",
 "desc": {},
 "traits": [
  "COMPLETED"
 ],
 "set_name": "Fear No Evil Campaign",
 "text": "<b>Setup</b>: After resolving mulligans, each player may search their deck and discard pile for a support and add it to their hand. In expert mode, each player who did so discards 1 card from their hand."
}
```

Script `src/cards/pack/fne/fear_no_evil_campaign/60207a.py` :

```python
from . import *

# Protection Racket (COMPLETED) — Setup: After resolving mulligans, each player may search
#   their deck and discard pile for a support and add it to their hand. In expert
#   mode, each player who did so discards 1 card from their hand.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        Players.ForEachPlayer(effect, lambda player: ChercherEnMain(effect, player, Support))

    return [AbilityFactory.AfterGameSetup(mise_en_place)]
```

#### `60207b` Protection Racket (Failed)

```json
{
 "card_id": "60207b",
 "type": "Environment",
 "name": "Protection Racket",
 "subtitle": "Failed",
 "desc": {},
 "traits": [
  "FAILED"
 ],
 "set_name": "Fear No Evil Campaign",
 "text": "<b>Setup</b>: Each player chooses and discards 1 card from their hand <i>(in expert mode, 2 cards instead)</i>."
}
```

Script `src/cards/pack/fne/fear_no_evil_campaign/60207b.py` :

```python
from . import *

# Protection Racket (FAILED) — Setup: Each player chooses and discards 1 card
#   from their hand (in expert mode, 2 cards instead).

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        n = 2 if Worlds.IsExpert(effect) else 1
        Players.ForEachPlayer(effect, lambda player: DefausserDeLaMain(effect, player, n))

    return [AbilityFactory.AfterGameSetup(mise_en_place)]
```

#### `60208a` The Raft Breakout (Completed)

```json
{
 "card_id": "60208a",
 "type": "Environment",
 "name": "The Raft Breakout",
 "subtitle": "Completed",
 "desc": {},
 "traits": [
  "COMPLETED"
 ],
 "set_name": "Fear No Evil Campaign",
 "text": "<b>Setup</b>: After resolving mulligans, each player may search their deck and discard pile for an ally and add it to their hand. In expert mode, each player who did so discards 1 card from their hand."
}
```

Script `src/cards/pack/fne/fear_no_evil_campaign/60208a.py` :

```python
from . import *

# The Raft Breakout (COMPLETED) — Setup: After resolving mulligans, each player may search
#   their deck and discard pile for an ally and add it to their hand. In expert
#   mode, each player who did so discards 1 card from their hand.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        Players.ForEachPlayer(effect, lambda player: ChercherEnMain(effect, player, Ally))

    return [AbilityFactory.AfterGameSetup(mise_en_place)]
```

#### `60208b` The Raft Breakout (Failed)

```json
{
 "card_id": "60208b",
 "type": "Environment",
 "name": "The Raft Breakout",
 "subtitle": "Failed",
 "desc": {},
 "traits": [
  "FAILED"
 ],
 "set_name": "Fear No Evil Campaign",
 "text": "<b>Setup</b>: Shuffle each minion in The Raft Breakout encounter set into the encounter deck <i>(in expert mode, deal 1 of those minions at random to each player as a facedown encounter card before shuffling in the rest)</i>."
}
```

Script `src/cards/pack/fne/fear_no_evil_campaign/60208b.py` :

```python
from . import *

# The Raft Breakout (FAILED) — Setup: Shuffle each minion in The Raft Breakout
#   encounter set into the encounter deck (in expert mode, deal 1 of those
#   minions at random to each player as a facedown encounter card before
#   shuffling in the rest).
# Les six prisonniers sont fabriques s'ils ne sont pas deja dans le deck (le
# scenario The Raft Breakout les y a mis lui-meme).

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        deja = {f.paper.card_id for f in Worlds.GetEncounterDeckCards(effect.world)}
        faces = []
        for cid in PRISONNIERS_DU_RAFT:
            if cid in deja:
                continue
            faces.append(CardFactory.GenerateCard(cid, None, effect.world).face)
        if not faces:
            return
        if Worlds.IsExpert(effect):
            def distribuer(player: 'Player') -> None:
                if faces:
                    choisi = Rand.RandomChoice(faces, effect)
                    faces.remove(choisi)
                    player.DealEncounterCard(choisi, effect)
            Players.ForEachPlayer(effect, distribuer)
        if faces:
            Faces.ShuffleAllTo(faces, "EncounterDeck", effect)

    return [AbilityFactory.AfterGameSetup(mise_en_place)]
```

#### `60209a` Stop the Presses! (Completed)

```json
{
 "card_id": "60209a",
 "type": "Environment",
 "name": "Stop the Presses!",
 "subtitle": "Completed",
 "desc": {},
 "traits": [
  "COMPLETED"
 ],
 "set_name": "Fear No Evil Campaign",
 "text": "<b>Setup</b>: Each player puts 1 [[Daily Bugle]] support <i>(that has not been removed from the campaign)</i> into play from the Stop the Presses! encounter set."
}
```

Script `src/cards/pack/fne/fear_no_evil_campaign/60209a.py` :

```python
from . import *

# Stop the Presses! (COMPLETED) — Setup: Each player puts 1 DAILY BUGLE
#   support (that has not been removed from the campaign) into play from the
#   Stop the Presses! encounter set.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        retirees = set(Retirees(effect))
        en_jeu = {f.paper.card_id for f in Worlds.FindCardsOnField(effect, trait="DAILY BUGLE", card_type=Support)}
        candidats = []
        for cid in SOUTIENS_DAILY_BUGLE:
            if cid in en_jeu:
                continue
            face = CardFactory.GenerateCard(cid, None, effect.world).face
            if face.paper.name.lstrip('* ') in retirees:
                Faces.RemoveAllFromGame([face], effect)
                continue
            candidats.append(face)

        def chacun(player: 'Player') -> None:
            if not candidats:
                return
            choix = candidats[0] if len(candidats) == 1 else player.AskChooseFace(list(candidats), effect, prompt="Choose a Daily Bugle support")
            if choix is None:
                choix = candidats[0]
            candidats.remove(choix)
            choix.PutIntoPlay(player, effect, under_control=True)

        Players.ForEachPlayer(effect, chacun)
        if candidats:
            Faces.RemoveAllFromGame(list(candidats), effect)

    return [AbilityFactory.AfterGameSetup(mise_en_place)]
```

#### `60209b` Stop the Presses! (Failed)

```json
{
 "card_id": "60209b",
 "type": "Environment",
 "name": "Stop the Presses!",
 "subtitle": "Failed",
 "desc": {},
 "traits": [
  "FAILED"
 ],
 "set_name": "Fear No Evil Campaign",
 "text": "<b>Setup</b>: Deal each player 1 facedown encounter card <i>(in expert mode, 2 encounter cards instead)</i>."
}
```

Script `src/cards/pack/fne/fear_no_evil_campaign/60209b.py` :

```python
from . import *

# Stop the Presses! (FAILED) — Setup: Deal each player 1 facedown encounter
#   card (in expert mode, 2 encounter cards instead).

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        n = 2 if Worlds.IsExpert(effect) else 1
        Players.ForEachPlayer(effect, lambda player: player.DealEncounterCards(n, effect))

    return [AbilityFactory.AfterGameSetup(mise_en_place)]
```

#### `60210a` * Typhoid Mary (Mary Walker)

```json
{
 "card_id": "60210a",
 "type": "Ally",
 "name": "* Typhoid Mary",
 "subtitle": "Mary Walker",
 "desc": {
  "Cost": "0",
  "HP": "3",
  "ATK": "1*",
  "THW": "2*",
  "RES": "B",
  "Class": "Campaign;Basic",
  "Setup": "1",
  "Victory": "-1"
 },
 "traits": [
  "MUTANT",
  "PSIONIC"
 ],
 "set_name": "Fear No Evil Campaign",
 "text": "Setup. Victory -1.\n[star] <b>Forced Response</b>: After you reveal a minion, remove all damage from here and flip this card."
}
```

Script `src/cards/pack/fne/fear_no_evil_campaign/60210a.py` :

```python
from . import *

# * Typhoid Mary (Mary Walker) — alliee de campagne, Setup, Victory -1 : bases.
# [star] Forced Response: After you reveal a minion, remove all damage from
#   here and flip this card.
# « you » = le joueur qui controle l'alliee.

def GetAbilities() -> Sequence['Ability']:
    return [RechuteVers(Minion)]
```

#### `60210b` * Bloody Mary (Mary Walker)

```json
{
 "card_id": "60210b",
 "type": "Ally",
 "name": "* Bloody Mary",
 "subtitle": "Mary Walker",
 "desc": {
  "Cost": "0",
  "HP": "3",
  "ATK": "2*",
  "THW": "1*",
  "RES": "R",
  "Class": "Campaign;Basic",
  "Victory": "-1"
 },
 "traits": [
  "MUTANT",
  "PSIONIC"
 ],
 "set_name": "Fear No Evil Campaign",
 "text": "Victory -1.\n[star] <b>Forced Response</b>: After you reveal a side scheme, remove all damage from here and flip this card."
}
```

Script `src/cards/pack/fne/fear_no_evil_campaign/60210b.py` :

```python
from . import *

# * Bloody Mary (Mary Walker) — Victory -1 : base.
# [star] Forced Response: After you reveal a side scheme, remove all damage
#   from here and flip this card.

def GetAbilities() -> Sequence['Ability']:
    return [RechuteVers(EncounterSideScheme)]
```

## 2. Le code partagé du pack

Ces fichiers définissent des aides réutilisées par plusieurs cartes du même set. Lis-les pour comprendre un appel que le kit ne décrit pas.

### `src/cards/pack/fne/__init__.py`

```python
from cards.pack import *

def DiscountAbility(value: int, traits: Sequence['CardFace.TRAITS']) -> 'Ability':
    def check_control_trait(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        player = effect.this.GetControlByOrOwner()
        if not Player.IsType(player):
            return False
        for face in Worlds.FindCardsOnField(effect):
            if (face.GetControlBy() == player) and any(face.HasTrait(t) for t in traits):
                return True
        return False
    return AbilityFactory.ReduceCostToPlayThis(value, conditions=[check_control_trait])


def PeutCouvrirLeCout(joueur: 'Player', effect: 'Effect', cout: 'Cost') -> bool:
    """« You may spend X resources to ... Otherwise, ... » : la branche payante
    ne doit etre OFFERTE que si le joueur peut la payer, sinon le moteur la
    propose seule (Otherwise ne sort que quand aucune autre option n'existe),
    le paiement echoue et la carte ne fait rien. Mesure sur 60127 Tug of War
    (18/09/2026) : « couvert = 2 » sur un cout RRR, et pas d'Otherwise.

    On interroge les memes sources que `EffectChecker.UpdatePayResources`
    (message CheckPlayerCanPayCost) et on additionne ce qu'elles generent ;
    `Resources.CanPayThisCost` tranche, wild compris.
    """
    # ⚠⚠ NE PAS envoyer `Message.CheckPlayerCanPayCost` depuis une condition de
    # ChooseAbility : l'effet de choix n'a pas de couts calcules
    # (`cost_for_different_target` vide) et chaque carte en main qui repond au
    # message plante dans `add_to_pay_list` (« KeyError: None »,
    # resources.py:216). Vu par l'autoplay du 18/09/2026 (5 a 7 tracebacks par
    # partie), jamais par le harnais. On lit donc les icones IMPRIMEES de la
    # main et de la reserve, ce qui couvre le cas courant ; les generateurs en
    # jeu (supports a ressource) ne sont pas comptes : ecart assume, note au
    # gabarit de 60127.
    faces = list(joueur.hand_cards.Get()) + list(joueur.reserve.Get())
    total = FacesCounter.GetPrintedResources(faces)
    # ⚠ `Resources.CanPayThisCost` ne teste que la COULEUR (rbyg.py:110) : un
    # cout « 2 » y passe avec une seule carte. On exige aussi la QUANTITE.
    return total.CanPayThisCost(cout) and total.val >= cout.rbyga.total


def RetournerLAttachement(this: 'Attachment', effect: 'Effect', *, call_reveal: bool=True) -> None:
    """Retourne un attachement recto-verso SANS le perdre (Adamantium-Laced
    Spine, Out Front / Alongside, Mary Walker...). `card.Flip` DETACHE la carte
    (CanAttach.OnBeforeFlip -> DetachFrom2 -> MarkAsRemoved) et ne la raccroche
    (OnAfterFlip) que si sa zone est encore la zone d'ameliorations, ce qui
    n'est plus le cas : la face B restait dans les limbes (harnais du
    18/09/2026, RECETTES-MOTEUR §7quater). On memorise le porteur, on demarque
    la carte et on rejoue l'accrochage. `call_reveal` : la face qui apparait
    resout son When Revealed (Alongside, FAQ du livret)."""
    hote = this.GetBindFace()
    this.card.Flip(effect, call_reveal=call_reveal)
    nouvelle = this.card.face
    if hote is None or nouvelle is None:
        return
    carte = nouvelle.card
    carte.area.UnMarkAsRemoved(carte)
    nouvelle = nouvelle.CastTo(Attachment)
    if nouvelle.GetBindFace() is hote:
        nouvelle.AttachTo2(hote, effect)
        if not carte.state.is_attached:
            nouvelle.OnAttachTo(hote, True)
    else:
        nouvelle.AttachTo2(hote, effect)

def KingpinEnJeu(effect: 'Effect') -> 'Enemy|None':
    """« If Kingpin is in play » : le SBIRE Kingpin (nemesis d'Echo) OU le VILAIN
    Kingpin du scenario The King's Gambit.

    ⚠ `card_type=Minion` seul ne voit jamais le vilain, et dans ce scenario le
    sbire est justement retire du jeu par le Setup : « Pawn of the Kingpin »
    prenait surge au lieu de faire comploter Kingpin, et « Master Manipulator »
    en boost ne se revelait pas (signalement n°55, 04/10/2026). Regle choisie
    par l'utilisateur : le vilain compte, il s'appelle Kingpin et il est en jeu.
    """
    return (Worlds.FindCardOnField(effect, name='Kingpin', card_type=Minion)
            or Worlds.FindCardOnField(effect, name='Kingpin', card_type=Villain))
```

### `src/cards/pack/fne/art_museum_heist/__init__.py`

```python
from cards.pack import *
# Le helper de paiement vit au niveau du PACK ; `from . import *` d'une carte
# ne remonte qu'a ce module, il faut le re-exporter ici.
from cards.pack.fne import PeutCouvrirLeCout

# Helpers du set Art Museum Heist (Fear No Evil, 60121-60127).
# Les quatre oeuvres (60122-60125) portent le trait ART.


def OeuvresSur(face: 'CardFace') -> List['Attachment']:
    """Les attachements ART accroches a `face`."""
    return [a for a in face.GetAttachedAttachments() if a.HasTrait("ART")]


def OeuvresSurLesIdentites(effect: 'Effect') -> List['Attachment']:
    oeuvres: List['Attachment'] = []
    for joueur in effect.world.const_players:
        identite = joueur.GetIdentity()
        if identite is not None:
            oeuvres.extend(OeuvresSur(identite))
    return oeuvres


def DeplacerUneOeuvreVersLeVilain(effect: 'Effect', joueur: 'Player') -> bool:
    """« move an ART attachment from an identity to the villain ».
    Le joueur choisit l'oeuvre quand il y en a plusieurs. Rend False si aucune
    oeuvre n'est accrochee a une identite."""
    vilain = Worlds.FindVillain(effect)
    oeuvres = OeuvresSurLesIdentites(effect)
    if vilain is None or not oeuvres:
        return False
    oeuvre = joueur.AskChooseFace(oeuvres, effect, prompt="Move an Art attachment to the villain") if len(oeuvres) > 1 else oeuvres[0]
    if oeuvre is None:
        return False
    return oeuvre.AttachTo2(vilain, effect)


def DeplacerUneOeuvreDuVilainVers(effect: 'Effect', joueur: 'Player', cible: 'CardFace') -> bool:
    """« move an ART attachment from the villain to your identity »."""
    vilain = Worlds.FindVillain(effect)
    if vilain is None:
        return False
    oeuvres = OeuvresSur(vilain)
    if not oeuvres:
        return False
    oeuvre = joueur.AskChooseFace(oeuvres, effect, prompt="Move an Art attachment to your identity") if len(oeuvres) > 1 else oeuvres[0]
    if oeuvre is None:
        return False
    return oeuvre.AttachTo2(cible, effect)


def CapacitesDUneOeuvre(cout: 'Cost', a_l_attache: Callable[['Effect', 'Unit2'], None]|None) -> Sequence['Ability']:
    """Le tronc commun des quatre oeuvres :
    - Attach to the villain (+1 SCH / +1 THW : cles desc "SCH+"/"THW+") ;
    - Forced Response: After this card attaches to a character, <effet> ;
    - Hero Action: Spend a <ressource> OR exhaust your hero -> attach this card
      to your hero. Deux couts alternatifs = deux capacites (RECETTES §5).
    Surge est une base automatique (desc.Surge).
    """
    def apres_attache(effect: 'Effect', message: 'Message.AfterCardAttachTo') -> None:
        if a_l_attache is not None and Unit2.IsType(message.to_face):
            a_l_attache(effect, message.to_face.CastTo(Unit2))

    def pas_deja_sur_mon_heros(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        this = effect.this
        joueur = effect.GetInitiator()
        return this.GetBindFace() is not joueur.GetIdentity()

    def vers_mon_heros(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = effect.GetInitiator()
        this.AttachTo2(joueur.GetIdentity(), effect)

    capacites: List['Ability'] = [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            vers_mon_heros,
            conditions=[pas_deja_sur_mon_heros],
        ).SetName("Spend a resource: attach to your hero").SetCost(cout),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            vers_mon_heros,
            conditions=[pas_deja_sur_mon_heros],
        ).SetName("Exhaust your hero: attach to your hero").SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
    if a_l_attache is not None:
        capacites.append(
            AbilityFactory.AfterCardAttachTo(
                AbilityType.ForcedResponse,
                "This",
                Unit2,
                apres_attache,
            )
        )
    return capacites
```

### `src/cards/pack/fne/bullseye/__init__.py`

```python
from cards.pack import *
from cards.pack.fne import PeutCouvrirLeCout, RetournerLAttachement

# Helpers du set Bullseye (Fear No Evil, 60065-60075).


def TrouverBullseye(effect: 'Effect') -> 'Villain|None':
    return Worlds.FindCardOnField(effect, name="Bullseye", card_type=Villain)


def DeadlySaiAttache(effect: 'Effect') -> bool:
    """Deadly Sai (60070) : « Bullseye's attacks lose ranged ». Le ranged est
    accorde par la capacite etoilee de Bullseye lui-meme : c'est elle qui lit
    l'attachement, faute d'un `lost_ranged` dans AttackProperty."""
    bullseye = TrouverBullseye(effect)
    if bullseye is None:
        return False
    return any(a.IsName("Deadly Sai") for a in bullseye.GetAttachedAttachments())


def CapacitesDeBullseye() -> Sequence['Ability']:
    """[star] Forced Interrupt : When Bullseye activates, each of his boost
    cards gains [boost]. If this activation is an attack, it gains ranged.

    - icones : `IncreaseBoostIconsOnEncounterCard` (modele 15024), restreint
      aux cartes qui sont DANS la pile de boost de Bullseye ;
    - ranged : `WhenUnitWouldAttack(ForcedInterrupt, "This")` + GainRanged,
      sauf si Deadly Sai est attache (« lose ranged »).
    """
    # « each of HIS boost cards » : au moment du comptage la carte a quitte sa
    # pile (« deplacee vers la zone de boost », world.area_boosting), on ne peut
    # plus la rattacher a Bullseye par sa zone. On note donc l'ACTIVATION de
    # Bullseye elle-meme (drapeau pose a WhenUnitWouldAttack/Scheme, leve a
    # AfterEnemyActivationEnd) et on n'augmente que pendant celle-ci.
    etat = {"activation": False}

    def carte_boost_de_bullseye(effect: 'Effect', message: 'Message.WhenBoostIconsWouldBeCount') -> bool:
        this = effect.this
        zone = message.trigger.card.area
        return etat["activation"] and (zone is this.components.boostable.GetDeck() or zone is effect.world.area_boosting)

    def debut(effect: 'Effect', message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldScheme') -> None:
        etat["activation"] = True

        def fin() -> None:
            etat["activation"] = False

        RunAt.AfterEnemyActivationEnd(effect, message, fin)

    def ranged(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        debut(effect, message)
        if not DeadlySaiAttache(effect):
            message.GainRanged(effect)

    return [
        AbilityFactory.IncreaseBoostIconsOnEncounterCard(conditions=[carte_boost_de_bullseye]),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", ranged),
        AbilityFactory.WhenUnitWouldScheme(AbilityType.ForcedInterrupt, "This", debut),
    ]

def RetournerLaColonne(this: 'Attachment', effect: 'Effect') -> None:
    """Adamantium-Laced Spine <-> Damaged Spine : voir RetournerLAttachement
    (cards/pack/fne/__init__.py), commun a tous les attachements recto-verso du
    pack. Sans revelation : aucune des deux faces n'a de When Revealed."""
    RetournerLAttachement(this, effect, call_reveal=False)
```

### `src/cards/pack/fne/daredevil/__init__.py`

```python
from cards.pack import *
SENSE_DECK_IDS = ('60002', '60003', '60004', '60005', '60006')
def SelectSenseTopCard(effect: 'Effect') -> Sequence['CardFace']:
    initiator = effect.GetInitiator()
    face = initiator.additional_deck.GetTop()
    if face:
        return [face]
    return []
def PlaySenseUpgradeFree(player: 'Player', by_effect: 'Effect', *, any_number: bool = False, optional: bool = False) -> None:
    faces = player.additional_deck.Get()
    if not faces:
        return
    def action(targets: Sequence['CardFace']):
        for face in targets:
            face.CastTo(Upgrade).PutIntoPlay(player, by_effect)
    rng = ((0, len(faces)) if any_number else ((0, 1) if optional else (1, 1)))
    player.ChooseAbilities(by_effect, AbilityFactory.ForChoiceAbility('Choose an upgrade from the Sense deck and play it, ignoring its resource cost', action).SetTarget(faces, range=rng, not_move=True, not_shuffle=True))
def RafraichirDessusDeckAnnexe(effect: 'Effect', message: 'Message2') -> None:
    """Vide le cache `is_like_in_hand` des cartes ENCORE dans le deck annexe.

    CORRECTIF (25/09/2026, meme defaut que le signalement n°17 d'Echo,
    21/09/2026). `check_sense_top` (60001a.py) lit `additional_deck.GetTop()` :
    la reponse depend de QUELLE carte est actuellement au sommet, une donnee
    qui change des qu'une carte du deck annexe ENTRE ou SORT, sans que les
    AUTRES cartes du deck ne bougent elles-memes. Or `card.can_state.is_like_in_hand`
    (`card.py`) ne se remet a zero qu'au DEPLACEMENT de la carte elle-meme :
    la carte devenue nouveau dessus restait donc figee sur sa reponse
    precedente (souvent False, puisqu'elle n'etait pas au sommet la derniere
    fois qu'on l'a lue). Mesure et corrige le 25/09/2026
    (`tools/test_capacites.py`, cas « Sense the Top »).

    Les cinq cartes du deck Sense ne vivent QUE dans `additional_deck` ou en
    jeu (jouees) : tout deplacement de l'une d'elles signale donc un
    changement de dessus possible, sans condition supplementaire a verifier.
    """
    joueur = effect.this.GetControlByPlayer()
    if joueur is None:
        return
    for face in joueur.additional_deck.Get():
        if face is not None:
            face.card.can_state.is_like_in_hand = None
```

### `src/cards/pack/fne/disasters/__init__.py`

```python
from cards.pack import *


def CapacitesDeCatastrophe(cout: str, libelle: str, double: Callable[['CardFace'], bool]) -> Sequence['Ability']:
    """Environnement DISASTER : « Uses (2 civilian counters) » = base desc.
    Hero Action: Spend <cout> resources or exhaust a hero or ally you control ->
    remove 1 civilian counter from here (2 counters instead if you exhausted
    <double>).  Deux Hero Actions (RECETTES §5 « or ») : l'une payee en
    ressources, l'autre par CostFunc.Exhaust("Hero|Ally") dont on relit
    `return_exhausted_cards` pour savoir QUI a ete incline."""

    def retirer(effect: 'Effect', n: int) -> None:
        this = effect.this.CastTo(Environment)
        Faces.RemoveCountersOn([this], n, 'civilian', effect)

    def paye(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        retirer(effect, 1)

    inclinaison = CostFunc.Exhaust("Hero|Ally")

    def incline(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        n = 2 if any(double(f) for f in inclinaison.return_exhausted_cards) else 1
        retirer(effect, n)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, paye)
            .SetName(f"Spend {libelle}: remove 1 civilian counter")
            .SetCost(Cost(cout)),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, incline)
            .SetName("Exhaust a hero or ally you control: remove 1 civilian counter (2 instead)")
            .SetCostFunc(inclinaison),
    ]
```

### `src/cards/pack/fne/drive/__init__.py`

```python
from cards.pack import *
from cards.pack.fne import PeutCouvrirLeCout


def AUnVehicule(face: 'CardFace') -> bool:
    """« a character with a VEHICLE attachment » : un attachement VEHICLE dans
    sa zone d'ameliorations."""
    try:
        return any(a.HasTrait("VEHICLE") for a in face.GetInventoryDeck().Get())
    except Exception:
        return False


def CapacitesDUnVehicule(seuil: int, **choix) -> Sequence['Ability']:
    """Sports Car / Motorcycle / Utility Van : « Attach to the enemy with the
    <critere> without a VEHICLE attachment. Otherwise, this card gains surge.
    Forced Interrupt: When attached character would take any amount of damage,
    place it here instead. If there is <seuil> or more damage here, discard this
    card. »  Le critere passe par AttachToFaceWhenPutIntoPlay (highest_atk,
    highest_sch, fewest_remaining_hp) ; la pose des degats copie 60117
    Assembled Armor (PreventDamage("All") + compteurs 'damage')."""

    def encaisse(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)
        total = message.will_take_damage
        if total <= 0:
            return
        message.PreventDamage("All", effect)
        Faces.PlaceCountersOn([this], total, 'damage', effect)
        if this.GetCounters('damage') >= seuil:
            Faces.DiscardAll([this], effect)

    def le_porteur(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this.CastTo(Attachment)
        return message.trigger is this.GetBindFace()

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_type=Enemy, not_with_attach=CardFinder(trait="VEHICLE")),
            if_cannot_gain_surge=True,
            **choix,
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt, Enemy, encaisse, conditions=[le_porteur]),
    ]
```

### `src/cards/pack/fne/echo/__init__.py`

```python
from cards.pack import *
ASPECT_OR_BASIC_CLASSES = ('Aggression', 'Justice', 'Leadership', 'Protection', 'Basic', "'Pool")
def IsAspectOrBasicEvent(face: 'CardFace') -> bool:
    if not Event.IsType(face):
        return False
    return face.IsClass(*ASPECT_OR_BASIC_CLASSES)
def GetPrintedCostValue(face: 'CardFace') -> int:
    value = face.paper.desc.get('Cost', '')
    value = str(value).replace('*', '')
    try:
        cost = int(value)
    except ValueError:
        return 0
    return max(cost, 0)


# ----------------------------------------------------------------------------
# Photographic Reflexes (60040a / 60040b / 60040c), les TROIS variantes.
#
# « [star] If you are in hero form, you can discard Photographic Reflexes from
#   your hand to play an event tucked under Echo as if it were in your hand.
#   Reduce the cost to play that event by 2. You cannot trigger Echo's
#   "Watch and Learn" ability for that event. »
#
# Meme texte sur les trois, seule l'icone de ressource change (Y / B / R, lue
# dans `desc`) : un seul constructeur, appele par les trois modules.
#
# ⚠ POURQUOI CE MODULE EXISTE (21/09/2026, signalement n°17 de Yarro).
# Jusqu'ici les trois modules etaient VIDES : toute la mecanique vivait sur
# Echo, qui rendait la carte GLISSEE jouable et defaussait Photographic
# Reflexes en consequence. Le resultat en jeu etait juste, mais le joueur
# tenait en main une carte ni jouable ni defaussable, et en a conclu — a bon
# droit — a un defaut. Le texte, lui, part bien de Photographic Reflexes.
# Les DEUX chemins existent maintenant, et aucun n'a ete retire :
#   A : cliquer Photographic Reflexes -> choisir l'evenement glisse ;
#   B : cliquer l'evenement glisse -> Photographic Reflexes part seule.
#
# Cartes de reference :
#  - `an006` Angelic Ribbons / `al014` Lurking : « discard this card → » est un
#    COUT, donc `SetCostFunc(CostFunc.Discard("This"))`, jamais l'effet ;
#  - `21185` System Shock et `21032` Pip the Troll : une capacite DECLENCHEE
#    depuis la MAIN se monte sur `.CanWorkOnlyInHand()` ;
#  - `16130` Crystal Ball : « may play a card ..., reducing its resource cost »
#    -> `player.PlayOneCardLikeInTurn(faces, effect)`, qui demande LAQUELLE
#    puis la joue en payant vraiment.
#
# ⚠ `AbilityType.HeroAction` porte a lui seul le « If you are in hero form »
# (`Ability.GetAbilityTypeCondition` : `effect.GetInitiator().IsHero()`).
# ⚠ La reduction de 2 n'est PAS ici : elle est sur Echo, appliquee a toute
# carte payee depuis sa zone glissee, pour que les chemins A et B paient la
# meme chose et qu'une seconde copie en main ne la double pas.


# Drapeau pose par le chemin A pendant qu'il joue l'evenement glisse.
# ⚠ SANS LUI, DEUX Photographic Reflexes PARTENT POUR UN SEUL REJEU (mesure du
# 21/09/2026 : main ['60040a','60040b','60040c'], on clique 60040b, il reste
# ['60040c']). Le chemin A defausse la carte cliquee comme COUT ; Echo, elle,
# defausse une Photographic Reflexes des qu'une carte est jouee depuis sa zone
# glissee — ce qui est juste pour le chemin B, ou rien n'a encore ete paye, et
# faux pour le chemin A. Le drapeau dit a Echo « c'est deja paye ».
# Idiome repris de Magik (`aoa/magik/45030a.py`, `initiator.flag`).
REFLEXES_DEJA_PAYEES = "ECHO_REFLEXES_DEJA_PAYEES"


def EchoDeCeJoueur(effect: 'Effect') -> 'CardFace|None':
    """L'identite Echo du joueur qui declenche, ou None."""
    joueur = effect.GetInitiator()
    if joueur is None:
        return None
    identite = joueur.GetIdentity()
    if identite is None or not identite.IsName('Echo'):
        return None
    return identite


def EvenementsGlissesSousEcho(effect: 'Effect') -> List['CardFace']:
    """Les evenements actuellement glisses sous l'Echo de ce joueur."""
    identite = EchoDeCeJoueur(effect)
    if identite is None:
        return []
    zone = identite.GetPlacedCardArea()
    if zone is None:
        return []
    return [face for face in zone.Get(True)
            if face is not None and Event.IsType(face)]


def AbilitesPhotographicReflexes() -> Sequence['Ability']:
    def check_pas_payer_sa_propre_glissee(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> bool:
        """CORRECTIF (25/09/2026, signale en jeu). Sur le CHEMIN B, la
        permission de jouer la carte glissee (`check_tucked_playable`) est
        accordee DES que Photographic Reflexes est en main, et sa vraie
        defausse n'arrive qu'APRES coup (`discard_photographic_reflexes`,
        WhenPlayerPlayCard). Entre les deux, rien n'empechait de la depenser
        comme RESSOURCE GENERIQUE (regle de base, n'importe quelle carte en
        main) pour payer le cout — deja reduit de 2 — de la carte glissee
        qu'elle vient elle-meme d'autoriser. Le joueur gagnait alors la
        reduction ET la valeur de ressource sur la MEME carte, alors que
        `discard_photographic_reflexes` ne trouvait plus rien a defausser
        ensuite (elle avait deja quitte la main via la zone de ressources).

        Avec UNE SEULE copie en main, la depense comme ressource est donc
        refusee : il faut qu'une carte de la main paie normalement, et
        Photographic Reflexes partira comme prevu apres coup. Avec une
        SECONDE copie disponible pour porter ce vrai cout, rien ne l'empeche
        : ce n'est plus la meme carte qui financerait les deux avantages.
        """
        joueur = message.GetToPlayer()
        if joueur is None:
            return True
        identite = joueur.GetIdentity()
        if identite is None or not identite.IsName('Echo'):
            return True
        zone = identite.GetPlacedCardArea()
        if zone is None:
            return True
        paying_for = message.paying_for_effect.this
        if paying_for.card.area != zone:
            return True
        autres = [x for x in joueur.hand_cards.Get()
                  if x.IsName('Photographic Reflexes') and x != effect.this]
        return bool(autres)

    def il_y_a_un_evenement_glisse(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        # Sans evenement sous Echo, la carte ne doit pas etre cliquable du
        # tout : la defausser pour rien recreerait le defaut d'origine sous
        # une autre forme.
        return bool(EvenementsGlissesSousEcho(effect))

    def photographic_reflexes(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        faces = EvenementsGlissesSousEcho(effect)
        if joueur is None or not faces:
            return
        # `PlayOneCardLikeInTurn` DEMANDE laquelle quand il y en a plusieurs,
        # puis la joue comme si elle etait en main, cout reellement paye.
        #
        # ⚠ ARBITRAGE ASSUME : LE COUT EST PAYE D'ABORD, ET IL N'EST PAS RENDU.
        # `CostFunc.Discard("This")` defausse Photographic Reflexes AVANT cet
        # appel. Si le joueur renonce ensuite, ou s'il ne peut pas payer
        # l'evenement glisse, la carte cliquee est perdue et rien n'est joue.
        # Le chemin B, lui, ne consomme Photographic Reflexes qu'une fois le jeu
        # effectif : LES DEUX CHEMINS DIVERGENT DONC SUR CE SEUL POINT.
        # C'est la lecture litterale du texte imprime — « you can DISCARD
        # Photographic Reflexes from your hand TO play an event » fait de la
        # defausse un COUT, et un cout paye ne se reprend pas — et c'est le
        # comportement ordinaire du moteur pour `SetCostFunc`. Arbitrage non
        # confirme par un ruling : aucun n'existe (recherche du 21/09/2026).
        #
        # ⚠ Le drapeau couvre toute la resolution, pas seulement la carte
        # choisie. Sans effet observable : `discard_photographic_reflexes` ne
        # part que sur une carte jouee DEPUIS la zone glissee, et le chemin A
        # n'en joue qu'une.
        joueur.flag.Update(REFLEXES_DEJA_PAYEES, +1)
        try:
            joueur.PlayOneCardLikeInTurn(faces, effect)
        finally:
            joueur.flag.Update(REFLEXES_DEJA_PAYEES, -1)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            photographic_reflexes,
            conditions=[il_y_a_un_evenement_glisse],
        ).SetCostFunc(CostFunc.Discard("This"))
        .CanWorkOnlyInHand(),
        # Remplace la depense-comme-ressource par defaut de ClassCard (une
        # seule declaration : `ClassCard.GetAbilities` ne pose plus la sienne
        # des qu'elle en trouve une portant ce nom). Meme montant que le
        # comportement d'origine (`effect.this.printed_resource`), une garde
        # de plus.
        AbilityFactory.CheckThisCanDropPay(conditions=[check_pas_payer_sa_propre_glissee]),
    ]
```

### `src/cards/pack/fne/electro/__init__.py`

```python
from cards.pack import *
from cards.pack.fne import PeutCouvrirLeCout

# Helpers du set Electro (Fear No Evil, 60076-60085).
# Le stock du set est le compteur 'charge' pose sur l'attachement Electric
# Charge (60079), Permanent, attache a Electro.


def TrouverElectro(effect: 'Effect') -> 'Villain|None':
    return Worlds.FindCardOnField(effect, name="Electro", card_type=Villain)


def TrouverElectricCharge(effect: 'Effect') -> 'Attachment|None':
    return Worlds.FindCardOnField(effect, name="Electric Charge", card_type=Attachment)


def Charges(effect: 'Effect') -> int:
    charge = TrouverElectricCharge(effect)
    return charge.GetCounters('charge') if charge else 0


def PoserCharges(effect: 'Effect', n: 'int|str') -> None:
    charge = TrouverElectricCharge(effect)
    if charge:
        Faces.PlaceCountersOn([charge], n, 'charge', effect)


def RetirerCharges(effect: 'Effect', n: int) -> None:
    charge = TrouverElectricCharge(effect)
    if charge:
        Faces.RemoveCountersOn([charge], n, 'charge', effect)


def CapacitesDElectro(charges_par_manigance: int, charges_au_reveil: 'str|None') -> Sequence['Ability']:
    """When Revealed (I, II) : Find Electric Charge, attach it to Electro, and
    place 2[per_hero] charge counters on it. (III : place 3[per_hero] charge
    counters on Electric Charge, sans la chercher : elle y est deja.)
    [star] Forced Response : After Electro schemes, place N charge counter(s)
    on Electric Charge."""
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Villain)
        if TrouverElectricCharge(effect) is None:
            Find.FindAndAttachTo(effect, this, who_perform=message.GetToPlayer(), name="Electric Charge", card_type=Attachment)
        PoserCharges(effect, charges_au_reveil or "2*")

    def apres_manigance(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        PoserCharges(effect, charges_par_manigance)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.AfterUnitSchemeEnd(AbilityType.ForcedResponse, "This", apres_manigance),
    ]


def ChoixPayerEnergieOuDeux(joueur: 'Player', effect: 'Effect', nom: str, action: Callable[[], None]) -> Sequence['Ability']:
    """« Spend a [energy] resource or 2 resources of any type » : deux branches
    payantes, chacune offerte seulement si elle est payable (PeutCouvrirLeCout,
    lecon de Tug of War)."""
    return [
        AbilityFactory.ForChoiceAbilityWithCost(
            Cost("Y"), f"Spend [energy]: {nom}", lambda targets, res: action(),
            conditions=[lambda e, m: PeutCouvrirLeCout(joueur, e, Cost("Y"))]),
        AbilityFactory.ForChoiceAbilityWithCost(
            Cost("2"), f"Spend 2 resources: {nom}", lambda targets, res: action(),
            conditions=[lambda e, m: PeutCouvrirLeCout(joueur, e, Cost("2"))]),
    ]
```

### `src/cards/pack/fne/fear_no_evil_campaign/__init__.py`

```python
from cards.pack import *
from cards.pack.fne.campaign import Retirees, SOUTIENS_DAILY_BUGLE, PRISONNIERS_DU_RAFT

# Environnements de campagne (60205-60209, une carte, deux faces : Completed
# recto, Failed verso) et l'alliee Mary Walker (60210). Leur texte « Setup: »
# se resout quand la carte est deja en jeu, posee par la mise en place de
# campagne (cards/pack/fne/campaign.py) : AfterGameSetup, qui part APRES les
# mulligans (« Resolve Character Setup Abilities », journal du 18/09/2026), ce
# qui couvre aussi les « After resolving mulligans » du livret.


def ChercherEnMain(effect: 'Effect', joueur: 'Player', card_type) -> None:
    """« each player may search their deck and discard pile for a <type> and
    add it to their hand. In expert mode, each player who did so discards
    1 card from their hand. »"""
    face = Search.SearchForCard(
        effect, joueur,
        include_player_deck=True, include_player_discard_pile=True,
        card_type=card_type, may=True, not_move=True,
    )
    if face is None:
        return
    Faces.AddToHand([face], joueur, effect)
    if Worlds.IsExpert(effect):
        DefausserDeLaMain(effect, joueur, 1)


def DefausserDeLaMain(effect: 'Effect', joueur: 'Player', n: int) -> None:
    for _ in range(n):
        main = list(joueur.hand_cards.Get(True))
        if not main:
            return
        carte = main[0] if len(main) == 1 else joueur.AskChooseFace(main, effect, prompt="Choose a card to discard")
        if carte is None:
            return
        Faces.DiscardAll([carte], effect)


def RechuteVers(card_type):
    def apres_revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Ally)
        this.HealHealth("All", effect)
        this.card.Flip(effect)

    def par_son_controleur(effect: 'Effect', message: 'Message.WhenCardRevealed') -> bool:
        return message.GetToPlayer() is effect.this.GetControlByPlayer()

    return AbilityFactory.WhenCardRevealed(AbilityType.ForcedResponse, card_type, apres_revelation, conditions=[par_son_controleur])
```

### `src/cards/pack/fne/hammerhead/__init__.py`

```python
from cards.pack import *

# Helpers du set Hammerhead (Fear No Evil, 60086-60096).


def TrouverHammerhead(effect: 'Effect') -> 'Villain|None':
    """Le vilain Hammerhead en jeu, quel que soit son stade."""
    return Worlds.FindCardOnField(effect, name="Hammerhead", card_type=Villain)


def ReponseForceeCoupDeBoule(degats: int) -> 'Ability':
    """[star] Forced Response : After Hammerhead attacks and damages a
    character, stun that character. If that character was already stunned,
    deal N damage to them.

    Modele : 01118 Sonic Converter (AfterUnitAttackAndDamageUnit sur
    "Character", target_in_play=True). « already stunned » se lit AVANT de
    poser le statut : un personnage Steady a une carte peut etre re-etourdi
    sans avoir ete « stunned » au sens des regles.
    """
    def coup_de_boule(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Villain)
        cible = message.attacked
        deja_etourdi = cible.IsStunned()
        Faces.GiveStatus([cible], "Stunned", effect)
        if deja_etourdi:
            this.DealDamage([cible], degats, effect)

    return AbilityFactory.AfterUnitAttackAndDamageUnit(
        AbilityType.ForcedResponse,
        "This",
        "Character",
        coup_de_boule,
        target_in_play=True,
    )
```

### `src/cards/pack/fne/kingpin/__init__.py`

```python
from cards.pack import *
from cards.pack.fne import PeutCouvrirLeCout, RetournerLAttachement
from game.card.face.attribute.can_boost import CanBoost

# Helpers du set Kingpin (Fear No Evil, 60159-60176), scenario final.
# Le vilain est une carte RECTO-VERSO (A1/A2 en standard, B1/B2 en expert) :
# face 1 intouchable (Stalwart, pas de degats, pas d'amelioration, manigance
# au lieu d'attaquer), face 2 atteignable (Steady, MARTIAL ARTIST). C'est
# Public Support (60163a) qui le retourne au debut d'une phase du mechant.
# Les nemesis des joueurs sont mises en jeu par le complot (60161a Setup,
# 60162a When Revealed) et par les traitrises (60175, 60176).

TRAIT_ARTS_MARTIAUX = "MARTIAL ARTIST"
TRAIT_UNDERLING = "UNDERLING"
GABARIT_ALLIE_BLACK_CAT = "fne_black_cat_ally"   # ATK 0** / THW 0** (2 degats consecutifs), Villainous, THIEF UNDERLING (pack "")


def TrouverKingpin(effect: 'Effect') -> 'Villain|None':
    """Le vilain Kingpin en jeu, quelle que soit sa face. `card_type=Villain`
    ecarte le SBIRE nemesis d'Echo, qui porte le meme nom."""
    return Worlds.FindCardOnField(effect, name="Kingpin", card_type=Villain)


def KingpinArtMartial(effect: 'Effect') -> bool:
    """« If Kingpin has the MARTIAL ARTIST trait » : la face 2 seulement."""
    k = TrouverKingpin(effect)
    return k is not None and k.HasTrait(TRAIT_ARTS_MARTIAUX)


def TrouverPublicSupport(effect: 'Effect') -> 'Environment|None':
    return Worlds.FindCardOnField(effect, name="Public Support", card_type=Environment)


def SbireNemesisEnJeu(joueur: 'Player', effect: 'Effect') -> 'Minion|None':
    """« Your nemesis minion », s'il est en jeu (marqueur `nemesis_of_player`
    pose a la mise en place, lu par `CardFinder(is_nemesis=joueur)`)."""
    return Worlds.FindCardOnField(effect, finder=CardFinder(card_type=Minion, is_nemesis=joueur))


def SbiresNemesisMisDeCote(joueur: 'Player') -> List['Minion']:
    """Le(s) sbire(s) nemesis encore dans la reserve nemesis du joueur."""
    return [f for f in joueur.set_aside_nemesis_sets.Get()
            if Minion.IsType(f) and f.IsNemesis(joueur)]


def CartesNemesisMisesDeCote(joueur: 'Player') -> List['CardFace']:
    """« your set-aside nemesis set » : ce qui reste dans la reserve."""
    return [f for f in joueur.set_aside_nemesis_sets.Get()
            if f.card.area is joueur.set_aside_nemesis_sets]


def TrouverEtRevelerUnderling(effect: 'Effect', joueur: 'Player') -> 'Minion|None':
    """« finds an UNDERLING minion that is not in play and reveals it » :
    Find (deck, defausse, mise de cote), jamais une carte deja en jeu."""
    return Find.FindAndReveal(
        effect, joueur,
        finder=CardFinder(card_type=Minion, trait=TRAIT_UNDERLING,
                          check_effect_fn=lambda e, f: not f.IsInPlay()),
    )


def CapacitesDeKingpin1() -> Sequence['Ability']:
    """Face 1 (A1 / B1). Stalwart : base desc.
    « Kingpin cannot be dealt damage or have upgrades attached » :
    UnitCannotTakeDamage (sd022, rend une LISTE) + UnitCannotHaveUpgradeAttached
    (46003, liste aussi).
    « [star] Forced Interrupt: When Kingpin would attack you, he schemes
    instead » : WhenUnitWouldAttack + message.DoSchemeInstead (51019
    Invisibility Gear, ag005)."""
    def manigance(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.DoSchemeInstead(effect)

    moi = CardFinder(name="Kingpin", card_type=Villain)
    return [
        *AbilityFactory.UnitCannotTakeDamage(moi),
        *AbilityFactory.UnitCannotHaveUpgradeAttached(moi),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", manigance),
    ]


def CapacitesDeKingpin2(*, overkill: bool) -> Sequence['Ability']:
    """Face 2 (A2 / B2). Steady : base desc.
    « [star] Forced Interrupt: When Kingpin activates against you, if you are
    not engaged with a minion, give Kingpin 1 additional boost card for this
    activation [B2 : and this activation gains overkill if it is an attack] » :
    modele 60093 Maggia Underboss (WhenUnitWouldAttack + WhenUnitWouldScheme,
    GiveAdditionalBoostCardForThisActivation, condition dans `conditions`)."""
    def sans_sbire(effect: 'Effect', message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldScheme') -> bool:
        joueur = message.GetAgainstPlayer()
        return joueur is not None and joueur.engaged_minions.GetSize() == 0

    def boost_en_plus(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        message.GiveAdditionalBoostCardForThisActivation(1, effect)

    def boost_et_overkill(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GiveAdditionalBoostCardForThisActivation(1, effect)
        if overkill:
            message.GainOverKill(effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", boost_et_overkill, conditions=[sans_sbire]),
        AbilityFactory.WhenUnitWouldScheme(AbilityType.ForcedInterrupt, "This", boost_en_plus, conditions=[sans_sbire]),
    ]


def ReponseForceeSoutien() -> 'Ability':
    """Public Support (les deux faces) : « Forced Response: After a minion is
    defeated, place 1 support counter here » (60094 Consolidate Power)."""
    def sbire_vaincu(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        Faces.PlaceCountersOn([effect.this], 1, 'support', effect)

    return AbilityFactory.AfterUnitBeDefeated(AbilityType.ForcedResponse, Minion, sbire_vaincu)


def AttacheAKingpin() -> 'Ability':
    """« Attach to Kingpin » (When Revealed des PERSONA / WEAPON)."""
    return AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Kingpin", card_type=Villain))


def CapacitesDUnePersona(trait_evenement: str, nom_action: str,
                         a_la_revelation: Callable[['Effect', 'Player', 'Villain'], None],
                         action: Callable[['Effect', 'Player', 'Villain'], None],
                         ) -> Sequence['Ability']:
    """James Wesley / Vanessa Fisk : +1 SCH (desc SCH+).
    When Revealed: Attach to Kingpin [+ effet].
    Hero Action: Discard a <TRAIT> event from your hand -> discard this.
      Kingpin <schemes | attacks you>.
    [star] Boost: Attach this card to Kingpin.
    Modeles : 60117 (AttachToFaceWhenPutIntoPlay(Villain)), 45014
    (CostFunc.Discard("YourHandCards")), 21170 (WhenThisBoostAttachTo)."""
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        kingpin = TrouverKingpin(effect)
        if kingpin is not None:
            a_la_revelation(effect, message.GetToPlayer(), kingpin)

    def agir(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this
        joueur = effect.GetInitiator()
        kingpin = TrouverKingpin(effect)
        Faces.DiscardAll([this], effect)
        if kingpin is not None:
            action(effect, joueur, kingpin)

    return [
        AttacheAKingpin(),
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, agir)
            .SetName(nom_action)
            .SetCostFunc(CostFunc.Discard("YourHandCards", trait=trait_evenement, card_type=Event)),
        AbilityFactory.WhenThisBoostAttachTo(CardFinder(name="Kingpin", card_type=Villain)),
    ]


def ConvertirBlackCatEnAlliee(sbire: 'Minion', joueur: 'Player', effect: 'Effect') -> bool:
    """« take control of Black Cat as an ally » (an ally that takes 2
    consequential damage after she attacks or thwarts) : Faces.TreatAsAlly
    (faces.py:340, modele iron_patriot), gabarit fne_black_cat_ally (pack "",
    ajoute le 18/09/2026 : ATK 0** / THW 0**, Villainous 1, THIEF UNDERLING).
    TreatAsAlly recopie nom, image, ATK et SCH->THW ; les 2 degats consecutifs
    viennent des deux etoiles du gabarit ; Villainous est garde (FAQ du livret,
    `Ally` herite de HasVillainous depuis le 18/09/2026)."""
    return Faces.TreatAsAlly(sbire, GABARIT_ALLIE_BLACK_CAT, joueur, effect)
```

### `src/cards/pack/fne/protection_racket/__init__.py`

```python
from cards.pack import *
from cards.pack.fne import PeutCouvrirLeCout

# Protection Racket : CHAQUE joueur a son complot principal dans son aire de
# jeu (livret mc60 p. 13, « Separate Main Schemes »). Le moteur sait faire
# vivre plusieurs complots principaux a la fois (Tower Defense 21098/21099 :
# `world.area_schemes_main` en contient plusieurs, la phase du vilain les fait
# tous avancer, `Worlds.FindMainScheme` pose la question `GettingMainScheme`
# quand il y en a plus d'un). Ce module fournit :
#  - la propriete `proprietaire_racket` (player_id) posee sur la CARTE ;
#  - `GettingMainScheme` -> le complot du joueur courant (`world.current_player`
#    : le joueur qui joue, celui contre qui l'ennemi s'active, celui a qui la
#    carte rencontre est distribuee), sinon celui de son proprietaire ;
#  - « in this play area » = controle par le proprietaire, ou sbire engage avec
#    lui (livret : identites, allies, ameliorations, sbires...).
# Regle FFG (article Fear No Evil) : quand un ennemi manigance, la menace va
# SEULEMENT sur le complot du joueur contre qui il s'active. Ecart assume : un
# texte d'environnement ou de manigance annexe qui dit « the main scheme »
# tombe sur le complot du joueur courant, pas sur tous (livret p. 13).

NOMS_RACKET = ("Battle in the Bodega", "Bull in a China Shop", "Hung Out to Dry",
               "Pawn Shop Showdown", "A Slice of the Pizza Dough")
CLE = "proprietaire_racket"


def Proprietaire(face: 'CardFace') -> 'Player|None':
    pid = getattr(face.card, CLE, None)
    if pid is None:
        return None
    for p in face.card.world.players:
        if p.player_id == pid:
            return p
    return None


def ComplotsRacket(effect: 'Effect') -> List['MainScheme']:
    return [s for s in Worlds.GetAllMainSchemes(effect) if s.paper.set_name == "Protection Racket"]


def ComplotDuJoueur(effect: 'Effect', joueur: 'Player') -> 'MainScheme|None':
    for s in ComplotsRacket(effect):
        if Proprietaire(s) is joueur:
            return s
    return None


def DansCetteAire(face: 'CardFace', scheme: 'CardFace') -> bool:
    """« in this play area » : controle par le proprietaire du complot, ou
    sbire engage avec lui."""
    proprio = Proprietaire(scheme)
    if proprio is None or face is None:
        return False
    if Minion.IsType(face):
        return getattr(face, "engaged_player", None) is proprio
    if Enemy.IsType(face):
        # Le vilain n'est dans l'aire de personne. `WhenUnitBeDefeated(Unit2)`
        # arrive aussi pour lui (Bullseye I vaincu) et `GetControlByPlayer`
        # posait un assert : partie bloquee en autoplay (18/09/2026).
        return False
    # Un allie deja vaincu (AfterUnitTookDamage arrive apres la defausse)
    # n'a plus de controleur : son proprietaire fait foi.
    controleur = face.GetControlByOrOwner()
    if not Player.IsType(controleur):
        return False
    return controleur is proprio


def MettreEnJeuLeComplot(face_a: 'CardFace', joueur: 'Player', effect: 'Effect') -> 'MainScheme|None':
    """Un complot Protection Racket (face A, mis de cote) entre en jeu dans
    l'aire de `joueur` et se retourne sur sa face 1B (Reveal, comme Tower
    Defense 21098a fait entrer son second complot)."""
    setattr(face_a.card, CLE, joueur.player_id)
    face_a.Reveal(joueur, effect)
    return face_a.card.face.CastTo(MainScheme) if MainScheme.IsType(face_a.card.face) else None


def ComplotsDeCote(effect: 'Effect') -> List['CardFace']:
    return [f for f in Worlds.GetSetAsideAreaCards(effect)
            if MainScheme.IsType(f) and f.paper.set_name == "Protection Racket"]


def EchangerLeComplot(effect: 'Effect', joueur: 'Player') -> None:
    """Change of Venue : « Swap your main scheme with a random set-aside main
    scheme. Place the threat from the previous scheme on the new scheme. »
    Les attachements de l'ancien complot sont defausses (FAQ du livret)."""
    ancien = ComplotDuJoueur(effect, joueur)
    candidats = ComplotsDeCote(effect)
    if ancien is None or not candidats:
        return
    nouveau_a = Rand.RandomChoice(candidats, effect)
    menace = ancien.threat
    attaches = list(ancien.GetInventoryDeck().Get())
    if attaches:
        Faces.DiscardAll(attaches, effect)
    setattr(ancien.card, CLE, None)
    Faces.SetAside([ancien], effect)
    nouveau = MettreEnJeuLeComplot(nouveau_a, joueur, effect)
    if nouveau is not None and menace > 0:
        nouveau.PlaceThreatOnSchemes([nouveau], menace, effect)


def CapacitesCommunes1B() -> Sequence['Ability']:
    """Sur chaque face 1B : resolution de « the main scheme », defaite si
    n'importe quel complot est accompli ou un joueur elimine, et pion
    d'acceleration partage (« place that acceleration token near the villain :
    each token adds 1 threat to each main scheme »)."""

    def le_complot(effect: 'Effect', message: 'Message.GettingMainScheme') -> 'MainScheme|None':
        this = effect.this.CastTo(MainScheme)
        monde = effect.world
        courant = getattr(monde, "current_player", None)
        demandeur = getattr(message, "face", None) or getattr(message, "trigger", None)
        joueur = None
        if demandeur is not None:
            if Minion.IsType(demandeur):
                joueur = getattr(demandeur, "engaged_player", None)
            elif not EncounterCard.IsType(demandeur):
                joueur = demandeur.GetControlByPlayer()
        if joueur is None:
            joueur = courant
        # Un joueur qui possede plusieurs complots (cas de test, Puzzle.Reveal
        # d'un complot de rechange) : seul le PREMIER repond, sinon le dernier
        # SetReturn l'emporte au hasard de l'ordre des effets.
        if joueur is not None and ComplotDuJoueur(effect, joueur) is this:
            return this
        return None

    def elimine(effect: 'Effect', message: 'Message.WhenPlayerEliminated') -> None:
        Worlds.SetGameOver(False, effect)

    etat = {"en_cours": False}

    def partager(effect: 'Effect', message: 'Message.AfterCardPlacedToken') -> None:
        if etat["en_cours"]:
            return
        this = effect.this.CastTo(MainScheme)
        etat["en_cours"] = True
        try:
            for s in ComplotsRacket(effect):
                if s is not this:
                    s.PlaceAccelerationToken(1, effect)
        finally:
            etat["en_cours"] = False

    def un_pion_acceleration(effect: 'Effect', message: 'Message.AfterCardPlacedToken') -> bool:
        return not etat["en_cours"] and getattr(message, "token_name", None) == 'acceleration_token'

    def ranger(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        # La carte du deck de complots que personne n'a choisie : le moteur
        # l'a retournee d'office (world.py:542), on la met de cote ici, sur la
        # face 1B (les capacites de la face 1A ne vivent plus apres le flip).
        this = effect.this
        if getattr(this.card, CLE, None) is None and this.IsInPlay():
            Faces.SetAside([this], effect)

    return [
        AbilityFactory.AfterGameSetup(ranger),
        AbilityFactory.GetMainScheme(le_complot),
        Ability(AbilityType.NonKeyword, Message.WhenPlayerEliminated, [], elimine),
        AbilityFactory.AfterCardPlacedToken(AbilityType.ForcedResponse, "This", None, partager, conditions=[un_pion_acceleration]),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]


def CapacitesDe1A() -> Sequence['Ability']:
    """Setup: Each player chooses a single Protection Racket main scheme (at
    random in expert mode), places it in their play area, and flips it to its
    1B side. Set each unused main scheme aside, out of play.
    Cette carte (celle du deck de complots) est candidate comme les quatre
    mises de cote. Si personne ne la choisit, elle est mise de cote juste
    apres la mise en place (AfterGameSetup) : le moteur l'a deja retournee
    d'office (world.py:542), on ne peut pas l'en empecher sans le toucher."""

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        candidats: List['CardFace'] = [this] + ComplotsDeCote(effect)

        def choisir(player: 'Player') -> None:
            if not candidats:
                return
            if Worlds.IsExpert(effect):
                choix = Rand.RandomChoice(candidats, effect)
            else:
                choix = candidats[0] if len(candidats) == 1 else player.AskChooseFace(list(candidats), effect, prompt="Choose your Protection Racket main scheme")
            if choix is None:
                choix = candidats[0]
            candidats.remove(choix)
            if choix is this:
                setattr(this.card, CLE, player.player_id)
            else:
                MettreEnJeuLeComplot(choix, player, effect)

        Players.ForEachPlayer(effect, choisir)

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        if getattr(this.card, CLE, None) is None:
            joueur = message.GetToPlayer()
            if joueur is not None:
                setattr(this.card, CLE, joueur.player_id)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
```

### `src/cards/pack/fne/purple_man/__init__.py`

```python
from cards.pack import *

# Helpers du set Purple Man (Fear No Evil, 60097-60109).


def TrouverPurpleMan(effect: 'Effect') -> 'Villain|None':
    return Worlds.FindCardOnField(effect, name="Purple Man", card_type=Villain)


def CapacitesDePurpleMan(*, guard: bool, villainous: bool, patrol: bool) -> Sequence['Ability']:
    """Each INFLUENCED minion gains guard (II : and villainous ; III : guard,
    patrol, and villainous) -> GiveKeywordToInPlayWhenApplyThis (liste).
    Each boost card from the Purple Man encounter set gains « [star] Boost :
    After this activation, deal this card to yourself as a facedown encounter
    card » -> une seule capacite sur le vilain, WhenCardBecomeBoost filtre par
    set_name, `message.AfterThisActivation` (07009) puis `DealEncounterCard`
    (27093 Fearmonger). « yourself » = le joueur contre qui l'ennemi s'active.
    """
    mots = {}
    if guard: mots['guard'] = 1
    if villainous: mots['villainous'] = 1
    if patrol: mots['patrol'] = 1

    def du_set(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> bool:
        return message.trigger.paper.set_name == "Purple Man"

    def a_toi(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        carte = message.trigger
        joueur = message.GetToPlayer()

        def donner() -> None:
            if joueur is not None and not carte.IsInPlay():
                joueur.DealEncounterCard(carte, effect)

        message.AfterThisActivation(effect, donner)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(trait="INFLUENCED", card_type=Minion),
            **mots,
        ),
        AbilityFactory.WhenCardBecomeBoost(None, a_toi, conditions=[du_set]),
    ]


def ObligationCommandee(nom: str, action: Callable[['Effect', 'Player', 'Obligation'], None]) -> Sequence['Ability']:
    """« Fight. » / « Protect. » / « Serve. » : Uses (3 command counters) en
    base desc ; Forced Action : Exhaust this card and remove 1 command counter
    from it -> <effet>. Modele ls016 (WhenInYourPlayTurn(ForcedAction) +
    CostFunc.Exhaust("This")), le pion en second cout (CostFunc.Counter)."""
    def executer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        action(effect, effect.GetInitiator(), this)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.ForcedAction, executer)
            .SetName(nom)
            .SetCostFunc(CostFunc.Exhaust("This"))
            .SetCostFunc(CostFunc.Counter("This", 1, 'command')),
    ]
```

### `src/cards/pack/fne/sense_deck/__init__.py`

```python
from cards.pack import *
from cards.pack.fne.daredevil import SENSE_DECK_IDS
Unused(SENSE_DECK_IDS)
ENEMY_OR_SCHEME = (CardFinder(card_type=Enemy) | CardFinder(card_type=Scheme2))
def SenseDiscard(this: 'CardFace', by_effect: 'Effect') -> None:
    Faces.DiscardAll([this], by_effect)
```

### `src/cards/pack/fne/stop_the_presses/__init__.py`

```python
from cards.pack import *


def SoutiensDailyBugle(effect: 'Effect', joueur: 'Player|None'=None) -> List['CardFace']:
    """Les soutiens DAILY BUGLE en jeu (sous le controle de `joueur` si donne)."""
    faces = Worlds.FindCardsOnField(effect, trait="DAILY BUGLE", card_type=Support)
    if joueur is not None:
        faces = [f for f in faces if f.GetControlByPlayer() is joueur]
    return list(faces)


def RetirerUneEndurance(face: 'CardFace', effect: 'Effect') -> None:
    Faces.RemoveCountersOn([face], 1, 'stamina', effect)


def CoutDeReporter() -> Sequence['CostFunc.Base']:
    """« Exhaust <nom> and remove 1 stamina counter from him » : deux couts
    (60105 Fight., meme patron)."""
    return [CostFunc.Exhaust("This"), CostFunc.Counter("This", 1, 'stamina')]
```

### `src/cards/pack/fne/the_getaway/__init__.py`

```python
from cards.pack import *
from cards.pack.fne import PeutCouvrirLeCout, RetournerLAttachement


def CompteursDeVitesse(effect: 'Effect') -> int:
    """« speed counters on the main scheme »."""
    scheme = Worlds.FindMainScheme(effect)
    return scheme.GetCounters('speed') if scheme is not None else 0


def TrouverOutFrontOuAlongside(effect: 'Effect') -> 'Attachment|None':
    face = Worlds.FindCardOnField(effect, name="Out Front", card_type=Attachment)
    if face is None:
        face = Worlds.FindCardOnField(effect, name="Alongside", card_type=Attachment)
    return face


def PourChaqueCompteurDeVitesse(effect: 'Effect', joueur: 'Player', branches: Callable[[], Sequence['Ability']]) -> None:
    """Burning Rubber / Pedestrians : « For each speed counter on the main
    scheme, choose: ... » -> un choix par compteur (60083 Chain Lightning)."""
    for _ in range(CompteursDeVitesse(effect)):
        joueur.ChooseAbilities(effect, *branches())
```

### `src/cards/pack/fne/the_raft_breakout/__init__.py`

```python
from cards.pack import *
from cards.pack.fne import PeutCouvrirLeCout


def DistribuerLesBoostsDeCeType(effect: 'Effect', message: 'Message.WhenCardBecomeBoost', type_carte, *, attaque: bool, vilain_seulement: bool) -> None:
    """Master Key / Mysterio : « deal each of that activation's boost cards that
    is a <minion|treachery> to yourself as a facedown encounter card ». Meme
    patron que Purple Man (WhenCardBecomeBoost + AfterThisActivation +
    DealEncounterCard) ; `yourself` = le joueur contre qui l'ennemi s'active."""
    carte = message.trigger
    if not type_carte.IsType(carte):
        return
    ennemi = message.activating_enemy
    if vilain_seulement and not Villain.IsType(ennemi):
        return
    if ennemi is not effect.this.GetBindFace() if vilain_seulement else ennemi is not effect.this:
        return
    est_attaque = message.being_message.IsAttack() if message.being_message is not None else False
    if attaque != est_attaque:
        return
    joueur = message.GetToPlayer()

    def donner() -> None:
        if joueur is not None and not carte.IsInPlay():
            joueur.DealEncounterCard(carte, effect)

    message.AfterThisActivation(effect, donner)


def EstUnDeceived(face: 'CardFace') -> bool:
    return Minion.IsType(face) and face.HasTrait("DECEIVED") and face.card.IsAsOtherCard()


def ConvertirEnDeceived(face: 'CardFace', effect: 'Effect') -> 'Minion|None':
    """Baron Zemo : « Treat each ally with threat on it as a DECEIVED minion
    with a blank text box. Its SCH is equal to its base THW and it does not
    take consequential damage. » Copie de la branche diff == 1 de
    `TreatAttachedCardAsMinion` (treat.py), sans le cadre `apply` (qui ne sait
    pas defaire la conversion sur retrait du jeton) ni les temporaires de
    `TreatAsMinion`. PV, degats et jetons vivent sur la CARTE : le sbire les
    garde. Le sbire s'engage avec le controleur de l'allie."""
    from game.card.factory import CardFactory
    from cards.database import CardsDB
    if not Ally.IsType(face) or face.card.IsAsOtherCard():
        return None
    joueur = face.GetControlByPlayer()
    if joueur is None:
        return None
    paper = CardFactory.FindCardPapers("Deceived Minion")[0]
    minion = CardFactory.CreateFace(paper, effect.world)
    minion.pic_id = face.paper.card_id
    minion.SetName(face.printed_name)
    minion.SetSubtitle(face.printed_subtitle)
    minion.printed_attack = face.printed_attack
    minion.printed_scheme = face.printed_thwart
    minion = face.card.SwapCardFace(minion, effect, no_detach=True)
    if not minion.IsInPlay():
        return None
    minion.ability.Add(*CardsDB.FindAbilities(paper.card_id, paper.pack, paper.set_name))
    minion.effect.face = minion
    CardFactory.FaceRegisterEffects(minion)
    # Meme sauvegarde que le correctif du 18/09/2026 dans treat.py : les
    # mots-cles donnes par d'autres faces survivent au ResetKeywords.
    etrangers = {k: {f: v for f, v in d.items() if f is not minion and v}
                 for k, d in minion.keywords.items()}
    minion.ResetKeywords()
    for k, d in etrangers.items():
        for f, v in d.items():
            minion.keywords.setdefault(k, {})
            minion.keywords[k][f] = minion.keywords[k].get(f, 0) + v
    if hasattr(minion, "SetGuardPatrolEffectedBy"):
        minion.SetGuardPatrolEffectedBy(minion.IsGuard(), minion.IsPatrol())
    minion.EngagePlayer(joueur, effect)
    minion.PutIntoPlay(joueur, effect)
    return minion


def RendreLAllie(minion: 'CardFace', effect: 'Effect') -> 'CardFace|None':
    """Le sbire DECEIVED redevient l'allie imprime, sous le controle du joueur
    avec qui il etait engage (= son controleur d'origine) ; les jetons restent
    sur la carte (FAQ : « threat remains »)."""
    if not EstUnDeceived(minion):
        return None
    joueur = minion.CastTo(Minion).GetEngagedPlayer()
    face = minion.card.SwapBackToPrintedCard(effect)
    if face.IsInPlay() and not face.IsDefeated():
        face.PutIntoPlay(joueur, effect, under_control=True)
    else:
        Faces.DiscardAll([face], effect)
    return face
```

### `src/cards/pack/fne/tombstone/__init__.py`

```python
from cards.pack import *
import re


def AttacheAuSbireLePlusSolide() -> 'Ability':
    """« Attach to the minion with the highest base hit points and give that
    minion a tough status card. Otherwise, this card gains surge. »
    highest_printed_hp = PV imprimes (« base »), when_attach_operation pose la
    robustesse au moment de l'accrochage."""
    return AbilityFactory.AttachToFaceWhenPutIntoPlay(
        Minion,
        highest_printed_hp=True,
        if_cannot_gain_surge=True,
        when_attach_operation=lambda face, effect: Faces.GiveStatus([face], "Tough", effect),
    )


def PeutSAccrocherAUnSbire(face: 'CardFace', sbire: 'CardFace') -> bool:
    """« an attachment that can attach to a minion » (60197 Beetle).
    La regle moteur `Asset2.CanAttachTo` (asset.py:69) ne connait que MaxPerUnit
    et `CheckIfFaceCanAttachTo` : elle acceptait Energy Gatling Gun (« Attach to
    the villain ») sur un sbire (harnais du 18/09/2026). La VRAIE cible
    imprimee vit dans le selecteur de `AttachToFaceWhenPutIntoPlayInternal`,
    expose depuis le 18/09/2026 (coordinateur) en `ability.attach_selector`
    sur l'ability `func_name="AttachToWhenEnterPlay"`.
    On interroge `selector_filter.CheckFinder(sbire, effet)` : le finder
    (Villain / Minion / Enemy, `non_trait`, `not_with_attach`...) et ses
    conditions (`CanAttachTo`, MaxPerUnit), SANS `selector_rule.Process`
    (le tri highest_printed_hp / highest_atk de `GetAllLegalTargets`), sinon
    « peut s'accrocher a un sbire » dependrait des AUTRES sbires en jeu.
    Repli, seulement si aucune ability n'expose de selecteur (attachement
    ecrit sans cette fabrique) : relecture de la phrase imprimee
    « Attach to ... » du texte de la carte."""
    if not Attachment.IsType(face) or not face.CastTo(Attachment).CanAttachTo(sbire):
        return False
    selecteurs = [getattr(a, "attach_selector", None)
                  for a in face.ability.Find(func_name="AttachToWhenEnterPlay")]
    selecteurs = [x for x in selecteurs if x is not None]
    if selecteurs:
        from game.effect.rule import GameRule   # pas re-exporte par cards.pack
        effet = GameRule(face)
        return any(sel.selector_filter.CheckFinder(sbire, effet) for sel in selecteurs)
    # Repli texte (aucun selecteur expose).
    texte = getattr(face.paper, "text", "") or ""
    m = re.search(r"\battach(?:es)? (?:this card )?to (?:the |a |an |each )?([^.\n]*)", texte, re.I)
    if not m:
        return True
    phrase = m.group(1).lower()
    if not re.search(r"\b(minion|enemy|character)\b", phrase):
        return False
    for trait in re.findall(r"non-\[\[([^\]]+)\]\]", phrase):
        if sbire.HasTrait(trait.upper()):
            return False
    for trait in re.findall(r"(?<!non-)\[\[([^\]]+)\]\] (?:minion|enemy|character)", phrase):
        if not sbire.HasTrait(trait.upper()):
            return False
    return True
```

### `src/cards/pack/fne/tracksuit_mafia/__init__.py`

```python
from cards.pack import *


def TrouverTracksuitMafia(effect: 'Effect') -> 'EncounterSideScheme|None':
    return Worlds.FindCardOnField(effect, name="Tracksuit Mafia", card_type=EncounterSideScheme)
```

### `src/cards/pack/fne/typhoid_mary/__init__.py`

```python
from cards.pack import *
from cards.pack.fne import PeutCouvrirLeCout

# Helpers du set Typhoid Mary (Fear No Evil, 60110-60120).
# Le vilain est une carte RECTO-VERSO (Typhoid Mary / Bloody Mary), sur une
# face au hasard a la mise en place, retournee a la fin de chaque phase du
# mechant. On ne le vainc pas : chaque « defaite » pose un jeton damage sur
# Disturbed Psyche et remet ses PV ; Establish Trust vaincue pose un jeton
# threat. Trois jetons = victoire. Modele du vilain : MaGog 39001a/b.


def TrouverMary(effect: 'Effect') -> 'Villain|None':
    """La face active, quelle qu'elle soit."""
    for nom in ("Typhoid Mary", "Bloody Mary"):
        v = Worlds.FindCardOnField(effect, name=nom, card_type=Villain)
        if v:
            return v
    return None


def TrouverDisturbedPsyche(effect: 'Effect') -> 'Environment|None':
    return Worlds.FindCardOnField(effect, name="Disturbed Psyche", card_type=Environment)


def TrouverMaryWalker(effect: 'Effect') -> 'Attachment|None':
    return Worlds.FindCardOnField(effect, name="Mary Walker", card_type=Attachment)


def MaryActive(effect: 'Effect', nom: str) -> bool:
    """« If Typhoid Mary is activating » / « If Bloody Mary is activating » :
    la face VISIBLE du vilain porte ce nom."""
    v = TrouverMary(effect)
    return v is not None and v.IsName(nom)


def JetonsPsyche(effect: 'Effect') -> int:
    env = TrouverDisturbedPsyche(effect)
    if env is None:
        return 0
    return env.GetTokens('damage') + env.GetTokens('threat')


def VerifierVictoire(effect: 'Effect') -> None:
    """If there are 3 or more tokens here, the players win the game!"""
    if JetonsPsyche(effect) >= 3 and not Worlds.IsGameOver(effect):
        Worlds.SetGameOver(True, effect)


def FlipMaryWalkerVersEstablishTrust(effect: 'Effect', joueur: 'Player') -> None:
    """« flip it and reveal Establish Trust » : l'attachement Mary Walker
    (113b) se retourne en manigance Establish Trust (113a), qui est revelee."""
    mw = TrouverMaryWalker(effect)
    if mw is None:
        return
    mw.card.Flip(effect, call_reveal=False)
    face = mw.card.face
    face.Reveal(joueur, effect)


def CapacitesDeMary(pv: str) -> Sequence['Ability']:
    """Forced Interrupt : When <Mary> would be defeated, place 1 damage token
    on Disturbed Psyche instead and reset her hit points to N[per_hero]."""
    def vaincue(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(EncounterVillain)
        message.SetBeInstead(effect)
        this.ResetHealth(effect, num=pv)
        env = TrouverDisturbedPsyche(effect)
        if env:
            Faces.PlaceTokensOn([env], 1, 'damage', effect)
        VerifierVictoire(effect)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.ForcedInterrupt, "This", vaincue),
    ]
```

## 3. Les scénarios et les sets de rencontre

### `data/scenarios/art_museum_heist_bullseye.json`

```json
{
    "version": "0.5.8",
    "name": "Art Museum Heist (Bullseye)",
    "villain": [
        "60065",
        "60066"
    ],
    "expert": false,
    "schemes": [
        "60121a,60121b"
    ],
    "set_aside": [
        "60122",
        "60123",
        "60124",
        "60125"
    ],
    "encounters": [],
    "encounter_sets": [
        "bullseye",
        "art_museum_heist",
        "standard"
    ],
    "modular_sets": [
        "cops",
        "the_owl"
    ]
}
```

### `data/scenarios/art_museum_heist_bullseye_expert.json`

```json
{
    "version": "0.5.8",
    "name": "Art Museum Heist (Bullseye)",
    "villain": [
        "60066",
        "60067"
    ],
    "expert": true,
    "schemes": [
        "60121a,60121b"
    ],
    "set_aside": [
        "60122",
        "60123",
        "60124",
        "60125"
    ],
    "encounters": [],
    "encounter_sets": [
        "bullseye",
        "art_museum_heist",
        "standard",
        "expert"
    ],
    "modular_sets": [
        "cops",
        "the_owl"
    ]
}
```

### `data/scenarios/art_museum_heist_typhoid_mary.json`

```json
{
    "version": "0.5.8",
    "name": "Art Museum Heist (Typhoid Mary)",
    "villain": [
        "60110a,60110b"
    ],
    "expert": false,
    "schemes": [
        "60121a,60121b"
    ],
    "set_aside": [
        "60122",
        "60123",
        "60124",
        "60125"
    ],
    "encounters": [],
    "encounter_sets": [
        "typhoid_mary",
        "art_museum_heist",
        "standard"
    ],
    "modular_sets": [
        "cops",
        "the_owl"
    ]
}
```

### `data/scenarios/art_museum_heist_typhoid_mary_expert.json`

```json
{
    "version": "0.5.8",
    "name": "Art Museum Heist (Typhoid Mary)",
    "villain": [
        "60111a,60111b"
    ],
    "expert": true,
    "schemes": [
        "60121a,60121b"
    ],
    "set_aside": [
        "60122",
        "60123",
        "60124",
        "60125"
    ],
    "encounters": [],
    "encounter_sets": [
        "typhoid_mary",
        "art_museum_heist",
        "standard",
        "expert"
    ],
    "modular_sets": [
        "cops",
        "the_owl"
    ]
}
```

### `data/scenarios/kingpin_fne.json`

```json
{
    "version": "0.5.8",
    "name": "Kingpin",
    "villain": [
        "60159a,60159b"
    ],
    "expert": false,
    "schemes": [
        "60161a,60161b",
        "60162a,60162b"
    ],
    "set_aside": [
        "60163a,60163b"
    ],
    "encounters": [],
    "encounter_sets": [
        "kingpin_fne"
    ],
    "modular_sets": [
        "tombstone",
        "tracksuit_mafia"
    ]
}
```

### `data/scenarios/kingpin_fne_expert.json`

```json
{
    "version": "0.5.8",
    "name": "Kingpin",
    "villain": [
        "60160a,60160b"
    ],
    "expert": true,
    "schemes": [
        "60161a,60161b",
        "60162a,60162b"
    ],
    "set_aside": [
        "60163a,60163b"
    ],
    "encounters": [],
    "encounter_sets": [
        "kingpin_fne",
        "expert"
    ],
    "modular_sets": [
        "tombstone",
        "tracksuit_mafia"
    ]
}
```

### `data/scenarios/protection_racket_bullseye.json`

```json
{
    "version": "0.5.8",
    "name": "Protection Racket (Bullseye)",
    "villain": [
        "60065",
        "60066"
    ],
    "expert": false,
    "schemes": [
        "60134a,60134b"
    ],
    "set_aside": [
        "60135a,60135b",
        "60136a,60136b",
        "60137a,60137b",
        "60138a,60138b"
    ],
    "encounters": [],
    "encounter_sets": [
        "bullseye",
        "protection_racket",
        "standard"
    ],
    "modular_sets": [
        "disasters",
        "tracksuit_mafia"
    ]
}
```

### `data/scenarios/protection_racket_bullseye_expert.json`

```json
{
    "version": "0.5.8",
    "name": "Protection Racket (Bullseye)",
    "villain": [
        "60066",
        "60067"
    ],
    "expert": true,
    "schemes": [
        "60134a,60134b"
    ],
    "set_aside": [
        "60135a,60135b",
        "60136a,60136b",
        "60137a,60137b",
        "60138a,60138b"
    ],
    "encounters": [],
    "encounter_sets": [
        "bullseye",
        "protection_racket",
        "standard",
        "expert"
    ],
    "modular_sets": [
        "disasters",
        "tracksuit_mafia"
    ]
}
```

### `data/scenarios/protection_racket_typhoid_mary.json`

```json
{
    "version": "0.5.8",
    "name": "Protection Racket (Typhoid Mary)",
    "villain": [
        "60110a,60110b"
    ],
    "expert": false,
    "schemes": [
        "60134a,60134b"
    ],
    "set_aside": [
        "60135a,60135b",
        "60136a,60136b",
        "60137a,60137b",
        "60138a,60138b"
    ],
    "encounters": [],
    "encounter_sets": [
        "typhoid_mary",
        "protection_racket",
        "standard"
    ],
    "modular_sets": [
        "disasters",
        "tracksuit_mafia"
    ]
}
```

### `data/scenarios/protection_racket_typhoid_mary_expert.json`

```json
{
    "version": "0.5.8",
    "name": "Protection Racket (Typhoid Mary)",
    "villain": [
        "60111a,60111b"
    ],
    "expert": true,
    "schemes": [
        "60134a,60134b"
    ],
    "set_aside": [
        "60135a,60135b",
        "60136a,60136b",
        "60137a,60137b",
        "60138a,60138b"
    ],
    "encounters": [],
    "encounter_sets": [
        "typhoid_mary",
        "protection_racket",
        "standard",
        "expert"
    ],
    "modular_sets": [
        "disasters",
        "tracksuit_mafia"
    ]
}
```

### `data/scenarios/stop_the_presses_bullseye.json`

```json
{
    "version": "0.5.8",
    "name": "Stop the Presses! (Bullseye)",
    "villain": [
        "60065",
        "60066"
    ],
    "expert": false,
    "schemes": [
        "60151a,60151b"
    ],
    "set_aside": [
        "60152",
        "60153",
        "60154",
        "60155",
        "60156"
    ],
    "encounters": [],
    "encounter_sets": [
        "bullseye",
        "stop_the_presses",
        "standard"
    ],
    "modular_sets": [
        "tombstone",
        "tracksuit_mafia"
    ]
}
```

### `data/scenarios/stop_the_presses_bullseye_expert.json`

```json
{
    "version": "0.5.8",
    "name": "Stop the Presses! (Bullseye)",
    "villain": [
        "60066",
        "60067"
    ],
    "expert": true,
    "schemes": [
        "60151a,60151b"
    ],
    "set_aside": [
        "60152",
        "60153",
        "60154",
        "60155",
        "60156"
    ],
    "encounters": [],
    "encounter_sets": [
        "bullseye",
        "stop_the_presses",
        "standard",
        "expert"
    ],
    "modular_sets": [
        "tombstone",
        "tracksuit_mafia"
    ]
}
```

### `data/scenarios/stop_the_presses_typhoid_mary.json`

```json
{
    "version": "0.5.8",
    "name": "Stop the Presses! (Typhoid Mary)",
    "villain": [
        "60110a,60110b"
    ],
    "expert": false,
    "schemes": [
        "60151a,60151b"
    ],
    "set_aside": [
        "60152",
        "60153",
        "60154",
        "60155",
        "60156"
    ],
    "encounters": [],
    "encounter_sets": [
        "typhoid_mary",
        "stop_the_presses",
        "standard"
    ],
    "modular_sets": [
        "tombstone",
        "tracksuit_mafia"
    ]
}
```

### `data/scenarios/stop_the_presses_typhoid_mary_expert.json`

```json
{
    "version": "0.5.8",
    "name": "Stop the Presses! (Typhoid Mary)",
    "villain": [
        "60111a,60111b"
    ],
    "expert": true,
    "schemes": [
        "60151a,60151b"
    ],
    "set_aside": [
        "60152",
        "60153",
        "60154",
        "60155",
        "60156"
    ],
    "encounters": [],
    "encounter_sets": [
        "typhoid_mary",
        "stop_the_presses",
        "standard",
        "expert"
    ],
    "modular_sets": [
        "tombstone",
        "tracksuit_mafia"
    ]
}
```

### `data/scenarios/the_getaway_bullseye.json`

```json
{
    "version": "0.5.8",
    "name": "The Getaway (Bullseye)",
    "villain": [
        "60065",
        "60066"
    ],
    "expert": false,
    "schemes": [
        "60128a,60128b"
    ],
    "set_aside": [
        "60129a,60129b"
    ],
    "encounters": [],
    "encounter_sets": [
        "bullseye",
        "the_getaway",
        "standard"
    ],
    "modular_sets": [
        "cops",
        "drive"
    ]
}
```

### `data/scenarios/the_getaway_bullseye_expert.json`

```json
{
    "version": "0.5.8",
    "name": "The Getaway (Bullseye)",
    "villain": [
        "60066",
        "60067"
    ],
    "expert": true,
    "schemes": [
        "60128a,60128b"
    ],
    "set_aside": [
        "60129a,60129b"
    ],
    "encounters": [],
    "encounter_sets": [
        "bullseye",
        "the_getaway",
        "standard",
        "expert"
    ],
    "modular_sets": [
        "cops",
        "drive"
    ]
}
```

### `data/scenarios/the_getaway_typhoid_mary.json`

```json
{
    "version": "0.5.8",
    "name": "The Getaway (Typhoid Mary)",
    "villain": [
        "60110a,60110b"
    ],
    "expert": false,
    "schemes": [
        "60128a,60128b"
    ],
    "set_aside": [
        "60129a,60129b"
    ],
    "encounters": [],
    "encounter_sets": [
        "typhoid_mary",
        "the_getaway",
        "standard"
    ],
    "modular_sets": [
        "cops",
        "drive"
    ]
}
```

### `data/scenarios/the_getaway_typhoid_mary_expert.json`

```json
{
    "version": "0.5.8",
    "name": "The Getaway (Typhoid Mary)",
    "villain": [
        "60111a,60111b"
    ],
    "expert": true,
    "schemes": [
        "60128a,60128b"
    ],
    "set_aside": [
        "60129a,60129b"
    ],
    "encounters": [],
    "encounter_sets": [
        "typhoid_mary",
        "the_getaway",
        "standard",
        "expert"
    ],
    "modular_sets": [
        "cops",
        "drive"
    ]
}
```

### `data/scenarios/the_raft_breakout_bullseye.json`

```json
{
    "version": "0.5.8",
    "name": "The Raft Breakout (Bullseye)",
    "villain": [
        "60065",
        "60066"
    ],
    "expert": false,
    "schemes": [
        "60142a,60142b"
    ],
    "set_aside": [
        "60143"
    ],
    "encounters": [],
    "encounter_sets": [
        "bullseye",
        "the_raft_breakout",
        "standard"
    ],
    "modular_sets": [
        "the_owl",
        "tombstone"
    ]
}
```

### `data/scenarios/the_raft_breakout_bullseye_expert.json`

```json
{
    "version": "0.5.8",
    "name": "The Raft Breakout (Bullseye)",
    "villain": [
        "60066",
        "60067"
    ],
    "expert": true,
    "schemes": [
        "60142a,60142b"
    ],
    "set_aside": [
        "60143"
    ],
    "encounters": [],
    "encounter_sets": [
        "bullseye",
        "the_raft_breakout",
        "standard",
        "expert"
    ],
    "modular_sets": [
        "the_owl",
        "tombstone"
    ]
}
```

### `data/scenarios/the_raft_breakout_typhoid_mary.json`

```json
{
    "version": "0.5.8",
    "name": "The Raft Breakout (Typhoid Mary)",
    "villain": [
        "60110a,60110b"
    ],
    "expert": false,
    "schemes": [
        "60142a,60142b"
    ],
    "set_aside": [
        "60143"
    ],
    "encounters": [],
    "encounter_sets": [
        "typhoid_mary",
        "the_raft_breakout",
        "standard"
    ],
    "modular_sets": [
        "the_owl",
        "tombstone"
    ]
}
```

### `data/scenarios/the_raft_breakout_typhoid_mary_expert.json`

```json
{
    "version": "0.5.8",
    "name": "The Raft Breakout (Typhoid Mary)",
    "villain": [
        "60111a,60111b"
    ],
    "expert": true,
    "schemes": [
        "60142a,60142b"
    ],
    "set_aside": [
        "60143"
    ],
    "encounters": [],
    "encounter_sets": [
        "typhoid_mary",
        "the_raft_breakout",
        "standard",
        "expert"
    ],
    "modular_sets": [
        "the_owl",
        "tombstone"
    ]
}
```

### `data/encounter_sets/art_museum_heist.json`

```json
{
    "version": "0.5.8",
    "name": "Art Museum Heist",
    "encounters": [
        "60126",
        "60126",
        "60127",
        "60127"
    ]
}
```

### `data/encounter_sets/bullseye.json`

```json
{
    "version": "0.5.8",
    "name": "Bullseye",
    "encounters": [
        "60068a,60068b",
        "60069",
        "60070",
        "60071",
        "60071",
        "60071",
        "60072",
        "60073",
        "60074",
        "60075",
        "60075"
    ]
}
```

### `data/encounter_sets/cops.json`

```json
{
    "version": "0.5.8",
    "name": "Cops",
    "encounters": [
        "60182",
        "60182",
        "60183",
        "60184",
        "60185"
    ]
}
```

### `data/encounter_sets/disasters.json`

```json
{
    "version": "0.5.8",
    "name": "Disasters",
    "encounters": [
        "60177",
        "60178",
        "60179",
        "60180",
        "60181"
    ]
}
```

### `data/encounter_sets/drive.json`

```json
{
    "version": "0.5.8",
    "name": "Drive",
    "encounters": [
        "60186",
        "60187",
        "60188",
        "60189",
        "60190"
    ]
}
```

### `data/encounter_sets/expert.json`

```json
{
    "version": "0.5.8",
    "name": "Expert",
    "encounters": [
        "01191",
        "01192",
        "01193"
    ]
}
```

### `data/encounter_sets/kingpin_fne.json`

```json
{
    "version": "0.5.8",
    "name": "Kingpin",
    "encounters": [
        "60164",
        "60165",
        "60166",
        "60167",
        "60168",
        "60169",
        "60170",
        "60171",
        "60172",
        "60173",
        "60174",
        "60175",
        "60175",
        "60176",
        "60176"
    ]
}
```

### `data/encounter_sets/protection_racket.json`

```json
{
    "version": "0.5.8",
    "name": "Protection Racket",
    "encounters": [
        "60139",
        "60140",
        "60141",
        "60141"
    ]
}
```

### `data/encounter_sets/stop_the_presses.json`

```json
{
    "version": "0.5.8",
    "name": "Stop the Presses!",
    "encounters": [
        "60157",
        "60158",
        "60158"
    ]
}
```

### `data/encounter_sets/the_getaway.json`

```json
{
    "version": "0.5.8",
    "name": "The Getaway",
    "encounters": [
        "60130",
        "60131",
        "60132",
        "60132",
        "60133",
        "60133"
    ]
}
```

### `data/encounter_sets/the_owl.json`

```json
{
    "version": "0.5.8",
    "name": "The Owl",
    "encounters": [
        "60191",
        "60191",
        "60192",
        "60193",
        "60194"
    ]
}
```

### `data/encounter_sets/the_raft_breakout.json`

```json
{
    "version": "0.5.8",
    "name": "The Raft Breakout",
    "encounters": [
        "60144",
        "60145",
        "60146",
        "60147",
        "60148",
        "60149",
        "60150"
    ]
}
```

### `data/encounter_sets/tombstone.json`

```json
{
    "version": "0.5.8",
    "name": "Tombstone",
    "encounters": [
        "60195",
        "60196",
        "60197",
        "60198",
        "60199"
    ]
}
```

### `data/encounter_sets/tracksuit_mafia.json`

```json
{
    "version": "0.5.8",
    "name": "Tracksuit Mafia",
    "encounters": [
        "60200",
        "60201",
        "60202",
        "60202",
        "60203",
        "60203",
        "60204"
    ]
}
```

### `data/encounter_sets/typhoid_mary.json`

```json
{
    "version": "0.5.8",
    "name": "Typhoid Mary",
    "encounters": [
        "60112",
        "60113a,60113b",
        "60114",
        "60115",
        "60115",
        "60116",
        "60117",
        "60118",
        "60118",
        "60119",
        "60120",
        "60120",
        "60120"
    ]
}
```

## 4. La campagne

### `data/campagnes/fne.json`

```json
{
    "version": "1.0",
    "code": "fne",
    "cle_extension": "60. Fear No Evil",
    "nom": "Peur de Rien",
    "nom_en": "Fear No Evil",
    "resume": "Une vague de crime orchestrée par le Caïd. Cinq affaires à résoudre dans l'ordre de votre choix, chacune contre un sous-fifre différent ; avant chaque partie, deux affaires non résolues progressent au hasard et une affaire qui progresse trois fois est perdue. Quand les cinq sont résolues, gagnées ou perdues, Kingpin vous attend.",
    "resume_en": "A crime wave orchestrated by the Kingpin. Five cases to solve in any order, each against a different underling villain; before each game, two unresolved cases progress at random, and a case that progresses three times is lost. Once all five are resolved, won or lost, Kingpin awaits.",
    "ordre_libre": true,
    "pages_regles": [
        "00-campagne-regles-1.jpg",
        "00-campagne-regles-2.jpg",
        "00-campagne-regles-3.jpg"
    ],
    "pages_intro": [
        "00-campagne-intro-1.jpg"
    ],
    "pages_vilains": [
        "00-vilains-1.jpg",
        "00-vilains-2.jpg"
    ],
    "expert": {
        "pv_persistants": true,
        "note": "Campagne experte : les PV restants sont reportés d'un scénario au suivant (livret p. 9), une défaite fait progresser le scénario perdu, et la victoire finale contre Kingpin exige de rejouer tant qu'il reste un environnement Completed à retourner."
    },
    "vilains": [
        {
            "id": "hammerhead",
            "nom": "Hammerhead",
            "ordre": 1
        },
        {
            "id": "bullseye",
            "nom": "Bullseye",
            "ordre": 2
        },
        {
            "id": "electro",
            "nom": "Electro",
            "ordre": 3
        },
        {
            "id": "purple_man",
            "nom": "Purple Man",
            "ordre": 4
        },
        {
            "id": "typhoid_mary",
            "nom": "Typhoid Mary",
            "ordre": 4
        }
    ],
    "scenarios": [
        {
            "id": "art_museum_heist",
            "manigance": true,
            "numero": 1,
            "nom": "Art Museum Heist",
            "nom_fr": "Le casse du musée",
            "resume": "L'alarme silencieuse du musée d'art vient de se déclencher ; les gardes ne répondent plus. Quelqu'un vole les œuvres au grand jour, comme s'il voulait être vu.",
            "enjeu": "Complété : chaque identité commence la partie suivante avec une carte de statut robuste. Échoué : chaque joueur commence étourdi ou désorienté (les deux en expert).",
            "pages": {
                "intro": [
                    "01-art_museum_heist-intro-1.jpg"
                ],
                "regles": [
                    "01-art_museum_heist-regles-1.jpg"
                ]
            },
            "environnement": "60205a,60205b",
            "victoire": []
        },
        {
            "id": "the_getaway",
            "manigance": true,
            "numero": 2,
            "nom": "The Getaway",
            "nom_fr": "La fuite",
            "resume": "Un coupé jaune file vers le tunnel avec l'argent de la banque. Chaque fin de round où la menace n'est pas retombée à zéro, la poursuite accélère.",
            "enjeu": "Complété : après les mulligans, chaque joueur peut chercher une amélioration dans son deck. Échoué : chaque joueur révèle un attachement du deck rencontre à la mise en place.",
            "pages": {
                "intro": [
                    "02-the_getaway-intro-1.jpg"
                ],
                "regles": [
                    "02-the_getaway-regles-1.jpg"
                ]
            },
            "environnement": "60206a,60206b",
            "victoire": []
        },
        {
            "id": "protection_racket",
            "manigance": true,
            "numero": 3,
            "nom": "Protection Racket",
            "nom_fr": "Le racket",
            "resume": "Des voyous cassent une boutique de quartier. Chaque héros protège son propre commerce : un complot principal par joueur, et l'ennemi ne pose sa menace que sur celui du joueur qu'il vise.",
            "enjeu": "Complété : après les mulligans, chaque joueur peut chercher un soutien dans son deck. Échoué : chaque joueur défausse 1 carte de sa main (2 en expert).",
            "pages": {
                "intro": [
                    "03-protection_racket-intro-1.jpg"
                ],
                "regles": [
                    "03-protection_racket-regles-1.jpg"
                ]
            },
            "environnement": "60207a,60207b",
            "victoire": []
        },
        {
            "id": "the_raft_breakout",
            "manigance": true,
            "numero": 4,
            "nom": "The Raft Breakout",
            "nom_fr": "L'évasion du Raft",
            "resume": "Un intrus a la clé maîtresse du Raft et libère les prisonniers un à un. Chaque sbire vaincu retire de la menace au complot.",
            "enjeu": "Complété : après les mulligans, chaque joueur peut chercher un allié dans son deck. Échoué : les prisonniers du Raft sont mêlés au deck rencontre.",
            "pages": {
                "intro": [
                    "04-the_raft_breakout-intro-1.jpg"
                ],
                "regles": [
                    "04-the_raft_breakout-regles-1.jpg"
                ]
            },
            "environnement": "60208a,60208b",
            "victoire": []
        },
        {
            "id": "stop_the_presses",
            "manigance": true,
            "numero": 5,
            "nom": "Stop the Presses!",
            "nom_fr": "Arrêtez les rotatives !",
            "resume": "Les bureaux du Daily Bugle sont saccagés, J. Jonah Jameson est ligoté dans son fauteuil. Chaque joueur protège un membre de la rédaction : s'il quitte le jeu, la partie est perdue.",
            "enjeu": "Complété : chaque joueur commence avec un soutien Daily Bugle en jeu. Échoué : chaque joueur reçoit 1 carte rencontre face cachée à la mise en place (2 en expert).",
            "pages": {
                "intro": [
                    "05-stop_the_presses-intro-1.jpg"
                ],
                "regles": [
                    "05-stop_the_presses-regles-1.jpg"
                ]
            },
            "environnement": "60209a,60209b",
            "victoire": []
        },
        {
            "id": "kingpin",
            "catalogue": "kingpin_fne",
            "numero": 6,
            "final": true,
            "nom": "Kingpin",
            "nom_fr": "Le Caïd",
            "resume": "La vague de crime avait un chef d'orchestre. Kingpin tire les ficelles depuis l'ombre : il faut d'abord regagner la confiance du public, sbire après sbire, avant de pouvoir l'affronter en face.",
            "enjeu": "La victoire gagne la campagne. En expert, s'il reste un environnement Complété, il faut en retourner un côté Échoué et rejouer.",
            "pages": {
                "intro": [
                    "06-kingpin-intro-1.jpg"
                ],
                "regles": [
                    "06-kingpin-regles-1.jpg"
                ],
                "epilogue": [
                    "06-kingpin-epilogue-1.jpg"
                ]
            },
            "victoire": [
                {
                    "cle": "Remaining hit points",
                    "parJoueur": true,
                    "type": "auto",
                    "format": "int",
                    "detection": "pv_restants",
                    "libelle": "Points de vie restants",
                    "aide": "La campagne s'achève : ce chiffre n'est là que pour le récit."
                }
            ]
        }
    ],
    "victoire_commune": [
        {
            "cle": "Completed Scenarios",
            "type": "auto",
            "format": "liste",
            "libelle": "Affaires résolues",
            "aide": "Relevé par le jeu : la manigance gagnée rejoint la liste des scénarios Complétés. Son environnement entrera en jeu côté Completed à chaque partie suivante."
        },
        {
            "cle": "Trust Established?",
            "type": "auto",
            "format": "int",
            "libelle": "Confiance établie (Typhoid Mary)",
            "aide": "Relevé par le jeu : Disturbed Psyche en jeu avec au moins 2 jetons menace à la victoire. Avec « Mary vaincue » non cochée, l'alliée Typhoid Mary / Bloody Mary entre en jeu sous votre contrôle aux parties suivantes."
        },
        {
            "cle": "Mary Defeated?",
            "type": "auto",
            "format": "int",
            "libelle": "Mary vaincue",
            "aide": "Relevé par le jeu : l'alliée Mary Walker dans la pile de victoire à la fin de la partie."
        },
        {
            "cle": "Allies removed from the campaign",
            "type": "auto",
            "format": "liste",
            "libelle": "Alliés et soutiens uniques retirés de la campagne",
            "aide": "Relevé par le jeu : chaque allié ou soutien unique retiré du jeu pendant la partie (Bullseye, Unerring Desire...) est retiré de votre deck pour le reste de la campagne."
        }
    ],
    "victoire_commune_expert": [
        {
            "cle": "Remaining hit points",
            "parJoueur": true,
            "type": "auto",
            "format": "int",
            "detection": "pv_restants",
            "libelle": "Points de vie restants",
            "aide": "Campagne experte : vos PV restants sont vos PV de départ au scénario suivant."
        }
    ]
}
```

### `src/cards/pack/fne/campaign.py`

```python
"""Campagne « Fear No Evil » (livret mc60 p. 8-9, 13-23) : mise en place et
releve du carnet.

Le fil : cinq affaires jouables dans l'ordre choisi par les joueurs (Art
Museum Heist, The Getaway, Protection Racket, The Raft Breakout, Stop the
Presses!), chacune contre un vilain UNDERLING ; avant chaque partie, deux
affaires non resolues PROGRESSENT (marques), trois marques = affaire echouee ;
quand les cinq sont Completed ou Failed, Kingpin. Chaque affaire a un
environnement recto-verso Completed / Failed (60205-60209) qui entre en jeu a
toutes les parties suivantes.

Cles du carnet (les chaines litterales que `tools/verifier_campagnes.py`
compare a `data/campagnes/fne.json`) :
  - "Completed Scenarios" / "Failed Scenarios" : listes de manigances ;
  - "Progress: <manigance>" : 0..3 (ecrit par l'ecran des campagnes) ;
  - "Villain: <manigance>" : le vilain enregistre pour l'affaire ;
  - "Trust Established?" / "Mary Defeated?" : "1" ;
  - "Allies removed from the campaign" : titres (allies ET soutiens uniques) ;
  - "Remaining hit points" par joueur (campagne experte, cle du moteur).
La progression et l'affectation des vilains sont l'affaire de l'ecran
(public/js/campagne/app.js, vue « ordre libre ») : le moteur ne fait que lire.
"""
from cards.pack import *
from cards.pack.mts.campaign import WriteCampaignLogAtGameOver

MANIGANCES = ("art_museum_heist", "the_getaway", "protection_racket", "the_raft_breakout", "stop_the_presses")
ENVIRONNEMENTS = {
    "art_museum_heist":  ("60205a", "60205b"),
    "the_getaway":       ("60206a", "60206b"),
    "protection_racket": ("60207a", "60207b"),
    "the_raft_breakout": ("60208a", "60208b"),
    "stop_the_presses":  ("60209a", "60209b"),
}
SOUTIENS_DAILY_BUGLE = ("60153", "60154", "60155", "60156")
PRISONNIERS_DU_RAFT = ("60144", "60145", "60146", "60147", "60148", "60149")
MARY = "60210a,60210b"
CLE_COMPLETED = "Completed Scenarios"
CLE_FAILED = "Failed Scenarios"
CLE_TRUST = "Trust Established?"
CLE_MARY = "Mary Defeated?"
CLE_RETIREES = "Allies removed from the campaign"


def Completed(effect: 'Effect') -> List[str]:
    return CampaignLog.GetListInternal(CLE_COMPLETED, effect)


def Failed(effect: 'Effect') -> List[str]:
    return CampaignLog.GetListInternal(CLE_FAILED, effect)


def Progression(manigance: str, effect: 'Effect') -> int:
    return CampaignLog.GetIntInternal(f"Progress: {manigance}", effect)


def Retirees(effect: 'Effect') -> List[str]:
    return CampaignLog.GetListInternal(CLE_RETIREES, effect)


def EnvironnementsEnJeu(effect: 'Effect') -> List['CardFace']:
    ids = {a for a, b in ENVIRONNEMENTS.values()} | {b for a, b in ENVIRONNEMENTS.values()}
    faces = []
    for card in effect.world.object_manager.card_dict.values():
        face = card.face
        if face is not None and face.IsInPlay() and face.paper.card_id in ids:
            faces.append(face)
    return faces


def NombreDeCompleted(effect: 'Effect') -> int:
    return len([f for f in EnvironnementsEnJeu(effect) if f.paper.card_id.endswith('a')])


def MettreLesEnvironnements(conditions=[]) -> 'Ability':
    """Etape 12 de la mise en place de campagne : l'environnement de chaque
    affaire Completed face Completed, de chaque affaire Failed face Failed."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        premier = Worlds.GetFirstPlayer(effect)
        deja = {f.paper.card_id for f in EnvironnementsEnJeu(effect)}
        for manigance, (a, b) in ENVIRONNEMENTS.items():
            if manigance in Completed(effect):
                ids = f"{a},{b}"
            elif manigance in Failed(effect):
                ids = f"{b},{a}"
            else:
                continue
            if ids.split(',')[0] in deja:
                continue
            card = CardFactory.GenerateCard(ids, None, effect.world)
            card.face.PutIntoPlay(premier, effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=conditions)


def RetirerLesCartesRetirees(conditions=[]) -> 'Ability':
    """Etape 8 : chaque joueur retire de son deck les cartes dont le titre est
    au carnet (allies et soutiens uniques retires du jeu). Le complement de
    deck en dessous du minimum n'est pas fait ici : c'est un choix de
    construction, hors mise en place automatique."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        titres = set(Retirees(effect))
        if not titres:
            return
        for player in Worlds.GetPlayers(effect):
            zones = list(player.player_deck.Get(True)) + list(player.hand_cards.Get(True)) + list(player.discard_pile.Get(True))
            a_retirer = [f for f in zones if f.paper.name.lstrip('* ') in titres or f.paper.name in titres]
            if a_retirer:
                Faces.RemoveAllFromGame(a_retirer, effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=conditions)


def MaryWalker(conditions=[]) -> 'Ability':
    """Etape 13 : « Trust Established? » coche et « Mary Defeated? » non ->
    l'alliee Typhoid Mary (210A) entre en jeu sous le controle d'un joueur."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        if not CampaignLog.GetStrInternal(CLE_TRUST, effect) or CampaignLog.GetStrInternal(CLE_MARY, effect):
            return
        premier = Worlds.GetFirstPlayer(effect)
        card = CardFactory.GenerateCard(MARY, None, effect.world)
        card.face.PutIntoPlay(premier, effect, under_control=True)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=conditions)


def MarquesDeLAffaire(manigance: str, conditions=[]) -> 'Ability':
    """Les encarts CAMPAIGN INSTRUCTIONS / SETUP du livret (p. 13-21), selon
    le nombre de marques de progression de l'affaire jouee."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        n = Progression(manigance, effect)
        if n <= 0:
            return
        expert = Worlds.IsExpert(effect)
        premier = Worlds.GetFirstPlayer(effect)
        if manigance in ("art_museum_heist", "protection_racket"):
            # « Place 1 threat (2 in expert) on the/each main scheme for each check mark »
            par_marque = 2 if expert else 1
            for scheme in Worlds.GetAllMainSchemes(effect):
                scheme.PlaceThreatOnSchemes([scheme], par_marque * n, effect)
        elif manigance == "the_getaway":
            camion = Worlds.FindCardOnField(effect, name="Jackknifed Tanker Truck", card_type=EncounterSideScheme)
            if camion is None:
                camion = Find.FindAndReveal(effect, premier, name="Jackknifed Tanker Truck", card_type=EncounterSideScheme)
            if n >= 2 and camion is not None:
                camion.PlaceThreatOnSchemes([camion], 2 if expert else 1, effect)
        elif manigance == "the_raft_breakout":
            prisonniers = Worlds.FindCardsOnField(effect, trait="PRISONER", card_type=Minion)
            if prisonniers:
                Faces.GiveStatus(prisonniers, "Tough", effect)
                if n >= 2:
                    Faces.GiveFacedownBoostCards(prisonniers, 1, effect)
        elif manigance == "stop_the_presses":
            for soutien in Worlds.FindCardsOnField(effect, trait="DAILY BUGLE", card_type=Support):
                Faces.RemoveCountersOn([soutien], n, 'stamina', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=conditions)


def MarquesKingpin(conditions=[]) -> 'Ability':
    """Kingpin, SETUP (p. 23) : 3 environnements Completed -> chaque sbire en
    jeu robuste ; 4 -> trouver et reveler James Wesley."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        n = NombreDeCompleted(effect)
        if n >= 3:
            sbires = Worlds.GetOnFieldMinions(effect)
            if sbires:
                Faces.GiveStatus(sbires, "Tough", effect)
        if n >= 4:
            Find.FindAndReveal(effect, Worlds.GetFirstPlayer(effect), name="James Wesley", card_type=Attachment)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=conditions)


def _partie_gagnee(message: 'Message.WhenGameOver') -> bool:
    """Le resultat vient du MESSAGE, pas du monde.

    ⚠ `GameOver.SetGameOver` envoie `WhenGameOver` PUIS pose `players_won` sur
    le monde : pendant le message, `world.game_over` dit encore « perdue ».
    La version precedente lisait le monde, donc « Completed Scenarios » n'etait
    JAMAIS ecrit, meme sur une victoire. Personne ne l'avait vu parce que rien
    ne jouait la fin d'une partie (trouve le 19/09/2026 par
    `tools/test_campagnes.py`).
    """
    return bool(getattr(message, "players_won", False))


def CollectFNE(manigance: 'str|None', effect: 'Effect', message: 'Message.WhenGameOver') -> dict:
    """Le carnet sortant, releve a la fin de la partie (VICTORY du livret) :
    l'affaire gagnee rejoint « Completed Scenarios » ; « Trust Established? »
    si Disturbed Psyche a au moins 2 jetons menace ; « Mary Defeated? » si
    l'alliee est dans la pile de victoire ; les allies et soutiens UNIQUES
    retires du jeu s'ajoutent a « Allies removed from the campaign »."""
    updates = {}
    gagnee = _partie_gagnee(message)
    if manigance and gagnee:
        faits = Completed(effect)
        if manigance not in faits:
            updates[CLE_COMPLETED] = ";".join(faits + [manigance])
    if gagnee:
        psyche = Worlds.FindCardOnField(effect, name="Disturbed Psyche", card_type=Environment)
        if psyche is not None and psyche.GetTokens('threat') >= 2:
            updates[CLE_TRUST] = "1"
    for card in effect.world.object_manager.card_dict.values():
        face = card.face
        if face is not None and face.paper.card_id in ("60210a", "60210b") and card.area.flags.is_victory_display:
            updates[CLE_MARY] = "1"
    retirees = list(Retirees(effect))
    for face in effect.world.area_removed.Get(True):
        # ⚠ `paper.name` n'a PLUS l'etoile a l'execution (paper.py:45 la
        # retire et pose `is_unique`) : tester le drapeau, pas le prefixe
        # (cas « Carnet sortant » rouge le 18/09/2026, Black Cat non relevee).
        if (Ally.IsType(face) or Support.IsType(face)) and face.paper.is_unique:
            proprietaire = face.GetOwner()
            if Player.IsType(proprietaire):
                titre = face.paper.name.lstrip('* ')
                if titre not in retirees:
                    retirees.append(titre)
    if retirees and retirees != list(Retirees(effect)):
        updates[CLE_RETIREES] = ";".join(retirees)
    return updates


def CapacitesDeCampagne(manigance: str, garde=None) -> List['Ability']:
    """A poser sur la face 1A de chaque manigance interchangeable.

    `garde(effect, message) -> bool` : condition supplementaire sur les
    capacites de mise en place. Protection Racket a UN complot principal PAR
    JOUEUR (cinq copies de 60134a-60138a) : sans garde, chaque copie
    remettrait les environnements, Mary Walker et les marques de l'affaire
    (Mary entrerait N fois). La garde ne laisse parler que le premier complot
    en jeu ; le carnet de fin de partie, lui, est idempotent."""
    conditions = [garde] if garde else []
    return [
        MettreLesEnvironnements(conditions),
        RetirerLesCartesRetirees(conditions),
        MarquesDeLAffaire(manigance, conditions),
        MaryWalker(conditions),
        AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP(),
        WriteCampaignLogAtGameOver(lambda effect, message: CollectFNE(manigance, effect, message)),
    ]


def CapacitesDeCampagneKingpin() -> List['Ability']:
    """A poser sur The King's Gambit 1A (60161a)."""
    return [
        MettreLesEnvironnements(),
        RetirerLesCartesRetirees(),
        MarquesKingpin(),
        MaryWalker(),
        AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP(),
        WriteCampaignLogAtGameOver(lambda effect, message: CollectFNE(None, effect, message)),
    ]
```

## 5. Les arbitrages déjà tranchés

Extraits du journal du portage (18/09/2026) : questions posées à l'auteur, hypothèses retenues, limites connues. Ce qui y est décidé n'est pas une erreur à signaler.

### Bloc 1 — Hammerhead, Art Museum Heist, Cops, The Owl (18/09/2026)

#### 6. Gates statiques du bloc (18/09/2026)

- `test_cards` : 5598 ok / 0 err ; `verifier_api_cartes` : 0 fichier fne en faute ;
  `audit_cartes` : aucune suspicion sur les 27 cartes ; `verifier_coherence_cartes`
  : rien sur le bloc ; `verifier_appels_modules fne` : OK ; `verifier_noms_modules fne` : OK.
- Harnais : **57/57 cas `[fne]`** (PARALLELES=4, port 40000).
- Substitution : 27/27 modules prouvés (5 passes `substituer_pack.py`, préfixes 6008/6009/6012/6018/6019, ports 31000-35800) ; empreinte md5 du pack identique avant/après (`6dd56080…`). Deux cas restent verts sans module, tous deux des contre-cas d'ABSENCE d'effet : `60093` « non étourdi, seul le boost Villainous » et `60193` « la riposte de Black Panther touche The Owl » (pas ranged).
- Autoplay : 8 parties Spider-Man vs `art_museum_heist_hammerhead` (profil équilibré, graines 1-8) : 0 V / 8 D, 0 bloquée, 5,5 rounds, **0 traceback** (grep exhaustif des 8 journaux) ; témoin `rhino` même fournée : 0 V / 8 D, 0 bloquée, 7,5 rounds, 0 traceback. Première fournée : 12 `KeyError: None` sur Tug of War (voir §4), corrigé puis rejoué.
- Passe complète des decks (fichiers partagés touchés) : 135/136 (14:37 → 15:01). L'échec, `superior_iron_man`, est étranger au pack : `si012.py` Spectacular Save appelait `GetControlByPlayer()` sur l'ennemi qui subit les dégâts (assert `isinstance(owner, Player)`) dès que la carte était en main lors d'une attaque du héros. Corrigé à la source (`GetControlByOrOwner` + `Player.IsType`), deck remonté sur `.game-src-b2` : OK (identité si001a, main 6, deck 9). → 136/136.
- Batterie complète `test_capacites` : **1987/1991** (15:01 → 16:18, PARALLELES=4, port 40000). Les 4 rouges sont les rouges PRÉEXISTANTS de `.planning/todos/2026-08-31-cas-rouges-sg-ss.md` (`sg006`, `sg007`, `sg009`, `sg013`) ; rejoués un par un : toujours rouges ; `sg009` rejoué avec `obligation.py` et `card_face.py` remis à l'état git (stash) : toujours rouge → aucune régression du bloc 1. `launch.json` principal vérifié : `127.0.0.1:2345`.
- Plateau : `ui-app/src/board/fne-oeuvre-volee.test.ts` 3/3.


#### 7. Ce que ces gates ne voient pas (à dire en fin de bloc)

- Aucune partie humaine jouée dans le navigateur sur ce scénario.
- L'overkill de Head First! (voir gabarit 60096).
- `PeutCouvrirLeCout` ignore les générateurs de ressources EN JEU (gabarit 60127).
- La modale de choix du vilain n'existe pas encore : avec un seul underling
  porté, la tuile « Art Museum Heist (Hammerhead) » suffit ; la modale arrive
  avec Bullseye (bloc 2).


### Bloc 3A — The Getaway, The Raft Breakout, Stop the Presses! (18/09/2026, agent A)

#### 6. Questions pour l'utilisateur (hypothèse littérale implémentée)

Aucune ambiguïté bloquante. Deux hypothèses littérales implémentées, à confirmer si l'on veut :

1. **60131 Jackknifed Tanker Truck + Out Front** (scan `scratchpad/scans/60131.jpg`, `60129a.jpg`) : quand le vilain « cannot be dealt damage » et qu'Out Front dit « when the villain **would** be dealt damage, remove that amount of threat instead », j'ai retenu que « cannot » prime : aucun dégât ET aucune menace retirée (c'est ce que fait le moteur). Options : A) garder (recommandé, c'est la règle « cannot » du RRG) ; B) la menace est quand même retirée ; C) Autre (précise).
2. **60152 Daily Bugle « (Any player can do this.) »** et **60156 Robbie « After a player is dealt … »** : implémentés pour tout joueur, mais seule une partie à UN joueur a été montée au harnais. Options : A) suffisant pour l'instant (recommandé) ; B) monter un cas à deux joueurs (`heros2`) avant livraison ; C) Autre (précise).


#### 7. Ce que ces gates ne voient pas

- Aucune partie humaine dans le navigateur sur ces trois scénarios.
- Preuve par substitution : passe finale du coordinateur (`substituer_pack.py`), non lancée ici (interdit du brief §3.4). Contre-cas d'ABSENCE d'effet attendus verts sous substitution : 60128b « sans menace », 60143 × 2, 60147 × 2, 60145 « aucun allié », 60151b « défendue », 60154 « Betty inclinée », 60157 « témoin Ready », 60130 « 1 compteur ».
- Parties à deux joueurs (Daily Bugle « any player », Robbie « a player », Raft 1A « each player », Alongside « each player ») : non montées.
- `PeutCouvrirLeCout` (Burning Rubber) ignore les générateurs de ressources en jeu (écart hérité du bloc 1).


### Bloc 3B — Drive, Disasters, Tombstone, Tracksuit Mafia (18/09/2026, agent B)

#### 6. Questions pour l'utilisateur (hypothèse littérale implémentée)

1. **60180 Collapsing Bridge** (scan `scratchpad/scans/60180.jpg`) : quand la DERNIÈRE menace est retirée du pont, que se passe-t-il ?
   A) Le pont est vaincu, la Réponse Forcée ne résout pas (implémenté : un complot annexe est vaincu dès que sa dernière menace part, RRG « Defeated » ; sinon il ne peut jamais être vaincu par un contre).
   B) Le pont reçoit 1 menace et reste en jeu (le moteur faisait cela avant ma garde : il fallait retirer TOUTE la menace puis… c'était impossible).
   C) Autre (précise).
2. **Teamwork (60200-60203)** : le moteur applique par défaut la règle pré-1.6 (`v16_teamwork = False`) : quand Ivan entre avec Bro déjà en jeu, LES DEUX s'activent (4 dégâts mesurés). La règle RRG 1.6 n'active que le nouveau venu. Quelle règle veux-tu pour tout le jeu ? (réglage moteur, hors de mon périmètre)
   A) Garder la règle par défaut du moteur (tous s'activent).
   B) Passer `v16_teamwork = True` (seul l'entrant s'active).
   C) Autre (précise).


#### 7. Ce que ces gates ne voient pas

- `src/cards/pack/fne/tombstone/__init__.py` (helper `PeutSAccrocherAUnSbire`, passe 2 : `attach_selector` + import local de `GameRule`), `tombstone/60197.py`, `tombstone/60199.py`, `disasters/60180.py`.
- `tools/test_capacites.py` : bloc 3B (66 cas) et section `# ---- pack fne (bloc 3B)`, uniquement par le générateur sous `flock`.
- Générateur de cas : `gen_cas_fne_b.py` (copié dans `.planning/todos/generateurs-fne/`).
- Rien sous `src/game/`, ni `data/`, ni `fne/__init__.py`, ni git.

Ce que ces gates ne voient pas : aucune partie humaine dans le navigateur ; Traffic Jam et Carjacking jamais révélés en autoplay (8 parties courtes) ; le plateau n'a pas été relancé sur un état contenant un véhicule sur l'identité (couvert par analogie avec les œuvres d'Art Museum Heist, même zone).


### Bloc 3P — Protection Racket (18/09/2026, coordinateur)

#### 6. Questions pour l'utilisateur
Aucune : les règles du livret p. 13 et l'article FFG sur les complots par joueur ont été relus (voir la discussion du 18/09/2026).


#### 7. Ce que ces gates ne voient pas
Aucune partie à DEUX joueurs sur Protection Racket hors les cas de campagne (`heros2`) ; aucune partie humaine.


### Bloc 4 — Kingpin (18/09/2026, agent C)

#### 6. Questions pour l'utilisateur (hypothèse littérale implémentée)

**Q1, 60173 Kingpin's Influence** (scan `scratchpad/scans/60173.jpg`) : « places 3 threat on
their nemesis side scheme. If it is not in play, they find it and reveal it. » Quand le
complot nemesis n'est PAS en jeu :
- A) (implémenté, lecture littérale) on le trouve et on le révèle, avec sa menace de
  départ seulement (Highway Robbery : 3) ;
- B) on le révèle PUIS on y pose les 3 menaces (3 + 3 = 6) ;
- C) Autre (précise).

**Q2, 60163b Public Support HIGH** (scan `60163b.jpg`) : « When an enemy would be given a
facedown boost card, remove 1[per_hero] support counters from here instead. » Tant que le
moteur n'a pas la fenêtre D2, l'Interrupt ne remplace que la carte boost de l'ACTIVATION
(une par activation), pas celles données par James Wesley ou Bag of Tricks :
- A) acceptable en attendant D2 (recommandé) ;
- B) bloquer la carte jusqu'à D2 ;
- C) Autre (précise).

**Q3, 60169 Black Cat** (scan `60169.jpg`) : une fois alliée, la FAQ du livret dit qu'elle
GARDE Villainous (une carte boost à chaque attaque de base, comme un héros villainous).
Le moteur ne le sait pas pour un allié :
- A) écart accepté, elle attaque sans carte boost (implémenté) ;
- B) demander au coordinateur d'étendre `HasVillainous` aux alliés (moteur) ;
- C) Autre (précise).


#### 7. Ce que ces gates ne voient pas

- Aucune partie humaine jouée dans le navigateur sur ce scénario ; le rendu du
  retournement de Public Support et de Black Cat convertie n'a pas de cas plateau propre.
- Bear Hug contre un ÉVÉNEMENT d'attaque/contre du héros (non exercé par le harnais).
- Les faces B en autoplay n'atteignent jamais le stade 2 (parties perdues au round 3).
- Preuve par substitution : passe finale du coordinateur (`substituer_pack.py` non lancé,
  brief §3.4). Empreinte md5 des 23 fichiers du set au moment du rapport :
  `md5sum src/cards/pack/fne/kingpin/*.py | md5sum` = `3cd6f556e7c3fe29e1572cc37acc5302`.


### Bloc 5 — Campagne (18/09/2026, coordinateur)

#### 1. Inventaire → card_id (6 cartes, 12 faces)

60205a,60205b Art Museum Heist ; 60206a,60206b The Getaway ; 60207a,60207b
Protection Racket ; 60208a,60208b The Raft Breakout ; 60209a,60209b Stop the
Presses! (environnements Completed / Failed) ; 60210a,60210b * Typhoid Mary /
* Bloody Mary (alliée de campagne). Set « Fear No Evil Campaign ».


#### 2. Fichiers écrits

- `src/cards/pack/fne/campaign.py` : clés du carnet (`Completed Scenarios`,
  `Failed Scenarios`, `Progress: <affaire>`, `Villain: <affaire>`, `Trust
  Established?`, `Mary Defeated?`, `Allies removed from the campaign`, PV
  restants par joueur = clé moteur) ; `MettreLesEnvironnements`,
  `RetirerLesCartesRetirees`, `MaryWalker`, `MarquesDeLAffaire(manigance)`,
  `MarquesKingpin`, `CollectFNE`, `CapacitesDeCampagne(manigance, garde=None)`,
  `CapacitesDeCampagneKingpin()` ; branchées sur 60121a, 60128a, 60134a (garde
  `_premier_complot`), 60142a, 60151a, 60161a.
- `src/cards/pack/fne/fear_no_evil_campaign/` (`ChercherEnMain`,
  `DefausserDeLaMain`, `RechuteVers` ; 12 scripts).
- `src/cards/pack/mts/campaign.py` : estampille nettoyée (`[^a-z0-9_]`), sans
  quoi « Stop the Presses! » ne correspondait à aucun scénario.
- `data/campagnes/fne.json` (`ordre_libre`, vilains, 5 affaires + Kingpin
  `catalogue: kingpin_fne`, victoire commune) ; `verifier_campagnes.py` OK.
- Lanceur : `public/js/campagne/ordre-libre.js` (module pur : tirage de
  progression, états, vilains, catalogue, défaite) + `tools/tests-lanceur/ordre-libre.test.mjs`
  (12/12) ; `public/js/campagne/app.js` (`vueCampagneLibre`, `lancerScenario`
  avec catalogue et vilain, `estTerminee`) ; CSS `campagne.css` (carnet) ;
  `dico-en.js` ; test d'écran `ui-check/tests/campagne-ordre-libre.spec.ts`
  (4/4 sur un moteur port 40000).
- Harnais : 27 cas `[fne5]` (`.planning/todos/generateurs-fne/gen_cas_fne_5.py`) + vérificateurs
  `fne5_trait`, `fne5_collect` ; clé de cas `carnet` (→ `campaign_log` + règle `mode_campaign`).


#### 4. Ce que le harnais a trouvé
`KeyError: 'Class'` sur les environnements de campagne (desc sans `Class`) ;
`WhenCampaignSetup` part après le retournement des complots (garde par CARTE) ;
Hinder du camion ; statuts à lire sur l'alter-ego ; `CollectFNE` testait le
préfixe « * » du nom alors que `paper.py` le retire au chargement (`is_unique`) :
les alliés retirés n'étaient jamais relevés. **BILAN : 27/27 cas passes**
(`[fne5]`, ports 41000 puis 42200 pour les 4 derniers).


#### 5. Gabarits PROCESSUS-CARTE (un par carte)

#### 60205a,60205b : Art Museum Heist (Completed / Failed)
- [x] Étape 2 : `MettreLesEnvironnements` (WhenCampaignSetup, face selon « Completed Scenarios » / « Failed Scenarios »), Setup de la face : chaque identité reçoit un statut robuste (`GiveStatus Tough`, `AfterGameSetup`) ; côté Failed : chaque joueur choisit étourdi ou désorienté (`ChooseAbilities`), les deux en expert (`Worlds.IsExpert`).
- [x] Étape 5 : « each identity » → le héros ET l'alter-ego portent le statut (mesuré sur 01001b, la partie commence en alter-ego) ; « choose : stunned or confused » → choix, « both in expert ».
- [x] Étape 6 : environnement à deux faces (`"60205a,60205b"`), traits COMPLETED / FAILED, set « Fear No Evil Campaign », sans `Class`.
- [x] Étape 7 : `60205a Art Museum Heist (Completed) [fne5] — carnet : affaire completee -> l'environnement entre en jeu, chaque identite est robuste`, `60205b Art Museum Heist (Failed) [fne5] — carnet : affaire echouee -> face Failed, le joueur choisit etourdi (premiere option)`, `60205b Art Museum Heist (Failed) [fne5] (expert) — etourdi ET desoriente`, `Marques de progression [fne5] — 2 marques sur Art Museum Heist : +2 menaces sur le complot a la mise en place (1 + 2)`, `Marques de progression [fne5] (expert) — 2 marques : +4 (1 + 4)`. Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : couvert par l'autoplay des blocs 2 à 4 (le mode campagne s'y ajoute sans changer le déroulé) et par les 4 tests d'écran `ui-check/tests/campagne-ordre-libre.spec.ts` (tirage, choix, défaite, Kingpin).
- [x] Étape 8 bis : NON (environnement standard, sans compteur).
- Carte terminée : OUI


#### 60206a,60206b : The Getaway (Completed / Failed)
- [x] Étape 2 : `MettreLesEnvironnements` (WhenCampaignSetup, face selon « Completed Scenarios » / « Failed Scenarios »), Setup de la face : après les mulligans, chaque joueur peut chercher une amélioration dans son deck (`WhenCampaignSetupAfterMulligans`, `ChercherEnMain`) ; côté Failed : chaque joueur révèle un attachement du deck rencontre (`Find.FindAndReveal(Attachment)`).
- [x] Étape 5 : « after mulligans » → message dédié `WhenCampaignSetupAfterMulligans` (pas au Setup) ; « **may** search » → `forced=False`.
- [x] Étape 6 : environnement à deux faces (`"60206a,60206b"`), traits COMPLETED / FAILED, set « Fear No Evil Campaign », sans `Class`.
- [x] Étape 7 : `60206a The Getaway (Completed) [fne5] — en jeu ; apres les mulligans, chercher une amelioration (may) : la main compte 7 cartes`, `60206b The Getaway (Failed) [fne5] — en jeu ; chaque joueur revele un attachement du deck rencontre a la mise en place (1 oeuvre au Setup + 1 revelee + 1 par l'Art Thief qu'elle appelle = 3 attachements)`. Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : couvert par l'autoplay des blocs 2 à 4 (le mode campagne s'y ajoute sans changer le déroulé) et par les 4 tests d'écran `ui-check/tests/campagne-ordre-libre.spec.ts` (tirage, choix, défaite, Kingpin).
- [x] Étape 8 bis : NON (environnement standard, sans compteur).
- Carte terminée : OUI


#### 60207a,60207b : Protection Racket (Completed / Failed)
- [x] Étape 2 : `MettreLesEnvironnements` (WhenCampaignSetup, face selon « Completed Scenarios » / « Failed Scenarios »), Setup de la face : après les mulligans, chaque joueur peut chercher un soutien ; côté Failed : chaque joueur défausse 1 carte de sa main (2 en expert, `DefausserDeLaMain`).
- [x] Étape 5 : « discard 1 card (2 in expert) » → après la pioche de départ, main 6 → 5 ; en expert 6 → 4.
- [x] Étape 6 : environnement à deux faces (`"60207a,60207b"`), traits COMPLETED / FAILED, set « Fear No Evil Campaign », sans `Class`.
- [x] Étape 7 : `60207a Protection Racket (Completed) [fne5] — en jeu ; apres les mulligans, chercher un soutien (may) : Aunt May arrive en main`, `60207b Protection Racket (Failed) [fne5] — en jeu ; chaque joueur defausse 1 carte de sa main (6 -> 5)`. Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : couvert par l'autoplay des blocs 2 à 4 (le mode campagne s'y ajoute sans changer le déroulé) et par les 4 tests d'écran `ui-check/tests/campagne-ordre-libre.spec.ts` (tirage, choix, défaite, Kingpin).
- [x] Étape 8 bis : NON (environnement standard, sans compteur).
- Carte terminée : OUI


#### 60208a,60208b : The Raft Breakout (Completed / Failed)
- [x] Étape 2 : `MettreLesEnvironnements` (WhenCampaignSetup, face selon « Completed Scenarios » / « Failed Scenarios »), Setup de la face : après les mulligans, chaque joueur peut chercher un allié ; côté Failed : les six prisonniers du Raft sont mêlés au deck rencontre (`GenerateCard` + `ShuffleAllTo('EncounterDeck')`).
- [x] Étape 5 : « shuffle the PRISONER minions into the encounter deck » → les six, même hors du set de rencontre du scénario (générés).
- [x] Étape 6 : environnement à deux faces (`"60208a,60208b"`), traits COMPLETED / FAILED, set « Fear No Evil Campaign », sans `Class`.
- [x] Étape 7 : `60208a The Raft Breakout (Completed) [fne5] — en jeu ; apres les mulligans, chercher un allie (may) : Black Cat arrive en main`, `60208b The Raft Breakout (Failed) [fne5] — en jeu ; les six prisonniers du Raft sont meles au deck rencontre`. Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : couvert par l'autoplay des blocs 2 à 4 (le mode campagne s'y ajoute sans changer le déroulé) et par les 4 tests d'écran `ui-check/tests/campagne-ordre-libre.spec.ts` (tirage, choix, défaite, Kingpin).
- [x] Étape 8 bis : NON (environnement standard, sans compteur).
- Carte terminée : OUI


#### 60209a,60209b : Stop the Presses! (Completed / Failed)
- [x] Étape 2 : `MettreLesEnvironnements` (WhenCampaignSetup, face selon « Completed Scenarios » / « Failed Scenarios »), Setup de la face : chaque joueur met un soutien DAILY BUGLE en jeu sous son contrôle (`PutIntoPlay(under_control)`, moins les retirés) ; côté Failed : chaque joueur reçoit 1 carte rencontre face cachée (2 en expert, `DealEncounterCards`).
- [x] Étape 5 : « a DAILY BUGLE support » → parmi les quatre du set, moins ceux retirés de la campagne ; « dealt 1 facedown encounter card (2 in expert) ».
- [x] Étape 6 : environnement à deux faces (`"60209a,60209b"`), traits COMPLETED / FAILED, set « Fear No Evil Campaign », sans `Class`.
- [x] Étape 7 : `60209a Stop the Presses! (Completed) [fne5] — en jeu ; chaque joueur met un soutien DAILY BUGLE en jeu sous son controle`, `60209b Stop the Presses! (Failed) [fne5] — en jeu ; 1 carte rencontre distribuee face cachee`. Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : couvert par l'autoplay des blocs 2 à 4 (le mode campagne s'y ajoute sans changer le déroulé) et par les 4 tests d'écran `ui-check/tests/campagne-ordre-libre.spec.ts` (tirage, choix, défaite, Kingpin).
- [x] Étape 8 bis : NON (environnement standard, sans compteur).
- Carte terminée : OUI


#### 60210a,60210b : * Typhoid Mary / * Bloody Mary (alliée de campagne)
- [x] Étape 2 : `MaryWalker` (WhenCampaignSetup : « Trust Established? » coché et « Mary Defeated? » non → `PutIntoPlay(under_control=True)`), alliée à deux faces (`RechuteVers(card_type)` : retour côté Bloody Mary / Typhoid Mary), `CollectFNE` coche « Mary Defeated? » quand elle est dans la pile de victoire.
- [x] Étape 5 : « if Trust Established is checked **and** Mary Defeated is not » → double condition ; « put into play under **any** player's control » → premier joueur ; « Mary Defeated? » → pile de victoire à la fin de la partie.
- [x] Étape 6 : alliée unique, deux faces `"60210a,60210b"`, set « Fear No Evil Campaign ».
- [x] Étape 7 : `60210a Typhoid Mary (alliee) [fne5] — carnet : Trust Established sans Mary Defeated -> l'alliee entre en jeu sous ton controle`, `60210a Typhoid Mary (alliee) [fne5] — contre-cas : Mary Defeated coche -> pas d'alliee`, `60210a Typhoid Mary (alliee) [fne5] — apres que tu reveles un sbire : soignee et retournee (Bloody Mary)`, `Carnet sortant [fne5] — victoire avec Disturbed Psyche a 2 jetons et Black Cat retiree du jeu : Completed + Trust Established? + Allies removed` (a trouve un vrai defaut : `paper.name` n'a plus l'etoile a l'execution, `is_unique` a la place ; sans ce cas aucun allie retire n'aurait jamais ete inscrit au carnet), `Cartes retirees de la campagne [fne5] — carnet : Black Cat retiree -> hors du deck de Spider-Man (retiree du jeu)`, `Environnements multiples [fne5] — deux affaires completees et une echouee : trois environnements en jeu sur la bonne face`. Subst : passe finale.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : couvert par l'autoplay des blocs 2 à 4 (le mode campagne s'y ajoute sans changer le déroulé) et par les 4 tests d'écran `ui-check/tests/campagne-ordre-libre.spec.ts` (tirage, choix, défaite, Kingpin).
- [x] Étape 8 bis : NON (alliée standard).
- Carte terminée : OUI

#### Capacités de campagne des manigances (60121a, 60128a, 60134a, 60142a, 60151a, 60161a)
- [x] Étape 7 : `The Getaway (campagne) [fne5] — carnet : Art Museum Heist completee -> 60205a entre en jeu sur The Getaway aussi`, `The Getaway (campagne) [fne5] — 2 marques : Jackknifed Tanker Truck est revele avec 1 menace de plus (2 + Hinder 1 + 1 marque = 4)`, `The Raft Breakout (campagne) [fne5] — 2 marques : chaque prisonnier revele au Setup est robuste et recoit 1 carte boost`, `Stop the Presses! (campagne) [fne5] — 1 marque : le soutien DAILY BUGLE du joueur perd 1 compteur stamina (3 -> 2)`, `Protection Racket (campagne, 2 joueurs) [fne5] — deux complots 1A, mais UN SEUL environnement 60205a entre en jeu`, `Protection Racket (campagne) [fne5] — 1 marque : 1 menace de plus sur le complot du joueur`, `Kingpin (campagne) [fne5] — 3 affaires completees : les trois environnements en jeu, chaque sbire en jeu robuste`, `Kingpin (campagne) [fne5] — 4 affaires completees : James Wesley est trouve et revele (attache a Kingpin)`, plus les cas Art Museum Heist (marques 1 menace / 2 en expert, cartes retirées, PV persistants).
- Carte terminée : OUI (capacités inertes hors campagne : `Worlds.IsCampaign`).


#### 6. Décisions et questions
- Ordre libre : tirage fait par l'écran une fois par partie (`campagne.tirage`), défaite déclarée par le joueur (le plateau n'ouvre pas de panneau sur une défaite standard), en expert l'affaire progresse ; Kingpin en expert retourne un environnement Completed ou perd la campagne. Vilain : ordre recommandé du livret au premier parcours, imposé une fois inscrit.
- Aucune question ouverte.


#### 7. Ce que ces gates ne voient pas
Aucune campagne jouée de bout en bout à la main ; le panneau de récompenses du plateau relit l'estampille (nettoyée) mais n'a pas été rejoué sur les six manigances.

### Revérification de Daredevil et données relues sur scan (11/10/2026)

Décisions prises avec l'auteur du projet, carte par carte, scan à l'appui :

- `60001a` Superhuman Senses : la carte du dessus du deck Sens se joue « comme en main », sans bouton d'Action dédié ni limite par tour (une Action n'a pas de limite sans « once per »). Gardé tel quel.
- `60002` à `60006` : les cinq Interruptions/Réponses des Sens sont facultatives et le moteur le demande au joueur (Passer offert), mesuré par 9 cas acceptation/refus.
- `60009` Deposition : « You may choose » → le choix d'une amélioration Sens est facultatif (0 ou 1).
- `60012` Focus the Senses : la première moitié du When Defeated (déplacer des améliorations Sens en jeu vers d'autres cartes où elles peuvent s'attacher) manquait ; ajoutée, facultative, restrictions d'attache respectées (`60004`/`60005` ennemi, `60006` manigance, `60002`/`60003` les deux).
- `60018` The Man Without Fear et `60032` Sensory Overload : « deal 1 damage to Daredevil » / « take 1 damage » sont des dégâts DIRECTS à l'identité, plus des dégâts indirects répartissables sur un allié. Le choix « Choose any upgrade from the Sense deck » de `60018` reste obligatoire une fois l'option prise (pas de « may »).
- `60095` Power Struggle : l'icône imprimée est **Amplify** (glyphe `F` de `ChampionsIcons.ttf`), ni Acceleration (valeur d'origine) ni Hazard (valeur du 11/10 matin).
- `60191` Flight Serum : aucune icône de boost imprimée (`Boost` 0).
- `60001a` THW 2 et second paragraphe, `60018` coquille « Daredeveil », `60161a` « expert mode. » : relus sur scan.
- `60033` Bullseye : seule l'image a changé (vraie illustration), la fiche et le script sont inchangés.
