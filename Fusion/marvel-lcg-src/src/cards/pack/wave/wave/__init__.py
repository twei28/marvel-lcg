from cards.pack import *

# ---------------------------------------------------------------------------
# La RISING TIDE AREA -- mecanique maison du pack Wave (auteure "Mysteltainn")
#
# L'insert la definit ainsi :
#   « Pearl Pangan/Wave has a unique area [...]. At the start of the game,
#     this area is empty, and cards can only be placed inside [...] by an
#     effect that explicitly places them in this area [...]. When a card is
#     placed [...], it is placed face-up, and can be flipped face-down by
#     effects that flip cards [...] face-down. Cards [...] cannot be affected
#     by effects that do not explicitly target the Rising Tide area.
#     At the end of the player phase, before players draw up to their hand
#     size, place all cards in the Rising Tide area in their owner's discard
#     pile. »
#
# La zone elle-meme vit dans le moteur (`player.rising_tide`,
# DeckType.RisingTideArea, voir les # AJOUT (pack wave) de
# game/deck/deck_type.py, game/player/player.py, game/render/to_descriptor.py,
# game/render/descriptor/world.py et game/ability/factory/turn_phase.py).
#
# ⚠ AUCUN NOUVEAU MECANISME DE FACE CACHEE. `Card.state.is_face_up` (par
# CARTE, pas par zone) et `Card.Flip()` existent deja nativement : pour une
# carte joueur ordinaire (`back_faces == []`), `Flip()` bascule ce booleen
# tout seul, sans jamais deplacer la carte. Le rendu envoie deja
# `down_card_ids = ['player']` (dos generique carte joueur) pour toute carte
# face cachee dont le proprietaire n'est pas le scenario -- verifie par
# lecture de `Card.Render()`, aucun code cote rendu a ecrire.
#
# Ce fichier ne porte que ce qui est propre AUX CARTES du pack : poser une
# carte dans la Rising Tide area, la retourner, et le crochet du paiement.
# ---------------------------------------------------------------------------


def PlacerFaceVisibleDansRisingTide(face: 'CardFace', effect: 'Effect') -> bool:
    """Deplace une carte dans la Rising Tide area de SON PROPRIETAIRE, et la
    retourne face visible.

    ⚠ ON RETOURNE NOUS-MEMES, SANS COMPTER SUR L'AUTO-RETOURNEMENT DE ZONE.
    `DeckType.RisingTideArea` porte bien `is_face_up = True`, et
    `Card.CheckIfCanMove` sait retourner automatiquement une carte qui entre
    dans une zone ainsi marquee -- MAIS seulement sur le chemin
    `Card.MoveToArea` direct, et seulement si `ui_group=False` (card.py,
    ~L405). Le second appelant de ce fichier (le crochet de defausse
    redirigee de Wave, `65001a.py`) route sa carte via `Message.
    WhenCardWouldDiscard.SetToArea`, un chemin qui passe par
    `MoveToAreaInternal` DIRECTEMENT et saute cette verification. Retourner
    la carte nous-memes, apres coup, marche sur les deux chemins et ne
    depend d'aucun detail d'implementation du deplacement.
    """
    proprietaire = face.GetOwner()
    if not isinstance(proprietaire, Player):
        return False
    if not face.card.MoveToArea(proprietaire.rising_tide, effect):
        return False
    if not face.card.IsFaceUp():
        face.card.Flip(effect)
    return True


def CartesDansRisingTide(joueur: 'Player', *, face_visible: bool) -> List['CardFace']:
    """Les cartes ACTUELLEMENT dans la Rising Tide area de ce joueur, filtrees
    par etat (face visible ou face cachee). PAS de `is_visible` ici : le
    proprietaire choisit parmi SES PROPRES cartes, qu'il les voie ou non --
    c'est lui qui les y a placees, et l'insert ne restreint que les effets
    D'AUTRUI (« cannot be affected by effects that do not explicitly target
    the Rising Tide area »), jamais le choix du proprietaire sur sa propre
    zone.
    """
    return [c for c in joueur.rising_tide.GetAll(False)
            if c.IsFaceUp() == face_visible]


