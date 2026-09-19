from . import *

# Pawn Shop Showdown 1B — 10, +1 : bases desc.
# Reduce the cost of the first upgrade played into this play area each round by 1.
# Forced Response: After an attachment or upgrade enters play in this play
#   area, place 1 threat here.
# La reduction : ReduceCostToPlayFaceWhen(Upgrade) pour le proprietaire, une
# fois par round (drapeau remis a zero en fin de round).

def GetAbilities() -> Sequence['Ability']:
    etat = {"round": -1}

    def premiere_du_round(effect: 'Effect', message: 'Message') -> bool:
        return etat["round"] != effect.world.round_id

    def apres_entree(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(MainScheme)
        carte = message.trigger
        if Upgrade.IsType(carte) and carte.GetControlByPlayer() is Proprietaire(this):
            etat["round"] = effect.world.round_id
        this.PlaceThreatOnSchemes([this], 1, effect)

    def concerne(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> bool:
        carte = message.trigger
        this = effect.this
        if Upgrade.IsType(carte):
            return carte.GetControlByPlayer() is Proprietaire(this)
        if Attachment.IsType(carte):
            porteur = carte.GetBindFace()
            return porteur is not None and DansCetteAire(porteur, this)
        return False

    def du_proprietaire(effect: 'Effect', message: 'Message') -> bool:
        joueur = effect.world.current_player
        return joueur is not None and joueur is Proprietaire(effect.this)

    return [
        AbilityFactory.ReduceCostToPlayFaceWhen(Upgrade, 1, "AnyPlayer", conditions=[premiere_du_round, du_proprietaire]),
        AbilityFactory.AfterCardEnterPlay(AbilityType.ForcedResponse, None, apres_entree, conditions=[concerne]),
        *CapacitesCommunes1B(),
    ]
