from . import *

# Lack of Chi — OBLIGATION d'Iron Fist (IRON FIST 1/1). 2 icones de boost.
# Give to the Danny Rand player.
# When Revealed: Move all chi counters from your identity to this card.
# Forced Interrupt: When you would place a chi counter on Iron Fist, place it here instead. If there are at least
#   4 chi counters here, discard this card.
#
# MOT-CLE : compteur chi — fiche docs/reference/mots-cles/chi-counter.md.
#
# CARTES DE REFERENCE
#  - obligation qui RESTE en jeu chez son joueur : `nebula/22027` (`WhenThisObligationGiveToYou`, la carte ne part que
#    par un `DiscardAll` explicite ; `obligation.py` ne la defausse pas d'elle-meme).
#  - compteur detourne : `human_torch_nemesis/ht012` (`WhenCardWouldBePlacedCounter`) et `04065` Crossbones' Armor
#    (`message.SetBeInstead(effect)` puis pose sur cette carte, defausse au seuil).
#
# TEXTE CONTRE CODE
#  ⚠ « MOVE all chi counters » : retires de l'identite, poses ici. Le seuil de 4 n'est PAS relu a la revelation : la
#    phrase « If there are at least 4 » appartient a l'Interruption forcee (elle ne se lit qu'apres un chi detourne).
#  ⚠ « on Iron Fist » = l'identite du joueur de l'obligation (les deux faces sont la meme carte ; seule la face heros
#    pose du chi). Un chi pose sur une AUTRE carte (64009 Embody the Dragon) n'est pas detourne.
#  ⚠ « place it here INSTEAD » : remplacement, l'identite ne recoit rien. La pose ICI a cette carte pour cible et ne
#    se redeclenche donc pas.
#  ⚠ « discard this card » : les chi poses dessus partent avec elle (perdus).

SEUIL = 4


def GetAbilities() -> Sequence['Ability']:

    def identite_du_joueur(this: 'Obligation') -> 'CardFace|None':
        if not this.card.IsOnField():
            return None
        joueur = this.GetGaveToPlayer()
        return joueur.GetIdentity() if joueur else None

    def deplacer_le_chi(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        identite = message.GetGaveToPlayer().GetIdentity()
        stock = Chi(identite)
        if stock > 0:
            Faces.RemoveCountersOn([identite], stock, CHI, effect)
            Faces.PlaceCountersOn([this], stock, CHI, effect)

    def sur_iron_fist(effect: 'Effect', message: 'Message.WhenCardWouldBePlacedCounter') -> bool:
        this = effect.this.CastTo(Obligation)
        identite = identite_du_joueur(this)
        return identite is not None and message.trigger.card is identite.card and message.counters > 0

    def detourner(effect: 'Effect', message: 'Message.WhenCardWouldBePlacedCounter') -> None:
        this = effect.this.CastTo(Obligation)
        message.SetBeInstead(effect)
        Faces.PlaceCountersOn([this], message.counters, CHI, effect)
        if Chi(this) >= SEUIL:
            Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            deplacer_le_chi,
        ),
        AbilityFactory.WhenCardWouldBePlacedCounter(
            AbilityType.ForcedInterrupt,
            None,
            CHI,
            detourner,
            conditions=[sur_iron_fist],
        ),
    ]
