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
# Les sbires THUNDERBOLT qui peuvent survivre au scenario 4, avec le set
# modulaire qui les apporte. Le nom est la cle : c'est lui que `CollectAOS`
# releve au carnet (`paper.name`, sans etoile — mesure faite).
#
# Jolt n'a PAS de set : elle appartient au set du scenario 4 lui-meme
# (`data/scenarios/thunderbolts.json`, cle `encounters`), et aucun fichier de
# `data/encounter_sets/` ne la contient. C'est exactement ce que dit le livret
# p.19 par « except for Jolt's » — il n'y a rien a rapporter avec elle, on ne
# remet que la carte.
THUNDERBOLTS = {
    'Jolt':            ('50133', None),
    'Moonstone':       ('50139', 'gravitational_pull'),
    'Songbird':        ('50143', 'hard_sound'),
    'Black Widow':     ('50148', 'pale_little_spider'),
    'Radioactive Man': ('50152', 'power_of_the_atom'),
    'MACH-IV':         ('50156', 'supersonic'),
    'Batroc':          ('50161', 'the_leaper'),
}
CLE_THUNDERBOLTS = 'Surviving Thunderbolts'
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
CLE_SCENARIOS_VIDES = 'Scenarios With A Cleared Board Member'


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


def ConseilEntierementRetourne() -> 'Ability':
    """Trois attachements [[Board Member]] en jeu : la partie est perdue.

    Le texte est sur les trois cartes attachement (50181b, 50182b, 50183b) :
    « If there are 3 [[Board Member]] attachments in play, the players lose the
    game. » Le livret p.18 le redit pour Zemo : « If all of the board members
    join Baron Zemo, the players lose the scenario. »

    Le pack le cable en REPONSE A UN RETOURNEMENT
    (`IfThereAre3BoardMemberAttachmentsInPlayPlayersLoseTheGame`, sur
    `AfterFlipToThisFace`). Cela suffit tant que le troisieme bascule EN COURS
    DE PARTIE. En campagne, non : les secrets se reportent, un membre a quatre
    secrets arrive DEJA retourne, et `Card.Flip` n'envoie `AfterCardFlip` que
    si `world.is_game_started` — ce qui est faux pendant la mise en place.

    Mesure avant correction, scenario 5 expert avec les trois membres a trois
    secrets : les trois basculent au setup, `game_over` reste faux, et comme
    plus AUCUN retournement ne peut survenir ensuite, la condition ne se
    declenche jamais. Les joueurs jouaient une partie qu'ils avaient perdue,
    avec les trois attachements sur le dos.

    La condition est un etat, pas un evenement : on la relit donc une fois la
    mise en place de campagne faite. Elle vaut a TOUS les scenarios — les trois
    cartes portent le texte, et un Conseil peut basculer avant le dernier.
    """
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        attachements = Worlds.FindCardsOnField(effect, trait='BOARD MEMBER',
                                               card_type=Attachment)
        if len(attachements) >= 3:
            Worlds.SetGameOver(False, effect)
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


def _thunderbolts_survivants(effect: 'Effect') -> 'List[Tuple[str, str|None]]':
    """Ce que le carnet a retenu du scenario 4, traduit en cartes et en sets."""
    survivants = []
    for nom in _liste(CampaignLog.GetStrInternal(CLE_THUNDERBOLTS, effect)):
        entree = THUNDERBOLTS.get(nom)
        if entree:
            survivants.append(entree)
    return survivants


def SetsDesThunderboltsSurvivants() -> 'Ability':
    """Scenario 5 : les sets des Thunderbolts encore debout reviennent.

    Livret p.19 : « If you recorded any "Surviving Thunderbolts" in the
    campaign log, shuffle those minions AND THEIR ENCOUNTER SETS, except for
    Jolt's, into the encounter deck. »

    Le set porte le sbire : l'ajouter au deck de rencontre ramene donc les deux
    d'un coup, et c'est le moteur qui melange. On passe par
    `encounter_set_names` a la creation du deck plutot que par la mise en place
    de campagne, pour la meme raison que `EcarterLesPreuvesDuScenario` : c'est
    la seule etape ou le contenu du deck se decide encore.

    Jusqu'ici la cle `Surviving Thunderbolts` etait ECRITE au scenario 4 et
    RELUE nulle part : rien ne revenait.
    """
    def action(effect: 'Effect', message: 'Message.WhenGameBeginSetup'):
        for _, set_name in _thunderbolts_survivants(effect):
            if set_name and set_name not in message.encounter_set_names:
                message.encounter_set_names = message.encounter_set_names + [set_name]
    return AbilityFactory.WhenGameBeginSetup(
        action,
        conditions=[lambda effect, message: Worlds.IsCampaign(effect)],
    )


