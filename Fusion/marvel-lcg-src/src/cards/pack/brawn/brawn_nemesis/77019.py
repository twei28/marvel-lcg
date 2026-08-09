from . import *

# Rising Tide (manigance secondaire nemesis) — custom « Rainy »
# Hinder 2[per_hero].
# When Revealed: Place 1 acceleration token here.
# Forced Interrupt: When the villain phase begins, place 1 acceleration token
#   here.
#
# Le compteur monte donc d'au moins 1 par round, et chaque jeton nourrit deux
# choses a la fois : l'escalade du complot principal (regle generale des jetons
# d'acceleration) et les statistiques de Namor 77020, qui gagne +X ATK et
# +X SCH pour X jetons en jeu. Laisser vivre Rising Tide coute cher deux fois.

def GetAbilities() -> Sequence['Ability']:

    def a_la_revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        this.PlaceAccelerationToken(1, effect)

    def au_debut_de_la_phase_du_vilain(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        this.PlaceAccelerationToken(1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            a_la_revelation,
        ),

        AbilityFactory.WhenVillainPhaseBegin(
            AbilityType.ForcedInterrupt,
            au_debut_de_la_phase_du_vilain,
        ),
    ]
