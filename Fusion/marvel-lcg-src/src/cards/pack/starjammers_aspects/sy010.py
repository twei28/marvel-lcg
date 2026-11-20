from . import *
# * Center Section Garden (Basic, soutien 2 [mental]). LOCATION. STARJAMMER.
# Alter-Ego Response: After you make a basic recovery, exhaust Centre Section Garden → heal 2 damage from your identity or a
# STARJAMMER character.   (le titre imprime est « Center », le texte imprime dit « Centre » : coquille de l'auteur, texte recopie tel quel)
#
# Cartes de reference : 45015 Sidekick (`AfterUnitMakeRecovery(.., "You", op, is_basic_recovery=True)` + `HealthUnits`) ; wt010
# (`SetTarget(check_fn=.., Identity|Ally)` pour « votre identite ou un allie ») ; recette `AlterEgoResponse` (RECETTES §4bis).
# « your identity OR a STARJAMMER character » : l'identite du joueur (quel que soit son trait) ET tout personnage ami portant le trait.
def GetAbilities() -> Sequence['Ability']:
    def garden(effect: 'Effect', message: 'Message.AfterUnitRecovery') -> None:
        effect.this.HealthUnits(effect.targets, 2, effect)
    def cible(effect: 'Effect', face: 'CardFace') -> bool:
        joueur = JoueurDe(effect)
        if Identity.IsType(face) and joueur is not None and face.GetControlByPlayer() is joueur:
            return True
        return (Identity.IsType(face) or Ally.IsType(face)) and face.HasTrait("STARJAMMER")
    return [
        AbilityFactory.AfterUnitMakeRecovery(
            AbilityType.AlterEgoResponse,
            "You",
            garden,
            is_basic_recovery=True,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Friend, canbe_heal=True, check_fn=cible),
    ]
