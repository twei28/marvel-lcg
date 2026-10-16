from . import *

# Baxter's Laboratory (1B) — MANIGANCE PRINCIPALE, face B (Baxter's Lab 4/22).
# 11[per_hero] menaces, depart 1[per_hero], escalade +1[per_hero].
# Replicate — Special: Place 1 all-purpose counter on each SWARM minion engaged with you. If there
#   are no SWARM minions engaged with you, deal yourself a facedown encounter card.
# If this scheme is completed, the players lose the game.
#
# Cartes de reference : `ab007` / `zeus` pour `WhenResolveSpecialAbility("This", ...)` (le joueur qui
# resout est `message.GetToPlayer()`) ; `gmw/16034` Battery Pack pour « all-purpose counter » (la
# carte qui porte le compteur en definit le type, FAQ officielle) ; `ar012` pour `joueur.DealEncounterCards(1)`.
# « If this scheme is completed, the players lose » : regle de base du dernier stade, aucun module
# (comme sp001b / 56124b).
#
# Mots-pieges : « engaged with YOU » (le joueur qui resout, pas tous) ; « each SWARM minion » (tous
# ceux qui lui sont engages) ; « If there are NO SWARM minions » (aucun compteur pose, alors une carte face
# cachee) ; « deal YOURSELF » (celui qui resout), jamais le premier joueur.


def GetAbilities() -> Sequence['Ability']:

    def replicate(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        sbires = joueur.GetEngagedMinions(CardFinder(trait=TRAIT_SWARM))
        if sbires:
            for sbire in sbires:
                PlacerUnCompteurSur(sbire, 1, effect)
        else:
            joueur.DealEncounterCards(1, effect)

    return [AbilityFactory.WhenResolveSpecialAbility("This", replicate).SetName(NOM_DU_SPECIAL)]
