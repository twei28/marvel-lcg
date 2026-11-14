from . import *

def GetAbilities() -> Sequence['Ability']:
    def polymathe(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = effect.GetInitiator()
        identite = joueur.GetIdentity()
        # RR « Wild Resource » : un wild depense compte pour UN type, celui que le joueur declare (`GetPaidResources(True)` le lui
        # demande et le remplace par la couleur choisie, modele No Holding Back `gs301`).
        paye = effect.GetPaidResources(True)
        if paye.GetColor("R") > 0:
            Faces.GiveStatus([identite], "Tough", effect)
        if paye.GetColor("Y") > 0:
            Faces.ReadyAll([identite], effect)
        if paye.GetColor("B") > 0:
            joueur.DrawUp(1, effect)
            PlusUneTailleDeMain(effect, identite)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            polymathe,
        ).SetPlay().SetLabel(),
    ]
