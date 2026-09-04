from . import *

# Astral Travel (x2) — EVENEMENT, cout 2, [energy]. SUPERPOWER. THWART.
# ⚠ NOM : les fichiers du zip et la decklist disent « Turning Astral ». LA
#   CARTE dit ASTRAL TRAVEL, et le scan fait foi. Question posee a l'auteur.
# While this card is in your hand your thwarts remove 1 additional threat.
# Hero Action (thwart): Remove 3 threat from a scheme.
#
# TEXTE CONTRE CODE
#  « your thwarts remove 1 additional threat » -> `thwart=1` sur l'identite.
#    ⚠ ECART ASSUME : le texte parle des « contres » du joueur, on code un +1
#    CTR a l'identite. Les deux se confondent pour un contre de base ; un
#    evenement qui contre, lui, ne profite pas du bonus. C'est la lecture
#    retenue partout au depot pour cette tournure.
#  « Hero Action (thwart) » -> `SetLabel('thwart')` : le libelle compte, il
#    ouvre les fenetres de reponse « apres un contre » et subit Patrouille.


def GetAbilities() -> Sequence['Ability']:

    # ⚠ `RemoveThreatFromSchemes` et NON `RemoveThreat`, qui n'existe pas :
    # « 'Event' object has no attribute 'RemoveThreat' », exception AVALEE.
    # Sorti par l'autoplay, jamais par les cas — ils s'arretaient avant.
    def voyage_astral(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        this.RemoveThreatFromSchemes(effect.targets, 3, effect)

    return [
        # ⚠ La moitie « tant que cette carte est dans votre main » n'est PAS
        # ici : elle est portee par le HEROS (dr001a), seule facon de la faire
        # fonctionner. Raison detaillee dans `__init__.py`.
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            voyage_astral,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
