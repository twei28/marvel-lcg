from cards.pack import *

# ===========================================================================
# Helpers partages du set « Spider-Man Noir » (Rainy, set 160, prefixe `sn`).
#
# ⚠ TOUT LE PACK REPOSE SUR UNE SEULE ZONE : les cartes GLISSEES SOUS
# L'IDENTITE. Le heros a **ATQ 0 et CTR 0 imprimes** et gagne +X aux deux, X
# etant le nombre de cartes glissees (plafond 3). Sans cette pile il ne fait
# donc RIEN. Onze des seize cartes la lisent ou l'alimentent :
#   - sn001a la COMPTE (+X ATQ/CTR) et la REMPLIT (apres une traitrise) ;
#   - sn001b la remplit depuis le deck de rencontre, ou echange contre du contre ;
#   - sn002 y glisse le sbire qu'elle vainc ;
#   - sn003 y glisse la carte defaussee ;
#   - sn004 y detourne une carte de boost ;
#   - sn005 en defausse une pour redresser, puis en reglisse une ;
#   - sn006, sn007, sn009, sn010 en DEFAUSSENT une comme cout ;
#   - sn011 en revele une au hasard ;
#   - sn013 en donne une au sbire comme carte de boost ;
#   - sn014 compte les icones de boost de la pile pour infliger des degats.
#
# ⚠ LA ZONE EST PORTEE PAR LA CARTE, PAS PAR LA FACE.
# `CardFace.GetPlacedCardArea()` rend `self.card.components.placed_card`
# (card_face.py:1017) : **les deux faces partagent la meme pile**. C'est ce que
# le texte imprime suppose sans le dire — il ecrit tantot « under him »
# (sn001a), tantot « here » (sn001b), tantot « under your hero » (sn003,
# sn007, sn009), tantot « under your identity » (sn006, sn011, sn013, sn014).
# Quatre formulations, UNE seule zone. Verifie dans le moteur, pas suppose.
#
# ⚠ HOMONYME MAJEUR : « Spider-Man Noir » est DEJA le nom de deux ALLIES du
# depot — `31015` (pack spdr) et `wd118` (pack web_of_deceit). Un
# `CardFinder(name="Spider-Man Noir")` les attraperait. Toutes les cartes qui
# nomment le heros passent donc par le TYPE ou par le litteral `"YourHero"`,
# JAMAIS par le nom. Meme discipline que `beta_ray_bill`, pour la raison
# inverse (la-bas les deux faces portaient le meme nom).
#
# ⚠ ET « Peter Parker » EST DEJA PRIS QUATRE FOIS : `01001b` (Spider-Man
# officiel), `sr001b` (spider_man_rainy), `as001b` (armored_spidey) et
# `bt014` (un ALLIE du pack beast). L'obligation `sn011` ecrit malgre tout
# `desc.GiveTo = "Peter Parker"`, comme le texte imprime et comme les TROIS
# obligations deja livrees qui font pareil (`01165`, `sr013`, `as014`).
# `Worlds.FindPlayerByName` rend le PREMIER joueur qui repond a ce nom : en
# solo c'est toujours le bon, a plusieurs avec deux Peter Parker a la table
# l'ambiguite existe — elle est ANTERIEURE et partagee par les quatre cartes.
# ===========================================================================

NOM_HEROS = "Spider-Man Noir"
NOM_ALTER_EGO = "Peter Parker"
SET_HEROS: 'CardFace.SETNAMES' = "Spider-Man Noir"
NOM_PISTOLETS = "Dual Pistols"

# « to a maximum of 3 » — le plafond est imprime sur SEPT cartes du set. Une
# constante, pour qu'une relecture du zip n'ait qu'un endroit a corriger.
PLAFOND_PILE = 3


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit.

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception — la carte ne fait alors rien, et aucun outil ne le voit
    (leçon `Player.GetHero()`, pack lady_sif).

    ⚠ Passer le joueur EXPLICITEMENT quand la carte qui agit ne lui appartient
    pas : c'est le cas de l'obligation sn011 et de tout le set nemesis, cartes
    de RENCONTRE (leçon yd013 / dr010 / tt020 / br012 / tg011).
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
    """L'identite en jeu, QUELLE QUE SOIT SA FACE.

    C'est elle qui porte la pile : `GetPlacedCardArea()` lit
    `self.card.components`, donc la face courante suffit pour atteindre la
    pile des deux faces.
    """
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    return joueur.GetIdentity()


