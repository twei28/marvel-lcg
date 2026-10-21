from . import *

# Burning Building — ATTACHEMENT. Boost 1.
# When Revealed : Attach to an unoccupied location and place 1 acceleration token here. Otherwise, surge.
# Forced Response : After the player phase ends, place 1 acceleration token here.
# Hero Action : Exhaust your identity and discard cards from your deck equal to the number of acceleration tokens here → discard this card.
#
# Cartes de reference : pu009 (`WhenThisRevealed` + `AttachTo2`), nt015 (`ThisCardGainSurge`), `AbilityFactory.AfterPhaseEnd` (turn_phase.py),
# `AbilityFactory.PlayerActionToDiscardThis(HeroAction, ex_operation=...)` (attachment.py), `Player.DiscardDeckTopCards`, `Ville.AuLieu` (brique M1,
# lit le lieu qui PORTE l'attachement).
# ⚠ « Attach to an unoccupied location » : le joueur qui revele CHOISIT parmi les lieux sans joueur ; aucun (ou plus de ville) : surge, et la carte
# (non attachee) est defaussee ; « acceleration token » = compteur `acceleration` (un attachement n'a pas de jeton d'acceleration de manigance) ;
# « discard cards from your deck equal to the number of tokens » : decide a l'action (le cout n'est pas bloque par un deck trop court) ; « Hero
# Action » : seulement par un joueur qui OCCUPE le lieu porteur (FAQ La Ville : on n'interagit qu'avec le lieu qu'on occupe).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        lieu = ChoisirLieuInoccupe(effect, message.GetToPlayer())
        if lieu is not None and this.AttachTo2(lieu, effect):
            Faces.PlaceCountersOn([this], 1, 'acceleration', effect)
        else:
            ThisCardGainSurge(effect)
            Faces.DiscardAll([this], effect)

    def fin_de_phase(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        Faces.PlaceCountersOn([effect.this], 1, 'acceleration', effect)

    def defausser_du_deck(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        n = effect.this.GetCounters('acceleration')
        if n:
            message.GetToPlayer().DiscardDeckTopCards(n, effect)

    def attache(effect: 'Effect', message: 'Message2') -> bool:
        return getattr(effect.this, 'bind_face', None) is not None

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.AfterPhaseEnd(AbilityType.ForcedResponse, "Player", fin_de_phase, conditions=[attache]),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction, conditions=[Ville.AuLieu], ex_operation=defausser_du_deck)
        .SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
