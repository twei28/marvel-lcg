from . import *

# * Captain America (Steve Rogers) — custom « Rainy »
# Retaliate 1.
# Interrupt: When Captain America defends against an attack and would take
# damage, reduce that damage by 2 (to a minimum of 1).
#
# Modele : Self-propelled Glide (56179, Spider-Woman), pour le declencheur
# WhenUnitWouldTakeDamage / message.ReduceDamage en interruption de defense.
#
# Le Retaliate 1 n'a besoin d'aucun script : c'est un attribut lu depuis
# `desc['Retaliate']` par `HasRetaliate` (attribute/can_retaliate.py), comme
# tout allie officiel a Retaliate imprime (U.S. Agent 04014, Charlie-27
# 21059) : ces cartes n'ont pas de fichier .py pour leur Retaliate.
#
# RESERVE (7/8/2026) : la fiche 79002 dans data/cards.json ne porte pas la
# cle desc['Retaliate']. Sans elle, Captain America n'aura aucun Retaliate en
# jeu malgre le texte imprime, meme une fois ce script construit. Signale
# dans le rapport de tache 2 : correctif attendu de la tache 1 (donnees),
# hors perimetre de cette tache-ci qui ne cree que des fichiers sous
# src/cards/pack/agent_13/.
#
# La reduction est bornee a 1 point de degats minimum : on ne retranche
# jamais plus que (degats_prevus - 1), jamais moins que 0.

def GetAbilities() -> Sequence['Ability']:

    def captain_america_interrupt(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        value = min(2, message.will_take_damage - 1)
        if value > 0:
            message.ReduceDamage(value, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "This",
            captain_america_interrupt,
            is_from_attack=True,
            while_defending=True,
        ),
    ]
