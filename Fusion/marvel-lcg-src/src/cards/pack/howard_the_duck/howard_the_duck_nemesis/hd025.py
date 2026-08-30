from . import *

# Duck, Duck, Doom! — manigance annexe nemesis, menace 2*, Boost 2
# When Revealed: Place an ally you control beneath this card. If you cannot,
#   confuse your identity.
# When Defeated: Return the ally beneath here to its owner's hand.
#
# Modele exact : aos/aim_abduction/50081.py (Abduct Superhumans) —
# `this.TuckCardUnderHere(ally, effect)` pour glisser l'allie SOUS la
# manigance, puis `this.GetPlacedCardArea().Get()` au When Defeated pour
# retrouver ce qui y est range. 50081 remet les allies EN JEU, hd025 les rend
# EN MAIN a leur proprietaire -> `Faces.ReturnToHand(faces, "Owner", effect)`
# (faces.py:306, mode "Owner" prevu pour cela).
#
# « an ally YOU control » : `player.GetControlCardsByType(ally=True)`
# (piege `you control` du tableau). « If you CANNOT » : aucune allie du tout,
# verifie AVANT le choix ; le repli confuse l'IDENTITE du joueur vise
# (`Faces.GiveStatus([player.GetIdentity()], "Confused", effect)`, modele
# core/spider_man/32008.py Steel Fist pour le statut).
# « the ally BENEATH HERE » (When Defeated) : la zone rangee de CETTE carte,
# pas un allie quelconque — piege `that <nom>` du tableau.


def GetAbilities() -> Sequence['Ability']:

    def duck_duck_doom(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        player = message.GetToPlayer()
        if player is None:
            return

        allies = player.GetControlCardsByType(ally=True)
        if allies:
            cible = allies[0] if len(allies) == 1 else player.AskChooseFace(allies, effect)
            if cible is not None:
                this.TuckCardUnderHere(cible, effect)
                return

        Faces.GiveStatus([player.GetIdentity()], "Confused", effect)

    def duck_duck_doom_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)

        faces = list(this.GetPlacedCardArea().Get())
        if faces:
            Faces.ReturnToHand(faces, "Owner", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            duck_duck_doom,
        ),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            duck_duck_doom_defeated,
        ),
    ]
