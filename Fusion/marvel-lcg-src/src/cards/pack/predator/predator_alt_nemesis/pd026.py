from . import *

# Chopper — MANIGANCE ANNEXE (set « Predator Alt Nemesis »), menace 3 (fixe), Boost 2. Permanent. Hazard.
# Permanent.
# While there is no threat here, this scheme loses the [hazard] icon.
# Forced Response: After threat is placed here, if there is at least 8 threat here, the players lose the game.
#
# Cartes de reference :
#  - `sk285` Ultimate Nullifier / `27144` : `ThisGainKeyword(fn, hazard=N, change_on_event=...)` (l'icone Hazard portee par la carte) ;
#    `sk138` : `change_on_event=OnEvent.Threat("This")` (un bonus qui suit la MENACE de la carte) ;
#  - `AfterSchemePlaceThreat(type, "This", op, has_at_least_threat=N)` (scheme.py) ; `Worlds.SetGameOver(False, effect)` (27102b,
#    sk145b) pour « the players lose the game » ;
#  - `Permanent` et `Hazard` : bases automatiques (`desc`), AUCUN script (fiches permanent.md, hazard.md).
#
# ⚠ Mots-pieges :
#  - « WHILE there is NO threat here, loses the hazard icon » : l'icone (imprimee, `desc.Hazard 1`) disparait a 0 menace et
#    REVIENT des qu'il y en a de nouveau (bonus -1 dynamique, pas une suppression definitive).
#  - « AFTER threat is placed here » : la menace POSEE (pas l'escalade des autres cartes) ; « at least 8 » = 8 ou plus, comptee
#    sur la carte entiere.
#  - « Permanent » : elle ne quitte pas le jeu (meme vaincue : a verifier au harnais) ; « the PLAYERS lose » : defaite collective.


def GetAbilities() -> Sequence['Ability']:

    def sans_menace(effect: 'Effect', faces: List['CardFace']) -> int:
        Unused(faces)
        this = effect.this.CastTo(EncounterSideScheme)
        return 1 if this.threat == 0 else 0

    def perdu(effect: 'Effect', message: 'Message.AfterSchemePlaceThreat') -> None:
        Unused(message)
        Worlds.SetGameOver(False, effect)

    return [
        AbilityFactory.ThisGainKeyword(
            sans_menace,
            hazard=-1,
            change_on_event=OnEvent.Threat("This"),
        ),
        AbilityFactory.AfterSchemePlaceThreat(
            AbilityType.ForcedResponse,
            "This",
            perdu,
            has_at_least_threat=8,
        ),
    ]
