from . import *
# * Minister T'Cahr (sbire SHI'AR, 5 PV, SCH 2*, ATQ 1*, boost 2). Sbire nemesis d'Hepzibah.
#
# [star] Forced Response: After T'Cahr activates against you, search the encounter deck and discard pile for a SHI'AR card and
# reveal it.
#
# Cartes de reference : 15025 Luminous (`AfterEnemyActivatesAgainstYou`), 15027 (`Search.EncounterCard(.., include_discard_pile=True)`),
# ag013 (`face.Reveal(player, effect)`).
def GetAbilities() -> Sequence['Ability']:
    def tcahr(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        joueur = message.GetAgainstPlayer()
        face = Search.EncounterCard(effect, include_discard_pile=True, trait=TRAIT_SHIAR)
        if face:
            face.Reveal(joueur, effect)
    return [
        AbilityFactory.AfterEnemyActivatesAgainstYou(
            AbilityType.ForcedResponse,
            "This",
            tcahr,
        ),
    ]
