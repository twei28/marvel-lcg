from cards.pack import *

# ===========================================================================
# Helpers partages du set « Spider-Man 2099 » (Rainy, set 166, prefixe `sm`).
#
# ⚠⚠ TOUT LE PACK TOURNE AUTOUR D'UNE SEULE CAPACITE, ET ELLE PORTE UN NOM
# DEJA PRIS. « Acceleration » est ici une CAPACITE D'IDENTITE, sans aucun
# rapport avec l'ICONE officielle du meme nom (`desc.Acceleration`,
# `HasAccelerationIcon`). Fiche dediee :
# `docs/reference/mots-cles/acceleration-2099.md`. Le pack n'emploie
# `desc.Acceleration` qu'a UN endroit, et c'est bien l'icone : sur
# l'obligation `sm013` Future in Crisis, verifie par comparaison d'image
# contre `ag011` le 08/09/2026.
#
# ARCHITECTURE, ET POURQUOI ELLE EST CELLE-LA
#
# Six cartes du pack relisent « ai-je joue cette carte VIA Acceleration ? » ou
# « viens-je de RESOUDRE Acceleration ? ». Le moteur a deja les deux briques,
# et le modele complet est `ab001a` * Albert (pack albert, capacite
# « Initiate Protocol ») :
#
#  1. La capacite elle-meme est une ability `AbilityType.Special` posee sur la
#     face heros, `WhenResolveSpecialAbility("This", ...).SetName(NOM_ACCEL)`.
#     Le declencheur imprime (« After your hero uses a basic power ») est une
#     Response SEPAREE qui appelle `ResolveSpecialAbility(name=NOM_ACCEL)`.
#  2. « After you resolve your hero's Acceleration ability » (sm010, sm011,
#     sm012) est un SECOND envoi, sous un autre nom (`NOM_ACCEL_FINI`), fait
#     par sm001a une fois son operation terminee. `check_ability_name`
#     (`factory/resolve.py:17`) fait le tri : une ability ne repond qu'au nom
#     qu'elle porte.
#     ⚠ Il FAUT deux noms. Un seul envoi ferait partir sm010/11/12 « pendant »
#     la resolution, pas apres, et l'ordre entre effets d'un meme message
#     n'est pas garanti — or Hyper-Agility (sm010) doit savoir si un evenement
#     a ete joue, ce qui n'est vrai qu'a la FIN.
#
# LE MARQUEUR « joue via Acceleration » n'a, lui, aucune brique moteur : rien
# ne dit d'une carte par quelle capacite elle a ete jouee. Le pack le pose
# donc lui-meme, sur le JOUEUR, autour de l'appel a `PlayCardsLikeInTurn`, et
# `JoueViaAcceleration(effect, face)` le relit. C'est le seul etat maison du
# pack, il est remis a zero a chaque resolution, et il ne survit jamais a une
# operation.
#
# ⚠ HOMONYMES. La face heros s'appelle « * Spider-Man », comme `01001a`
# (Peter Parker), `sr001a` (spider_man_rainy) et la face heros du pack
# superior_spider_man. « * Ghost Rider » (sm002) existe aussi en identite
# officielle (`24001a`, `47001a`) et en allie (`21029`). CONSEQUENCE : AUCUNE
# carte de ce pack ne cherche une carte par son NOM. L'identite se retrouve
# par `card_ids`, les cartes du pack par leur `set_name`.
# ===========================================================================

SET_HEROS: 'CardFace.SETNAMES' = "Spider-Man 2099"
ID_HEROS = "sm001a"
ID_ALTER_EGO = "sm001b"

NOM_ACCEL = "Acceleration"
NOM_ACCEL_DEBUT = "Acceleration Starting"
NOM_ACCEL_FINI = "Acceleration Resolved"

TRAIT_ATTACK: 'CardFace.TRAITS' = "ATTACK"
TRAIT_AERIAL: 'CardFace.TRAITS' = "AERIAL"
COMPTEUR_TOILE: 'CardFace.COUNTER' = 'web'

# Attributs poses sur l'objet `Player` pendant une resolution d'Acceleration.
_EN_COURS = "_sm2099_acceleration_en_cours"
_EVENT_JOUE = "_sm2099_acceleration_event_joue"
_DEFAUSSEES = "_sm2099_acceleration_defaussees"
_CONTINUER = "_sm2099_acceleration_continuer"


