from . import *

# Civilian (face VISIBLE, `a`) : AMELIORATION (CONDITION. SUPERPOWER.) PERMANENTE, forme metamorphe. Sans cout.
# Shapeshift Form. Permanent.
# Action: Exhaust Civilian -> remove 1 threat from a scheme.
# Forced Response: When this card is turned faceup, flip each other shapeshift form upgrade facedown.
#
# CARTES DE REFERENCE
#  - `26002b` Dense (vision) : amelioration a deux faces qui reagit au changement de forme ; `hf041` / `state.py` : `AfterCardFlipToThisSide` pour « when THIS card is turned faceup ».
#  - `01037` Mark V Helmet : `this.RemoveThreatFromSchemes(effect.targets, n, effect)` + `.SetTarget(Scheme2)` (cible de manigance). `Faces.ReadyAll` / `CostFunc.Exhaust("This")` (`my002`).
#
# TEXTE CONTRE CODE
#  « Exhaust Civilian » : cout de l'Action (inclinaison de CETTE carte). « WHEN THIS CARD IS TURNED FACEUP » : le retournement de b vers a, pas la mise en jeu (la forme entre en jeu face cachee). « flip EACH OTHER form
#    FACEDOWN » : les deux autres formes visibles passent face cachee (celles deja cachees ne bougent pas) ; la forme qui vient d'etre retournee reste visible. Face cachee (`b`) : aucune capacite.
#  Chiffres : aucun cout, aucun nombre hors « 1 threat, 1 scheme ».


def GetAbilities() -> Sequence['Ability']:

    def retirer_menace(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        effect.this.RemoveThreatFromSchemes(effect.targets, 1, effect)

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
            retirer_menace,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Scheme2),
        AbilityFactory.AfterCardFlipToThisSide(
            AbilityType.ForcedResponse,
            retourner_les_autres,
        ),
    ]