def RetournerCartesRisingTide(effect: 'Effect', joueur: 'Player', *,
                              face_visible: bool, minimum: int, maximum: int,
                              prompt: str) -> List['CardFace']:
    """« Flip up to N cards in your Rising Tide area face(up|down) ». Rend les
    cartes EFFECTIVEMENT retournees (jamais plus que ce qui existait).

    ⚠ `AskChooseFaces` PLUTOT QU'UN `SetTarget` DECLARATIF : aucune zone
    « Rising Tide » n'existe dans `SELECT.WHERE` (game/selector/
    selector_where.py) -- ni pour la Reserve du pack `brawn`, qui procede de
    la meme facon (voir `AskChooseFace` employe par ses propres scripts). Une
    liste de candidats DEJA CONNUE (celle-ci) n'a pas besoin d'un chercheur
    generique.
    """
    candidates = CartesDansRisingTide(joueur, face_visible=face_visible)
    if not candidates:
        return []
    choisies = joueur.AskChooseFaces(
        candidates, (minimum, maximum), effect, prompt=prompt, forced=False,
    )
    for face in choisies:
        face.card.Flip(effect)
    return choisies


def RetournerUneCarteRisingTide(effect: 'Effect', joueur: 'Player', *,
                                face_visible: bool, prompt: str,
                                forced: bool = True) -> 'CardFace|None':
    """« Flip a faceup/facedown card in your Rising Tide area » (UNE carte,
    pas « jusqu'a »). `forced=False` pour un cout qui peut echouer faute de
    carte au bon etat (Pearl's Lolo, Wave's Swords : payer suppose une carte
    disponible, sans quoi le cout n'est pas payable).
    """
    candidates = CartesDansRisingTide(joueur, face_visible=face_visible)
    if not candidates:
        return None
    choisie = joueur.AskChooseFace(candidates, effect, prompt=prompt, forced=forced)
    if choisie:
        choisie.card.Flip(effect)
    return choisie


def CoutRetournerUneCarteRisingTide(*, face_visible: bool, prompt: str) -> 'CostFunc.Base':
    """Cout combinable (`.SetCostFunc`) : « flip a faceup card in your Rising
    Tide area » comme UN DES couts d'une capacite (Pearl's Lolo, Wave's
    Swords). Chainable avec un autre `.SetCostFunc(...)` sur la meme
    capacite -- `Ability.SetCostFunc` EMPILE (`cost_funcs.append`, voir
    `game/ability/ability.py`), il ne remplace pas ; c'est ainsi que
    `luke_cage/62018.py` combine `CostFunc.Exhaust("This")` avec un second
    cout sur la meme capacite.

    ⚠ LA VERIFICATION DE PAYABILITE (`check_effect_fn` sur un `Select.
    From("This", finder=...)`) EST SEPAREE DE L'EXECUTION (`call_fn`) : sans
    elle, une capacite serait proposee au joueur puis echouerait a l'usage
    faute de carte au bon etat dans la Rising Tide area -- la meme lecon que
    `CostFunc.LookAtDeck` (`has_enought_size`, cost_func.py) et que la garde
    de `PileNonVide` du pack `black_cat` (RECETTES §5 : une capacite jouable
    sans cout payable defausse la carte pour rien).
    """
    def payable(effect: 'Effect', face: 'CardFace') -> bool:
        Unused(face)
        joueur = effect.GetInitiator()
        if not isinstance(joueur, Player):
            return False
        return bool(CartesDansRisingTide(joueur, face_visible=face_visible))

    def payer(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)
        joueur = effect.GetInitiator()
        if not isinstance(joueur, Player):
            return False
        choisie = RetournerUneCarteRisingTide(
            effect, joueur, face_visible=face_visible, prompt=prompt, forced=True,
        )
        return choisie is not None

    selecteur = Select.From("This", finder=CardFinder(check_effect_fn=payable))
    return CostFunc.Custom(selecteur, payer)
