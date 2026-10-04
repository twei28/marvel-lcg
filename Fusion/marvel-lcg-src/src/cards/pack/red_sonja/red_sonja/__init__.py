from cards.pack import *

# ---------------------------------------------------------------------------
# Le mecanisme partage « She-Devil » (rs001a) : jouer un evenement de la main
# a cout -1, et laisser cet evenement savoir qu'il a ete joue AINSI (rs006,
# rs007, rs008 portent chacun « If you used your "She-Devil" ability to
# reduce the cost of this card, ... »).
#
# ⚠ Pas de fabrique native pour « cet evenement precis sait qu'une AUTRE
# capacite a paye sa reduction de cout ». Choix retenu : un marqueur POSE
# DIRECTEMENT SUR L'OBJET `Card` (pas un dict global cote module -- un
# process peut heberger plusieurs parties en meme temps, un dict par carte
# EVITE toute fuite entre parties). Pose a `True` juste avant l'appel a
# `PlayCardsLikeInTurn` (qui resout la capacite `Play` de la carte de facon
# SYNCHRONE avant de rendre la main), relu par la carte jouee dans son propre
# `GetAbilities()`, puis remis a `False` juste apres. A verifier en jeu reel
# (test_capacites.py + substitution) : c'est le point le plus original de ce
# portage.
#
# ⚠⚠ DEUX CORRECTIFS (23/09/2026, trouves par un cas reel de
# test_capacites.py) :
#
# 1) La PREMIERE version choisissait la carte a jouer via un `AskChooseFace`
#    BRUT (hors du mecanisme de ciblage standard), puis appelait
#    `PlayCardsLikeInTurn` directement dans le corps de l'Action. Modele qui
#    MARCHE, `ar001a` Bring the War (branche « play an event from your hand,
#    ignoring its resource cost ») : la carte a jouer est choisie par le
#    MECANISME DE CIBLAGE STANDARD d'un `ForChoiceAbility(...)
#    .SetTarget(Event, canbe_play=True, from_where=["YourHandCards"])`.
#    Reecrit sur ce modele (n'a pas suffi seul, voir 2).
#
# 2) LE VRAI BUG : `update_resources_cost` de `PlayCardsLikeInTurn`
#    (player_action.py:937) attend une valeur **NEGATIVE** pour REDUIRE le
#    cout (`update_resources_cost=-1` = « -1 au cout »), jamais positive --
#    verifie en relisant TOUS les appels existants du depot (`12024.py`,
#    `49017.py`, `27054.py`, `26036.py`, `51001b.py`, `61008.py`, `55012.py` :
#    tous passent une valeur negative). `update_resources_cost=1` (positif)
#    AUGMENTE le cout de 1 au lieu de le reduire -- confirme par un cas reel
#    (rs006 passait de cout 2 a 3, pas 2 a 1, `target_payment.cost` trace a
#    l'appui) et par la lecture de la composition `ReduceCostToPlayThis` ->
#    `ReduceCostToPlayFaceWhen` -> `UpdateCostOfCardInternal` (deux negations
#    imbriquees qui n'annulent PAS un signe deja negatif du cote appelant).
#    Le nom du parametre est donc trompeur (« update » et non « reduce »),
#    a documenter dans RECETTES-MOTEUR si un futur portage en a besoin.
# ---------------------------------------------------------------------------

MARQUEUR_SHE_DEVIL = "rs_reduit_par_she_devil"


def AUtiliseSheDevil(face: 'CardFace') -> bool:
    """Est-ce que CETTE carte est en train d'etre jouee via l'Action
    « She-Devil » de rs001a (cout deja reduit de 1) ? A lire au moment de la
    resolution de la capacite `Play` de la carte elle-meme, jamais plus tard.
    """
    return bool(getattr(face.card, MARQUEUR_SHE_DEVIL, False))


