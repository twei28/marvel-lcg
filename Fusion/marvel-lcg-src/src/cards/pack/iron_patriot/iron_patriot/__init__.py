from cards.pack import *

# ===========================================================================
# LE SYSTEME REGISTERED — helpers partages du pack IRON PATRIOT
# (Neptune, set 142, prefixe `ip`).
#
# Norman Osborn joue avec un SECOND DECK de 20 sbires, le deck REGISTERED. Il
# en revele le dessus, le sbire entre en jeu ENGAGE AVEC LUI, puis on peut
# payer des ressources egales a ses ICONES DE BOOST pour en prendre le
# controle comme ALLIE REGISTERED. Sinon il reste sbire.
#
# ⚠⚠ RIEN DE TOUT CELA N'EST A INVENTER : le moteur sait deja tout faire, et
# le precedent tient en une carte, `09001b` Stephen Strange (deck d'Invocation).
#
#   besoin du pack                     | ce qui existe deja
#   -----------------------------------|-----------------------------------
#   un second deck ET sa defausse      | player.additional_deck /
#                                      | additional_discard_pile (player.py:97)
#   le remplir au montage              | AbilityFactory.BeginGameWithSetAside
#                                      | + WhenPlayerSelectHero (09001b)
#   defausse SEPAREE de la rencontre   | WhenCardWouldMoveToArea +
#                                      | message.ChangeToArea (09001b)
#   sbire -> allie, CTR = MNG imprimee | Faces.TreatAsAlly (faces.py:340), qui
#                                      | RECOPIE DEJA printed_scheme dans
#                                      | printed_thwart — c'est mot pour mot
#                                      | la regle imprimee
#   la capacite « Special »            | AbilityFactory.WhenResolveSpecialAbility
#                                      | pour la DECLARER (modele sm011),
#                                      | face.ResolveSpecialAbility pour la
#                                      | RESOUDRE (modele cameo/58031)
#
# ⚠ LE COUT EST EN ICONES DE BOOST, PAS EN COUT DE RESSOURCE. L'insert insiste :
# une carte qui reduit le COUT d'une carte ne change rien au recrutement ; une
# carte qui change le nombre d'ICONES DE BOOST, si (c'est tout le role de
# `ip008` Director of Security).
# ===========================================================================

# Le gabarit d'allie, en donnee (cards.json). `Faces.TreatAsAlly` recopie
# par-dessus le nom, l'image, l'ATQ et la MNG du sbire ; le gabarit ne fournit
# que le TYPE (Ally), le trait REGISTERED et l'unique etoile de degat
# consecutif — « They take 1 consequential damage after they attack or thwart ».
# Modele : `karma_controlled_ally` / `phoenix_controlled_ally` (pack rogue).
GABARIT_ALLIE_REGISTERED = "registered_ally"

TRAIT_REGISTERED = "REGISTERED"

# ⚠⚠ MARQUEUR POSE SUR LA CARTE, PAS SUR LA FACE. Quand un allie REGISTERED
# est vaincu, `Faces.TreatAsAlly` REMET la face de sbire (faces.py:374, son
# `AfterCardLeavePlay` Temp2) — et le trait REGISTERED disparait avec elle. La
# regle de defausse de l'insert, elle, se decide APRES : « their separation
# determined by if they gained the REGISTERED trait when they entered play ».
# Lire le trait a ce moment-la, c'est toujours lire « non », et l'allie partait
# en defausse de RENCONTRE au lieu de rentrer dans son deck. Mesure du
# 10/09/2026 (`set_aside = []`).
# Le marqueur vit sur la CARTE physique, que l'echange de face ne touche pas.
MARQUEUR_RECRUTE = "iron_patriot_recrute"
TRAIT_HAMMER = "H.A.M.M.E.R."


def DeckRegistered(player: 'Player'):
    """Le deck REGISTERED. C'est le deck ADDITIONNEL du joueur, pas un troisieme
    paquet : le moteur n'en propose qu'un, et il suffit."""
    return player.additional_deck


def DefausseRegistered(player: 'Player'):
    """La defausse du deck REGISTERED, distincte de celle du joueur ET de celle
    de rencontre. Le moteur la lie deja au deck additionnel (player.py:99)."""
    return player.additional_discard_pile


