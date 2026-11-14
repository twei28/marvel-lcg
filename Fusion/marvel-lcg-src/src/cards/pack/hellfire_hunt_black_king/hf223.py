from . import *

# Hellfire Indoctrination (x2, hf222-hf223). Traitrise HELLFIRE TACTIC. « When Revealed : Confuse each ally you control. If there is no CAPTIVE ally is
# confused in this way, this gains surge. [star] Boost : After this activation, place 2 energy counters on Sebastian Shaw. »
# Cartes de reference : hf118 (WQ : `ThisCardGainSurge`, allies du joueur), 41029 (`Faces.GiveStatus(..., "Confused")`, le RETOUR compte les unites
# reellement servies, faces.py:180), 49042 (`AfterThisActivation`).
# ⚠ « confused IN THIS WAY » : un captif DEJA desoriente n'est pas desoriente « de cette facon » ; on compte donc les captifs desorientes par CETTE carte.


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        allies = [f for f in joueur.GetControlCards(CardFinder(card_type=Ally)) if f.IsInPlay()]
        captifs = [f for f in allies if f.HasTrait(CAPTIF)]
        autres = [f for f in allies if not f.HasTrait(CAPTIF)]
        Faces.GiveStatus(autres, "Confused", effect)
        desorientes = Faces.GiveStatus(captifs, "Confused", effect) or 0
        if desorientes == 0:
            ThisCardGainSurge(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        def apres_l_activation() -> None:
            PlacerEnergie(effect, 2)

        message.AfterThisActivation(effect, apres_l_activation)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
