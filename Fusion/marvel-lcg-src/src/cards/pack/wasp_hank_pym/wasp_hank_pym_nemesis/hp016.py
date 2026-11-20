from . import *
# Seized Control — attachement (HACKED). S'attache a Ultron, sinon au vilain. When Revealed : glisse dessous la carte que tu
# controles au cout le plus BAS ; sinon surge et defausse cette carte. Forced Interrupt : quand le personnage porteur
# subirait des degats, les place ICI a la place ; puis, si au moins X degats ici (X = cout de la carte glissee), defausse.
def GetAbilities() -> Sequence['Ability']:
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        candidates = [face for face in joueur.GetControlCards() if (Upgrade.IsType(face) or Support.IsType(face) or Ally.IsType(face))]
        face = Filter.One(candidates, effect, lowest_cost=True)
        if face and this.TuckCardUnderHere([face], effect):
            return
        ThisCardGainSurge(effect)
        Faces.DiscardAll([this], effect)
    def absorbe(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)
        n = message.will_take_damage
        message.PreventDamage("All", effect)
        Faces.PlaceCountersOn([this], n, 'damage', effect)
        glissees = this.GetPlacedCardArea().GetAll()
        x = sum(face.printed_cost for face in glissees)
        if this.GetCounters('damage') >= x:
            Faces.DiscardAll([this], effect)
    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name="Ultron"),
            if_cannot_attach_to=Villain,
        ),
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            "AttachedCharacter",
            absorbe,
        ),
    ]
