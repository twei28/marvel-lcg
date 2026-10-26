"""Campagne « Hellfire Hunt » (Dipsome) : FONDATIONS COMMUNES aux cinq scenarios (mise en place de campagne, releve du carnet).

Livret : p.5-7 (regles de campagne, Setup commun), p.24 (carnet), instructions de campagne de chaque scenario (voir
docs/rapports/2026-10-26-hellfire-hunt-lecture-livret.md §2-§3 et docs/packs/hellfire-hunt/GABARITS.md).

Ce module ne contient QUE ce qui est commun a plusieurs scenarios. Chaque scenario l'appelle depuis sa manigance principale 1A :
    from cards.pack.hellfire_hunt.campaign import CampaignSetup
    ... return [..., *CampaignSetup(level)]
(modele : `cards.pack.skrull_menace.campaign.CampaignSetup`).

Mise en place commune (`MiseEnPlace(level)`, une seule capacite pour que l'ordre soit celui du livret) :
  1. les 16 allies RECRUITED sont mis de cote (zone « mise de cote » du scenario : les manigances POTENTIAL ALLY les y cherchent), SAUF ceux que le
     carnet note deja : ils rejoignent le deck Recruited Mutants (E2, `__init__.py`) ;
  2. les manigances POTENTIAL ALLY : 1 par joueur, tiree au hasard parmi celles que le carnet n'a pas retirees, est melangee dans le deck de
     rencontre (E3) ;
  3. campagne experte, scenarios 2 a 5 : PV restants et soin par pion Acceleration (livret p.6).
Ce qui est PROPRE a un scenario (reveler Cerebro Insights au 1, Rally the Survivors et le retrait de Xavier's Institute au 5, mise en jeu de
l'environnement Xavier's Institute aux scenarios 1 a 4, Emma Frost's Redemption / Cryptic Threatening Message au 3...) est decrit par
`ETAPES_PAR_SCENARIO` et appliquee par `EtapesDuScenario(level)` : les scripts de scenario (autre agent) ne font qu'appeler `CampaignSetup`.

Cles du carnet (toutes declarees dans `data/campagnes/hellfire_hunt.json`) :
  - `Recruited Allies` : ids des allies Recruited gagnes (liste) ;
  - `Removed Potential Allies` : ids des manigances POTENTIAL ALLY vaincues (retirees de la campagne) ;
  - `Removed Campaign Cards` : ids retires de la campagne par leur texte (Tactical Help, Enemy Of Enemy) ;
  - `Emma Frost's Redemption: Defeated`, `Cryptic Threatening Message: Defeated` : cases ;
  - `Player N Remaining hit points`, `Player N Identity` (communes a toutes les boites).
"""
from cards.pack import *
from cards.pack.mts.campaign import WriteCampaignLogAtGameOver, FaceExists
from . import RecruitedMutants, AjouterAuxRecrutes

SEP = ';'

# Les cinq scenarios, dans l'ordre du livret. C'est aussi l'estampille du carnet sortant (le panneau de recompenses ignore tout releve dont
# l'estampille differe de l'id du scenario de `data/campagnes/hellfire_hunt.json`).
SCENARIOS = ['hellfire_white_queen', 'hellfire_black_king', 'hellfire_black_queen', 'hellfire_torn', 'hellfire_cassandra_nova']

CLE_RECRUTES = 'Recruited Allies'
CLE_PA_RETIRES = 'Removed Potential Allies'
CLE_RETIREES = 'Removed Campaign Cards'
CLE_EMMA = "Emma Frost's Redemption: Defeated"
CLE_CRYPTIC = 'Cryptic Threatening Message: Defeated'

# Les 16 allies RECRUITED (hf013-hf028), dans l'ordre du dossier.
ALLIES = ['hf013', 'hf014', 'hf015', 'hf016', 'hf017', 'hf018', 'hf019', 'hf020', 'hf021', 'hf022', 'hf023', 'hf024', 'hf025', 'hf026', 'hf027', 'hf028']
EMMA_FROST = 'hf025'
# Les 12 manigances POTENTIAL ALLY (hf029-hf040).
POTENTIAL_ALLY = ['hf029', 'hf030', 'hf031', 'hf032', 'hf033', 'hf034', 'hf035', 'hf036', 'hf037', 'hf038', 'hf039', 'hf040']
# Cartes de campagne : manigances annexes numerotees du livret et l'environnement.
CEREBRO_INSIGHTS, EMMAS_REDEMPTION, CRYPTIC_MESSAGE = 'hf041', 'hf042', 'hf043'
PSYCHIC_MINEFIELD, RALLY_THE_SURVIVORS, TACTICAL_HELP, ENEMY_OF_ENEMY = 'hf044', 'hf045', 'hf046', 'hf047'
XAVIERS_INSTITUTE = 'hf048'


