from . import *

# Agent 13's Pistol — custom « Rainy »
# Restricted.
# Hero Response: After Agent 13 attacks, exhaust Agent 13's Pistol and discard
# the top card of the encounter deck -> deal 1 damage to an enemy for each
# boost icon discarded this way.
#
# Modele officiel : Hex Bolt (15004, Scarlet Witch), pour le vocabulaire de la
# mecanique du pack -- defausser une carte de rencontre puis compter ses
# icones de bonus par `FacesCounter.CountTotalBoostIcons`. Ici pas de palier :
# le nombre d'icones EST le nombre de degats, sans branche 0/1/2/3+.
#
# Le declencheur nomme Agent 13 explicitement (comme Superhuman Strength
# 01028 nomme She-Hulk, Weapons Training 41011 nomme Psylocke) :
# `CardFinder(name="Agent 13")` sur `AfterUnitAttackEnd`, pas "YourHero". La
# fiche 01019a de She-Hulk (nom imprime "* She-Hulk") confirme que le moteur
# compare ce nom sans le prefixe d'affichage « * » : "Agent 13" suffit.
#
# Si la carte defaussee ne porte aucune icone, `DealDamage(targets, 0, effect)`
# inflige zero degat : resultat legitime du texte imprime (« for each boost
# icon discarded this way »), pas une erreur a esquiver.

def GetAbilities() -> Sequence['Ability']:

    def agent_13s_pistol(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        faces = Worlds.DiscardEncounterCards(1, effect)
        icones = FacesCounter.CountTotalBoostIcons(faces)
        this.DealDamage(effect.targets, icones, effect)

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.HeroResponse,
            CardFinder(name="Agent 13"),
            agent_13s_pistol,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Enemy),
    ]
