from cards.pack import *

class Buff_50168a(Buff):

    def __init__(self) -> None:
        super().__init__()
        self.means = ""
        self.motive = ""
        self.opportunity = ""
        self.accused: 'CardFace'

def RemoveSecretCountersFromAmongBoardMemberEnvironments(size: int|Literal["1*"], by_effect: 'Effect'):
    player = Worlds.GetFirstPlayer(by_effect)

    faces = Worlds.FindCardsOnField(by_effect, has_counter='secret', card_type=CanPlaceCounter)
    faces = [x for face in faces for x in [face] * face.GetCounters('secret')]

    size = Worlds.ConvertPerPlayerIconToInt(size, by_effect)

    player.ChooseAbilities(
        by_effect,
        AbilityFactory.ForChoiceAbility(
            "",
            lambda targets:
                Faces.RemoveCountersOn(targets, 1, 'secret', by_effect)
        ).SetTarget(faces, range=(0, size))
    )

def PlaceSecretCounterOnEachBoardMemberCard(size: int, by_effect: 'Effect'):
    faces = Worlds.FindCardsOnField(by_effect, trait="BOARD MEMBER")
    Faces.PlaceCountersOn(faces, size, 'secret', by_effect)

def PlaceSecretCounterOnBoardMemberCard(card_type: Type[Environment|CardFace], size: int, by_effect: 'Effect', with_fewest_secret: bool=False):
    faces = Worlds.FindCardsOnField(by_effect, trait="BOARD MEMBER", card_type=card_type)

    if with_fewest_secret:
        fewest_counter = 'secret'
    else:
        fewest_counter = False

    face = Filter.One(faces, by_effect, fewest_counter=fewest_counter)

    if face:
        Faces.PlaceCountersOn([face], size, 'secret', by_effect)


def BaronZemoA(health: int):

    def baron_zemo(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(EncounterVillain)
        Unused(this)

        message.SetBeInstead(effect)

        this.ResetHealth(effect, health)
        RemoveSecretCountersFromAmongBoardMemberEnvironments(3, effect)


    return AbilityFactory.WhenUnitWouldBeDefeated(
        AbilityType.ForcedInterrupt,
        "This",
        baron_zemo
    )

def BaronZemoB(secret: int):
    
    def baron_zemo(effect: 'Effect', message: 'Message.WhenEnemyActivateAgainstYou') -> None:
        this = effect.this.CastTo(EncounterVillain)
        Unused(this)

        player = message.GetToPlayer()

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                f"Place {secret} secret counter on a [[Board Member]] card",
                lambda targets:
                    Faces.PlaceCountersOn(targets, secret, 'secret', effect)
            ).SetTarget(trait="BOARD MEMBER"),
            AbilityFactory.ForChoiceAbility(
                "Give Baron Zemo an additional boost card for this activation",
                lambda targets:
                    message.GiveAdditionalBoostCardForThisActivation(1, effect)
            ),
        )


    return AbilityFactory.WhenEnemyActivateAgainstYou(
        AbilityType.ForcedInterrupt,
        "This",
        baron_zemo
    )

# LES DEUX ENVELOPPES NE SONT JAMAIS DES PAQUETS DE CARTES, campagne ou pas.
#
# Le pack d'origine les montait en piles avec `SetAsideDeck`. Or `SetAsideDeck.Create`
# inscrit la pile dans `world.additional_decks`, et `to_descriptor` rend toutes ces
# piles au navigateur avec le `card_id` reel de chaque carte, face cachee ou non.
# Mesure faite hors campagne : les neuf preuves arrivaient au client, identifiants en
# clair, TRIEES PAR ENVELOPPE. Or le secret n'est pas l'existence des neuf preuves —
# elle est imprimee dans le livret — c'est leur REPARTITION : savoir lesquelles trois
# dorment dans l'enveloppe A.I.M., c'est connaitre la taupe sans jouer.
#
# La campagne fermait deja la fuite en ne fabriquant aucune carte avant que le joueur
# n'ait le droit de la voir (voir `cards/pack/aos/campaign.py`). Hors campagne, la
# meme approche s'applique depuis le 12/8/2026 : les neuf preuves quittent le jeu
# TOUTES ENSEMBLE — une seule zone, donc aucune information — et la combinaison de la
# taupe vit dans le store, sous une cle que `WriteCampaignLogAtGameOver` filtre
# (`CLES_SECRETES`). Les lecteurs ci-dessous n'ont donc plus qu'un seul chemin.

