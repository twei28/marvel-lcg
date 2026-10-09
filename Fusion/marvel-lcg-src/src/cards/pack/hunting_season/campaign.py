"""Campagne « Hunting Season » (Nugget, livret p.2-12) : mise en place et releve.

Cles du carnet (comparees par `tools/verifier_campagnes.py` a
`data/campagnes/hunting_season.json`) :
  - par joueur (« Player N <cle> ») : "Experience" (solde), "Cards added to deck"
    (ids, recompenses, achats du Lodge, cartes du set expert), "Hero-specific
    cards removed" (ids retires pour toute la campagne), "Hero-specific cards to
    remove" (penalite en attente, appliquee a la mise en place suivante),
    "Remaining hit points" (campagne experte) ;
  - communes : "Vermin escaped", "Scorpion joined you", "Lizard escaped",
    "Vulture joined you", "Gibbon unlocked", "Hunter Mode", "Master Hunter".

Les depenses de mise en place (2 XP pour une carte de plus, XP contre des soins)
sont DEBITEES dans le store du monde : `WriteCampaignLogAtGameOver` le recopie
au carnet sortant, et le releve ajoute les gains a ce solde-la.

Decision de l'utilisateur (09/10/2026, POINTS_OUVERTS n°8) : une defaite aux
scenarios 1 a 4 fait continuer la campagne ; seul Kraven decide de sa fin.
"""
from cards.pack import *
from cards.pack.mts.campaign import WriteCampaignLogAtGameOver, ActiveMainSchemeStartswith

SCENARIOS = ('hs_vermin', 'hs_scorpion', 'hs_the_lizard', 'hs_vulture', 'hs_kraven_the_hunter')
HUNTER_ENVIRONMENTS = ('hs222', 'hs223', 'hs224', 'hs225', 'hs226')
REWARDS = {1: 'hs200', 2: 'hs201', 3: 'hs202', 4: 'hs203'}
EXPERT_SETS = {n: tuple(f'hs{x:03}' for x in range(206 + (n - 1) * 4, 210 + (n - 1) * 4)) for n in range(1, 5)}

CLE_XP = 'Experience'
CLE_AJOUTS = 'Cards added to deck'
CLE_RETIREES = 'Hero-specific cards removed'
CLE_A_RETIRER = 'Hero-specific cards to remove'
CLE_PV = 'Remaining hit points'
CLE_HUNTER = 'Hunter Mode'
CLE_MASTER = 'Master Hunter'
SEP = ';'


def CleJoueur(player: 'Player', cle: str) -> str:
    return f'Player {player.player_id + 1} {cle}'


def _liste(effect: 'Effect', cle: str) -> List[str]:
    return CampaignLog.GetListInternal(cle, effect)


def _entier(effect: 'Effect', cle: str) -> int:
    try:
        return CampaignLog.GetIntInternal(cle, effect)
    except ValueError:
        return 0


def Experience(effect: 'Effect', player: 'Player') -> int:
    return _entier(effect, CleJoueur(player, CLE_XP))


def PoserExperience(effect: 'Effect', player: 'Player', valeur: int) -> None:
    CampaignLog.SetStr(CleJoueur(player, CLE_XP), str(max(0, valeur)), effect.world)


def Ajouts(effect: 'Effect', player: 'Player') -> List[str]:
    return _liste(effect, CleJoueur(player, CLE_AJOUTS))


def PoserAjouts(effect: 'Effect', player: 'Player', ids: List[str]) -> None:
    CampaignLog.SetStr(CleJoueur(player, CLE_AJOUTS), SEP.join(ids), effect.world)


def ModeHunter(effect: 'Effect') -> bool:
    return Worlds.IsExpert(effect) and _entier(effect, CLE_HUNTER) > 0


def MaitreChasseur(effect: 'Effect') -> int:
    """Siege (1 a 4) du Master Hunter ; le joueur 1 tant que rien n'est note."""
    return _entier(effect, CLE_MASTER) or 1


# ---------------------------------------------------------- mise en place --

