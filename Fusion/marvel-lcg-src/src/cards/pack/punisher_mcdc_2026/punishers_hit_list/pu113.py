from . import *

# Punisher's Arsenal — COMPLOT ANNEXE. Menace de depart 2 par joueur, Boost 1, Hazard 1 (icone « carte + », natif).
# When Revealed : Find an ARMAMENT attachment that is not in play and reveal it.
# When Defeated : Find Punisher and reveal him. Resolve his "Punishment" ability.
#
# Cartes de reference : `Find.FindAndReveal` (pu065 : par type et trait), jigsaw/pu065 (`WhenSchemeBeDefeated`).
# ⚠ « that is NOT in play » : cherche dans le deck, la defausse et les cartes de cote ; l'arme revelee s'attache
# (au Punisher sinon au vilain : voir punishers_armory) ou selon sa propre carte.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Find.FindAndReveal(effect, message.GetToPlayer(), trait="ARMAMENT", card_type=Attachment)

    def vaincu(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        joueur = Worlds.GetFirstPlayer(effect)
        Find.FindAndReveal(effect, joueur, name="Punisher", card_type=Minion)
        Punishment(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
