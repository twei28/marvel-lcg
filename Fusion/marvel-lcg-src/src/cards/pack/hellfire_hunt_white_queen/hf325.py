from . import *

# Veil of Mind's Mirage. Attachement ILLUSION PSIONIC. « Attach to your identity. When Revealed : Find your nemesis side scheme, then reveal it. If your
# nemesis side scheme has the permanent keyword, discard this card. Forced Response : After the player phase ends, if your nemesis side scheme is in play,
# deal 1 damage to your identity. Otherwise, discard this card. » Cartes de reference : 01190 Shadow of the Past (nemesis mis de cote), 90xxx.


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        scheme = Search.EncounterCard(effect, joueur, include_discard_pile=True, include_set_aside=True, card_type=SchemeSide2, is_nemesis=joueur)
        if scheme is not None:
            scheme.Reveal(joueur, effect)
            if getattr(scheme, "permanent", 0):
                Faces.DiscardAll([this], effect)

    def fin_de_phase(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this
        joueur = effect.GetInitiator() if Player.IsType(effect.GetInitiator()) else Worlds.GetFirstPlayer(effect)
        present = any(f.IsInPlay() for f in Worlds.GetOnFieldCards(effect) if SchemeSide2.IsType(f) and f.IsNemesis(joueur))
        if present:
            joueur.GetIdentity().TakeDamage(this, 1, effect)
        else:
            Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenPlayerPhaseEnd(AbilityType.ForcedResponse, fin_de_phase),
    ]
