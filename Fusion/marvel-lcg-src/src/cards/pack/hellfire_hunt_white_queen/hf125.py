from . import *

# Telepathic Interrogation. Manigance annexe, icone Crise. « When Revealed : Place 2 additional threat here for each ILLUSION card in play.
# [star] Boost : If the White Queen is in PSIONIC form, you are confused. » Cartes de reference : 02026 / 06027 (menace selon le nombre de
# cartes en jeu), 41029 (`GiveStatus(..., "Confused")`).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        valeur = 2 * NombreDIllusions(effect)
        if valeur > 0:
            this.PlaceThreatOnSchemes([this], valeur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if EstPsionique(VilainWQ(effect)):
            Faces.GiveStatus([message.GetToPlayer().GetIdentity()], "Confused", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
