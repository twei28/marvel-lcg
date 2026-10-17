from . import *

# Press and Protect — EVENEMENT 1 [wild], aspect Basic (TMNT Aspects, Inkwire).
# Team-Up (April O'Neil and Casey Jones). Max 1 per deck.
# Action: Remove 3 threat from a scheme and give a tough status card to a friendly character.
#
# NOUVELLE. Cartes de reference : 62023 Power Man and Iron Fist (Team-Up + effets a cibles : premier selecteur
# « TeamUp » EXIGE par le chargeur, puis `SetTarget2` / `SetTarget3`, cibles decalees dans `targets2/3`) ;
# 60055 (retirer 3 menaces : `RemoveThreatFromSchemes(..., 3)` sur `Scheme2`). Fiche mots-cles/teamup.md :
# `desc.TeamUp = "April O'Neil;Casey Jones"`, les ALLIES comptent (ub001 April O'Neil, ub005/tr002 Casey Jones,
# ou le heros Casey Jones tc001).
# TEXTE CONTRE CODE : « Action » (pas Action de heros : jouable en alter ego) ; « a scheme » (principale ou
#   annexe) ; « a FRIENDLY character » (identite ou allie) ; « Max 1 per deck » = `desc.MaxPerDeck`.


def GetAbilities() -> Sequence['Ability']:

    def press_and_protect(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.RemoveThreatFromSchemes(effect.targets2, 3, effect)
        Faces.GiveStatus(effect.targets3, "Tough", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, press_and_protect)
        .SetPlay().SetLabel()
        .SetTarget("TeamUp")
        .SetTarget2(Scheme2, range=(1, 1))
        .SetTarget3(Friend, range=(1, 1)),
    ]
