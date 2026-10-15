from . import *

# Dard'van Fanatic (x2, 184) — SBIRE. SKRULL. MNG 2, ATQ 2, 4 PV, 2 icones Y.
# When Revealed: Choose to either deal 1 damage to each character you control or place 1 threat on each
#   scheme in play.
#
# Cartes de reference :
#  - « Choose to either A or B » : **`skrull_menace/lyja/sk039`** Faking Death (`player.ChooseAbilities(effect,
#    ForChoiceAbility(...), ForChoiceAbility(...))`) ;
#  - « 1 damage to each character you control » : **`gmw/menagerie_medley/16137`** (`this.DealDamage(
#    player.GetControlCharacters(), 1, effect)`) ; « 1 threat on each scheme in play » : **`sm/sinister_assault/
#    27158`** (`PlaceThreatOnSchemes("EachScheme", 1, effect)`, principal ET annexes).
#
# ⚠ Mots-pieges : « EITHER ... OR » (un seul des deux) ; « each character YOU CONTROL » (identite et allies du
# joueur qui revele, pas les ennemis) ; « each scheme IN PLAY » (complot principal compris, tous les complots
# annexes) ; « 1 threat » (pas par joueur).


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetToPlayer()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 1 damage to each character you control",
                lambda cibles: this.DealDamage(list(joueur.GetControlCharacters()), 1, effect),
            ),
            AbilityFactory.ForChoiceAbility(
                "Place 1 threat on each scheme in play",
                lambda cibles: this.PlaceThreatOnSchemes("EachScheme", 1, effect),
            ),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
