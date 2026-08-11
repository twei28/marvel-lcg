"""Campagne « Agents of S.H.I.E.L.D. » : mise en place et releve du carnet.

Regles du livret officiel mc50 : page 4 pour le mode campagne, 5 et 6 pour le
Conseil executif et les preuves, puis les encarts CAMPAIGN INSTRUCTIONS des
pages 9, 11, 13, 15 et 19.

Le fil de la campagne est le CONSEIL EXECUTIF. Ses trois membres entrent en jeu
a chaque scenario avec les compteurs secrets qu'ils avaient a la fin du
precedent : c'est la seule campagne du jeu ou l'etat d'une carte se reporte
tel quel, chiffre par chiffre, d'une partie a l'autre. Vider un membre de ses
secrets rapporte une preuve, et les preuves demasquent la taupe.

LES PREUVES : gagner une preuve a la fin d'un scenario est ici (voir
`_preuve_gagnee`). La combinaison de la taupe n'est jamais dans le carnet que
le joueur lit : le serveur la tire, la retire de tout ce qui part vers le
navigateur et la reinjecte dans le carnet du moteur juste avant `NewGame`.
C'est cette fonction qui la lit, et la seule.

CE QUI N'EST PAS ENCORE ICI : la grille de deduction du carnet (rayer les
combinaisons au fur et a mesure, cote ecran), la capacite « Setup » des
preuves gagnees a poser au scenario suivant, et l'accusation du scenario 5.
Voir docs/CAMPAGNES.md.
"""
from . import *
from cards.pack.mts.campaign import WriteCampaignLogAtGameOver

# Les trois membres du Conseil. La face B est leur attachement : le moteur
# retourne la carte tout seul quand les secrets s'accumulent.
CONSEIL = [
    ('Chief Medical Officer', '50181a,50181b'),
    ('Chief Surveillance Officer', '50182a,50182b'),
    ('Chief Tactical Officer', '50183a,50183b'),
]
INTERFERENCES = ('50184a', '50184b', '50184c')
ADAPTOIDS = ('50109', '50110', '50111', '50112')
ADAPTOID_MINION = '50113'
ALERTE = '50090'
CAPTIF_LIBERE = '50091'

SECRETS_AU_DEPART = 2
SEPARATEUR = ';'

# Les neuf preuves, dans l'ordre des trois series du livret p.5 : le moyen, le
# mobile, l'occasion. Trois d'entre elles (une par serie) dorment dans
# l'enveloppe A.I.M. et designent la taupe ; les six autres sont l'enveloppe
# S.H.I.E.L.D., ou les joueurs puisent.
PREUVES = ('50185', '50186', '50187',   # moyen    : dossiers, ecoute, scanner
           '50188', '50189', '50190',   # mobile   : argent, chantage, ideologie
           '50191', '50192', '50193')   # occasion : habilitation, voyages, autorite
# Le secret n'est PAS dans le carnet que le joueur voit : le serveur le tire,
# le retire de tout ce qui sort vers le navigateur (`_sans_secret`) et le
# reinjecte dans le carnet du moteur juste avant `NewGame`. Voir
# `server_campagne.py` et `server_new_game.py`.
CLE_ENVELOPPE_AIM = 'A.I.M. Envelope'
CLE_PREUVES = 'Evidence Gained'


def _liste(valeur: str) -> 'List[str]':
    return [x for x in (valeur or '').split(SEPARATEUR) if x]


def _entier(effect: 'Effect', cle: str) -> int:
    try:
        return int(CampaignLog.GetStrInternal(cle, effect) or 0)
    except ValueError:
        return 0


def _sur_le_terrain(effect: 'Effect', prefixes: 'Sequence[str]', **kw) -> 'List[CardFace]':
    return [f for f in Worlds.FindCardsOnField(effect, **kw)
            if f.paper.card_id.startswith(tuple(prefixes))]


