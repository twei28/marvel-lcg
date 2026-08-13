from cards.pack import *


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