def EstJoueur(objet: Any) -> bool:
    """`Player.IsType` SANS le risque d'AttributeError (lecon sf002 / sf013)."""
    return objet is not None and hasattr(objet, "IsPlayer") and Player.IsType(objet)


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit.

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception (lecon `Player.GetHero()`, pack lady_sif). Meme helper que
    ares, blade, sunfire, black_cat, throg.
    """
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if EstJoueur(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if EstJoueur(initiateur):
        return initiateur
    return None


def IdentiteDuJoueur(effect: 'Effect', joueur: 'Player|None' = None) -> 'CardFace|None':
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    return joueur.GetIdentity()


def HerosDuJoueur(effect: 'Effect', joueur: 'Player|None' = None) -> 'CardFace|None':
    """La face HEROS du pack, ou None si le joueur est en civil.

    ⚠ LE FILTRE EST LE TYPE, JAMAIS LE NOM : « Spider-Man » designe quatre
    cartes differentes au depot.
    """
    identite = IdentiteDuJoueur(effect, joueur)
    if identite is None or not Hero.IsType(identite):
        return None
    return identite


def Hote(face: 'CardFace|None') -> 'CardFace|None':
    """A QUI cette carte est-elle accrochee ? `None` si elle ne l'est pas."""
    return getattr(face, "bind_face", None) if face is not None else None


################################################################################
# Le marqueur « via Acceleration »
################################################################################

def OuvrirAcceleration(joueur: 'Player') -> None:
    """Ouvre une resolution d'Acceleration : le marqueur est neuf a chaque
    fois, jamais cumule avec la resolution precedente."""
    setattr(joueur, _EN_COURS, True)
    setattr(joueur, _EVENT_JOUE, None)
    setattr(joueur, _DEFAUSSEES, [])
    setattr(joueur, _CONTINUER, False)


def AutoriserContinuation(joueur: 'Player') -> None:
    """Pose par le MODULE de `sm008` Accelerated Vision, en reponse au message
    `NOM_ACCEL_DEBUT`. C'est ce qui rend la substitution de sm008 mordante :
    sans son module, le drapeau n'est jamais pose et la continuation ne peut
    pas avoir lieu."""
    setattr(joueur, _CONTINUER, True)


def ContinuationAutorisee(joueur: 'Player|None') -> bool:
    return bool(joueur is not None and getattr(joueur, _CONTINUER, False))


def FermerAcceleration(joueur: 'Player') -> None:
    """Ferme la resolution. ⚠ `_EVENT_JOUE` SURVIT a la fermeture : les
    evenements sm003-sm006 lisent le marqueur pendant LEUR propre resolution,
    qui a lieu a l'interieur de `PlayCardsLikeInTurn` — mais Fangs and Talons
    (sm009) est une Interruption qui part AVANT, et Hyper-Agility (sm010) une
    Reponse qui part APRES. Seul `_EN_COURS` retombe ici."""
    setattr(joueur, _EN_COURS, False)


def AccelerationEnCours(effect: 'Effect', joueur: 'Player|None' = None) -> bool:
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    return bool(joueur is not None and getattr(joueur, _EN_COURS, False))


def NoterEventJoue(joueur: 'Player', face: 'CardFace|None') -> None:
    setattr(joueur, _EVENT_JOUE, face)


def JoueViaAcceleration(effect: 'Effect', face: 'CardFace|None' = None) -> bool:
    """« If you played THIS card using your Acceleration ability ».

    ⚠ On compare la FACE, pas le card_id : le deck contient deux exemplaires
    de sm003, sm004, sm005 et sm006, et un card_id ne designe pas un objet
    (piege du §7 de RECETTES). Celui qu'on a joue est celui qu'on a memorise.
    """
    joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return False
    if face is None:
        face = getattr(effect, "this", None)
    memorisee = getattr(joueur, _EVENT_JOUE, None)
    return memorisee is not None and face is not None and memorisee is face


