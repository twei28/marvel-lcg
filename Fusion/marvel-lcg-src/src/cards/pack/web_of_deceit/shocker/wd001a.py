from . import *

# * Shocker (A)

def GetAbilities() -> Sequence['Ability']:

    def shocker(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(EncounterVillain)

        # « When Defeated: Remove 5 threat from a side scheme. Flip this card. »
        #
        # Shocker n'est JAMAIS vaincu pour de bon : le vaincre le retourne sur
        # sa face experte, et la partie ne se gagne que par The Long Night. On
        # interrompt donc la defaite au lieu de la laisser terminer la partie.
        message.SetBeInstead(effect)
        RetirerMenaceDUneManigance(effect, 5)
        this.card.Flip(effect)
        nouvelle = this.card.face.CastTo(Villain)
        nouvelle.ResetHealth(GameRule(nouvelle))

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.ForcedInterrupt,
            "This",
            shocker,
        ),
    ]
