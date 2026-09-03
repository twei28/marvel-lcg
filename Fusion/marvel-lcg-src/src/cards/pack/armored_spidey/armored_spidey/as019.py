from . import *

# * The Daily Bugle — soutien d'aspect PROTECTION, x1. LOCATION. Cout 2,
# ressource [mental].
# Response: After a character or a side scheme is defeated, exhaust The Daily
#   Bugle -> place 1 article counter here.
# Alter-Ego Action: Remove each article counter from here -> heal 1 damage
#   from a character you control for each article counter removed this way.
#
# Cartes de reference :
#  - **`42018`** * Angel's Aerie : la SECONDE capacite y est mot pour mot —
#    `CostFunc.RemoveEachCounter("This", <compteur>)` puis
#    `effect.cost_func.Get(CostFunc.RemoveEachCounter).return_remove_counter`
#    et `this.HealthUnits(cibles, valeur, effect)`, avec
#    `SetTarget(..., canbe_heal=True)`.
#  - `ok014` / `08031` pour `AfterUnitBeDefeated(Response, <qui>, op)` et
#    `bt004` / `60015` pour `AfterSchemeBeDefeated(Response, SchemeSide2, op)`.
#  - `17022` * Knowhere pour `CostFunc.Exhaust("This")` sur un soutien.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « a character **or** a side scheme » : DEUX declencheurs distincts, donc
#    DEUX capacites. Un seul `Ability` ne peut pas ecouter deux messages.
#  - « a **character** » : heros, alter-ego ou allie — de N'IMPORTE QUEL
#    camp, et sans restriction « you control ». Un sbire n'est pas un
#    personnage au sens du jeu ; le vilain non plus. Le filtre est donc sur
#    les unites de type personnage, pas sur `Enemy`.
#  - « a **side** scheme » : `SchemeSide2` (les annexes de rencontre ET de
#    joueur), jamais le complot principal. ⚠ `SideScheme` N'EXISTE PAS dans
#    `cards.pack`, la classe est `SchemeSide2`.
#  - « **exhaust** The Daily Bugle -> » : la fleche en fait un cout ; le
#    soutien deja incline ne declenche rien, une seule fois par tour de
#    redressement.
#  - « heal 1 damage from a character **you control** » : celui-la est bien
#    restreint, contrairement au declencheur. `from_where=["YouControlCards"]`.
#  - « for **each** article counter removed **this way** » : le decompte
#    porte sur ce que le COUT a enleve, pas sur ce que la carte portait.
#  - ⚠ « **a** character » au singulier : les soins vont a UN SEUL
#    personnage, pas repartis. Un compteur = 1 PV rendu a cette cible.


def GetAbilities() -> Sequence['Ability']:

    def article(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        Faces.PlaceCountersOn([this], 1, 'article', effect)

    def daily_bugle(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        retires = effect.cost_func.Get(CostFunc.RemoveEachCounter).return_remove_counter
        if retires <= 0:
            return
        this.HealthUnits(effect.targets, retires, effect)

    return [
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.Response,
            CardFinder(card_type=Unit2),
            article,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.AfterSchemeBeDefeated(
            AbilityType.Response,
            SchemeSide2,
            article,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            daily_bugle,
        ).SetCostFunc(CostFunc.RemoveEachCounter("This", 'article'))
        .SetTarget(CardFinder(card_type=Unit2), from_where=["YouControlCards"], canbe_heal=True),
    ]
