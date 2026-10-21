from . import *

# Escaping Punishment (2B) — MANIGANCE PRINCIPALE. Menace 9 par joueur, depart 1, acceleration +1.
# Forced Response : After resolving step one of the villain phase, the TARGETED villain activates against the first player.
# If this scheme is completed, the TARGETED villain escapes and the players lose the game.
#
# Cartes de reference : pu088b. « If this scheme is completed, ... players lose » : regle du DERNIER stade du complot
# principal (native : « If this stage is completed, the players lose the game »), aucun script.

def GetAbilities() -> Sequence['Ability']:

    def apres_etape_un(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        cible = VilainCible(effect)
        if cible is not None:
            cible.CastTo(Enemy).DoActivate(Worlds.GetFirstPlayer(effect), effect)

    return [
        AbilityFactory.AfterResolveVillainPhaseStep(AbilityType.ForcedResponse, 1, apres_etape_un),
    ]
