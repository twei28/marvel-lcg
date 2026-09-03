from . import *

# Burst It! — evenement signature, x2. TACTIC. Cout 0, ressource [energy].
# Hero Action: Remove each metal counter from Spider Armor -> deal 1 damage to
#   each enemy in play for each metal counter removed this way.
#
# Cartes de reference :
#  - **`42018`** * Angel's Aerie : `CostFunc.RemoveEachCounter("This",
#    'fatigue')` puis
#    `effect.cost_func.Get(CostFunc.RemoveEachCounter).return_remove_counter`.
#    C'est le SEUL montage qui rend « for each counter removed **this way** »,
#    parce que le cout garde la trace de ce qu'il a reellement enleve.
#  - `01053` Relentless Assault / `hk006` pour l'evenement de degats de zone,
#    et `Worlds.GetOnFieldEnemies(effect)` pour « each enemy in play ».
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Remove each** metal counter -> » : la fleche en fait un COUT, et
#    c'est TOUT le stock, pas un nombre au choix. Sans compteur, la carte
#    n'est pas jouable : `RemoveEachCounter` filtre deja sur
#    `GetCounters(name) > 0`. LE RETRAIT VA DANS LE COUT.
#  - « for **each** metal counter removed **this way** » : le decompte porte
#    sur ce que le COUT a enleve, pas sur ce que l'armure portait avant.
#    Lire `return_remove_counter`, jamais `GetCounters` apres coup, qui
#    vaudrait 0.
#  - « 1 damage to **each enemy in play** » : tous les ennemis du terrain, y
#    compris les sbires engages avec un AUTRE joueur, et pas seulement ceux
#    engages avec vous. Pas de restriction imprimee.
#  - « **Hero Action** » sans libelle (attack) : la carte n'est PAS une
#    attaque, elle ne subit donc pas Sonne et ne declenche pas Riposte.
#    Aucun `SetLabel`.
#  - ⚠ CONSEQUENCE DE JEU : vider l'armure retourne forcement as002a sur
#    as002b DESTROYED. Burst It! coute 0 ressource, mais 1 ATQ et 1 DEF
#    jusqu'a reparation.


def GetAbilities() -> Sequence['Ability']:

    def burst_it(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        retires = effect.cost_func.Get(CostFunc.RemoveEachCounter).return_remove_counter
        if retires <= 0:
            return

        ennemis = Worlds.GetOnFieldEnemies(effect)
        if ennemis:
            this.DealDamage(list(ennemis), retires, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            burst_it,
        ).SetPlay()
        .SetCostFunc(CostFunc.RemoveEachCounter(ArmureCible, 'metal')),
    ]