def HerosDuJoueur(effect: 'Effect', joueur: 'Player|None' = None) -> 'CardFace|None':
    """La face HEROS (« Spider-Man Noir »), ou None si le joueur est en civil.

    ⚠ LE FILTRE EST LE TYPE, JAMAIS LE NOM : deux ALLIES du depot s'appellent
    « Spider-Man Noir » (`31015`, `wd118`).
    """
    identite = IdentiteDuJoueur(effect, joueur)
    if identite is None or not Hero.IsType(identite):
        return None
    return identite


def CartesGlissees(effect: 'Effect', joueur: 'Player|None' = None) -> List['CardFace']:
    """Les cartes de la pile, dans l'ordre ou elles y sont.

    Modele `GetTuckedCards` du pack wonder_man (58001a/58002), a ceci pres que
    la pile n'est pas sur un soutien mais sur l'identite elle-meme.
    """
    identite = IdentiteDuJoueur(effect, joueur)
    if identite is None:
        return []
    return list(identite.GetPlacedCardArea().Get())


def PlaceRestanteDansLaPile(effect: 'Effect', joueur: 'Player|None' = None) -> int:
    """Combien de cartes on peut encore glisser avant le plafond de 3.

    ⚠ Le plafond est imprime sur CHAQUE carte qui glisse, jamais sous-entendu :
    on le verifie donc a chaque fois, meme quand l'appelant croit savoir.
    """
    return max(0, PLAFOND_PILE - len(CartesGlissees(effect, joueur)))


def GlisserSousIdentite(effect: 'Effect', faces: Sequence['CardFace'],
                        joueur: 'Player|None' = None) -> List['CardFace']:
    """Glisse des cartes sous l'identite, dans la limite du plafond.

    Rend la liste REELLEMENT glissee — c'est elle qu'on mesure dans les cas,
    jamais celle qu'on esperait glisser.
    """
    identite = IdentiteDuJoueur(effect, joueur)
    if identite is None:
        return []
    place = PlaceRestanteDansLaPile(effect, joueur)
    glissees: List['CardFace'] = []
    for face in faces:
        if place <= 0:
            break
        if face is None:
            continue
        if identite.TuckCardUnderHere(face, effect):
            glissees.append(face)
            place -= 1
    return glissees


def PileNonVide(effect: 'Effect', message: 'Message') -> bool:
    """Condition : « discard a card tucked under ... » est PAYABLE.

    ⚠ SANS ELLE, LE JOUEUR PERD SA CARTE POUR RIEN. Constate le 05/09/2026 sur
    le contre-cas de `sn005` : pile vide, l'evenement etait quand meme propose,
    joue et DEFAUSSE, `CostFunc.Custom` rendait `False`, l'effet ne tombait pas
    — et la carte etait perdue. Le moteur n'annule pas la mise en jeu sur un
    cout impaye : `CostFunc.Base.HasTargets` (cost_func.py:47) rend True des
    que le selecteur a une cible, or `CostFunc.Custom(None, ...)` se rabat sur
    `Select.From("This")`, c'est-a-dire la carte elle-meme, toujours presente.

    La regle imprimee, elle, interdit de payer un cout qu'on ne peut pas payer.
    On conditionne donc l'OFFRE de la capacite, exactement comme `58008` Ionic
    Belt du pack wonder_man, seule carte du depot a payer sur une pile glissee
    (`conditions=[check_mode]`, qui teste `len(GetTuckedCards(...)) > 0`).

    Portee : les CINQ capacites du set dont le cout est « discard a card tucked »
    (`sn005`, `sn006`, `sn007`, `sn009` Action, `sn010`).
    """
    Unused(message)
    return len(CartesGlissees(effect)) > 0


def DefausserUneCarteGlissee(effect: 'Effect', joueur: 'Player|None' = None) -> bool:
    """« discard a card tucked under ... » — le COUT de quatre cartes du set.

    Le joueur CHOISIT laquelle : les cartes glissees ne sont pas
    interchangeables, `sn014` comptant leurs icones de boost.
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


def IconesDeBoost(faces: Sequence['CardFace']) -> int:
    """Le total des icones de boost CHIFFREES portees par des cartes.

    Sert a `sn001b` et `sn003`, qui disent « the number of BOOST icons
    discarded » : l'etoile n'y compte pas. Modele `15004` / `ho014`.

    ⚠ NE PAS S'EN SERVIR POUR `sn014`, qui dit « each icon ([star] AND
    [boost]) » : `CountTotalBoostIcons` ne somme que
    `CountBoostIconsInternal` (faces_counter.py:142), l'etoile vit dans
    `boost_star` (has_boost_icon.py:52), et seule
    `CountTotalBoostStarAndBoost` additionne les deux. Piege releve le
    05/09/2026, apres avoir ecrit sn014 de travers.
    """
    if not faces:
        return 0
    return FacesCounter.CountTotalBoostIcons(list(faces))
