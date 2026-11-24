from . import *
# * Ultron — sbire nemesis (Stalwart, Villainous dans desc). When Revealed : trouve Seized Control MIS DE COTE et le revele ;
# sinon « seek » une carte HACKED du deck rencontre et la revele. [star] Boost : incline une amelioration que tu controles.
def GetAbilities() -> Sequence['Ability']:
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        joueur = message.GetToPlayer()
        cachees = [face for face in joueur.set_aside_deck.GetAll() if face.paper.card_id == "hp016"]
        if cachees:
            cachees[0].Reveal(None, effect)
            return
        autres: List['CardFace'] = []
        trouvee = Worlds.DiscardEncounterCardsUntil(effect, trait="HACKED", return_other_faces=autres)
        if trouvee:
            trouvee.Reveal(None, effect)
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        prets = [face for face in joueur.GetControlCards(CardFinder(card_type=Upgrade)) if face.CanExhaust()]
        if prets:
            Faces.ExhaustAll([prets[0] if len(prets) == 1 else joueur.AskChooseFace(prets, effect)], effect)
    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
