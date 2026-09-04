from cards.pack import *

# ===========================================================================
# Helpers partages du set « Texas Twister » (Kajislav, zip Texas Twister
# (Released), set 157, prefixe `tt`).
#
# ⚠ TOUT LE PACK TIENT SUR UNE SEULE PHRASE : « After you use one of Texas
# Twister's basic powers (THW, ATK, or DEF), ... ». Elle revient sur QUATRE
# cartes — l'identite heros elle-meme (tt001a, +1 a ce pouvoir), tt004 Keep
# Spinning (le redresser), tt007 Cyclonic Suction (piocher) et tt019 Twist
# Again (redresser le heros ET Shooting Star). Le kit consiste donc a
# enchainer les pouvoirs de base, chacun rendant le suivant meilleur.
#
# Le moteur a la fabrique dediee : `AbilityFactory.AfterUnitUseBasicPower`
# (friend.py:373), avec `powers=["ATK", "THW", "DEF"]` et le message qui
# expose `message.power`. Modeles du depot : `14001a` Quicksilver (redresse),
# `04032` Captain Marvel (pioche), `28001a` Nova.
#
# ⚠ NE PAS ECRIRE `powers="Hero"` PAR PARESSE : le litteral est traduit en
# `["ATK", "THW", "DEF"]` par la fabrique elle-meme, mais l'ecrire en clair
# rend le filtre lisible a cote du texte imprime, qui les cite nommement.
# ===========================================================================

NOM_HEROS = "Texas Twister"
NOM_CIVIL = "Drew Daniels"
NOM_SHOOTING_STAR = "Shooting Star"
TRAIT_RANGER = "RANGER"
TRAIT_ROTATION = "ROTATION"
POUVOIRS_DE_BASE: List["CardFace.BASIC_POWER"] = ["ATK", "THW", "DEF"]


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit.

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception — la carte ne fait alors rien, et aucun outil ne le voit
    (leçon `Player.GetHero()`, pack lady_sif). `GetControlByOrOwner` retombe
    sur le PROPRIETAIRE quand la carte n'est pas en jeu.

    ⚠ Passer le joueur EXPLICITEMENT quand la carte qui agit ne lui appartient
    pas : c'est le cas de l'obligation tt020, carte de RENCONTRE donnee au
    joueur, pour laquelle ce helper ne rend rien (leçon yd013 / dr010).
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


def HerosDuJoueur(effect: 'Effect') -> 'CardFace|None':
    """La face HEROS de l'identite du joueur, ou None s'il est en civil."""
    joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    identite = joueur.GetIdentity()
    if identite is None or not Hero.IsType(identite):
        return None
    return identite


def BonusAuPouvoir(face: 'CardFace|None', pouvoir: str, effect: 'Effect') -> None:
    """« +1 to THAT power until the end of the round ».

    ⚠ LE POUVOIR EST LU SUR LE MESSAGE (`message.power`), jamais devine : la
    carte ne donne PAS +1 partout, elle donne +1 au SEUL pouvoir qui vient
    d'etre utilise. Confondre les deux ferait de tt001a un triple de tt003
    Accelerated Rotation, qui elle donne bien les trois.

    `GainUntilRoundEnd` est l'idiome du depot pour un bonus de statistique a
    duree de round (modele `12016` Moxie).
    """
    if face is None:
        return
    if pouvoir == "ATK":
        face.GainUntilRoundEnd(effect, attack=1)
    elif pouvoir == "THW":
        face.GainUntilRoundEnd(effect, thwart=1)
    elif pouvoir == "DEF":
        face.GainUntilRoundEnd(effect, defense=1)


def CarteEnJeu(effect: 'Effect', nom: str) -> 'CardFace|None':
    """Une carte nommee, sur le terrain, ou None."""
    return Worlds.FindCardOnField(effect, name=nom)


def RangersDuJoueur(effect: 'Effect') -> List['CardFace']:
    """« each [[RANGER]] character you control » (tt016 Lone Star Rangers).

    ⚠ « CHARACTER » ET NON « ALLY » : l'identite heros de Texas Twister porte
    elle-meme le trait RANGER, elle est donc redressee avec les allies. C'est
    tout l'interet de la carte, et le mot-piege du texte.
    """
    joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return []
    faces = list(joueur.GetControlCards(CardFinder(card_type=Unit2, trait=TRAIT_RANGER)))
    identite = joueur.GetIdentity()
    if identite is not None and identite.HasTrait(TRAIT_RANGER) and identite not in faces:
        faces.append(identite)
    return faces