def ShieldEnvelopeHasCards(by_effect: 'Effect'):
    from cards.pack.aos.campaign import EnveloppeShield
    return EnveloppeShield(by_effect) != []

def GainCardsFromShieldEnvelope(size: int, by_effect: 'Effect'):
    from cards.pack.aos.campaign import EnveloppeShield, NoterPreuveGagnee, PreuveEnJeu
    restantes = EnveloppeShield(by_effect)
    for _ in range(min(size, len(restantes))):
        card_id = str(Rand.RandomChoice(restantes, by_effect))
        restantes.remove(card_id)
        # Notee AVANT d'entrer en jeu : c'est l'inscription qui vide l'enveloppe,
        # donc qui empeche la meme preuve de ressortir dans la meme partie.
        NoterPreuveGagnee(by_effect, card_id)
        PreuveEnJeu(by_effect, card_id)

"""
PREPARING THE EVIDENCE
To determine the mole at the start of the campaign, follow these steps:
1. Separate the nine evidence cards ( 185–193) by their card backs into three sets of three cards.
2. Shuffle each set of three cards separately and put one card from each set into the A.I.M. envelope without looking at them.
    » Insert the cards facedown with the side of the envelope with the “A.I.M.” logo faceup so that you can later remove the cards from the envelope without seeing their faces.
3. Shuffle the six remaining evidence cards together and put them in the S.H.I.E.L.D. envelope without looking at them.
    » Insert the cards facedown with the side of the envelope with the “S.H.I.E.L.D.” logo faceup so that you can later remove the cards from the envelope without seeing their faces.
"""
def PreparingTheEvidence(effect: 'Effect'):
    """Prepare les preuves SANS trier les cartes, pour ne rien livrer au client.

    Le livret fait separer les neuf preuves par dos, en tirer une de chaque serie
    dans l'enveloppe A.I.M. et ranger les six autres dans l'enveloppe S.H.I.E.L.D.
    Monter ces deux piles dans le monde publiait la reponse : `additional_decks` part
    au navigateur avec les `card_id`, donc avec la repartition.

    On fait donc exactement ce que fait la campagne : les neuf preuves quittent le
    jeu TOUTES ENSEMBLE — une seule zone, aucune information a en tirer — et la
    combinaison de la taupe est ecrite dans le store sous `CLE_ENVELOPPE_AIM`, que
    `WriteCampaignLogAtGameOver` filtre. Une preuve n'est fabriquee qu'au moment ou
    le joueur a le droit de la voir (`PreuveEnJeu`).
    """
    from cards.pack.aos.campaign import CLE_ENVELOPPE_AIM, PREUVES, SEPARATEUR

    faces = Worlds.GetEncounterDeckCards(effect) + Worlds.GetEncounterDiscardPileCards(effect)
    evidences = Filter.ByType(faces, Evidence)

    # Une preuve par SERIE, tiree au hasard. Les series sont les trois dos du
    # livret ; le moteur les porte en `subtype` (Means, Motive, Opportunity), et
    # l'ordre des identifiants les groupe aussi par trois.
    par_serie: 'Dict[str, List[str]]' = {}
    for face in evidences:
        par_serie.setdefault(str(face.subtype), []).append(face.paper.card_id)
    if not par_serie:
        # Aucune preuve dans ce deck : rien a preparer, et surtout rien a inventer.
        return

    combinaison: 'List[str]' = []
    for serie in sorted(par_serie):
        choix = sorted(par_serie[serie])
        combinaison.append(str(Rand.RandomChoice(choix, effect)))

    CampaignLog.SetStr(CLE_ENVELOPPE_AIM, SEPARATEUR.join(combinaison), effect.world)

    # Les neuf partent ensemble. `RemoveAllFromGame` les met dans `area_removed`,
    # que le descripteur rend — mais toutes au meme endroit, donc sans dire laquelle
    # est ou. C'est la repartition qui etait le secret, pas la liste : les neuf
    # identifiants sont imprimes dans le livret.
    Faces.RemoveAllFromGame(evidences, effect)
    Unused(PREUVES)

