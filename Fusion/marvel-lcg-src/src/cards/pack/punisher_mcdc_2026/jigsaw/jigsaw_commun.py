from . import *

# Jigsaw (pack MC×DC 2026 « La ville ne dort jamais »), capacité commune aux
# quatre faces de vilain (pu056a/b, pu057a/b) :
# ★ Forced Response : après que Jigsaw vous a attaqué, si le dessus de la
#   défausse de rencontre est un sbire, le mettre en jeu engagé avec vous ;
#   sinon, placer N menace sur la manigance principale (N = 1, sauf pu057b : 2).
#
# Cartes de reference : sm/sinister_six/27099.py (Vulture) pour le declencheur
# `AfterUnitAttackUnit(ForcedResponse, "This", "You")` ;
# angela/angela_nemesis/an015.py pour lire la defausse de rencontre
# (`Worlds.GetEncounterDiscardPile(effect).Get(True)`, index 0 = dessus) ;
# sm/sinister_six/27100a.py pour `PutIntoPlay(joueur, effect)` et
# `PlaceThreatOnSchemes`.
#
# ⚠ « mettre en jeu » ne declenche PAS « When Revealed » (RR, Put into play).

def Jigsaw(menace_sinon: int) -> 'Ability':

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(EncounterVillain)
        open("/tmp/jigdbg.txt","a").write("appel %s\n" % this.paper.card_id)
        joueur = message.GetToPlayer()

        pile = list(Worlds.GetEncounterDiscardPile(effect).Get(True))
        if pile and Minion.IsType(pile[0]):
            pile[0].PutIntoPlay(joueur, effect)
            return
        schemes = Worlds.GetMainSchemes(effect)
        if schemes:
            this.PlaceThreatOnSchemes(schemes[:1], menace_sinon, effect)

    return AbilityFactory.AfterUnitAttackUnit(
        AbilityType.ForcedResponse,
        "This",
        "You",
        apres_attaque,
    )
