from . import *

# Raise the Stakes (CONDITION) — Attach to Bullseye.
# [star] Forced Interrupt: When Bullseye attacks, give him 1 additional boost
#   card for this attack. If this attack defeats a friendly character, remove
#   them and this card from the game. Otherwise, shuffle this card into the
#   encounter deck.
# Modeles : 02020 Hysteria (boost supplementaire), 01099 Charge
# (RunAt.AfterEnemyActivationEnd), 24023 Out for Blood (temp WhenUnitBeDefeated
# borne a l'attaque en cours pour SAVOIR qui a ete vaincu).

def GetAbilities() -> Sequence['Ability']:

    def mise(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Attachment)
        message.GiveAdditionalBoostCardForThisActivation(1, effect)
        vaincus: List['CardFace'] = []

        def noter(e: 'Effect', m: 'Message.WhenUnitBeDefeated') -> None:
            vaincus.append(m.trigger)

        temps = this.effect.Registers(
            AbilityFactory.WhenUnitBeDefeated(
                AbilityType.Temp0,
                Friend,
                noter,
                conditions=[lambda e, m: getattr(m, 'would_atk_message', None) is message],
            )
        )

        def fin() -> None:
            Effects.UnRegister(temps)
            if vaincus:
                Faces.RemoveAllFromGame(vaincus + [this], effect)
            elif this.IsInPlay():
                Faces.ShuffleAllTo([this], "EncounterDeck", effect)

        RunAt.AfterEnemyActivationEnd(effect, message, fin)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Bullseye")),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            CardFinder(name="Bullseye"),
            mise,
        ),
    ]
