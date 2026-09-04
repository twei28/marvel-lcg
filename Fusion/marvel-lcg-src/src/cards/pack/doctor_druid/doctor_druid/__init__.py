from cards.pack import *

# ===========================================================================
# Helpers partages du set « Doctor Druid » (Kajislav, zip Doctor Druid
# (Released), set 155, prefixe `dr`).
#
# ⚠ LE PACK ENTIER TIENT SUR UNE ZONE INHABITUELLE : LA MAIN.
# SEPT des huit cartes signature portent « While this card is in your hand,
# ... ». Ce sont des capacites qui doivent etre ACTIVES SANS QUE LA CARTE SOIT
# EN JEU, ce que le moteur rend par `Ability.CanWorkOnlyInHand()`
# (ability.py:651). Le drapeau est lu par `CheckNotOutOfPlay`
# (effect_checker.py:241), qui est le controle de zone GENERIQUE de toute
# capacite : il vaut donc pour n'importe quelle famille, pas seulement pour le
# calcul de cout.
#
# ⚠ PREMIER USAGE NON-COUT DU DEPOT. Les neuf cartes qui employaient deja
# `CanWorkOnlyInHand()` (hercules/59009, fne/60048, mts/21032, deadpool/44012,
# aos/50013, red_guardian/rg008...) s'en servent TOUTES pour modifier un cout.
# Ici on s'en sert pour accorder des mots-cles et des bonus de statistique.
#
# ⚠ ET LE SET NEMESIS VISE EXACTEMENT CETTE RESSOURCE : l'obligation dr010, la
# manigance dr012 et l'attachement dr013 defaussent des cartes « specifiques a
# l'identite » DE LA MAIN. Le pack se joue donc sur une tension permanente :
# chaque carte vaut mieux gardee que jouee, et l'adversaire vide la main.
# ===========================================================================

NOM_HEROS = "Doctor Druid"
NOM_CIVIL = "Anthony Druid"
SET_HEROS: 'CardFace.SETNAMES' = "Doctor Druid"


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit.

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception — la carte ne fait alors rien, et aucun outil ne le voit
    (leçon `Player.GetHero()`, pack lady_sif). `GetControlByOrOwner` retombe
    sur le PROPRIETAIRE quand la carte n'est pas en jeu, ce qui couvre a la
    fois l'evenement en cours de resolution ET, ici, les cartes qui agissent
    depuis la MAIN.

    ⚠ Passer le joueur EXPLICITEMENT quand la carte qui agit ne lui appartient
    pas : c'est le cas de l'obligation dr010, carte de RENCONTRE donnee au
    joueur, pour laquelle ce helper ne rend rien (leçon yd013, pack yondu).
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


def EstCarteDuDruide(face: 'CardFace|None') -> bool:
    """« a Doctor Druid card » (dr003 Ancient One, dr004 Fellow Druid).

    Le moteur a la primitive : `IsDeckBuildingClass` (card_player.py:169)
    verifie D'ABORD la classe `IdentitySpecific`, PUIS l'egalite litterale du
    `set_name`. Ne PAS comparer les noms a la main.
    """
    if face is None or not ClassCard.IsType(face):
        return False
    return face.IsDeckBuildingClass(SET_HEROS)


def EstSpecifiqueIdentite(face: 'CardFace|None') -> bool:
    """« an identity-specific card » (dr010, dr012, dr013).

    ⚠ PLUS LARGE que `EstCarteDuDruide` : le texte du set nemesis ne dit PAS
    « a Doctor Druid card », il dit « identity-specific ». En solo les deux se
    confondent, mais pas des qu'un autre heros est a table — et c'est
    exactement la carte du VOISIN qu'il ne faut pas defausser. On teste donc
    la seule classe, sans le set_name.

    Ecriture reprise telle quelle de `beast/beast_nemesis/bt021.py:46`, qui
    est aussi une carte NEMESIS defaussant des cartes specifiques a
    l'identite : `ClassCard.IsType(face) and face.IsClass(...)`. Le garde de
    type est obligatoire — `IsClass` n'existe que sur `ClassCard`.
    """
    if face is None or not ClassCard.IsType(face):
        return False
    return face.IsClass("IdentitySpecific")


def MainDuJoueur(joueur: 'Player|None') -> List['CardFace']:
    """Les cartes de la main, ou une liste vide."""
    if joueur is None:
        return []
    return list(joueur.hand_cards.Get())


def EvenementsSpecifiquesEnMain(joueur: 'Player|None') -> List['CardFace']:
    """Les evenements specifiques a l'identite presents dans la main.

    Utilise par dr010 (« discard EACH identity-specific EVENT from your
    hand ») et dr013 (« discard AN identity-specific event »). ⚠ EVENT et non
    « carte » : dr012, elle, dit bien « card ». Trois textes voisins, trois
    portees differentes, a ne jamais confondre.
    """
    return [f for f in MainDuJoueur(joueur)
            if Event.IsType(f) and EstSpecifiqueIdentite(f)]


