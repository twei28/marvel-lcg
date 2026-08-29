from . import *

# Shield Ricochet
# Play only if Red Guardian's Shield is attached to an enemy or a scheme.
# Hero Action: Move Red Guardian's Shield to an enemy or a scheme X times ->
#   deal 3 damage to each enemy and remove 3 threat from each scheme Red
#   Guardian's Shield was moved to.
#
# X est le montant paye au-dela du cout imprime : `effect.GetCostX()`, le
# meme accesseur que les cartes officielles a cout X (Speed Cyclone 14006,
# Lethal Intent 22010).
#
# Le rebond est une BOUCLE, pas une selection de cibles : le joueur choisit une
# cible a la fois, et il doit la choisir APRES avoir vu ou le bouclier a atterri
# au coup precedent. Un `SetTarget(..., range=(1, X))` ne conviendrait donc pas
# (le moteur demanderait tout d'un bloc, et X n'est pas connu a la declaration
# de la capacite). Montage retenu : `AskChooseFace` a chaque iteration, comme
# Brains and Brawn (bw025), qui repete lui aussi un choix de cible autant de
# fois qu'un compteur calcule en cours d'effet le demande.
#
# `AttachTo2` fait tout le deplacement : il detache le bouclier de son porteur
# actuel avant de le planter sur la nouvelle cible.
#
# Les degats et la menace ne tombent qu'A LA FIN, une seule fois par cible :
# le texte dit « each enemy » et « each scheme », donc une cible visitee deux
# fois ne prend pas 6. La liste `visites` est donc dedupliquee a l'insertion.


def GetAbilities() -> Sequence['Ability']:

    def shield_ricochet(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        x = effect.GetCostX()
        if x <= 0:
            return

        visites: List['CardFace'] = []
        for _ in range(x):
            bouclier = BouclierEnJeu(effect)
            if bouclier is None:
                break

            cibles = list(Worlds.FindCardsOnField(effect, card_type=Enemy)) + \
                list(Worlds.FindCardsOnField(effect, card_type=Scheme2))
            if not cibles:
                break

            cible = joueur.AskChooseFace(cibles, effect, not_move=True)
            if cible is None:
                break

            if not bouclier.CastTo(Upgrade).AttachTo2(cible, effect):
                break

            if cible not in visites:
                visites.append(cible)

        ennemis = [face for face in visites if Enemy.IsType(face)]
        manigances = [face for face in visites if Scheme2.IsType(face)]

        if ennemis:
            this.DealDamage(ennemis, 3, effect)
        if manigances:
            this.RemoveThreatFromSchemes(manigances, 3, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            shield_ricochet,
            conditions=[BouclierEstAttache],
        ).SetPlay(),
    ]
