from cards.pack import *


def JouableSiVousControlez(ability: 'Ability', traits: List[str]) -> 'Ability':
    """« Play only if you control a <A> or <B> card » (ub033, ub045).

    `SetPlay(only_if_you_control_trait=...)` n'accepte qu'UN trait, et `only_if_you_control_face` lit
    l'inventaire de l'IDENTITE (ses attachements), pas les cartes controlees. Meme condition que
    `only_if_you_control_trait` (ability.py : `initiator.IsControl(CardFinder2(trait))`), etendue a
    plusieurs traits (OU), posee en tete des conditions de jeu comme le fait `SetPlay`."""
    def controle(effect: 'Effect', message: 'Message2') -> bool:
        initiateur = effect.GetInitiator()
        return any(initiateur.IsControl(CardFinder2(t)) for t in traits)
    ability.conditions = [controle] + ability.conditions
    return ability
