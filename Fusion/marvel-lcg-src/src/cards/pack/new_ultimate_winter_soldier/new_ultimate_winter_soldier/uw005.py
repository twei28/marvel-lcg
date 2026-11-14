from . import *

# Wild Slash — evenement signature, x2. ATTACK. Cout 0, [energy].
# Hero Action: Discard 1 card from your hand at random -> make the following attack up to X times, where X is equal to the
# numeral in the printed resource cost of that card:
#  • Take 1 damage -> deal 3 damage to an enemy.
#
# Cartes de reference : `35009` Slice and Dice (« Make the following 2 attacks » : `ChooseAbilities(ForChoiceAbility(..)
# .SetLabel('attack').SetTarget(Enemy))` + `this.AttackDamage`, AUCUN libelle sur l'evenement, comme ici) ; `35008`
# Berserker Barrage (`identite.TakeDamage(this, n, effect)` et `MayChooseOneAbility` pour un « may ») ; le cout au
# hasard : `CoutDefausseAuHasard()`.
#
# Mots-pieges : « up to X TIMES » (le joueur s'arrete quand il veut : `MayChooseOneAbility` offre « Cancel ») ; chaque
# attaque est une INSTANCE distincte : sa propre cible, son propre « take 1 damage » ; X = 0 (carte sans cout imprime) :
# aucune attaque ; plus d'ennemi en jeu : on s'arrete.


def GetAbilities() -> Sequence['Ability']:

    def wild_slash(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()

        def attaque(cibles: 'Sequence[CardFace]') -> None:
            joueur.GetIdentity().TakeDamage(this, 1, effect)
            this.AttackDamage(cibles, 3, effect)

        for _ in range(XDeLaCarteDefaussee(effect)):
            if not any(Enemy.IsType(f) for f in Worlds.GetOnFieldCards(effect)):
                return
            choix = joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Take 1 damage → deal 3 damage to an enemy",
                    attaque,
                ).SetLabel('attack')
                .SetTarget(Enemy),
            )
            if choix is None:
                return

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            wild_slash,
            conditions=[UneCarteADefausser],
        ).SetPlay()
        .SetCostFunc(CoutDefausseAuHasard()),
    ]
