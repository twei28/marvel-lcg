from . import *

# * Shocker (B)

def GetAbilities() -> Sequence['Ability']:

    def shocker(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(EncounterVillain)

        # « When Defeated: Deal 1 damage to each hero. Remove 10 threat from a
        # side scheme. Flip this card. » Meme boucle que la face A : la defaite
        # de Shocker n'est pas une fin de partie, c'est un tour de roue.
        message.SetBeInstead(effect)

        def degat(joueur: 'Player') -> None:
            this.DealDamage([joueur.GetIdentity()], 1, effect)

        Players.ForEachPlayer(effect, degat)
        RetirerMenaceDUneManigance(effect, 10)
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
