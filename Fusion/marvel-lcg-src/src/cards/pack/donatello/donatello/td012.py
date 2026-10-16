from . import *

# * Donatello's Shell — AMELIORATION, cout 2, [physical]. ARMOR. TECH.
# You may play, spend, or discard cards tucked here as if they were in your
#   hand. (Max 1 tucked card.)
# Hero Action: Exhaust Donatello's Shell -> choose a card in your hand and tuck
#   it here.
#
# CARTES DE REFERENCE
#  - `60030` Contingency Planning (fne) : amelioration qui range UNE carte de
#    la main (`this.TuckCardUnderHere`) et la rend jouable comme en main
#    (`AbilityFactory.AttachedCardCanPlayLikeInHand`), condition « aucune
#    carte rangee ».
#  - `dd008` Doomstadt / `dz014` : plafond de cartes rangees =
#    `this.GetPlacedCardArea().GetSize()`, cible `YourHandCards`.
#
# TEXTE CONTRE CODE
#  « ANY card in your hand » -> aucun filtre de type (≠ dz014 : Event, 60030 :
#    Upgrade).
#  « (Max 1 tucked card.) » -> condition `GetSize() < 1` sur l'ACTION, sinon
#    on inclinerait la Carapace pour rien.
#  « play, spend, OR discard ... as if in hand » -> les TROIS, en entier (decision
#    du 15/10/2026, fidelite 100 %) : `AttachedCardCanPlayLikeInHand(also_discard=True,
#    also_spend=True)`. Jouer : `IsLikeInHand` ; depenser : `IsLikeInHandForSpend`
#    (cloisonnement des paiements, factory/resources.py) ; defausser :
#    `IsLikeInHandForDiscard` (couts `CostFunc.Discard("YourHandCards")` de td001b et
#    td009, et `Player.DiscardHandCards`). Voir mots-cles/tuck.md.
#  « Hero Action » : jouable en forme heros seulement.
#  L'insert fait de la Carapace le point d'ancrage de Metalhead (td002).


def GetAbilities() -> Sequence['Ability']:

    def ranger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        for face in effect.targets:
            if face is not None:
                this.TuckCardUnderHere(face, effect)

    def aucune_carte_rangee(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return effect.this.GetPlacedCardArea().GetSize() < 1

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.AttachedCardCanPlayLikeInHand(also_discard=True, also_spend=True),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            ranger,
            conditions=[aucune_carte_rangee],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("YourHandCards", range=(1, 1)),
    ]
