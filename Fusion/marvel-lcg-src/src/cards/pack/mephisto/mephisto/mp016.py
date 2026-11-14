from . import *

# Aid the Condemned — MANIGANCE ANNEXE. Boost 1, Crisis, menace de depart 2 (fixe), Hinder 2[per_hero] (natifs, `desc`).
# When Defeated : Each player looks at 1[per_hero] card in Damnation and shuffles it back into their owner's deck.
#
# Cartes de reference : hf508 (`WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", ..)`), mp008 (choix dans la Damnation), `RegarderEtRemelanger`.
# ⚠ Mots-pieges : « EACH player » : une fois par joueur, dans l'ordre ; « 1[per_hero] » = 1 x nombre de joueurs, PAR joueur ; « its OWNER's deck » :
# le proprietaire de la carte, pas celui qui la regarde.


def GetAbilities() -> Sequence['Ability']:
    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        Unused(message)
        for joueur in JoueursDansLOrdre(effect):
            RegarderEtRemelanger(effect, joueur, NombreDeJoueurs(effect))

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
