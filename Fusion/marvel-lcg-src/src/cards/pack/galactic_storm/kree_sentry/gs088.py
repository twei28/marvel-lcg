from . import *

# "Gotcha!" — TRAITRISE (Kree Sentry), 2 exemplaires. Aucune icone de boost (etoile rouge seule : ★ Boost).
# When Revealed: Attach a set aside copy of Sentry's Grasp to Rick Jones. If you cannot, this card gains surge.
# [star] Boost: Attach a set aside copy of Sentry's Grasp to Rick Jones.
#
# Cartes de reference :
#  - « If you cannot, this card gains surge » : `ThisCardGainSurge(effect)`, modele OFFICIEL 40189 Mutant Insurrection.
#  - « attach a set aside copy ... to Rick Jones » : `AttacherUnePoigne` (kree_sentry/__init__.py).
#  - Boost : `WhenCardBecomeBoost("This", op)` (RECETTES §1, modele an013).
#
# ⚠ Mots-pieges : « If you CANNOT » = plus aucune copie mise de cote (ou Rick Jones absent) ; le Boost attache sans
# clause de surge ; l'icone etoile rouge seule du coin n'est PAS une icone de boost.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        if not AttacherUnePoigne(effect, RickJones(effect)):
            ThisCardGainSurge(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        AttacherUnePoigne(effect, RickJones(effect))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
