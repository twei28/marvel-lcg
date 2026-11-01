from . import *

# Energic Backlash (x2, hf224-hf225). Traitrise SKILL. « When Revealed (Alter-Ego) : Place 4 energy counters on Sebastian Shaw. When Revealed (Hero) :
# Place 2 energy counters on Sebastian Shaw. Sebastian Shaw attacks you. [star] Boost : After this activation, place 3 energy counters on Sebastian Shaw. »
# Cartes de reference : hf120 (WQ : forme du joueur `IsAlterEgo()` / `DoAttackYou`), 49042 (`AfterThisActivation`).
# ⚠ L'attaque de Shaw passe par son Forced Interrupt (retire jusqu'a 3 compteurs pour +1 ATK chacun) : les 2 compteurs poses AVANT l'attaque servent donc.


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur.IsHero():
            PlacerEnergie(effect, 2)
            shaw = ShawVilain(effect)
            if shaw is not None:
                shaw.DoAttackYou(joueur, effect)
        else:
            PlacerEnergie(effect, 4)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        def apres_l_activation() -> None:
            PlacerEnergie(effect, 3)

        message.AfterThisActivation(effect, apres_l_activation)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
