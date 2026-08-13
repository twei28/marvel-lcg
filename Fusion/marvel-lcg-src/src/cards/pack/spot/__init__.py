from cards.pack import *

# Les cartes du DECK RENCONTRE qui portent le mot-cle Threat Level.
#
# `CardFinder` ne sait pas filtrer sur un mot-cle : il connait les noms, les
# traits, les types, les classes, pas les attributs de `desc`. Une recherche
# « a Spot card with the Threat Level keyword » se fait donc par identifiants.
# Sans cette liste, la mise en place proposait les 20 cartes du set, y compris
# les traitrises qui n'ont aucun niveau -- vu sur le plateau, pas deduit.
#
# Le vilain et le complot principal en portent aussi, mais ils ne sont jamais
# dans le deck rencontre : ils n'ont donc rien a faire ici.
CARTES_A_NIVEAU: List[str] = [
    "sp007",  # Rocket Racer      2
    "sp008",  # Puma              3
    "sp009",  # Anywhere & Everywhere  4
    "sp010",  # Chameleon         5
    "sp011",  # Penchant for Pilfery   6
    "sp012",  # Living Laser      7
    "sp013",  # Spotty Pasts      8
    "sp014",  # Warp Hole         9
    "sp015",  # The Hypernova    10
]



def GagneParMenacePosee(diviseur: int, *, maximum: int|None=None, **statistique) -> 'Ability':
    """« +1 <stat> pour chaque N menaces sur lui. »

    La forme revient sur quatre cartes du set (Puma, Chameleon, Living Laser,
    et les quatre stades de The Spot). La menace est un JETON, pas un
    compteur : d'ou `GetTokens('threat')` et `OnEvent.Token`, sans quoi la
    statistique ne se rafraichirait jamais quand la menace bouge.
    """
    def valeur(effect: 'Effect', ui: List['CardFace']) -> int:
        gagne = effect.this.CastTo(CanPlaceToken).GetTokens('threat') // diviseur
        return min(gagne, maximum) if maximum is not None else gagne

    return AbilityFactory.ThisGainKeyword(
        valeur,
        change_on_event=OnEvent.Token("This", 'threat'),
        **statistique
    )
