from core import *
from build import Build
from engine.device import *
from engine.controller import *
from engine.lib import Json
from engine.log import Log, Notify
from game.ability import *
from game.message import *
from game.render import *
from game.scene.replay import *
from game.exceptions import *

CATEGORY_NAME = "CONTROLLER"

class Controller:

    def __init__(self, player_id: int, devices: 'DeviceManager', manager: 'ControllerManager'):
        self.player_id = player_id

        self.manager = manager
        self.render, self.input = devices.CreateDevices(self)

        devices.AddController(self)

    @property
    def game(self):
        return self.manager.game

    @property
    def world(self):
        return self.manager.game.world

    def PrintStepID(self) -> str:
        return self.manager.replay.PrintStepID()

    ################################################################################
    #
    # GetInput
    def RendreLesRefus(self, by_effect: 'Effect|None') -> List[Any]:
        """Les effets ECARTES de la question en cours, au format des options.

        POURQUOI (10/09/2026, demande de l'utilisateur : « quand on survole une
        carte qu'on ne peut pas jouer, j'aimerais avoir la raison ») :
        `EventManager.FilterAvailableEffects` jette les effets refuses ET le
        motif que `CheckCondition` vient d'ecrire. Le plateau ne pouvait donc
        rien dire : la carte injouable n'etait meme pas mentionnee dans la
        question. Ce canal la mentionne, sans rien changer aux options.

        ⚠ CETTE FONCTION NE DOIT JAMAIS FAIRE TOMBER UNE PARTIE. C'est un
        confort d'affichage greffe sur le chemin le plus chaud du moteur :
        toute exception y est avalee et l'effet concerne simplement omis. Une
        raison manquante est un desagrement ; une partie interrompue est une
        partie perdue.
        """
        refus: List[Any] = []
        try:
            refus += self._RefusDesCartesAJouer(by_effect)
        except Exception:
            pass
        try:
            derniers = getattr(self.world.render, "derniers_refus", None) or []
            for effect in derniers:
                try:
                    descriptor = effect.Render(by_effect, self.player_id)
                except Exception:
                    continue
                if not descriptor.failure_reason:
                    continue
                descriptor.failure_reason = Controller.NormaliserLeMotif(descriptor.failure_reason)
                refus.append(descriptor)
        except Exception:
            pass
        # 01/10/2026 : « ca devrait jamais etre affiche sur les cartes de heros
        # et d'alter ego ». `Effect.Render(by_effect)` rend le `bind_id` de
        # `by_effect` quand il existe : pendant « Resolve Mulligans » ou le Setup
        # d'un heros, le refus d'une carte de la main (ou d'une capacite de
        # l'autre forme) se retrouvait donc colle sur l'IDENTITE. On filtre sur
        # la carte a laquelle le refus serait ATTACHE, pas sur `effect.this`.
        try:
            ids_identites = {j.GetIdentity().card.object_id
                             for j in self.world.players if j.GetIdentity() is not None}
            refus = [r for r in refus if r.bind_id not in ids_identites]
        except Exception:
            pass
        return refus

    @staticmethod
    def NormaliserLeMotif(motif: str) -> str:
        """Un CODE STABLE, jamais une phrase.

        Le moteur ne parle pas la langue du joueur : c'est le plateau qui ecrit
        la phrase, en francais ou en anglais, comme il le fait deja pour tout le
        reste (`langue.ts`). Ici on se contente de rendre le motif previsible.

        Presque tous les motifs sont deja des identifiants stables : soit une
        valeur de `EffectFailure` (« out of play »), soit le nom de la fonction
        de condition qui a refuse (« check_hero_form_only »). UN SEUL porte des
        chiffres, celui du cout (effect_checker.py:251), et il est le plus utile
        de tous : on en extrait les deux nombres au lieu de les noyer dans une
        chaine libre.
        """
        if motif.startswith("pay cost, need "):
            reste = motif[len("pay cost, need "):]
            demande, _, disponible = reste.partition(", but only have ")
            return f"cout_insuffisant|{demande.strip()}|{disponible.strip()}"
        return motif

    def _RefusDesCartesAJouer(self, by_effect: 'Effect|None') -> List[Any]:
        """Pourquoi les cartes de la MAIN ne sont pas jouables, une par une.

        ⚠ IL FAUT LE DEMANDER, ON NE PEUT PAS L'ECOUTER. Le refus d'une carte
        en main est bien calcule par `CanPlayBy` (has_cost.py:43), qui appelle
        `FilterAvailableEffects` dans une passe A ELLE. Le tampon
        `world.render.derniers_refus` est donc ecrase par les passes suivantes
        bien avant que la question ne parte : mesure du 10/09/2026, 1 seul
        refus transmis sur une main entiere. On rejoue donc le filtre ICI,
        volontairement, au moment de construire la question.

        ⚠ Cout : une passe de conditions par carte en main, uniquement quand le
        moteur interroge CE joueur. Le meme travail que fait deja `CanPlayBy`
        pour griser la carte, une seconde fois. Si cela pesait, ce serait a
        `CanPlayBy` de rendre son motif plutot qu'un booleen.
        """
        from game.event.manager import EventManager
        from game.effect.rule import GameRule
        from game.message import Message

        refus: List[Any] = []
        joueur = None
        for candidat in self.world.players:
            if candidat.player_id == self.player_id:
                joueur = candidat
                break
        if joueur is None:
            return refus

        identite = joueur.GetIdentity()
        if identite is None:
            return refus

        for face in list(joueur.hand_cards.GetAll()):
            if face is None:
                continue
            effets = face.effect.Find(func_name="Play", when=Message.WhenPlayerInTurn)
            if not effets:
                continue
            message = Message.WhenPlayerLikeInTurn(joueur, GameRule(identite))
            message.Send()
            face.card.can_state.is_like_in_hand = True
            try:
                disponibles = EventManager.FilterAvailableEffects(
                    message, effets, joueur, self.world, None)
            finally:
                face.card.can_state.is_like_in_hand = None
            if disponibles:
                continue  # jouable : rien a expliquer
            for effet in effets:
                try:
                    descriptor = effet.Render(by_effect, self.player_id)
                except Exception:
                    continue
                if not descriptor.failure_reason:
                    continue
                descriptor.failure_reason = Controller.NormaliserLeMotif(descriptor.failure_reason)
                refus.append(descriptor)
        return refus

    def ChoiceOne(self, effect_list: Sequence['Effect'], by_effect: 'Effect|None', message: 'Message2', priority: 'TimingPriority', is_forced: bool|Literal["Forced_Action"], masquer_passer: bool=False) -> Tuple['Effect|None', bool]:
        from game.scene.replay.operation import CardEffectInt

        controller_manager = self.manager

        if len(effect_list) == 0:
            return None, False
        if not self.game.state.is_running:
            return None, False

        # LES GESTES MANUELS DUS S'APPLIQUENT AVANT LE CRC, ET C'EST TOUT
        # L'OBJET DE CES DEUX LIGNES ICI (ronde de correction 2 du
        # 20/09/2026).
        #
        # Le moteur grave dans chaque entree un CRC de la table, et le
        # compare au rechargement, deux lignes plus bas. A l'enregistrement,
        # le geste est applique PUIS la question est re-posee : le CRC grave
        # dans l'entree du rang porte donc la table AVEC le geste. Rejouer ce
        # geste apres ce calcul -- ne serait-ce que d'une question, ce que
        # faisait la ronde 1 en n'appliquant qu'au moment du suivi de `skip`
        # -- comparait une table SANS lui : un `Log.Assert` de niveau Error a
        # chaque ouverture de la sauvegarde, et un `read_ok` qui ne restait
        # vrai que par accident (`all(...)` sur un generateur vide vaut
        # `True`, `crc_ignore_ids` etant vide par defaut). Le jour ou ce
        # `read_ok` devient faux -- c'est deja le cas en mode test --, le
        # bloc `if not read_ok` juste en dessous COUPE le rejeu en plein
        # milieu : la panne de la famille C1, revenue par la fenetre.
        #
        # ⚠ SEULEMENT LA MOITIE QUI N'A BESOIN DE RIEN. On applique ici les
        # gestes dont le rang est atteint ; la FERMETURE de la porte du
        # silence, elle, reste plus bas, apres le bloc qui met
        # `skip.is_skipping` a jour -- c'est le seul endroit qui sait si le
        # rejeu est fini.
        self.game.session.RejouerGestesManuelsJusqua(
            controller_manager.replay.current_step_id)

        # if DeviceManager.is_skipping:
        #     play_json = Render.ToPlayJson()
        #     DeviceManager.play_json_crc = CRC(str(play_json))
        # else:
        #     DeviceManager.play_json_crc = Render.last_render_crc
        controller_manager.replay.calculated_crc = message.world.render.CalculateCRC()

        effect_descriptors = [effect.Render(by_effect, self.player_id) for effect in effect_list]

        # Load replay
        is_puzzle = message.world.scene.is_puzzle
        replay_input, read_ok = controller_manager.replay.GetReplayOperation(is_puzzle)
        if not read_ok:
            if controller_manager.skip.SetIsSkipping(False):
                message.world.render.PresentForceNoWait()

        if replay_input:
            replay_debug_cmd = replay_input.effect.GetDebugCommand()
        else:
            replay_debug_cmd = ""

        replay_inputs_max_size = controller_manager.replay.GetReplayOperationLen()

        if replay_input:
            fallthrough_input = Json.Dumps(replay_input.effect)
        else:
            fallthrough_input = "{}"

        from game.test import Test

        if Test.IsInTesting():
            test_text = f"\r{controller_manager.replay.current_step_id} / {replay_inputs_max_size}\r"
            Log.Test(test_text)
            # if DeviceManager.step_index == replay_inputs_max_size:
            #     Game.SetGameOver(True)
            #     return None, False
        elif controller_manager.skip.is_skipping:
            test_text = f"\r{controller_manager.replay.current_step_id} / {replay_inputs_max_size}\r"
            Log.Print(test_text, end="")
        else:
            # Log.Debug(
            #     CATEGORY_NAME,
            #     self.PrintStepID()
            # )
            pass

        # Check for current event, debug only
        if replay_input and controller_manager.replay.replay_step_id < controller_manager.skip.skip_to:
            event = replay_input.event
            if str(message) != event and not str(message).endswith(event) and str(message).split()[-1] != event.split()[-1]:
                Log.Warn(CATEGORY_NAME, f'Last message different, hope "{event}" but get "{message}"')
                # DebugBreak()

        select_cmd = CommandDescriptor()
        select_effect: 'Effect|None' = None

        fallthrough_cmd = Json.LoadsAs(fallthrough_input, CommandDescriptor)
        convert_fallthrough_input = fallthrough_input

        Notify.Clean()

        try:
            # Convert replay data
            def convert_replay_data(check_object: CommandDescriptor) -> str:
                new_effect_id = CommandDescriptor.FindNewEffectId(check_object.id, effect_list)
                found_effect = None
                for check_effect in effect_list:
                    if check_effect.object_id == new_effect_id:
                        found_effect = check_effect
                        break
                assert found_effect
                resources_effects = found_effect.checker.cost_for_different_target.GetAllPayEffects()

                new_resource_ids: List[str] = []
                for resources_effect_str in check_object.resources:
                    new_resource_ids.append(str(CommandDescriptor.FindNewEffectId(resources_effect_str, resources_effects)))

                command = CommandDescriptor(
                    str(new_effect_id),
                    check_object.targets,
                    new_resource_ids
                )
                return Json.Dumps(command)
            if fallthrough_cmd.id and not replay_debug_cmd:
                convert_fallthrough_input = convert_replay_data(fallthrough_cmd)
        except Exception as exc:
            # Log.FailedTrace(CATEGORY_NAME, exc)
            pass

        if by_effect != None and by_effect.GetDisplayName() == 'End Phase':
            message_name = "End Turn"
        else:
            message_name = message.name

        while True:
            user_input = ''

            if not user_input:
                # if controller_manager.replay.replay_step_id >= controller_manager.skip.skip_to or not replay_input:
                #     controller_manager.skip.SetIsSkipping(False)
                #     if self.world:
                #         self.world.render.PresentForce()
                # if controller_manager.skip.skip_to:
                if controller_manager.replay.replay_step_id >= controller_manager.skip.skip_to or \
                    not replay_input: # Fix skip
                    if controller_manager.skip.SetIsSkipping(False):
                        if self.world:
                            self.world.render.PresentForceNoWait()

                # LA PORTE DU SILENCE SE REFERME QUAND LE REJEU EST FINI, ET
                # ICI SEULEMENT (ronde de correction 1 du 20/09/2026,
                # constat C1). Pas dans `GameSetup`, parce qu'ICI seulement
                # on sait ou en est le rejeu : les deux lignes au-dessus
                # viennent de mettre `skip.is_skipping` a jour. La refermer
                # plus tot faisait rejouer la partie entiere sans
                # declencheurs ni effets de regle -- `manuel_actif` ferme
                # `BroadcastMessage` -- et le joueur retrouvait une table
                # vierge a la place de la sienne.
                #
                # ⚠ L'AUTRE MOITIE EST PARTIE PLUS HAUT (ronde 2) : les
                # gestes dus s'appliquent AVANT `calculated_crc`, en tete de
                # cette methode, sans quoi le CRC de l'entree du rang est
                # compare a une table qui n'a pas encore recu le geste.
                # Celle-ci n'a besoin que de `skip`, celle-la que du rang :
                # les separer, c'est mettre chacune la ou son information
                # existe.
                if not (controller_manager.skip.is_skipping and replay_input is not None):
                    self.game.session.FinirLeRejeuDesGestes()

                if (controller_manager.skip.is_skipping or controller_manager.replay.replay_step_id < controller_manager.skip.skip_to) and replay_input:
                    user_input = convert_fallthrough_input
                    Log.DebugSilent("FAST_UNDO", f'{controller_manager.replay.current_step_id}, {user_input}, {len(effect_list)}')
                    
                    # Hack fix quickstrike
                    # if "Response" in fallthrough_input and \
                    #     "01066" in fallthrough_input and \
                    #     "WhenUnitBeingAttack" in message_name:
                    #     user_input = None
                    #     if controller_manager.skip.SetIsSkipping(False):
                    #         if self.world:
                    #             self.world.render.PresentForceNoWait()
                    #     from core.lib.beep import Beep
                    #     Beep.Warning()

            # Hack
            # if fallthrough_obj.id.startswith(":"):
            #     user_input = convert_fallthrough_input
            # else:
            #     user_input = ""
            #     if DeviceManager.is_skipping:
            #         DeviceManager.SetIsSkipping(False)
            #     DeviceManager.SetSkipTo(0)
            #     if not DeviceManager.is_skipping:
            #         Render.PresentForce() # For update UI
            #     pass

            if not user_input:
                # Tip, replay input
                if fallthrough_input or True:
                    
                    text = """    {}
    Effect: [{}]
    Target: {}
    Cost:   {}""".format(
                        replay_input.event if replay_input else None,
                        fallthrough_cmd.id,
                        [f"{card}" for card in fallthrough_cmd.targets],
                        [f"{effect}" for effect in fallthrough_cmd.resources])

                    from game.render.symbol import Symbol
                    text = Symbol.AddColor(text)
                    Log.Debug(CATEGORY_NAME, self.PrintStepID())
                    Log.Debug(CATEGORY_NAME, text)
                # for effect in effect_list:
                #     # Log.Debug("{:03} {:30} {} {}".format(
                #     #     effect.object_id,
                #     #     f'[{effect.ability.name if effect.ability.name else effect.this.name}]',
                #     #     [face.card.object_id for face in effect.for_select_targets],
                #     #     [pay.object_id for pay in effect.for_select_pay_resource_effects]))

                #     # Log.Debug(CATEGORY_NAME, "c{:<3} {:30} {}".format(
                #     #     effect.object_id,
                #     #     f'[{effect.ability.name if effect.ability.name else effect.this.name}]',
                #     #     [face.card.object_id for face in effect.all_legal_targets])
                #     # )
                #     pass
                check_message = message
                prompt_text = ""

                if isinstance(check_message, Message.WhenPlayerChooseAbility) and check_message.titre:
                    prompt_text = check_message.titre
                elif isinstance(check_message, Message.WhenPlayerChooseAbility) and \
                    check_message.by_effect.bind_message:
                    if check_message.step[1] > 1:
                        prompt_text = f"({check_message.step[0]}/{check_message.step[1]})"
                    check_message = check_message.by_effect.bind_message

                if not prompt_text and check_message.prompt:
                    prompt_text = check_message.prompt.text_no_symbol

                # Get input here
                from engine.device.manager.base import AskOptionPayload
                user_input = self.input.GetInput(
                    AskOptionPayload(
                        options_json=Json.Dumps(effect_descriptors),
                        refus_json=Json.Dumps(self.RendreLesRefus(by_effect)),
                        ability_type=priority.name,
                        event_name=message_name,
                        prompt_text=prompt_text,
                        show_cancel=is_forced == False and not masquer_passer,
                        replay_input=fallthrough_input,
                    )
                )

                if user_input == None:
                    # LES GESTES D'ABORD, LE RENDU ENSUITE (correctif du
                    # constat C1 de la revue finale, 20/09/2026). `DoGetInput`
                    # vient peut-etre de DRAINER un geste manuel : il l'a
                    # applique au monde, mais il ne sait pas l'ecrire dans la
                    # scene -- il est du moteur et ne connait ni `World` ni
                    # `Scene`. Cette methode, elle, tient deja `message.world`
                    # (elle s'en sert quatre lignes plus bas) : c'est donc ici
                    # que le geste entre dans la sauvegarde, exactement comme
                    # `World.ManualLoop` le fait pour l'autre chemin de
                    # drainage (world.py : `self.scene.manuel_commands +=
                    # appliquees`).
                    #
                    # ⚠ AVANT TOUTE GARDE, ET C'EST DELIBERE. Le bloc qui suit
                    # renonce au rendu sur une partie finie ou un moteur qui
                    # s'arrete : renoncer de meme a l'ENREGISTREMENT perdrait
                    # pour toujours le geste qui vient de terminer la partie
                    # (`Puzzle.Win()`), donc la possibilite de l'annuler.
                    # Un rendu perdu se rattrape au rendu suivant ; un geste
                    # perdu ne se rattrape pas.
                    #
                    # LE RANG EST PRIS ICI, ET C'EST LE BON (ronde de
                    # correction 1, constat C2) : `current_step_id` compte
                    # les entrees DEJA jouees, et l'entree de cette
                    # question-ci n'est pas encore empilee -- le geste a donc
                    # bien eu lieu « apres N entrees ». Le rejeu le remettra
                    # exactement la.
                    gestes = controller_manager.device_manager.ConsommerGestesAppliques()
                    message.world.scene.EnregistrerGestesManuels(
                        gestes, controller_manager.replay.current_step_id)

                    # TACHE 8 : le rendu qui manquait. `GetInput` vient de
                    # rendre la main SANS entree ; l'appelant (ChooseEffects,
                    # EventManager) va reposer LA MEME question, et sur ce
                    # chemin-la le seul rendu possible est
                    # `SenderPlayer.PlayerOnEvent_Text`, qui n'appelle
                    # `Present` que pour un `Message.WhenPlayerInTurn`. Une
                    # pause posee pendant le mulligan ou une fenetre
                    # d'interruption ne publiait donc JAMAIS `manuel_actif` :
                    # la trame ne bougeait pas d'un numero et `/get_world`
                    # servait l'ancienne, le plateau croyant que le moteur
                    # parle encore. Mesure du 20/09/2026 : mulligan
                    # (30, False) -> (30, False), Spider-Sense
                    # (82, False) -> (82, False), tour de heros
                    # (35, False) -> (36, True).
                    #
                    # ⚠ PAS A CHAQUE `None`, et c'est tout l'objet de
                    # `ConsommerRenduAForcer` : `DoGetInput` rend aussi
                    # `None` sur une entree arrivee pour un AUTRE joueur ou
                    # sur une sortie d'attente demandee (console, rejeu,
                    # arret du moteur), et rend "{}" sur expiration de
                    # minuterie. Forcer un rendu dans ces cas changerait le
                    # rythme de rendu de chemins etrangers a la pause. Seules
                    # les deux causes qui ont MUTE le monde sans le publier
                    # arment le marqueur : une bascule de pause
                    # (`SignalerPauseAPublier`) et un geste manuel draine
                    # (branche `DrainSandboxCommands` de `DoGetInput`).
                    #
                    # ⚠ LE `SetIsSkipping(False)` N'EST PAS UN ORNEMENT :
                    # `PresentForceNoWait` porte un `assert skip == False`, et
                    # un rejeu silencieux (Ctrl+Z -> AnnulerDernierGeste ->
                    # LoadScene) laisse `skip` arme. Meme precaution, dans le
                    # meme ordre, que `World.ManualLoop` (world.py) juste
                    # avant SON rendu force, et que le debut de cette
                    # methode.
                    #
                    # ⚠ LES GARDES DE FIN D'ABORD (ronde de correction 1) :
                    # `ManualLoop` teste `is_game_over` AVANT son rendu
                    # force, on s'aligne. Une partie finie ou un moteur qui
                    # s'arrete n'a plus d'etat a publier, et les quatre
                    # lignes qui suivent ce bloc rendent justement
                    # `None, False` dans ces cas-la. Le marqueur est
                    # CONSOMME dans tous les cas, jamais laisse arme
                    # derriere une garde.
                    forcer = controller_manager.device_manager.ConsommerRenduAForcer()
                    if forcer and not message.world.is_game_over and self.game.state.is_running:
                        controller_manager.skip.SetIsSkipping(False)
                        message.world.render.PresentForceNoWait()
                    return None, True

                if not Build.release:
                    if controller_manager.console.TryBreak(message.world):
                        continue

                if controller_manager.console.Execute(message.GetReplayText(), message.world, effect_list):
                    return None, True
                if controller_manager.replay.is_updated:
                    return None, True
                if message.world.is_game_over:
                    return None, False
                if not self.game.state.is_running:
                    return None, False

                # When click auto
                if controller_manager.skip.is_skipping or controller_manager.skip.skip_to > 0:
                    user_input = convert_fallthrough_input
                    controller_manager.console.SetCommand(replay_debug_cmd, message.world)
                    if controller_manager.console.Execute(message.GetReplayText(), message.world, effect_list):
                        return None, True
                Log.Debug(CATEGORY_NAME, "Input:", user_input)

            else:
                controller_manager.console.SetCommand(replay_debug_cmd, message.world)
                if controller_manager.console.Execute(message.GetReplayText(), message.world, effect_list):
                    return None, True

            try:
                input_effect = Json.LoadsAs(user_input, CommandDescriptor)
                input_effect_id = CardEffectInt(input_effect.id)
                if input_effect_id == 0:
                    if is_forced:
                        assert len(effect_descriptors) == 1 and effect_descriptors[0].target_num_range[0] == 0, f"{is_forced}"
                    break

                # Update selected
                for effect in effect_descriptors:
                    index = effect_descriptors.index(effect)
                    if effect.id == input_effect_id:
                        select_effect = effect_list[index]
                        break
                    else:
                        select_effect = None
                if select_effect == None and replay_debug_cmd:
                    continue
                # Hack
                if select_effect == None and len(effect_descriptors) == 1 and input_effect.resources == []:
                    select_effect = effect_list[0]

                assert select_effect != None, f"{select_effect=}"

                select_effect.targets.clear()
                for check_target in input_effect.targets:
                    found = False
                    for target in select_effect.context.all_legal_targets:
                        if target.card.object_id == CardEffectInt(check_target):
                            select_effect.context.targets_internal.append(target)
                            found = True
                            break
                    # TODO, update to warning
                    assert found, f"{select_effect=}"
                if select_effect.targets == [] and select_effect.context.target_range[0] > 0:
                    assert False, f"{select_effect=} {select_effect.targets=} {select_effect.context.target_range=}"

                # CORRECTIF (30/08/2026) : l'ancien second garde-fou plantait
                # aussi sur une reponse PARTIELLE (au moins 1 cible legale
                # fournie, mais moins que `target_range[0]`), retire.
                # Observe reproductible (pack custom scarlet_spider, set 128) :
                # `can_health.py` demande a `ChooseOrder([sbire,
                # overkill_target])` d'ordonner 2 unites simultanees (le sbire
                # vaincu et le VILLAIN qui recoit le deversement d'exces via
                # `Worlds.FindVillain`, can_attack.py) ; `target_range=(2, 2)`
                # est fige au moment ou le choix est RENDU au joueur/pilote,
                # mais `all_legal_targets` est REEVALUE au moment de VALIDER
                # la reponse -- si la legalite du vilain comme cible change
                # entre les deux passages, le nombre de cibles reellement
                # selectionnables ne correspond plus au minimum annonce, et
                # une reponse pourtant complete (tout ce qui etait montre a
                # ete choisi) etait rejetee -- boucle infinie d'AssertionError
                # (le moteur reposait la meme question sans jamais avancer).
                # Le premier garde-fou ci-dessus (reponse totalement VIDE)
                # reste actif : seule la reponse PARTIELLE-mais-non-vide n'est
                # plus fatale. Precedent direct pour cette meme famille de cas
                # (le vilain comme cible melangee a d'autres unites) : le
                # `select_rule.startswith('VillainAnd')` que ce bloc verifiait
                # deja plus haut avant ce correctif.

                select_effect.context.paid_this_res_effects.clear()
                for resources in input_effect.resources:
                    taraget = select_effect.targets[0] if select_effect.targets != [] else None
                    effect = select_effect.checker.cost_for_different_target.FindPayEffect(taraget, CardEffectInt(resources))
                    assert effect, f"{select_effect=}"

                    select_effect.context.paid_this_res_effects.append(effect)

                select_cmd = CommandDescriptor(
                    select_effect.GetReplayText(),
                    [x.GetReplayText() for x in select_effect.targets],
                    [x.GetReplayText() for x in select_effect.context.paid_this_res_effects])
                break

            except Exception as exc:
                if controller_manager.skip.SetIsSkipping(False):
                    if self.world:
                        self.world.render.PresentForceNoWait()

                info = Log.FailedTrace(CATEGORY_NAME, exc, no_take_as_error=True)
                message.world.render.ErrorOccurred(info + "UndoRequest\n")
                from core.lib.beep import Beep
                Beep.Warning()
                Log.Debug(CATEGORY_NAME, f'Input:  {user_input}')

        operation = OperationDescriptor(
            controller_manager.replay.current_step_id,
            message.GetReplayText(),
            select_cmd,
            controller_manager.replay.calculated_crc[0])
        controller_manager.replay.Push(operation)

        self.game.statistics.RecordValue("operation", 1)

        if controller_manager.replay.current_step_id > controller_manager.skip.skip_to:
            if controller_manager.skip.SetIsSkipping(False):
                if self.world:
                    self.world.render.PresentForceNoWait()

        return select_effect, False

    def Render(self):
        return self.render.Render()