def _liste(effect: 'Effect', cle: str) -> List[str]:
    return CampaignLog.GetListInternal(cle, effect)


def _generer(effect: 'Effect', card_id: str) -> 'CardFace':
    return CardFactory.GenerateCard(card_id, None, effect.world).face


def _mettre_de_cote(effect: 'Effect', card_id: str) -> 'CardFace':
    """Une carte creee directement dans la zone « mise de cote » du scenario (modele skrull_menace/campaign.py)."""
    return CardFactory.GenerateCard(card_id, effect.world.aside_deck, effect.world).face


# ----------------------------------------------------------------------------- les trois pas communs
def _allies_recrutes(effect: 'Effect') -> None:
    """Pas 1. Les allies deja gagnes forment le deck Recruited Mutants ; les autres attendent de cote."""
    gagnes = [i for i in _liste(effect, CLE_RECRUTES) if i in ALLIES]
    RecruitedMutants(effect)                       # le deck existe meme vide (Xavier's Institute / Rally the Survivors le tiennent)
    faces = [CardFactory.GenerateCard(i, None, effect.world).face for i in gagnes]
    if faces:
        AjouterAuxRecrutes(effect, faces)
    for card_id in ALLIES:
        if card_id not in gagnes:
            _mettre_de_cote(effect, card_id)


def _potential_allies(effect: 'Effect') -> None:
    """Pas 2. Une manigance POTENTIAL ALLY par joueur, au hasard parmi celles qui n'ont pas quitte la campagne."""
    from engine.lib import Random
    disponibles = [i for i in POTENTIAL_ALLY if i not in _liste(effect, CLE_PA_RETIRES)]
    for _ in Worlds.GetPlayers(effect):
        if not disponibles:
            break
        choisie = Random.RandomChoice(disponibles)
        disponibles.remove(choisie)
        Faces.ShuffleAllTo([_generer(effect, choisie)], "EncounterDeck", effect)


def _campagne_experte(effect: 'Effect') -> None:
    """Pas 3 (livret p.6) : PV restants persistants, soin complet par un pion Acceleration sur la manigance principale."""
    this = effect.this
    for player in Worlds.GetPlayers(effect):
        identity = player.GetIdentity()
        restants = CampaignLog.GetIntByPlayer('Remaining hit points', player.player_id, effect)
        if restants > 0:
            identity.SetHealth(min(restants, identity.max_health), effect)
        if identity.health >= identity.max_health:
            continue

        def soigner(targets: Sequence['CardFace'], this=this, identity=identity) -> None:
            this.PlaceTokensInternal(1, 'acceleration_token', effect)
            identity.CastTo(CanHealth).HealHealth('All', effect)
        player.MayChooseOneAbility(effect, AbilityFactory.ForChoiceAbility(
            'Place 1 acceleration token on the main scheme to heal to full', soigner))


# Etapes PROPRES a un scenario, d'apres le livret (docs/rapports/2026-10-26-hellfire-hunt-lecture-livret.md §3). Les etapes de scenario sont
# des sequences de couples (verbe, carte) lues par `EtapesDuScenario`. Les scenarios 2 (Black King) et 4 (Torn) n'ont ICI que les pas communs :
# leurs instructions de campagne propres relevent du scenario.
ETAPES_PAR_SCENARIO = {
    1: [('reveler', CEREBRO_INSIGHTS), ('en_jeu', XAVIERS_INSTITUTE)],
    2: [('en_jeu', XAVIERS_INSTITUTE)],
    3: [('en_jeu', XAVIERS_INSTITUTE), ('emma_ou_message', None)],
    4: [('en_jeu', XAVIERS_INSTITUTE)],
    5: [('melanger_rencontre', TACTICAL_HELP), ('melanger_rencontre', ENEMY_OF_ENEMY), ('reveler', RALLY_THE_SURVIVORS), ('emma_dans_recrutes', None)],
}


