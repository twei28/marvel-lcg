from . import *

# Demolish — EVENEMENT 3* [physical], aspect Aggression (TMNT Aspects, Inkwire). ATTACK. FERAL. NYC.
# [star] Rampage 3. (As an additional cost for this card, take 3 damage and discard 3 cards from the
#   top of your deck.)
# Hero Action (attack): Deal 8 damage to an enemy. If you control a [[NYC]] support, this attack gains
#   overkill and piercing.
#
# MOT-CLE (fiche lue AVANT le code) : RAMPAGE X — docs/reference/mots-cles/rampage.md. Cout additionnel
# du moteur `CostFunc.Rampage(3)` (cost_func.py). Le « 3* » du cout et le [star] devant Rampage ne
# sont qu'un RAPPEL (Rules Reference v1.8, « Star Icon ») : aucune ligne de code.
# Mots-cles cites dans l'effet : overkill / piercing (fiches overkill.md, piercing.md), portes par
# `AttackProperty`.
#
# CARTES DE REFERENCE
#  - `nt006` Melon Grab : « Deal 8 damage to an enemy », puis « this attack gains piercing and
#    overkill » sous condition = `this.DealDamage(..., property=AttackProperty(piercing=True,
#    overkill=True))` ; evenement d'attaque `.SetPlay().SetLabel('attack').SetTarget(Enemy)`.
#  - `36007` Storm's Cape / `27011` : un SOUTIEN a trait controle = `CardFinder2("<TRAIT>", Support)`,
#    lu par `joueur.IsControl(...)` (player_get.py).
#  - `tr011` / `hulk_rainy 90107` : un cout « take N damage » = `CostFunc.TakeDamage(N,
#    "YourIdentity")`, que `CostFunc.Rampage` compose avec `CostFunc.DiscardDeckTopCards`.
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « As an additional cost » : se paie AVEC la carte ; un cout impaye (degats empeches par un Tough)
#    annule TOUT l'effet — c'est le moteur qui le fait, `ProcessSelfCost` rend False.
#  ⚠ « take 3 damage » : l'IDENTITE du joueur (heros ici, l'action est une Hero Action).
#  ⚠ « discard 3 cards from the top of YOUR deck » : le deck du joueur, pas celui de rencontre.
#  ⚠ « an enemy » : vilain OU sbire.
#  ⚠ « If you control a NYC SUPPORT » : un soutien (pas une amelioration, pas un allie) au trait NYC,
#    sous le controle du joueur qui joue la carte. Lu AU MOMENT de l'attaque.
#  ⚠ « overkill AND piercing » : les deux, ou aucun.
#  Aucune limite imprimee.


def ControleUnSoutienNYC(effect: 'Effect') -> bool:
    joueur = effect.GetInitiator()
    return joueur is not None and joueur.IsControl(CardFinder2("NYC", Support))


def GetAbilities() -> Sequence['Ability']:

    def demolish(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        if ControleUnSoutienNYC(effect):
            this.DealDamage(effect.targets, 8, effect,
                            property=AttackProperty(overkill=True, piercing=True))
        else:
            this.DealDamage(effect.targets, 8, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            demolish,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy)
        .SetCostFunc(CostFunc.Rampage(3)),
    ]
