from . import *

# * Battleworld — SOUTIEN BASIQUE, cout 1, RES [energy]. LOCATION.
# Hero Action: Spend a [energy] resource and discard cards from the encounter
#   deck until a minion is discarded. Put that minion into play engaged with
#   you -> discard cards from the top of your deck until an ally is discarded.
#   Put that ally into play under your control.
#
# ⚠⚠ ON S'INFLIGE UN SBIRE POUR GAGNER UN ALLIE. La carte est un echange, pas
# un cadeau : elle sort un sbire du deck de rencontre AVANT de rendre l'allie,
# et la fleche dit bien que la premiere moitie est le PRIX de la seconde.
#
# CARTES DE REFERENCE
#  - `CostFunc.DiscardDeckTopUntil` (cost_func.py:1042) : defausser jusqu'a
#    trouver, comme COUT. C'est exactement la premiere moitie.
#  - `bc006` Lucky Hit : `Worlds.DiscardEncounterTopCard`, qui rend la carte.
#
# TEXTE CONTRE CODE
#  ⚠ « UNTIL a minion is discarded » : on ne s'arrete pas, on vide s'il le
#    faut. Deck de rencontre sans sbire : la carte ne se joue pas.
#  ⚠ « Put that minion into play ENGAGED WITH YOU » : il vient sur VOTRE table,
#    pas sur celle du voisin.
#  ⚠ « from the top of YOUR DECK » pour l'allie : le deck du joueur, pas celui
#    de rencontre. Deux paquets differents dans la meme phrase.
#  ⚠ « under YOUR control » : l'allie compte dans VOTRE limite d'allies.


def GetAbilities() -> Sequence['Ability']:

    def battleworld(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        # PREMIERE MOITIE — le prix : un sbire sorti du deck de rencontre.
        sbire = None
        for _ in range(60):
            face = Worlds.DiscardEncounterTopCard(effect)
            if face is None:
                break
            if Minion.IsType(face):
                sbire = face
                break
        if sbire is None:
            return
        sbire.PutIntoPlay(joueur, effect)

        # SECONDE MOITIE — le gain : un allie sorti du deck du joueur.
        allie = None
        for _ in range(60):
            face = joueur.DiscardDeckTopCard(effect)
            if face is None:
                break
            if Ally.IsType(face):
                allie = face
                break
        if allie is not None:
            allie.PutIntoPlay(joueur, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            battleworld,
        ).SetCostFunc(CostFunc.Spend(Cost("Y"))),
    ]
