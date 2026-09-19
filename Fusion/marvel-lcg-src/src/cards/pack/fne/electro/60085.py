from . import *

# Shocking Revelation
# When Revealed: Discard the top card of your deck for each card you control.
#   For each card with a printed [energy] resource discarded this way, choose:
#   - Take 1 indirect damage.  - Place 1 charge counter on Electric Charge.
# « each card you control » : tout ce qui est en jeu sous ton controle,
# identite comprise.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        # GetControlByOrOwner : `GetControlByPlayer` leve un assert sur les cartes
        # du scenario (lecon si012, 18/09/2026).
        n = len([f for f in Worlds.FindCardsOnField(effect) if f.GetControlByOrOwner() is joueur])
        if n <= 0:
            return
        defaussees = joueur.DiscardDeckTopCards(n, effect)
        for carte in defaussees:
            if not (ClassCard.IsType(carte) and carte.printed_resource.HasColorPrinted("Y")):
                continue
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility("Take 1 indirect damage", lambda targets: joueur.GetIdentity().TakeIndirectDamage(this, 1, effect)),
                AbilityFactory.ForChoiceAbility("Place 1 charge counter on Electric Charge", lambda targets: PoserCharges(effect, 1)),
            )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
