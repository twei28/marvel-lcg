from . import *

# Attack on Mount Athena

def GetAbilities() -> Sequence['Ability']:

    def attack_on_mount_athena(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        villain = Worlds.FindVillain(effect)
        assert villain
        faces = SetupCards.SetAsideCards(
            effect,
            set_name="Experimental Weapons",
        )
        GetExperimentalWeapons(effect).Create(effect, villain, has_discard_pile=False)
        GetExperimentalWeapons(effect).PushCards(faces, effect)
        # « shuffle them together, and set them facedown ». `PushCards` ne
        # melange pas : l'ordre n'etait aleatoire que parce que les cartes
        # sortaient du deck rencontre deja melange (audit du 04/10/2026).
        GetExperimentalWeapons(effect).deck.Shuffle(effect)


    return [
        AbilityFactory.WhenCardSetup(
            "This",
            attack_on_mount_athena
        ),
    ]