# ------------------------------------------------------------ mise en place --
def PoserLeConseil(level: int) -> 'Ability':
    """Les trois membres, avec les secrets herites du scenario precedent.

    Livret p.9 : deux secrets chacun au scenario 1. Ensuite (p.11, 13, 15, 19),
    « equal to the number of secret counters recorded for that environment »
    au scenario d'avant. Le livret precise que poser assez de secrets RETOURNE
    la carte sur sa face attachement : c'est le moteur qui s'en charge, on ne
    fait que poser les compteurs.
    """
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for nom, card_id in CONSEIL:
            base = card_id.split(',')[0][:-1]
            # Le scenario de Baron Zemo apporte DEJA le Conseil avec son set :
            # en poser un second exemplaire donnait six membres sur la table.
            # On ne cree la carte que si elle n'est pas la, et dans tous les
            # cas on lui rend ses compteurs.
            face = None
            for existante in Worlds.FindCardsOnField(effect):
                if existante.paper.card_id.startswith(base):
                    face = existante
                    break
            if face is None:
                card = CardFactory.GenerateCard(card_id, None, effect.world)
                face = card.face
                face.PutIntoPlay('FirstPlayer', effect)
            secrets = (SECRETS_AU_DEPART if level == 1
                       else _entier(effect, f'Secret Counters: {nom}'))
            # Apres l'entree en jeu : elle remet les compteurs a zero.
            deja = face.GetCounters('secret')
            if secrets > deja:
                face.PlaceCountersInternal(secrets - deja, 'secret', effect)
            elif secrets < deja:
                face.RemoveCountersInternal(deja - secrets, 'secret', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


def MelangerLesInterferences() -> 'Ability':
    """Les trois A.I.M. Interference, une par type de ressource."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for card_id in INTERFERENCES:
            card = CardFactory.GenerateCard(card_id, None, effect.world)
            Faces.ShuffleAllTo([card.face], 'EncounterDeck', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


def MenaceSurLeNiveauDAlerte() -> 'Ability':
    """Scenario 2 : ce qu'on a laisse debout au scenario 1 se paie ici.

    Livret p.11 : « Place threat on the Alert Level environment equal to the
    number of minions and side schemes recorded in the campaign log for
    scenario #1. »
    """
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        valeur = _entier(effect, 'Minions and Side Schemes')
        if valeur <= 0:
            return
        for face in _sur_le_terrain(effect, [ALERTE], card_type=Environment):
            # Un environnement n'est pas une manigance : la menace s'y pose en
            # jetons, comme le fait la carte elle-meme (batroc/50090a.py).
            Faces.PlaceTokensOn([face], valeur, 'threat', effect)
            return
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


def VerrousDeLaCellule() -> 'Ability':
    """Scenario 3 : chaque captif libere au 2 ouvre une serrure ici.

    Livret p.13 : « Place 3 additional lock counters on the top card of the
    Holding Cell deck, then remove X lock counters from that card, where X is
    the number of "Rescued Captives in Play" recorded in the campaign log. »
    Le solde ne descend jamais sous zero.
    """
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        from cards.pack.aos.modok import GetHoldingCellDeck
        deck = GetHoldingCellDeck(effect)
        face = deck.GetTopCard() if deck else None
        if face is None:
            return
        solde = 3 - _entier(effect, 'Rescued Captives')
        if solde > 0:
            face.PlaceCountersInternal(solde, 'lock', effect)
        elif solde < 0:
            face.RemoveCountersInternal(min(-solde, face.GetCounters('lock')), 'lock', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


def RetourDesAdaptoids() -> 'Ability':
    """Scenario 5 : les Adaptoides laisses en jeu au 3 reviennent (p.19)."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for card_id in _liste(CampaignLog.GetStrInternal('Adaptoid Environments', effect)):
            if card_id not in ADAPTOIDS:
                continue
            card = CardFactory.GenerateCard(card_id, None, effect.world)
            card.face.PutIntoPlay('FirstPlayer', effect)
        for _ in range(3):
            card = CardFactory.GenerateCard(ADAPTOID_MINION, None, effect.world)
            Faces.ShuffleAllTo([card.face], 'EncounterDeck', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


def CampaignSetup(level: int) -> 'List[Ability]':
    abilities: List['Ability'] = [PoserLeConseil(level)]
    if level <= 4:
        # Le scenario 5 ne remelange pas les interferences : le livret ne les
        # cite plus dans son encart.
        abilities.append(MelangerLesInterferences())
    if level == 2:
        abilities.append(MenaceSurLeNiveauDAlerte())
    if level == 3:
        abilities.append(VerrousDeLaCellule())
    if level == 5:
        abilities.append(RetourDesAdaptoids())
    if level >= 2:
        abilities.append(AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP())
    abilities.append(WriteCampaignLogAtGameOver(lambda effect: CollectAOS(level, effect)))
    return abilities


# ------------------------------------------------------------------ releve --
def _preuve_gagnee(effect: 'Effect') -> 'List[str]|None':
    """Une preuve de plus, ou rien. Rend la liste COMPLETE, pas l'ajout.

    Livret p.6 et encarts VICTORY des pages 9, 11, 13 et 15, mot pour mot :
    « If at least one Board Member environment in play has no secret counters
    on it, gain one evidence card from the S.H.I.E.L.D. envelope ».

    Trois lectures a ne pas rater :

    * « environment » : un membre passe face attachement (quatre secrets, trois
      en expert) n'est plus un environnement, et de toute facon il en a. Le
      filtre `card_type=Environment` suffit donc a le mettre de cote.
    * « from the S.H.I.E.L.D. envelope » : jamais une des trois preuves de
      l'enveloppe A.I.M., et jamais deux fois la meme. Le tirage se fait donc
      dans les neuf moins la taupe moins ce qui est deja gagne.
    * la carte gagnee ne rejoint aucun deck : elle ne sert qu'a rayer des
      combinaisons du carnet, et a poser sa capacite « Setup » au scenario
      suivant.
    """
    aim = _liste(CampaignLog.GetStrInternal(CLE_ENVELOPPE_AIM, effect))
    if len(aim) != 3:
        # Sans l'enveloppe A.I.M. on ne sait pas quelles preuves sont dans
        # l'enveloppe S.H.I.E.L.D. En tirer une au hasard reviendrait a pouvoir
        # remettre au joueur une carte de la taupe, ce qui rendrait la grille
        # de deduction fausse : on prefere ne rien donner.
        return None
    deja = _liste(CampaignLog.GetStrInternal(CLE_PREUVES, effect))
    restantes = [p for p in PREUVES if p not in aim and p not in deja]
    if not restantes:
        return None
    bases = [card_id.split(',')[0][:-1] for _, card_id in CONSEIL]
    membres = _sur_le_terrain(effect, bases, card_type=Environment)
    if not any(f.GetCounters('secret') == 0 for f in membres):
        return None
    return deja + [str(Rand.RandomChoice(restantes, effect))]


def CollectAOS(level: int, effect: 'Effect') -> dict:
    updates: Dict[str, Any] = {}

    # Les secrets de chaque membre, a tous les scenarios : c'est ce qui se
    # reporte. Un membre passe face attachement garde son identifiant en 'a'.
    for nom, card_id in CONSEIL:
        base = card_id.split(',')[0][:-1]
        valeur = 0
        for face in Worlds.FindCardsOnField(effect):
            if face.paper.card_id.startswith(base):
                valeur = face.GetCounters('secret')
                break
        updates[f'Secret Counters: {nom}'] = str(valeur)

    if level == 1:
        sbires = len(Worlds.FindCardsOnField(effect, card_type=Minion))
        manigances = len(Worlds.FindCardsOnField(effect, card_type=EncounterSideScheme))
        updates['Minions and Side Schemes'] = str(sbires + manigances)
    elif level == 2:
        captifs = len(_sur_le_terrain(effect, [CAPTIF_LIBERE], card_type=Ally))
        updates['Rescued Captives'] = str(captifs)
    elif level == 3:
        en_jeu = [f.paper.card_id[:5] for f in _sur_le_terrain(effect, ADAPTOIDS, card_type=Environment)]
        if en_jeu:
            updates['Adaptoid Environments'] = SEPARATEUR.join(sorted(set(en_jeu)))
    elif level == 4:
        noms = sorted({f.paper.name for f in Worlds.FindCardsOnField(effect, card_type=Minion)
                       if 'THUNDERBOLT' in [t.upper() for t in (f.paper.traits or [])]})
        if noms:
            updates['Surviving Thunderbolts'] = SEPARATEUR.join(noms)

    preuves = _preuve_gagnee(effect)
    if preuves is not None:
        updates[CLE_PREUVES] = SEPARATEUR.join(preuves)

    return updates
