from . import *

# Lightforce Cleansing — custom « DesignHacker »
# Hero Action: Heal 3 damage from a friendly character. If 2 or more damage
#   was healed from Cloak this way, draw 2 cards.
# (Texte d'origine : « draw 1 card from each of your identities' decks » ;
#  avec un seul deck, cela devient « draw 2 cards ». Écart §9.)


def GetAbilities() -> Sequence['Ability']:

    def lightforce_cleansing(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()

        cible = effect.targets[0]
        soigne = this.HealthUnits([cible], 3, effect)

        identite = initiator.GetIdentity()
        est_cloak = (
            cible == identite and
            Hero.IsType(identite) and
            CardFinder(name=NOM_CLOAK).Check(identite)
        )
        if est_cloak and soigne >= 2:
            initiator.DrawUp(2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            lightforce_cleansing,
        ).SetPlay()
        .SetTarget(Friend, canbe_heal=True),
    ]
