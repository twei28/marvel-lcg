from . import *

# Scarab

def GetAbilities() -> Sequence['Ability']:

    def scarab(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        scheme = Worlds.FindCardOnField(
            effect,
            name="Ancient Ritual",
            card_type=Scheme2
        )
        if scheme:
            value = 1
            # CORRECTIF : le texte dit « 3 threat instead if the attack DEFEATED
            # an ally ». damaged_targets liste les cibles qui ont SUBI des
            # degats : 3 menaces etaient posees des qu'un allie etait blesse,
            # meme s'il survivait. Il faut aussi qu'il soit vaincu.
            if [x for x in message.damaged_targets if Ally.IsType(x) and x.IsDefeated()]:
                value = 3
            this.PlaceThreatOnSchemes([scheme], value, effect)

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.NonKeywordStar,
            "This",
            scarab
        ),
    ]

