from . import *

# Scaly Setback

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « [star] Boost: If the villain is attacking, this attack gains
        # overkill. » `during_attack` porte la condition « si le vilain
        # attaque » : hors d'une attaque, la fabrique ne declenche rien.
        message.would_atk_message.GainOverKill(effect)

    return [
        # « The Lizard gets +10 hit points. » Le modele est celui de
        # « The "Immortal" Klaw » (01127) : la manigance porte les PV, et le
        # vilain les perd quand elle tombe.
        #
        # ⚠ Rend une LISTE d'abilites : l'etoile n'est pas optionnelle.
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name="The Lizard", card_type=Villain),
            health=10,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
            during_attack=True,
        ),
    ]