def IconesDeBoostDe(face: 'CardFace') -> int:
    """Le nombre d'icones de boost d'une carte — LE PRIX d'un sbire REGISTERED.

    ⚠ `CountBoostIconsInternal` et non `printed_boost` : le premier passe par
    le message du moteur, donc il voit les modificateurs. C'est indispensable,
    `ip008` Director of Security retirant une icone a la premiere carte
    revelee de chaque round.
    """
    if face is None:
        return 0
    lire = getattr(face, "CountBoostIconsInternal", None)
    return lire() if lire is not None else 0


def RedirectionVersLeDeckRegistered(player: 'Player') -> 'Ability':
    """« REGISTERED allies get put into the REGISTERED deck discard pile when
    defeated, while REGISTERED deck minions get put into the ENCOUNTER deck
    discard pile » (insert).

    La carte appartient au JOUEUR : sans rien, le moteur la range dans SA
    defausse a lui, dans les DEUX cas. On redirige donc les deux.

    ⚠⚠ CETTE CAPACITE SE POSE SUR CHAQUE FACE, ET IL Y EN A DEUX. `ip001b` la
    pose sur les 20 faces de sbire au montage ; `RecruterCommeAllieRegistered`
    la repose sur la face d'ALLIE apres la conversion. Sans le second
    passage, un allie recrute puis vaincu partait dans la defausse du joueur —
    la face de sbire n'etant plus la face active, son effet ne s'appliquait
    plus. Mesure du 10/09/2026 : « was discarded to Iron Patriot's
    DiscardPile ».

    ⚠ Le tri se fait sur `MARQUEUR_RECRUTE`, pose sur la CARTE, et non sur le
    trait REGISTERED : au moment de la defausse la face d'origine est parfois
    deja revenue.
    """
    def vers_la_bonne_defausse(effect: 'Effect',
                               message: 'Message.WhenCardWouldMoveToArea') -> None:
        this = effect.this
        if player.discard_pile != message.into_area and \
                player.player_deck != message.into_area:
            return

        if getattr(this.card, MARQUEUR_RECRUTE, False) or \
                this.HasTrait(TRAIT_REGISTERED):
            if player.discard_pile == message.into_area:
                message.ChangeToArea(DefausseRegistered(player), effect)
            else:
                message.ChangeToArea(DeckRegistered(player), effect)
            return

        rencontre = Worlds.GetEncounterDiscardPile(effect)
        if rencontre is not None:
            message.ChangeToArea(rencontre, effect)

    return AbilityFactory.WhenCardWouldMoveToArea(
        AbilityType.Temp0,
        "This",
        vers_la_bonne_defausse,
        conditions=[
            lambda e, m:
                player.discard_pile == m.into_area or
                player.player_deck == m.into_area
        ],
    )