def EvenementJoueParAcceleration(joueur: 'Player|None') -> 'CardFace|None':
    """L'evenement que la DERNIERE resolution d'Acceleration a effectivement
    joue, ou `None` si elle n'en a joue aucun.

    ⚠ C'est la lecture de `sm010` Hyper-Agility (« without playing an
    event »). Elle n'est juste que parce que `OuvrirAcceleration` remet le
    marqueur a zero au debut de CHAQUE resolution : sans cela, une resolution
    muette heriterait de l'evenement joue par la precedente, et la carte ne
    partirait jamais.
    """
    if joueur is None:
        return None
    return getattr(joueur, _EVENT_JOUE, None)


def NoterDefaussees(joueur: 'Player', faces: Sequence['CardFace']) -> None:
    setattr(joueur, _DEFAUSSEES, [f for f in faces if f is not None])


def DefausseesParAcceleration(effect: 'Effect') -> List['CardFace']:
    joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return []
    return list(getattr(joueur, _DEFAUSSEES, []) or [])


################################################################################
# La limite « une fois par phase », comptee par le pack
################################################################################

def UsagesCettePhase(joueur: 'Player|None', effect: 'Effect') -> int:
    """Combien de fois Acceleration a deja ete resolue dans CETTE phase, par
    CE joueur.

    ⚠ Pourquoi le pack compte lui-meme au lieu d'un `LimitOncePerPhase()` du
    moteur : `sm008` Accelerated Vision donne « one additional time per phase »,
    et la limite du moteur ne sait pas compter jusqu'a deux.
    ⚠ Mais le COMPTEUR, lui, reste celui du moteur :
    `once_per_phase_player_effects` est vide par `WorldStat.OnPhaseEnd`
    (world_stat.py:80). Aucun etat maison a remettre a zero, donc aucun a
    oublier. Meme montage que `BloodRushPasEncoreResolue` (pack blade).
    """
    if joueur is None:
        return 0
    registre = getattr(effect.world.stat, "once_per_phase_player_effects", {}) or {}
    return sum(1 for x in registre.get(joueur, [])
               if getattr(getattr(x, "ability", None), "name", "") == NOM_ACCEL)


def NoterUsage(joueur: 'Player', effect: 'Effect') -> None:
    """⚠ RECETTES §1 : `once_per_phase_player_effects` NE S'ALIMENTE PAS TOUT
    SEUL. `Effect.SetHasSpellInPhase` ne l'alimente que pour une
    `TriggerNonePlayerMessage` ; `WhenResolveSpecialAbility` en est une, mais
    on n'y touche que par ce chemin-ci, donc la carte inscrit elle-meme son
    usage — sinon la limite LIT un registre que rien ne REMPLIT, et ne mord
    jamais (lecon `gb020` You Are My God)."""
    effect.world.stat.RecordEffectWithPlayer(effect, joueur)


def LimiteAcceleration(joueur: 'Player|None') -> int:
    """1 normalement, 2 si Accelerated Vision (sm008) est en jeu chez ce
    joueur. Filtre par card_id : « Accelerated Vision » n'a pas d'homonyme,
    mais le pack s'interdit les recherches par nom (voir l'en-tete).
    ⚠ `face.card_id` N'EXISTE PAS : c'est `face.paper.card_id`."""
    if joueur is None:
        return 1
    for carte in joueur.GetControlCards():
        if carte is not None and Upgrade.IsType(carte) and CardId(carte) == "sm008":
            return 2
    return 1


def PionsDeToile(face: 'CardFace|None') -> int:
    """Les pions `web` poses sur cette carte (sm011 Spinnerets).

    ⚠ `GetCounters` vit sur `CanPlaceCounter`, qui n'est PAS exporte par
    `cards.pack` : on passe par la face telle quelle, avec un `getattr` sur
    pour ne pas lever d'AttributeError que le moteur avalerait en silence.
    """
    if face is None:
        return 0
    lire = getattr(face, "GetCounters", None)
    if lire is None:
        return 0
    return int(lire(COMPTEUR_TOILE) or 0)


def CardId(face: 'CardFace|None') -> str:
    """Le card_id d'une face. ⚠ `face.card_id` n'existe pas (AttributeError
    avalee par le moteur) : le chemin est `face.paper.card_id`."""
    paper = getattr(face, "paper", None) if face is not None else None
    return getattr(paper, "card_id", "") or ""
