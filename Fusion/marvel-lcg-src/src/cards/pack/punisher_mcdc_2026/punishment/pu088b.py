from . import *

# One Last Kill (1B) — MANIGANCE PRINCIPALE. Menace 8 par joueur, depart 1 par joueur, acceleration +1 par joueur.
# When Revealed : Find and reveal Punisher's M1911s.
# Forced Response : After resolving step one of the villain phase, the TARGETED villain activates against the first player.
#
# Cartes de reference : sm/sinister_six/27100b.py (`AfterResolveVillainPhaseStep`), `Find.FindAndReveal`,
# `Enemy.DoActivate`. Menaces et acceleration : natifs (`desc`).
# ⚠ « the TARGETED villain activates against the FIRST player » : le vilain cible (sous-fifre), pas Punisher ; contre le
# premier joueur (pas contre chacun) ; apres l'etape 1 de la phase du vilain (la menace du complot).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Find.FindAndReveal(effect, message.GetToPlayer() or Worlds.GetFirstPlayer(effect), name="Punisher's M1911s", card_type=Attachment)

    def apres_etape_un(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        cible = VilainCible(effect)
        if cible is not None:
            cible.CastTo(Enemy).DoActivate(Worlds.GetFirstPlayer(effect), effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.AfterResolveVillainPhaseStep(AbilityType.ForcedResponse, 1, apres_etape_un),
    ]
