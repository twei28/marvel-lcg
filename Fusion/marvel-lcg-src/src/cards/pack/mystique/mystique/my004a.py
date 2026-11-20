from . import *

# Enemy (face VISIBLE, `a`) : AMELIORATION (CONDITION. SUPERPOWER.) PERMANENTE, forme metamorphe. Sans cout.
# Shapeshift Form. Permanent.
# Action: Exhaust Enemy -> deal 1 damage to an enemy.
# Forced Response: When this card is turned faceup, flip each other shapeshift form upgrade facedown.
#
# CARTES DE REFERENCE
#  - `26002b` Dense (vision) : amelioration a deux faces qui reagit au changement de forme ; `hf041` / `state.py` : `AfterCardFlipToThisSide` pour « when THIS card is turned faceup ».
#  - `27182a` Compact Darts : `this.DealDamage(effect.targets, 1, effect)` + `.SetTarget(Enemy)`.
#
# TEXTE CONTRE CODE
#  « Exhaust Enemy » : cout de l'Action (inclinaison de CETTE carte). « WHEN THIS CARD IS TURNED FACEUP » : le retournement de b vers a, pas la mise en jeu (la forme entre en jeu face cachee). « flip EACH OTHER form
#    FACEDOWN » : les deux autres formes visibles passent face cachee (celles deja cachees ne bougent pas) ; la forme qui vient d'etre retournee reste visible. Face cachee (`b`) : aucune capacite.
#  Chiffres : aucun cout, aucun nombre hors « 1 damage, 1 enemy ».


def GetAbilities() -> Sequence['Ability']:

    def infliger_degat(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        effect.this.DealDamage(effect.targets, 1, effect)

    def retourner_les_autres(effect: 'Effect', message: 'Message.AfterCardFlip') -> None:
        Unused(message)
        this = effect.this
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        for forme in Formes(joueur):
            if forme.card is not this.card and EstVisible(forme):
                RetournerCachee(forme, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            infliger_degat,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Enemy),
        AbilityFactory.AfterCardFlipToThisSide(
            AbilityType.ForcedResponse,
            retourner_les_autres,
        ),
    ]
