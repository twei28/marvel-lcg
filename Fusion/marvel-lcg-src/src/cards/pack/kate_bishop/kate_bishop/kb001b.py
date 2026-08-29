from . import *

# * Kate Bishop
# Skillful — During deck building you may include SKILL cards from any
#   aspect. (Flavor uniquement : cette regle de construction de deck n'est
#   pas validee par le moteur cote serveur, cf. Cyclops 33001b qui porte la
#   meme clause sans code associe.)
# Action: Search your deck and discard pile for Kate's Bow and put it into
#   play. (Limit once per round.)
#
# Modele : Alexei Shostakov (red_guardian/rg001b), meme structure de
# recherche + mise en jeu directe, sans cout de ressource ici (contrairement
# a Rescue the Shield qui coute 1 ressource).


def GetAbilities() -> Sequence['Ability']:

    def kate_bishop(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            card_type=Upgrade,
            name=NOM_ARC,
        )
        if face:
            face.PutIntoPlay(initiator, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            kate_bishop,
        ).SetName("Search for Kate's Bow")
        .LimitOncePerRound(),
    ]