def RecruterCommeAllieRegistered(minion: 'CardFace', player: 'Player',
                                 effect: 'Effect') -> bool:
    """« take control of that minion and treat it as a REGISTERED ally ».

    `Faces.TreatAsAlly` echange la FACE du sbire contre celle du gabarit, en
    recopiant son nom, son image, son ATQ et — c'est le point — sa MNG
    imprimee dans la CTR de l'allie.

    ⚠⚠ MAIS ELLE NE RECOPIE PAS LES CAPACITES, ET C'EST TOUT LE PACK QUI EN
    DEPEND. `TreatAsAlly` appelle `minion.card.SwapCardFace(face, effect)`
    puis `CardFactory.FaceRegisterEffects(face)` (faces.py:361) : la nouvelle
    face est celle du GABARIT `registered_ally`, qui n'a AUCUNE capacite. Le
    « Special » imprime du sbire, et tout le reste de sa boite a outils,
    disparaissaient donc a la seconde meme ou l'on payait pour les obtenir.
    Mesure du 09/09/2026. L'insert dit exactement le contraire, deux fois :
      « Unlike the CONTROLLED trait, these minions are ABLE TO USE THEIR
        ABILITIES while working under Iron Patriot. »
      « Each of these REGISTERED deck minions has a special ability that
        Norman can use. »
    On releve donc TOUTES les capacites de la face du sbire AVANT l'echange et
    on les reinscrit sur la face d'allie. Partager l'objet `Ability` est le
    modele du moteur lui-meme : `CardsDB.ability_cache` rend LE MEME objet aux
    trois exemplaires d'une carte (database.py:217).

    ⚠ Les MOTS-CLES, eux, disparaissent bien — Guard, Patrol, Incite,
    Villainous, Retaliate : ils viennent de `desc`, pas d'une capacite, et
    c'est la face echangee qui les porte. Un allie ne garde pas la garde. Rien
    a faire pour cela, c'est deja le comportement.

    ⚠⚠ ON NE PEUT PAS REINSCRIRE LES OBJETS `Ability` DEJA EN PLACE. Le moteur
    lie chaque capacite a SON papier des sa premiere inscription
    (`face_ability.py:18`, `ability.paper = self.face.paper`) et refuse ensuite
    de la poser ailleurs (`card.py:316`,
    `assert ability.paper == self.face.paper`). Mesure du 09/09/2026 :
    `AssertionError: ability.paper=Paper(card_id='ip020') self.face.paper=
    Paper(card_id='registered_ally')`.
    La sortie est de RECHARGER le module du sbire : `GetAbilities()` rend des
    objets NEUFS, dont le `paper` est encore vide, et qui s'inscrivent donc
    sans discuter. Le cache du moteur (`CardsDB.ability_cache`) n'est pas
    touche : il garde les siens pour la face de sbire.
    """
    neuves = _CapacitesNeuvesDuSbire(minion)
    traits = list(getattr(minion.paper, "traits", []) or [])
    carte = minion.card
    if not Faces.TreatAsAlly(minion, GABARIT_ALLIE_REGISTERED, player, effect):
        return False
    allie = minion.card.face
    if allie is None:
        return False
    if neuves:
        effets = allie.effect.Registers(*neuves)
        _AmorcerLesEffetsContinus(effets)
    # ⚠⚠ LES TRAITS IMPRIMES NE SUIVENT PAS NON PLUS. `TreatAsAlly` recopie le
    # nom, l'image, l'ATQ et la MNG, mais le gabarit `registered_ally` ne porte
    # que REGISTERED : Bullseye recrute cessait d'etre ASSASSIN, AVENGER et
    # ELITE, et surtout les trois H.A.M.M.E.R. cessaient d'etre H.A.M.M.E.R. —
    # ce qui vide de sens `ip021` Suppressive Fire et `ip022` Counter
    # Intelligence, dont toute la valeur se compte « for each H.A.M.M.E.R.
    # character in play ». La regle imprimee dit « TREAT IT AS a REGISTERED
    # ally » : la carte reste elle-meme, elle CHANGE DE CAMP.
    for trait in traits:
        if trait and not allie.HasTrait(trait):
            allie.GainTraits(1, trait, effect)
    setattr(carte, MARQUEUR_RECRUTE, True)
    # La face d'allie doit connaitre le chemin du retour, elle aussi.
    allie.effect.Registers(RedirectionVersLeDeckRegistered(player))
    return True


def _CapacitesNeuvesDuSbire(minion: 'CardFace') -> List['Ability']:
    """Recharge le module du sbire pour en tirer des capacites VIERGES.

    Meme resolution de chemin que le moteur (`cards/database.py:190`) :
    `cards.pack.<pack>.<set_name nettoye>.<card_id>`, avec repli sans set_name.
    Un module introuvable rend une liste vide — la carte perd son « Special »,
    ce qui est deja le comportement d'avant, jamais une erreur.
    """
    import importlib
    paper = getattr(minion, "paper", None)
    if paper is None:
        return []
    from engine.file.manager import FileManager
    set_name = FileManager.CleanName(paper.set_name or "")
    chemins = []
    if set_name:
        chemins.append(f"cards.pack.{paper.pack}.{set_name}.{paper.card_id}")
    chemins.append(f"cards.pack.{paper.pack}.{paper.card_id}")
    for chemin in chemins:
        try:
            module = importlib.import_module(chemin)
        except Exception:
            continue
        fabrique = getattr(module, "GetAbilities", None)
        if fabrique is None:
            continue
        return list(fabrique())
    return []


def JoueurQuiControle(face: 'CardFace') -> "Player|None":
    """Le joueur qui controle cette carte, ou None si ce n'est pas un joueur.

    ⚠⚠ `CardFace.GetControlByPlayer()` AFFIRME que le controleur est un joueur
    (`assert isinstance(owner, Player)`, card_face.py:972). Sur une carte du
    deck REGISTERED c'est FAUX la moitie du temps : tant qu'on ne l'a pas
    payee, elle est un sbire du SCENARIO. `ip028` Taskmaster levait
    `AssertionError` a chaque recalcul de son bonus, 32 fois sur 16 parties
    d'autoplay le 10/09/2026 — et jamais dans un cas, ou il est toujours deja
    allie.
    """
    if face is None:
        return None
    proprietaire = face.GetControlBy()
    return proprietaire if Player.IsType(proprietaire) else None


