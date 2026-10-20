from cards.pack import *

# ===========================================================================
# Pack DAZZLER — contenu custom de Lord Havok.
#
# Tout le set tourne autour d'une zone, la SETLIST, et d'une seconde capacite
# imprimee sur les evenements, « Showtime! ».
#
# LE CYCLE
#   1. Tu joues un evenement [[SONG]] et tu resous son « Hero Action ».
#   2. Live Concert (dz017a) le rattrape et l'attache a cote d'elle : c'est la
#      Setlist, 4 places, sans remplacement possible.
#   3. « Rehearsal » (le heros, dz001a) pose un compteur `sound` sur un SONG de
#      la Setlist qui n'en a pas, et resout son « Showtime! ».
#   4. La Hero Action de Live Concert la retourne sur Showtime! (dz017b), qui
#      resout TOUS les « Showtime! » de la Setlist, la vide, et si 4 cartes en
#      sont parties : 4 degats ou 4 menaces.
#
# ---------------------------------------------------------------------------
# COMMENT « Showtime! » EST RENDU
# ---------------------------------------------------------------------------
# Le moteur sait deja resoudre une capacite d'un TYPE donne sur une autre
# carte : `Faces.ResolveAbility(faces, player, ability_type, effect)`, utilisee
# par des cartes officielles (Quatre Cavaliers 45090, Celestial Tech 45158).
# Il fallait donc un type de capacite libre, que rien d'autre n'emploie.
#
# `AbilityType.Special` est exactement cela : il est declare, ses flags
# existent (`ui_display_name`, donc le nom s'affiche), il est absent de
# TYPE_PRIORITY mais celui-ci a un defaut — et AUCUNE carte du jeu ne
# l'utilise. Aucune modification du moteur n'a donc ete necessaire.
#
# La capacite est accrochee a un message qui ne lui parvient jamais, et sa
# condition est fausse par construction : elle ne peut PAS se declencher toute
# seule, elle n'est joignable que par `ResoudreShowtime`.
# ===========================================================================

NOM_HEROS = "Dazzler"
NOM_CONCERT = "Live Concert"
NOM_SHOWTIME = "Showtime!"
TRAIT_SONG = "SONG"
COMPTEUR = "sound"
PLACES_SETLIST = 4


def Showtime(operation: Any) -> 'Ability':
    """La seconde capacite d'un [[SONG]], celle qui n'agit que dans la Setlist.

    Elle n'est jamais declenchee par un message : `jamais` la verrouille, et
    seule `ResoudreShowtime` sait l'atteindre. `NoOutOfPlayLimit` est
    indispensable : la carte vit dans la Setlist, que le moteur ne compte pas
    comme « en jeu ».
    """
    def jamais(effect: 'Effect', message: 'Message2') -> bool:
        return False

    return Ability(
        AbilityType.Special,
        Message.WhenCardRevealed,
        [jamais],
        operation,
    ).SetName(NOM_SHOWTIME).NoOutOfPlayLimit()


def ResoudreShowtime(faces: Sequence['CardFace'], player: 'Player',
                     effect: 'Effect') -> int:
    """Resout le « Showtime! » de chaque carte donnee. Rend le nombre resolu."""
    return Faces.ResolveAbility(faces, player, AbilityType.Special, effect)


def CiblesShowtime(effect: 'Effect', nombre: int = 1) -> List['CardFace']:
    """Fait CHOISIR au joueur la cible d'un « Showtime! ».

    POURQUOI CE HELPER EXISTE
    -------------------------
    Un « Showtime! » n'est jamais joue par le joueur : il est resolu par une
    AUTRE carte (Rehearsal, ou le retournement de Showtime!). Or le chemin du
    moteur, `CardFace.ResolveAbility` (card_face.py:797), remplit les cibles
    tout seul :

        found_effect.context.targets_internal = all_legal_targets[:min_target_num]

    Autrement dit il prend LA PREMIERE cible legale, sans rien demander. Les
    filtres sont bien respectes — un ELITE ne sera jamais visee si la carte
    l'exclut — mais le joueur ne choisit pas LEQUEL des ennemis valides encaisse.

    On garde donc le `SetTarget(...)` de chaque carte, qui reste la source de
    verite des cibles LEGALES, mais avec un minimum de 0 pour que le moteur ne
    presume de rien ; puis on relit `all_legal_targets` et on pose la question.
    L'utilisateur a tranche pour ce comportement le 29/08/2026.
    """
    joueur = effect.GetInitiator()
    candidats = [f for f in (effect.context.all_legal_targets or [])
                 if f is not None]
    if joueur is None or not candidats:
        return []
    if len(candidats) <= nombre:
        return candidats[:nombre]
    choisie = joueur.AskChooseOneText(candidats)
    return [choisie] if choisie is not None else []


