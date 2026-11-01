from . import *

# Psychic Tremor : OBLIGATION, boost 2. A donner au joueur de Mantis.
# You may flip to alter-ego form. Choose:
# • Exhaust your alter ego → remove Psychic Tremor from the game.
# • Discard 1 card from your hand for each confused character you control and each confused enemy. If no cards were discarded this way, this card gains surge. Discard this obligation.
#
# CARTES DE REFERENCE
#  - `01165` Eviction Notice / `03026` Man Out of Time : le gabarit des obligations a deux branches : `WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm` + `ChooseAbilities`
#    (branche 1 : `condition=player.IsAlterEgo()` + `Exhaust("YourIdentity")` + `Faces.RemoveAllFromGame`) ; defausse de N cartes de la main choisies par le joueur :
#    `SetTarget(range=(n, n), from_where=["YourHandCards"], canbe_discard=True)` ; `this.GainSurge(1, effect)`.
#
# TEXTE CONTRE CODE
#  « each confused CHARACTER YOU CONTROL » : l'identite et les allies de ce joueur qui portent le statut. « and each confused ENEMY » : tous les ennemis en jeu (vilain et sbires) qui le portent.
#  « discard 1 card FROM YOUR HAND » : le joueur CHOISIT les cartes (pas au hasard), et jamais plus que sa main. « If NO cards were discarded this way, this card gains surge » : sans carte defaussee
#    (aucun confus, ou main vide). La phrase « Discard this obligation » appartient a la seconde branche (comme sur les obligations officielles) : la branche 1 la RETIRE DU JEU.
#  Chiffres : boost 2, 1 carte par personnage confus.


def GetAbilities() -> Sequence['Ability']:

    def psychic_tremor(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(joueur, effect)

        # Compte AU MOMENT du choix (apres l'eventuel retournement : il ne change aucun statut).
        confus = [f for f in joueur.GetControlCharacters() if f.IsConfused()]
        confus += [f for f in Worlds.FindCardsOnField(effect, card_type=Enemy) if f.IsConfused()]
        a_defausser = min(len(confus), joueur.hand_cards.GetSize())

        def defausser_et_defausser_celle_ci(cibles: Sequence['CardFace']) -> None:
            Faces.DiscardAll(cibles, effect)
            if not cibles:
                this.GainSurge(1, effect)
            Faces.DiscardAll([this], effect)

        seconde = AbilityFactory.ForChoiceAbility(
            "Discard 1 card from your hand for each confused character you control and each confused enemy. Discard this obligation",
            defausser_et_defausser_celle_ci,
        )
        if a_defausser > 0:
            seconde.SetTarget(range=(a_defausser, a_defausser), from_where=["YourHandCards"], canbe_discard=True)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust your alter ego → remove Psychic Tremor from the game",
                lambda cibles:
                    Faces.RemoveAllFromGame([this], effect),
                condition=joueur.IsAlterEgo(),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
            seconde,
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            psychic_tremor,
        ),
    ]
