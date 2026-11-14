from . import *

# * Prowler — SBIRE UNIQUE. CRIMINAL. THIEF. SCH 2, ATQ 2, 4 PV, Boost 1, Quickstrike 1.
# Quickstrike.
# Forced Response : After Prowler damages your hero, discard 2 cards from the encounter deck. If a treachery was
#   discarded this way, discard an upgrade or support you control.
#
# Cartes de reference : jigsaw/pu064.py (`AfterUnitAttackUnit` ForcedResponse), 27099 Vulture
# (`AfterUnitAttackAndDamageUnit(ForcedResponse, "This", "You")`), `Worlds.DiscardEncounterCards`.
# Quickstrike : natif (fiche mots-cles/quickstrike.md).
#
# ⚠ « damages YOUR HERO » : l'attaque doit blesser le heros (pas un allie, pas un alter ego : un sbire attaque un alter
# ego ? non, il manigance) ; « an upgrade OR support YOU control » : le joueur choisit parmi SES ameliorations
# (y compris celles de ses allies) et SES soutiens ; aucun = rien.

def GetAbilities() -> Sequence['Ability']:

    def apres_blessure(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        joueur = message.GetToPlayer()
        if joueur is None or not joueur.IsHero():
            return
        cartes = Worlds.DiscardEncounterCards(2, effect)
        if not any(Treachery.IsType(c) for c in cartes):
            return
        candidates = list(joueur.GetControlUpgrade()) + list(joueur.supports.Get())
        if not candidates:
            return
        choisie = candidates[0] if len(candidates) == 1 else joueur.AskChooseFace(candidates, effect)
        if choisie is not None:
            Faces.DiscardAll([choisie], effect)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(AbilityType.ForcedResponse, "This", "You", apres_blessure),
    ]