def EnvironnementHunter(level: int) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        if not ModeHunter(effect):
            return
        card = CardFactory.GenerateCard(HUNTER_ENVIRONMENTS[level - 1], None, effect.world)
        card.face.PutIntoPlay('FirstPlayer', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


def CartesAjoutees() -> 'Ability':
    """Les cartes gagnees vivent au carnet, pas dans le deck enregistre : le
    moteur les remet a chaque mise en place (modele `gmw`, cartes du Marche)."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        for player in Worlds.GetPlayers(effect):
            ids = Ajouts(effect, player)
            if not ids:
                continue
            for card_id in ids:
                CardFactory.GenerateCard(card_id, player.player_deck, effect.world)
            player.player_deck.Shuffle(effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


def _cartes_du_heros(player: 'Player') -> List['CardFace']:
    zones = list(player.player_deck.Get(True)) + list(player.hand_cards.Get(True))
    return [f for f in zones if ClassCard.IsType(f) and f.CastTo(ClassCard).IsClass('IdentitySpecific')]


def CartesSpecifiquesRetirees() -> 'Ability':
    """Defaites aux scenarios 2 et 3 : « Each player must remove 1 hero-specific
    card from their deck from the game ». Le choix se fait a la mise en place
    suivante (le carnet note la penalite en attente) ; l'id choisi rejoint la
    liste des retraits, rejouee a chaque scenario d'apres."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        for player in Worlds.GetPlayers(effect):
            retirees = _liste(effect, CleJoueur(player, CLE_RETIREES))
            restantes = list(retirees)
            for face in list(player.player_deck.Get(True)):
                if face.paper.card_id in restantes:
                    restantes.remove(face.paper.card_id)
                    Faces.RemoveAllFromGame([face], effect)
            a_choisir = _entier(effect, CleJoueur(player, CLE_A_RETIRER))
            for _ in range(a_choisir):
                candidates = _cartes_du_heros(player)
                if not candidates:
                    break
                choisie = player.AskChooseFace(candidates, effect) if len(candidates) > 1 else candidates[0]
                if choisie is None:
                    choisie = candidates[0]
                retirees.append(choisie.paper.card_id)
                Faces.RemoveAllFromGame([choisie], effect)
            if a_choisir:
                CampaignLog.SetStr(CleJoueur(player, CLE_RETIREES), SEP.join(retirees), effect.world)
                CampaignLog.SetStr(CleJoueur(player, CLE_A_RETIRER), '0', effect.world)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


def ChangementsDeKraven() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        for key, cid in [('Vermin escaped', 'hs204'), ('Lizard escaped', 'hs205')]:
            if _entier(effect, key):
                card = CardFactory.GenerateCard(cid, None, effect.world)
                Faces.ShuffleAllTo([card.face], 'EncounterDeck', effect)
        for key, cid in [('Scorpion joined you', 'hs160'), ('Vulture joined you', 'hs158')]:
            if _entier(effect, key):
                matches = [f for f in Worlds.GetEncounterDeckCards(effect) if f.paper.card_id == cid]
                if matches:
                    Faces.RemoveAllFromGame(matches, effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


def CarteDeDepartEnPlus() -> List['Ability']:
    """« Each player may spend 2 Experience to increase their starting hand size
    by 1. The additional card is only drawn during setup. » La mise en place de
    campagne (etape 13) precede la pioche (etape 14) : +1 main le temps de la
    pioche et des mulligans, retire ensuite."""
    def offrir(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        for player in Worlds.GetPlayers(effect):
            if Experience(effect, player) < 2:
                continue

            def prendre(cibles: Sequence['CardFace'], player: 'Player'=player) -> None:
                PoserExperience(effect, player, Experience(effect, player) - 2)
                player.GetIdentity().Gain(effect, 1, hand_size=1)
                Stores.SetStr(f'_hs_main_en_plus_{player.player_id}', '1', effect)

            player.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility('Spend 2 Experience to increase your starting hand size by 1', prendre),
            )

    def rendre(effect: 'Effect', message: 'Message.WhenCampaignSetupAfterMulligans') -> None:
        for player in Worlds.GetPlayers(effect):
            cle = f'_hs_main_en_plus_{player.player_id}'
            if Stores.HasKey(cle, effect) and Stores.GetStr(cle, effect) == '1':
                player.GetIdentity().Gain(effect, -1, hand_size=1)
                Stores.SetStr(cle, '0', effect)

    return [AbilityFactoryCampaign.WhenCampaignSetup(offrir),
            AbilityFactoryCampaign.WhenCampaignSetupAfterMulligans(rendre)]


def PointsDeVieExperts() -> 'Ability':
    """Campagne experte, dans l'ordre du livret : PV notes, puis 1 XP = 1 soin,
    puis une carte aleatoire de SON set expert pour revenir au maximum. Un joueur
    vaincu (PV notes a 0) doit prendre la carte pour rejoindre ses equipiers."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        for player in Worlds.GetPlayers(effect):
            identite = player.GetIdentity()
            cle_pv = CleJoueur(player, CLE_PV)
            note = CampaignLog.GetStrInternal(cle_pv, effect)
            vaincu = note == '0'
            if note and not vaincu:
                identite.SetHealth(int(note), effect)

            if not vaincu:
                while Experience(effect, player) > 0 and identite.GetLostHealth() > 0:
                    pris = []

                    def soigner(cibles: Sequence['CardFace'], player: 'Player'=player, identite: 'CardFace'=identite) -> None:
                        PoserExperience(effect, player, Experience(effect, player) - 1)
                        identite.CastTo(CanHealth).HealHealth(1, effect)
                        pris.append(True)

                    player.MayChooseOneAbility(
                        effect, AbilityFactory.ForChoiceAbility('Spend 1 Experience to heal 1 damage', soigner))
                    if not pris:
                        break

            numero = (player.player_id % 4) + 1
            ajouts = Ajouts(effect, player)
            restantes = [x for x in EXPERT_SETS[numero] if x not in ajouts]
            if not restantes or (not vaincu and identite.GetLostHealth() == 0):
                continue

            def ajouter(cibles: Sequence['CardFace'], player: 'Player'=player, identite: 'CardFace'=identite,
                        restantes: List[str]=restantes) -> None:
                card_id = Rand.RandomChoice(restantes, effect)
                PoserAjouts(effect, player, Ajouts(effect, player) + [card_id])
                CardFactory.GenerateCard(card_id, player.player_deck, effect.world)
                player.player_deck.Shuffle(effect)
                identite.CastTo(CanHealth).HealHealth('All', effect)

            if vaincu:
                ajouter([])
            else:
                player.MayChooseOneAbility(
                    effect,
                    AbilityFactory.ForChoiceAbility(
                        'Add 1 random card from your expert campaign set to your deck to heal to full', ajouter))
    return AbilityFactoryCampaign.WhenCampaignSetupExpertOnly(action)


# ------------------------------------------------------------------ releve --

def _gagnee(message: 'Message.WhenGameOver') -> bool:
    # Le resultat est sur le MESSAGE : `world.game_over` n'est pose qu'apres.
    return bool(getattr(message, 'players_won', False))


def _rats_engages(player: 'Player') -> int:
    return len([f for f in player.engaged_minions.GetAll() if f.HasTrait('RAT')])


def _allies_predateurs(effect: 'Effect', player: 'Player') -> int:
    n = 0
    for card in effect.world.object_manager.card_dict.values():
        face = card.face
        if face is None or not Ally.IsType(face) or not face.HasTrait('PREDATOR'):
            continue
        if face.GetOwner() is player:
            n += 1
    return n


def _queue_mise_de_cote(effect: 'Effect') -> bool:
    aside = list(Worlds.AsideDeck(effect).Get(True))
    return any(f.paper.card_id == 'hs036' for f in aside)


def _blessures_jameson(effect: 'Effect') -> int:
    jj = Worlds.FindCardsOnField(effect, name='J. Jonah Jameson')
    return min((f.GetCounters('wound') for f in jj), default=0)


def _reptiles_sur_le_lizard(effect: 'Effect') -> int:
    from cards.pack.hunting_season.the_lizard import NombreReptiles
    return NombreReptiles(effect)


def _menace_principale(effect: 'Effect') -> int:
    return sum(s.threat for s in Worlds.GetAllMainSchemes(effect.world))


def GainsDExperience(level: int, effect: 'Effect', gagnee: bool) -> Dict['Player', int]:
    """Le livret, puce par puce (reference : campaign_rules.experience_awards)."""
    joueurs = Worlds.GetPlayers(effect)
    n = len(joueurs)
    if level == 5:
        return {p: 0 for p in joueurs}
    commun = 3 if gagnee else 2
    if ModeHunter(effect) and gagnee:
        commun += 1
    if level == 1:
        if gagnee and ActiveMainSchemeStartswith(effect, 'hs004'):
            commun += 1
        return {p: commun + int(_rats_engages(p) == 0) for p in joueurs}
    if level == 2:
        if gagnee and _blessures_jameson(effect) <= 1:
            commun += 1
        if _queue_mise_de_cote(effect):
            commun += 1
    if level == 3:
        if ActiveMainSchemeStartswith(effect, 'hs057') or ActiveMainSchemeStartswith(effect, 'hs058'):
            commun += 1
        if _reptiles_sur_le_lizard(effect) < n:
            commun += 1
    if level == 4:
        if _menace_principale(effect) < 7 * n:
            commun += 1
        gains = {}
        for p in joueurs:
            identite = p.GetIdentity()
            moitie = identite is not None and 2 * identite.health >= identite.max_health
            gains[p] = commun + int(moitie)
        return gains
    return {p: commun for p in joueurs}


def ProprietaireDeLaRecompense(level: int, effect: 'Effect') -> 'Player|None':
    """Scenarios 2 a 4 : le joueur qui POSSEDE le moins d'allies PREDATOR ; le
    Master Hunter tranche les egalites (et choisit seul au scenario 1). Le moteur
    propose ; le panneau de fin de partie laisse corriger."""
    joueurs = Worlds.GetPlayers(effect)
    if not joueurs:
        return None
    if level == 1:
        eligibles = list(joueurs)
    else:
        bas = min(_allies_predateurs(effect, p) for p in joueurs)
        eligibles = [p for p in joueurs if _allies_predateurs(effect, p) == bas]
    maitre = MaitreChasseur(effect) - 1
    for p in eligibles:
        if p.player_id == maitre:
            return p
    return eligibles[0]


def CollectHS(level: int, effect: 'Effect', message: 'Message.WhenGameOver') -> dict:
    updates: Dict[str, Any] = {}
    gagnee = _gagnee(message)
    gains = GainsDExperience(level, effect, gagnee)
    for player, gain in gains.items():
        updates[CleJoueur(player, CLE_XP)] = str(Experience(effect, player) + gain)

    if level < 5 and gagnee:
        proprietaire = ProprietaireDeLaRecompense(level, effect)
        if proprietaire is not None:
            updates[CleJoueur(proprietaire, CLE_AJOUTS)] = SEP.join(Ajouts(effect, proprietaire) + [REWARDS[level]])

    if level in (2, 3) and not gagnee:
        for player in Worlds.GetPlayers(effect):
            cle = CleJoueur(player, CLE_A_RETIRER)
            updates[cle] = str(_entier(effect, cle) + 1)

    for player in Worlds.GetPlayers(effect):
        identite = player.GetIdentity()
        if identite is not None:
            base = identite.printed_health if identite.printed_health > 0 else identite.max_health
            updates[CleJoueur(player, CLE_PV)] = str(max(0, min(identite.health, base)))

    if level == 1 and not gagnee:
        updates['Vermin escaped'] = '1'
    if level == 2 and gagnee:
        updates['Scorpion joined you'] = '1'
    if level == 3 and not gagnee:
        updates['Lizard escaped'] = '1'
    if level == 4 and gagnee:
        updates['Vulture joined you'] = '1'
        updates['Gibbon unlocked'] = '1'
    for player in Worlds.GetPlayers(effect):
        # Cle de travail de `CarteDeDepartEnPlus` : elle ne sort pas au carnet.
        updates[f'_hs_main_en_plus_{player.player_id}'] = None
    return updates


def CampaignSetup(level: int) -> List['Ability']:
    """A poser sur la face 1A du complot principal du scenario `level`."""
    abilities: List['Ability'] = [CartesAjoutees(), CartesSpecifiquesRetirees()]
    if level == 5:
        abilities.append(ChangementsDeKraven())
    if level >= 2:
        abilities.extend(CarteDeDepartEnPlus())
        abilities.append(PointsDeVieExperts())
    abilities.append(EnvironnementHunter(level))
    abilities.append(WriteCampaignLogAtGameOver(lambda effect, message: CollectHS(level, effect, message),
                                                scenario_id=SCENARIOS[level - 1]))
    return abilities
