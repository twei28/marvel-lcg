from . import *

def GetAbilities() -> Sequence['Ability']:
    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        # « Discard the top 2 cards of YOUR deck » : le joueur qui a VAINCU Mentor (arbitrage utilisateur du 26/10/2026 ; precedent FFG :
        # errata de Mystique's Manipulations « the defeating player »). Sans vainqueur (degats directs), le joueur engage avec lui.
        joueur = getattr(message, "defeating_player", None) or this.GetEngagedPlayer() or JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        faces = joueur.DiscardDeckTopCards(2, effect)
        differentes = set()
        for face in faces:
            differentes |= Types(face)
        if differentes:
            this.PlaceThreatOnSchemes("MainScheme", len(differentes), effect)

    return [
        # Modele 04054 The Viper.
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Identity,
            control_by="EngagedPlayer",
            hand_size=-1,
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            vaincu,
        ),
    ]