# ---------------------------------------------------------------------------
# La Setlist
# ---------------------------------------------------------------------------
def Concert(effect: 'Effect', joueur: 'Player|None'=None) -> 'CardFace|None':
    """Live Concert en jeu, quelle que soit sa face, chez le joueur courant.

    Les deux faces portent des noms differents : on cherche donc les deux.

    `joueur` est indispensable pour les cartes RENCONTRE : quand une trahison
    est revelee depuis le deck rencontre, l'initiateur de l'effet est le VILAIN,
    et `effect.GetInitiator()` leve alors une assertion
    (`self.initiator=Rhino`, cf. game/effect/effect.py:417). Ces cartes-la
    passent le joueur vise, lu sur le message (`message.GetToPlayer()`).
    """
    if joueur is None:
        joueur = effect.GetInitiator()
    # ⚠ CORRECTIF DU 20/10/2026 (backlog 12) : le filtre etait passe en
    # `check_effect_fn` a `Worlds.FindCardOnField`, qui ne transmet pas l'effet
    # au `CardFinder` : le filtre n'etait JAMAIS appele (« Only call when has
    # effect », card_finder/checker.py) et la fonction rendait la Live Concert
    # de n'importe quel joueur. On filtre donc ici, a la main.
    for nom in (NOM_CONCERT, NOM_SHOWTIME):
        for face in Worlds.FindCardsOnField(effect, name=nom):
            if face is not None and face.GetControlByPlayer() == joueur:
                return face
    return None


def JoueurDeDazzler(effect: 'Effect') -> 'Player|None':
    """Le joueur dont l'identite est Dazzler (l'une ou l'autre forme).

    Pour les cartes qui NOMMENT la Setlist de Dazzler (« Dazzler's Setlist »,
    Stealing Sound dz022) : la carte peut etre revelee par un autre joueur.
    """
    for joueur in effect.world.players:
        identite = joueur.GetIdentity()
        if identite is None:
            continue
        heros = identite.GetHeroFace() if hasattr(identite, "GetHeroFace") else identite
        if heros is not None and heros.IsName(NOM_HEROS):
            return joueur
    return None


def Setlist(effect: 'Effect', joueur: 'Player|None'=None) -> List['CardFace']:
    """Les [[SONG]] actuellement dans la Setlist, dans l'ordre de pose."""
    concert = Concert(effect, joueur)
    if concert is None:
        return []
    zone = concert.GetPlacedCardArea()
    if zone is None:
        return []
    return list(zone.Get(True))


def SetlistALaPlace(effect: 'Effect') -> bool:
    """« to a maximum of 4 » : la Setlist accepte-t-elle une carte de plus ?"""
    return len(Setlist(effect)) < PLACES_SETLIST


# ---------------------------------------------------------------------------
# Le compteur `sound` sur les SONG de la Setlist
# ---------------------------------------------------------------------------
# Le compteur est pose LA OU LA CARTE LE DIT : « place 1 sound counter ON A
# SONG in the Setlist ». C'est un vrai compteur du moteur, sur la chanson
# elle-meme, pas une marque tenue a cote.
#
# Cela a demande une addition d'API dans le moteur : les evenements
# n'heritaient pas de `CanPlaceCounter`, parce qu'aucun evenement du jeu ne
# sejournait en jeu avant ce pack. Le correctif est commente dans
# `game/card/face/card_type/event.py` ; il n'alloue aucun etat nouveau, le
# composant de stockage existant deja sur toute carte.
#
# LIMITE D'AFFICHAGE (mesuree, et hors de notre portee) : la Setlist est batie
# sur la `PlaceCardArea`, declaree `is_out_of_play = True`
# (game/deck/deck_type.py:34), et `GetRenderInfo` (card_face.py:369) n'emet
# rien pour une carte hors jeu. Le jeton EXISTE sur la bonne carte, le journal
# l'annonce (« recoit 1 compteur(s) sound »), mais aucun badge ne se dessine
# dessus. Le corriger demanderait de rendre cette zone « en jeu », ce qui
# toucherait la vingtaine de cartes officielles qui s'en servent et la notion
# meme d'« en jeu » (ciblage, limites, declenchements).


def EstRepete(effect: 'Effect', face: 'CardFace') -> bool:
    Unused(effect)
    return face.CastTo(CanPlaceCounter).GetCounters(COMPTEUR) > 0


def MarquerRepete(effect: 'Effect', face: 'CardFace') -> None:
    """Pose le compteur `sound` : la chanson ne sera plus repetable."""
    face.CastTo(CanPlaceCounter).PlaceCountersInternal(1, COMPTEUR, effect)


def EffacerRepete(effect: 'Effect', face: 'CardFace') -> bool:
    """Retire le compteur `sound` (Sound Collector Suit). Vrai s'il y en avait un."""
    porteur = face.CastTo(CanPlaceCounter)
    if porteur.GetCounters(COMPTEUR) <= 0:
        return False
    porteur.RemoveCountersInternal(1, COMPTEUR, effect)
    return True


