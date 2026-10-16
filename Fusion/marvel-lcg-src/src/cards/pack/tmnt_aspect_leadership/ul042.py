from . import *

# * Zanna — ALLIE Leadership a DOS DE RENCONTRE (TMNT Aspects, Inkwire), sans cout, [energy].
# NINJA. WEASEL. THW 2* / ATQ 0* / PV 1.
# Linked (Weasel In).
# Zanna does not count against your ally limit.
# When Revealed: Remove 2 threat from a scheme and put Zanna into play under your control. This card gains
#   surge. This effect cannot be canceled.
#
# Montage commun : `AbilitiesBelette` (__init__ du pack, modele `39071` Longshot).
#
# TEXTE CONTRE CODE
#  ⚠ « a scheme » : principale ou annexe, choisie par le joueur qui revele.
#  ⚠ « under YOUR control » : le joueur qui revele la carte.


def GetAbilities() -> Sequence['Ability']:

    def retirer(effect: 'Effect', joueur: 'Player') -> None:
        this = effect.this.CastTo(Ally)
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 2 threat from a scheme",
                lambda cibles: this.RemoveThreatFromSchemes(cibles, 2, effect),
            ).SetTarget(Scheme2),
        )

    return AbilitiesBelette(retirer)
