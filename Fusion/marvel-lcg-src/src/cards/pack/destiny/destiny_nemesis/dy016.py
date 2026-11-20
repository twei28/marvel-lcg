from . import *

# So, What's the Plan? (x3) : TRAITRISE (TEMPORAL.), nemesis de Destiny. Boost 2. Incite 1.
# When Revealed: Remove 1[per_hero] threat from Destiny's Warning. If you cannot, Mister Sinister activates against you. If you cannot, this card gains surge.
#
# CARTES DE REFERENCE
#  - `dy015` / `dy014` : `RemoveThreatFromSchemes(.., "1*", effect)`, `ActiverSinister` (helper du set).
#  - `rl015` Shi'ar Host / `surge.md` : `ThisCardGainSurge(effect, message)` pour « if you cannot, this card gains surge ».
#
# TEXTE CONTRE CODE
#  « Remove 1[per_hero] threat FROM DESTINY'S WARNING » : ce complot annexe precise, 1 par joueur. « If you CANNOT » : Warning absente du jeu. « Sinister activates against YOU » : le joueur qui revele ; « If you cannot »
#    (Sinister absent) : la carte gagne surge. Trois branches exclusives, la premiere possible l'emporte. Incite 1 lu dans `desc`.
#  Chiffres : boost 2, Incite 1, 1 menace par joueur.


def GetAbilities() -> Sequence['Ability']:

    def plan(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        warnings = WarningsEnJeu(effect)
        if warnings:
            this.RemoveThreatFromSchemes(warnings[:1], "1*", effect)
            return
        sinisters = SinistersEnJeu(effect)
        if sinisters and joueur is not None:
            ActiverSinister(effect, sinisters[0], joueur)
            return
        ThisCardGainSurge(effect, message)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            plan,
        ),
    ]
