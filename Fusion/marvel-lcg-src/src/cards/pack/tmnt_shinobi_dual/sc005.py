from . import *

# Yoi-Dachi — AMELIORATION DUALE Bushido/Taijutsu, cout 2, [energy]. OATH. STANCE.
# Classe : « Bushido;Taijutsu ».
# Max 1 per player. Uses (3 samurai counters).
# Response: After you take damage from an enemy attack, remove 1 samurai counter from here -> daze that enemy.
#
# Mots-cles (fiches lues AVANT le code) : Uses (uses.md) ; samurai counter / OATH (samurai-counter.md) ; Daze (dazed.md) ;
# Max N per player (base native `desc.MaxPerUnit`).
#
# Cartes de reference :
#  - declencheur « After you take damage from an enemy attack » : `bkw/08030` Counterattack
#    (`AfterUnitTookDamage(..., "You", fn, is_from_attack=True, who_dealt_damage=Enemy)`, cible `"Attacker"`) ;
#  - cout « remove N counters from here » : `jennika/tj006` (`CostFunc.Counter("This", n, 'samurai')`) ;
#  - daze : `ShinobiDaze` (helper partage).
#
# TEXTE CONTRE CODE
#  ⚠ « After YOU take damage FROM AN ENEMY ATTACK » : le joueur (identite : heros OU alter-ego) subit au moins 1 degat d'une
#    attaque d'ennemi ; une attaque entierement defendue, un degat hors attaque, ou le degat subi par un ALLIE ne declenchent
#    rien. « Response » (et non « Hero Response ») : les deux formes.
#  ⚠ « daze THAT enemy » : l'ennemi qui a attaque (`"Attacker"`), pas un ennemi au choix ; un ennemi deja hebete n'en recoit
#    pas une seconde.
#  ⚠ « remove 1 samurai counter FROM HERE » : cout (devant la fleche), sur CETTE carte ; au 3e usage la carte quitte le jeu
#    (Uses). Aucune inclinaison imprimee, aucune limite par round : une Response par attaque tant qu'il reste des compteurs.


def GetAbilities() -> Sequence['Ability']:

    def yoi_dachi(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        ShinobiDaze(effect, [e for e in effect.targets if not e.IsDefeated()])

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.Response,
            "You",
            yoi_dachi,
            is_from_attack=True,
            who_dealt_damage=Enemy,
        ).SetCostFunc(CostFunc.Counter("This", 1, 'samurai'))
        .SetTarget("Attacker"),
    ]
