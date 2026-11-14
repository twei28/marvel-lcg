from . import *

# Starformation — TRAITRISE (Starforce). 1 icone de boost.
# When Revealed: Give each STARFORCE minion a tough status card and a facedown boost card. Otherwise, give the
#   villain a tough status card and a facedown boost card.
#
# Cartes de reference :
#  - **`ares/ar014`** Lead the Charge : « give each minion a facedown boost card »
#    (`Faces.GiveFacedownBoostCards(sbires, 1, effect)`) ; **`next_evol/40156`** : `Faces.GiveStatus(...,
#    "Tough", effect)`.
#  - « Otherwise » = aucun sbire STARFORCE EN JEU (RECETTES §2 : la branche alternative de « each » vide).
#
# ⚠ Mots-pieges : « EACH STARFORCE minion » (en jeu ; les mis de cote ne sont pas « en jeu ») ; « a tough status
# card AND a facedown boost card » (les deux, a chacun) ; « Otherwise » (aucun sbire STARFORCE en jeu) ->
# le MECHANT recoit les deux ; un sbire deja Tenace ne recoit pas de seconde carte Tenace (plafond natif) mais
# recoit sa carte de boost.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        sbires = [f for f in Worlds.GetOnFieldCards(effect)
                  if Minion.IsType(f) and f.IsInPlay() and f.HasTrait("STARFORCE")]
        if not sbires:
            mechant = Worlds.FindVillain(effect)
            sbires = [mechant] if mechant is not None else []
        if sbires:
            Faces.GiveStatus(sbires, "Tough", effect)
            Faces.GiveFacedownBoostCards(sbires, 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
