from . import *

# Welcome to the Jungle (Concrete Jungle) : mise en jeu par le Setup du complot
# (tk005a). « When Defeated: Each player may choose 1 set-aside NYC card and put it
# into play. » Les 4 cartes `Linked (Welcome to the Jungle)` sont mises de cote par
# le moteur des que cette carte est creee (desc.Linked, cards/database.py).

def GetAbilities() -> Sequence['Ability']:

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        def action(joueur: 'Player') -> None:
            candidates = [f for f in Worlds.GetSetAsideAreaCards(effect) if f.HasTrait("NYC")]
            if not candidates:
                return

            def mettre(targets):
                for face in targets:
                    face.PutIntoPlay(joueur, effect, under_control=True)

            joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility("Put a set-aside NYC card into play", mettre)
                .SetTarget(CardFace, trait="NYC", from_where=["SetAside"]),
            )

        Players.ForEachPlayer(effect, action)

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
