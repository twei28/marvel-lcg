from . import *

# Cloaked (carte d'etat maison, pack TMNT, Shredder v3, scan Inkwire)
#
# Texte imprime : « The next time this character uses a basic power or
# activates, increase that value by 2, then discard this status card. The next
# time this character would take any amount of damage, decrease that value by 2,
# then discard this status card. »
#
# DECISION DE L'UTILISATEUR : UN SEUL effet, le premier qui arrive, puis la
# carte est defaussee (une carte Cloaked ne sert qu'une fois). Fiche :
# docs/reference/mots-cles/cloaked.md. Modele : `tough.py` (meme forme, meme
# `AbilityType.Status` sur le personnage porteur).
#
# Trois declencheurs, un seul consommateur (`consommer`) :
#  - un personnage non ennemi (heros, allie) utilise un pouvoir de base
#    (ATQ, CTR, DEF ou REC : `WhenUnitUseBasicPower`) -> +2 a CE pouvoir ;
#  - un ENNEMI s'active (`WhenEnemyActivateAgainstYou`, avec `would_act_message`,
#    qui n'existe que pour une vraie activation) -> +2 a son ATQ ou a sa MNG ;
#  - le personnage va subir des degats (`WhenUnitWouldTakeDamage`) -> -2, au
#    minimum 0.
# Un ennemi qui attaque ou manigance passe par `WhenUnitUseBasicPower` ET par
# `WhenEnemyActivateAgainstYou` : le premier branchement l'exclut (condition
# `pas_ennemi`), sans quoi le +2 serait compte deux fois.

# CORRECTIF (16/10/2026, scenario Baxter Stockman v3) : « Cloaked and Dazed status cards
# always resolve SIMULTANEOUSLY » (insert Dazed). Un porteur qui a AUSSI une carte Dazed
# laisse `dazed.py` resoudre le lot (somme des effets, puis les deux cartes defaussees) :
# `pas_de_dazed` ecarte donc les trois declencheurs ci-dessous dans ce cas.


def GetAbilities() -> Sequence['Ability']:

    def pas_de_dazed(effect: 'Effect') -> bool:
        return not effect.this.CastTo(StatusCard).GetBindFace().IsDazed()

    def consommer(effect: 'Effect') -> None:
        from game.operate.faces import Faces
        this = effect.this.CastTo(StatusCard)
        Faces.DiscardAll([this], effect)

    def pas_ennemi(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> bool:
        return not Enemy.IsType(message.trigger) and pas_de_dazed(effect)

    def pouvoir_de_base(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        message.GainValue(2, effect)
        consommer(effect)

    def activation(effect: 'Effect', message: 'Message.WhenEnemyActivateAgainstYou') -> None:
        would = message.would_message
        if isinstance(would, Message.WhenUnitWouldAttack):
            would.GainATKForThisAttack(2, effect)
        else:
            would.GainSCHForThisScheme(2, effect)
        consommer(effect)

    def vraie_activation_de_base(effect: 'Effect', message: 'Message.WhenEnemyActivateAgainstYou') -> bool:
        if message.would_act_message is None or not pas_de_dazed(effect):
            return False
        would = message.would_message
        if isinstance(would, Message.WhenUnitWouldAttack):
            return would.IsBasicAttack()
        return would.IsBasicScheme()

    def degats(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        a_retirer = min(2, message.will_take_damage)
        if a_retirer > 0:
            message.PreventDamage(a_retirer, effect)
            consommer(effect)

    return [
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.Status,
            "AttachedCharacter",
            pouvoir_de_base,
            conditions=[pas_ennemi],
        ),
        AbilityFactory.WhenEnemyActivateAgainstYou(
            AbilityType.Status,
            "AttachedEnemy",
            activation,
            conditions=[vraie_activation_de_base],
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Status,
            "AttachedCharacter",
            degats,
            conditions=[lambda effect, message: pas_de_dazed(effect)],
        ),
    ]
