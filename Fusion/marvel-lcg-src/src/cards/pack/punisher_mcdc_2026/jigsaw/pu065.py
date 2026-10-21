from . import *

# Putting the Pieces Together — COMPLOT ANNEXE. Menace de depart 1 par joueur, Boost 2, Crisis 1.
# When Revealed : Place 2 threat on this scheme for each MAGGIA character in play.
# When Defeated : In player order, each player finds a MAGGIA minion that is not in play and reveals it.
#
# Cartes de reference : sm/sinister_six/27100a.py (`PlaceThreatOnSchemes([face], n, effect)`), sm/sandman/27068.py (`WhenSchemeBeDefeated(WhenDefeated, "This")`), agent_13 / the_getaway
# pour `Find.FindAndReveal`. Crisis : natif (fiche mots-cles/crisis.md).
#
# ⚠ « each MAGGIA CHARACTER in play » : sbires ET vilain (Jigsaw porte le trait MAGGIA), mechants multiples
# compris ; compter aussi un allie MAGGIA s'il y en avait un. « that is NOT in play » : cherche dans le deck,
# la defausse et les cartes mises de cote (`Find`), « in player order » : a partir du premier joueur.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        nombre = len([c for c in Worlds.GetOnFieldEnemies(effect) if c.HasTrait("MAGGIA")])
        nombre += len([a for j in Worlds.GetPlayers(effect) for a in j.GetControlAllies() if a.HasTrait("MAGGIA")])
        if nombre > 0:
            this.PlaceThreatOnSchemes([this], 2 * nombre, effect)

    def vaincu(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        for joueur in list(Worlds.GetPlayers(effect)):
            Find.FindAndReveal(effect, joueur, trait="MAGGIA", card_type=Minion)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
