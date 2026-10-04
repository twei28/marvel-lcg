from . import *

# Frozen Fury — TREACHERY, RED SONJA NEMESIS (5/5). Boost 0.
# When Revealed: For each upgrade you control (to a maximum of 3), choose:
# * Take 1 indirect damage.
# * Place 1 threat on the main scheme.
#
# CARTES DE REFERENCE
#  - `night_thrasher_nemesis/nt015.py` : `this.DealIndirectDamage(identite,
#    N, effect)` pour « indirect damage ».
#  - `core/she_hulk/01160.py` : `Worlds.FindMainScheme(effect)` +
#    `scheme.PlaceThreatInternal(N, effect)` pour « place threat on the
#    main scheme ».
#  - `wave/65004.py` Marine Patrol : choix repete « for each » -- ICI chaque
#    iteration ROUVRE les deux memes options (contrairement a Marine Patrol,
#    ou chaque branche n'est offerte qu'une fois au total : rien n'impose
#    « max 1 chacune » sur cette carte-ci, verifie au texte imprime).
#
# TEXTE CONTRE CODE : « to a maximum of 3 » : `min(n_ameliorations, 3)`
# iterations, jamais plus meme si le joueur en controle davantage.

def GetAbilities() -> Sequence['Ability']:

    def frozen_fury(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()
        if not isinstance(joueur, Player):
            return

        ameliorations = joueur.GetControlCards(CardFinder(card_type=Upgrade))
        n = min(len(ameliorations), 3)

        def prendre_degats(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            this.DealIndirectDamage(joueur.GetIdentity(), 1, effect)

        def poser_menace(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            scheme = Worlds.FindMainScheme(effect)
            if scheme:
                scheme.PlaceThreatInternal(1, effect)

        for _ in range(n):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Take 1 indirect damage", prendre_degats,
                ),
                AbilityFactory.ForChoiceAbility(
                    "Place 1 threat on the main scheme", poser_menace,
                ),
            )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            frozen_fury,
        ),
    ]
