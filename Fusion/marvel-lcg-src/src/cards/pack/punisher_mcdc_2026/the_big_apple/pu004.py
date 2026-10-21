from . import *

# Gunrunner — ATTACHEMENT. SCH +1, ATK +1 (desc). Linked (Gunrunner's Warehouse) : desc. Permanent : desc.
# Attached villain gains steady and gets +7[per hero] hit points.
# When Revealed : Give the villain a tough status card.
# When attached villain is defeated, the players win the game.
#
# Cartes de reference : punishment/pu092.py (`GiveKeywordToAttached(Villain, health=..., trait=...)`, `WhenUnitBeDefeated(WhenDefeated,
# "AttachedCharacter", ...)`), linked.md (carte mise de cote par son complot 3A/3B), `Faces.GiveStatus(..., "Tough", ...)`.
# ⚠ « +7 PAR joueur » : 7 x joueurs ; « the villain » du When Revealed : celui auquel Gunrunner est attache ; Steady : donne au porteur.

def GetAbilities() -> Sequence['Ability']:

    def pv_supplementaires(effect: 'Effect') -> int:
        return 7 * Worlds.GetPlayerNum(effect)

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        porteur = this.bind_face
        villain = porteur if porteur is not None and Villain.IsType(porteur) else Worlds.FindVillain(effect)
        if villain is not None:
            Faces.GiveStatus([villain], "Tough", effect)

    def victoire(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Worlds.SetGameOver(True, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(Villain, health=pv_supplementaires, steady=1),
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "AttachedCharacter", victoire),
    ]
