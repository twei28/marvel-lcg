from . import *

# Corporate Demonstration : COMPLOT ANNEXE (nemesis 2/5). Menace 4, boost 1, icone Amplification.
# When Revealed: If ED-209 is not in play, find it and put it into play engaged with the RoboCop player.
#
# CARTES DE REFERENCE
#  - `bf023` Hush : « find X and put it into play engaged with you » (`Trouver` + `face.PutIntoPlay(joueur, effect)`). `nt016` : `Worlds.FindCardOnField(effect, name=..)` pour
#    « if X is not in play ». `16054` Vendetta : `desc.Amplify = 1` (icone lue nativement).
#
# TEXTE CONTRE CODE
#  « If ED-209 is NOT IN PLAY » -> teste AVANT de chercher ; present sur le terrain = on ne fait rien (le sbire n'est pas deplace). « FIND it » : deck rencontre, defausse ET mise de cote
#    (c'est la qu'attend le sbire nemesis). « engaged with THE ROBOCOP PLAYER » : ce joueur, pas celui qui a revele. L'icone imprimee (avion + croix) est l'AMPLIFICATION
#    (comparee a `16054`), pas l'Acceleration.
#  Chiffres : menace 4, boost 1.


def GetAbilities() -> Sequence['Ability']:

    def corporate_demonstration(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        if Worlds.FindCardOnField(effect, name=NOM_ED_209, card_type=Minion) is not None:
            return
        joueur = JoueurRoboCop(effect) or message.GetToPlayer()
        if joueur is None:
            return
        ed_209 = Trouver(effect, joueur, NOM_ED_209, Minion)
        if ed_209 is not None:
            ed_209.PutIntoPlay(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            corporate_demonstration,
        ),
    ]
