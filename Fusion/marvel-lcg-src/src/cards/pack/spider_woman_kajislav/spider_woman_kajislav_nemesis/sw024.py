from . import *

# Violent Disturbance — TRAITRISE de nemesis (4/5 et 5/5), x2. Boost 1.
# When Revealed: Discard all identity-specific cards from your hand.
#
# ⚠ LA VERSION BRUTALE DE `sw021` Man-Bull : lui en fait defausser UNE a
# chacun, elle les prend TOUTES au joueur qui la revele. Contre Spider-Woman,
# dont tout le moteur vit dans son set heros, c'est la carte la plus dure du
# set.
#
# ⚠ Le fichier source s'appelle « interruption nemesis » : le nom du FICHIER
# n'est pas celui de la carte. Voir l'importeur.
#
# CARTE DE REFERENCE
#  - `sw021` * Man-Bull : `EstSpecifiqueALIdentite`, partage par les deux.
#
# TEXTE CONTRE CODE
#  ⚠ « from YOUR hand » : celui qui revele, pas toute la table. C'est la
#    difference exacte avec Man-Bull.
#  ⚠ « ALL » : pas de choix, pas de compte.


def GetAbilities() -> Sequence['Ability']:

    def perturbation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(effect.this)
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        cartes = [f for f in joueur.hand_cards.GetAll()
                  if f is not None and EstSpecifiqueALIdentite(f)]
        if cartes:
            Faces.DiscardAll(cartes, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, perturbation),
    ]