def AlliesRegistered(player: 'Player') -> List['CardFace']:
    """Les allies REGISTERED que ce joueur controle.

    ⚠ On lit le TRAIT sur la face en jeu, pas le papier : `ip001a` Iron Patriot
    donne le trait REGISTERED a CHAQUE allie qu'il controle, y compris ceux qui
    ne viennent pas du deck REGISTERED.
    """
    if player is None:
        return []
    return [f for f in player.allies.Get()
            if f is not None and f.HasTrait(TRAIT_REGISTERED)]


NOM_OBLIGATIONS_DU_CABAL = "Cabal Obligations"


def AlliesRegistredPouvantResoudreUnSpecial(player: 'Player') -> List['CardFace']:
    """Les allies REGISTERED dont ce joueur peut resoudre le « Special ».

    ⚠⚠ C'EST LE SEUL POINT DE PASSAGE, ET C'EST VOULU. `ip018` Cabal
    Obligations dit « REGISTERED allies you control cannot ... resolve
    "Special" abilities », mais `Message.WhenResolveSpecialAbility` n'est pas
    annulable cote moteur (sender_player.py:405, pas de `CanBeInstead`). Le
    blocage se pose donc a la source : les trois cartes du pack qui resolvent
    un « Special » d'allie — `ip001b` Norman Osborn, `ip009` Total Authority
    et `ip028` Taskmaster pour la defausse — lisent leurs cibles ici, et ici
    seulement. Cabal Obligations attachee, la liste est vide et plus rien n'est
    proposable : c'est exactement ce que le joueur doit voir.
    """
    allies = AlliesRegistered(player)
    if not allies:
        return []
    identite = player.GetIdentity() if player is not None else None
    if identite is not None:
        for attachee in identite.GetInventoryDeck().GetAll():
            if attachee is not None and attachee.IsName(NOM_OBLIGATIONS_DU_CABAL):
                return []
    return allies


def SpecialRegistered(nom: str, operation, *, conditions=[]) -> 'Ability':
    """Declare la capacite « Special » NOMMEE d'une carte REGISTERED.

    Toutes les cartes du deck en portent une, et trois cartes du pack les
    resolvent : `ip001b` Norman Osborn, `ip009` Total Authority et `ip028`
    Taskmaster (celui-la jusque dans la DEFAUSSE du deck REGISTERED).

    ⚠ La fabrique FORCE `AbilityType.Special` : on ne peut pas y declarer un
    sous-type « heros » ou « alter ego ». Lecon deja ecrite sur `sm011`.
    """
    return AbilityFactory.WhenResolveSpecialAbility(
        "This",
        operation,
        conditions=conditions,
    ).SetName(nom)


# ===========================================================================
# « THE FIRST CARD REVEALED FROM THE REGISTERED DECK THIS ROUND »
#
# Deux cartes imprimees s'appuient sur cette notion, et elles n'ont pas la meme
# fenetre : `ip020` H.A.M.M.E.R. Agents la lit DANS SON « When Revealed », et
# `ip008` Director of Security la lit AU MOMENT DU PAIEMENT, qui peut tomber a
# la fin du round (`ip002a` Registration Act). Il faut donc retenir non pas un
# booleen fugace mais QUELLE FACE etait la premiere, et pour QUEL round.
#
# Le moteur ne tient pas ce compteur : on l'accroche a `effect.world`, comme le
# font deja `jessica_jones` (manigances vaincues du round) et `moon_knight`
# (aspects joues du round). `world.round_id` est le numero de round du moteur.
# ===========================================================================

ATTR_PREMIERE_REVELEE = "iron_patriot_premiere_revelee_registered"


def _revelations(world: Any) -> Any:
    table = getattr(world, ATTR_PREMIERE_REVELEE, None)
    if table is None:
        table = {}
        setattr(world, ATTR_PREMIERE_REVELEE, table)
    return table


def EstLaPremiereRevelationDuRound(player: 'Player', effect: 'Effect') -> bool:
    """Vrai si AUCUNE carte du deck REGISTERED n'a encore ete revelee ce round.

    A appeler AVANT de reveler : c'est la question que pose `ip020`.
    """
    world = effect.world
    entree = _revelations(world).get(id(player))
    return entree is None or entree[0] != world.round_id


def MarquerLaRevelation(player: 'Player', effect: 'Effect', face: 'CardFace',
                        *, premiere: bool) -> None:
    """Enregistre la revelation. Seule la PREMIERE du round est retenue."""
    if not premiere:
        return
    _revelations(effect.world)[id(player)] = (effect.world.round_id, face)


