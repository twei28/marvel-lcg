from core import *
from build import Build
from game.card.face import *
from game.effect import *
from game.message import *
from game.player import *
from engine.log import Log
from engine.profile import Coverage
from game.world import *

CATEGORY_NAME = "EFFECT"

class EffectInvoker:

    @staticmethod
    def InvokeOperation(effect: 'Effect', message: 'Message2'):
        from game.message import Message
        from game.card.face.base import Unit2
        from game.player import Player
        # from game.operate.faces import Faces

        world = effect.world
        effect.context.ResetBeforeOperation()

        ################################################################################
        try:
            effect.ability.operation(effect, message) # type: ignore
        except Exception as exc:
            # Fix "09004"
            if effect.world.is_game_over:
                pass
            else:
                raise exc

        if Coverage.is_enable:
            Coverage.TrackCallable(effect.ability.operation)

        ################################################################################
        if effect.context.end_attack_messages:
            attacked_targets: List['CardFace'] = []
            damage_targets: List['Unit2'] = []
            atk_messages: List['Message.AfterUnitAttackUnit|Message.AttackEndsBeforeDamageDealt'] = []

            retaliated_unit: Set['CardFace'] = set()

            end_atk_message = effect.context.end_attack_messages[0]
            total_dealt_damage = 0
            for message in effect.context.end_attack_messages:
                # assert message.by_effect == end_atk_message.by_effect
                assert message.attacker == end_atk_message.attacker
                # We remove this assert for "09004"
                # assert message.would_atk_message == end_atk_message.would_atk_message
                attacked_targets += message.attacked_targets
                damage_targets += message.damaged_targets
                total_dealt_damage += message.total_dealt_damage
                atk_messages += message.atk_messages

                for atk_message in message.atk_messages:
                    would_atk_unit_message = atk_message.would_atk_unit_message
                    if would_atk_unit_message:
                        for atk_target in atk_message.attacked_targets:
                            if atk_target not in retaliated_unit:
                                retaliated_unit.add(atk_target)
                                if Unit2.IsType(atk_target) and \
                                    atk_target.IsInPlay() and \
                                    not world.rule.v18_retaliate:
                                    atk_target.ResolveRetaliate(would_atk_unit_message)

                for message in message.atk_messages:
                    message.Send()

            end_message = Message.AfterUnitAttackEnd(
                end_atk_message.attacker,
                attacked_targets,
                damage_targets,
                total_dealt_damage,
                end_atk_message.by_effect,
                atk_messages,
                end_atk_message.would_atk_messages[0]
            )

            end_message.Send()
            world.stat.RecordAttack(end_message)

        if effect.context.end_thwart_messages:
            schemes: List[Scheme2] = []
            after_thw_messages: List['Message.AfterUnitThwartScheme'] = []
            total_remove_threat = 0

            end_thw_message = effect.context.end_thwart_messages[0]

            for message in effect.context.end_thwart_messages:
                # We remove this assert for "44023"
                # assert message.would_thw_message == end_thw_message.would_thw_message
                schemes += message.schemes
                total_remove_threat += message.total_remove_threat
                after_thw_messages += message.after_thw_messages

            end_message = Message.AfterUnitThwartEnd(
                end_thw_message.trigger,
                schemes,
                total_remove_threat,
                end_thw_message.by_effect,
                after_thw_messages
            )

            end_message.Send()
            world.stat.RecordThwart(end_message)

        # if end_attack_message:
        #     end_attack_message.Send()

        if effect.ability.is_label_defense and \
            isinstance(message, AttackerMessageInternal) and \
            Player.IsType(effect.initiator):
            for would_atk_message in message.would_atk_messages:
                assert would_atk_message.has_resolves_defense_labeled_ability_internal == None or \
                    would_atk_message.has_resolves_defense_labeled_ability_internal == effect.initiator
                would_atk_message.has_resolves_defense_labeled_ability_internal = effect.initiator

    @staticmethod
    def ResolveSelfInternal(effect: 'Effect', message: 'Message2|None', to_player: 'Player|None', by_effect: 'Effect', ref_message: 'Message2|None'=None, *, skip_cost: bool=False) -> bool:
        """Resout l'effet, PUIS referme son sas de recherche quoi qu'il arrive.

        ⚠ LE `try/finally` N'EST PAS DECORATIF (21/09/2026, ronde de relecture
        du correctif Aghenatak). Le corps a un RETOUR ANTICIPE : quand
        `WhenEffectWouldResolve` est remplace (`resolve_message.is_be_instead`),
        il sort sans rien faire d'autre. Une recherche menee pendant
        `ProcessSelfCost` ou pendant le choix des cibles, suivie d'un effet
        remplace, laissait donc la carte coincee dans le sas, c'est-a-dire le
        defaut d'origine, sur une branche que ce correctif pretend couvrir.
        C'est LA raison d'etre du `finally`.

        ⚠ IL NE RATTRAPE PAS « le plantage d'un script » : celui-la est deja
        attrape sur place, dans `InvokeOperation`. Le gain sur les exceptions
        est reel mais ETROIT — il ne couvre que ce qui leve HORS de ce try :
        `SpecialDefense`, `after_message.Send()`, `cost_func.AfterCheck`,
        `ResetAfterOperation`, `console.TryBreak`.

        ⚠ IL EST SUR LE try EXTERIEUR, ET C'EST VOULU : pose sur le `try`
        interne de `_ResolveSelfInternal`, il refermerait le sas AVANT
        `cost_func.AfterCheck` et `ResetAfterOperation`.
        """
        try:
            return EffectInvoker._ResolveSelfInternal(
                effect, message, to_player, by_effect, ref_message, skip_cost=skip_cost)
        finally:
            # ⚠ HORS de tout `if can_action`, ET C'EST VOULU : une recherche
            # peut avoir lieu pendant le CHOIX DES CIBLES, donc avant que le
            # cout soit paye. Un effet abandonne faute de paiement doit rendre
            # lui aussi ce qu'il a sorti du deck.
            EffectInvoker.CloseSearchTransit(effect)

    @staticmethod
    def _ResolveSelfInternal(effect: 'Effect', message: 'Message2|None', to_player: 'Player|None', by_effect: 'Effect', ref_message: 'Message2|None'=None, *, skip_cost: bool=False) -> bool:
        from game.player import Player
        from game.card.face.attribute.can_defense import CanDefense

        can_action = True

        ability = effect.ability
        initiator = effect.initiator
        world = effect.world
        this = effect.this

        control_by = effect.this.GetControlBy()

        if not skip_cost:
            can_action = effect.ProcessSelfCost()

        if can_action:
            if isinstance(initiator, Player) and to_player == None:
                to_player = initiator

            if ability.flags.is_check_pay:
                pass
            if ability.is_label_defense:
                defender = effect.GetInitiator().GetIdentity()
                if message and CanDefense.IsType(defender):
                    # When a player initiates a triggered ability labeled as
                    # a defense—such as “Hero Interrupt (defense)”—
                    # during an enemy attack, that player’s identity
                    # becomes the defender and is considered to have
                    # defended the attack if there is not already a defender.
                    # if isinstance(message, Send.WhenUnitBeingAttack|Send.WhenUnitWouldAttack):
                    # if message.defender == None:
                    defender.SpecialDefense(message, effect)

        if can_action:
            if effect.is_unregister_after_exec:
                effect.UnRegisterSelf()
            if message and message.send_resolve_message:
                effect.SetHasSpellInPhase()

            from engine import Engine
            controller_manager = Engine.game.controller_manager
            if not Build.release:
                controller_manager.console.TryBreak(world)

            resolve_message = None

            try:
                # invoke_operation
                should_send = False
                if message == None:
                    should_send = True
                if message and message.send_resolve_message and not ability.flags.is_delay_ability and not ability.flags.is_statistics:
                    from game.card.face.card_type import Event
                    from game.card.face.card_type import Resource

                    should_send = True
                    # if Event.IsType(self.this):
                    if ability.is_play and not Event.IsType(this):
                        should_send = False
                    if ability.flags.is_discard_pay and not Resource.IsType(this):
                        should_send = False

                if should_send:
                    resolve_message = Message.WhenEffectWouldResolve(effect, message, by_effect, to_player, control_by)
                    resolve_message.Send()
                    if resolve_message.is_be_instead:
                        return False

                if isinstance(ref_message, ability.when):
                    EffectInvoker.InvokeOperation(effect, ref_message)
                elif isinstance(message, ability.when):
                    EffectInvoker.InvokeOperation(effect, message)
                    if isinstance(message, Message.WhenCardRevealed):
                        message.reveal_message.AddResolved(effect)
                else:
                    assert ability.when in [
                        Message.WhenCardRevealed,
                        Message.WhenUnitBeDefeated,
                        Message.WhenUnitWouldAttack,
                        Message.WhenUnitWouldScheme,
                        Message.AfterUnitAttackEnd,
                        Message.AfterUnitTookDamage,
                        Message.WhenSchemeBeDefeated,
                        Message.WhenResolvePreparationAbility,
                        Message.WhenCardBecomeBoost,
                    ]

                    class ExTriggerPlayerMessage(TriggerNonePlayerMessage):
                        def __init__(self, player: 'Player|None', world: 'World') -> None:
                            self.by_effect = by_effect
                            super().__init__(player, world=world)
                        def GetKillerPlayer(self) -> None:
                            return None
                        def GetAgainstPlayer(self) -> 'Player|None':
                            return self.to_player
                        def GetByPlayer(self) -> 'Player|None':
                            return self.to_player
                        def GetDefeatingPlayer(self) -> 'Player|None':
                            return self.to_player

                    to_player_message = ExTriggerPlayerMessage(to_player, world)
                    EffectInvoker.InvokeOperation(effect, to_player_message)

            except Exception as exc:
                info = Log.OnCrash(CATEGORY_NAME, exc, effect.GetDisplayName(), ability.operation)
                world.render.ErrorOccurred(info)

            if not Build.release:
                controller_manager.console.TryBreak(world)

            send_resolve_message = message and message.send_resolve_message or message == None
            if send_resolve_message and \
                not ability.flags.is_check_pay and \
                ( \
                    ability.flags.is_interrupt or \
                    ability.flags.is_response or \
                    ability.flags.is_resource or \
                    ability.flags.is_when_completed or \
                    ability.flags.is_when_reveal or \
                    ability.flags.is_when_defeated or \
                    ability.flags.is_setup or \
                    ability.flags.is_boost or \
                    ability.flags.is_special or \
                    ability.flags.is_action
                ):
                    if resolve_message != None:
                        after_message = Message.AfterEffectResolved(effect, message, resolve_message)
                        after_message.Send()
            for cost_func in effect.cost_func.GetAll():
                cost_func.AfterCheck(effect)
            effect.cost_func.Reset()
            effect.context.ResetAfterOperation()

        # Le sas de recherche est referme par `ResolveSelfInternal`, dans son
        # `finally` : il y a un retour anticipe plus haut dans cette methode.
        return can_action

    @staticmethod
    def CloseSearchTransit(effect: 'Effect') -> None:
        """Referme le SAS de recherche : ce que personne n'a reclame rentre.

        CORRECTIF DU 21/09/2026. Signalement Aghenatak du 20/09/2026 : « Squirrel
        Girl jouee comme un support » et « Piecing all together joue comme un
        support », deux symptomes d'un seul defaut.

        Une RECHERCHE (`Search.SearchForCards`) sort du deck la carte trouvee et
        la pose dans la zone de traitement, pour la montrer au joueur. C'est
        ensuite a l'operation appelante d'en faire quelque chose : l'ajouter a
        la main, la jouer, la defausser. Quand elle ne le fait pas (le joueur
        refuse le choix qui suit, `range=(0, 1)` de 61008 Calling in Favors et
        de 61019 Strategy Session ; ou la carte tiree ne convient pas au filtre
        applique APRES coup, 62022 Dynamic Duo), RIEN ne ramenait la carte.
        Elle restait dans le sas pour le reste de la partie : ni en jeu, ni en
        defausse, ni dans le deck. Le plateau la dessine posee sur la table, le
        joueur la prend pour un soutien, et aucune action ne la touche.

        On rend donc chaque carte au deck d'ou elle sort, puis on remelange ce
        deck : elle est repartie a sa place, et sa position n'est pas connue.
        Le sas est vide dans les deux cas, pour ne jamais rendre deux fois.

        ⚠ LE SAS EST PORTE PAR L'EFFET DE LA CARTE QUI CHERCHE (le `by_effect`
        de `SearchInternal.SearchForCardsInternal`), JAMAIS par l'effet jetable
        que `AskChooseSelect` fabrique pour poser la question : ce dernier se
        termine des que le joueur a repondu, donc AVANT que l'operation
        appelante ait pu consommer la carte. Une premiere version notait le sas
        dans `SelectorEnd.DoMove`, qui recoit justement cet effet jetable : elle
        cassait `ze014` The Mother of Night, qui enchaine DEUX
        `Search.PlayerCard`. La premiere carte etait rendue au deck entre les
        deux, la seconde recherche retombait dessus, et une seule carte
        finissait posee sous la manigance au lieu de deux (mesure du
        21/09/2026, signalee par la session voisine).
        """
        from game.operate.faces import Faces

        transit = effect.context.search_transit
        if not transit:
            return
        effect.context.search_transit = []

        a_rendre: Dict['Deck', List['CardFace']] = {}
        for face, deck in transit:
            # Reclamee entre-temps (jouee, mise en main, defaussee) : rien a faire.
            if not face.card.area.flags.is_processing:
                continue
            # ⚠ GARDE MORTE DANS LES DEUX SENS AUJOURD'HUI, ET IL FAUT DIRE
            # EXACTEMENT CE QU'ELLE FAIT (ronde de relecture du 21/09/2026).
            #
            # CE QU'ELLE TESTE REELLEMENT : `is_revealing` est un drapeau de
            # ZONE (deck_type.py, `RevealingArea`), VRAI EN PERMANENCE pour
            # cette zone. Ce n'est PAS « une revelation est en cours ».
            # `RevealingArea` porte aussi `is_processing`, d'ou la ligne : sans
            # elle, une carte posee en zone de revelation serait traitee comme
            # une carte oubliee dans le sas.
            #
            # ELLE NE SERT A RIEN SUR LE SEUL CHEMIN CONNU. `01095` Rhino (II)
            # (`Search.EncounterCard` puis `face.Reveal`) termine sa revelation
            # A L'INTERIEUR de l'operation : quand le sas se referme, la
            # manigance est deja en jeu, c'est la PREMIERE garde
            # (`not ... is_processing`) qui l'ecarte, et celle-ci n'est jamais
            # atteinte. Le temoin « 01095 Rhino (II) — recherche puis REVELE »
            # reste VERT avec cette ligne neutralisee : mesure faite.
            #
            # ET SON MODE DE DEFAILLANCE PROPRE VA DANS L'AUTRE SENS.
            # `CardFaceOnEvent.Reveal` (face_on_event.py) a DEUX sorties
            # anticipees APRES avoir gare la carte dans `world.area_revealing`
            # (`OnPlayerRevealCard` faux, puis `reveal_message.is_be_instead`).
            # Sur un tel chemin la carte reste GAREE dans cette zone, et cette
            # ligne n'y protege rien : elle EMPECHE le filet de l'attraper et
            # reproduit le defaut d'origine. Aucun cas atteignable n'a ete
            # trouve, ni dans un sens ni dans l'autre.
            #
            # On garde la ligne parce qu'elle ne coute rien et que le sens
            # « ne pas arracher une carte en cours de revelation » est le plus
            # defendable des deux. Le prochain arbitrage se fera sur ce
            # commentaire : ne pas y toucher sans un cas qui tranche.
            if face.card.area.flags.is_revealing:
                continue
            Log.Debug(CATEGORY_NAME,
                      f"recherche non consommee : {face} rendue a {deck}")
            a_rendre.setdefault(deck, []).append(face)

        # `Faces.ShuffleAllTo` est LA recette du depot pour « remettre dans le
        # deck et melanger » : elle annonce le retour au journal
        # (`CardsShuffleToDeck_Text`) et marque le deplacement `by_shuffle=True`,
        # ce qu'un `MoveAllTo` suivi d'un `Shuffle` ecrit a la main ne fait pas.
        for deck, faces in a_rendre.items():
            Faces.ShuffleAllTo(faces, deck, effect)

