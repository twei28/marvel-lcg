from . import *

# Just a Ricochet — evenement d'aspect PROTECTION, x1. DEFENSE. Cout 1,
# ressource [physical].
# Play only if you control an [[ARMOR]] upgrade.
# Hero Response (attack): After your hero makes a basic defense and takes no
#   damage, deal damage to an enemy equal to your hero's DEF.
#
# Cartes de reference :
#  - **`bt001a`** * Beast : « When you take 0 damage when defending » —
#    `AfterUnitDefendAgainstAttack(type, "You", op, take_no_damage=True)`.
#    Le drapeau existait deja (do_attack.py:294) mais AUCUNE carte officielle
#    ne l'employait avant le portage Beast du 1/9/2026.
#  - `SetPlay(only_if_you_control_face=CardFinder(...))` (ability.py:618) pour
#    « Play only if you control an [[ARMOR]] upgrade », modele des cartes a
#    condition de mise en jeu (`58034`, `29034`).
#  - `05015` Tackle / `ho003` pour le libelle `('attack')`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « and **takes no damage** » : 0 degat SUBI, pas « aucune attaque ».
#    `take_no_damage=True` lit `message.taken_damage == 0`. Sans lui, la
#    carte se declencherait sur toute defense.
#  - « **your hero** » : la face heros, pas un allie qui defend. `"You"`
#    resout sur l'identite, et l'evenement est de toute facon une
#    `HeroResponse`.
#  - « equal to your hero's **DEF** » : la DEF COURANTE au moment de la
#    resolution, bonus compris (as002b la baisse de 1, as017 la monte de 3).
#    Lire `heros.defense`, jamais la valeur imprimee.
#  - « **an** enemy » : un ennemi au choix, pas forcement l'attaquant. C'est
#    la difference exacte avec as016, qui ecrit « the attacking enemy ».
#  - « an [[ARMOR]] **upgrade** » : le trait ARMOR sur une AMELIORATION.
#    Deux cartes du pack le portent : `as002a/b` Spider Armor et `as013`
#    Vibranium Enhancement. La condition est verifiee A L'ANNONCE.
#  - ⚠ ECART ASSUME : « makes a **basic** defense » ne se distingue pas d'une
#    defense declaree par une autre carte — `Message.AfterUnitDefendEnd`
#    n'expose aucun drapeau pour ca. Toute defense du heros a 0 degat
#    declenche donc la carte. Signale plutot que masque.


def GetAbilities() -> Sequence['Ability']:

    def just_a_ricochet(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        heros = message.defender
        if heros is None:
            return
        degats = heros.defense
        if degats <= 0:
            return
        this.DealDamage(effect.targets, degats, effect)

    return [
        AbilityFactory.AfterUnitDefendAgainstAttack(
            AbilityType.HeroResponse,
            "You",
            just_a_ricochet,
            take_no_damage=True,
        ).SetPlay(only_if_you_control_face=CardFinder(card_type=Upgrade, trait="ARMOR"))
        .SetLabel('attack')
        .SetTarget(Enemy),
    ]
