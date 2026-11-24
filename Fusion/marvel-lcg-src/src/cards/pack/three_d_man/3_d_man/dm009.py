from . import *

# The Triune Understanding (Support)
#
# Alter-Ego Action: Add 1 threat to the main scheme, exhaust The Triune Understanding -> reduce the cost of the
#   next identity-specific card you play this round by 3.
#
# CARTES DE REFERENCE
#  - `an006` Angelic Ribbons : "discard this card" est un COUT -> `CostFunc.Discard("This")`, ici "exhaust This
#    card" -> `CostFunc.Exhaust("This")`.
#  - `bg012` Utility Belt / dm007 (meme session) : "reduce the cost of the next <X> card you play this round/turn"
#    -> `Worlds.UpdateNextCardPlayCost(joueur, -N, effect, finder=..., in_this=...)`.
#  - `card_face.py:1039` `PlaceThreatOnSchemes` : "add N threat to the main scheme" -> `PlaceThreatOnSchemes(
#    "MainScheme", N, effect)`.
#
# TEXTE CONTRE CODE
#  "Add 1 threat to the main scheme, exhaust ..." : DEUX clauses avant la fleche, mais le moteur n'a qu'un COUT
#    formel pour l'inclinaison (`CostFunc.Exhaust`) ; l'ajout de menace n'a pas de CostFunc dedie et ne peut de
#    toute facon pas "echouer" (une main scheme existe toujours en partie), donc execute sans condition en debut
#    d'operation, avant d'armer la reduction -- choix technique (pas de lecture de regle alternative possible,
#    les deux actes sont inconditionnels et simultanes a la resolution de l'Action).
#  "the next IDENTITY-SPECIFIC card" -> classe `IdentitySpecific` (`identity.py`'s `parse` : `Class: "Hero"` ->
#    `"IdentitySpecific"`) -> `CardFinder(card_class="IdentitySpecific")`.
#  "this ROUND" (pas "this turn"/"this phase") -> `in_this="Round"`.
#  "by 3" -> -3.

def GetAbilities() -> Sequence['Ability']:

    def triune_understanding(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        this.PlaceThreatOnSchemes("MainScheme", 1, effect)

        Worlds.UpdateNextCardPlayCost(
            joueur, -3, effect,
            finder=CardFinder(card_class="IdentitySpecific"),
            in_this="Round",
        )

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            triune_understanding,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
