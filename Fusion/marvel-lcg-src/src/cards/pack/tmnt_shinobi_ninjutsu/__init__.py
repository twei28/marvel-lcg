from cards.pack import *

# Aides du pack TMNT Shinobi Ninjutsu (Inkwire, sa001-sa020). Aucune n'est partagee avec un autre pack :
# les helpers communs a tout Shinobi (CarteShinobi, ShinobiCloak...) vivent dans `cards/pack/__init__.py`.
#
# Mots-cles lus AVANT ce code : cloak.md, cloaked.md (statut, UN seul par personnage, Solide n'y change rien,
# Coriace avant Cloaked), shinobi.md.


def HerosCamoufle(joueur: 'Player|None') -> bool:
    """« Your hero is cloaked » : l'identite du joueur est en FORME HEROS et porte une carte Cloaked.
    (En forme alter-ego il n'y a pas de « heros » en jeu : faux. Voir .planning/tmnt/shinobi-ninjutsu-questions.md, Q-N1.)"""
    if joueur is None or not joueur.IsHero():
        return False
    return joueur.GetHero().IsCloaked()


def IdentiteCamouflee(joueur: 'Player|None') -> bool:
    """« Your identity is cloaked » : l'identite du joueur, quelle que soit sa forme, porte une carte Cloaked."""
    return joueur is not None and joueur.GetIdentity().IsCloaked()


def JouableSiHerosCamoufle(ability: 'Ability') -> 'Ability':
    """« Play only if your hero is cloaked. » : condition de jeu posee en tete des conditions (comme
    `JouableSiVousControlez` du pack tmnt_aspect_basic)."""
    def camoufle(effect: 'Effect', message: 'Message2') -> bool:
        Unused(message)
        return HerosCamoufle(effect.GetInitiator())
    ability.conditions = [camoufle] + ability.conditions
    return ability


def _controles(effect: 'Effect', face: 'CardFace') -> bool:
    joueur = Select.GetYou(effect)
    return face in joueur.GetControlCharacters()


def CoutDefausserCloaked(qui: str) -> 'CostFunc.Custom':
    """Cout « Discard a cloaked status card from <qui> » : `qui` vaut "hero" (votre heros, forme heros), "identity"
    (votre identite) ou "controlled" (un personnage que vous controlez, au choix). Sans carte Cloaked sur un
    personnage valide, l'action n'est pas proposee. Modele : `sk049` (cout Custom sur le personnage + DiscardTough)."""
    def valide(effect: 'Effect', face: 'CardFace') -> bool:
        joueur = Select.GetYou(effect)
        if qui == "hero":
            return Hero.IsType(face) and face == joueur.GetIdentity()
        if qui == "identity":
            return face == joueur.GetIdentity()
        return _controles(effect, face)

    def defausser(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        return bool(cibles) and cibles[0].DiscardCloaked(effect, rule=1) > 0

    return CostFunc.Custom(CardFinder(has_status="Cloaked", check_effect_fn=valide), defausser)  # type: ignore


def CoutCamoufler(qui: str = "controlled") -> 'CostFunc.Custom':
    """Cout « Cloak a character you control » (sa003 Reconnaissance) : pose une carte Cloaked sur un personnage que
    vous controlez ET qui peut en recevoir une (un personnage deja camoufle n'est pas une cible valide : le cout
    ne serait pas paye)."""
    def valide(effect: 'Effect', face: 'CardFace') -> bool:
        return _controles(effect, face) and face.cloaked < face.cloaked_max  # type: ignore

    def camoufler(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(qui)
        return bool(cibles) and ShinobiCloak(effect, cibles[0]) > 0

    return CostFunc.Custom(CardFinder(check_effect_fn=valide), camoufler)  # type: ignore
