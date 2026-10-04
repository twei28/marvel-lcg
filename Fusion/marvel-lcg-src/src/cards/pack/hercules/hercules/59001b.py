from . import *
def GetAbilities() -> Sequence['Ability']:
    def with_labor_and_gift_decks(effect: 'Effect', message: 'Message.WhenPlayerSelectHero') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)
        initiator = effect.GetInitiator()
        faces = list(initiator.set_aside_deck.Get()) + list(initiator.additional_discard_pile.Get())
        gifts = [f for f in faces if f.HasTrait('GIFT')]
        labors = [f for f in faces if f.HasTrait('LABOR')]
        Faces.FlipAllTo(gifts + labors, False, effect)
        Faces.MoveAllTo(labors + gifts, initiator.additional_deck, effect)
        # Encart du pack : « shuffle the three gift cards together to form the
        # gift deck and the three labor cards to form the labor deck ». Les deux
        # decks partagent le deck annexe et leur dessus se cherche PAR TRAIT
        # (`GetAdditionalDeckTop`) : melanger le tout melange chacun des deux.
        # Oubli signale en jeu le 04/10/2026 (« toujours dans le meme ordre »).
        initiator.additional_deck.Shuffle(effect)
    def new_labors(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)
        initiator = effect.GetInitiator()
        face = GetAdditionalDeckTop(initiator, 'LABOR')
        if face:
            face.Reveal(initiator, effect)
    def check_no_labor(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        if (Worlds.FindCardOnField(effect, trait='LABOR') != None):
            return False
        initiator = effect.GetInitiator()
        if not initiator:
            return False
        return (GetAdditionalDeckTop(initiator, 'LABOR') != None)
    return [AbilityFactory.BeginGameWithSetAside([*LABOR_IDS, *GIFT_IDS], with_labor_and_gift_decks),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, new_labors, conditions=[check_no_labor]).SetName('New Labors of Hercules')]
