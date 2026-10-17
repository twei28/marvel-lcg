from . import *

# Kenbu — EVENEMENT DUAL Ninjutsu/Taijutsu, cout 2, [mental]. ATTACK.
# Classe : « Ninjutsu;Taijutsu ».
# Hero Action (attack): Discard a cloaked status card from your hero -> deal 1 damage to up to 3 enemies. Daze each enemy
#   damaged this way.
#
# Mots-cles (fiches lues AVANT le code) : Cloaked (cloaked.md) ; Daze (dazed.md) ; Shinobi (shinobi.md).
#
# Cartes de reference :
#  - « Discard a <statut> status card from X and choose up to N enemies -> deal N damage to each » : `skrull_menace/lyja/sk049`
#    The Thing (`CostFunc.Custom(CardFinder(..., with_tough=True), defausser)`, `SetTarget(Enemy, range=(0, N))`,
#    `DealDamage(effect.targets, ...)`) ; ici le statut est Cloaked : `has_status="Cloaked"` et `DiscardCloaked(effect, rule=1)` ;
#  - Hero Action (attack) sur un evenement : `jennika/tj004` (`SetPlay().SetLabel('attack')`) ;
#  - daze : `ShinobiDaze`.
#
# TEXTE CONTRE CODE
#  ⚠ « Discard a CLOAKED status card FROM YOUR HERO » : COUT (devant la fleche), UNE carte Cloaked retiree du HEROS (forme
#    heros) ; sans Cloaked sur le heros la carte n'est pas jouable. Le heros perd ainsi son camouflage (Cloaked ne sert pas).
#  ⚠ « deal 1 damage TO UP TO 3 enemies » : de 0 a 3 ennemis, 1 degat A CHACUN (pas 1 au total) ; vilain ou sbires.
#  ⚠ « Daze EACH enemy DAMAGED THIS WAY » : seulement ceux qui ont reellement perdu des PV (un ennemi protege par Tenace n'est
#    pas « damaged » : pas de daze ; un sbire vaincu n'est plus hebete). Un ennemi deja hebete n'en recoit pas une seconde.
#  ⚠ « Hero Action (attack) » : forme heros, libelle `attack`.


def GetAbilities() -> Sequence['Ability']:

    def defausser_un_cloaked_du_heros(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        return bool(targets) and targets[0].DiscardCloaked(effect, rule=1) > 0

    def kenbu(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        cibles = list(effect.targets)
        avant = {e: e.health for e in cibles}
        this.DealDamage(cibles, 1, effect)
        blesses = [e for e in cibles if not e.IsDefeated() and e.health < avant[e]]
        ShinobiDaze(effect, blesses)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            kenbu,
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Custom(
            Select.From("YourHero", finder=CardFinder(has_status="Cloaked")),
            defausser_un_cloaked_du_heros,
        ))
        .SetTarget(Enemy, range=(0, 3)),
    ]
