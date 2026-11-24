from . import *
# Submit or Perish — traitrise (HACKED). When Revealed : incline chaque amelioration que tu controles ; si MOINS DE 2 ont
# ete inclinees, cherche Ultron dans le deck rencontre et la defausse et le met en jeu engage avec toi ; sinon surge.
def GetAbilities() -> Sequence['Ability']:
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        joueur = message.GetToPlayer()
        inclinees = Faces.ExhaustAll(joueur.GetControlCards(CardFinder(card_type=Upgrade)), effect)
        if len(inclinees) >= 2:
            ThisCardGainSurge(effect)
            return
        ultron = Search.EncounterCard(effect, include_discard_pile=True, name="Ultron", card_type=Minion)
        if ultron:
            ultron.PutIntoPlay(joueur, effect)
        else:
            ThisCardGainSurge(effect)
    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
