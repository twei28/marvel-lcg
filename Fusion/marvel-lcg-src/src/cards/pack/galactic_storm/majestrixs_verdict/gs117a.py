from . import *

# Earn the People's Favor (1A) — MANIGANCE PRINCIPALE, stade 1 (Majestrix's Verdict).
# Contents: Deathbird (I) and Deathbird (II) (Deathbird (II) and Deathbird (III) instead for expert mode).
#   Majestrix's Verdict, and Standard encounter sets. One modular encounter set (Imperial Guard).
# Setup: Set the Shi'ar Throne side scheme aside. Put the Imprisoned on Chandilar side scheme into play and
#   tuck each STARJAMMER ally under it.
#
# Cartes de reference :
#  - « Setup » d'une face 1A : `WhenCardSetup("This")` (modele officiel 50087a Batroc, qui met en jeu un
#    environnement mis de cote et met des allies de cote) ; `SetupCards.PutIntoPlay` / `SetAsideCards`.
#  - « tuck » : face VISIBLE sous la manigance (livret p.4), helper `Glisser` (`PlaceCardHere(.., True, ..)`).
#  - « Contents » : composition du scenario, portee par data/scenarios/gs_majestrix_verdict*.json.
#
# ⚠ Mots-pieges : « EACH STARJAMMER ally » = les six (Lilandra comprise) ; le Trone reste DE COTE (il entre en
# jeu par la Reponse forcee de Lilandra) ; Imprisoned on Chandilar entre en jeu avec ses 6 menaces de depart.


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        SetupCards.SetAsideCards(effect, name=TRONE, card_type=SchemeSide2)
        prison = SetupCards.PutIntoPlay(effect, name=PRISON, card_type=SchemeSide2)
        if prison is None:
            prison = Prison(effect)
        if prison is None:
            return
        starjammers = Worlds.GetSetAsideAreaCards(effect, CardFinder(trait=STARJAMMER, card_type=Ally))
        Glisser(prison, starjammers, effect)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
    ]