def EtapesDuScenario(effect: 'Effect', level: int) -> None:
    for verbe, carte in ETAPES_PAR_SCENARIO.get(level, []):
        if verbe == 'reveler':
            _generer(effect, carte).Reveal(effect.world.GetFirstPlayer(), effect)
        elif verbe == 'en_jeu':
            _generer(effect, carte).PutIntoPlay("FirstPlayer", effect)
        elif verbe == 'melanger_rencontre':
            Faces.ShuffleAllTo([_generer(effect, carte)], "EncounterDeck", effect)
        elif verbe == 'emma_ou_message':
            # Scenario 3 : « si Emma Frost's Redemption n'est pas cochee, la reveler ; sinon melanger Emma Frost dans le deck Recruited Mutants
            # et reveler Cryptic Threatening Message ».
            if CampaignLog.GetStrInternal(CLE_EMMA, effect):
                AjouterAuxRecrutes(effect, [_generer(effect, EMMA_FROST)])
                _generer(effect, CRYPTIC_MESSAGE).Reveal(effect.world.GetFirstPlayer(), effect)
            else:
                _generer(effect, EMMAS_REDEMPTION).Reveal(effect.world.GetFirstPlayer(), effect)
        elif verbe == 'emma_dans_recrutes':
            if not CampaignLog.GetStrInternal(CLE_EMMA, effect):
                AjouterAuxRecrutes(effect, [_generer(effect, EMMA_FROST)])


def Executer(effect: 'Effect', level: int) -> None:
    """Le corps de la mise en place de campagne (sorti de la capacite pour que le banc de test le joue sans lancer de campagne)."""
    _allies_recrutes(effect)
    _potential_allies(effect)
    EtapesDuScenario(effect, level)
    if level >= 2 and Worlds.IsExpert(effect):
        _campagne_experte(effect)


def MiseEnPlace(level: int) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        Executer(effect, level)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


# -------------------------------------------------------------------- releve --
def Releve(level: int, effect: 'Effect', message: 'Message.WhenGameOver') -> dict:
    """Ce que le livret fait noter a la VICTOIRE du scenario (a la defaite : on rejoue sans penalite, rien n'est note)."""
    if not message.players_won:
        return {}
    updates: Dict[str, Any] = {}
    world = effect.world

    # --- Campagne experte : PV restants (plafonnes aux PV de base)
    for player in world.const_seat_order_players:
        identity = player.GetIdentity()
        if identity and not player.is_eliminated:
            updates[f'Player {player.player_id + 1} Remaining hit points'] = str(max(0, min(identity.health, identity.printed_health)))

    # --- Allies Recruited en jeu a la fin : gagnes (jamais perdus), ajoutes a la liste
    recrutes = list(_liste(effect, CLE_RECRUTES))
    for card_id in ALLIES:
        if card_id not in recrutes and (FaceExists(effect, card_id, in_play=True) or FaceExists(effect, card_id, in_victory=True)):
            recrutes.append(card_id)
    updates[CLE_RECRUTES] = SEP.join(recrutes)

    # --- Manigances POTENTIAL ALLY dans la pile de victoire : retirees de la campagne
    retirees = list(_liste(effect, CLE_PA_RETIRES))
    for card_id in POTENTIAL_ALLY:
        if card_id not in retirees and FaceExists(effect, card_id, in_victory=True):
            retirees.append(card_id)
    updates[CLE_PA_RETIRES] = SEP.join(retirees)

    # --- Textes « Remove this card from the campaign » (Tactical Help, Enemy Of Enemy)
    hors = list(_liste(effect, CLE_RETIREES))
    for card_id in (TACTICAL_HELP, ENEMY_OF_ENEMY):
        if card_id not in hors and FaceExists(effect, card_id, in_victory=True):
            hors.append(card_id)
    updates[CLE_RETIREES] = SEP.join(hors)

    # --- Les deux cases « defaite » du carnet
    if FaceExists(effect, EMMAS_REDEMPTION, in_victory=True):
        updates[CLE_EMMA] = '1'
    if FaceExists(effect, CRYPTIC_MESSAGE, in_victory=True):
        updates[CLE_CRYPTIC] = '1'
    return updates


def CampaignSetup(level: int) -> 'List[Ability]':
    """Ce que la manigance principale 1A du scenario `level` (1 a 5) doit appeler."""
    return [
        MiseEnPlace(level),
        WriteCampaignLogAtGameOver(lambda effect, message: Releve(level, effect, message), scenario_id=SCENARIOS[level - 1]),
    ]
