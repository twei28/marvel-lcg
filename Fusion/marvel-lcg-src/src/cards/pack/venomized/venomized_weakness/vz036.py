from . import *

# Flash Fire — TRAITRISE du set « Venomized Weakness » (1/2).
# Weakness. (Begins the game in your deck and is discarded into your discard
#   pile.)
# Forced Response: After this card enters your hand, take 1 indirect damage.
#   (You may discard this card from your hand at the end of the player phase
#   like any other card.)
#
# MOT-CLE
#  - `weakness` : mot-cle MAISON de l'aspect Venomized. Fiche complete dans
#    `docs/reference/mots-cles/weakness.md`, ecrite avant ce module. En deux
#    mots : la carte est une carte de RENCONTRE qui vit dans le DECK DU
#    JOUEUR, ne compte pas dans la taille du deck, et part dans la defausse DU
#    JOUEUR. RIEN DE TOUT CELA N'EST CODE ICI — le placement est une regle de
#    construction de deck, le reste est le comportement natif d'une carte du
#    deck joueur.
#
# CARTE DE REFERENCE
#  - `bk002` * Sabretooth (pack blink) : « After Sabretooth enters your hand,
#    ... ». Le SEUL declencheur du depot sur cette fenetre, et il prouve que
#    `AfterCardEnterHand` fonctionne depuis la main.
#  - `al022` (pack alligator_loki) : `identite.TakeIndirectDamage(this, 1,
#    effect)`, l'indirect sur une Reponse forcee.
#
# TEXTE CONTRE CODE
#  ⚠ « enters your HAND » et non « after you draw » : une carte rendue en main
#    par un autre effet declenche aussi. C'est la lecon de `bk002`.
#  ⚠ `which_card="This"` pose `CanWorkOnlyInHand()` TOUT SEUL
#    (`card_move.py`) : ne pas le rajouter, la capacite serait branchee deux
#    fois.
#  ⚠ « Forced Response » : la joueuse ne peut pas refuser -> `ForcedResponse`.
#  ⚠ La parenthese « You may discard this card ... like any other card » ne se
#    code PAS : c'est deja ce que fait n'importe quelle carte en main a la fin
#    de la phase du joueur. La rappeler serait ajouter une regle en double.
def GetAbilities() -> Sequence['Ability']:

    def flash_fire(effect: 'Effect', message: 'Message.AfterCardEnterHand') -> None:
        this = effect.this
        Unused(message)

        joueur = this.GetControlByOrOwner()
        if not Player.IsType(joueur):
            return
        joueur.GetIdentity().TakeIndirectDamage(this, 1, effect)

    return [
        AbilityFactory.AfterCardEnterHand(
            AbilityType.ForcedResponse,
            "This",
            flash_fire,
        ),
    ]
