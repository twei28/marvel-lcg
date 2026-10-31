from . import *

# Hush — ENVIRONNEMENT (nemesis 4/5), boost 2.
# Each encounter card gains peril.
# Hero Action: Spend [energy][mental][physical] resources → discard this card and find the Gentlemen and put them into play engaged with you.
#
# CARTES DE REFERENCE
#  - `39064` The One with the Breakup : `GiveKeywordToInPlayWhenApplyThis(EncounterCard, peril=1)` pour « each encounter card gains peril ».
#  - `60122` (attachement a Hero Action payee) : `WhenInYourPlayTurn(HeroAction, op).SetCost(Cost(..))`.
#
# TEXTE CONTRE CODE
#  « each encounter card » -> `EncounterCard` (toute carte rencontre). « Spend [energy][mental][physical] » -> UNE de chaque : `Cost("YBR")`.
#  « discard this card AND find the Gentlemen and put them into play engaged with you » -> les deux, dans l'ordre. « engaged with YOU » ->
#    le sbire entre en jeu engage avec le joueur qui paie (`PutIntoPlay(joueur, ..)`). The Gentlemen sont LIES a Hush (`desc.Linked`).


def GetAbilities() -> Sequence['Ability']:

    def hush(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Environment)
        Unused(message)
        joueur = effect.GetInitiator()
        Faces.DiscardAll([this], effect)
        messieurs = Trouver(effect, joueur, NOM_GENTLEMEN, Minion)
        if messieurs:
            messieurs.PutIntoPlay(joueur, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            EncounterCard,
            peril=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            hush,
        ).SetCost(Cost("YBR")),
    ]
