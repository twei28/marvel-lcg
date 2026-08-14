from . import *

# * Electro (Francine Frye)

def GetAbilities() -> Sequence['Ability']:

    def attache_une_ressource(effect: 'Effect', message: 'Message.AfterMinionEngagePlayer') -> None:
        this = effect.this.CastTo(Minion)

        # « choose 1 card from your hand with a printed [energy] resource and
        # attach it to her. »
        joueur = message.GetToPlayer()
        cartes = CardFinder(has_printed_res="Y").Checks(joueur.hand_cards.Get())
        if not cartes:
            return
        choisie = joueur.AskChooseFace(cartes, effect, prompt="Attach to Electro")
        Faces.AttachAllTo([choisie or cartes[0]], this, effect)

    return [
        # « Electro gets +1 hit point for each [energy] resource attached to
        # her. » Les cartes attachees vivent dans la zone posee sous elle.
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui: len(CardFinder(has_printed_res="Y").Checks(
                effect.this.GetPlacedCardArea().Get())),
            health=1,
            change_on_event=OnEvent.PlacedCard("This"),
        ),
        AbilityFactory.AfterMinionEngagePlayer(
            AbilityType.ForcedResponse,
            "This",
            "You",
            attache_une_ressource
        ),
        AbilityFactory.AfterEnemyActivatesAgainstYou(
            AbilityType.ForcedResponse,
            "This",
            attache_une_ressource
        ),
    ]
