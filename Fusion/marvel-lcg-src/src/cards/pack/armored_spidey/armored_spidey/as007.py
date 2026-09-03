from . import *

# Sell It! — evenement signature, x1. SKILL. Cout 2, ressource [mental].
# Alter-Ego Action: Remove any number of metal counters from Spider Armor. For
#   each metal counter removed this way, draw 2 cards.
#
# Cartes de reference :
#  - **`CostFunc.Counter(cible, (min, max), 'metal')`** (cost_func.py:792) :
#    la forme TUPLE appelle `player.DeclareNumber(min, max)` et plafonne
#    d'elle-meme au stock reel. C'est exactement « any number », et c'est le
#    seul montage qui garde ensuite la trace de ce qui a ete retire
#    (`return_remove_counter`), comme `42018` * Angel's Aerie pour
#    `RemoveEachCounter`.
#  - `bt023` / `an001b` pour `initiator.DrawUp(n, effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « for each metal counter removed **this way** » : le decompte porte sur
#    ce qui vient d'etre retire, pas sur ce que l'armure portait. Lire
#    `return_remove_counter`, jamais `GetCounters` apres coup, qui aurait
#    deja baisse.
#  - « draw **2** cards » PAR compteur, pas 1. Trois compteurs = 6 cartes.
#  - « **Alter-Ego** Action » : rien en forme heros. La carte demande donc de
#    ranger le costume pour vider l'armure, ce qui la laisse DESTROYED au
#    reveil — as002b coute alors 3 ressources, ou as003 Spider-Bot.
#  - ⚠ ECART ASSUME, arbitrage technique (§9 du GUIDE, pas une question de
#    regles) : « any number » inclut litteralement ZERO, mais le retrait est
#    monte en COUT avec un minimum de 1. Consequence : la carte n'est pas
#    jouable quand l'armure est vide, au lieu d'etre jouable pour ne rien
#    faire. Choix delibere — la forme « jouable pour rien » est exactement le
#    motif qui a bloque une partie sur 32 en autoplay au pack
#    iron_man_model_42, et aucun joueur ne paierait 2 ressources pour piocher
#    0 carte.


def GetAbilities() -> Sequence['Ability']:

    def sell_it(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        retires = effect.cost_func.Get(CostFunc.Counter).return_remove_counter
        if retires <= 0:
            return

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        initiator.DrawUp(retires * 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            sell_it,
        ).SetPlay()
        .SetCostFunc(CostFunc.Counter(ArmureCible, (1, MAX_METAL), 'metal')),
    ]
