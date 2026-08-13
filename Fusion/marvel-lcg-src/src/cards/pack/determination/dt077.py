from . import *

# * Hit-Monkey

def GetAbilities() -> Sequence['Ability']:

    def hit_monkey(effect: 'Effect', message: 'Message.WhenAllyWouldTakeConsequentialDamage') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        initiator = effect.GetInitiator()
        faces = initiator.LookAtDeck("EncounterDeck", 1, effect)
        if not faces:
            return
        # Les deux icones que compte la carte : `boost_icon` pour les [boost],
        # `boost_star` pour l'etoile (has_boost_icon.py).
        carte = faces[0].CastTo(HasBoostIcon)
        valeur = carte.boost_icon + carte.boost_star
        if valeur > 0:
            message.PreventDamage(valeur, effect)

    def check_this(effect: 'Effect', message: 'Message.WhenAllyWouldTakeConsequentialDamage') -> bool:
        return effect.this == message.trigger

    return [
        Ability(
            AbilityType.Interrupt,
            Message.WhenAllyWouldTakeConsequentialDamage,
            [check_this],
            hit_monkey,
            is_local=True
        ),
    ]
