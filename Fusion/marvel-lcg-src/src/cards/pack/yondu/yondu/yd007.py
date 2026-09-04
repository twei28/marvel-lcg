from . import *

# Jackpot! — RESSOURCE signature, x1 (n/15 = 10). Ressource [wild].
# Response: After you spend this card, treat the next card you spend as if it
#   has double the resources.
#
# Cartes de reference :
#  - **`AfterYouSpendThisCard(type, op)`** (resources.py:508) pour « After you
#    spend this card ».
#  - **`29038`** Haywire (set Zzzax) : le SEUL montage du depot qui reecrit ce
#    que vaut une carte au moment du paiement —
#    `WhenCountingResourcesOnCards(None, op, from_where=DeckType.HandsArea)`
#    puis `message.SetReturnValue(res, effect)` (ability_factory.py:447,
#    sender_player.py:474). Voir aussi `ma005` (pack ms_america), qui commente
#    longuement la meme fenetre.
#  - `im013` / `as015` pour `RegisterTemp(..., unregister_after_exec=True)`.
#
# ⚠ POURQUOI PAS `DoubleResourcesThisGenerates` (resources.py:36), employe par
# `01055` The Power of Aggression et ses quatre jumelles. Cette fabrique double
# ce que **CETTE** carte genere. Jackpot! double ce que genere **LA SUIVANTE**,
# et ne genere elle-meme qu'un [wild] ordinaire. Les deux textes se
# ressemblent, la mecanique est inverse.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « the **NEXT** card you spend » : UNE seule carte, la premiere comptee
#    apres celle-ci. D'ou `unregister_after_exec=True`, qui retire l'effet des
#    qu'il a servi. Sans lui, tout le paiement serait double.
#  - « as if it has **double the resources** » : on double ce que la carte
#    VAUT, pas le cout a payer. `SetReturnValue(res * 2)`.
#  - « After you **spend** this card » : depensee comme RESSOURCE, pas jouee.
#    Jackpot! est une carte de type Resource, elle n'a pas d'autre usage.
#  - ⚠ ECART ASSUME. `WhenCountingResourcesOnCards` se declenche au COMPTAGE
#    des ressources d'une carte de la main, ce qui n'est pas exactement
#    « depenser ». Le moteur n'offre pas de fenetre plus fine, et c'est deja
#    par celle-ci que passent Haywire et Ms. America. Consequence possible :
#    si le moteur compte une carte que le joueur ne depense finalement pas, le
#    doublement est consomme pour rien. Signale plutot que masque.


def GetAbilities() -> Sequence['Ability']:

    def jackpot(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(message)

        def doubler(sous_effect: 'Effect', sous_message: 'Message.WhenCountingResourcesOnCards') -> None:
            sous_message.SetReturnValue(sous_message.return_res * 2, sous_effect)

        this.effect.RegisterTemp(
            AbilityFactory.WhenCountingResourcesOnCards(
                None,
                doubler,
                from_where=DeckType.HandsArea,
            ),
            unregister_after_exec=True,
            until_phase_end=True,
        )

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.Response,
            jackpot,
        ),
    ]
