from . import *

# Skyfather (amelioration, cout 2, OLYMPUS TITLE, joker)
# Each event you own that does not have a printed "Special" ability gains:
# "Special: Deal 2 damage to an enemy."
# Response: After you resolve your "Skyfather's Tempest" ability, gain +1
# hand size until the end of the phase.
#
# ⚠ LE SPECIAL DONNE N'EST PAS CODE ICI. Le moteur n'a pas de fabrique qui
# greffe une capacite sur les cartes d'un joueur ou qu'elles soient (main,
# deck, defausse), et le seul moment ou ce Special peut etre resolu est
# l'appel de `ResoudreLeSpecialDe` (Tempest, Hera) : c'est LA qu'il vit, dans
# __init__.py, en consultant `SkyfatherDe(joueur)`. Ce module ne porte que
# la Response.
#
# Modeles : ab007 (capacite nommee), 12033 Assess the Situation
# (`GainUntilPhaseEnd(effect, hand_size=1)` sur l'identite).

def GetAbilities() -> Sequence['Ability']:

    def main_plus_un(effect: 'Effect', message: 'Message.AfterEffectResolved') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        initiator = effect.GetInitiator()
        initiator.GetIdentity().GainUntilPhaseEnd(effect, hand_size=1)

    return [
        AbilityFactory.AfterPlayerResolveAbility(
            AbilityType.Response,
            "You",
            CardFinder(name="Zeus", card_type=Hero),
            main_plus_un,
            ability_name=TEMPEST,
        ),
    ]
