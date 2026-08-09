from . import *

# * Ratatoskr
# Forced Interrupt: When Ratatoskr activates against you, discard 1 SQUIRREL
#   ally you control. If you cannot, Ratatoskr gets 1 additional boost card for
#   this activation.

def GetAbilities() -> Sequence['Ability']:

    def semer_la_zizanie(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        joueur = message.GetToPlayer()

        ecureuils = EcureuilsControles(effect, joueur)
        if ecureuils:
            choisi = joueur.AskChooseFace(ecureuils, effect)
            Faces.DiscardAll([choisi] if choisi else ecureuils[:1], effect)
        else:
            message.GiveAdditionalBoostCardForThisActivation(1, effect)

    return [
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.ForcedInterrupt,
            "This",
            semer_la_zizanie,
        ),
    ]
