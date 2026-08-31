from . import *

# Regained Youth — amelioration signature. CONDITION. Cout 2.
# You get +4 hit points.
# Response: After your deck runs out of cards, heal 2 damage from your
#   identity.
#
# Cartes de reference (RECETTES-MOTEUR §3) :
#  - +4 PV : an008 Siri's Dress, `GiveKeywordToAttached("You", health=4)` ;
#  - « after your deck runs out of cards » : 21068 Universal Church of Truth
#    (« After a player resets their deck »), `AfterDeckReset(...,
#    is_player_deck=True)` — c'est le MEME evenement moteur, le deck qui se
#    vide est aussitot reconstitue depuis la defausse.
#
# ⚠ « YOUR deck » : on filtre sur le proprietaire du deck reconstitue, pas
# sur le premier joueur.

def GetAbilities() -> Sequence['Ability']:

    def regained_youth(effect: 'Effect', message: 'Message.AfterDeckReset') -> None:
        this = effect.this.CastTo(Upgrade)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        identite = initiator.GetIdentity()
        if identite is not None:
            this.HealthUnits([identite], 2, effect)

    def mon_deck(effect: 'Effect') -> 'Deck':
        return effect.this.GetControlByPlayer().player_deck

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=4,
        ),
        AbilityFactory.AfterDeckReset(
            AbilityType.Response,
            mon_deck,
            regained_youth,
            is_player_deck=True,
        ),
    ]
