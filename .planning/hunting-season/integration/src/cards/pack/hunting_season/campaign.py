from . import *
from cards.pack.mts.campaign import WriteCampaignLogAtGameOver

HUNTER_ENVIRONMENTS = ('hs222', 'hs223', 'hs224', 'hs225', 'hs226')
ADDED_CARDS_KEY = 'Cards added to deck'
REMOVED_CARDS_KEY = 'Hero-specific cards removed'

def CampaignSetup(level: int) -> List['Ability']:
    def hunter_environment(effect, message):
        if CampaignLog.GetIntInternal('Hunter Mode', effect):
            card = CardFactory.GenerateCard(HUNTER_ENVIRONMENTS[level - 1], None, effect.world)
            card.face.PutIntoPlay('FirstPlayer', effect)

    def kraven_encounters(effect, message):
        for key, cid in [('Vermin escaped', 'hs204'), ('Lizard escaped', 'hs205')]:
            if CampaignLog.GetIntInternal(key, effect):
                card = CardFactory.GenerateCard(cid, None, effect.world)
                Faces.ShuffleAllTo([card.face], 'EncounterDeck', effect)
        for key, cid in [('Scorpion joined you', 'hs160'), ('Vulture joined you', 'hs158')]:
            if CampaignLog.GetIntInternal(key, effect):
                matches = [f for f in Worlds.GetEncounterDeckCards(effect)
                           if f.paper.card_id == cid]
                Faces.RemoveAllFromGame(matches, effect)

    def restore_added_cards(effect, message):
        for player in Worlds.GetPlayers(effect):
            ids = CampaignLog.GetListByPlayer(ADDED_CARDS_KEY, player.player_id, effect)
            if ids:
                # A_FAIRE_CLAUDE: inspect existing deck assembly first; generate
                # only missing copies, so UI campaign injection cannot duplicate them.
                pass
        # A_FAIRE_CLAUDE: remove exactly recorded hero-specific physical copies
        # in all modes, retaining their IDs and count in the persistent campaign.

    def collect(effect, message):
        # Outcome is on message.players_won; never on world.
        updates = {}
        if level == 1 and not message.players_won: updates['Vermin escaped'] = '1'
        if level == 2 and message.players_won: updates['Scorpion joined you'] = '1'
        if level == 3 and not message.players_won: updates['Lizard escaped'] = '1'
        if level == 4 and message.players_won:
            updates['Vulture joined you'] = '1'
            updates['Gibbon unlocked'] = '1'
        # A_FAIRE_CLAUDE: adapt reference/campaign_rules.py experience_awards
        # using live ending snapshot, then persist XP and capped base HP per player.
        # A_FAIRE_CLAUDE: choose reward owner (fewest OWNED PREDATOR allies on
        # scenarios 2-4; Master Hunter decides ties), and removals on losses 2/3.
        # A_FAIRE_CLAUDE: preserve snapshot before final villain leaves play.
        return updates

    abilities = [AbilityFactoryCampaign.WhenCampaignSetup(hunter_environment),
                 AbilityFactoryCampaign.WhenCampaignSetup(restore_added_cards)]
    if level == 5:
        abilities.insert(0, AbilityFactoryCampaign.WhenCampaignSetup(kraven_encounters))
    if level >= 2:
        abilities.append(AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP())
        # A_FAIRE_CLAUDE: in booklet order, offer one extra starting card for
        # 2 XP, restore expert HP, XP healing, random numbered expert-set card.
        # The generic obligation healer is insufficient without checking it
        # supports the minion and treachery contained in each four-card set.
    # A_FAIRE_CLAUDE: verify helper infers hs_* scenario IDs correctly; otherwise
    # use real supported explicit scenario_id signature from mts/campaign.py.
    abilities.append(WriteCampaignLogAtGameOver(collect))
    return abilities
