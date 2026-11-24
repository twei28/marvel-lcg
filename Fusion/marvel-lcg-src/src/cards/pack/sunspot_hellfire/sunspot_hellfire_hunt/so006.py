from . import *

# Soak Up the Sun — EVENEMENT, cout 2, RES [energy], x2. SUPERPOWER.
# Alter-Ego Action: Place 5 solar counters on your identity card.
# Hero Action: If you have the AERIAL trait, place 3 solar counters on Sunspot.
#
# CARTES DE REFERENCE
#  - `hp003` Gigantification, `hp005` Self-Shrinking : un evenement a DEUX capacites de jeu (`.SetPlay()` chacune) doit etre
#    declare dans la liste blanche de `game/card/factory.py` (lecon ls005) : `so006` y est (CORRECTIF du 26/10/2026).
#  - `sw001b` : poser des compteurs sur l'identite.
#
# TEXTE CONTRE CODE
#  ⚠ « If you have the AERIAL trait » : la Hero Action reste JOUABLE sans le trait (carte jouee, aucun compteur).


def GetAbilities() -> Sequence['Ability']:

    def soak_up_alter_ego(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        Unused(message)
        PoserSolaires(effect.GetInitiator(), 5, effect)

    def soak_up_hero(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        Unused(message)
        joueur = effect.GetInitiator()
        if EstAerien(joueur):
            PoserSolaires(joueur, 3, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            soak_up_alter_ego,
        ).SetPlay().SetLabel(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            soak_up_hero,
        ).SetPlay().SetLabel(),
    ]
