from . import *

# * Hel-Wolf — sbire nemesis. CREATURE. UNDEAD. PV 6 / SCH 1 / ATK 3*.
# [star] The engaged player must defend against Hel-Wolf's attacks with an
#   ally they control, if able.
# [star] Boost: This attack gains overkill.
#
# Carte de reference : 01132 * Melter (pack core), qui porte la premiere
# phrase MOT POUR MOT — `WhenUnitAttackYou(AbilityType.NonKeywordStar, "This",
# ... message.MustDefendWithAlly(effect))`. Le « if able » est porte par le
# moteur lui-meme, pas par une condition a ecrire.
#
# Pour le boost : 01099 (attache a Rhino) accorde overkill a l'attaque en
# cours par `message.GainOverKill(effect)`.

def GetAbilities() -> Sequence['Ability']:

    def boost_overkill(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        # « This attack gains overkill » : l'attaque en cours est celle pour
        # laquelle la carte vient d'etre revelee en boost.
        attaque = getattr(message, "would_atk_message", None)
        if attaque is not None:
            attaque.GainOverKill(effect)

    return [
        AbilityFactory.WhenUnitAttackYou(
            AbilityType.NonKeywordStar,
            "This",
            lambda effect, message:
                message.MustDefendWithAlly(effect),
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost_overkill,
        ),
    ]
