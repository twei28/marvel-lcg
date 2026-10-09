from . import *

# hs108b The Great Hunt
# Forced Response : apres qu'un TRAP est revele, 1 menace ici (limite 1 par ronde et par joueur).
# Complot complete = defaite (regle native).

def GetAbilities() -> Sequence['Ability']:

    def piege_revele(effect: 'Effect', message: 'Message.AfterCardRevealedEnd') -> bool:
        return message.trigger.HasTrait("TRAP") and \
            LimiteParJoueurEtParRound(effect, message.to_player, "hs108b", 1, consommer=False)

    def poser(effect: 'Effect', message: 'Message.AfterCardRevealedEnd') -> None:
        LimiteParJoueurEtParRound(effect, message.to_player, "hs108b", 1, consommer=True)
        effect.this.PlaceThreatOnSchemes([effect.this], 1, effect)

    return [AbilityFactory.AfterPlayerRevealCard(
        AbilityType.ForcedResponse, "AnyPlayer", None, poser, conditions=[piege_revele])]
