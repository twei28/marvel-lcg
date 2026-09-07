from . import *

# Vampire Bite — EVENEMENT, cout 1, [physical]. ATTACK. SUPERPOWER. x2.
# Hero Action (attack): Deal 2 damage to an enemy. Choose to either heal 2
#   damage from Blade or place 1 blood counter on him (do both instead if this
#   attack defeats that enemy).
#
# CARTES DE REFERENCE
#  - `bl003` / `01053` : l'attaque du heros par `DealDamage(...,
#    property=AttackProperty(...))`.
#  - `av008` : `this.HealthUnits([identite], n, effect)`.
#  - `23001a` : `Faces.PlaceCountersOn([identite], 1, 'blood', effect)`.
#  - `08013` / `ar001a` : deux branches par `ChooseAbilities` + `ForChoiceAbility`.
#
# TEXTE CONTRE CODE
#  ⚠ « your Vampire Bite attacks gain piercing » (Daywalker, bl009) est lu ICI :
#    `piercing=ControleDaywalker(...)` a la source de l'attaque. C'est
#    Daywalker qui parle de Vampire Bite, pas l'inverse, mais la propriete
#    d'une attaque se declare quand on la fait.
#  ⚠ « do BOTH instead if this attack DEFEATS that enemy » -> on lit l'etat de
#    la cible APRES les degats (`not IsInPlay()`) ; si elle est tombee, pas de
#    question, les deux effets partent.
#  ⚠ « heal 2 damage from BLADE » -> l'identite (forme heros de fait : Hero
#    Action). « place 1 blood counter on HIM » -> l'identite aussi.


def GetAbilities() -> Sequence['Ability']:

    def vampire_bite(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        heros = HerosDuJoueur(effect, joueur)
        if joueur is None or heros is None:
            return
        cibles = [c for c in effect.targets if c is not None and Enemy.IsType(c)]
        if not cibles:
            return
        percant = ControleDaywalker(effect, joueur)
        heros.DealDamage(cibles, 2, effect, property=AttackProperty(piercing=percant))

        vaincu = any(not c.IsInPlay() for c in cibles)

        def soigner(faces: Sequence['CardFace']) -> None:
            Unused(faces)
            this.HealthUnits([heros], 2, effect)

        def saigner(faces: Sequence['CardFace']) -> None:
            Unused(faces)
            Faces.PlaceCountersOn([heros], 1, COMPTEUR_SANG, effect)

        if vaincu:
            soigner([])
            saigner([])
            return

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Heal 2 damage from Blade", soigner),
            AbilityFactory.ForChoiceAbility("Place 1 blood counter on Blade", saigner),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            vampire_bite,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
