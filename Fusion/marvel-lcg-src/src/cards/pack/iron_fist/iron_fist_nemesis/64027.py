from . import *

# * Davos — SBIRE nemesis d'Iron Fist (N 1/5). K'UN-LUN. MARTIAL ARTIST. MAN 1, ATQ 2, PV 5. 2 icones de boost.
# When Revealed: Find and tuck the 3 Crane Daughter minions under here.
# Forced Interrupt: When Davos would take any amount of damage, shuffle a tucked Crane Daughter from under Davos
#   into the encounter deck instead.
#
# MOTS-CLES : find (fiche find.md), tuck (fiche tuck.md).
#
# CARTES DE REFERENCE
#  - glisser sous une carte de rencontre : `throg_nemesis/tg015` (`this.TuckCardUnderHere`, `GetPlacedCardArea().Get()`).
#  - degats remplaces : `04065` Crossbones' Armor (`WhenUnitWouldTakeDamage` + `message.SetBeInstead(effect)`).
#
# TEXTE CONTRE CODE
#  ⚠ « FIND » (Rules Reference 1.8 p.19) : toutes les zones ou la carte peut etre — deck et defausse de rencontre,
#    zone mise de cote (set nemesis), EN JEU. Pas les cartes face cachee distribuees ni les cartes de boost.
#    Le deck de rencontre fouille est melange ensuite.
#  ⚠ « would take ANY amount of damage » : toute source, tout montant ; TOUT le degat est remplace par UNE Crane
#    Daughter melangee. Sans Crane Daughter dessous, rien ne remplace : Davos prend le degat.
#  ⚠ « instead » : le degat n'est pas inflige (pas de reponse « apres degats », pas d'exces).


def GetAbilities() -> Sequence['Ability']:

    def trouver_et_glisser(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)
        du_deck = [f for f in Worlds.GetEncounterDeckCards(effect) if EstCrane(f)]
        ailleurs = [f for f in Worlds.GetEncounterDiscardPileCards(effect) + Worlds.GetSetAsideAreaCards(effect) if EstCrane(f)]
        trouvees = Types.RemoveDuplicates(du_deck + ailleurs + CranesEnJeu(effect))[:3]
        Glisser(this, trouvees, effect)
        if du_deck:
            Worlds.GetEncounterDeck(effect).Shuffle(effect)

    def a_une_crane(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        return bool(CranesSous(effect.this))

    def sacrifier_une_crane(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Minion)
        dessous = CranesSous(this)
        if not dessous:
            return
        message.SetBeInstead(effect)
        Faces.ShuffleAllTo([dessous[0]], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            trouver_et_glisser,
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            "This",
            sacrifier_une_crane,
            conditions=[a_une_crane],
        ),
    ]
