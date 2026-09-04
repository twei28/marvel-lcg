from . import *

# * Clarice Ferguson (face alter-ego) — MUTANT. REC 3, main 6, PV 9.
# Deserved Vacation - Forced Response: After you change to this form, shuffle
#   each [[PORTAL]] upgrade from play into your deck. Heal 1 damage from your
#   identity for each upgrade shuffled this way.
#
# TEXTE CONTRE CODE
#  « EACH ... from PLAY » -> tous les portails du terrain, contraste imprime
#    avec bk001a qui n'en prend QU'UN, et depuis la DEFAUSSE.
#  « for each upgrade SHUFFLED THIS WAY » -> le soin est compte sur ce qui a
#    REELLEMENT ete remelange, pas sur le nombre de portails avant l'effet.
#  « FORCED Response » -> obligatoire : passer en civil purge le moteur, c'est
#    le prix a payer pour le soin.


def GetAbilities() -> Sequence['Ability']:

    def vacances_meritees(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        portails = PortailsEnJeu(effect)
        if not portails:
            return
        Faces.ShuffleAllTo(portails, joueur.player_deck, effect)
        identite = joueur.GetIdentity()
        if identite is not None:
            this.HealthUnits([identite], len(portails), effect)

    return [
        AbilityFactory.AfterFlipToThisFace(
            AbilityType.ForcedResponse,
            vacances_meritees,
        ).SetName("Deserved Vacation"),
    ]
