from . import *

# Quack Attack (1/2) — ATTACK — evenement, cout 1
# Hero Interrupt (attack/defense): When you would take any amount of damage,
#   prevent 2 of that damage. Deal 1 damage to an enemy for each side scheme
#   in the victory display.
#
# Exemplaire physique 1 de 2 (hd005 RES physique, hd006 RES energie : meme
# texte, deux card_id distincts — modele ok004/ok005).
#
# Declencheur : modele exact next_evol/cable/40012.py (Telekinetic Force
# Field), `AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.HeroInterrupt,
# <qui>, ...)` + `message.PreventDamage(<n>, effect)`. Deux ecarts VOULUS par
# le texte : la cible est « you » (l'identite du joueur, `"You"`, la ou Force
# Field couvre tout `Friend`) et la prevention vaut 2 (pas "All").
# « any amount of damage » = aucun filtre supplementaire (ni `is_from_attack`,
# ni `is_consequential_damage`) : le declencheur nu couvre tout.
#
# Degats : `for each side scheme in the victory display` = TOUTES les
# manigances annexes, celles du vilain comprises (portee large, voir le
# __init__.py du set) -> `NombreDeManigancesEnVictoire`, modele exact
# next_evol/cable/40011.py (Plasma Rifle). La cible ennemie est choisie a la
# resolution (`ChooseAbilities` imbrique, modele ok008) et non par un
# `SetTarget` statique : la carte est jouee en INTERRUPTION, le SetTarget de
# l'ability principale serait resolu avant de savoir s'il y a des degats a
# infliger (0 manigance en victoire = aucun degat, donc aucune cible a
# demander).


# CORRECTIF (30/08/2026) : la capacite PRINCIPALE portait `SetLabel()` VIDE ; seul
# le `ForChoiceAbility` imbrique portait un label. Mesure : un label pose sur une
# ability imbriquee ne livre PAS la capacite aux statuts. Sonne et Desoriente
# ecoutent `AfterPlayerTriggerAbility(label=...)` sur l'ability JOUEE
# (`cards/pack/status/`), et la carte passait donc en force. Modele : la carte
# OFFICIELLE 18004 Crosscounter, meme forme, qui pose ses trois labels imprimes
# sur l'ability principale.


def GetAbilities() -> Sequence['Ability']:

    def quack_attack(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)

        message.PreventDamage(2, effect)

        valeur = NombreDeManigancesEnVictoire(effect)
        if valeur <= 0:
            return

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        def frapper(targets: Sequence['CardFace']) -> None:
            if targets:
                this.DealDamage(targets, valeur, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 1 damage to an enemy for each side scheme in the victory display",
                frapper,
            ).SetLabel('attack').SetTarget(Enemy),
        )

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            quack_attack,
        ).SetPlay().SetLabel('attack', 'defense'),
    ]