def RetourDeJolt() -> 'Ability':
    """Jolt seule, sans set, si elle a survecu au scenario 4.

    Elle est le « except for Jolt's » du livret : son set est celui du scenario
    4, qu'on ne rapporte pas. Elle passe donc par la mise en place de campagne,
    carte par carte, comme les Adaptoides.
    """
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for card_id, set_name in _thunderbolts_survivants(effect):
            if set_name is None:
                card = CardFactory.GenerateCard(card_id, None, effect.world)
                Faces.ShuffleAllTo([card.face], 'EncounterDeck', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


SET_DES_PREUVES = 'executive_board_evidence'


def EcarterLesPreuvesDuScenario() -> 'Ability':
    """Le scenario 5 apporte les NEUF preuves : en campagne, c'est de trop.

    `baron_zemo.json` charge le set `executive_board_evidence` complet. Le
    moteur resout la capacite « Setup » de toute carte Evidence qu'il trouve
    dans un deck (voir l'etape 12 de `world.GameSetup`), si bien qu'en mode
    campagne les neuf preuves entraient en jeu face visible — dont les TROIS
    de l'enveloppe A.I.M., ce qui donnait la taupe au joueur sans qu'il ait a
    enqueter. Mesure faite a la sonde avant correction : `area_evidence`
    contenait 50185 a 50193.

    On retire donc le set a la creation du deck de rencontre, et les preuves
    gagnees sont posees plus tard, une par une, par `PoserLesPreuves`. Hors
    campagne on ne touche a rien : le set garde son role de module.
    """
    def action(effect: 'Effect', message: 'Message.WhenGameBeginSetup'):
        message.encounter_set_names = [x for x in message.encounter_set_names
                                       if x != SET_DES_PREUVES]
    return AbilityFactory.WhenGameBeginSetup(
        action,
        conditions=[lambda effect, message: Worlds.IsCampaign(effect)],
    )


def PoserLesPreuves() -> 'Ability':
    """Les preuves gagnees entrent en jeu et resolvent leur « Setup ».

    Livret, encarts SETUP des scenarios 2 a 5 : « After resolving mulligans,
    resolve the "Setup" ability of each evidence card the players have
    earned. » D'ou l'accroche `WhenCampaignSetupAfterMulligans` plutot que
    `WhenCampaignSetup` : ces capacites cherchent une carte dans le deck et
    l'ajoutent A LA MAIN, ce qui n'a de sens qu'une fois la main piochee et
    mulliganee. Elles posent aussi un compteur secret sur un membre du
    Conseil, qui doit donc deja porter le compte reporte du scenario
    precedent — `PoserLeConseil` s'en charge a l'etape 13, avant.

    On pose la carte NOUS-MEMES avant de resoudre sa mise en place.
    `Evidence.OnWhenCardSetup` sait entrer en jeu tout seul, mais seulement
    depuis un vrai deck (`IsInDeck`), et la reserve n'en est pas un
    (`DeckTypeFlags.AsideDeck.is_deck` est faux) : la generer la donnait une
    aire des preuves vide, capacite jamais partie. `PutIntoPlay` la range dans
    `area_evidence`, puis `Setup` fait partir la capacite.
    """
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetupAfterMulligans'):
        for card_id in _liste(CampaignLog.GetStrInternal(CLE_PREUVES, effect)):
            if card_id not in PREUVES:
                continue
            card = CardFactory.GenerateCard(card_id, None, effect.world)
            card.face.PutIntoPlay('FirstPlayer', effect)
            card.face.Setup(False)
    return AbilityFactoryCampaign.WhenCampaignSetupAfterMulligans(action)


def SoinExpertDuConseil() -> 'Ability':
    """Le prix du soin, en campagne experte : un secret de plus sur le Conseil.

    Encarts SETUP des scenarios 2 a 5, sous « Expert Campaign Only » : « Each
    player may place one secret counter on a Board Member environment to heal
    damage from their identity equal to their REC. »

    Les huit boites-campagnes font toutes payer le retour a la sante, et
    jamais deux fois de la meme facon : une carte rencontre face cachee pour
    sm et next_evol, une obligation ajoutee au deck pour trors. Ici c'est un
    secret de plus sur le Conseil, ce qui rapproche un membre du basculement —
    donc de Zemo. Le soin se paie en terrain perdu sur le fil de la campagne,
    pas en cartes.

    Deux ecarts avec les sept autres, tous deux voulus par le livret :

    * on soigne de sa REC, pas jusqu'aux PV imprimes. Une identite tres
      abimee ne revient donc pas a neuf.
    * le cout se pose sur une carte du DECOR, choisie par le joueur, et pas
      dans son propre deck.

    L'ordre compte : cette capacite doit passer APRES
    `ExpertCampaignSetPlayersHPToTheirRemainingHP`, qui vient de ramener les
    PV a leur valeur reportee, et APRES `PoserLeConseil`, sans quoi il n'y
    aurait aucun environnement a viser.
    """
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        this = effect.this

        def pour_ce_joueur(player: 'Player'):
            identite = player.GetIdentity()
            if identite is None:
                return

            def soigner(targets: 'Sequence[CardFace]'):
                Faces.PlaceCountersOn(targets, 1, 'secret', effect)
                # `recover` est la REC courante, buffs compris. Elle vit sur la
                # face alter-ego, celle qui est active en debut de partie.
                this.HealthUnits([identite], getattr(identite, 'recover', 0), effect)

            player.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Place 1 secret counter on a [[Board Member]] environment to heal damage from your identity equal to your REC",
                    soigner,
                ).SetTarget(Environment, trait="BOARD MEMBER")
            )

        Players.ForEachPlayer(effect, pour_ce_joueur)

    return AbilityFactoryCampaign.WhenCampaignSetupExpertOnly(action)