def JouerEvenementReduitParSheDevil(effect: 'Effect', joueur: 'Player') -> None:
    """« Action: Exhaust a WEAPON upgrade you control -> play an event from
    your hand, reducing its resource cost by 1. » Le cout (exhaust WEAPON)
    est pose par l'appelant via `.SetCostFunc(CostFunc.Exhaust(trait="WEAPON"))` ;
    cette fonction ne fait que l'effet, via le mecanisme de ciblage standard
    (modele `ar001a`).
    """
    def jouer(cibles: Sequence['CardFace']) -> None:
        faces = [c for c in cibles if c is not None]
        if not faces:
            return
        choisi = faces[0]
        setattr(choisi.card, MARQUEUR_SHE_DEVIL, True)
        try:
            joueur.PlayCardsLikeInTurn(
                [choisi], effect, update_resources_cost=-1, forced=True,
            )
        finally:
            setattr(choisi.card, MARQUEUR_SHE_DEVIL, False)

    joueur.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility(
            "Play an event from your hand, reducing its resource cost by 1",
            jouer,
        ).SetTarget(Event, canbe_play=True, from_where=["YourHandCards"]),
    )


def QueenDeSogariaEstEnVitrine(effect: 'Effect') -> bool:
    """rs009 Queen of Sogaria est-elle dans la vitrine de victoire ?

    ⚠⚠ POURQUOI CETTE FONCTION EXISTE ET OU ELLE EST APPELEE (23/09/2026,
    bug trouve PAR le cas de test de rs009, pas a la lecture). « While Queen
    of Sogaria is in the victory display, Red Sonja GAINS: Response... » avait
    d'abord ete implemente DIRECTEMENT SUR rs009 elle-meme (capacite posee
    dans son propre `GetAbilities()`, condition = suis-je dans la vitrine).
    Ca ne peut JAMAIS se declencher : `DeckType.VictoryDisplay` porte
    `is_out_of_play=True` (deck_type.py) et `CardFace.IsInPlay()` teste
    `self.card.IsOnField()` -> `area.flags.is_in_play`, donc AUCUNE capacite
    d'une carte assise dans la vitrine n'est jamais enregistree aupres du bus
    de messages, quelle que soit la condition ecrite a l'interieur -- le
    handler n'est simplement jamais appele. `works_in_the_victory_display`
    (environment_helper.py) existe bien pour ce cas de figure, mais UNIQUEMENT
    via `GiveKeywordToInPlayWhenApplyThis` (mot-cle/statistique en scan
    continu) : aucune fabrique publique n'accorde une capacite ARBITRAIRE de
    cette facon.
    Corrige en deplacant la capacite sur L'IDENTITE (rs001a.py), qui reste
    TOUJOURS en jeu : cette fonction lit juste la zone de rs009 a l'instant T.
    """
    from game.operate.worlds import Worlds
    return any(
        getattr(f.paper, "card_id", None) == "rs009"
        for f in Worlds.VictoryDisplay(effect).GetAll()
    )


def CapaciteQueenDeSogariaEnVitrine() -> 'Ability':
    """La Reponse « While Queen of Sogaria is in the victory display... »,
    postee IDENTIQUEMENT sur les deux faces de l'identite (rs001a ET rs001b)
    -- le texte imprime ne restreint pas a une forme, et seule la face
    ACTIVEMENT en jeu enregistre ses propres capacites (`CardFace.
    GetAbilities()` est par FACE, jamais partage entre les deux faces d'une
    meme identite). La poser sur une seule face l'aurait rendue inerte des
    que le joueur change de forme.
    """
    def queen_en_vitrine(effect: 'Effect', message: 'Message.AfterCardExhausted') -> bool:
        return QueenDeSogariaEstEnVitrine(effect)

    def hyrkanium_blade_exhaustee(effect: 'Effect', message: 'Message.AfterCardExhausted') -> bool:
        return Condition.CheckWhichCard(
            CardFinder(name="Hyrkanium Blade"), message.trigger, effect,
        )

    def piocher(effect: 'Effect', message: 'Message.AfterCardExhausted') -> None:
        Unused(message)

        joueur = effect.GetInitiator()
        if isinstance(joueur, Player):
            joueur.DrawUp(1, effect)

    return (
        Ability(
            AbilityType.Response,
            Message.AfterCardExhausted,
            [queen_en_vitrine, hyrkanium_blade_exhaustee],
            piocher,
        ).SetName("Queen of Sogaria (victory display)")
        .LimitOncePerRound()
    )


