from . import *

# Family Ties — Obligation (set « Shang-Chi »), Boost 2, « Give to the Shang-Chi player ».
# You may flip to alter-ego form. Choose:
#  • Deal 2 damage to Shang-Chi → remove Family Ties from the game.
#  • Deal 2 damage to each ally. Discard this obligation.
#
# Cartes de reference :
#  - `sv011` Silver Down (silver_surfer) : MEME squelette — `WhenThisObligationGiveToYou`, `YouMayFlipToYourAlterEgoForm`,
#    puis `joueur.ChooseAbilities` avec `condition=` par branche.
#  - `45113` / `aoa` : `this.DealDamage(unites, N, effect)` ; allies en jeu : `Worlds.FindCardsOnField(effect, card_type=Ally)`.
#
# ⚠ Mots-pieges :
#  - 1re branche : « → remove FROM THE GAME » (jamais defausse) ; 2e branche : « DISCARD this obligation » : les deux sorties
#    DIFFERENTES de la meme carte (hc013 : une obligation reste en jeu tant qu'on ne la deplace pas).
#  - « Deal 2 damage to SHANG-CHI » est devant la fleche : un COUT (paye en degats a l'identite, forme comprise).
#  - « each ALLY » : tous les allies en jeu (le texte ne dit pas « you control »), 2 degats chacun ; sans allie la branche
#    reste jouable (elle ne fait que defausser l'obligation).


def GetAbilities() -> Sequence['Ability']:

    def family_ties(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return

        YouMayFlipToYourAlterEgoForm(joueur, effect)

        identite = joueur.GetIdentity()

        def subir_puis_retirer(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            if identite is not None:
                this.DealDamage([identite], 2, effect)
            Faces.RemoveAllFromGame([this], effect)

        def blesser_les_allies(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            allies = Worlds.FindCardsOnField(effect, card_type=Ally)
            if allies:
                this.DealDamage(list(allies), 2, effect)
            Faces.DiscardAll([this], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 2 damage to Shang-Chi → remove Family Ties from the game",
                subir_puis_retirer,
                condition=identite is not None,
            ),
            AbilityFactory.ForChoiceAbility(
                "Deal 2 damage to each ally. Discard this obligation",
                blesser_les_allies,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            family_ties,
        ),
    ]
