from . import *

# Judge, Jury... Execution! — COMPLOT ANNEXE. Menace de depart 3 par joueur, Boost 2, Amplify 1 (icone natif).
# When Defeated : Discard the minion with the fewest remaining hit points and deal damage to the TARGETED villain equal to that
#   minion's remaining hit points. Otherwise, give Punisher a facedown boost card.
#
# Cartes de reference : jigsaw/pu065 (`WhenSchemeBeDefeated(WhenDefeated, "This")`), `Faces.DiscardAll`, `DealDamage`
# (hobgoblin/pu059), `Faces.GiveFacedownBoostCards`.
# ⚠ « the minion with the FEWEST remaining HP » : un sbire en jeu, egalite au premier joueur ; les degats = ses PV RESTANTS
# (avant la defausse) ; « Otherwise » : aucun sbire en jeu.

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this
        sbires = list(Worlds.GetOnFieldMinions(effect))
        if not sbires:
            DonnerUneCarteBoostFaceCachee(effect, Punisher(effect), 1)
            return
        mini = LePlusFaible(effect, sbires)
        pv = mini.health
        Faces.DiscardAll([mini], effect)
        cible = VilainCible(effect)
        if cible is not None and pv > 0:
            this.DealDamage([cible], pv, effect)

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
