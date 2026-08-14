from . import *

# * Spider-UK

def GetAbilities() -> Sequence['Ability']:

    def entree(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        # « Response: After Spider-UK enters play, give another WEB-WARRIOR
        # character a tough status card. If you cannot, discard cards from the
        # top of your deck until you discard an ally and add it to your hand. »
        this = effect.this.CastTo(Ally)
        joueur = effect.GetInitiator()

        camarades = [x for x in Worlds.GetOnFieldFriendlyCharacters(
            effect, CardFinder(trait="WEB-WARRIOR")) if x != this]
        if camarades:
            choisi = joueur.AskChooseFace(camarades, effect, prompt="Give a tough status card")
            Faces.GiveStatus([choisi or camarades[0]], "Tough", effect)
            return

        allie, _ = joueur.DiscardDeckUntil(effect, card_type=Ally)
        if allie:
            Faces.AddToHand([allie], joueur, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            entree
        ),
    ]
