from . import *

# Alien Onslaught — MANIGANCE ANNEXE. Menace 4 (fixe). Boost 2.
# Hinder 2[per_hero].
# When Revealed: Each player discards the top 2[per_hero] of their deck. Place 1 acceleration token here for each [[XENOMORPH]] minion
#   discarded this way.
# Forced Response: After you thwart this scheme, discard the top 2[per_hero] cards of your deck.
#
# Cartes de reference : `DiscardDeckTopCards(n)` ; jeton d'acceleration sur une manigance : `PlaceAccelerationToken` ; « After you thwart
#   this scheme » : `AfterUnitThwartScheme(ForcedResponse, Unit2, "This")` (le contreur est une carte du joueur : « you »).
#
# ⚠ Mots-pieges :
#  - un Alien Scout atteint par la defausse COMPTE pour un jeton ET est distribue face cachee (arbitrage 4 du 25/10/2026) : la Scout le
#    signale sur l'effet (`_ap_scouts_interceptes`) ;
#  - « EACH player » : chacun son deck ; 2[per_hero] = 2 x joueurs ;
#  - « After YOU thwart » : contrecarrer (THW, pas un retrait de menace par une carte de rencontre).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)
        effect._ap_scouts_interceptes = 0
        jetons = 0
        for joueur in Worlds.GetPlayers(effect):
            defaussees = joueur.DiscardDeckTopCards(2 * NombreDeJoueurs(effect), effect)
            jetons += sum(1 for f in defaussees if Minion.IsType(f) and f.HasTrait("XENOMORPH") and f.card.area.flags.is_discards)
        jetons += getattr(effect, "_ap_scouts_interceptes", 0)
        if jetons > 0:
            this.PlaceAccelerationToken(jetons, effect)

    def contrecarree(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> None:
        joueur = message.trigger.GetControlByOrOwner()
        if not Player.IsType(joueur):
            return
        joueur.DiscardDeckTopCards(2 * NombreDeJoueurs(effect), effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.AfterUnitThwartScheme(AbilityType.ForcedResponse, Unit2, "This", contrecarree),
    ]
