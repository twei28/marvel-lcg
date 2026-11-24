from . import *

# Sentry's Grasp — ATTACHEMENT de scenario (Kree Sentry), DEUX exemplaires (mis de cote). CONDITION. Aucun cout.
# Attached character cannot thwart or scheme and can only attack Kree Sentry or this card.
# Any player can attack this card as if it were a minion. If there is 3 or more damage here, set Sentry's Grasp aside.
# Forced Interrupt: When this card would leave play, set it aside instead.
#
# Cartes de reference :
#  - « Any player can attack this card as if it were a minion », degats sur la carte, seuil de degats : modele OFFICIEL
#    54035 Encased in Ice (`ThisGainKeyword(consider_as=(trait, ..))` + `IfCardHasOrMoreCounters(.., 'damage', ..)`) ;
#    ⚠ considere comme ENEMY (cible de l'attaque de base : `SetTarget(Enemy)`) et NON comme Minion, contrairement a 54035 :
#    `Worlds.GetOnFieldMinions` testait `Minion.IsType` et rendait la Poigne, dont Teamwork (can_teamwork.py) lisait
#    `.teamwork` -> AttributeError sur l'attachement (mesure du 20/10/2026, Loyal Devotion + deux sbires IMPERIAL GUARD) ;
#    le seuil est dynamique (`at_least` accepte une fonction) car Death Grip (gs085) le porte a 5.
#  - « can only attack Kree Sentry or this card » : `CheckIfUnitCanBeAttackBy` + `SetCannotBeAttack`, memes
#    messages que `UnitCannotAttackTarget` (54035 : `can_only_attack="This"`) ; la fabrique n'accepte qu'UNE
#    designation, on ecrit donc la capacite (cible = ni Kree Sentry ni cette carte).
#  - « cannot thwart » : `UnitCannotThwartTarget("AttachedCharacter", cannot_thwart=True)` (modele 03028).
#  - « cannot ... scheme » : un personnage de joueur ne manigance pas ; sur un SBIRE le livret p.9 precise « that minion
#    cannot activate for a scheme or attack » -> `EnemyCannotActivate("AttachedEnemy")` (modele 49007 / 60113b).
#  - « When this card would leave play, set it aside instead » : `WhenCardWouldLeavePlay(ForcedInterrupt, "This")` +
#    `SetBeInstead` + `Faces.SetAside` (modele 37034 pour l'interruption de depart).
#
# ⚠ Mots-pieges : « can ONLY attack Kree Sentry OR THIS card » (pas une autre Poigne, pas un sbire) ; « scheme »
# n'existe pas pour un joueur (aucune restriction a coder) mais vaut pour un sbire porteur ; « as if it were a MINION »
# = seulement pour l'ATTAQUE (livret p.9) : les cartes et capacites qui visent un sbire sans attaquer ne peuvent pas la
# viser (`refuse_target_fn`, point d'accroche du selecteur, modele squirrel_girl) ; « set it aside INSTEAD » : le depart
# vers la defausse est remplace, jamais double ; le seuil de degats lit Death Grip EN JEU (3 sinon 5).


def GetAbilities() -> Sequence['Ability']:

    def ni_sentry_ni_cette_carte(effect: 'Effect', message: 'Message.CheckIfUnitCanBeAttackBy') -> bool:
        cible = message.being_attack
        return not (cible.IsName(SENTRY) or cible is effect.this)

    def porteur_attaque(effect: 'Effect', message: 'Message.CheckIfUnitCanBeAttackBy') -> bool:
        return Condition.CheckWhichCard("AttachedCharacter", message.attacker, effect)

    def interdire(effect: 'Effect', message: 'Message.CheckIfUnitCanBeAttackBy') -> None:
        message.SetCannotBeAttack(effect)

    def mettre_de_cote(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> None:
        Unused(message)
        Faces.SetAside([effect.this], effect)

    def sort_ailleurs_qu_en_reserve(effect: 'Effect', message: 'Message.WhenCardWouldLeavePlay') -> bool:
        reserves = [effect.world.aside_deck] + [j.set_aside_deck for j in effect.world.const_players]
        return not any(message.into_area is r for r in reserves)

    def a_la_place(effect: 'Effect', message: 'Message.WhenCardWouldLeavePlay') -> None:
        message.SetBeInstead(effect)
        Faces.SetAside([effect.this], effect)

    def seulement_les_attaques(effet_cible: 'Effect') -> bool:
        """Vrai = la Poigne REFUSE d'etre choisie. Seules les attaques (capacite de base ou etiquetee `attack`) la
        visent."""
        ability = getattr(effet_cible, "ability", None)
        if ability is None:
            return True
        return not (ability.IsLabel('attack') or ability.IsFunction("ATK"))

    def installer_le_refus(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Unused(message)
        effect.this.refuse_target_fn = seulement_les_attaques

    return [
        AbilityFactory.AfterCardEnterPlay(AbilityType.NonKeyword, "This", installer_le_refus),
        *AbilityFactory.UnitCannotThwartTarget("AttachedCharacter", cannot_thwart=True),
        AbilityFactory.EnemyCannotActivate(AbilityType.NonKeyword, "AttachedEnemy"),
        Ability(
            AbilityType.NonKeyword,
            Message.CheckIfUnitCanBeAttackBy,
            [porteur_attaque, ni_sentry_ni_cette_carte],
            interdire,
        ),
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui: 1,
            consider_as=("CONDITION", Enemy),
        ),
        AbilityFactory.IfCardHasOrMoreCounters(
            "This",
            SeuilDeLaPoigne,
            'damage',
            mettre_de_cote,
        ),
        AbilityFactory.WhenCardWouldLeavePlay(
            AbilityType.ForcedInterrupt,
            "This",
            a_la_place,
            conditions=[sort_ailleurs_qu_en_reserve],
        ),
    ]
