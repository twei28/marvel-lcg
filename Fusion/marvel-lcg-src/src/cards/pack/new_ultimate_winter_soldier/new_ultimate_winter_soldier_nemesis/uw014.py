from . import *

# Directorate X — complot annexe de l'ennemi juré. Menace de depart 2 par joueur. Pas d'icone de boost.
# Forced Response: After the villain phase ends, if Alonya Prostovich is in play, the engaged player discards cards from
# the encounter deck until a minion is discarded and reveal it. If it is not in play, the first player finds it and
# reveals it.
#
# Cartes de reference : `pu114` Punisher's Armory (« After the villain phase begins, ... discard from the encounter deck
# until a WEAPON is discarded. Reveal that card » = `Worlds.DiscardEncounterCardsUntil` + `face.Reveal(joueur, effect)`) ;
# `AfterPhaseEnd(ForcedResponse, "Villain", ...)` ; `Find.FindAndReveal(effect, joueur, name=...)` (`54037` Whiteout :
# « Find Blizzard and reveal him »).
#
# ⚠ ARBITRAGE PROVISOIRE (voir le gabarit) : le texte imprime est ambigu (« it » deux fois). Lecture retenue : « it » = Alonya
# Prostovich dans « if it is not in play, the first player finds it ». Alonya EN JEU : le joueur AVEC QUI ELLE EST ENGAGEE
# defausse le deck rencontre jusqu'a un sbire et le revele ; Alonya ABSENTE : le premier joueur la cherche (deck rencontre,
# defausse) et la revele.

ALONYA = "Alonya Prostovich"


def GetAbilities() -> Sequence['Ability']:

    def directorate_x(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        premier = Worlds.GetFirstPlayer(effect)
        alonya = next((f for f in Worlds.GetOnFieldCards(effect) if Minion.IsType(f) and f.IsName(ALONYA)), None)
        if alonya is not None:
            joueur = alonya.GetEngagedPlayer() or premier
            sbire = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
            if sbire is not None:
                sbire.Reveal(joueur, effect)
            return
        Find.FindAndReveal(effect, premier, name=ALONYA, card_type=Minion)

    return [
        AbilityFactory.AfterPhaseEnd(
            AbilityType.ForcedResponse,
            "Villain",
            directorate_x,
        ),
    ]
