from . import *

# Nendō — EVENEMENT DUAL Bushido/Kuji-Kiri, cout 2, [physical]. ATTACK. PSIONIC.
# Classe : « Bushido;Kuji-Kiri » (compte pour LES DEUX types, livret p.7).
# Hero Action (attack): Exhaust a WEAPON upgrade you control -> deal 4 damage to an enemy. Daze that enemy.
#
# Mots-cles (fiches lues AVANT le code) : Daze (dazed.md) ; Shinobi (shinobi.md).
#
# Cartes de reference :
#  - cout « Exhaust a <trait> upgrade you control » : `tmnt_aspect_*/td005` Improvised Tactics
#    (`CostFunc.Exhaust(card_type=Upgrade, trait=..., from_where=["YouControlCards"])`, `SetPlay()`) ;
#  - Hero Action (attack) a 1 cible, degats puis statut : `jennika/tj004` Decisive Strike (`SetPlay().SetLabel('attack')
#    .SetTarget(Enemy)`, `Faces.GiveStatus` apres `DealDamage`) ;
#  - daze : helper partage `ShinobiDaze` (tx016 Wrapped Up : `Faces.GiveStatus(..., "Dazed", ...)`).
#
# TEXTE CONTRE CODE
#  ⚠ « Exhaust a WEAPON upgrade YOU CONTROL » est DEVANT la fleche : un COUT (l'amelioration s'incline, elle n'est pas
#    defaussee) ; sans amelioration WEAPON redressee sous son controle, la carte n'est pas jouable.
#  ⚠ « deal 4 damage to AN enemy » PUIS « Daze THAT enemy » : le meme ennemi, apres les degats (un ennemi vaincu n'est plus
#    hebete) ; vilain ou sbire.
#  ⚠ « Hero Action (attack) » : forme heros, libelle `attack` (alimente Sonne/Desoriente).


def GetAbilities() -> Sequence['Ability']:

    def nendo(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.DealDamage(effect.targets, 4, effect)
        ShinobiDaze(effect, [e for e in effect.targets if not e.IsDefeated()])

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            nendo,
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust(
            card_type=Upgrade,
            trait="WEAPON",
            from_where=["YouControlCards"],
        ))
        .SetTarget(Enemy),
    ]
