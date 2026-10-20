from . import *

# * Iron Fist (face heros, 1A) — DEFENDER. K'UN-LUN. MARTIAL ARTIST.
# PV 10, ATQ 2, CTR 1, DEF 2, main 5.
# Martial Arts Master — Response: After you play a card, place 1 chi counter here.
# Forced Response: After the player phase ends, remove all but 4 chi counters from here
#   and heal 1 damage for each chi counter removed this way.
#
# CARTES DE REFERENCE
#  - « After you play a card » (toute carte) : `fne/60027` Move in Shadow
#    (`AfterPlayerPlayedCard(Response, "You", None, op)` : `None` = n'importe quelle carte).
#  - compteur pose sur l'identite : `venus/tv001a` (`Faces.PlaceCountersOn([identite], n, 'dredge', effect)`).
#  - « After the player phase ends » : `aos/maria_hill/50029` Press Conference et
#    `michelangelo/tm009` (`AfterPhaseEnd(ForcedResponse, "Player", op)`).
#  - soin de soi : `jubilee/47012` (`this.HealthUnits([this], n, effect)`).
#
# TEXTE CONTRE CODE
#  ⚠ « Response » nu (pas « Hero Response ») mais imprime sur la face HEROS : la capacite
#    n'existe que quand cette face est visible ; Danny Rand ne pose pas de chi.
#  ⚠ « play a card » : une carte JOUEE (paiement compris), pas « mise en jeu » (Meditation,
#    Book of the Iron Fist ne declenchent rien) ; toute carte, tout type.
#  ⚠ « here » = cette carte, l'identite : les compteurs restent au retournement (decision n°5).
#  ⚠ « remove all BUT 4 » : on garde 4, on retire le SURPLUS (rien si 4 ou moins).
#  ⚠ « heal 1 damage for EACH chi counter removed THIS WAY » : soin = nombre retire par cet
#    effet, sur Iron Fist (« heal » sans cible = le personnage qui porte la capacite).
#  ⚠ Forced Response : aucune question ; ne part que s'il y a un surplus (sinon rien a faire).


def GetAbilities() -> Sequence['Ability']:

    def poser_un_chi(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)
        Faces.PlaceCountersOn([this], 1, CHI, effect)

    def surplus(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> bool:
        return Chi(effect.this) > CHI_CONSERVES

    def fin_de_phase(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)
        retires = Chi(this) - CHI_CONSERVES
        if retires <= 0:
            return
        Faces.RemoveCountersOn([this], retires, CHI, effect)
        this.HealthUnits([this], retires, effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            None,
            poser_un_chi,
        ).SetName("Martial Arts Master"),
        AbilityFactory.AfterPhaseEnd(
            AbilityType.ForcedResponse,
            "Player",
            fin_de_phase,
            conditions=[surplus],
        ),
    ]
