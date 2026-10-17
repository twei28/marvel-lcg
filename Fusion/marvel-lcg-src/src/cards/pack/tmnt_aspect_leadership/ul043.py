from . import *

# * Zink — ALLIE Leadership a DOS DE RENCONTRE (TMNT Aspects, Inkwire), sans cout, [mental].
# NINJA. WEASEL. THW 0* / ATQ 2* / PV 1.
# Linked (Weasel In).
# Zink does not count against your ally limit.
# When Revealed: Deal 2 damage to an enemy and put Zink into play under your control. This card gains
#   surge. This effect cannot be canceled.
#
# Montage commun : `AbilitiesBelette` (__init__ du pack, modele `39071` Longshot).
#
# TEXTE CONTRE CODE
#  ⚠ « an enemy » : vilain ou sbire, choisi par le joueur qui revele. Pas une attaque.
#  ⚠ « under YOUR control » : le joueur qui revele la carte.


def GetAbilities() -> Sequence['Ability']:

    def blesser(effect: 'Effect', joueur: 'Player') -> None:
        this = effect.this.CastTo(Ally)
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 2 damage to an enemy",
                lambda cibles: this.DealDamage(cibles, 2, effect),
            ).SetTarget(Enemy),
        )

    return AbilitiesBelette(blesser)
