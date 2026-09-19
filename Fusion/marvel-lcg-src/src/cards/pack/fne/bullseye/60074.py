from . import *

# Everything is a Weapon
# When Revealed (Alter-Ego): Take 2 indirect damage.
# When Revealed (Hero): Choose: Either Bullseye activates against you, or
#   remove an ally you control from the game.
# [star] Boost: If Bullseye is attacking, give him an additional boost card
#   and this attack gains piercing.
# Modeles : 27080 (indirect), 08013 (ChooseAbilities a deux branches), 11041
# Deathunt (GiveBoostCardForThisActivation en contexte de boost).

def GetAbilities() -> Sequence['Ability']:

    def alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        message.GetToPlayer().GetIdentity().TakeIndirectDamage(this, 2, effect)

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        bullseye = TrouverBullseye(effect)

        def active(targets: Sequence['CardFace']) -> None:
            if bullseye:
                bullseye.DoActivate(joueur, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Bullseye activates against you", active),
            AbilityFactory.ForChoiceAbility(
                "Remove an ally you control from the game",
                lambda targets: Faces.RemoveAllFromGame(targets, effect),
            ).SetTarget("YourAlly"),
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        attaque = getattr(message, 'would_atk_message', None)
        if attaque is None:
            return
        message.GiveBoostCardForThisActivation(Enemy, 1, effect)
        attaque.GainPiercing(effect)

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", heros),
        AbilityFactory.WhenCardBecomeBoost(
            "This", boost,
            during_attack=True,
            activating_enemy=CardFinder(name="Bullseye"),
        ),
    ]
