from cards.pack import *

# ===========================================================================
# LES COMPTEURS `psionic web` — helpers partages du pack SPIDER-WOMAN
# (Kajislav, set 169, prefixe `sw`).
#
# Julia Carpenter en pose 5 au montage, 3 par Action, jusqu'a un plafond de 10.
# Spider-Woman les depense pour annuler des icones de boost, contrer, frapper.
# DOUZE des 29 cartes du pack les lisent, les posent ou les depensent : c'est
# le pack entier qui tourne autour de ce seul stock.
#
# ⚠⚠ LE STOCK VIT SUR L'IDENTITE, PAS SUR UNE CARTE. Les textes disent tantot
# « on your identity », tantot « on Spider-Woman », tantot « on Julia
# Carpenter » — c'est le MEME stock, et il doit survivre au changement de
# forme. On passe donc toujours par `IdentiteDe(...)`, jamais par la face
# courante.
#
# ⚠ LE COMPTEUR S'APPELLE `psionic web`, PAS `psionic`. Le moteur connaissait
# deja `psionic` (card_face.py:164), et il est PRIS : `mw002` (pack
# madame_web) et `35013` (Wolverine) s'en servent. Or Madame Web est justement
# une ALLIEE de ce pack-ci — les deux stocks peuvent se retrouver sur la meme
# table. D'ou une entree a part, ajoutee le 10/09/2026, au nom imprime.
# ===========================================================================

COMPTEUR = 'psionic web'
PLAFOND = 10


def EstSpecifiqueALIdentite(face: 'CardFace') -> bool:
    """« an identity-specific card » : une carte du set d'un heros.

    Deux cartes du set nemesis A la lisent — `sw021` Man-Bull en fait
    defausser une, `sw024` Violent Disturbance les fait TOUTES defausser — et
    c'est la ou le pack fait le plus mal : tout le moteur de Spider-Woman
    (les compteurs) vit dans son set heros.

    ⚠ Le moteur classe deja les cartes : `IsClass("IdentitySpecific")`
    (card_player.py:177). On ne relit pas `desc.Class` a la main, la table de
    correspondance etant a lui.
    """
    if face is None or not ClassCard.IsType(face):
        return False
    return face.CastTo(ClassCard).IsClass("IdentitySpecific")


def JoueurQuiControleCetteCarte(effect: 'Effect') -> "Player|None":
    """Le joueur qui controle la carte porteuse, ou None si ce n'en est pas un.

    ⚠ `CardFace.GetControlByPlayer()` AFFIRME que le controleur est un joueur
    (`assert isinstance(owner, Player)`, card_face.py:972) et TOMBE sinon. Une
    carte de ce pack peut se retrouver controlee par le scenario — `sw023` Bad
    Inspiration transforme un allie en SBIRE — et un bonus continu qui se
    recalcule a ce moment-la ferait exploser la partie. Lecon payee le
    10/09/2026 sur le pack iron_patriot, 32 fois sur 16 parties d'autoplay.
    """
    proprietaire = effect.this.GetControlBy()
    return proprietaire if Player.IsType(proprietaire) else None


def IdentiteDe(joueur: 'Player') -> "CardFace|None":
    """L'identite du joueur, quelle que soit sa forme.

    Toutes les cartes du pack passent par ici : « on your identity », « on
    Spider-Woman » et « on Julia Carpenter » designent la MEME carte, et le
    stock ne doit pas se perdre au changement de forme.
    """
    if joueur is None:
        return None
    return joueur.GetIdentity()


def ToilesDe(joueur: 'Player') -> int:
    """Combien de compteurs `psionic web` porte l'identite de ce joueur."""
    identite = IdentiteDe(joueur)
    if identite is None:
        return 0
    return identite.CastTo(CanPlaceCounter).GetCounters(COMPTEUR)


def PoserDesToiles(joueur: 'Player', nombre: int, effect: 'Effect') -> int:
    """« place N psionic web counters ... (to a maximum of 10) ».

    ⚠ LE PLAFOND EST IMPRIME SUR SEPT CARTES, TOUJOURS LE MEME : 10. On ne le
    recalcule PAS a la main : `Faces.PlaceCountersOn` prend un `maximum`
    (faces.py:206) et s'en charge. Le compter soi-meme, c'est se tromper une
    fois sur sept.
    """
    identite = IdentiteDe(joueur)
    if identite is None or nombre <= 0:
        return 0
    return Faces.PlaceCountersOn([identite], nombre, COMPTEUR, effect,
                                 maximum=PLAFOND) or 0


def RetirerDesToiles(joueur: 'Player', nombre: int, effect: 'Effect') -> int:
    """Retire jusqu'a `nombre` compteurs, et dit combien sont VRAIMENT partis.

    ⚠ C'est la valeur RENDUE qui compte, jamais celle demandee : `sw006`
    Psi-Web Trap et `sw007` Psionic Web Blast retirent « X » et agissent sur
    X. Demander plus que le stock ne cree pas de menace retiree en trop.
    """
    identite = IdentiteDe(joueur)
    if identite is None or nombre <= 0:
        return 0
    retire = min(nombre, ToilesDe(joueur))
    if retire <= 0:
        return 0
    return Faces.RemoveCountersOn([identite], retire, COMPTEUR, effect) or 0


def DemanderCombienDeToiles(joueur: 'Player', effect: 'Effect') -> int:
    """« Remove X psionic web counters » : X est un CHOIX du joueur.

    ⚠ Le moteur n'a pas de « demande un nombre ». Il a `AskChooseOneText`, qui
    prend une liste d'items quelconques et rend celui qu'on a choisi
    (player_ask.py:56) : une liste d'entiers en fait exactement une saisie de
    nombre, et le moteur affiche leur `str()`.
    ⚠ On borne au STOCK REEL : proposer 5 quand il en reste 2 offrirait un
    choix qui ment. `sw006` et `sw007` agissent ensuite sur ce que
    `RetirerDesToiles` a VRAIMENT retire, jamais sur le nombre demande.
    """
    stock = ToilesDe(joueur)
    if stock <= 0:
        return 0
    return joueur.AskChooseOneText(list(range(stock, -1, -1)))


def ToilesParRessourceMentale(effect: 'Effect', par_ressource: int) -> int:
    """« place N psionic web counters ... for each [mental] resource you used
    to pay for this card ».

    Quatre cartes du pack l'impriment (`sw005`, `sw008`, `sw009`, `sw010`).
    C'est la brique « provenance du paiement », deja rodee sur Brawn (bw008),
    Ant-Man (12031), Mojo (39037) et Nebula (22011) :
    `effect.GetPaidResources()` (effect.py:501) rend les ressources REELLEMENT
    depensees pour CETTE carte, et `GetColor("B")` compte les mentales.

    ⚠ PREMIERE ECRITURE FAUSSE, corrigee le 10/09/2026 : on lisait
    `effect.cost_func.Get(CostFunc.Spend).return_res`. Cet objet existe, la
    ligne ne levait rien, et le compte rendu valait TOUJOURS zero — quatre
    cartes posaient donc zero compteur en silence. Vu seulement par le harnais
    (`sw005` : 5 compteurs au lieu de 7).

    ⚠ Une ressource [wild] compte comme la ressource qu'elle a payee : c'est
    le defaut de `GetColor` (`convert_green_res=True`), et le choix de bw008.
    """
    return effect.GetPaidResources().GetColor("B") * par_ressource
