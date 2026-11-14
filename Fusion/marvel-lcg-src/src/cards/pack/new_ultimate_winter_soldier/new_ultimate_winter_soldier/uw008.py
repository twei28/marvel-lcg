from . import *

# Desperate Regenerate — evenement signature, x2. SUPERPOWER. Cout 2, [energy].
# Action: Draw 2 cards. Discard 1 card from your hand at random. Choose:
#  • Heal 3 damage from your identity.
#  • Discard each stunned and confused status card from your identity.
#
# Carte de reference : `35012` Regenerative Healing (Wolverine officiel) : MEME choix (« Heal N damage from your identity »
# / « Discard each stunned and confused status card ») = `ChooseAbilities(ForChoiceAbility.. "YourIdentity")` ; ici N = 3
# et, avant le choix, « Draw 2 cards. Discard 1 card from your hand at random » (un EFFET, pas un cout : pas de fleche).
#
# Mots-pieges : l'ordre (piocher d'abord, puis defausser : la carte piochee peut etre tiree) ; la defausse au hasard ne
# prend jamais l'evenement en cours (`exclude`) ; la carte reste jouable sans degats ni statut (elle pioche quand meme) :
# pas de condition d'identite, contrairement a 35012.


def GetAbilities() -> Sequence['Ability']:

    def desperate_regenerate(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()

        initiator.DrawUp(2, effect)
        initiator.DiscardRandomHandCards(1, effect, exclude=[this])

        def soigner(cibles: 'Sequence[CardFace]') -> None:
            this.HealthUnits(cibles, 3, effect)

        def defausser(cibles: 'Sequence[CardFace]') -> None:
            identite = cibles[0].CastTo(Identity)
            identite.DiscardStunned(effect, rule="All")
            identite.DiscardConfused(effect, rule="All")

        identite = initiator.GetIdentity()
        peut_soigner = identite.CanHeath()
        a_un_statut = identite.IsStunned() or identite.IsConfused()
        if not (peut_soigner or a_un_statut):
            return
        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Heal 3 damage from your identity",
                soigner,
                condition=peut_soigner,
            ).SetTarget("YourIdentity", canbe_heal=True),
            AbilityFactory.ForChoiceAbility(
                "Discard each stunned and confused status card from your identity",
                defausser,
                condition=a_un_statut,
            ).SetTarget("YourIdentity", has_status=["Stunned", "Confused"]),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            desperate_regenerate,
        ).SetPlay(),
    ]
