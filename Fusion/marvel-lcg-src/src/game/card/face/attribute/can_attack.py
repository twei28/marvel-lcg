from . import *

@dataclass
class AttackProperty(PowerProperty):
    additional_boost_card: int = field(default=0) # Only for basic attack
    do_not_give_boost: bool = field(default=False)

    overkill: bool = field(default=False)
    ranged: bool = field(default=False) # ignore retaliate
    piercing: bool = field(default=False) # discard tough
    other_characters_cannot_defend: bool = field(default=False)
    must_defend_with_ally: bool = field(default=False)
    deal_indirect_damage: bool = field(default=False)
    ignore_retaliate: bool = field(default=False)
    lost_piercing: bool = field(default=False)
    attack_in_event: bool = field(default=False) # "08004"
    divide_damage_among_each_character_attacked_player_control: bool = field(default=False) # "31031"

    against_player: 'Player|None' = field(default=None)

    would_act_message: 'Message.WhenEnemyWouldActivate|None' = field(default=None)

    def HasKeyWord(self):
        return self.overkill or self.ranged or self.piercing

    def GetDamage(self, this: 'CardFace') -> int:
        value = 0
        if self.divided_evenly:
            value = 0
        elif self.is_basic_power:
            if HasAttack.IsType(this):
                value = this.attack
        return self.additional_value + value

################################################################################
#
class HasAttack(HasAttribute):
    @override
    def __init__(self, paper: 'Paper') -> None:
        self.base_attack = 0

        self.printed_attack = 0
        self.printed_attack_consequential_damage = 0

        super().__init__(paper)

        def parse(value: str):
            if '*' in value:
                consequential_damage = value.count('*')
                self.printed_attack_consequential_damage = consequential_damage
                value = value.replace('*', '')
            self.printed_attack = int(value)
        self.RegisterAttribute("ATK", parse)
        self.RegisterInfoDict('attack')

    @final
    @property
    def attack(self) -> int:
        # After all active modifiers have been taken into account, if a value is below zero, it is treated as zero: a card cannot have “negative” icons, attributes, traits, cost, or keywords.
        return max(0, self.GetKeyword('ATK'))

    @override
    def OnResetKeywords(self, by_effect: 'Effect'):
        self.base_attack = self.printed_attack
        self.GainAttack(self.base_attack, by_effect)
        return super().OnResetKeywords(by_effect)

    @final
    def GainAttack(self, diff: int, by_effect: 'Effect', *, render_ui: bool=False) -> None:
        self.GainKeyword(diff, 'ATK', by_effect, render_ui=render_ui)

    @final
    def SetBaseAttack(self, value: int, by_effect: 'Effect') -> None:
        if self.base_attack != value:
            diff = value - self.base_attack
            self.base_attack = value
            self.GainAttack(diff, by_effect)

