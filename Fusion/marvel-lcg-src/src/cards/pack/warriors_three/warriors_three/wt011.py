from . import *


def GetAbilities() -> Sequence['Ability']:
    def mighty(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if paye_avec(effect, "Volstagg"):
            amis = [joueur.GetIdentity()] + list(joueur.allies.Get())
            choisie = joueur.AskChooseFace(amis, effect, prompt="Give a tough status card", forced=True)
            if choisie is not None:
                Faces.GiveStatus([choisie], "Tough", effect)
            return
        # « Otherwise, give Volstagg a tough status card » : actif, c'est l'identite ; inactif, la carte d'etat attend sur son
        # soutien (notice de l'auteur : les etats des heros inactifs restent sur eux) et le suit quand il redevient actif.
        donner_etat_a_un_heros(effect, joueur, "Volstagg", "Tough")

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, mighty).SetPlay().SetLabel(),
    ]
