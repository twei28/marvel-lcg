from . import *

# Silver Down — Obligation (set « Silver Surfer »), Boost 1, « Give to the Norrin Radd player ».
# You may flip to alter-ego form. Choose:
#  • Exhaust Norrin Radd -> remove Silver Down from the game.
#  • Summon Dawn Greenwood and remove her from the game -> remove Silver Down from the game.
#
# Cartes de reference :
#  - `yd013` Banished (yondu) et `lj013` Canine Urges (lockjaw) : MEME squelette — `WhenThisObligationGiveToYou`,
#    `YouMayFlipToYourAlterEgoForm`, puis `joueur.ChooseAbilities` avec `condition=` sur chaque branche.
#  - `Convoquer` du set (mot-cle maison `summon`, fiche summon.md).
#
# ⚠ Mots-pieges :
#  - AUCUNE branche ne DEFAUSSE l'obligation : les deux la RETIRENT DE LA PARTIE (piege hc013 : une obligation
#    reste en jeu tant qu'on ne la deplace pas).
#  - « Exhaust Norrin Radd » : l'alter-ego, donc seulement apres le retournement et si elle est prete ;
#    la fleche en fait un COUT.
#  - « Summon Dawn Greenwood AND REMOVE HER FROM THE GAME -> » : le tout est le COUT de la 2e branche ; elle
#    n'est offerte que si Dawn existe hors jeu (deck, defausse, main...). Dawn est RETIREE de la partie : plus
#    jamais disponible.


def GetAbilities() -> Sequence['Ability']:

    def silver_down(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
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

        def convoquer_dawn(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            dawn = Convoquer(effect, NOM_DAWN, Ally, joueur)
            if dawn is not None:
                Faces.RemoveAllFromGame([dawn], effect)
                Faces.RemoveAllFromGame([this], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Norrin Radd → remove Silver Down from the game",
                incliner_puis_retirer,
                condition=(identite is not None and joueur.IsAlterEgo() and not identite.IsExhaust()),
            ),
            AbilityFactory.ForChoiceAbility(
                "Summon Dawn Greenwood and remove her from the game → remove Silver Down from the game",
                convoquer_dawn,
                condition=PeutConvoquer(joueur, NOM_DAWN),
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            silver_down,
        ),
    ]
