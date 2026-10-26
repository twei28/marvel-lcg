from . import *

# * Marvel Girl (Rachel Summers) — HEROS. THW 3, ATK 1, DEF 2, HS 4, PV 10. PSIONIC. X-FORCE.
# Chronoskimming — Response: After your turn begins, shuffle your hand into your deck -> draw a new hand.
# Reduce the cost of the next card you play this turn by 1.
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - « After your turn begins » : `22001a` Nebula (`AfterPlayerTurnBegin`), `03019` Quinjet.
#  - melanger dans le deck : `14007` Serval Industries (`Faces.ShuffleAllTo(faces, joueur.player_deck, effect)`).
#  - reduire le cout de la prochaine carte : `05008` Nakia Bahadir (`Worlds.UpdateNextCardPlayCost(.., in_this="Phase")`) ;
#    ici « this turn » -> `in_this="Turn"`.
#
# MOTS-PIEGES
#  - « shuffle your hand into your deck -> draw a new hand » : la fleche annonce un COUT (remelanger), puis « draw a new
#    hand » = piocher jusqu'a la taille de main (`DrawUp("Max")`, qui tient compte de la taille de main reduite).
#  - le nom de la capacite (« Chronoskimming ») est LU par Temporal Retrieval (rm010) : ne pas le changer.
def GetAbilities() -> Sequence['Ability']:
    def chronoskimming(effect: 'Effect', message: 'Message.AfterPlayerTurnBegin') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)
        joueur = effect.GetInitiator()
        main = list(joueur.hand_cards.Get())
        if main:
            Faces.ShuffleAllTo(main, joueur.player_deck, effect)
        joueur.DrawUp("Max", effect)
        Worlds.UpdateNextCardPlayCost(joueur, -1, effect, in_this="Turn")

    return [
        AbilityFactory.AfterPlayerTurnBegin(
            AbilityType.Response,
            "You",
            chronoskimming,
        ).SetName("Chronoskimming"),
    ]
