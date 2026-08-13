from . import *

# Superhero Registration Act

def GetAbilities() -> Sequence['Ability']:

    def superhero_registration_act(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        player = Worlds.GetFirstPlayer(effect)

        if Worlds.IsCompetitiveMode(effect):
            # « In competitive mode, the enemy team finds the Choosing Sides
            # side scheme and your team reveals it. »
            #
            # La recherche appartient a l'equipe adverse, la revelation se fait
            # sur VOTRE table : c'est le joueur de votre camp qui recoit la
            # manigance. Le moteur cherche dans le deck rencontre de la zone du
            # chercheur, et les deux camps ont le leur.
            Find.FindAndReveal(
                effect,
                Worlds.GetYourTeam(effect),
                finder=CardFinder(name="Choosing Sides", card_type=EncounterSideScheme)
            )
            return
        if Worlds.IsCooperativeMode(effect):
            leader = Worlds.GetEnemyLeader(effect)
            if leader:
                Find.FindAndReveal(
                    effect,
                    player,
                    finder=CardFinder(card_type=EncounterSideScheme, set_name=leader.paper.set_name)
                )


    return [
        AbilityFactory.WhenCardSetup(
            "This",
            superhero_registration_act
        ),
    ]

