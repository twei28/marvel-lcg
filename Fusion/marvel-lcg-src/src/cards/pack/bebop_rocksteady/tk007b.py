from . import *

# Headfirst (Temper de Bebop, face ENRAGED)

def GetAbilities() -> Sequence['Ability']:

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this
        # « your identity » : le joueur qui resout le Special (tranche par l'utilisateur
        # le 16/10/2026, Q1 : celui qui a blesse Bebop, a defaut le premier joueur).
        joueur = message.GetToPlayer() or Worlds.GetFirstPlayer(effect)
        this.DealDamage([joueur.GetIdentity()], 1, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(Villain, trait="ENRAGED"),
        AbilityFactory.WhenResolveSpecialAbility("This", special),
        *TempersEnrages("Bebop"),
    ]
