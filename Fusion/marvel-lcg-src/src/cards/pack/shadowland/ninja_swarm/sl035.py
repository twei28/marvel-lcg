from . import *

# Dancing Shadows — COMPLOT ANNEXE. Menace de depart 3 (fixe), Boost ★.
# Each NINJA minion gets +1 hit point.
# Threat cannot be removed from this scheme while at least 1 NINJA minion is in play.
# [star] Boost : Reveal this card.
#
# Cartes de reference : skrull_menace/army_of_skrulls/sk113 (`GiveKeywordToInPlayWhenApplyThis(CardFinder2(trait, Minion), ...)`), shadows_in_the_night/sl003 (`ThreatCannotBeRemovedFromWhile`
#  + condition), shadows_in_the_night/sl006 (boost `RevealThisCard`).
# ⚠ Mots-pieges : « each NINJA minion » = tout sbire NINJA en jeu, y compris ceux des autres joueurs ; « 3 » est FIXE (pas par joueur) ; « at least 1 NINJA minion in play » : la
#  contrainte vaut sur CETTE manigance seulement, et tombe des que le dernier sbire NINJA quitte le jeu ; boost : la carte est REVELEE (elle entre en jeu), pas jouee.


def GetAbilities() -> Sequence['Ability']:

    def un_ninja_en_jeu(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        return Worlds.FindCardOnField(effect, CardFinder2("NINJA", Minion)) is not None

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder2("NINJA", Minion), health=1),
        AbilityFactory.ThreatCannotBeRemovedFromWhile("This", conditions=[un_ninja_en_jeu]),
        AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard),
    ]
