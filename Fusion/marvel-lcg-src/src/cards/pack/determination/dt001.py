from . import *

# * Cable

def GetAbilities() -> Sequence['Ability']:

    # « Reckless » n'a aucun crochet dans le moteur : le mot-cle est ecrit en
    # clair, tel que la carte le rappelle elle-meme entre parentheses. Les trois
    # autres cartes Reckless de l'aspect reprendront ces quatre lignes.
    def reckless(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        this.PlaceThreatOnSchemes("EachScheme", 1, effect)

    def cable(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)

        initiator = effect.GetInitiator()
        faces = initiator.DiscardHandCards((0, "All"), effect)
        if faces:
            this.GainForThisActive(effect, message, attack=len(faces))

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            reckless
        ),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.Interrupt,
            "This",
            cable
        ),
    ]