def OublierLaSetlist(effect: 'Effect', faces: Sequence['CardFace']) -> None:
    """La Setlist se vide : les jetons partent avec les cartes.

    Sans cela, une chanson ramenee par Encore et rejouee arriverait dans la
    Setlist en portant deja son jeton, ce qui n'est ecrit nulle part.
    """
    for face in faces:
        porteur = face.CastTo(CanPlaceCounter)
        if porteur.GetCounters(COMPTEUR) > 0:
            porteur.RemoveCountersInternal("All", COMPTEUR, effect)


def SongsSansCompteur(effect: 'Effect') -> List['CardFace']:
    """Les SONG de la Setlist SANS compteur `sound`.

    C'est la cible de « Rehearsal », qui n'accepte qu'un SONG « without a sound
    counter on it ».
    """
    return [f for f in Setlist(effect) if not EstRepete(effect, f)]


def SongsAvecCompteur(effect: 'Effect') -> List['CardFace']:
    """Les SONG deja repetes : la cible de Sound Collector Suit."""
    return [f for f in Setlist(effect) if EstRepete(effect, f)]


def EstUnSong(face: 'CardFace') -> bool:
    return Event.IsType(face) and face.HasTrait(TRAIT_SONG)


NOM_ANGOISSE = "Performance Anxiety"


def AngoisseEnJeu(effect: 'Effect') -> bool:
    """L'obligation « Performance Anxiety » (dz019) est-elle posee chez toi ?

    Elle interdit deux choses NOMMEMENT : le « Songwriter » de l'alter-ego
    (dz001b) et la Hero Action de Live Concert (dz017a). L'interdit est donc
    verifie LA OU il s'applique, sur les deux cartes concernees, plutot que
    depuis l'obligation : le moteur n'a pas de mecanisme pour eteindre une
    capacite nommee d'une autre carte.
    """
    joueur = effect.GetInitiator()
    if joueur is None:
        return False
    # Filtre a la main : `check_effect_fn` n'est pas appele par
    # `FindCardOnField` (voir `Concert`, correctif du 20/10/2026).
    return any(f is not None and f.GetControlByOrOwner() == joueur
               for f in Worlds.FindCardsOnField(effect, name=NOM_ANGOISSE))


def SongsDansLaDefausseBornee(effect: 'Effect', maximum: int = 4) -> int:
    """Le compte de [[SONG]] dans ta defausse, plafonne.

    Les quatre cartes d'aspect (dz024 a dz027) disent toutes « to a maximum of
    4 » : le plafond est imprime sur la carte, il n'est pas une limite du
    moteur.
    """
    joueur = effect.GetInitiator()
    if joueur is None:
        return 0
    return min(SongsDansLaDefausse(joueur), maximum)


def SongsDansLaDefausse(joueur: 'Player') -> int:
    """Combien de [[SONG]] dans ta defausse.

    Quatre cartes d'aspect comptent dessus (Song of Aggression / Justice /
    Leadership / Protection), plafonnees a 4 sur les cartes elles-memes.
    """
    total = 0
    for face in joueur.discard_pile.Get(True):
        if face is not None and face.HasTrait(TRAIT_SONG):
            total += 1
    return total


def RetirerUnStatut(face: 'CardFace', effect: 'Effect') -> bool:
    """« Remove a status card » : UNE carte de statut, pas toutes.

    CORRECTIF (partie reelle) : `Faces.RemoveStatus` N'EXISTE PAS. dz013 et
    dz028 plantaient sur `AttributeError: type object 'Faces' has no attribute
    'RemoveStatus'` des que le joueur choisissait l'option. Le retrait est une
    methode de la FACE — `DiscardStunned` / `DiscardConfused` / `DiscardTough`
    avec `rule=1` pour n'en enlever qu'une (can_status.py:98, modele Uncanny
    Resilience 07045 et The Thing th007).

    CORRECTIF DU 20/10/2026 (backlog 12) : « a status card » vise TOUTES les
    cartes d'etat du moteur (`CardFace.STATUS` : Stunned, Confused, Tough,
    Exposed, Cloaked, Dazed, Intensified), et quand le personnage en porte
    plusieurs, c'est le JOUEUR qui choisit laquelle part (RECETTES-MOTEUR §2,
    modele `RetirerUneCarteDeStatut` du pack donatello). L'ancienne version ne
    connaissait que Stunned / Confused / Tough et retirait d'office dans cet
    ordre. Le retrait passe par `LoseState`, le chemin commun des `Discard<X>`.
    """
    presents = [nom for nom in STATUTS_RETIRABLES if face.HasStatus(nom)]
    if not presents:
        return False
    unite = face.CastTo(CanStatus)

    def retirer(nom: str) -> None:
        unite.LoseState(nom, effect, 1)

    if len(presents) == 1:
        retirer(presents[0])
        return True
    joueur = effect.GetInitiator()
    if joueur is None:
        return False
    joueur.ChooseAbilities(
        effect,
        *[AbilityFactory.ForChoiceAbility(
            "Discard a %s status card" % nom,
            lambda cibles, nom=nom: retirer(nom))
          for nom in presents])
    return True


STATUTS_RETIRABLES = ("Stunned", "Confused", "Tough", "Exposed", "Cloaked",
                      "Dazed", "Intensified")