def EstLaPremiereReveleeDuRound(player: 'Player', effect: 'Effect',
                                face: 'CardFace') -> bool:
    """Vrai si CETTE face est la premiere revelee du deck REGISTERED ce round.

    ⚠ On compare l'identite de la face, pas son nom : le deck contient trois
    exemplaires de H.A.M.M.E.R. Agents, et la reduction de `ip008` ne vaut que
    pour celui qui a ete revele en premier.
    """
    entree = _revelations(effect.world).get(id(player))
    return (entree is not None
            and entree[0] == effect.world.round_id
            and entree[1] is face)


def RevelerEtProposerLeRecrutement(player: 'Player', effect: 'Effect', *,
                                   a_la_fin_du_round: bool) -> None:
    """Le geste central du pack, partage par les DEUX faces de la manigance.

    L'insert du pack le decrit mot pour mot :
      « When you reveal a minion from the REGISTERED deck, it enters play as a
        minion first and RESOLVES ANY REVEALED EFFECTS. After this, you may
        spend resources equal to the number of boost icons on that minion's
        card to take control of it as a REGISTERED ally. If you do not, it
        remains in play as a minion engaged with you. »

    `a_la_fin_du_round` est la SEULE difference entre les deux faces :
      - `ip002a` Registration Act fait payer « at the end of the round » ;
      - `ip002b` Dark Reign fait payer tout de suite.
    Contrer la manigance, c'est gagner ce temps-la.

    ⚠⚠ ON REVELE, ON NE POSE PAS. `Deck.RevealTopCard` -> `face.Reveal`
    (face_on_event.py:245) enchaine tout seul : mise en jeu du sbire, engagement
    avec le joueur (minion.py:57), puis resolution du « When Revealed » et de
    `Surge`. Une premiere version appelait `PutIntoPlay` + `EngagePlayer` a la
    main : elle mettait bien le sbire en jeu, mais LE « WHEN REVEALED » NE
    PARTAIT JAMAIS — donc `ip020` H.A.M.M.E.R. Agents, dont c'est toute la
    carte, etait mort. L'insert tranche : « resolves any revealed effects ».

    ⚠ Le prix est lu au MOMENT DU PAIEMENT, pas a la revelation : entre les
    deux, `ip008` Director of Security a pu retirer une icone.

    ⚠ Trois raisons de ne rien proposer apres la revelation : le sbire n'est
    plus en jeu (vaincu par un effet revele), il n'est plus un sbire (`ip020`
    l'a deja converti en allie), ou le deck etait vide.
    """
    deck = DeckRegistered(player)
    if deck.GetSize() == 0:
        return

    # ⚠⚠ ON MARQUE AVANT DE REVELER. Le « When Revealed » de `ip020`,
    # `ip021` et `ip022` demande « if this is the first card revealed from the
    # REGISTERED deck this round » ET IL SE RESOUT PENDANT `RevealTopCard`.
    # Marquer apres coup, c'est lui repondre non a chaque fois.
    attendu = deck.GetTop()
    if attendu is None:
        return
    MarquerLaRevelation(player, effect, attendu,
                        premiere=EstLaPremiereRevelationDuRound(player, effect))
    if attendu is not None:
        # Une carte qui ressort du deck REGISTERED repart de zero : tant qu'on
        # ne l'a pas repayee, elle n'est qu'un sbire.
        setattr(attendu.card, MARQUEUR_RECRUTE, False)
    sbire = deck.RevealTopCard(player, effect)
    if sbire is None:
        return

    def proposer() -> None:
        if not sbire.IsInPlay() or not Minion.IsType(sbire):
            return
        prix = IconesDeBoostDe(sbire)

        def recruter(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            RecruterCommeAllieRegistered(sbire, player, effect)

        player.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Take control of that minion as a REGISTERED ally",
                recruter,
            ).SetHasNoTargetEffect()
            .SetCostFunc(CostFunc.Spend(Cost(str(prix)))),
        )

    if a_la_fin_du_round:
        RunAt.RoundEnd(effect, proposer)
    else:
        proposer()


