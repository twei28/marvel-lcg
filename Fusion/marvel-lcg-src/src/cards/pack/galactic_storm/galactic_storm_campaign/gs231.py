from . import *

# * Goliath (CLINT BARTON) — ALLIE de campagne (Identity-Specific / Campaign, n° 231). Cout 4.
# THW 1 / ATK 2, 4 PV. GIANT.
# Honorary.
# Response: After Goliath uses a basic power, discard the top card of your deck. If a [physical]
#   resource was discarded this way, deal 1 damage to each enemy.
#
# Cartes de reference :
#  - **`game/ability/factory/friend.py`** `AbilityFactory.AfterUnitUseBasicPower` : trigger natif « After
#    X uses a basic power ».
#  - **`core/spider_man/01002`** Black Cat : `initiator.DiscardDeckTopCards(1, effect)` puis filtrage
#    `CardFinder(has_printed_res=...)` sur les cartes defaussees.
#
# ⚠ Mots-pieges :
#  - « Goliath uses a basic power » : Goliath lui-meme (un allie n'a normalement pas de pouvoir de base a
#    activer en dehors d'une capacite qui le lui donne — verifie construction uniquement, voir reste du
#    travail) ;
#  - « to EACH enemy » : sbires ET mechant, pas seulement les sbires engages ;
#  - condition stricte : le dommage ne part QUE si une carte [physical] a ete defaussee (pas « sinon »).


def GetAbilities() -> Sequence['Ability']:

    def goliath(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        Unused(message)
        this = effect.this.CastTo(Ally)
        joueur = this.GetControlByPlayer()
        defaussees = joueur.DiscardDeckTopCards(1, effect)
        if CardFinder(has_printed_res="R").Checks(defaussees):
            this.DealDamage(Worlds.FindCardsOnField(effect, CardFinder(card_type=Enemy)), 1, effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.ForcedResponse,
            "This",
            goliath,
        ),
    ]
