from . import *
def GetAbilities() -> Sequence['Ability']:
    def discard_tough(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        target = message.target
        target.DiscardTough(effect, rule="All")
    def discard_this(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.DiscardAll([this], effect)
    return [
        # CORRECTIF (10/10/2026) : « Attach to Cottonmouth. Otherwise, attach to
        # the villain. » Un OU de CardFinder pouvait choisir le mechant meme avec
        # Cottonmouth en jeu. Modele : 51040 Energy Truncheon. Le « +1★ ATK »
        # imprime vit dans data/cards.json (`ATK+`), comme 01100.
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name='Cottonmouth'), otherwise_attach_to=Villain),
        AbilityFactory.WhenUnitWouldAttackUnit(AbilityType.ForcedInterrupt, "AttachedCharacter", None, discard_tough),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, discard_this).SetCostFunc(CostFunc.Spend(Cost('BB'))),
    ]
