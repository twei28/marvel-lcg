from cards.pack.web_of_deceit import *


def Negate(valeur: int) -> 'Ability':
    """« Negate X. » — mot-cle neuf de la campagne (livret p.2).

    « After this card is revealed or turned faceup during an enemy activation,
    if any of its effects are canceled, the revealing player draws X cards. »

    Le moteur annonce DEJA l'annulation d'une carte rencontre : `CancelEffects`
    et `CancelAllEffectsInternal` envoient `WhenEffectBeCancel`, et le
    presentateur l'affiche meme sous le nom « negate ». Il n'y a pas de fabrique
    pour ce message, l'abilite se construit donc a la main.

    ⚠ ECART, ecrit : le texte restreint le mot-cle a une annulation survenue
    PENDANT une activation d'ennemi ; le moteur ne rapporte pas ce contexte dans
    le message, la carte pioche donc quelle que soit la fenetre d'annulation.
    """
    def piocher(effect: 'Effect', message: 'Message.WhenEffectBeCancel') -> None:
        joueur = Worlds.GetCurrentPlayer(effect)
        joueur.DrawUp(valeur, effect)

    return Ability(
        AbilityType.ForcedResponse,
        Message.WhenEffectBeCancel,
        [Condition2.ThisIsTrigger],
        piocher,
        is_local=True
    )
