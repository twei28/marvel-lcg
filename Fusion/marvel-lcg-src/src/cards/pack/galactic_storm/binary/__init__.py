from cards.pack import *

# Helpers partages du set « Binary » (Galactic Storm, Kajislav).
#
# Tout le kit tourne autour d'UNE grandeur : « the number of [energy]
# resources in your hand ». Elle est lue par l'identite (ATK X, Burnout), par
# huit cartes du set et par la nemesis (Energy Transfer). Une seule fonction la
# calcule, pour que la reponse a la question Q3 (le wild compte-t-il ?) se
# change a UN endroit.
#
# Lecture retenue (voir .planning/todos/2026-10-20-gs1-questions.md, Q3, et le
# gabarit de gs001a) :
#  - on compte des ICONES, pas des cartes : Energy Torrent (YY) vaut 2. C'est ce
#    que le livret de deck confirme en creux (Energy Torrent n'existe que pour
#    nourrir X) ;
#  - on lit la ressource IMPRIMEE telle que le moteur la voit EN MAIN, donc APRES
#    Energy Conversion (gs010), qui passe par `WhenCountingResourcesOnCards`
#    (FAQ du livret 1.2 p.22 : Cosmic Influx apres Energy Conversion ne fait
#    aucun degat) ;
#  - une icone [wild] n'est PAS une ressource [energy] tant qu'elle reste en
#    main (`convert_green_res=False`, comme `has_printed_res` du moteur).

NOM_ENERGY_CONVERSION = "Energy Conversion"


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit.

    ⚠ Pas `effect.GetInitiator()` en premier : il leve un assert quand
    l'initiateur n'est pas un joueur, et le moteur avale l'exception (lecon
    lady_sif). Les capacites continues (ATK X, Body in Flames) sont evaluees
    hors tour de jeu, sans initiateur.
    """
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if controleur is not None and Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def EnergieDeLaCarte(face: 'CardFace') -> int:
    """Nombre d'icones [energy] que la carte porte LA OU ELLE EST (main comprise,
    donc apres Energy Conversion). Une carte sans ressource vaut 0."""
    return FacesCounter.GetPrintedResourcesCount([face], "Y")


def NonEnergieDeLaCarte(face: 'CardFace') -> int:
    """Nombre d'icones de ressource qui ne sont PAS [energy] (physique, mentale,
    wild, et l'eventuelle « L »). Lu par Cosmic Influx (gs002)."""
    return FacesCounter.GetPrintedResourcesCount([face], ["R", "B", "G", "L"])


def EnergieEnMain(joueur: 'Player|None') -> int:
    """« the number of [energy] resources in your hand »."""
    if joueur is None:
        return 0
    return sum(EnergieDeLaCarte(f) for f in joueur.hand_cards.Get())


def CartesEnergieEnMain(joueur: 'Player|None') -> List['CardFace']:
    """« each [energy] resource from your hand » : les CARTES qui portent au
    moins une icone [energy] (Burnout gs001a, Energy Transfer gs240)."""
    if joueur is None:
        return []
    return [f for f in joueur.hand_cards.Get() if EnergieDeLaCarte(f) > 0]


def EnergieDuJoueur(effect: 'Effect') -> int:
    return EnergieEnMain(JoueurDeCetteCarte(effect))


def RecalculEnergie() -> List['OnEvent.Base']:
    """Les evenements qui changent la grandeur : la main bouge, ou Energy
    Conversion entre en jeu / en sort (elle change la COULEUR des icones sans
    rien deplacer dans la main)."""
    return [
        OnEvent.HandCards("EngagedPlayer"),
        OnEvent.CardInPlay(CardFinder(name=NOM_ENERGY_CONVERSION)),
    ]
