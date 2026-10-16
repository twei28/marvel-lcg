from . import *

# Dazed (Hebete), carte d'etat maison, scenario Baxter Stockman v3 (Inkwire).
#
# Texte imprime (scan « Dazed (1).png ») : « The next time this character uses a
# basic power or activates, decrease that value by 2, then discard this status
# card. The next time this character would take any amount of damage, increase
# that value by 2, then discard this status card. »
#
# Encart « Dazed Rules Insert » (regle) : « Unlike other status cards, this status
# card has TWO ways in which it will trigger: when the character uses a basic power
# (or activates), when the character would receive damage. » Un personnage ne peut
# porter qu'UNE carte Dazed (sauf mention contraire), Steady / Stalwart ne changent
# rien. « Tough status cards always resolve before Cloaked status cards, and Cloaked
# and Dazed status cards always resolve SIMULTANEOUSLY. » Fiche :
# docs/reference/mots-cles/dazed.md. Modele : `cloaked.py` (meme trois declencheurs,
# meme consommateur unique : le premier qui arrive, puis la carte part).
#
# SIMULTANEITE AVEC CLOAKED : le resultat d'un Cloaked (+2 puissance / -2 degats) et
# d'un Dazed (-2 puissance / +2 degats) pris ENSEMBLE n'est pas celui de deux
# resolutions successives : 1 degat avec Cloaked seul d'abord donne 0 (le Dazed ne
# se declenche alors plus) ; pris ensemble, 1 - 2 + 2 = 1 et les deux cartes partent.
# `cloaked.py` s'efface donc devant un Dazed du meme porteur, et c'est CE module qui
# resout le lot : somme des effets, puis toutes les cartes concernees defaussees.
#
# TOUGH D'ABORD : si le porteur a une carte Tough qui va absorber les degats (pas de
# perforant), ni Dazed ni Cloaked ne sont consommes : Tough resout avant eux.


def GetAbilities() -> Sequence['Ability']:

    def porteur(effect: 'Effect') -> 'Unit2':
        return effect.this.CastTo(StatusCard).GetBindFace()

    def consommer_le_lot(effect: 'Effect') -> None:
        """Defausse CETTE carte Dazed et, si le porteur en a, ses Cloaked (simultanes)."""
        from game.operate.faces import Faces
        this = effect.this.CastTo(StatusCard)
        unit = porteur(effect)
        Faces.DiscardAll([this], effect)
        if unit.cloaked > 0:
            unit.DiscardCloaked(effect, rule="All")

    def delta_de_puissance(effect: 'Effect') -> int:
        """-2 pour Dazed, +2 par Cloaked simultane."""
        return -2 + 2 * porteur(effect).cloaked

    def pas_ennemi(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> bool:
        return not Enemy.IsType(message.trigger)

    def pouvoir_de_base(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        delta = delta_de_puissance(effect)
        if delta != 0:
            message.GainValue(delta, effect)
        consommer_le_lot(effect)

    def activation(effect: 'Effect', message: 'Message.WhenEnemyActivateAgainstYou') -> None:
        delta = delta_de_puissance(effect)
        would = message.would_message
        if delta != 0:
            if isinstance(would, Message.WhenUnitWouldAttack):
                would.GainATKForThisAttack(delta, effect)
            else:
                would.GainSCHForThisScheme(delta, effect)
        consommer_le_lot(effect)

    def vraie_activation_de_base(effect: 'Effect', message: 'Message.WhenEnemyActivateAgainstYou') -> bool:
        if message.would_act_message is None:
            return False
        would = message.would_message
        if isinstance(would, Message.WhenUnitWouldAttack):
            return would.IsBasicAttack()
        return would.IsBasicScheme()

    def tough_absorbe(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        unit = porteur(effect)
        return unit.IsTough() and not message.property.ignore_tough

    def avant_degats(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        """« would take ANY AMOUNT of damage » : au moins 1, et Tough n'a pas la priorite."""
        return message.will_take_damage > 0 and not tough_absorbe(effect, message)

    def degats(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        unit = porteur(effect)
        subis = message.will_take_damage
        # +2 (Dazed), -2 par Cloaked simultane ; le total ne descend pas sous 0.
        total = max(0, subis + 2 - 2 * unit.cloaked)
        if total > subis:
            message.IncreaseDamage(total - subis, effect)
        elif total < subis:
            message.PreventDamage(subis - total, effect)
        consommer_le_lot(effect)

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
            conditions=[avant_degats],
        ),
    ]