def DegatsExcedentairesDeCetteAttaque(effect: 'Effect', cibles: Sequence['CardFace'],
                                       degats: int) -> int:
    """Inflige `degats` a `cibles` via l'attaque de CETTE carte (`effect.this`),
    et rend le total des DEGATS EXCEDENTAIRES (au-dela des PV restants d'une
    cible vaincue par cette attaque precise). Modele `ar005` Ares' Battle Helm
    (`AfterUnitDefeatedUnit(is_from_attack=True, has_excess_damage=True)`,
    `message.excess_damage`), capte ici par un ecouteur TEMPORAIRE scope a la
    seule resolution en cours (`until_resolve_effect=effect` : la defaite
    eventuelle arrive de facon SYNCHRONE pendant `DealDamage` ci-dessous,
    avant que cette fonction ne rende la main).

    ⚠⚠ BUG REEL TROUVE PAR LE CAS DE TEST DE rs003 (23/09/2026) :
    `unregister_after_exec=True` COMBINE a `until_resolve_effect` faisait
    lever `AssertionError` (`face_effect.py:110`,
    `assert unregister_after_exec == False`) DES QUE l'ecouteur recevait
    vraiment un message -- c'est-a-dire des qu'un ennemi etait REELLEMENT
    vaincu par cette attaque, jamais avant. `AfterUnitDefeatedUnit` produit
    une capacite `is_delay_ability`, pour laquelle le moteur EXIGE
    `unregister_after_exec=False` (le demontage doit passer par un des
    `until_*`, jamais par le drapeau immediat). L'exception, non rattrapee,
    faisait echouer TOUTE la resolution de la carte (degats deja infliges,
    carte deja defaussee, mais reduction de cout JAMAIS appliquee) --
    silencieusement du point de vue du joueur (juste un `<F> Traceback` au
    journal moteur). Aucun cas de test n'avait auparavant fait tuer une
    cible via cette fonction, donc jamais declenche.
    """
    this = effect.this.CastTo(Event)
    total = {"val": 0}

    def capter(effet_temp: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        total["val"] += int(getattr(message, "excess_damage", 0) or 0)

    effect.this.effect.RegisterTemp(
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Temp0, "You", Enemy, capter,
            is_from_attack=True, has_excess_damage=True,
        ),
        unregister_after_exec=False,
        until_resolve_effect=effect,
    )

    this.DealDamage(cibles, degats, effect)
    return total["val"]


def MenaceExcedentaireDeCeContre(effect: 'Effect', cibles: Sequence['CardFace'],
                                  menace: int) -> int:
    """Retire `menace` menace de `cibles` (une manigance normalement, un
    contre visant une seule cible), et rend la MENACE EXCEDENTAIRE (le
    retrait au-dela de ce qui restait sur la manigance). ⚠ « Excess threat »
    n'est PAS un concept officiel du moteur (contrairement a « excess
    damage », voir `DegatsExcedentairesDeCetteAttaque` ci-dessus) : calcul
    direct, lu AVANT le retrait (`CardFace.threat`), pas via un message.
    """
    this = effect.this.CastTo(Event)
    total_exces = 0
    for cible in cibles:
        avant = cible.CastTo(Scheme2).threat
        total_exces += max(0, menace - avant)

    this.RemoveThreatFromSchemes(cibles, menace, effect)
    return total_exces
