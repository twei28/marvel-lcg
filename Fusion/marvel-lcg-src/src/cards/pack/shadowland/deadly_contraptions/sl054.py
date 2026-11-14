from . import *

# Poison Darts — TRAITRISE. TRAP! Boost 2.
# When Revealed : Choose :
#  • Avoid — Spend [energy][energy] resources.
#  • Disarm — Spend [mental][mental][physical] resources, then deal 3 damage to the villain.
#  • Trip — Deal 3 damage to your identity and exhaust it.
#
# Cartes de reference : shadows_in_the_night/sl004a (`ForChoiceAbilityWithCost(Cost("RR"), ...)` gardee par `PeutCouvrirLeCout`), fne/art_museum_heist/60127 (choix payants),
# core/rhino/01099.
# ⚠ Mots-pieges : resources d'apres les icones verifiees contre le pack (eclair = ENERGIE Y, reseau de noeuds = MENTALE B, poing = PHYSIQUE R : Cost("YY") et Cost("BBR")) ;
#  l'option payante n'est offerte que si payable (sinon le moteur la reduit au plus gros morceau payable) ; « the VILLAIN » (pas un sbire) ; Trip : degats PUIS epuise.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        this = effect.this

        def desarme() -> None:
            vilain = Worlds.FindVillain(effect)
            if vilain is not None:
                this.DealDamage([vilain], 3, effect)

        def declenche() -> None:
            DegatsEtStatut(effect, joueur, 3, "Exhausted")

        ChoixDePiege(effect, joueur,
                     OptionDePiege(effect, joueur, PIEGE_AVOID, "Spend [energy][energy] resources", lambda: None, cout="YY"),
                     OptionDePiege(effect, joueur, PIEGE_DISARM, "Spend [mental][mental][physical] resources, then deal 3 damage to the villain", desarme, cout="BBR"),
                     OptionDePiege(effect, joueur, PIEGE_TRIP, "Deal 3 damage to your identity and exhaust it", declenche))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
