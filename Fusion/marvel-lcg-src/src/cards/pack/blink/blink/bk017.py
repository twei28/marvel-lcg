from . import *

# Stranger in This Reality — OBLIGATION. 2 icones de boost.
#
# ⚠ EMPLACEMENT DU MODULE : le bandeau dit « BLINK », pas « BLINK NEMESIS ».
# Son `set_name` est celui du set HEROS, le module vit donc ICI.
# `database.py:197` cherche le module dans le dossier du SET : range dans
# `_nemesis/`, il ne serait JAMAIS charge et l'obligation entrerait en jeu
# sans rien faire, en silence. Piege bt019 / nt012 / yd013 / dr010 — CINQUIEME
# fois qu'il se presente, et la premiere ou il est vu AVANT d'ecrire.
#
# CARTES DE REFERENCE : `yd013` Banished et `dr010` Ancient Order of Druids,
# structure identique a deux branches.
#
# TEXTE CONTRE CODE
#  « REMOVE from the game » vs « DISCARD this obligation » : deux sorties
#    DIFFERENTES, jamais l'une pour l'autre.
#  « EACH PORTAL from play » -> tous, pas un.
#  « If NO PORTAL was discarded this way » -> le Renfort ne tombe que si le
#    terrain n'en portait AUCUN.
#  ⚠ Le joueur est pris sur le MESSAGE (`GetGaveToPlayer`), jamais sur
#    `effect.this` : une obligation est une carte de RENCONTRE (leçon yd013).


def GetAbilities() -> Sequence['Ability']:

    def etrangere(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return

        YouMayFlipToYourAlterEgoForm(joueur, effect)
        identite = joueur.GetIdentity()

        def incliner_puis_retirer(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            if identite is None:
                return
            Faces.ExhaustAll([identite], effect)
            Faces.RemoveAllFromGame([this], effect)

        def sacrifier_les_portails(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            portails = PortailsEnJeu(effect)
            if portails:
                Faces.DiscardAll(portails, effect)
            else:
                ThisCardGainSurge(effect)
            Faces.DiscardAll([this], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Clarice Ferguson to remove this from the game",
                incliner_puis_retirer,
                condition=(identite is not None and not identite.IsExhaust()),
            ),
            AbilityFactory.ForChoiceAbility(
                "Discard each Portal upgrade from play",
                sacrifier_les_portails,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            etrangere,
        ),
    ]
