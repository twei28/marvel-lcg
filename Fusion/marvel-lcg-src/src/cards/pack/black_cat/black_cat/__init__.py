from cards.pack import *

# ===========================================================================
# Helpers partages du set « Black Cat » (Rainy, set 161, prefixe `bc`).
#
# ⚠ TOUT LE PACK REPOSE SUR DEUX CHOSES A LA FOIS :
#   1. la PILE glissee sous l'identite, plafonnee a 3 ;
#   2. les ICONES DE BONUS des cartes de rencontre, lues partout comme une
#      monnaie : degats (bc006, bc008), menace retiree (bc005), prevention
#      (bc011), malus a l'ennemi (bc007), et substitution pure (bc001a).
#
# ⚠ LE PLAFOND N'EST PAS UN PLAFOND DE POSE. Les deux faces impriment :
#   « If there are more than 3 tucked cards here, discard all but 3 of those
#   cards. »
# Ce n'est PAS « to a maximum of 3 » comme chez `spider_man_noir` : ici on
# PEUT depasser 3, et c'est une regle continue qui ramene la pile a 3 APRES
# coup, en defaussant. La difference est observable : une carte qui glisse
# alors que la pile est pleine ENTRE quand meme, et c'est une AUTRE carte qui
# peut partir (le joueur choisit). Ne pas recopier `GlisserSousIdentite` du
# pack Noir, qui refuse la pose.
#
# ⚠ LA ZONE EST PORTEE PAR LA CARTE, PAS PAR LA FACE.
# `CardFace.GetPlacedCardArea()` rend `self.card.components.placed_card`
# (card_face.py:1017) : les deux faces partagent la meme pile. C'est ce que le
# texte imprime suppose en ecrivant tantot « here » (bc001a, bc001b), tantot
# « under Black Cat » (bc005, bc006, bc008, bc009), tantot « under your hero »
# (bc007), tantot « under your identity » (bc010, bc012). QUATRE formulations,
# UNE seule zone.
#
# ⚠ HOMONYMES MAJEURS — AUCUNE CARTE DU PACK NE CHERCHE PAR LE NOM.
#  - « * Black Cat » est DEJA `01002` (alliee du set Spider-Man), `wd045`
#    (SBIRE du set Electro) et `vp002` (alliee de Venompool). Trois cartes.
#  - « * Spider-Man » existe QUINZE fois au depot (`01001a` en tete). Les deux
#    allies du pack, `bc002` et `bc003`, sont les seizieme et dix-septieme.
#  - « Grappling Hook » est deja `08008` (amelioration Black Widow) et `50069`
#    (attachement Black Widow). `bc009` est la troisieme.
# Toutes les cartes qui nomment l'heroine passent donc par le TYPE ou par le
# litteral `"YourHero"` / `"YourIdentity"`, JAMAIS par `CardFinder(name=...)`.
# Meme discipline que `spider_man_noir`, et pour la meme raison.
#
# ⚠ « MULTIVERSE » (bc003) N'EST PAS UN TRAIT ICI, c'est le mot-cle maison :
# fiche `docs/reference/mots-cles/multiverse.md`, creee pour ce pack.
# ZERO ligne de code — c'est l'unicite native qui fait le travail. A ne pas
# confondre avec le TRAIT `MULTIVERSE` de `wd029`.
#
# ⚠ COMPTER LES ICONES : « ([star] and [boost]) » EST IMPRIME SUR CINQ CARTES.
# `FacesCounter.CountTotalBoostIcons` ne somme QUE les icones chiffrees
# (faces_counter.py:142) ; l'etoile vit dans `boost_star`
# (has_boost_icon.py:52). Seule `CountTotalBoostStarAndBoost`
# (faces_counter.py:160) additionne les deux. Piege paye la veille sur
# `sn014`. Le helper `IconesEtEtoiles` ci-dessous est le seul point d'entree.
# ⚠ SEULE `bc008` Black Cat's Claws dit « the number of icons » SANS preciser
# « [star] and [boost] » : elle emploie donc `IconesSeules`. Deux comptes
# differents dans le meme set, et c'est imprime.
# ===========================================================================

