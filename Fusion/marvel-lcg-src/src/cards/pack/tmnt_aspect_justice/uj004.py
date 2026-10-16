from . import *

# * Cowabunga (Mikey) — ALLIE 2 [mental], aspect Justice (TMNT Aspects, Inkwire). NINJA. PARTY. TURTLE.
# PV 2, THW 2 (1 degat consecutif), ATK 1 (1 degat consecutif).
# Response: After Cowabunga enters play, discard a resource card from your hand → draw 2 cards and heal
#   2 damage from a friendly character.
#
# CARTES DE REFERENCE
#  - `01083` Mockingbird / RECETTES §1 : « After <allie> enters play » = `AfterCardEnterPlay(Response,
#    "This", op)`.
#  - Cout « discard a <type> card from your hand → » : `CostFunc.Discard("YourHandCards", card_type=...)`
#    (cost_func.py, cible `YourHandCardsDiscardable`), modele `card_type=Resource` des cartes qui ciblent
#    une carte RESSOURCE de la main.
#  - `tv001b` Bonnie : « heal 2 damage from a friendly character » = `HealthUnits(cibles, 2, effect)` sur
#    `Friend` blesse.
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « enters play » (pas « you play from your hand ») : toute entree en jeu, y compris par un effet.
#  ⚠ « discard a RESOURCE card from your hand → » : FLECHE = COUT ; une carte de TYPE Resource (pas une
#    carte quelconque utilisee pour ses icones). Sans carte ressource en main, la Reponse n'est pas offerte.
#  ⚠ « draw 2 cards AND heal 2 damage » : les deux ; le soin vise UN personnage AMI blesse (heros, allie,
#    de n'importe quel joueur). Personne de blesse : on pioche quand meme, le soin est sans objet.
#  Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def cowabunga(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        joueur.DrawUp(2, effect)

        blesses = [f for f in Worlds.GetOnFieldFriendlyCharacters(effect)
                   if f.max_health > f.health]
        if not blesses:
            return

        def soigner(cibles: Sequence['CardFace']) -> None:
            this.HealthUnits(list(cibles), 2, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Heal 2 damage from a friendly character", soigner,
            ).SetTarget(blesses, range=(1, 1), not_move=True),
        )

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            cowabunga,
        ).SetCostFunc(CostFunc.Discard("YourHandCards", card_type=Resource)),
    ]
