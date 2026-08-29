from . import *

# Early Start — side scheme nemesis d'Iron Lad (1/5)
# When Revealed: Exhaust each Iron Lad upgrade in play.
# While this scheme is in play, Iron Lad upgrades cannot be readied.
#
# "Upgrade Iron Lad" = carte du pack (set_name "Iron Lad"), pas un filtre par
# trait : voir UpgradesIronLadEnJeu (__init__.py). Restriction continue :
# `AbilityFactory.CardCannotReady(...)` (game/ability/factory/state.py),
# active tant que la carte est en jeu -- pas de garde supplementaire requise,
# ses abilities cessent de s'appliquer des qu'elle quitte le jeu.

def GetAbilities() -> Sequence['Ability']:

    def early_start(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this, message)

        upgrades = UpgradesIronLadEnJeu(effect)
        if upgrades:
            Faces.ExhaustAll(upgrades, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            early_start,
        ),
        *AbilityFactory.CardCannotReady(
            CardFinder(card_type=Upgrade, check_face_fn=lambda f: f.paper.set_name == "Iron Lad"),
        ),
    ]
