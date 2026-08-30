from . import *

# Kinetic Flurry (2/2) — exemplaire physique 2 de 2, contenu identique a sd006
# (voir ce fichier pour le detail des modeles et l'ECART ASSUME sur la couleur
# du cout X).


def GetAbilities() -> Sequence['Ability']:

    def kinetic_flurry(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        if not effect.targets:
            return
        cible = effect.targets[0]

        nombre_d_attaques = effect.GetPaidResources().GetColor("Y")

        for _ in range(nombre_d_attaques):
            if not cible.IsInPlay() or cible.IsDefeated():
                break
            degats = 3 if PorteUnCompteurExplosif(cible) else 2
            this.DealDamage([cible], degats, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            kinetic_flurry,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
