from . import *

# * Purple Peril

def GetAbilities() -> Sequence['Ability']:

    def purple_peril(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        # X = le nombre de cartes au tableau des victoires, plafonne a 5 par la
        # carte elle-meme.
        tableau = Worlds.VictoryDisplay(effect)
        valeur = min(5, len(tableau.GetAll()) if tableau else 0)
        for _ in range(valeur):
            face = initiator.DiscardDeckTopCard(effect)
            if face is None:
                break
            if face.paper.card_class == "Determination":
                initiator.GainCard(face, effect)

    return [
        AbilityFactory.CanPlayThisSchemeCard(),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.HeroResponse,
            'This',
            purple_peril
        ),
    ]