def DepuisLaMain(abilities: List['Ability']) -> List['Ability']:
    """« While this card is in your hand, ... » applique a TOUTE une fabrique.

    Les fabriques de bonus (`GiveKeywordToInPlayWhenApplyThis`,
    `GiveKeywordToAttached`) rendent une LISTE d'abilities, pas une seule :
    poser `.CanWorkOnlyInHand()` sur le resultat direct ne marcherait pas. On
    l'applique donc a chacune, en un seul endroit, pour que les sept cartes
    concernees s'ecrivent toutes pareil et qu'aucune ne l'oublie.
    """
    return [a.CanWorkOnlyInHand() for a in abilities]


def EvenementRejouable(face: 'CardFace|None') -> bool:
    """Un evenement porteur d'une capacite « Action » ou « Hero Action ».

    Le filtre de `dr001a` Druidic Ritual. ⚠ « Action » et « Hero Action »
    SEULEMENT : `dr008` Mystical Protection est une Hero INTERRUPT et n'est
    donc PAS rejouable, alors qu'elle est bien un evenement du set. C'est le
    mot-piege de la carte.
    """
    if face is None or not Event.IsType(face):
        return False
    for effet in face.effect.Find():
        drapeaux = effet.ability.flags
        if drapeaux.is_action:
            return True
    return False


def EstEnMain(effect: 'Effect') -> bool:
    """La carte qui porte cette capacite est-elle DANS LA MAIN, maintenant ?

    ⚠ CORRECTIF DU 04/09/2026, ET C'EST LE COEUR DU PACK.
    `CanWorkOnlyInHand()` NE SUFFIT PAS pour un modificateur CONTINU. Ce
    drapeau est lu par `CheckNotOutOfPlay` (effect_checker.py:241), qui
    gouverne la RESOLUTION d'une capacite ; les bonus permanents rendus par
    `GiveKeywordToInPlayWhenApplyThis` sont, eux, collectes par un autre
    chemin qui ne passe pas par ce controle.

    Mesure qui l'a etabli : `dr007` Elemental Control donnait +1 ATQ au heros
    AUSSI BIEN en main qu'une fois JOUEE et partie a la defausse (ATQ 2 dans
    les deux cas). Le cas « en main » passait donc par accident, et le
    contre-temoin « jouee » l'a sorti — c'est exactement pour ca qu'il avait
    ete ecrit.

    La fabrique expose un `condition=` evalue A CHAQUE LECTURE de la valeur :
    c'est lui, et pas le drapeau de zone, qui rend l'effet reellement
    conditionnel a la main.
    """
    porteur = getattr(effect, "this", None)
    return porteur is not None and porteur.IsLikeInHand()


# ===========================================================================
# ⚠ POURQUOI LES BONUS « EN MAIN » VIVENT SUR LE HEROS ET NON SUR LES CARTES
#
# Constat du 04/09/2026, apres trois montages successifs qui ont TOUS echoue :
#   1. `CanWorkOnlyInHand()` seul  -> le bonus s'appliquait TOUJOURS, meme la
#      carte partie a la defausse (effect_checker.py:241 ne gouverne que la
#      RESOLUTION d'une capacite, pas la collecte des modificateurs continus).
#   2. + `condition=` -> aucun changement.
#   3. + `change_on_event=OnEvent.HandCards(...)` -> aucun changement.
#
# La raison de fond : AUCUNE carte du depot n'a jamais fait porter un
# modificateur CONTINU par une carte SITUEE EN MAIN. `21032` Pip the Troll,
# que le moteur cite nommement dans son controle de zone, emploie bien
# `CanWorkOnlyInHand()` — mais sur une capacite DECLENCHEE, pas sur un bonus
# permanent. La fabrique `GiveKeywordToInPlayWhenApplyThis` ne sait pas
# s'alimenter depuis la main.
#
# LE MONTAGE RETENU est celui de `sm/personal_nightmare/27154` (Evil
# Doppelganger), seule carte du jeu a lire une main : la carte qui PORTE le
# bonus est EN JEU et compte ce que la main contient. Ici c'est donc le HEROS
# qui porte les sept bonus, avec `change_on_event=OnEvent.HandCards`.
#
# ⚠ CONSEQUENCE POUR LA PREUVE PAR SUBSTITUTION : la moitie « en main » de
# dr004-dr009 n'est plus dans leur module. Retirer l'un de ces modules ne fera
# donc PAS tomber le cas « en main » correspondant ; seule leur moitie JOUEE
# (l'Action) reste de leur ressort. C'est assume et documente ici plutot que
# masque.
# ===========================================================================

def ExemplairesEnMain(effect: 'Effect', nom: str) -> int:
    """Combien d'exemplaires de la carte nommee le joueur a-t-il en main ?

    Le compte, et non un booleen : deux Elemental Control en main donnent bien
    +2 ATQ, ce que le texte imprime implique sans le dire.
    """
    joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return 0
    return len([f for f in joueur.hand_cards.Get() if f.IsName(nom)])


def BonusSelonLaMain(nom: str, **stats: int) -> 'Ability':
    """Un bonus au heros, proportionnel aux exemplaires de `nom` en main."""
    def compter(effect: 'Effect', ui: List['CardFace']) -> int:
        Unused(ui)
        return ExemplairesEnMain(effect, nom)
    return AbilityFactory.ThisGainKeyword(
        compter,
        change_on_event=OnEvent.HandCards("EngagedPlayer"),
        **stats,
    )
