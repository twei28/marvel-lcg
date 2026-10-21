from . import *

# * Microchip — SBIRE UNIQUE. GENIUS. VIGILANTE. SCH ★, ATQ ★, 3 PV, Boost 1.
# Punisher cannot attack this minion.     (porte par `CARTES_QUE_PUNISHER_NE_PEUT_PAS_ATTAQUER_PU` dans __init__.py)
# ★ Forced Interrupt : When Microchip would activate, give Punisher a facedown boost card instead.
# When Defeated : Reveal the top WEAPON attachment in the encounter discard pile.
#
# Cartes de reference : `WhenEnemyWouldActivate` + `SetBeInstead` (pu091a), `Faces.GiveFacedownBoostCards` (sk167),
# `Worlds.GetEncounterDiscardPileCards` (ag001b), `face.Reveal(joueur, effect)`.
# ⚠ « instead » : Microchip ne s'active pas ; « the TOP weapon » : l'arme la plus HAUTE de la defausse (la plus recente) ; aucune =
# rien. SCH/ATQ « ★ » : `desc` `0**`.

def GetAbilities() -> Sequence['Ability']:

    def au_lieu_d_activer(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        message.SetBeInstead(effect)
        DonnerUneCarteBoostFaceCachee(effect, Punisher(effect), 1)

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        armes = [c for c in Worlds.GetEncounterDiscardPileCards(effect) if Attachment.IsType(c) and c.HasTrait("WEAPON")]
        if armes:
            armes[0].Reveal(Worlds.GetFirstPlayer(effect), effect)

    return [
        AbilityFactory.WhenEnemyWouldActivate(AbilityType.ForcedInterrupt, "This", au_lieu_d_activer),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