def RevelerLeDessusDuDeckRegistered(player: 'Player', effect: 'Effect') -> 'CardFace|None':
    """Revele le dessus du deck REGISTERED, SANS proposer de le recruter.

    Deux cartes revelent sans offrir le marche : `ip019` Assembled Resistance
    (le texte s'arrete a « put it into play engaged with you » — c'est une
    punition) et rien d'autre. Le marquage « premiere du round » vaut quand
    meme : le texte de `ip020` dit « revealed from the REGISTERED deck », sans
    preciser par quoi.
    """
    deck = DeckRegistered(player)
    if deck.GetSize() == 0:
        return None
    attendu = deck.GetTop()
    if attendu is None:
        return None
    MarquerLaRevelation(player, effect, attendu,
                        premiere=EstLaPremiereRevelationDuRound(player, effect))
    setattr(attendu.card, MARQUEUR_RECRUTE, False)
    return deck.RevealTopCard(player, effect)


def SiPremiereReveleeAlorsAllie() -> 'Ability':
    """« When Revealed: If this is the first card revealed from the REGISTERED
    deck this round, put this card under your control as a REGISTERED ally. »

    Le texte est IDENTIQUE sur les trois cartes H.A.M.M.E.R. du deck (`ip020`,
    `ip021`, `ip022`), qui sont aussi les trois seules a trois exemplaires. Il
    dit deux choses : la pietaille se rallie GRATUITEMENT — on ne paie pas ses
    icones de boost — mais une seule fois par round.

    ⚠⚠ ELLE N'EST PAS MONTEE SUR `WhenThisRevealed`, ET C'EST OBLIGE. Convertir
    le sbire PENDANT sa revelation le sort du jeu en tant que sbire, et le
    moteur verifie juste apres qu'un sbire revele est bien engage :
    `minion.py:41`, `assert self.card.world.is_game_over,
    f"{self.engaged_player=}"`. Mesure du 09/09/2026 :
    `AssertionError: self.engaged_player=None`.
    On se pose donc une fenetre plus tard, sur `AfterCardRevealedEnd`, qui est
    envoye APRES cette verification (face_on_event.py:333). Le joueur ne voit
    aucune difference : la conversion conclut la revelation.
    """
    def action(effect: 'Effect', message: 'Message.AfterCardRevealedEnd') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        if joueur is None or not this.IsInPlay():
            return
        if not EstLaPremiereReveleeDuRound(joueur, effect, this):
            return
        RecruterCommeAllieRegistered(this, joueur, effect)

    return AbilityFactory.AfterPlayerRevealCard(
        AbilityType.ForcedResponse,
        "AnyPlayer",
        "This",
        action,
    )


def PersonnagesHammerEnJeu(effect: 'Effect') -> int:
    """« for each H.A.M.M.E.R. character in play » (`ip021`, `ip022`).

    ⚠ IN PLAY, pas « you control » : les sbires H.A.M.M.E.R. encore ennemis
    comptent, et Iron Patriot lui-meme porte le trait. Trois Commandos en jeu
    plus le heros, cela fait quatre.
    """
    return len(Worlds.FindCardsOnField(effect, trait=TRAIT_HAMMER,
                                       card_type=Unit2))


def _AmorcerLesEffetsContinus(effets: Sequence['Effect']) -> None:
    """Allume les bonus continus qu'on vient d'inscrire sur la face d'allie.

    ⚠⚠ TROISIEME PIEGE DE LA CONVERSION, et le plus discret. Un bonus continu
    (`AbilityFactory.ThisGainKeyword`, et toute la famille `WhileValid`) n'est
    pas evalue a l'inscription : la fabrique le suspend a
    `WhenCardEnterPlay("This")` (on_while.py:177), et ne le calcule qu'a
    l'entree en jeu de la carte. Or on inscrit APRES l'echange de face, donc
    APRES que la face d'allie soit entree en jeu : le message est deja passe,
    et le bonus reste eteint pour toujours.
    Mesure du 09/09/2026 : `ip028` Taskmaster recrute restait a ATQ 0, alors
    meme que sa propre presence aurait du lui donner +1.

    On rejoue donc la fenetre a la main, et UNIQUEMENT pour ces effets-la :
    `when == Message.WhenCardEnterPlay` et type `NonKeyword`, ce qui est la
    signature exacte du paquet monte par `WhileValid`. Aucune capacite
    imprimee du pack n'a cette forme, il n'y a donc rien d'autre a reveiller.
    """
    for effet in effets:
        ability = getattr(effet, "ability", None)
        if ability is None:
            continue
        if ability.when is not Message.WhenCardEnterPlay:
            continue
        if ability.type is not AbilityType.NonKeyword:
            continue
        ability.operation(effet, None)
