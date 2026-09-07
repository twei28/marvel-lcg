from . import *

# Go for the Heart — EVENEMENT, cout 2, [physical]. ATTACK. TACTIC. x3.
# Hero Action (attack): Deal 4 damage to an enemy. This attack gains piercing.
#   You may exhaust a WEAPON upgrade you control to stun that enemy.
#
# CARTES DE REFERENCE
#  - `01053` Relentless Assault / `ar002` : `hero.DealDamage(cibles, n, effect,
#    property=AttackProperty(...))`, une vraie ATTAQUE du heros.
#  - `AttackProperty.piercing` (can_attack.py:10) : « this attack gains
#    piercing » se declare a la source.
#  - `al023` / `an010` : `Faces.GiveStatus([cible], "Stunned", effect)`.
#  - `ar003` : une option facultative par `ChooseAbilities(..., forced=False)`
#    avec `SetTarget(CardFinder(...), from_where=["YouControlCards"],
#    canbe_exhaust=True)`.
#
# TEXTE CONTRE CODE
#  ⚠ « This attack gains piercing » -> Blade's Sword (+1) et le doublement du
#    set nemesis s'appliquent : 4 + 1 = 5, puis x2 sur un Vampire = 10
#    (arbitrage du 07/09 : bonus puis doublement).
#  ⚠ « You MAY exhaust a WEAPON upgrade » -> facultatif, `forced=False`. Pas
#    propose si aucune arme prete, ni si l'ennemi est deja vaincu.
#  ⚠ « stun THAT enemy » -> la cible de l'attaque, pas au choix.


def GetAbilities() -> Sequence['Ability']:

    def go_for_the_heart(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        heros = HerosDuJoueur(effect, joueur)
        if joueur is None or heros is None:
            return
        cibles = [c for c in effect.targets if c is not None and Enemy.IsType(c)]
        if not cibles:
            return
        heros.DealDamage(cibles, 4, effect, property=AttackProperty(piercing=True))

        vivantes = [c for c in cibles if c.IsInPlay()]
        if not vivantes or not ArmesPretes(joueur):
            return

        def empaler(armes: Sequence['CardFace']) -> None:
            outils = [a for a in armes if a is not None]
            if not outils:
                return
            Faces.ExhaustAll(outils, effect)
            Faces.GiveStatus(vivantes, "Stunned", effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust a WEAPON upgrade you control to stun that enemy",
                empaler,
            ).SetTarget(CardFinder(card_type=Upgrade, trait=TRAIT_WEAPON),
                        from_where=["YouControlCards"], canbe_exhaust=True),
            forced=False,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            go_for_the_heart,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
