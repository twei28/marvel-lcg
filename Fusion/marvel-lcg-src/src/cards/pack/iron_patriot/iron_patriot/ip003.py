from . import *

# * Absolute Power — MANIGANCE-JOUEUR, cout 1, RES [physical], 3 menaces.
# Victory 0.
# Threat cannot be removed from this scheme by heroes or allies.
# While in the victory display, each REGISTERED character gets +1 ATK.
# Hero Action: Exhaust a REGISTERED character you control -> remove 1 threat
#   from here. Any player may trigger this ability.
#
# CARTE DE REFERENCE, ET ELLE FAIT LES DEUX MOITIES
#  - `40006` * Technovirus Purge (pack next_evol) : la MEME carte, structure
#    pour structure. `ThreatCannotBeRemovedFromWhile("This", by_character=...)`
#    pour le verrou, et `GiveKeywordToInPlayWhenApplyThis(...,
#    works_in_the_victory_display=True)` pour le bonus qui ne s'allume QU'UNE
#    FOIS LA MANIGANCE VAINCUE. Ce dernier parametre existe litteralement pour
#    cette carte-la : la signature de la fabrique le cite en commentaire.
#
# TEXTE CONTRE CODE
#  ⚠ Le verrou et l'Action ne se contredisent PAS : la menace n'est pas retiree
#    « par un heros ou un allie », elle l'est PAR LA MANIGANCE, qui se paie en
#    inclinant un personnage. Le personnage est le COUT, pas l'auteur du
#    retrait. Sans cette lecture la carte serait impossible a contrer.
#  ⚠ « ANY PLAYER may trigger » : en multijoueur, ce n'est pas reserve au
#    proprietaire.
#  ⚠ « each REGISTERED CHARACTER », pas « ally » : Iron Patriot lui-meme porte
#    le trait, il gagne donc le bonus.
#  ⚠ `CardFinder(trait=...)` SEUL ne passe pas : la fabrique exige un
#    `card_type` en plus des le moment ou un trait est donne
#    (`assert len(card_finder.params) == 2`, environment.py:134). D'ou
#    `card_type=Unit2`, qui EST « character » dans le vocabulaire du moteur.


def GetAbilities() -> Sequence['Ability']:

    def un_heros_ou_un_allie(face: 'CardFace') -> bool:
        return Hero.IsType(face) or AlterEgo.IsType(face) or Ally.IsType(face)

    def retirer_une_menace(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(message)
        this.RemoveThreatFromSchemes([this], 1, effect)

    return [
        AbilityFactory.ThreatCannotBeRemovedFromWhile(
            "This",
            by_character=CardFinder(check_face_fn=un_heros_ou_un_allie),
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Unit2, trait=TRAIT_REGISTERED),
            works_in_the_victory_display=True,
            attack=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            retirer_une_menace,
        ).SetCostFunc(CostFunc.Exhaust(CardFinder(trait=TRAIT_REGISTERED))),
    ]
