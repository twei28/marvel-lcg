from . import *

# Damaged Reality — MANIGANCE ANNEXE NEMESIS. 2 menaces, 2 boost, 1 crise.
# When Revealed: Place 1 additional threat here for each [[PORTAL]] upgrade in
#   play. Then, discard 1 of those upgrades.
# When Defeated: Discard Timebroker.
#
# LE MIROIR DU KIT : plus Blink deploie de portails, plus la manigance coute
# cher a contrer — et c'est pourtant le SEUL moyen de se debarrasser de
# Timebroker, qui ne peut pas subir de degats.
#
# TEXTE CONTRE CODE
#  « for each PORTAL IN PLAY » -> tout le terrain, pas seulement ceux du
#    joueur actif : en multijoueur, la manigance compte TOUS les portails.
#  « THEN, discard 1 OF THOSE upgrades » -> un seul, et parmi ceux qui viennent
#    d'etre comptes. La menace est posee AVANT la defausse (« Then »).


def GetAbilities() -> Sequence['Ability']:

    def realite_endommagee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(SchemeSide2)
        Unused(message)
        portails = PortailsEnJeu(effect)
        if not portails:
            return
        # ⚠ `PlaceThreatOnSchemes`, et sur `[this]` : « place threat HERE »
        # vise la manigance elle-meme, pas le complot principal. Une premiere
        # version appelait `PlaceThreatOn`, qui N'EXISTE PAS — le moteur avale
        # l'exception, la manigance sortait donc avec ses 2 menaces imprimees
        # et le cas ne voyait qu'un chiffre trop bas. Modele `ag011`/`01109`.
        this.PlaceThreatOnSchemes([this], len(portails), effect)
        Faces.DiscardAll([portails[0]], effect)

    def defausser_timebroker(effect: 'Effect', message: 'Message2') -> None:
        Unused(message)
        sbire = TimebrokerEnJeu(effect)
        if sbire is not None:
            Faces.DiscardAll([sbire], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            realite_endommagee,
        ),
        # ⚠ `WhenSchemeBeDefeated` (defeated.py:436) : la fabrique dediee aux
        # MANIGANCES, distincte de celle des personnages.
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            defausser_timebroker,
        ),
    ]
