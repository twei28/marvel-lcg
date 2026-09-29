from . import *

# Melee

def GetAbilities() -> Sequence['Ability']:

    def melee(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        this.DealDamage(effect.targets, 3, effect)

        initiator = effect.GetInitiator()
        faces = Worlds.GetOnFieldEnemies(effect)
        # FAQ (MC4DB, 29/09/2026) : la 2e phrase est une cible d'ATTAQUE comme
        # la 1re. Le vilain n'y est ciblable que si le sbire guard est tombe a
        # la 1re phrase (`Villain.CanBeAttackBy` : guard engage -> refus) ; un
        # ennemi deja vaincu n'est plus propose non plus.
        faces = [x for x in faces
                 if x not in effect.targets and x.IsInPlay() and x.CanBeAttackBy(effect)]
        unit = initiator.AskChooseFace(faces, effect)
        if unit:
            this.DealDamage([unit], 3, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            melee
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy)
        # Melee is one attack with two separate targets. You resolve the damage separately, but it is still a single attack. That means that if you are stunned, playing Melee will only remove the stunned status card and nothing else.
        # When you play Melee, you are treated as having made **a single attack** (with multiple instances of damage); this should help provide context for my answers to your specific questions below.
    ]

