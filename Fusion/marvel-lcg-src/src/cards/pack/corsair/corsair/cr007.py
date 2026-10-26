from . import *
# Parry. Evenement DEFENSE SKILL, cout 0.
#
# Hero Interrupt (defense): When Corsair defends against an attack, he gets +3 DEF for that attack. Draw 1 card. (If the
#   last card you played was Remise, draw 3 cards instead.)
#
# Cartes de reference : 03033 Expert Defense (`WhenUnitDefendAgainstAttack(HeroInterrupt, "YourHero")` +
# `message.GainDEFForThisAttack`) ; 01027 Focused Rage (`DrawUp(n, effect)` pioche n cartes) ; nt005 Kickflip (la derniere
# carte jouee = `player.stat.this_round_played_cards`, la carte en cours en est ecartee).
def GetAbilities() -> Sequence['Ability']:
    def parry(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = JoueurDe(effect)
        message.GainDEFForThisAttack(3, effect)
        if joueur is not None:
            joueur.DrawUp(3 if DerniereEstUne(effect, joueur, REMISE) else 1, effect)
    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.HeroInterrupt,
            "YourHero",
            parry,
        ).SetPlay().SetLabel('defense'),
    ]
