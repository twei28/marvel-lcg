from . import *

# * Pestilent Nature — pacte BARGAIN (Corruptive Offers). Boost 3, Peril (natifs). Communs : `AbilitesDePacteCorrompu`.
# Interrupt : When a card you control leaves play, place 1 corrupt counter here -> shuffle that card into your deck instead.
#
# Cartes de reference : card_move.py `WhenCardWouldLeavePlay` (+ `SetBeInstead`), `Faces.ShuffleAllTo(.., joueur.player_deck, ..)` (nt001b).
# ⚠ Mots-pieges : « a card YOU CONTROL » : allies, ameliorations, soutiens du porteur (PAS cette carte elle-meme : sa propre defausse est le cout de sa Response) ;
# « INSTEAD » : la carte ne va pas en defausse, elle retourne dans le deck de son joueur ; carte de joueur seulement (jamais une carte de rencontre).


def GetAbilities() -> Sequence['Ability']:
    def une_des_miennes(effect: 'Effect', message: 'Message.WhenCardWouldLeavePlay') -> bool:
        porteur = effect.this.CastTo(Attachment).GetBindFace()
        joueur = porteur.GetControlByPlayer() if porteur is not None else None
        carte = message.trigger
        return (joueur is not None and carte is not effect.this and PlayerCard.IsType(carte)
                and carte.GetControlByPlayer() == joueur and not Identity.IsType(carte))

    def remelange(effect: 'Effect', message: 'Message.WhenCardWouldLeavePlay') -> None:
        this = effect.this.CastTo(Attachment)
        carte = message.trigger
        joueur = carte.GetControlByPlayer()
        # ⚠ Garde : le remelange fait QUITTER LE JEU la carte une seconde fois (message identique) : sans elle l'interruption se relance (52 compteurs vus).
        if getattr(this, "_mp113_en_cours", False):
            return
        this._mp113_en_cours = True
        try:
            Faces.PlaceCountersOn([this], 1, 'corrupt', effect)
            message.SetBeInstead(effect)
            Faces.ShuffleAllTo([carte], joueur.player_deck, effect)
        finally:
            this._mp113_en_cours = False

    return [
        *AbilitesDePacteCorrompu(),
        AbilityFactory.WhenCardWouldLeavePlay(AbilityType.Interrupt, CardFinder(), remelange, conditions=[une_des_miennes]),
    ]
