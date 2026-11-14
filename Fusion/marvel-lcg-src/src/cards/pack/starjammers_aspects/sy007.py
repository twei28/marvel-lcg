from . import *
# Life-Bonded Crewmates (Basic, evenement 1 [physical]). Team-Up (Corsair and Hepzibah). Max 1 per deck.
# Action: Heal 2 damage from Corsair and Hepzibah. Search your discard for an event and add it to your hand.
#
# Cartes de reference : hc020 Green Hell (`desc.TeamUp` + `.SetPlay().SetTarget("TeamUp")` obligatoire, fiche teamup.md) ; 12020 Swarm
# Tactics ; 45048 Triage (`HealthUnits`) ; 08011 / bp51014 (`Search.PlayerCard` + `GainCard`).
# « Action » : PAS « Hero Action » : jouable en forme heros comme en alter ego. « Heal 2 damage from Corsair AND Hepzibah » : 2 chacun.
# « Search your discard » : la DEFAUSSE seulement (pas le deck) ; « an event » : tout evenement, y compris celui-ci s'il y est deja.
def GetAbilities() -> Sequence['Ability']:
    def crewmates(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.HealthUnits(effect.targets, 2, effect)
        joueur = effect.GetInitiator()
        face = Search.PlayerCard(effect, joueur, include_player_deck=False, include_discard_pile=True, card_type=Event)
        if face:
            joueur.GainCard(face, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            crewmates,
        ).SetPlay().SetTarget("TeamUp"),
    ]
