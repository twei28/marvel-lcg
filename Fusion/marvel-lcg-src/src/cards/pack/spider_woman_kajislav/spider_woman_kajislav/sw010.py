from . import *

# Hold 'Em Tight — EVENEMENT, cout X, RES [physical], x2. ATTACK. SUPERPOWER.
# Hero Action (attack): Deal X damage to an enemy. If that enemy was damaged
#   this way, stun it. Place 2 psionic web counters on Spider-Woman for each
#   [mental] resource you used to pay for this card (to a maximum of 10).
#
# ⚠ LA SEULE CARTE A COUT X DU PACK. Elle transforme tout le surplus de
# ressources en degats ET en etourdissement, et rend 2 compteurs par [mental]
# depense — c'est la carte de fin de partie du deck.
#
# CARTE DE REFERENCE
#  - `ht009` Radiate (pack human_torch) : `effect.GetCostX()`, le X REELLEMENT
#    paye. Ne jamais le recalculer depuis les ressources : un effet qui reduit
#    le cout changerait le compte.
#
# TEXTE CONTRE CODE
#  ⚠ « If that enemy WAS DAMAGED this way » : X vaut 0, ou l'ennemi est
#    Resistant, et rien n'est etourdi. On mesure donc les degats REELLEMENT
#    encaisses, pas le X demande.
#  ⚠ « 2 counters for each [mental] » : DEUX, comme `sw008`, pas un.


def GetAbilities() -> Sequence['Ability']:

    def serrer_fort(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        cibles = [c for c in effect.targets if c is not None]
        degats = effect.GetCostX()
        if cibles and degats > 0:
            avant = cibles[0].CastTo(Unit2).sustained
            this.DealDamage(cibles, degats, effect)
            if cibles[0].CastTo(Unit2).sustained > avant:
                Faces.GiveStatus(cibles, "Stunned", effect)
        PoserDesToiles(effect.GetInitiator(),
                       ToilesParRessourceMentale(effect, 2), effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            serrer_fort,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
