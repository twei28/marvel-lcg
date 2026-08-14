from . import *

# * The Lizard (A)

def GetAbilities() -> Sequence['Ability']:

    def formules(effect: 'Effect', face: 'CardFace') -> int:
        # « Each REPTILIAN enemy gets +1 ATK for each formula counter here. »
        this = effect.this.CastTo(CanPlaceCounter)
        return this.GetCounters('formula')

    def se_retourner(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        # « Forced Interrupt: When The Lizard would be defeated, instead:
        # discard each attachment from him, remove each formula counter from
        # here, place 1[per_hero] sanity counters on Lizard Brain, and flip this
        # card. »
        #
        # Meme piege que Shocker : les PV sont portes par la CARTE. On les lui
        # rend AVANT de retourner, puis on remet la nouvelle face a son maximum,
        # sans quoi Curt Connors arriverait deja vaincu et la boucle tournerait.
        this = effect.this.CastTo(EncounterVillain)
        message.SetBeInstead(effect)

        attaches = this.GetInventoryDeck().FindCards(card_type=Attachment)
        if attaches:
            Faces.DiscardAll(attaches, effect)
        Faces.RemoveCountersOn([this], "All", 'formula', effect)

        cerveau = LizardBrain(effect)
        if cerveau:
            Faces.PlaceCountersOn([cerveau], "1*", 'sanity', effect)

        this.ResetHealth(effect)
        this.card.Flip(effect)
        connors = this.card.face.CastTo(Villain)
        connors.ResetHealth(effect)

    return [
        # ⚠ Rend une LISTE d'abilites : sans l'etoile, le moteur plante des la
        # generation, et `test_cards` ne le voit pas.
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(trait="REPTILIAN", card_type=Enemy),
            get_new_value=formules,
            attack=1,
            change_on_event=OnEvent.Counter("This", 'formula'),
        ),
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.ForcedInterrupt,
            "This",
            se_retourner,
        ),
    ]