################################################################################
#
class CanAttack(CardFace):

    @staticmethod
    def OnDealDamageInternal(this: 'Unit2|CanAttack', units: List['Unit2'], damage: 'int|DamageProperty', by_effect: 'Effect', *, property: 'AttackProperty|None'=None, attack_in_event: bool) -> int|None:
        has_damage = True

        if attack_in_event or by_effect.ability.is_like_attack:
            if not property:
                property = AttackProperty(is_basic_power=False, attack_in_event=attack_in_event)
            if isinstance(damage, int):
                damage = DamageProperty(damage)
            property.additional_value = damage.damage
            attack_message = CanAttack.SpecialAttack(this, units, by_effect, property=property)
            if attack_message:
                total_damage = attack_message.total_dealt_damage
                has_damage = True
            else:
                total_damage = 0
            if has_damage:
                return total_damage
            else:
                return None
        else:
            # boost damage
            return this.DefaultDealDamageTo(this, units, damage, by_effect)

    @override
    def OnDealDamage(self, units: List['Unit2'], damage: 'int|DamageProperty', by_effect: 'Effect', *, property: 'AttackProperty|None'=None, attack_in_event: bool) -> int|None:
        # Fix "44013"
        # Fix "40038"
        # if not self.IsInPlay():
        #     return None
        return CanAttack.OnDealDamageInternal(self, units, damage, by_effect, property=property, attack_in_event=attack_in_event)

    ################################################################################
    #
    @staticmethod
    def AttackInternal(this: 'Unit2|CanAttack', units: List['Unit2'], by_effect: 'Effect',
                        *, property: 'AttackProperty',
                        if_this_defeat_unit: Callable[['CardFace'], None]|None=None,
                        ) -> Message.AfterUnitAttackEnd|None:
        from game.message import Message
        from game.card.face.base import Unit2
        from game.card.face.attribute.can_boost import CanBoost
        from game.card.face.base import Enemy
        from game.effect.rule import GameRule
        from game.operate.worlds import Worlds
        from game.operate.effects import Effects

        def gain_value_when_divided_for_this_target(gain_value_message: 'Message.WhenUnitBeingAttack|Message.WhenUnitWouldAttackUnit') -> int:
            if gain_value_message.gain_atk > 0 and property.is_divided:
                return gain_value_message.gain_atk
            return 0

        def gain_value_when_divided(gain_value_message: 'Message.WhenUnitWouldAttack'):
            if gain_value_message.gain_atk > 0 and property.is_divided:
                gain_value = gain_value_message.gain_atk
                player = unit.GetControlByPlayer()
                new_added_targets = player.AskChooseFaces(units, (gain_value, gain_value), GameRule(unit), prompt="Assign", repeat_rules="Any")
                for check_unit in new_added_targets:
                    if Unit2.IsType(check_unit):
                        gain_value_message.AddTarget(check_unit)

        is_base_attack = property.is_basic_power
        world = this.card.world
        this = this.card.CastTo(Unit2)

        # ANNONCE de l'activation (fait d'INTENTION, lu par ui-app).
        #
        # « Klaw va attaquer Colossus », AVANT que le coup soit resolu. Sa
        # place est le sujet meme de la correction : elle part ICI, juste avant
        # `WhenUnitWouldAttack`, parce que c'est ce message-la qui ouvre la
        # fenetre ou le joueur peut interrompre, et `WhenUnitBeingAttack` (plus
        # bas, dans la boucle) celle ou il peut defendre. Une intention posee
        # apres eux arriverait apres les questions, donc trop tard pour que le
        # cartouche montre ce qui va se passer pendant qu'on y repond.
        #
        # Les cartes de boost sont retournees ENTRE les deux temps : l'annonce
        # ne les porte pas, le fait resolu oui.
        #
        # `annonce_id` vaut 0 des qu'il n'y a rien a annoncer (l'attaquant
        # n'est pas un ennemi, ce n'est pas une attaque de base, aucune cible) :
        # tout ce qui suit devient alors sans effet.
        annonce_cible = units[0] if units else None
        annonce_base = this.attack if HasAttack.IsType(this) else 0
        annonce_id = CanAttack.AnnoncerActivation(
            this, annonce_cible, 'attaque', annonce_base,
            is_base_attack, by_effect,
        )

        def cloturer_annonce_non_resolue(par: 'Effect|None' = None) -> None:
            """L'attaque annoncee n'a pas eu lieu : on ferme l'intention.

            Sans cette cloture, le cartouche resterait sur « Klaw va attaquer
            Colossus » jusqu'a la fin de la phase. Le fait de cloture porte le
            MEME identifiant, donc il remplace l'intention au lieu de s'ajouter.
            """
            nonlocal annonce_id
            if not annonce_id:
                return
            identifiant, annonce_id = annonce_id, 0
            CanAttack.AnnulerActivation(this, annonce_cible, 'attaque', identifiant, by_effect, par)

        # Q: If Ebony Maw is prevented from attacking or scheming by a status card, he removes the status gard instead of resolving his activation.
        would_atk_message = Message.WhenUnitWouldAttack(this, units, by_effect, property=property)
        would_atk_message.Send()
        if would_atk_message.is_be_instead:
            cloturer_annonce_non_resolue(would_atk_message.be_instead_by)
            return None

        if Enemy.IsType(this):
            activate_message = Message.WhenEnemyActivateAgainstYou(this, property.against_player, by_effect, would_atk_message, property.would_act_message)
            activate_message.Send()
        else:
            activate_message = None

        if is_base_attack:
            unit = this.card.CastTo(Unit2)
            use_basic_power_message = Message.WhenUnitUseBasicPower(unit, "ATK", would_atk_message)
            use_basic_power_message.Send()
        else:
            use_basic_power_message = None

        # We not check for `use_basic_power_message` as it make `would_atk_message` update gain_atk
        # And that's why we check `would_atk_message` after it
        gain_value_when_divided(would_atk_message)

        is_not_delay = activate_message or use_basic_power_message or not by_effect.ability.IsLabel('attack')

        attacked_targets: List['CardFace'] = []
        damage_targets: List['Unit2'] = []
        total_dealt_damage = 0
        atk_end_messages: List['Message.AfterUnitAttackUnit|Message.AttackEndsBeforeDamageDealt'] = []

        from game.operate.faces_helper import FacesHelper
        unit_dict = FacesHelper.ListToDict(would_atk_message.attacked_targets)

        divided_rest_damage = this.attack if HasAttack.IsType(this) else 0
        if unit_dict:
            divided_evenly_damage = int(divided_rest_damage / len(unit_dict) + .5)
        else:
            divided_evenly_damage = 0

        temp_effects: List['Effect'] = []
        if if_this_defeat_unit:
            from game.ability.factory import AbilityFactory
            temp_effects += this.effect.RegisterTemp(
                AbilityFactory.AfterUnitDefeatedUnit(
                    AbilityType.Temp0,
                    "This",
                    None,
                    lambda effect, message:
                        if_this_defeat_unit(message.target),
                    is_from_attack=True,
                ),
                unregister_after_exec=False
            )

        basic_defense_messages: List['Message.AfterUnitDefenseInternal'] = []
        attacker_is_defeated = 0

        for target in unit_dict:

            gain_divided_attack = 0

            # L'annonce ne vaut que pour la cible ANNONCEE. Une redirection, ou
            # une seconde cible dans la meme attaque, ferme l'intention en
            # cours : elle n'a rien anticipe de ce coup-ci, et la resolution qui
            # vient repartira d'un identifiant neuf.
            if annonce_id and annonce_cible is not None and \
                target.card.object_id != annonce_cible.card.object_id:
                cloturer_annonce_non_resolue()

            if not this.IsInPlay():
                break

            this = this.card.CastTo(Unit2)

            if not Unit2.IsType(target):
                continue

            if is_base_attack and not property.do_not_give_boost:
                can_boost = this
                if CanBoost.IsType(can_boost):
                    can_boost.GiveFacedownBoostCardsInternal(can_boost.GetBoostCardNum(would_atk_message) + property.additional_boost_card, GameRule(this), would_atk_message)

            # choose defender
            being_atk_message = Message.WhenUnitBeingAttack(target, would_atk_message)
            being_atk_message.Send()
            gain_divided_attack = gain_value_when_divided_for_this_target(being_atk_message)
            defender = being_atk_message.defender
            defense_messages = being_atk_message.defense_messages
            basic_defense_messages += [x for x in defense_messages if x.use_basic_power_message]

            defense = 0
            if defense_messages and defender:
                for defense_message in defense_messages:
                    defense += defense_message.property.GetDefense(defender)

            attacked_you = None
            def update_atk_target(target: 'Unit2'):
                nonlocal attacked_you
                attacked_you = target.GetControlByOrOwner()
                return target

            if defender:
                atk_target = update_atk_target(defender)
            else:
                atk_target = update_atk_target(target.card.CastTo(Unit2))

            if not this.IsInPlay():
                atk_end_message = Message.AttackEndsBeforeDamageDealt(this, atk_target, being_atk_message)
                atk_end_messages.append(atk_end_message)
                break

            # Put this after check is in play to Fix "27012" vs "01140"
            this = this.card.CastTo(Unit2)

            would_attack_unit_message = Message.WhenUnitWouldAttackUnit(this, atk_target, being_atk_message)
            would_attack_unit_message.Send()
            gain_divided_attack = gain_value_when_divided_for_this_target(would_attack_unit_message)
            atk_target = update_atk_target(would_attack_unit_message.target)

            # If the target of an ally’s basic power leaves play
            # before that ally deals damage equal to its ATK or
            # removes threat equal to its THW, the ally does not
            # take consequential damage
            if atk_target.IsDefeated():
                # Fix "40097"
                # If the defending ally leaves play prior to damage
                # from the attack being dealt, the attack is
                # considered to have no character defending
                if Enemy.IsType(atk_target):
                    continue

            boost_cards: List['CardFace'] = []
            # Ce que CHAQUE carte de boost a ajoute. `boost_cards` seule ne le
            # dit pas, et c'est pourtant la moitie de l'information : « 5 degats
            # (3 de base + 2 de boost) » ne se reconstitue pas apres coup.
            boost_apports: List[Tuple[str, int, int]] = []

            if is_base_attack:
                # We resolve boost first to
                # Fix "27073" attack "27078" as boost
                # assert property.base_value == self.attack

                if CanBoost.IsType(this):
                    def gain_att(face: CardFace, boost_value: int) -> None:
                        attacker = this.card.CastTo(Unit2)
                        nonlocal boost_cards
                        boost_cards.append(face)
                        boost_apports.append((face.name, face.card.object_id, boost_value))
                        attacker.GainForThisActive(
                            GameRule(face),
                            would_atk_message,
                            attack=boost_value,
                            render_ui=True
                        )
                    this.ResolveBoostCards(being_atk_message, gain_att)
                    if Worlds.IsGameOver(by_effect):
                        cloturer_annonce_non_resolue()
                        return None

                this = this.card.CastTo(Unit2)
                assert CanAttack.IsType(this), f"{this=}"

                if being_atk_message.defender:
                    atk_target = update_atk_target(being_atk_message.defender)

                if defender and defender.IsDefeated():
                    defense = 0
                    atk_target = update_atk_target(target)

            has_keyword_message = Message.CheckIfAttackMessageHasKeyword(would_attack_unit_message, by_effect)
            has_keyword_message.Send()
            Unused(has_keyword_message)

            if would_attack_unit_message.HasKeywords():
                keywords_attack_message = Message.WhenUnitMakeKeyWordAttack(this, would_attack_unit_message)
                keywords_attack_message.Send()

            if is_base_attack:
                this = this.card.CastTo(Unit2)
                if property.is_divided:
                    damage = 1
                elif property.divided_evenly:
                    damage = property.GetDamage(this) + divided_evenly_damage
                    divided_rest_damage -= divided_evenly_damage
                    if divided_rest_damage <= divided_evenly_damage:
                        divided_evenly_damage = divided_rest_damage
                else:
                    damage = property.GetDamage(this)
                value = unit_dict[target] * damage + would_attack_unit_message.temp_additional_value + gain_divided_attack
                recalculate = Message.WhenRecalculateAttackDamage(this, atk_target, value, would_atk_message)
                recalculate.Send()
                calculated_damage = recalculate.will_take_damage
            else:
                calculated_damage = unit_dict[target] * property.GetDamage(this) + would_attack_unit_message.temp_additional_value
                recalculate = Message.WhenRecalculateAttackDamage(this, atk_target, calculated_damage, would_atk_message)
                recalculate.Send()
                calculated_damage = recalculate.will_take_damage

            # LA VALEUR AVANT DEFENSE, retenue pour le journal du bilan.
            #
            # C'est la seule qui redonne le calcul que le joueur refait a la
            # main : `base + boost - defense = inflige`. La deduire apres coup
            # etait faux deux fois — `inflige` est plafonne a zero (une defense
            # superieure a l'attaque rendait une base trop grande), et la
            # valeur imprimee lue a la declaration ne connait ni
            # `additional_value` (applique par le constructeur de
            # `WhenUnitWouldAttack`), ni `temp_additional_value`, ni
            # `WhenRecalculateAttackDamage`. Ici, tout est deja compte.
            total_avant_defense = calculated_damage
            calculated_damage = max(0, calculated_damage - defense)

            # Le personnage qui defend VRAIMENT ce coup (un defenseur vaincu
            # avant les degats ne defend plus : `defense` vient d'etre remise a
            # zero plus haut). Le fait `boosts` et le fait resolu le nomment.
            defenseur_retenu = CanAttack._DefenseurRetenu(being_atk_message.defender or defender)

            # ETAT INTERMEDIAIRE de l'activation (fait `boosts`, lu par ui-app,
            # 04/10/2026). Le defenseur est choisi, les boosts sont retournes,
            # les degats ne sont pas encore tombes : le cartouche montre « Rhino
            # ATQ 2 + 1 boost, Spider-Man defend » pendant ce temps-la. Meme
            # identifiant que l'annonce, qu'il REMPLACE ; le fait resolu le
            # remplace a son tour. Seulement tant que l'annonce vit.
            CanAttack.JournaliserBoosts(
                this, target, 'attaque', annonce_id, annonce_base, defenseur_retenu,
                defense, boost_apports, boost_cards, total_avant_defense, by_effect,
            )

            # unit_health = target.health

            excess_damage = 0
            if would_attack_unit_message.IsPiercing():
                if atk_target.IsTough():
                    atk_target.DiscardTough(by_effect, rule="All")

            from game.card.face.card_type import Ally
            from game.card.face.card_type import Minion

            overkill_target = None
            damaged_overkill_target = None
            if would_attack_unit_message.IsOverKill():
                if Minion.IsType(atk_target):
                    overkill_target = Worlds.FindVillain(by_effect)
                elif Ally.IsType(atk_target):
                    overkill_target = atk_target.GetControlByPlayer().GetIdentity()

            took_damage_targets: List['Unit2'] = []

            # Send.WhenUnitAttacksUnit(target, calculated_damage, atk_message)
            if property.deal_indirect_damage:
                #  and atk_target == atk_target.GetControlByPlayer().GetIdentity():
                damage_messages = atk_target.TakeIndirectDamage(this, calculated_damage, by_effect, from_atk_message=would_atk_message)
                took_damage = 0
                for damage_message in damage_messages:
                    took_damage += damage_message.took_damage
                    took_damage_targets.append(damage_message.who_took_damage)
            elif property.divide_damage_among_each_character_attacked_player_control and \
                atk_target.GetControlByOrOwner().IsPlayer():
                assert property.against_player
                player_units = atk_target.GetControlByPlayer().GetControlCharacters()
                divide_damage, divide_remainder = Math.DivideEvenly(calculated_damage, player_units)
                if divide_remainder:
                    remainder_units = property.against_player.AskChooseFaces(player_units, (divide_remainder, divide_remainder), by_effect)
                else:
                    remainder_units = []

                divide_damage_messages: List['Message.AfterUnitDefeatedUnit|Message.AfterUnitTookDamage|None'] = []
                for divide_target in player_units:
                    if divide_target in remainder_units:
                        deal_divide_damage = 1+divide_damage
                    else:
                        deal_divide_damage = divide_damage
                    if deal_divide_damage:
                        divide_damage_messages.append(divide_target.TakeDamage(this, deal_divide_damage, by_effect))

                took_damage = 0
                excess_damage = 0
                for damage_message in divide_damage_messages:
                    if damage_message:
                        took_damage += damage_message.took_damage
                        excess_damage += damage_message.excess_damage
                        if took_damage > 0:
                            took_damage_targets.append(damage_message.who_took_damage)
                    else:
                        took_damage += 0
                        excess_damage += 0
            else:
                # original_health = atk_target.health
                damage_messages = atk_target.TakeDamageWithOverkillTarget(this, calculated_damage, by_effect, would_attack_unit_message, overkill_target)
                if damage_messages:
                    took_damage = damage_messages[0].took_damage
                    excess_damage = damage_messages[0].excess_damage
                    if took_damage > 0:
                        took_damage_targets.append(damage_messages[0].who_took_damage)
                    damaged_overkill_target = damage_messages[0].damaged_overkill_target
                    if damaged_overkill_target:
                        took_damage_targets.append(damaged_overkill_target)
                else:
                    took_damage = 0
                    excess_damage = 0

            # Fix facedown DRONE
            if atk_target.card.face != atk_target and Unit2.IsType(atk_target.card.face):
                atk_target = update_atk_target(atk_target.card.CastTo(Unit2))

            attacked_targets.append(atk_target)
            total_dealt_damage += calculated_damage

            if is_not_delay:
                retaliate_message = atk_target.ResolveRetaliate(would_attack_unit_message)
                attacker_is_defeated += retaliate_message != None and isinstance(retaliate_message, Message.AfterUnitDefeatedUnit)

                if being_atk_message.defense_messages:
                    defend_against_message = Message.AfterUnitDefendEnd(being_atk_message.defense_messages, would_atk_message, calculated_damage, took_damage)
                    defend_against_message.Send()
            else:
                assert being_atk_message.defense_messages == []

            # Journal du bilan de phase (ajout local, lu par ui-app). Il est
            # pose ICI, ou le calcul est encore entier : plus haut il manque le
            # resultat, plus bas les composantes ont disparu dans un total.
            #
            # SOUS GARDE, et sans condition : un journal d'affichage n'a aucune
            # raison de pouvoir interrompre une resolution de combat. S'il
            # echoue, la partie continue et il ne manque qu'une ligne de bilan.
            try:
                journalise = CanAttack.JournaliserActivation(
                    this, atk_target, is_base_attack,
                    boost_apports, defense, calculated_damage, took_damage,
                    by_effect, activation_id=annonce_id,
                    total_avant_defense=total_avant_defense,
                    boost_cards=boost_cards,
                    defenseur=defenseur_retenu, cible_annoncee=target,
                    base_imprimee=annonce_base,
                )
                # L'intention est CONSOMMEE, mais SEULEMENT si un fait resolu a
                # vraiment pris sa place : `JournaliserActivation` a ses propres
                # gardes (l'auteur n'est pas un ennemi, ce n'est pas une attaque
                # de base) et sort alors sans rien inscrire. La remettre a zero
                # dans ce cas laisserait une intention orpheline, que le filet
                # de fin de boucle ne pourrait plus clore.
                if journalise:
                    annonce_id = 0
            except Exception:
                pass

            atk_end_message = Message.AfterUnitAttackUnit(this, atk_target, attacked_you, damaged_overkill_target, took_damage_targets, calculated_damage, took_damage, excess_damage, boost_cards, would_attack_unit_message, being_atk_message.defense_messages)
            if is_not_delay:
                atk_end_message.Send()
            atk_end_messages.append(atk_end_message)

            damage_targets += took_damage_targets

        # Le filet : toutes les sorties de boucle passent par ici (attaquant
        # sorti du jeu, cible vaincue avant les degats, aucune cible retenue).
        # Sans effet quand la resolution a deja consomme l'annonce.
        cloturer_annonce_non_resolue()

        Effects.UnRegister(temp_effects)

        this = this.CastTo(Unit2)
        end_message = Message.AfterUnitAttackEnd(this, attacked_targets, damage_targets, total_dealt_damage, by_effect, atk_end_messages, would_atk_message)

        if is_not_delay:
            end_message.Send()

            if atk_end_messages:
                if activate_message:
                    assert Enemy.IsType(this)
                    after_activate_message = Message.AfterEnemyActivationEnd(this, end_message, activate_message)
                    after_activate_message.Send()

                if use_basic_power_message and \
                    not this.IsDefeated() and \
                    not attacker_is_defeated:
                    unit = this.card.CastTo(Unit2)
                    after_use_basic_power_message = Message.AfterUnitUseBasicPower(unit, "ATK", end_message, use_basic_power_message)
                    after_use_basic_power_message.Send()

                world.stat.RecordAttack(end_message)
            # If an ability triggers after a character uses a basic
            # power, that ability triggers after an attack in which
            # a character made a basic defense resolves.
            for basic_defense_message in basic_defense_messages:
                if basic_defense_message.IsBasicDefense() and basic_defense_message.use_basic_power_message:
                    after_use_def_power_message = Message.AfterUnitUseBasicPower(basic_defense_message.defender, "DEF", basic_defense_message, basic_defense_message.use_basic_power_message)
                    after_use_def_power_message.Send()
        else:
            # For event cards, or "08004"
            by_effect.context.AddAtkMessage(end_message)
        return end_message

    @staticmethod
    def CauseDeLActivation(auteur: 'CardFace', cible: 'CardFace',
                           phase: str, by_effect: 'Effect|None') -> str:
        """Ce QUI a declenche l'activation, quand ce n'est pas la regle du jeu.

        Une carte de rencontre peut faire attaquer le vilain une SECONDE fois
        (Assault : « le vilain vous attaque »). Cette attaque-la parait sortie
        de nulle part si on ne dit pas d'ou elle vient — signale en jeu, « on
        dirait qu'il m'attaque deux fois sans raison ».

        Deux garde-fous, tous deux poses apres coup sur des mesures :

        1. PENDANT l'etape des activations, un ennemi s'active parce que la
           regle le veut : il n'y a pas de cause a nommer.
        2. `by_effect.this` n'est PAS toujours l'origine qu'on cherche. Mesure
           faite sur une partie reelle : pour les activations ordinaires il
           porte le heros vise, ce qui aurait affiche « declenche par Black
           Panther ». On refuse donc un nom qui est celui de l'attaquant ou de
           sa cible : ce sont les deux facons connues de ne rien apprendre.
        """
        if phase == 'Enemy Activation':
            return ''
        source = getattr(by_effect, 'this', None)
        nom = getattr(source, 'name', '')
        if not nom or nom == auteur.name or nom == cible.name:
            return ''
        return nom

    @staticmethod
    def _CauseDe(auteur: 'CardFace', cible: 'CardFace', phase: str,
                 by_effect: 'Effect|None') -> 'Dict[str, Any]':
        """`cause` (le nom, '' quand la regle du jeu suffit) et, quand un nom
        est donne, `cause_id` : l'identifiant de la meme carte (04/10/2026).
        Le plateau range l'attaque sous la carte qui l'a provoquee par cet
        identifiant, sans comparer des noms (deux Stampede, un nom traduit)."""
        nom = CanAttack.CauseDeLActivation(auteur, cible, phase, by_effect)
        if not nom:
            return {'cause': nom}
        source = CanAttack._SourceDe(by_effect, 'cause')
        return {'cause': nom, **({'cause_id': source['cause_id']} if 'cause_id' in source else {})}

    @staticmethod
    def _DefenseurRetenu(defenseur: 'CardFace|None') -> 'CardFace|None':
        """Le defenseur d'un coup, ou None s'il n'y en a pas ou plus (vaincu
        avant les degats). Sous garde : il ne sert qu'au journal d'affichage."""
        try:
            if defenseur is None or defenseur.IsDefeated():
                return None
            return defenseur
        except Exception:
            return None

    @staticmethod
    def JournaliserBoosts(auteur: 'CardFace', cible: 'CardFace|None', genre: str,
                          activation_id: int, base_imprimee: int,
                          defenseur: 'CardFace|None', defense: int,
                          boost_apports: 'List[Tuple[str, int, int]]',
                          boost_cards: 'List[CardFace]|None',
                          total_avant_defense: int,
                          by_effect: 'Effect|None'=None) -> None:
        """Inscrit l'ETAT INTERMEDIAIRE d'une activation (`etat: 'boosts'`).

        Entre l'annonce et la resolution : le defenseur est choisi, les cartes
        de boost sont retournees, rien n'est encore subi. Meme identifiant que
        l'annonce, donc il la REMPLACE a la meme place ; le fait resolu le
        remplace a son tour. Ni `subi` ni `inflige` : ils n'existent pas encore.

        Rien a inscrire sans annonce vivante (`activation_id` nul) : l'appelant
        n'a alors rien annonce, ou l'a deja clos. Sous garde, comme tout ce
        journal d'affichage.
        """
        if not activation_id or cible is None:
            return
        try:
            world = auteur.card.world
            phase = world.GetPhaseText()
            world.stat.RecordFaitMechant(world.round_id, {
                'genre': genre,
                'etat': 'boosts',
                'activation_id': activation_id,
                'phase': phase,
                **CanAttack._CauseDe(auteur, cible, phase, by_effect),
                'auteur': auteur.name,
                'auteur_id': auteur.card.object_id,
                # La cible ANNONCEE, pas le defenseur : le cartouche montre qui
                # etait vise ET qui defend.
                'cible': cible.name,
                'cible_id': cible.card.object_id,
                'defenseur': defenseur.name if defenseur is not None else None,
                'defenseur_id': defenseur.card.object_id if defenseur is not None else None,
                'defense': defense,
                'boosts': CanAttack._BoostsPublies(boost_apports, boost_cards),
                'boost': sum(valeur for _, _, valeur in boost_apports),
                # La valeur que le moteur retranchera de la defense : tout y
                # est deja compte (voir `AttackInternal`).
                'total_avant_defense': total_avant_defense,
                # Ce qui est ecrit sur la carte, celle de l'annonce.
                'base_imprimee': base_imprimee,
            })
        except Exception:
            pass

    @staticmethod
    def AnnoncerActivation(auteur: 'CardFace', cible: 'CardFace|None', genre: str,
                           base: int, is_base_power: bool,
                           by_effect: 'Effect|None'=None) -> int:
        """Inscrit l'INTENTION d'une activation ennemie, et rend son identifiant.

        Rend 0 quand il n'y a rien a annoncer (pas un ennemi, pas une
        activation de base, pas de cible) : l'appelant n'a alors rien a clore
        ni a consommer.

        Le fait ne porte QUE ce qui est connu avant le coup — qui, contre qui,
        et la valeur imprimee. `subi`, `defense`, `restant`, les boosts :
        aucun n'existe encore, et en inventer un serait pire que se taire. Le
        fait de resolution les apportera tous, sous le meme identifiant.

        SOUS GARDE, comme le reste de ce journal : un journal d'affichage n'a
        aucune raison de pouvoir interrompre une resolution de combat.
        """
        from game.card.face.base import Enemy

        if cible is None or not is_base_power or not Enemy.IsType(auteur):
            return 0
        try:
            world = auteur.card.world
            phase = world.GetPhaseText()
            activation_id = world.stat.NouvelleActivation(world.round_id)
            world.stat.RecordFaitMechant(world.round_id, {
                'genre': genre,
                'etat': 'annonce',
                'activation_id': activation_id,
                'phase': phase,
                **CanAttack._CauseDe(auteur, cible, phase, by_effect),
                'auteur': auteur.name,
                'auteur_id': auteur.card.object_id,
                'cible': cible.name,
                'cible_id': cible.card.object_id,
                # La valeur IMPRIMEE : l'attaque ou la manigance de l'auteur
                # avant les cartes de boost, qui ne sont pas encore retournees.
                'base': base,
            })
            return activation_id
        except Exception:
            return 0

    @staticmethod
    def AnnulerActivation(auteur: 'CardFace', cible: 'CardFace|None', genre: str,
                          activation_id: int, by_effect: 'Effect|None'=None,
                          annule_par: 'Effect|None'=None) -> None:
        """Clot une intention qui n'a pas eu de resolution.

        Meme identifiant que l'annonce, donc le fait la REMPLACE : le
        cartouche du plateau voit son etape se completer en « l'attaque n'a pas
        lieu » plutot que de rester sur « va attaquer » jusqu'a la fin de la
        phase.

        Trois facons connues d'y arriver : un « ... instead » qui remplace
        l'activation, une cible qui quitte la table avant les degats, un
        attaquant qui sort du jeu entre-temps.
        """
        if not activation_id or cible is None:
            return
        try:
            world = auteur.card.world
            phase = world.GetPhaseText()
            world.stat.RecordFaitMechant(world.round_id, {
                'genre': genre,
                'etat': 'annule',
                'activation_id': activation_id,
                'phase': phase,
                **CanAttack._CauseDe(auteur, cible, phase, by_effect),
                'auteur': auteur.name,
                'auteur_id': auteur.card.object_id,
                'cible': cible.name,
                'cible_id': cible.card.object_id,
                # « → Annulée par X » (04/10/2026) : la carte dont l'effet a
                # remplace l'activation (Sonne, Desoriente, une carte de joueur).
                **CanAttack._SourceDe(annule_par, 'annule_par'),
            })
        except Exception:
            pass

    @staticmethod
    def JournaliserActivationEmpechee(auteur: 'CardFace', contre: 'Player',
                                      would_act_message: 'Any') -> None:
        """Inscrit un fait `sonne` : un ennemi SONNE s'est vu retirer son
        activation par la carte Sonne (05/10/2026, etat 04 du cartouche).

        `Enemy.DoActivate` s'arrete des que `WhenEnemyWouldActivate` est
        remplace, AVANT l'annonce : ni intention ni cloture n'existaient, et le
        cartouche sautait l'etape sans rien dire. Seule la carte Sonne est
        publiee ici ; une autre cause d'empechement ne change pas ce qu'on
        affichait. Sous garde, comme tout ce journal.
        """
        try:
            par = getattr(would_act_message, 'be_instead_by', None)
            source = getattr(par, 'this', None)
            if getattr(source, 'name', '') != 'Stunned':
                return
            from game.card.face.card_type.minion import Minion
            from game.operate.worlds import Worlds
            from game.player.action.player_action import PlayerAction
            world = auteur.card.world
            temps = 'attaque' if would_act_message.power == 'ATK' else 'manigance'
            cible = contre.GetIdentity() if temps == 'attaque' else Worlds.FindMainScheme(auteur)
            world.stat.RecordFaitMechant(world.round_id, {
                'genre': 'sonne',
                'phase': world.GetPhaseText(),
                'temps': temps,
                'type': 'sbire' if Minion.IsType(auteur) else 'mechant',
                'joueur': PlayerAction._SiegeDuJoueur(contre),
                'auteur': auteur.name,
                'auteur_id': auteur.card.object_id,
                'cible': cible.name if cible is not None else None,
                'cible_id': cible.card.object_id if cible is not None else None,
                # La carte Sonne a-t-elle quitte l'ennemi ? Un ennemi Constant
                # (Steady) en porte deux : la premiere s'en va, il reste Sonne.
                'statut_retire': not auteur.IsStunned(),
                **CanAttack._SourceDe(par, 'annule_par'),
                'fait_id': (f"sonne:{world.round_id}:{auteur.card.object_id}"
                            f":{len(world.stat.faits_mechant)}"),
            })
        except Exception:
            pass

    @staticmethod
    def _BoostsPublies(boost_apports: 'List[Tuple[str, int, int]]',
                       boost_cards: 'List[CardFace]|None') -> 'List[Dict[str, Any]]':
        """Les boosts du fait, et `etoile` sur ceux qui portent une capacite
        Boost (★) : le cartouche lui donne sa ligne sous l'attaque (04/10/2026)."""
        from game.ability import AbilityType
        etoiles: 'Set[int]' = set()
        for face in boost_cards or []:
            try:
                if face.effect.Find(type=AbilityType.Boost):
                    etoiles.add(face.card.object_id)
            except Exception:
                pass
        return [
            {'nom': nom, 'id': object_id, 'apport': valeur,
             **({'etoile': True} if object_id in etoiles else {})}
            for nom, object_id, valeur in boost_apports
        ]

    @staticmethod
    def _SourceDe(effet: 'Effect|None', cle: str) -> 'Dict[str, Any]':
        """`{cle: nom, cle_id: identifiant}` de la carte source d'un effet, ou {}."""
        try:
            source = effet.this if effet is not None else None
            if source is None:
                return {}
            return {cle: source.name, f'{cle}_id': source.card.object_id}
        except Exception:
            return {}

    @staticmethod
    def JournaliserActivation(attaquant: 'CardFace', cible: 'CardFace', is_base_attack: bool,
                              boost_apports: 'List[Tuple[str, int, int]]',
                              defense: int, inflige: int, subi: int,
                              by_effect: 'Effect|None'=None,
                              activation_id: int=0,
                              total_avant_defense: 'int|None'=None,
                              boost_cards: 'List[CardFace]|None'=None,
                              defenseur: 'CardFace|None'=None,
                              cible_annoncee: 'CardFace|None'=None,
                              base_imprimee: 'int|None'=None) -> bool:
        """Inscrit une attaque D'ENNEMI au journal du bilan de phase.

        On ne journalise que les ennemis : ce panneau raconte la phase du
        mechant, et y verser les attaques des heros le rendrait illisible.

        Le calcul est decompose comme le joueur le refait a la main :

            inflige = base + boost - defense

        `total_avant_defense` est la valeur que le moteur a REELLEMENT calculee
        juste avant de retrancher la defense (voir `AttackInternal`). C'est la
        seule source qui satisfasse l'egalite ci-dessus, et il en a fallu deux
        essais pour arriver la :

         - la DEDUCTION (`inflige + defense - boost`) se trompait des que
           `inflige` etait plafonne a zero — mesure du 06/09/2026, Rhino ATQ 2
           contre une defense de 3 journalisait « base 3 » ;
         - la valeur IMPRIMEE lue a la declaration (`this.attack`) ignore tout
           ce qui modifie l'attaque autrement qu'avec une carte de boost :
           `property.additional_value`, applique par le constructeur de
           `WhenUnitWouldAttack`, `temp_additional_value`, `gain_divided_attack`
           et `WhenRecalculateAttackDamage`. Sur un ennemi renforce, elle
           faisait mentir le recap (« N de base » pour une frappe plus forte).

        La valeur imprimee, elle, garde son seul emploi legitime : le fait
        d'INTENTION (`AnnoncerActivation`), qui annonce ce qui est ecrit sur la
        carte parce que rien d'autre n'est encore connu.

        Rend True si un fait a ete inscrit : l'appelant ne consomme son
        intention que dans ce cas.
        """
        from game.card.face.base import Enemy

        if not Enemy.IsType(attaquant) or not is_base_attack:
            return False

        world = attaquant.card.world
        boost_total = sum(valeur for _, _, valeur in boost_apports)
        # L'ETAPE ou l'activation a lieu. Sans elle, une attaque declenchee par
        # une carte revelee se rangeait sous « activations », et le vilain
        # semblait frapper deux fois sans raison.
        phase = world.GetPhaseText()

        world.stat.RecordFaitMechant(world.round_id, {
            'genre': 'attaque',
            # Le fait de RESOLUTION. Il remplace l'intention de meme
            # identifiant (voir WorldStat.RecordFaitMechant) ; sans intention
            # annoncee — une attaque qu'aucun de nos deux sites n'a pu voir
            # venir — il en prend un neuf, pour que TOUTE activation soit
            # identifiee de la meme facon cote client.
            'etat': 'resolu',
            'activation_id': activation_id or world.stat.NouvelleActivation(world.round_id),
            'phase': phase,
            **CanAttack._CauseDe(attaquant, cible, phase, by_effect),
            'auteur': attaquant.name,
            'auteur_id': attaquant.card.object_id,
            'cible': cible.name,
            'cible_id': cible.card.object_id,
            'base': (total_avant_defense - boost_total
                     if total_avant_defense is not None
                     else inflige + defense - boost_total),
            'boost': boost_total,
            'defense': defense,
            'inflige': inflige,
            'subi': subi,
            # Etat de la cible APRES coup. `getattr` parce que toutes les cibles
            # n'ont pas de PV (une carte retournee en cours d'attaque) : le
            # bilan se passe du reste plutot que de faire tomber la resolution.
            'restant': getattr(cible, 'health', None),
            'boosts': CanAttack._BoostsPublies(boost_apports, boost_cards),
            # Cartouche (04/10/2026). `cible` est la carte qui a pris le coup,
            # donc le DEFENSEUR quand il y en a un : le heros VISE est
            # `cible_annoncee`. `base_imprimee` (la valeur de l'annonce) separe
            # de `base` ce qu'un boost ★ ou un renfort a ajoute.
            'defenseur': defenseur.name if defenseur is not None else None,
            'defenseur_id': defenseur.card.object_id if defenseur is not None else None,
            'cible_annoncee': (cible_annoncee or cible).name,
            'cible_annoncee_id': (cible_annoncee or cible).card.object_id,
            'base_imprimee': base_imprimee,
        })
        CanAttack._CompterDefense(cible, defenseur, subi,
                                  total_avant_defense if total_avant_defense is not None else inflige + defense)
        return True

    @staticmethod
    def _CompterDefense(cible: 'CardFace', defenseur: 'CardFace|None', subi: int, attaque: int) -> None:
        """Statistiques de la PARTIE (ecran de fin, 10/10/2026) : ce qu'une
        attaque ennemie n'a PAS fait (DEF, Tough, preventions), compte au joueur
        dont le personnage etait vise, et l'attaque defendue, comptee au joueur
        du defenseur."""
        from engine import Engine
        from game.player import Player
        stats = Engine.game.session.statistics
        if Player.IsType(cible.GetControlBy()):
            stats.AddSiege(cible.GetControlByPlayer(), 'degats_evites', max(0, attaque - subi))
        if defenseur is not None and Player.IsType(defenseur.GetControlBy()):
            stats.AddSiege(defenseur.GetControlByPlayer(), 'attaques_defendues', 1)

    @staticmethod
    def JournaliserManigance(auteur: 'CardFace', manigance: 'CardFace', is_base_scheme: bool,
                             boost_apports: 'List[Tuple[str, int, int]]', pose: int,
                             by_effect: 'Effect|None'=None,
                             activation_id: int=0,
                             boost_cards: 'List[CardFace]|None'=None,
                             cible_annoncee: 'CardFace|None'=None,
                             base_imprimee: 'int|None'=None) -> bool:
        """Inscrit une MANIGANCE d'ennemi au meme journal que ses attaques.

        Elle vit ici, a cote de son attaque, parce que les deux forment une
        seule notion cote joueur — l'activation d'un ennemi — et qu'un lecteur
        qui cherche « comment le bilan est-il nourri ? » doit trouver les deux
        moities au meme endroit.

        Pas de defense sur une manigance : la menace posee (`pose`) est le total
        REELLEMENT place, apres `WhenRecalculateSchemeValue`, d'ou
        `base = pose - boost` — la meme egalite que l'attaque
        (`base + boost - defense = inflige`), avec une defense toujours nulle,
        et sans plafonnement a zero qui puisse la fausser. La valeur imprimee
        de la carte, elle, ne parait que dans le fait d'INTENTION.

        Rend True si un fait a ete inscrit : l'appelant ne consomme son
        intention que dans ce cas.
        """
        from game.card.face.base import Enemy

        if not Enemy.IsType(auteur) or not is_base_scheme:
            return False

        world = auteur.card.world
        boost_total = sum(valeur for _, _, valeur in boost_apports)
        phase = world.GetPhaseText()

        world.stat.RecordFaitMechant(world.round_id, {
            'genre': 'manigance',
            # Meme regle que l'attaque, juste au-dessus.
            'etat': 'resolu',
            'activation_id': activation_id or world.stat.NouvelleActivation(world.round_id),
            'phase': phase,
            **CanAttack._CauseDe(auteur, manigance, phase, by_effect),
            'auteur': auteur.name,
            'auteur_id': auteur.card.object_id,
            'cible': manigance.name,
            'cible_id': manigance.card.object_id,
            'base': pose - boost_total,
            'boost': boost_total,
            'defense': 0,
            'inflige': pose,
            'subi': pose,
            # Menace APRES la pose, et le seuil de la manigance visee (« /6 »,
            # cartouche du 04/10/2026) : la carte a pu avancer de stade dans la
            # foulee, le plateau ne le relit plus sur elle. None sans seuil.
            'restant': getattr(manigance, 'threat', None),
            'plafond': getattr(manigance, 'target_threat', None),
            'boosts': CanAttack._BoostsPublies(boost_apports, boost_cards),
            'cible_annoncee': (cible_annoncee or manigance).name,
            'cible_annoncee_id': (cible_annoncee or manigance).card.object_id,
            'base_imprimee': base_imprimee,
        })
        return True

    @staticmethod
    # Cannot use `Filter.FilterByType(units, Unit2)` because of ultron facedown drone
    def GetUnits(units: Sequence['CardFace']) -> List['Unit2']:
        from game.card.face.base import Unit2
        targets: List['Unit2'] = []
        for unit in units:
            target = unit.card.face
            if not Unit2.IsType(target) or target.IsDefeated():
                continue
            targets.append(target)
        return targets

    @staticmethod
    def SpecialAttack(this: 'Unit2|CanAttack', units: Sequence['CardFace'], by_effect: 'Effect', *, property: 'AttackProperty') -> 'Message.AfterUnitAttackEnd|None':
        targets = CanAttack.GetUnits(units)

        message = CanAttack.AttackInternal(this, targets, by_effect, property=property)
        return message

    def BasicAttack(self, units: Sequence['CardFace'], by_effect: 'Effect',
                    *,
                    property: 'AttackProperty|None'=None,
                    if_this_defeat_unit: Callable[['CardFace'], None]|None=None,
                    if_no_character_takes_damage: Callable[[], None]|None=None,
                    if_characters_damaged_by_this: Callable[[List['Unit2']], None|int]|None=None,
                    for_each_damage_dealt_by_this: Callable[[int], None|Any]|None=None,
                    if_no_attack_was_made: Callable[[], None]|None=None,
                    if_unit_defends_against: Callable[['Unit2', int], None]|None=None,
                    if_undefended: Callable[[], None]|None=None,
                    ) -> 'Message.AfterUnitAttackEnd|None':
        if not units:
            if if_no_attack_was_made:
                if_no_attack_was_made()
            return None

        if not self.IsCanAttack(by_effect):
            return None
        if property == None:
            property = AttackProperty(is_basic_power=True)
        else:
            property.is_basic_power = True

        controller = units[0].GetControlBy()
        if Player.IsType(controller):
            property.against_player = controller

        targets = CanAttack.GetUnits(units)

        message = CanAttack.AttackInternal(self, targets, by_effect,
                                            property=property,
                                            if_this_defeat_unit=if_this_defeat_unit,
                                            )

        if if_no_attack_was_made and message == None:
            if_no_attack_was_made()

        if if_no_character_takes_damage and message and message.damaged_targets == []:
            if_no_character_takes_damage()

        if if_characters_damaged_by_this and message:
            if_characters_damaged_by_this(message.damaged_targets)

        if for_each_damage_dealt_by_this and message and message.total_dealt_damage > 0:
            for_each_damage_dealt_by_this(message.total_dealt_damage)

        if if_unit_defends_against and message:
            for attack_message in message.atk_messages:
                if attack_message.defender:
                    if_unit_defends_against(attack_message.defender, attack_message.taken_damage)

        if if_undefended and message:
            for atk_message in message.atk_messages:
                if atk_message.defender == None:
                    if_undefended()

        return message

    def IsCanAttack(self, by_effect: 'Effect') -> bool:
        from game.card.face.base import Unit2

        if not self.IsInPlay():
            return False
        if not Unit2.IsType(self):
            return False
        check_message = Message.CheckIfUnitCanAttack(self, by_effect)
        check_message.Send()
        return check_message.can_attack

