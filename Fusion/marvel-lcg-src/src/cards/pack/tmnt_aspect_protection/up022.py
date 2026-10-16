from . import *

# * Lindsey Baker (bandeau « The Night Nurse ») — SOUTIEN 1 [mental], aspect Protection (TMNT Aspects,
# Inkwire). PERSONA.
# Uses (3 healing counters).
# Action: Exhaust Lindsey Baker and remove 1 healing counter from her -> heal 1 damage from a hero and
#   discard 1 status card from it.
#
# Texte de `09019` The Night Nurse au nom du COMPTEUR pres (« healing » au lieu de « medical ») : le module
# de 09019 ecrit 'medical' en dur. Script propre, copie de 09019 ; `desc.Uses` = "3,healing".
#
# MOT-CLE : Uses (fiche uses.md) — les compteurs sont poses par le moteur depuis `desc.Uses`.
#
# CARTE DE REFERENCE : `09019` The Night Nurse (copie ligne a ligne, seul le nom du compteur change).
#
# TEXTE CONTRE CODE
#  ⚠ « Exhaust ... AND remove 1 healing counter » : deux couts, les deux poses.
#  ⚠ « a HERO » : identite en forme heros seulement (`GetOnFieldHeroes`), soignable OU portant un statut.
#  ⚠ « heal 1 damage ... AND discard 1 status card from IT » : le meme heros.


def GetAbilities() -> Sequence['Ability']:

    def lindsey_baker(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)
        for target in effect.targets:
            this.HealthUnits([target], 1, effect)
            initiator = effect.GetInitiator()
            status = target.components.status.GetDeck().Get()
            status_face = initiator.AskChooseFace(status, effect)
            if status_face:
                Faces.DiscardAll([status_face], effect)

    def heros_soignables_ou_avec_statut(effect: 'Effect') -> Sequence['Hero']:
        return [x for x in Worlds.GetOnFieldHeroes(effect) if x.CanHeath() or x.HasStatus('Any')]

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            lindsey_baker
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'healing'))
        .SetTarget(heros_soignables_ou_avec_statut)
    ]
