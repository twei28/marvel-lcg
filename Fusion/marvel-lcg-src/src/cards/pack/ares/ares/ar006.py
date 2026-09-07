from . import *

# Feint — AMELIORATION, cout 0, [physical]. PREPARATION. TACTIC. x3.
# Attach to an enemy. Max 1 per enemy.
# Forced Hero Interrupt (attack/defense): When attached enemy initiates an
#   attack, discard Feint -> that enemy gets -2 ATK for that attack. Deal 2
#   damage to that enemy.
#
# BRIQUE 6 : une amelioration JOUEUR attachee a un ENNEMI (modeles `bk009`
# Portal, `yd012` Yaka Arrow, `sf009` Burning).
#
# CARTES DE REFERENCE
#  - `bk009` Portal : `CanPlayThisUpgradeCard(CardFinder(card_type=Enemy))`
#    pour « Attach to an enemy ».
#  - `02020` Hysteria : `WhenUnitWouldAttack(ForcedInterrupt, <ennemi>, op)`,
#    la fenetre « when attached enemy initiates an attack ».
#  - `19018` Subdue : `message.GainATKForThisAttack(-n, effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « Max 1 per enemy » -> `desc.MaxPerUnit = "1"`, lu par le moteur
#    (has_max_per.py), aucun code. Athena (ar012) refuse en plus toute
#    amelioration TACTIC, par sa propre regle.
#  ⚠ « FORCED HERO Interrupt » -> `AbilityType.ForcedInterruptHero` : forcee,
#    et seulement en forme heros. ⚠ LE MOTEUR NE POSE PAS CETTE RESTRICTION
#    LUI-MEME : `ForcedInterruptHero` n'a pas `is_hero_type` (ability_type.py,
#    contrairement a HeroInterrupt/HeroResponse), et la carte partait en forme
#    civile — vu par le contre-cas du 07/09/2026. D'ou la condition
#    `en_forme_heros`. En forme civile, la feinte reste posee et ne part pas.
#  ⚠ « (attack/defense) » : les libelles ne sont PAS poses. `check_sub_type`
#    (ability.py:169) n'accepte aucun libelle sur `ForcedInterruptHero` (le
#    type tombe sur `elif self.is_play`) : `SetLabel` ferait tomber LE MONTAGE
#    DU DECK (lecon ls005, RECETTES §4bis). L'ecart est cosmetique : un
#    libelle sert au moteur pour Sonne/Desoriente sur des capacites du joueur
#    ; une interruption forcee sur l'attaque d'un ennemi n'en a pas l'usage.
#  ⚠ « When ATTACHED enemy initiates an attack » -> `conditions=[est_mon_hote]`
#    sur `message.trigger`, l'attaquant. Un autre ennemi ne declenche rien.
#  ⚠ « discard Feint → -2 ATK ... Deal 2 damage » -> le malus et les degats
#    sont appliques AVANT la defausse, pour que `this.DealDamage` parte d'une
#    carte encore en jeu. L'ordre ne change rien pour le joueur.
#  ⚠ « -2 ATK for THAT attack » : temporaire, sur le message d'attaque, jamais
#    sur la carte.


def GetAbilities() -> Sequence['Ability']:

    def est_mon_hote(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        hote = Hote(effect.this)
        return hote is not None and getattr(message, "trigger", None) is hote

    def en_forme_heros(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        Unused(message)
        return HerosDuJoueur(effect) is not None

    def feinter(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        hote = Hote(this)
        message.GainATKForThisAttack(-2, effect)
        if hote is not None and Enemy.IsType(hote):
            this.DealDamage([hote], 2, effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Enemy)),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterruptHero,
            Enemy,
            feinter,
            conditions=[en_forme_heros, est_mon_hote],
        ),
    ]
