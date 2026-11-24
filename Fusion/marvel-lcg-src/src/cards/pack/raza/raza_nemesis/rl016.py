from . import *
def GetAbilities() -> Sequence['Ability']:
    def reveler(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        sbire = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
        if sbire is None:
            Faces.DiscardAll([this], effect)
            return
        sbire.Reveal(joueur, effect)
        this.AttachTo2(sbire, effect)
    def sbire_vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        sbire = message.trigger
        joueur = None
        if Minion.IsType(sbire):
            joueur = sbire.CastTo(Minion).GetEngagedPlayer()
        if joueur is None:
            joueurs = list(Worlds.GetPlayers(effect))
            joueur = joueurs[0] if joueurs else None
        MettreZzzxxEnJeu(effect, joueur)
    return [
        AbilityFactory.WhenThisRevealed(None, reveler),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.ForcedResponse,
            "AttachedMinion",
            sbire_vaincu,
        ),
    ]
