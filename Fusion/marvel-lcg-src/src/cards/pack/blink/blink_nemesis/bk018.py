from . import *

# * Timebroker — SBIRE NEMESIS. SCH 2 / ATQ 0 / PV 1. ILLUSION. 2 boost.
# Timebroker cannot take damage.
# [star] Forced Response: After Timebroker activates, place 2 threat on the
#   Damaged Reality side scheme.
# Forced Response: After Timebroker enters play, find the Damaged Reality side
#   scheme and reveal it.
#
# ⚠ UN SBIRE QU'ON NE TUE PAS. « cannot take damage » : le seul moyen de s'en
# debarrasser est de VAINCRE `bk019` Damaged Reality, dont le « When Defeated »
# le defausse. Le set entier est bati sur cette boucle, et il faut donc
# CONTRER, pas frapper.
#
# TEXTE CONTRE CODE
#  « ACTIVATES » -> attaque OU manigance, donc `AfterEnemyActivatesAgainstYou`
#    et pas `AfterUnitSchemeEnd` (leçon nt013).
#  « FIND the ... side scheme and REVEAL it » -> chercher ET reveler : la
#    trouver ne suffit pas.


def GetAbilities() -> Sequence['Ability']:

    def poser_deux_menaces(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)
        manigance = ManiganceEnJeu(effect)
        if manigance is not None:
            # ⚠ `PlaceThreatOn` N'EXISTE PAS (meme faute que bk019, corrigee le
            # meme jour). Le moteur avale l'exception : Timebroker manigançait
            # sans poser la moindre menace, et son cas restait VERT parce qu'il
            # mesurait l'autre moitie de la carte. C'est la gate
            # `verifier_appels_modules`, une fois reparee, qui l'a sortie.
            this.PlaceThreatOnSchemes([manigance], 2, effect)

    def convoquer_la_manigance(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        if ManiganceEnJeu(effect) is not None:
            return
        joueur = Worlds.GetCurrentPlayer(effect)
        faces = Search.SearchForCards(
            effect, joueur,
            include_encounter_deck=True,
            include_encounter_discard_pile=True,
            name=NOM_MANIGANCE,
        )
        if faces:
            faces[0].Reveal(joueur, effect)

    return [
        *AbilityFactory.UnitCannotTakeDamage("This"),
        AbilityFactory.AfterEnemyActivatesAgainstYou(
            AbilityType.ForcedResponse,
            "This",
            poser_deux_menaces,
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            convoquer_la_manigance,
        ),
    ]