NOM_HEROS = "Black Cat"
NOM_ALTER_EGO = "Felicia Hardy"
SET_HEROS: 'CardFace.SETNAMES' = "Black Cat"

# « discard all but 3 of those cards » — le nombre est imprime sur les DEUX
# faces. Une constante, pour qu'une relecture du zip n'ait qu'un endroit a
# corriger.
TAILLE_MAX_PILE = 3


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit.

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception — la carte ne fait alors rien, et aucun outil ne le voit
    (lecon `Player.GetHero()`, pack lady_sif).
    """
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def IdentiteDuJoueur(effect: 'Effect', joueur: 'Player|None' = None) -> 'CardFace|None':
    """L'identite en jeu, QUELLE QUE SOIT SA FACE : c'est elle qui porte la pile."""
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    return joueur.GetIdentity()


def HerosDuJoueur(effect: 'Effect', joueur: 'Player|None' = None) -> 'CardFace|None':
    """La face HEROS (« Black Cat »), ou None si le joueur est en civil.

    ⚠ LE FILTRE EST LE TYPE, JAMAIS LE NOM : trois cartes du depot s'appellent
    deja « * Black Cat » (`01002`, `wd045`, `vp002`).
    """
    identite = IdentiteDuJoueur(effect, joueur)
    if identite is None or not Hero.IsType(identite):
        return None
    return identite


def CartesGlissees(effect: 'Effect', joueur: 'Player|None' = None) -> List['CardFace']:
    """Les cartes de la pile, dans l'ordre ou elles y sont."""
    identite = IdentiteDuJoueur(effect, joueur)
    if identite is None:
        return []
    return list(identite.GetPlacedCardArea().Get(True))


def GlisserSousIdentite(effect: 'Effect', faces: Sequence['CardFace'],
                        joueur: 'Player|None' = None) -> List['CardFace']:
    """Glisse des cartes sous l'identite, SANS PLAFOND A LA POSE.

    ⚠ DIFFERENCE DE FOND AVEC LE PACK `spider_man_noir` : la-bas le plafond
    « (to a maximum of 3) » est imprime SUR CHAQUE CARTE QUI GLISSE et REFUSE
    la pose. Ici aucune carte du set ne porte ce plafond : ce sont les DEUX
    FACES de l'identite qui portent une regle continue, « if there are more
    than 3 tucked cards here, discard all but 3 ». La carte entre donc
    TOUJOURS, et le menage vient apres (`RegleDesTroisCartes`).

    Rend la liste REELLEMENT glissee — c'est elle qu'on mesure dans les cas,
    jamais celle qu'on esperait glisser.
    """
    identite = IdentiteDuJoueur(effect, joueur)
    if identite is None:
        return []
    glissees: List['CardFace'] = []
    for face in faces:
        if face is None:
            continue
        if identite.TuckCardUnderHere(face, effect):
            glissees.append(face)
    return glissees


def DefausserUneCarteGlissee(effect: 'Effect', joueur: 'Player|None' = None) -> bool:
    """« discard a card tucked under ... » — le COUT de `bc003` et `bc009`.

    Le joueur CHOISIT laquelle : les cartes glissees ne sont pas
    interchangeables, `bc001a` comptant leurs icones.
    """
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return False
    pile = CartesGlissees(effect, joueur)
    if not pile:
        return False
    choisie = joueur.AskChooseFaces(pile, (1, 1), effect,
                                    prompt="Discard a card tucked under your identity")
    if not choisie:
        return False
    Faces.DiscardAll(list(choisie), effect)
    return True


