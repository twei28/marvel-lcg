from . import *

# Bloodthirst of Hala — TRAITRISE (Hala Ultimatum). 1 icone de boost. 2 exemplaires.
# When Revealed: Give the villain a tough status card. If the villain already has a tough status card,
#   the villain activates against you.
#
# Cartes de reference :
#  - « Give the villain a tough status card. If ... already ... » : `DonnerTenaceAuVillainOuSinon`
#    (hala_ultimatum/__init__.py).
#  - « the villain activates against you » : `face.DoActivate(joueur, effect)`, modele OFFICIEL 11051
#    Ancient Grudge (« Kang activates against you »).
#
# ⚠ Mots-pieges : « against YOU » = le joueur qui revele cette carte, pas un autre ; CE scenario rend cette
# activation sans effet d'attaque direct puisque le mechant est HIDDEN tant que la face HIDDEN est active —
# la moitie attaque de HIDDEN (gs138a/gs139a/gs140a) redirige l'activation en carte de rencontre face
# cachee, AUCUN code supplementaire a ecrire ici : « the villain would attack you » s'applique de la meme
# facon, qu'elle vienne de la phase du mechant ou d'une activation forcee par une traitrise.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()

        def sinon(villain: 'Villain') -> None:
            if joueur is not None:
                villain.DoActivate(joueur, effect)

        DonnerTenaceAuVillainOuSinon(effect, sinon)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