def CartesDeLEnveloppeAim(by_effect: 'Effect') -> 'List[str]':
    """Les trois identifiants de l'enveloppe A.I.M.

    Un seul chemin, campagne ou pas : le store. En campagne le serveur les y injecte
    avant `NewGame` (et ne les rend jamais au navigateur) ; hors campagne
    `PreparingTheEvidence` les y tire au debut de la partie.
    """
    from cards.pack.aos.campaign import EnveloppeAim
    return EnveloppeAim(by_effect)


def MembreDeLaCombinaison(card_ids: 'Sequence[str]', by_effect: 'Effect') -> 'CardFace':
    """Le membre du Conseil que designe une combinaison, d'apres le carnet.

    La table est celle du carnet imprime : neuf combinaisons par membre,
    vingt-sept en tout. Elle sert deux fois — pour la taupe (les trois preuves
    de l'enveloppe A.I.M.) et pour l'accuse (les trois hypotheses des joueurs),
    puisque le livret p.19 dit que l'accuse DECOULE de la combinaison choisie :
    « Each combination is listed underneath a board member. This board member
    is the accused. »

    Le membre est rendu quelle que soit sa face : en campagne il peut deja
    avoir bascule cote attachement, et il le reste jusqu'a la fin.
    """
    ORANGE1 = "50185"
    BLUE1   = "50186"
    RED1    = "50187"
    GREEN2  = "50188"
    BLACK2  = "50189"
    YELLOW2 = "50190"
    PURPLE3 = "50191"
    RED3    = "50192"
    BLUE3   = "50193"

    ChiefMedicalOfficer = [
        [ORANGE1,   GREEN2,     PURPLE3],
        [ORANGE1,   GREEN2,     RED3],
        [ORANGE1,   BLACK2,     PURPLE3],
        [ORANGE1,   BLACK2,     BLUE3],
        [ORANGE1,   YELLOW2,    RED3],
        [BLUE1,     GREEN2,     PURPLE3],
        [BLUE1,     GREEN2,     RED3],
        [BLUE1,     BLACK2,     PURPLE3],
        [RED1,      GREEN2,     PURPLE3],
    ]

    ChiefSurveillanceOfficer = [
        [ORANGE1,   BLACK2,     RED3],
        [BLUE1,     GREEN2,     BLUE3],
        [BLUE1,     BLACK2,     RED3],
        [BLUE1,     BLACK2,     BLUE3],
        [BLUE1,     YELLOW2,    PURPLE3],
        [BLUE1,     YELLOW2,    RED3],
        [RED1,      BLACK2,     RED3],
        [RED1,      BLACK2,     BLUE3],
        [RED1,      YELLOW2,    RED3],
    ]

    ChiefTacticalOfficer = [
        [ORANGE1,   GREEN2,     BLUE3],
        [ORANGE1,   YELLOW2,    PURPLE3],
        [ORANGE1,   YELLOW2,    BLUE3],
        [BLUE1,     YELLOW2,    BLUE3],
        [RED1,      GREEN2,     RED3],
        [RED1,      GREEN2,     BLUE3],
        [RED1,      BLACK2,     PURPLE3],
        [RED1,      YELLOW2,    PURPLE3],
        [RED1,      YELLOW2,    BLUE3],
    ]

    card_ids = sorted(card_ids)

    if card_ids in ChiefMedicalOfficer:
        face = Worlds.FindCardOnField(by_effect, name="Chief Medical Officer")
        if face:
            return face
        face = Worlds.FindCardOnField(by_effect, name="Medical Officer's Aid")
        assert face
        return face

    if card_ids in ChiefSurveillanceOfficer:
        face = Worlds.FindCardOnField(by_effect, name="Chief Surveillance Officer")
        if face:
            return face
        face = Worlds.FindCardOnField(by_effect, name="Surveillance Officer's Aid")
        assert face
        return face

    if card_ids in ChiefTacticalOfficer:
        face = Worlds.FindCardOnField(by_effect, name="Chief Tactical Officer")
        if face:
            return face
        face = Worlds.FindCardOnField(by_effect, name="Tactical Officer's Aid")
        assert face
        return face

    assert False


def CalcMole(by_effect: 'Effect') -> 'CardFace':
    """La taupe : le membre que designent les trois preuves de l'enveloppe."""
    return MembreDeLaCombinaison(CartesDeLEnveloppeAim(by_effect), by_effect)