def PileNonVide(effect: 'Effect', message: 'Message') -> bool:
    """Condition : « discard a card tucked under ... » est PAYABLE.

    ⚠ SANS ELLE, LE JOUEUR PERD SA CARTE POUR RIEN. `CostFunc.Base.HasTargets`
    (cost_func.py:47) rend True des que le selecteur a une cible, or
    `CostFunc.Custom(None, ...)` se rabat sur `Select.From("This")` : la carte
    elle-meme, toujours presente. Le `False` du paiement arrive trop tard, la
    carte est jouee ET defaussee sans effet. Constate le 05/09/2026 sur
    `sn005` (pack spider_man_noir) et consigne dans RECETTES §5.
    """
    Unused(message)
    return len(CartesGlissees(effect)) > 0


def IconesEtEtoiles(faces: Sequence['CardFace']) -> int:
    """« each icon ([star] and [boost]) » — LES DEUX SORTES.

    ⚠ `CountTotalBoostIcons` ne rendrait que les icones CHIFFREES
    (faces_counter.py:142) ; l'etoile vit dans `boost_star`
    (has_boost_icon.py:52). Seule `CountTotalBoostStarAndBoost` additionne les
    deux. Employe par `bc001a`, `bc005`, `bc006`, `bc007` et `bc011`, qui
    impriment tous « ([star] and [boost]) ».
    """
    if not faces:
        return 0
    return FacesCounter.CountTotalBoostStarAndBoost(list(faces))


def IconesSeules(faces: Sequence['CardFace']) -> int:
    """« the number of icons in that card's boost area » — SANS l'etoile.

    ⚠ Reserve a `bc008` Black Cat's Claws, LA SEULE carte du set qui n'ecrit
    PAS « ([star] and [boost]) ». On code ce qui est imprime : la difference
    se voit sur une carte a etoile seule, qui vaut 0 degat ici et 1 ailleurs —
    et c'est justement la branche « If that number was 0, tuck it » qui rend
    l'ecart visible en jeu.
    """
    if not faces:
        return 0
    return FacesCounter.CountTotalBoostIcons(list(faces))


def RegleDesTroisCartes() -> 'Ability':
    """« If there are more than 3 tucked cards here, discard all but 3. »

    Regle CONTINUE, imprimee a l'identique sur les DEUX faces de l'identite.
    Elle n'empeche pas la pose : elle nettoie apres.

    Fenetre : `Message.AfterCardsMoved`, le seul message que le moteur envoie
    quand une carte entre dans une zone — c'est celui qu'ecoute
    `OnEvent.TuckUnder` / `OnEvent.PlacedCard` (on_event.py:410-423), et donc
    la garantie qu'on regarde au bon moment.

    ⚠ Le joueur CHOISIT lesquelles il garde : les cartes glissees ne sont pas
    interchangeables, toutes les cartes du set comptant leurs icones. « Discard
    all but 3 » ne dit pas « les plus anciennes ».
    """

    def la_pile_deborde(effect: 'Effect', message: 'Message.AfterCardsMoved') -> bool:
        return (effect.this.GetPlacedCardArea() in message.related_decks
                and effect.this.GetPlacedCardArea().GetSize() > TAILLE_MAX_PILE)

    def faire_le_menage(effect: 'Effect', message: 'Message.AfterCardsMoved') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        pile = list(effect.this.GetPlacedCardArea().Get(True))
        trop = len(pile) - TAILLE_MAX_PILE
        if trop <= 0:
            return
        if joueur is None:
            Faces.DiscardAll(pile[:trop], effect)
            return
        gardees = joueur.AskChooseFaces(
            pile, (TAILLE_MAX_PILE, TAILLE_MAX_PILE), effect,
            prompt="Keep 3 tucked cards, discard the rest")
        a_defausser = [f for f in pile if f not in (gardees or [])]
        if a_defausser:
            Faces.DiscardAll(a_defausser, effect)

    return AbilityFactory.AfterCardsMoved(
        AbilityType.ForcedResponse,
        None,
        faire_le_menage,
        conditions=[la_pile_deborde],
    )