def CampaignSetup(level: int) -> 'List[Ability]':
    # L'ordre compte : le Conseil est pose et rechargé de ses secrets AVANT
    # qu'on regarde s'il a entierement bascule.
    abilities: List['Ability'] = [PoserLeConseil(level), ConseilEntierementRetourne()]
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
        abilities.append(SetsDesThunderboltsSurvivants())
        abilities.append(RetourDeJolt())
        # Seul le scenario 5 charge le set complet des preuves.
        abilities.append(EcarterLesPreuvesDuScenario())
    if level >= 2:
        # Le scenario 1 ne peut avoir aucune preuve : le livret ne cite cette
        # instruction que dans les encarts des scenarios 2 a 5.
        abilities.append(PoserLesPreuves())
        abilities.append(AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP())
        # Apres la remise des PV, jamais avant : le livret pose les deux
        # instructions dans cet ordre, et l'inverse soignerait une identite dont
        # les PV seraient ecrases juste apres.
        abilities.append(SoinExpertDuConseil())
    abilities.append(WriteCampaignLogAtGameOver(lambda effect: CollectAOS(level, effect)))
    return abilities


# ------------------------------------------------------- les deux enveloppes --
# En campagne, les enveloppes ne sont PAS des paquets de cartes.
#
# Le pack d'origine les monte en vraies piles (`PreparingTheEvidence`, puis
# `Worlds.ScenarioDeck`), ce qui convient hors campagne : le secret n'y vit
# qu'une partie. Mais `SetAsideDeck.Create` inscrit la pile dans
# `world.additional_decks`, et `to_descriptor` rend TOUTES ces piles avec le
# `card_id` reel de chaque carte, face cachee ou non. Mesure faite hors
# campagne : les neuf preuves arrivent au navigateur, identifiants en clair.
#
# En campagne, ce serait rendre la taupe lisible depuis la console du
# navigateur, apres deux fuites deja fermees pour la meme raison. On garde donc
# les enveloppes ou le secret vit deja — le carnet — et on ne fabrique une
# carte qu'au moment ou le joueur a le droit de la voir.


