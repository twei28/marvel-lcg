from . import *

# * Powder Keg (manigance joueur Linked)

def GetAbilities() -> Sequence['Ability']:

    def hors_limite(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        for face in effect.this.card.printed_faces:
            face.not_count_player_side_scheme_limit = True

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this
        joueur = JoueurVainqueur(message, effect)
        for ennemi in Worlds.GetOnFieldEnemies(effect):
            degats = 4 if (ennemi.IsStunned() or ennemi.IsConfused()) else 2
            this.DealDamage([ennemi], degats, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(AbilityType.Temp0, "This", hors_limite),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
