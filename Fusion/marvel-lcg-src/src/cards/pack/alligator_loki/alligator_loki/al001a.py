from . import *

# * Alligator Loki — FACE HEROS. ASGARD. CREATURE.
# CTR 2 / ATQ 2 / DEF 1, main 5, 9 PV.
#
# Attached enemy gets -1 SCH and -1 ATK.
# Lock Jaws — Interrupt: When Alligator Loki makes a basic attack or defense
#   against an enemy, attach Alligator Loki to that enemy.
# Forced Response: After attached enemy activates, detach Alligator Loki.
#
# PV/ATQ/CTR/DEF/main sont lus NATIVEMENT dans `desc` : rien a coder.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - malus continu a UNE carte designee dynamiquement : `GiveKeywordToInPlay
#   WhenApplyThis(CardFinder(...), scheme=-1, attack=-1)`, le montage de ho005
#   et an002. Le filtre `check_effect_fn` (finder.py:217) permet de viser « la
#   carte a laquelle CE heros est accroche », ce qu'aucun filtre statique ne
#   sait exprimer.
# - Interrupt sur un pouvoir de BASE : 19005 et dd010, qui accrochent
#   `WhenUnitWouldAttack` / la defense pour un effet au moment de l'usage.
# - « After <ennemi> activates » : `AfterEnemyActivationEnd`, deja employe par
#   bt004 (pack beast) pour agir a la fin de l'activation d'un ennemi.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « ATTACHED enemy » -> l'ennemi tenu, et lui seul. Pas « chaque ennemi », pas
#   « l'ennemi engage ». D'ou le filtre par identite d'objet (`is`), jamais par
#   nom : le vilain et un sbire peuvent partager un nom (lecon « He's Mine! »).
# « makes a BASIC attack or defense » -> les deux pouvoirs, et seulement les
#   pouvoirs DE BASE. Une attaque d'evenement (al003 Chomp!) n'est PAS un
#   pouvoir de base : Chomp! porte donc sa propre clause d'accrochage, ce qui
#   serait redondant si ce declencheur-ci couvrait aussi les evenements.
# « AGAINST AN ENEMY » -> une defense contre un ennemi. Le moteur n'a pas de
#   defense sans attaquant, mais l'attaquant peut etre absent du message
#   (`message.attacker is None`) : on ne s'accroche alors a rien.
# « Interrupt » nu, pas « Forced » -> le joueur PEUT refuser de mordre.
#   `forced=False` sur le choix.
# « After attached enemy ACTIVATES » -> toute activation, attaque OU manigance,
#   d'ou `AfterEnemyActivationEnd` et non `AfterUnitAttackEnd`.
# « Forced Response » -> le joueur ne peut pas REFUSER le declencheur, mais
#   « detach » reste un detachement ordinaire : Unbreakable Grip (al013,
#   « when you WOULD detach ... exhaust instead ») est un effet de
#   remplacement, et un effet de remplacement s'applique aussi a un effet
#   force. C'est meme sa raison d'etre : l'activation de l'ennemi est LE
#   detachement que la Grip est faite pour empecher. D'ou `DetacherLeHeros`
#   sans `force`, qui ouvre la fenetre de la Grip. (Premiere version : `force=
#   True`, rendant la Grip inutile ; corrige le 01/09/2026.)


def GetAbilities() -> Sequence['Ability']:

    def mordre(effect: 'Effect', ennemi: 'CardFace|None') -> None:
        if ennemi is None or not Enemy.IsType(ennemi):
            return
        joueur = effect.GetInitiator()

        def accrocher(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            AccrocherLeHeros(effect, ennemi, joueur)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Lock Jaws: attach Alligator Loki to that enemy",
                accrocher,
            ).SetHasNoTargetEffect(),
            forced=False,
        )

    def lock_jaws_attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        # `attacked_targets` est une LISTE : une attaque de base ne vise qu'un
        # ennemi, on prend donc le premier, mais jamais en supposant qu'il y en
        # ait un.
        cibles = list(message.attacked_targets or [])
        mordre(effect, cibles[0] if cibles else None)

    def lock_jaws_defense(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        mordre(effect, message.attacker)

    def lacher_prise(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        # « After ATTACHED enemy activates » : on ne lache que si c'est bien
        # l'ennemi tenu qui vient de s'activer. L'ennemi est `message.trigger`
        # (sender_enemy.py:141, `TriggerUnitMessage`) ; `message.this`
        # n'existe pas sur ce message (AttributeError au harnais, 01/09/2026).
        if not EstAccrocheA(effect, message.trigger):
            return
        DetacherLeHeros(effect)

    return [
        # « Attached enemy gets -1 SCH and -1 ATK. »
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            # ⚠ `CardFinder` et non `CardFinder2` : le second ne prend que
            # `trait` et `card_type` (finder.py:391), il ignore tout predicat.
            CardFinder(
                card_type=Enemy,
                check_effect_fn=lambda effect, face: EstAccrocheA(effect, face),
            ),
            scheme=-1,
            attack=-1,
            # ⚠ Sans `change_on_event`, la liste des cibles n'est recalculee
            # qu'a l'entree en jeu d'un ennemi : l'accrochage, qui survient
            # bien apres, ne rafraichissait rien et l'ennemi tenu gardait ses
            # valeurs imprimees (harnais, 01/09/2026). `AttachHeroTo` et
            # `DetachHero` (identity.py) emettent `AfterCardAttachTo` /
            # `AfterCardDetachFrom` avec CE heros pour trigger : c'est
            # exactement ce qu'ecoute `OnEvent.AttachedMove("This")`.
            change_on_event=OnEvent.AttachedMove("This"),
        ),
        # ⚠ `is_basic_attack=True` / `is_basic_defense=True` : c'est ce drapeau,
        # et lui seul, qui rend « makes a BASIC attack or defense ». Sans lui,
        # une attaque portee par un evenement declencherait aussi, et la clause
        # d'accrochage propre a Chomp! (al003-al006) n'aurait plus de sens.
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.Interrupt,
            "This",
            lock_jaws_attaque,
            is_basic_attack=True,
        ).SetName("Lock Jaws"),
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.Interrupt,
            "This",
            lock_jaws_defense,
            is_basic_defense=True,
        ).SetName("Lock Jaws"),
        AbilityFactory.AfterEnemyActivationEnd(
            AbilityType.ForcedResponse,
            Enemy,
            lacher_prise,
        ),
    ]