def EnveloppeAim(effect: 'Effect') -> 'List[str]':
    """Les trois preuves de la taupe. Vide si le carnet ne les porte pas."""
    aim = _liste(CampaignLog.GetStrInternal(CLE_ENVELOPPE_AIM, effect))
    return aim if len(aim) == 3 else []


def EnveloppeShield(effect: 'Effect') -> 'List[str]':
    """Ce qu'il reste a puiser : les neuf, moins la taupe, moins le deja gagne."""
    aim = EnveloppeAim(effect)
    if not aim:
        return []
    deja = _liste(CampaignLog.GetStrInternal(CLE_PREUVES, effect))
    return [p for p in PREUVES if p not in aim and p not in deja]


def NoterPreuveGagnee(effect: 'Effect', card_id: str) -> None:
    """Inscrit une preuve au carnet EN COURS DE PARTIE.

    Le scenario 5 est le seul ou des preuves se gagnent en jouant (Reponse de
    l'etape 1B). Sans cette ecriture, l'enveloppe S.H.I.E.L.D. ne se viderait
    pas et la meme preuve pourrait sortir deux fois dans la meme partie.
    """
    deja = _liste(CampaignLog.GetStrInternal(CLE_PREUVES, effect))
    if card_id in deja:
        return
    CampaignLog.SetStr(CLE_PREUVES, SEPARATEUR.join(deja + [card_id]), effect.world)


def PreuveEnJeu(effect: 'Effect', card_id: str) -> 'CardFace':
    """Fabrique une preuve et la pose face visible dans l'aire des preuves."""
    card = CardFactory.GenerateCard(card_id, None, effect.world)
    card.face.PutIntoPlay('FirstPlayer', effect)
    return card.face


# ------------------------------------------------------------------ releve --
def _un_membre_sans_secret(effect: 'Effect') -> bool:
    """« At least one Board Member environment in play has no secret counters ».

    C'est la condition qui rapporte une preuve aux scenarios 1 a 4 — mais pas
    seulement. Le livret la reutilise mot pour mot dans l'encart DEFEAT du
    scenario 5, pour compter combien de preuves rendre a l'equipe qui rejoue.
    Elle est donc mesuree A PART de la recompense : l'enveloppe S.H.I.E.L.D.
    peut etre vide alors que la condition tient, et le compte ne doit pas s'en
    trouver fausse.

    « environment » : un membre passe face attachement n'en est plus un, et de
    toute facon il porte au moins quatre secrets.
    """
    bases = [card_id.split(',')[0][:-1] for _, card_id in CONSEIL]
    membres = _sur_le_terrain(effect, bases, card_type=Environment)
    return any(f.GetCounters('secret') == 0 for f in membres)


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
    if not _un_membre_sans_secret(effect):
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
            updates[CLE_THUNDERBOLTS] = SEPARATEUR.join(noms)

    # Scenarios 1 a 4 seulement. Leurs encarts VICTORY portent tous la clause
    # « If at least one Board Member environment in play has no secret
    # counters on it, gain one evidence card » ; celui du scenario 5 (p.19) ne
    # l'a pas, il n'a plus qu'une ligne : « Zemo is defeated, the mole is
    # exposed, the heroes are exonerated ». Au 5, les preuves se gagnent EN
    # PARTIE, par la Reponse de l'etape 1B.
    if level <= 4:
        preuves = _preuve_gagnee(effect)
        if preuves is not None:
            updates[CLE_PREUVES] = SEPARATEUR.join(preuves)
        # Le compte des scenarios ou le Conseil a ete vide, cumulatif. Le
        # carnet imprime le garde autrement : une colonne de compteurs secrets
        # par scenario (#1 a #4), qu'on relit a la fin pour compter. Le moteur,
        # lui, n'ecrase qu'une valeur par membre — d'ou ce compte tenu au fil
        # de l'eau. Il ne sert qu'a l'encart DEFEAT du scenario 5 (p.19), qui
        # rend une preuve par scenario ainsi compte quand on rejoue.
        if _un_membre_sans_secret(effect):
            updates[CLE_SCENARIOS_VIDES] = str(_entier(effect, CLE_SCENARIOS_VIDES) + 1)

    return updates
