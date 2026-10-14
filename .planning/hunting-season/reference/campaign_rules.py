"""Pure campaign calculations. No game engine imports or invented game APIs.

This module is an integration reference. Claude supplies the end-of-game
snapshot from the real repository and persists the result atomically.
"""
from copy import deepcopy

LODGE_COSTS = {
    **{f'hs{n:03}': 4 for n in [164,165,166,167,184]},
    'hs168': 1,
    **{f'hs{n:03}': 2 for n in [*range(169,172), *range(178,184),
                               *range(185,191), *range(197,200)]},
    **{f'hs{n:03}': 1 for n in [*range(172,175), *range(194,197)]},
    **{f'hs{n:03}': 3 for n in [*range(175,178), *range(191,194)]},
}
REWARDS = {1:'hs200',2:'hs201',3:'hs202',4:'hs203'}
EXPERT_SETS = {n: tuple(f'hs{x:03}' for x in range(206+(n-1)*4,210+(n-1)*4))
               for n in range(1,5)}

def initial_state(identities, master_hunter, *, expert=False, hunter=False):
    if not 1 <= len(identities) <= 4:
        raise ValueError('Campaign requires 1 to 4 players')
    if master_hunter not in identities:
        raise ValueError('Master Hunter must be a campaign player')
    if hunter and not expert:
        raise ValueError('Hunter mode requires expert campaign')
    return {
        'expert':expert,'hunter':hunter,'master_hunter':master_hunter,
        'next_scenario':1,'finished':False,'won':None,
        'flags':{'Vermin escaped':False,'Scorpion joined you':False,
                 'Lizard escaped':False,'Vulture joined you':False,'Gibbon unlocked':False},
        'stock':[f'hs{n:03}' for n in range(164,200) if n != 168],
        'players':{p:{'identity':identity,'number':i+1,'xp':0,'remaining_hp':None,
                      'added':[],'removed':[],'expert_available':list(EXPERT_SETS[i+1])}
                   for i,(p,identity) in enumerate(identities.items())},
    }

def experience_awards(level, won, hunter, snapshot):
    """snapshot: players[id]={rat_minions,hp,max_hp}; plus scheme_stage,
    jameson_wounds, tail_set_aside, reptile_attachments, main_threat as needed.
    HP/max_hp are live ending HP, not the base-HP cap used for persistence.
    """
    players=snapshot['players'];n=len(players)
    if level not in range(1,6) or not 1 <= n <= 4:
        raise ValueError('Invalid scenario/player count')
    if level==5:return {p:0 for p in players}
    common=3 if won else 2
    if hunter and won:common+=1
    if level==1:
        if won and snapshot['scheme_stage']==1:common+=1
        return {p:common+int(row['rat_minions']==0) for p,row in players.items()}
    if level==2:
        if won and snapshot['jameson_wounds']<=1:common+=1
        if snapshot['tail_set_aside']:common+=1
    if level==3:
        if snapshot['scheme_stage'] in (1,2):common+=1
        if snapshot['reptile_attachments']<n:common+=1
    if level==4:
        if snapshot['main_threat']<7*n:common+=1
        return {p:common+int(2*row['hp']>=row['max_hp']) for p,row in players.items()}
    return {p:common for p in players}

def eligible_reward_owners(level, players):
    """Each row contains the count of PREDATOR allies OWNED, not merely in play."""
    if level==1:return list(players)
    low=min(row['predator_allies_owned'] for row in players.values())
    return [p for p,row in players.items() if row['predator_allies_owned']==low]

def finish_scenario(state, level, won, snapshot, *, reward_owner=None,
                    removed_cards=None):
    result=deepcopy(state)
    if result['finished'] or level!=result['next_scenario']:
        raise ValueError('Scenario already resolved or out of order')
    if set(snapshot['players']) != set(result['players']):
        raise ValueError('Snapshot must contain every campaign player')
    awards=experience_awards(level,won,result['hunter'],snapshot)
    if level<5 and won:
        if reward_owner not in eligible_reward_owners(level,snapshot['players']):
            raise ValueError('Choose a valid reward owner; Master Hunter decides ties')
        result['players'][reward_owner]['added'].append(REWARDS[level])
    if not won and level in (2,3):
        # Claude validates each supplied ID against that player's hero-specific
        # cards and checks the physical copy remains available. No guessed IDs.
        if removed_cards is None or set(removed_cards)!=set(result['players']):
            raise ValueError('Each player must choose one hero-specific card to remove')
        for p,cid in removed_cards.items():
            if not isinstance(cid,str) or not cid:raise ValueError('Missing removed card ID')
            result['players'][p]['removed'].append(cid)
    for p,row in result['players'].items():
        row['xp']+=awards[p]
        if result['expert']:
            snap=snapshot['players'][p]
            row['remaining_hp']=max(0,min(snap['hp'],snap['base_hp']))
    flags=result['flags']
    if level==1 and not won:flags['Vermin escaped']=True
    if level==2 and won:flags['Scorpion joined you']=True
    if level==3 and not won:flags['Lizard escaped']=True
    if level==4 and won:
        flags['Vulture joined you']=True
        flags['Gibbon unlocked']=True
        if 'hs168' not in result['stock']:result['stock'].append('hs168')
    if level==5:result['finished']=True;result['won']=bool(won)
    else:result['next_scenario']=level+1
    return result

def buy_lodge(state, player, card_id):
    result=deepcopy(state)
    if result['finished'] or result['next_scenario']==1:
        raise ValueError('Lodge is only visited between scenarios')
    if card_id not in result['stock']:raise ValueError('This physical copy is unavailable')
    row=result['players'][player];cost=LODGE_COSTS[card_id]
    if row['xp']<cost:raise ValueError('Insufficient experience')
    row['xp']-=cost;row['added'].append(card_id);result['stock'].remove(card_id)
    return result

def prepare_player(state, player, *, extra_start_card=False, heal_xp=0,
                   expert_card=None, base_hp):
    """One setup transaction: extra card, restored HP, XP healing, expert card.
    Claude invokes once per scenario/player; persist a setup marker atomically.
    expert_card is selected randomly from expert_available by the engine/UI.
    """
    result=deepcopy(state);row=result['players'][player]
    if result['finished'] or result['next_scenario']<=1:
        raise ValueError('No inter-scenario setup available')
    if not isinstance(heal_xp,int) or isinstance(heal_xp,bool) or heal_xp<0:
        raise ValueError('Healing XP must be a nonnegative integer')
    if not result['expert'] and (heal_xp or expert_card):
        raise ValueError('Healing purchases require expert campaign')
    spent=(2 if extra_start_card else 0)+heal_xp
    if spent>row['xp']:raise ValueError('Insufficient experience')
    hp=min(base_hp,row['remaining_hp']+heal_xp) if result['expert'] else base_hp
    if expert_card is not None:
        if expert_card not in row['expert_available']:
            raise ValueError('Expert card unavailable or belongs to a different player')
        row['expert_available'].remove(expert_card);row['added'].append(expert_card);hp=base_hp
    if hp<=0:raise ValueError('Defeated player must restore HP before rejoining')
    row['xp']-=spent
    return result,{'starting_hp':hp,'extra_start_cards':int(extra_start_card)}

def kraven_changes(state):
    flags=state['flags']
    return {'add':[cid for flag,cid in [('Vermin escaped','hs204'),('Lizard escaped','hs205')] if flags[flag]],
            'remove':[cid for flag,cid in [('Scorpion joined you','hs160'),('Vulture joined you','hs158')] if flags[flag]]}
