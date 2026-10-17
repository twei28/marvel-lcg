from . import *

# Down the Drain — EVENEMENT Leadership (TMNT Aspects, Inkwire), cout 1*, [mental]. FERAL. NYC.
# [star] Rampage 2. (As an additional cost for this card, take 2 damage and discard 2 cards from the top
#   of your deck.)
# Hero Action: Discard an ally you control -> deal 2 damage to an enemy, remove 2 threat from a scheme,
#   and draw 2 cards.
#
# MOT-CLE (fiche lue AVANT le code) : RAMPAGE X — docs/reference/mots-cles/rampage.md.
#   `CostFunc.Rampage(2)` sur la capacite de JEU ; le « 1* » du cout et le [star] ne sont qu'un rappel.
#
# CARTES DE REFERENCE
#  - `ua015` Demolish : `WhenInYourPlayTurn(HeroAction).SetPlay().SetCostFunc(CostFunc.Rampage(X))`.
#  - `49018` Noble Sacrifice : « Discard an ally you control -> » = `CostFunc.Discard("YourAlly")`.
#  - `61027` Unbreakable Bond : une seconde cible (manigance) = `.SetTarget2(Scheme2, range=(1, 1))`.
#
# TEXTE CONTRE CODE
#  ⚠ « Discard an ally YOU CONTROL » est DEVANT la fleche : un COUT, comme Rampage. Sans allie a
#    defausser, la carte n'est pas jouable (et Rampage n'est donc pas paye).
#  ⚠ Trois effets, tous resolus : 2 degats a UN ennemi (vilain ou sbire), 2 menaces retirees d'UNE
#    manigance (principale ou annexe), 2 cartes piochees par le joueur qui joue la carte.
#  ⚠ Pas d'etiquette (attack)/(thwart) imprimee : ni attaque ni contre.
#  Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def down_the_drain(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.DealDamage(effect.targets, 2, effect)
        this.RemoveThreatFromSchemes(effect.targets2, 2, effect)
        joueur = effect.GetInitiator()
        joueur.DrawUp(2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            down_the_drain,
        ).SetPlay().SetLabel()
        .SetCostFunc(CostFunc.Rampage(2))
        .SetCostFunc(CostFunc.Discard("YourAlly"))
        .SetTarget(Enemy)
        .SetTarget2(Scheme2, range=(1, 1)),
    ]
