from . import *

# * Predator Elite — SBIRE unique. ELITE. YAUTJA. SCH 2, ATK 2, PV 6. Boost 2.
# When Revealed: Discard an upgrade or support you control.
# When Defeated: Discard the top card of your deck and deal damage to a [[XENOMORPH]] enemy equal to that cards printed cost.
#
# Cartes de reference : `DiscardControlCards(upgrade=True, support=True)` (07034, choix du joueur) ; `DiscardDeckTopCards(1)` +
#   `FacesCounter.GetPrintedCost` (27170) ; degats a un ennemi au choix.
#
# ⚠ Mots-pieges :
#  - « an upgrade OR support YOU control » : au choix du joueur ; rien -> rien ;
#  - « YOUR deck » (When Defeated) : le joueur qui l'a vaincu ; « A [[XENOMORPH]] enemy » : un seul, au choix ; carte sans cout -> 0.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        JoueurDuMessage(message, effect).DiscardControlCards(effect, upgrade=True, support=True)

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this
        joueur = JoueurQuiVainc(message, effect, this)
        defaussees = [f for f in joueur.DiscardDeckTopCards(1, effect) if not f.IsInPlay()]
        cout = FacesCounter.GetPrintedCost(defaussees) if defaussees else 0
        cibles = EnnemisParTrait(effect, "XENOMORPH")
        if cout <= 0 or not cibles:
            return
        cible = joueur.AskChooseFace(cibles, effect, prompt="Deal damage to a XENOMORPH enemy") or cibles[0]
        this.DealDamage([cible], cout, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        # NoOutOfPlayLimit : Expanding Hive a peut-etre deja donne la carte en boost ; son « When Defeated » se resout quand meme.
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu).NoOutOfPlayLimit(),
    ]
