from typing import Any, Dict, List, Tuple, TypeAlias
from core import *
from build import Build
from engine.log import Log
from game.card.face import *
from game.card import *
from game.deck import *
from game.ability import *
from game.selector import *
from game.ability.factory import *
from game.message import *
from game.player import *
from game.element.resources import Resources
from game.element.cost import Cost
from game.effect.effect_target_cost import TargetCost

CATEGORY_NAME = "PLAYER"

CardFaceType: TypeAlias = 'CardFace'

def MotifDEchec(effect: 'Effect') -> str:
    """Le motif du refus, pour le journal : « ... failed (check pay) ».

    Ajoute le 11/09/2026 : un effet qui echoue apres son offre (cout impaye,
    cible perdue) ne laissait que le mot « failed » dans le journal, et il a
    fallu sept cas de diagnostic pour comprendre pourquoi une carte du pack
    zeus refusait un paiement. Le motif existe deja (`effect.failures`), il
    n'etait simplement pas ecrit.
    """
    try:
        motif = effect.failures.GetText(effect.bind_player_id)
    except Exception:
        return ""
    return f" ({motif})" if motif else ""


class PlayerAction:
    def GetPlayer(self) -> 'Player':
        from game.player import Player
        return Cast(Player, self)

    ################################################################################
    # Journal de la phase du mechant (voir game/world/world_stat.py).
    #
    # Le client (ui-app) raconte la phase du mechant etape par etape. Les
    # ACTIVATIONS ennemies lui venaient deja du moteur ; la distribution et les
    # revelations, elles, etaient reconstituees dans le navigateur en comparant
    # deux photos du monde — une reconstitution perdue au moindre rechargement
    # de page, et incapable de dire QUI recoit quoi. Les deux methodes
    # ci-dessous inscrivent ces deux evenements la ou le moteur les produit.
    @staticmethod
    def _SiegeDuJoueur(player: 'Player') -> 'int|None':
        """L'indice de SIEGE du joueur, celui que le client retrouve.

        `World.players`, cote client, est rempli dans l'ordre de
        `world.const_seat_order_players` (game/render/to_descriptor.py) : c'est
        donc ce meme indice qui permet au client de nommer le heros concerne.
        `None` quand le joueur n'y figure pas, plutot qu'un indice invente.
        """
        try:
            return player.world.const_seat_order_players.index(player)
        except ValueError:
            return None

    @staticmethod
    def _JournaliserPhaseDuMechant(player: 'Player', phase_attendue: str,
                                   fait: 'Dict[str, Any]') -> None:
        """Inscrit un fait au journal, SI le moteur est bien a l'etape annoncee.

        Le filtre par phase distingue ces deux evenements des activations, que
        `can_attack.py` journalise sans condition. Un ennemi qui frappe hors de
        l'etape 2 reste un fait de la phase du mechant ; une carte rencontre
        distribuee pendant le tour d'un joueur (Deferlement, capacite de carte,
        danger) n'en est pas un, et noierait le cartouche d'etapes qui
        n'appartiennent a aucun point de la carte de reference.

        Le dictionnaire recu n'est jamais mute : on en construit un nouveau,
        que `RecordFaitMechant` recopie a son tour.
        """
        world = player.world
        phase = world.GetPhaseText()
        if phase != phase_attendue:
            return
        identite = player.GetIdentity()
        world.stat.RecordFaitMechant(world.round_id, {
            'phase': phase,
            'joueur': PlayerAction._SiegeDuJoueur(player),
            'joueur_nom': getattr(identite, 'name', None),
            **fait,
        })

    @staticmethod
    def _TypeDeLaCarte(face: 'CardFace') -> str:
        """Le type d'une carte rencontre, en anglais du moteur (`Treachery`)."""
        return getattr(face, 'type_name', type(face).__name__)

    @staticmethod
    def JournaliserRevelationHorsPhase(player: 'Player', face: 'CardFace',
                                       reveal_message: 'Message.WhenPlayerRevealCard',
                                       is_by_flipping: bool) -> None:
        """Une carte rencontre revelee PENDANT LE TOUR D'UN JOUEUR (D26,
        04/10/2026) : « Pendant ton tour » la montre comme la phase montre les
        siennes. Appelee par `ModelOnEvent.Reveal`, le seul passage commun :
        `RevealEncounterCards` (ci-dessus) ne sert qu'a l'etape 4, et
        `Puzzle.Reveal` ou `Worlds.RevealEncounterDeckTopCard` passent par
        `Reveal` directement.

        Quatre gardes : le tour d'un joueur (pas la mise en place, pas la phase
        du mechant, que l'etape 4 journalise deja) ; pas un retournement ; une
        carte rencontre, jamais une manigance principale ; venue du deck
        rencontre ou des cartes distribuees. Le fait a la forme de celui de
        l'etape 4, sans `effets`. Sous garde, comme tout ce journal.
        """
        from game.card.face.base.card_encounter import EncounterCard
        from game.card.face.card_type import MainScheme
        try:
            world = player.world
            phase = world.GetPhaseText()
            if not isinstance(phase, str) or not phase.startswith('Player ') or is_by_flipping:
                return
            if not EncounterCard.IsType(face) or MainScheme.IsType(face):
                return
            if not reveal_message.IsFromEncounterDeck():
                return
            world.stat.RecordFaitMechant(world.round_id, {
                'genre': 'revelation',
                'phase': phase,
                'joueur': PlayerAction._SiegeDuJoueur(player),
                'joueur_nom': getattr(player.GetIdentity(), 'name', None),
                'carte': face.name,
                'carte_id': face.card.object_id,
                'fait_id': (f"revelation:{world.round_id}:{face.card.object_id}"
                            f":{len(world.stat.faits_mechant)}"),
                'par_surge': bool(getattr(face.card, 'revele_par_surge', False)),
                'type': PlayerAction._TypeDeLaCarte(face),
            })
        except Exception:
            pass

    @staticmethod
    def _PhotoDeLaTable(world: 'World') -> 'Dict[str, Any]':
        """Ce qu'une carte revelee peut changer, photographie AVANT puis APRES.

        Trois registres, par identifiant d'objet :
        - `menaces` : la menace de chaque manigance (principales et annexes) ;
        - `pv` : les points de vie des vilains, des identites et des allies ;
        - `en_jeu` : les cartes rencontre presentes sur la table (sbires,
          manigances annexes, environnements), avec leur type en clair.

        La difference entre les deux photos (`_EffetsDeLaRevelation`) dit ce
        que la carte a fait, sans rien connaitre de son texte : c'est le seul
        moyen general, une carte rencontre pouvant tout faire.
        """
        from game.operate.worlds import Worlds
        menaces: Dict[int, Tuple[str, Any]] = {}
        for manigance in Worlds.GetOnAllFieldScheme(world):
            menaces[manigance.card.object_id] = (manigance.name, getattr(manigance, 'threat', None))
        pv: Dict[int, Tuple[str, Any]] = {}
        for vilain in Worlds.GetAllVillains(world):
            pv[vilain.card.object_id] = (vilain.name, getattr(vilain, 'health', None))
        en_jeu: Dict[int, Tuple[str, str]] = {}
        for manigance in Worlds.GetAllSideSchemes(world):
            en_jeu[manigance.card.object_id] = (manigance.name, 'manigance')
        for environnement in world.area_environment.Get():
            en_jeu[environnement.card.object_id] = (environnement.name, 'environnement')
        for joueur in world.const_seat_order_players:
            try:
                identite = joueur.GetIdentity()
            except Exception:
                identite = None
            if identite is not None:
                pv[identite.card.object_id] = (identite.name, getattr(identite, 'health', None))
            for allie in joueur.allies.Get():
                pv[allie.card.object_id] = (allie.name, getattr(allie, 'health', None))
            for sbire in joueur.engaged_minions.Get():
                en_jeu[sbire.card.object_id] = (sbire.name, 'sbire')
            for environnement in joueur.area_environment.Get():
                en_jeu[environnement.card.object_id] = (environnement.name, 'environnement')
        return {'menaces': menaces, 'pv': pv, 'en_jeu': en_jeu}

    @staticmethod
    def _EffetsDeLaRevelation(avant: 'Dict[str, Any]', world: 'World') -> 'List[Dict[str, Any]]':
        """La difference entre la photo d'avant et la table d'apres, en faits.

        Trois genres : `menace` (une manigance deja en jeu a monte), `degats`
        (un personnage a perdu des points de vie) et `entree` (une carte
        rencontre est arrivee sur la table). Une manigance qui ENTRE en jeu
        n'est comptee qu'une fois, comme une entree : sa menace de depart n'est
        pas un gain. Une carte qui ne change rien de mesurable (defausse,
        epuisement) ne produit aucun effet, et le client se tait plutot que
        d'inventer.
        """
        apres = PlayerAction._PhotoDeLaTable(world)
        effets: List[Dict[str, Any]] = []
        for object_id, (nom, menace) in apres['menaces'].items():
            if object_id not in avant['menaces']:
                continue
            menace_avant = avant['menaces'][object_id][1]
            if isinstance(menace, int) and isinstance(menace_avant, int) and menace > menace_avant:
                effets.append({'genre': 'menace', 'cible': nom, 'cible_id': object_id,
                               'montant': menace - menace_avant, 'restant': menace})
        for object_id, (nom, pv) in apres['pv'].items():
            if object_id not in avant['pv']:
                continue
            pv_avant = avant['pv'][object_id][1]
            if isinstance(pv, int) and isinstance(pv_avant, int) and pv < pv_avant:
                effets.append({'genre': 'degats', 'cible': nom, 'cible_id': object_id,
                               'montant': pv_avant - pv, 'restant': pv})
        for object_id, (nom, genre) in apres['en_jeu'].items():
            if object_id in avant['en_jeu']:
                continue
            effets.append({'genre': 'entree', 'carte': nom, 'carte_id': object_id, 'type': genre})
        return effets

    ################################################################################
    # Encounter
    def DealEncounterCard(self, face: 'CardFace', by_effect: 'Effect', *, by_surge: bool=False):
        from game.message import Message
        # from game.ability.rule import GameRule
        from game.operate.faces import Faces
        player = self.GetPlayer()
        world = self.GetPlayer().world

        would_message = Message.WhenPlayerWouldBeDealtEncounterCard(player, by_effect, face)
        would_message.Send()

        if would_message.is_be_instead:
            return

        # ⚠ MARQUE ICI, PAS PLUS TARD. `RevealEncounterCards` revele les cartes
        # de `dealt_encounter_cards` une par une, bien apres cet appel : sans
        # cette marque posee au moment de la distribution, rien ne dit plus
        # laquelle vient d'un Renfort (Surge) une fois dans la pile. Demande
        # de l'utilisateur (28/09/2026, signalement Yarro n27) : le joueur
        # doit voir a l'ecran qu'une nouvelle carte s'enchaine par Renfort,
        # pour ne pas croire qu'un effet d'annulation a echoue alors qu'une
        # DEUXIEME carte, sans rapport, vient d'etre revelee.
        face.card.revele_par_surge = by_surge

        pos = None
        if world.rule.v16_reveal:
            pos = "Bottom"
            if by_surge:
                pos = "Top"
            Faces.MoveAllToDeck([face], player.dealt_encounter_cards, pos, by_effect)
        else:
            Faces.MoveAllTo([face], player.dealt_encounter_cards, by_effect)

        message = Message.AfterPlayerDealEncounterCard(player, would_message)
        message.Send()

        # POINT 3 de la carte de reference : « distribuer une carte rencontre a
        # chaque joueur ». Un fait par CARTE distribuee, et non par joueur : la
        # carte est l'evenement, le mode Heroique en donne deux, et un danger
        # (Hazard) en ajoute une de plus — le cartouche doit toutes les
        # montrer. La carte reste face cachee : le fait ne dit pas laquelle,
        # seulement a qui.
        PlayerAction._JournaliserPhaseDuMechant(
            player, 'Deal Encounter Cards', {'genre': 'distribution'})

    # facedown
    def DealEncounterCards(self, size: int, by_effect: 'Effect', *, by_surge: bool=False) -> None:
        world = self.GetPlayer().world
        if world.is_game_over:
            return

        faces: List['CardFace'] = []
        def process(face: 'CardFace'):
            nonlocal faces
            faces.append(face)
            self.DealEncounterCard(face, by_effect, by_surge=by_surge)
        from game.operate.worlds import Worlds
        Worlds.PopEncounterCards(size, process, True, by_effect)

    def RevealEncounterCards(self) -> None:
        from game.effect.rule import GameRule
        player = self.GetPlayer()
        last_face = None
        while player.dealt_encounter_cards.GetSize() > 0:
            face = player.dealt_encounter_cards.GetTop()
            if not face:
                break
            assert face != last_face, f"{face=} {last_face=}"
            """
            You need to discard them by
            target = message.trigger
            target.Discard(effect)
            """
            # POINT 4 de la carte de reference : « chaque joueur revele sa carte
            # rencontre ». Un fait par carte revelee ; le Deferlement en
            # ajoute une, la boucle la reveille au tour suivant, et elle a donc
            # son propre fait.
            #
            # AVANT `Reveal`, et c'est le point important : une carte qui met le
            # heros a terre en se revelant sort de la boucle par `is_game_over`
            # ou `is_eliminated` juste apres, et son etape n'existerait jamais —
            # or c'est precisement le coup que le joueur veut voir. Le nom et
            # l'identifiant se lisent aussi avant : la carte quitte la zone du
            # joueur pendant sa propre resolution.
            # `fait_id` : le fait est REINSCRIT a la meme place apres l'effet,
            # enrichi de ce que la carte a change (`effets`, voir
            # `_EffetsDeLaRevelation`). Le rang dans le journal le rend
            # unique dans le round.
            world = player.world
            fait_id = f"revelation:{world.round_id}:{face.card.object_id}:{len(world.stat.faits_mechant)}"
            revelation = {
                'genre': 'revelation',
                'carte': face.name,
                'carte_id': face.card.object_id,
                'fait_id': fait_id,
                # Posee par `DealEncounterCard` au moment de la distribution
                # (voir la ou `by_surge` est lu). Signalement Yarro n27
                # (28/09/2026) : sans elle, le joueur ne peut pas distinguer
                # une DEUXIEME carte revelee par Renfort (Surge) d'une reprise
                # du meme evenement, et croit qu'un effet d'annulation a
                # echoue.
                'par_surge': bool(getattr(face.card, 'revele_par_surge', False)),
                # Le TYPE de la carte (cartouche, 04/10/2026), « Treachery »,
                # « Minion »... : le nom de classe, meme source que le
                # `card_type` du descripteur.
                'type': PlayerAction._TypeDeLaCarte(face),
            }
            PlayerAction._JournaliserPhaseDuMechant(player, 'Reveal Encounter Cards', revelation)
            avant = PlayerAction._PhotoDeLaTable(world)
            face.card.annulee_par = None
            face.Reveal(player, GameRule(face))
            effets = PlayerAction._EffetsDeLaRevelation(avant, world)
            # « → Annulée par X » (04/10/2026) : posee par WhenEffectBeCancel.
            annulee = getattr(face.card, 'annulee_par', None)
            if annulee:
                revelation = {**revelation, 'annulee_par': annulee[0], 'annulee_par_id': annulee[1]}
            if effets or annulee:
                PlayerAction._JournaliserPhaseDuMechant(
                    player, 'Reveal Encounter Cards',
                    {**revelation, **({'effets': effets} if effets else {})})
            if player.world.is_game_over:
                break
            if player.is_eliminated:
                break
            last_face = face
            player.stat.RecordReveal(last_face)

        player.dealt_encounter_cards.DiscardAll(GameRule(player.GetIdentity()))

    ################################################################################
    # Assign
    def AssignDamage(self, targets: Sequence['Unit2'], source: 'CardFace', damage: int, by_effect: 'Effect', *, operation: Callable[['Message.AfterUnitTookDamage'], None]|None=None, from_atk_message: 'Message.WhenUnitWouldAttack|None'=None):
        from game.operate.faces_helper import FacesHelper
        player = self.GetPlayer()

        messages: List['Message.AfterUnitDefeatedUnit|Message.AfterUnitTookDamage'] = []

        def assign() -> Dict['Unit2', int]:
            effects = player.ChooseAbilities(
                by_effect,
                AbilityFactory.ForChoiceAbility(
                    f"Assign {damage} damage",
                    lambda targets:
                        None,
                ).SetTarget(
                    targets,
                    range=("Zero", damage),
                    repeat_rules="Health")
            )
            if effects == []:
                # Fix "01111" when no heroes and allies
                # assert value == 0
                return {}
            else:
                # If indirect damage dealt to a player cannot be assigned to any character that player controls, that damage is ignored.
                assign_targets = effects[0].targets
                return FacesHelper.ListToDict(assign_targets) # type: ignore

        units = assign()
        from game.element.damage_property import DamageProperty

        for unit in units:
            damage = units[unit]
            message = unit.TakeDamage(source, DamageProperty(damage, is_indirect_damage=True), by_effect, operation=operation, from_atk_message=from_atk_message)
            if message:
                messages.append(message)

        # self.GetIdentity().TakeIndirectDamage(effect.this, damage, effect)
        return messages

    def AssignHeal(self, targets: Sequence['Unit2'], value: int, by_effect: 'Effect'):
        player = self.GetPlayer()

        def assign(targets: Sequence['Unit2'], value: int, by_effect: 'Effect') -> Dict['Unit2', int]:
            if not Select.From(faces=targets, repeat_rules="Sustained").GetAllLegalTargets(by_effect):
                return {}
            effects = player.ChooseAbilities(
                by_effect,
                AbilityFactory.ForChoiceAbility(
                    "",
                    lambda targets:
                        None,
                ).SetTarget(
                    targets,
                    repeat_rules="Sustained",
                    range=("Zero", value))
            )
            if effects == []:
                assert value == 0
                return {}
            else:
                from game.operate.faces_helper import FacesHelper
                return FacesHelper.ListToDict(effects[0].targets) # type: ignore

        units = assign(targets, value, by_effect)
        for unit in units:
            value = units[unit]
            unit.HealHealth(value, by_effect)

    ################################################################################
    # Effect
    def ChooseEffects(self, effects: List['Effect'], message: 'Message2', *, forced: bool=False, priority: 'TimingPriority'=TimingPriority.Normal, passer_refuse: bool=False) -> 'Effect|None':
        from game.event.manager import EventManager
        # from game.object.object_manager import ObjectManager
        player = self.GetPlayer()
        while True:
            # Clean all resource effect
            # ~~Call this late for avoid being reset before process all the paying effect~~
            # Must call this before filter
            # ObjectManager.ResetPayingEffect()
            filtered_effects = EventManager.FilterAvailableEffects(message, effects, player, player.world, None)
            if filtered_effects == []:
                return None
            from game.message import Message
            Message.PlayerOnEvent_Text(player, message)
            effect, cheat = self.ChoiceAndSpellEffect(filtered_effects, message, priority, forced, passer_refuse=passer_refuse)
            if cheat:
                continue
            else:
                break
        return effect

    def ChooseAbilities(self, by_effect: 'Effect', *abilities: 'Ability|None', forced: bool=True, repeat: int=1, choose_x_different_options: int|None=None, for_second_target: bool=False, titre: str="") -> List['Effect']:
        all_abilities = list(abilities)
        chose_effects: List['Effect'] = []

        must_different = False
        if choose_x_different_options != None:
            must_different = True
            repeat = choose_x_different_options

        # ⚠ « COMBIEN DE FOIS CE CHOIX ? » (rapport n°49, Yarro, 05/10/2026). Un « for each
        # ..., choose » est regle instance par instance (Rules Reference p.20 : chaque
        # iteration est une instance distincte, meme sur la meme cible, et l'etat du jeu
        # se met a jour apres chacune). Six traits = six fois « choisir l'effet » puis
        # « choisir la cible » : douze clics pour six degats sur Kingpin. On propose donc de
        # REPETER un choix N fois d'un coup, chaque instance etant appliquee a son tour. La
        # question n'existe que s'il reste au moins deux iterations et que les options
        # peuvent se repeter (`must_different` l'interdit : « X options DIFFERENTES »).
        #
        # Deux formes, au choix de l'utilisateur (05/10/2026, questions une a une) :
        #  - UNE SEULE option possible : la question vient AVANT tout (« 1 degat a un
        #    ennemi : combien de fois ? »). Le premier choix, automatique, se faisait sans
        #    rien dire et la question suivante ne s'expliquait pas (signalement Yarro).
        #  - Plusieurs options : on choisit, la premiere instance est jouee, puis on
        #    demande combien de fois EN PLUS, tant que le joueur s'en sert : une reponse
        #    « aucune » l'eteint pour le reste de l'effet.
        proposer = True
        a_repeter = 0
        if repeat > 1 and not must_different and forced:
            seule = self._SeuleOptionPossible(by_effect, all_abilities, (1, repeat), for_second_target)
            if seule is not None:
                total = self._DemanderCombienDeFoisAuTotal(by_effect, seule, repeat)
                a_repeter = total - 1
                proposer = False
        i = 0
        while i < repeat:
            effect = self.ChooseAbilitiesHelper(by_effect, *all_abilities, forced=forced, step=(i+1, repeat), for_second_target=for_second_target, titre=titre)
            i += 1
            if effect:
                chose_effects.append(effect)
                if must_different:
                    all_abilities.remove(effect.ability)
                elif a_repeter > 0 and self._PeutRepeterLeChoix(effect):
                    for _ in range(a_repeter):
                        if not self._RepeterLeChoix(effect, by_effect, (i+1, repeat), for_second_target):
                            break
                        i += 1
                    a_repeter = 0
                elif proposer and repeat - i >= 1 and self._PeutRepeterLeChoix(effect):
                    en_plus = self._DemanderCombienDeFoisEnPlus(by_effect, effect, i, repeat)
                    if en_plus == 0:
                        proposer = False
                    for _ in range(en_plus):
                        if not self._RepeterLeChoix(effect, by_effect, (i+1, repeat), for_second_target):
                            break
                        i += 1
        return chose_effects

    @staticmethod
    def _PeutRepeterLeChoix(effect: 'Effect') -> bool:
        """Un choix a cible(s) fixee(s), du type `ChooseAbility` (`ForChoiceAbility`), sans cout."""
        return effect.ability.type == AbilityType.ChooseAbility \
            and not effect.ability.NeedCost() \
            and len(effect.targets) > 0

    def _SeuleOptionPossible(self, by_effect: 'Effect', abilities: Sequence['Ability|None'], step: Tuple[int, int], for_second_target: bool) -> 'Effect|None':
        """L'unique option qu'offrirait la question, si elle n'en offre qu'une et qu'elle est repetable."""
        from game.event.manager import EventManager
        player = self.GetPlayer()
        identity = player.GetIdentity()
        effects = [Effect(identity, ability, world=by_effect.world) for ability in abilities if ability is not None]
        message = Message.WhenPlayerChooseAbility(player, by_effect, step, for_second_target)
        disponibles = EventManager.FilterAvailableEffects(message, effects, player, player.world, None)
        if len(disponibles) != 1:
            return None
        seule = disponibles[0]
        if seule.ability.type != AbilityType.ChooseAbility or seule.ability.NeedCost():
            return None
        return seule

    @staticmethod
    def _CarteCitee(by_effect: 'Effect') -> str:
        """La carte qui pose la question, au format que le plateau remet dans sa langue (« [(48,01097b) Nom] »)."""
        return by_effect.this.GetDisplayName()

    def _DemanderCombienDeFoisAuTotal(self, by_effect: 'Effect', seule: 'Effect', repeat: int) -> int:
        """Option unique : de 1 a `repeat` fois au total (1 = une par une, le defaut)."""
        textes = ["1 time"] + [f"{n} times" for n in range(2, repeat + 1)]
        titre = f"{self._CarteCitee(by_effect)}: {seule.GetDisplayName()}. How many times? (1 to {repeat})"
        return self.AskChooseOneText(list(range(1, repeat + 1)), textes, titre)

    def _DemanderCombienDeFoisEnPlus(self, by_effect: 'Effect', fait: 'Effect', i: int, repeat: int) -> int:
        """Plusieurs options : 0 (defaut) a `repeat - i` repetitions de plus du choix qui vient d'etre fait."""
        restantes = repeat - i
        textes = ["No repeat"] + [f"+{n}" for n in range(1, restantes + 1)]
        titre = f"{self._CarteCitee(by_effect)}: {fait.GetDisplayName()} done ({i} of {repeat}). How many more times?"
        return self.AskChooseOneText(list(range(0, restantes + 1)), textes, titre)

    def _RepeterLeChoix(self, modele: 'Effect', by_effect: 'Effect', step: Tuple[int, int], for_second_target: bool) -> bool:
        """Une instance de plus du meme choix, sur les memes cibles, si elles sont encore legales.

        Chaque instance est une `Effect` NEUVE, resolue seule : l'etat du jeu se met a jour
        entre deux (un sbire vaincu au 2e degat n'est plus une cible au 3e). Rend False des que
        les cibles ne sont plus toutes legales : les iterations restantes redeviennent des
        choix ordinaires.
        """
        player = self.GetPlayer()
        if by_effect.world.is_game_over:
            return False
        effect = Effect(player.GetIdentity(), modele.ability, world=by_effect.world)
        effect.checker.UpdateLegalTargets()
        legales = effect.context.all_legal_targets
        cibles = list(modele.targets)
        if not cibles or any(c not in legales for c in cibles):
            return False
        effect.context.targets_internal = cibles
        effect.context.initiator = player.GetIdentity()
        message = Message.WhenPlayerChooseAbility(player, by_effect, step, for_second_target)
        message.Send()
        effect.ResolveSelf(message, effect)
        return True

    # Only choose one
    def ChooseAbilitiesHelper(self, by_effect: 'Effect', *abilities: 'Ability|None', forced: bool=True, step: Tuple[int, int]=(1, 1), for_second_target: bool=False, titre: str="") -> 'Effect|None':
        priority = TimingPriority.Normal
        if not by_effect.is_rule:
            # Hack for "50014"
            type = by_effect.ability.flags
            if type.is_interrupt:
                priority = TimingPriority.Interrupt
            elif type.is_response:
                priority = TimingPriority.Response

        player = self.GetPlayer()
        player.world.object_manager.ResetChooseEffect()
        # « You may » : la CARTE a demande un choix facultatif. Pris AVANT que
        # `ForChoiceAbilityWithCost` n'abaisse `forced`, qui ne fait pas pour
        # autant du choix un « you may » (Sonic Boom 01123).
        passer_refuse = not forced
        effects: List['Effect'] = []
        identity = player.GetIdentity()
        for ability in abilities:
            if ability == None:
                continue
            effect = Effect(identity, ability, world=by_effect.world)
            effects.append(effect)

            if "ForChoiceAbilityWithCost" in ability.func_names:
                forced = False

        message = Message.WhenPlayerChooseAbility(player, by_effect, step, for_second_target, titre)
        message.Send()
        # Cannot set `forced=True`, see "39019"
        return self.ChooseEffects(effects, message, forced=forced, priority=priority, passer_refuse=passer_refuse)

    def MayChooseOneAbility(self, by_effect: 'Effect', *abilities: 'Ability') -> 'Effect|None':
        cancel_ability = AbilityFactory.ForChoiceAbility(
            "Cancel",
            lambda targets: None,
        )
        effects = self.ChooseAbilities(by_effect, *abilities, cancel_ability)
        if effects and effects[0].ability == cancel_ability:
            return None
        return effects[0]

    # effects[force_index] = fallthrough_effect
    def ChoiceAndSpellEffect(self, filtered_effects: List['Effect'], message: 'Message2', priority: 'TimingPriority', forced: bool|Literal["Forced_Action"]=False, *, passer_refuse: bool=False) -> Tuple['Effect|None', bool]:
        from engine import Engine
        game = Engine.game

        player = self.GetPlayer()

        assert filtered_effects != [], f"{filtered_effects=} {message=}"

        while True:
            fallthrough_effect: Effect|None = None
            need_choose = True

            backup_effects = filtered_effects[:]
            for find_effect in filtered_effects[:]:
                if find_effect.context.only_work_when_no_other_options:
                    filtered_effects.remove(find_effect)
            if filtered_effects == []:
                filtered_effects = backup_effects

            # find fallthrough_effect
            for find_effect in filtered_effects:
                if forced == True:
                    fallthrough_effect = find_effect
                    min_target_num = fallthrough_effect.context.target_range[0]
                    max_target_num = fallthrough_effect.context.target_range[1]
                    fallthrough_effect.context.targets_internal = fallthrough_effect.context.all_legal_targets[:min_target_num]
                    if not forced:
                        assert not fallthrough_effect.ability.NeedCost(), f"{fallthrough_effect.ability}"
                    if min_target_num == max_target_num:
                        if min_target_num <= 1:
                            if len(find_effect.context.all_legal_targets) <= find_effect.context.target_range[0]:
                                need_choose = False
                        # Assign
                        elif len([x for x in fallthrough_effect.targets if x == fallthrough_effect.targets[0]]) == len(fallthrough_effect.targets) and \
                            fallthrough_effect.context.all_legal_targets == fallthrough_effect.targets:
                            need_choose = False
                    break

            if len(filtered_effects) != 1:
                need_choose = True
            elif filtered_effects[0].ability.is_play and \
                not filtered_effects[0].ability.flags.is_delay_ability and \
                filtered_effects[0].this.IsLikeInHand() and \
                not filtered_effects[0].this.card.area.flags.is_processing:
                need_choose = True

            if fallthrough_effect == None:
                for find_effect in filtered_effects:
                    if find_effect.must_choose:
                        fallthrough_effect = find_effect
                        min_target_num = fallthrough_effect.context.target_range[0]
                        fallthrough_effect.context.targets_internal = fallthrough_effect.context.all_legal_targets[:min_target_num]
                        assert not fallthrough_effect.ability.NeedCost(), f"{fallthrough_effect.ability}"

            def choice_one_effect(effect_list: Sequence['Effect']) -> Tuple['Effect|None', bool]:
                if not need_choose:
                    return fallthrough_effect, False
                    # if not fallthrough_effect or \
                    #     fallthrough_effect.is_forced or \
                    #     fallthrough_effect.ability.type.is_discard_pay:
                    #     return fallthrough_effect, False

                if fallthrough_effect and \
                    fallthrough_effect.IsName("Cancel") and \
                    len(effect_list) == 1:
                    return fallthrough_effect, False

                # Fix "44028"
                if player.is_eliminated or message.world.is_game_over:
                    return None, False
                if type(message) is Message.WhenPlayerChooseAbility:
                    bind_effect = message.by_effect
                else:
                    bind_effect = None

                # ⚠ POINT DE REPRISE A CHAQUE DECISION, PAS SEULEMENT AUX 5
                # JALONS D'ORIGINE (demande de l'utilisateur, 28/09/2026,
                # signalement Yarro n25 : « Annuler » retombait souvent
                # plusieurs actions en arriere, parce que `last_step` ne
                # bougeait qu'a un tour qui commence/finit, une defense, une
                # revelation ou un mulligan -- tout le reste (jouer une carte,
                # choisir une cible, payer un cout...) etait invisible pour
                # lui). Verifie avant ce changement : `replay.Push()`
                # (engine/controller/module/replay.py) avance deja
                # `current_step_id` apres CHAQUE decision repondue, pas
                # seulement ces 5-la -- chaque decision a donc toujours eu son
                # propre step_id individuellement rejouable (`Cheat.try_skip_to`
                # /`/undo <n>` le prouvent en debug), aucun etat intermediaire
                # incoherent identifie. Le fait de ne poser `PushNewStep` que
                # sur 5 cas etait donc un choix de granularite, pas une
                # necessite technique.
                #
                # Compromis accepte explicitement par l'utilisateur : les 5
                # jalons d'origine marquaient le moment ou une information
                # cachee devient publique (carte de rencontre retournee...) --
                # elargir permet desormais d'annuler APRES avoir vu cette
                # information, ce qu'on ne peut pas faire a la vraie table.
                # Assume comme acceptable ici.
                game.controller_manager.undo.PushNewStep(game.controller_manager.replay.current_step_id)

                # PASSER NE DOIT JAMAIS ETRE UNE OPTION DEGUISEE (30/09/2026).
                # Sur un choix « you may », il refuse (voir plus bas). Sinon, il
                # retombe sur `fallthrough_effect` : il n'evite rien (Sonic Boom
                # 01123 : Passer = « Exhaust each character »), on le masque.
                passer_est_une_option = fallthrough_effect is not None and \
                    not fallthrough_effect.IsName("Cancel") and not passer_refuse
                selected, is_cheating = player.GetController().ChoiceOne(effect_list, bind_effect, message, priority, forced, masquer_passer=passer_est_une_option)

                game.controller_manager.undo.UpdateLastStep()

                if message.world.is_game_over:
                    return None, False
                return selected, is_cheating

            effect, is_cheating = choice_one_effect(filtered_effects)

            if is_cheating:
                return None, True
            else:
                break

        # ⚠ PAS SUR UN « YOU MAY » : `ForChoiceAbility` pose `SetDefault()`,
        # l'option unique d'un choix facultatif devenait le repli, et « Passer »
        # la PRENAIT (Top Speed sd011, Lock Jaws d'Alligator Loki...).
        if not effect and fallthrough_effect and not passer_refuse:
            effect = fallthrough_effect

        while True:
            if not effect:
                break
            if message.world.is_game_over:
                break
            if self.ResolveEffect(effect, message):
                break

            if effect != fallthrough_effect:
                if type(message) == Message.WhenPlayerInTurn:
                    game.controller_manager.replay.Pop()
                    if not Build.release:
                        game.controller_manager.skip.Clean()
                    message.world.render.PresentForceNoWait(is_update=False)
                    Log.Assert(CATEGORY_NAME, f"{effect} failed{MotifDEchec(effect)}")
                    # engine.DebugBreak()
                    break
                elif fallthrough_effect != None:
                    effect = fallthrough_effect
                else:
                    effect = None
                    break
            else:
                # Is is in selecting target
                # game.controller_manager.replay.PopHistoryInputs()
                # game.controller_manager.replay.PopHistoryInputs()
                return None, False
        return effect, False

    ################################################################################
    # Ability
    def ResolveSpecialAbility(self, faces: Sequence['CardFace'], by_effect: 'Effect'):
        player = self.GetPlayer()
        for face in faces:
            face.ResolveSpecialAbility(player, by_effect, sequence=faces)

    def ResolveEffect(self, effect: 'Effect', message: 'Message2') -> bool:
        from game.card.face.base import ClassCard
        from game.operate.faces import Faces

        this = effect.this

        is_like_from_hand = this.IsLikeInHand()
        # Fix for https://itch.io/t/4493777/interaction-between-magik-mutant-protector-defensive-energy
        if effect.ability.is_play and not effect.ability.flags.is_delay_ability:
            from_area = this.card.area
            effect.context.play_from_area = from_area # CORRECTIF (pack brawn)
            Faces.MoveAllToProcessingArea([this], effect)
        else:
            from_area = None

        player = self.GetPlayer()

        if effect.checker.CheckBeforeActive(player):
            # assert type(message) != Send.WhenPlayerPayingResources, f"{message=}"
            if effect.ability.is_play and not effect.ability.flags.is_delay_ability:
                assert from_area != None
                this = effect.this.CastTo(ClassCard)
                if this.Play(player, effect, message, effect.context.paid_this_resources, from_area, is_like_from_hand):
                    player.stat.RecordPlayedFace(this)
                    player.world.buff_manager.OnRecordPlayedFace(this)
            else:
                effect.ResolveSelf(message, effect)
            return True
        else:
            if effect.ability.is_play:
                # ⚠ LA CARTE NE PART PAS A LA DEFAUSSE (correctif du 20/09/2026,
                # signalement Yarro n°18). Une carte dont la mise en jeu ECHOUE
                # n'a jamais ete jouee : elle retourne d'ou elle vient. Il y
                # avait ici `Faces.DiscardAll([this], effect)`, qui jetait a la
                # defausse une carte encore en main deux instants plus tot --
                # le joueur la perdait sans l'avoir jouee, et sans un mot.
                # `play_from_area` est releve juste avant
                # `MoveAllToProcessingArea`, au debut de cette meme methode.
                origine = effect.context.play_from_area
                if origine != None:
                    Faces.MoveAllTo([this], origine, effect)
                else:
                    # Aucune zone d'origine relevee : la carte ne vient pas
                    # d'une mise en jeu ordinaire. On ne la laisse pas en zone
                    # de traitement, mais on dit pourquoi on la defausse.
                    Log.Assert(CATEGORY_NAME,
                               f"{effect} echoue sans zone d'origine, {this} est defaussee")
                    Faces.DiscardAll([this], effect)

        # Fix "45017"
        if effect.ability.selectors and \
            effect.ability.selectors[0]:
            effect.ability.selectors[0].IfSelectTargetFailure(effect)

        # Error
        from game.test import Test
        if Test.IsInTesting():
            from core.lib.beep import Beep
            Beep.Warning()
            # We can't call this, save data will broken
            # game.controller_manager.replay.PopHistoryInputs()
            # game.controller_manager.replay.UpdateReplayStepId(+1)
            # DebugBreak()

        Log.Assert(CATEGORY_NAME, f"{effect} failed{MotifDEchec(effect)}")
        if not Build.release:
            controller_manager = player.controller.manager
            if controller_manager.skip.SetIsSkipping(False):
                if player.world:
                    player.world.render.PresentForceNoWait()

        return False

    ################################################################################
    # Hand Size
    def GetCountHandSizeFaces(self):
        player = self.GetPlayer()
        count_faces: List['CardFace'] = []
        for face in player.hand_cards.Get():
            message = Message.CheckIfFaceCountHandSize(player, face)
            message.Send()
            if message.count_hand_size:
                count_faces.append(face)
        return count_faces

    ################################################################################
    # Hand Cards
    def DrawUp(self, size: int|Literal["Max"], by_effect: 'Effect') -> List['CardFace']:
        from game.message import Message
        from game.card.face.card_type import Obligation
        player = self.GetPlayer()

        if player.world.is_game_over:
            return []

        if player.is_eliminated:
            return []

        faces: List['CardFace'] = []

        if size == "Max":

            max_repeat_times = 10
            while True:
                assert max_repeat_times > 0
                max_repeat_times -= 1

                if player.is_eliminated:
                    return []
                if by_effect.world.is_game_over:
                    return []

                count_hand_cards = player.GetCountHandSizeFaces()
                size = player.hand_size - len(count_hand_cards)
                size -= len([x for x in faces if Obligation.IsType(x)]) # Fix "04163"
                if size > 0:
                    faces += player.DrawUp(size, by_effect)
                else:
                    break
        else:
            def draw_up(face: 'CardFace'):
                message = Message.WhenPlayerWouldDrawCard(player, face, by_effect)
                message.Send()
                if not message.is_be_instead:
                    face.card.MoveToArea(player.hand_cards, by_effect, ui_group=True)

            faces = self.PopPlayerDeckCards(
                size,
                draw_up,
                by_effect,
                continue_after_shuffle=True,
            )
            if len(faces) < size:
                player.Eliminate(by_effect)
            message = Message.AfterPlayerDrewCards(player, {x: player.player_deck for x in faces}, by_effect)
            message.Send()
        return faces

    # Add it to your hand
    def GainCard(self, faces: Sequence['CardFace']|Sequence['ClassCard']|'CardFace', by_effect: 'Effect') -> List['CardFace']:
        from game.operate.faces import Faces
        from game.card.face.card_face import CardFace
        from game.player import Player
        from game.effect.rule import GameRule
        player = self.GetPlayer()

        if isinstance(faces, CardFace):
            faces = [faces]

        for face in faces:
            if face.IsInPlay():
                Faces.DiscardAll(face.GetInventoryDeck().Get(), GameRule(face))
                Faces.DiscardAll(face.GetPlacedCardArea().Get(), GameRule(face))

            # Fix "04097"
            from game.card.face.base import ClassCard
            if type(face.card.GetOwner()) is not Player and ClassCard.IsType(face):
                face.card.SetOwner(player)

        moved_faces = Faces.MoveAllTo(faces, player.hand_cards, by_effect)
        Message.AfterPlayerGainCards_Text(player, moved_faces, by_effect)
        return moved_faces

    ################################################################################
    # CORRECTIF (pack brawn) : Reserve
    # Zone hors-jeu de 3 cartes maximum. On peut y poser une carte au-dela de la
    # limite, mais il faut alors immediatement redescendre a 3 en defaussant :
    # c'est le joueur qui choisit lesquelles, comme pour la limite de main.
    def PutIntoReserve(self, faces: Sequence['CardFace'], by_effect: 'Effect') -> List['CardFace']:
        from game.operate.faces import Faces
        player = self.GetPlayer()

        if not faces:
            return []

        moved_faces = Faces.MoveAllTo(faces, player.reserve, by_effect)
        player.EnforceReserveLimit(by_effect)
        return moved_faces

    def EnforceReserveLimit(self, by_effect: 'Effect') -> List['CardFace']:
        player = self.GetPlayer()

        excess = player.reserve.GetSize() - player.reserve_limit
        if excess <= 0:
            return []
        return player.AskDiscardFaces(player.reserve.Get(), (excess, excess), by_effect)

    def DiscardRandomHandCards(self, size: int, by_effect: 'Effect', rule: Literal["", "IdentitySpecific"]="") -> List['CardFace']:
        from game.operate.faces import Faces
        faces = self.GetRandomHandCards(size, rule)
        Faces.DiscardAll(faces, by_effect)
        return faces

    def GetRandomHandCards(self, size: int, rule: Literal["", "IdentitySpecific"]="") -> List['CardFace']:
        from game.card.face.base import ClassCard
        player = self.GetPlayer()

        # Log.GameInfo(f'{self} random choice {size} cards')
        faces = player.hand_cards.Get()
        if rule == "IdentitySpecific":
            for face in faces[:]:
                if not ClassCard.IsType(face) or not face.IsClass("IdentitySpecific"):
                    faces.remove(face)

        if len(faces) > size:
            from game.operate.rand import Rand
            return Rand.RandomChoice2(faces, size, player.world)
        return player.hand_cards.Get()

    def DiscardAllHands(self, by_effect: 'Effect', finder: 'CardFinder|None'=None) -> int:
        from game.operate.faces import Faces
        player = self.GetPlayer()

        faces = player.hand_cards.FindCards(finder)

        return len(Faces.DiscardAll(faces, by_effect))

    def GetAllResourceHandCards(self, text: "Resources.RBY") -> List['CardFace']:
        from game.card.face.base import ClassCard
        player = self.GetPlayer()

        return [x for x in player.hand_cards.Get() if ClassCard.IsType(x) and x.printed_resource.HasColorPrinted(text)]

    ################################################################################
    # Play
    def PlayAnAlly(self, ally: 'Ally', paying_cost: bool) -> bool:
        from game.element.resources import Resources
        from game.effect.rule import GameRule
        from game.operate.faces import Faces

        player = self.GetPlayer()

        effects = ally.effect.Find(func_name="Play")
        for effect in effects:
            # effect = effect.Copy()
            effect.context.initiator = player
            message = Message.WhenPlayerLikeInTurn(player, GameRule(player.GetIdentity()))
            message.Send()
            effect.checker.UpdateLegalTargets()
            effect.context.targets_internal = effect.context.all_legal_targets[:effect.context.target_range[1]]
            effect.context.bind_message = message
            from_area = ally.card.area
            if paying_cost:
                ally.card.can_state.is_like_in_hand = True
                self.ChooseEffects([effect], message)
                ally.card.can_state.is_like_in_hand = None
                # def play_ally(targets: Sequence['CardFace'], res: 'Resources'):
                #     ally.Play(player, effect, message, res, from_area)

                # # Cannot use `ForChoiceAbility` because we need the cost in `pay_effect`
                # play_effect = player.ChooseAbilities(
                #     effect,
                #     AbilityFactory.ForChoiceAbilityWithCost(
                #         AbilityType.ChooseAbility,
                #         ally.printed_cost,
                #         play_ally
                #     )
                # )
                # return play_effect != None
            else:
                Faces.MoveAllToProcessingArea([ally], effect)
                return ally.Play(player, effect, message, Resources("0"), from_area, False)
            # self.ChooseEffects([effect], )
        return False

    # CORRECTIF (pack custom superior_iron_man, Merlin) : `PlayAnAlly` ne fait
    # rien de specifique aux allies dans son corps (`face.card`, `face.effect`,
    # `face.Play` sont generiques a toute carte jouable, `CardPlayer.Play` vit
    # dans card_player.py, pas dans Ally) -- seul son annotation de type et son
    # nom le restreignaient. Stark Island (si008) a besoin du meme mecanisme
    # ("search ... and put it into play ... paying its cost") pour un Support,
    # ce qu'aucune carte officielle ne fait (toutes les recherches similaires
    # jouent gratuitement ou ajoutent seulement a la main). Generalisee ici
    # plutot que dupliquee sur PlayAnAlly, pour ne rien risquer sur son
    # comportement existant.
    def PlayACard(self, face: 'CardFace', paying_cost: bool) -> bool:
        from game.element.resources import Resources
        from game.effect.rule import GameRule
        from game.operate.faces import Faces

        player = self.GetPlayer()

        effects = face.effect.Find(func_name="Play")
        for effect in effects:
            effect.context.initiator = player
            message = Message.WhenPlayerLikeInTurn(player, GameRule(player.GetIdentity()))
            message.Send()
            effect.checker.UpdateLegalTargets()
            effect.context.targets_internal = effect.context.all_legal_targets[:effect.context.target_range[1]]
            effect.context.bind_message = message
            from_area = face.card.area
            if paying_cost:
                face.card.can_state.is_like_in_hand = True
                self.ChooseEffects([effect], message)
                face.card.can_state.is_like_in_hand = None
            else:
                Faces.MoveAllToProcessingArea([face], effect)
                return face.Play(player, effect, message, Resources("0"), from_area, False)
        return False

    def PlayOneCardLikeInTurn(self, faces: List['CardFace'],
                            by_effect: 'Effect',
                            *,
                            ignore_resources_cost: bool=False,
                            update_resources_cost: int=0,
                            forced: bool=False):
        from game.card.face.attribute.has_cost import HasCost
        from game.operate.faces import Faces
        player = self.GetPlayer()
        faces = [x for x in faces if x.CanPlayBy(player)]
        face = player.AskChooseFace(
            faces,
            by_effect,
            forced=forced,
            peek=True,
            not_move=False,
        )

        if HasCost.IsType(face):
            player.PlayCardsLikeInTurn(
                [face],
                by_effect,
                ignore_resources_cost=ignore_resources_cost,
                update_resources_cost=update_resources_cost,
                forced=forced
            )

        if face:
            if face.card.area.flags.is_processing:
                Faces.DiscardAll([face], by_effect)

    def MakeBasicPowerLikeInTurn(self,
                                faces: Sequence['CardFace'],
                                by_effect: 'Effect',
                                which_powers: List["CardFace.BASIC_POWER"],
                                *,
                                when_use: Callable[['Unit2', 'Message.WhenUnitUseBasicPower'], Any]|None=None,
                                ):
        from game.card.face.base import Friend
        from game.operate.effects import Effects

        effects: List['Effect'] = []
        temp_effects: List[Effect] = []

        for face in faces:
            if Friend.IsType(face):
                effects += face.GetBasicPowerEffects(which_powers)
        player = self.GetPlayer()
        identity = player.GetIdentity()

        if when_use:
            when_use_effects = identity.effect.Registers(
                AbilityFactory.WhenUnitUseBasicPower(
                    AbilityType.Temp0,
                    faces,
                    lambda effect, message:
                        when_use(message.trigger, message),
                )
            )
            temp_effects += when_use_effects

        message = Message.WhenPlayerLikeInTurn(player, by_effect)
        message.Send()
        player.ChooseEffects(effects, message)

        Effects.UnRegister(temp_effects)


    def PlayCardsLikeInTurn(self,
                            faces: List['CardFace'],
                            by_effect: 'Effect',
                            *,
                            ignore_resources_cost: bool=False,
                            update_resources_cost: int=0,
                            give_piercing: bool=False,
                            forced: bool=True,
                            after_play: Callable[['HasCost'], Any]|None=None,
                            if_not_play_discard_it: bool=True
                            ) -> List['CardFace']:
        from game.card.face.attribute.has_cost import HasCost
        from game.operate.effects import Effects
        from game.operate.faces import Faces

        player = self.GetPlayer()
        identity = player.GetIdentity()

        def play_card(face: HasCost) -> 'Effect|None':
            effects = face.GetTurnPlayEffects()

            # Fix "30004"
            # assert len(effects) == 1, f"{effects=}"
            temp_effects: List[Effect] = []
            if ignore_resources_cost:
                for check_effect in effects:
                    temp_effects += face.effect.Registers(
                        AbilityFactory.IgnoreThisCostIf(
                            AbilityType.Temp0,
                        )
                    )
            elif update_resources_cost != 0:
                for check_effect in effects:
                    temp_effects += face.effect.RegisterTemp(
                        AbilityFactory.ReduceCostToPlayThis(
                            lambda effect: -1 * update_resources_cost,
                            which_effect=check_effect
                        ),
                        unregister_after_exec=False
                    )

            if give_piercing:
                for check_effect in effects:
                    temp_effects += identity.effect.Registers(
                        AbilityFactory.WhenUnitWouldAttack(
                            AbilityType.Temp0,
                            None,
                            lambda effect, message:
                                message.GainPiercing(effect),
                            by_effect=check_effect,
                        )
                    )

            message = Message.WhenPlayerLikeInTurn(player, by_effect)
            message.Send()

            forced_play = forced
            if forced_play and not ignore_resources_cost:
                forced_play = False

            face.card.can_state.is_like_in_hand = True
            played = player.ChooseEffects(effects, message, forced=forced_play)
            face.card.can_state.is_like_in_hand = None

            # After play
            Effects.UnRegister(temp_effects)
            if after_play:
                after_play(face)

            if not played and if_not_play_discard_it:
                if face.IsInProcessingArea():
                    # CORRECTIF (25/09/2026, signalement D de Yarro). Une carte
                    # sortie d'un DECK par une recherche (`Search.SearchForCards`),
                    # ACCEPTEE puis impayable, ne doit pas partir en defausse :
                    # aucune lecture des regles ne le soutient, elle doit
                    # retourner au deck qui l'a fournie, remelange. C'est la
                    # meme famille que le sas de recherche corrige le
                    # 21/09/2026 (`effect_invoke.py`, `CloseSearchTransit`),
                    # mais CE filet-la ne mord pas ici : quand il se referme,
                    # cette carte a DEJA quitte la zone de traitement (elle est
                    # en defausse), donc `is_processing` est deja faux et son
                    # entree du sas est lue comme « reclamee », a tort.
                    #
                    # On consulte donc la MEME liste (`search_transit`) ICI,
                    # AVANT la defausse : si cette carte precise en vient, elle
                    # retourne a son origine au lieu d'etre perdue. Une carte
                    # qui ne vient pas d'une recherche (chemin A/B d'Echo, une
                    # carte de main ordinaire...) n'a aucune entree, et le
                    # comportement historique — defausser — ne change pas.
                    origine = None
                    for entree in by_effect.context.search_transit:
                        if entree[0] is face:
                            origine = entree[1]
                            by_effect.context.search_transit.remove(entree)
                            break
                    if origine is not None:
                        Faces.ShuffleAllTo([face], origine, by_effect)
                    else:
                        Faces.DiscardAll([face], by_effect)

            return played

        played_faces: List['CardFace'] = []
        for face in faces:
            if HasCost.IsType(face):
                # face.card.can_state.is_like_in_hand = None
                if play_card(face):
                    played_faces.append(face)
        return played_faces

    ################################################################################
    # Deck
    def PopPlayerDeckCards(self,
                           size: int,
                           process: Callable[['CardFace'], None|bool],
                           by_effect: 'Effect',
                           *,
                           continue_after_shuffle: bool=False,
                        #    is_group_action: Literal[False, "Draw", "Discard", "Set"]=False
                           ) -> List['CardFace']:
        player = self.GetPlayer()
        if player.is_eliminated:
            return []

        faces = player.player_deck.PopInternal(
            size,
            process,
            by_effect,
            continue_after_shuffle=continue_after_shuffle,
        )
        return faces

    def DiscardDeckTopCards(self, size: int|Literal["1*"], by_effect: 'Effect') -> List['CardFace']:
        player = self.GetPlayer()
        if player.is_eliminated:
            return []

        from game.operate.worlds import Worlds
        size = Worlds.ConvertPerPlayerIconToInt(size, by_effect)

        faces = player.player_deck.DiscardCardsInternal(
            size,
            by_effect,
            continue_after_shuffle=False,
        )
        return faces

    def DiscardDeckTopCard(self, by_effect: 'Effect') -> 'CardFace':
        faces = self.DiscardDeckTopCards(1, by_effect)
        return faces[0]

    def DiscardDeckUntil(self,
                         by_effect: 'Effect',
                        #  finder: 'CardFinder|None'=None,
                         *,
                         name: str|None=None,
                         trait: "CardFace.TRAITS|None"=None,
                         card_type: 'Type[TF]|CardFace'=CardFaceType,
                         return_other_faces: List['CardFace']|None=None,
                         **kwargs: Unpack['CardFinder.KWArgs'],
                         ) -> 'TF|None':
        player = self.GetPlayer()
        if player.is_eliminated:
            return None

        face, other = player.player_deck.DiscardUntil(
            by_effect,
            name=name,
            trait=trait,
            card_type=card_type,
            **kwargs
        )
        if return_other_faces != None:
            return_other_faces.clear()
            return_other_faces.extend(other)
        return face

    ################################################################################
    # Resources
    # def GetCanPayEffects(self, message: 'Send.CheckPlayerCanPayingResources', for_effect: 'Effect') -> List['Effect']:
    #     from cards.pack import World
    #     effects: List['Effect'] = []
    #     for player in World().GetPlayers(for_effect):
    #         for face in player.hand_cards.Get():
    #             for effect in face.effects:
    #                 if effect.ability.when == Send.WhenPlayerPayingResources:
    #                     effects += effect.ToAvailableArray(message)
    #         for face in player.GetControlCards():
    #             for effect in face.effects:
    #                 if effect.ability.when == Send.WhenPlayerPayingResources:
    #                     effects += effect.ToAvailableArray(message)
    #     return effects

    def SpendResource(self, for_effect: 'Effect', paid_effects: Sequence['Effect'], payment: 'TargetCost.Payment',
                      need_cost: 'Cost|None'=None) -> 'Resources':
        """Fait payer au joueur les moyens de paiement QU'IL A CHOISIS.

        ⚠ LE PAIEMENT EST ATOMIQUE (correctif du 20/09/2026, signalement Yarro
        n°18). `need_cost` est le cout a couvrir : si les moyens choisis
        rendent MOINS que lui, rien n'est depense du tout.

        POURQUOI. Un moyen de paiement peut ANNONCER plus qu'il ne GENERE. Sync
        Ratio (`31001a` SP//dr Suit) annonce, a la verification, la ressource
        imprimee de TOUTES les interfaces inclinables ; au paiement, son cout
        `CostFunc.Exhaust(range=(1, "All"))` laisse le joueur n'en incliner
        qu'une. Le joueur voyait donc « 2 » annonce pour un cout de 2, et le
        moteur n'en recevait qu'une. Meme forme exactement sur `50044` Fury's
        Watch (`CostFunc.RemoveTokens(..., (1, 2), 'threat')`) : le defaut est
        GENERIQUE, pas propre a SP//dr.

        Avant ce correctif, le manque etait constate APRES coup, par
        `EffectChecker.check_pay` : l'interface restait inclinee, la carte de
        main depensee restait defaussee, et `PlayerAction.ResolveEffect`
        defaussait par-dessus la carte qu'on voulait jouer. Perte seche des
        deux cotes, en un clic, sans message.
        """
        from game.message import Message

        player = self.GetPlayer()

        paid_faces: List['CardFace'] = []
        # Ce que chaque payeur a engage, releve JUSTE APRES qu'il ait paye :
        # (effet payeur, cout, releve). Voir `CostFunc.SnapshotCost` pour
        # pourquoi on ne relit pas l'objet cout au moment du rendu.
        releves: List[Tuple['Effect', Any, Any]] = []
        # La zone d'ou vient chaque payeur, relevee AVANT qu'il paie : c'est
        # la seule facon de renvoyer une carte de main depensee comme
        # ressource (elle transite par `area_resources`) la ou elle etait.
        zones_avant: Dict['CardFace', 'Deck'] = {}

        for paying_effect in paid_effects:
            paid = False
            for pay_info in payment.payments:
                if paying_effect in pay_info:
                    paid = True
                    expected_res = Resources.FromText(pay_info[paying_effect])
                    paying_effect.context.initiator = player
                    cost_check_effect = payment.cost_check[paying_effect]
                    # ⚠ LA PREMIERE ORIGINE GAGNE. Une meme carte peut porter
                    # DEUX effets payeurs d'un meme paiement ; au second tour
                    # elle est deja en zone de ressources, et enregistrer CETTE
                    # zone comme origine l'y laisserait bloquee.
                    if paying_effect.this not in zones_avant:
                        zones_avant[paying_effect.this] = paying_effect.this.card.area
                    message = Message.WhenPlayerPayingResources(player, paying_effect, for_effect, for_effect.targets, expected_res, cost_check_effect)
                    message.Send()
                    for cost_func in self._CoutsDuPayeur(paying_effect, cost_check_effect):
                        releves.append((paying_effect, cost_func, cost_func.SnapshotCost(paying_effect)))
                    paid_faces.append(paying_effect.this)
                    break
            if not paid:
                assert False, f"{paying_effect=} {for_effect=}"

        # for paying_effect in paying_effects:
        #     paying_effect.UnRegisterSelf()

        # LE POINT D'ABANDON. Tout ce qui precede est encore REVERSIBLE : les
        # cartes depensees attendent dans `area_resources` (rien n'est defausse
        # avant `DiscardResourcesArea`), et les couts des payeurs savent se
        # defaire (`CostFunc.RollbackCost`). C'est le dernier endroit ou rendre
        # ce qui a ete engage, et c'est donc ici que la reparation vit.
        if need_cost != None and not player.res_pool.Get().IsMatchCost(need_cost):
            self._RendreLePaiement(for_effect, releves, zones_avant)
            player.res_pool.Reset()
            return Resources("0")

        spent_message = Message.AfterCardsBeSpendAsResource(paid_faces, for_effect, player)
        spent_message.Send()

        for_effect.world.DiscardResourcesArea()

        resource = player.res_pool.Get()
        player.res_pool.Reset()

        return resource

    @staticmethod
    def _CoutsDuPayeur(paying_effect: 'Effect', cost_check_effect: 'Effect|None') -> List[Any]:
        """LES DEUX PORTEURS DE COUT d'un moyen de paiement, dedoublonnes.

        ⚠ Un moyen de paiement porte son `CostFunc` a l'un OU a l'autre de ses
        deux effets, et les deux sont payes :
        - sur `DoGenerateResources`, paye par `Effect.ProcessSelfCost` ;
        - sur `CanGenerateResources`, paye par `generate_resource` lui-meme,
          via `message.cost_check_effect.cost_func` (factory/resources.py).

        Ne regarder que le premier ne couvrait qu'UNE carte du jeu, `31001a`
        Sync Ratio -- celle sur laquelle ce correctif a ete mis au point.
        L'inclinaison est portee par `CanGenerateResources` sur 106 autres,
        dont `50044` Fury's Watch, la carte officielle donnee en preuve de
        generalite : le rendu ne l'aurait jamais redressee, ni meme signalee.
        """
        couts: List[Any] = []
        vus = set()
        for effect in (paying_effect, cost_check_effect):
            if effect == None:
                continue
            for cost_func in effect.cost_func.GetAll():
                if id(cost_func) in vus:
                    continue
                vus.add(id(cost_func))
                couts.append(cost_func)
        return couts

    def _RendreLePaiement(self, for_effect: 'Effect',
                          releves: Sequence[Tuple['Effect', Any, Any]],
                          zones_avant: Dict['CardFace', 'Deck']) -> None:
        """Rend au joueur tout ce qu'un paiement abandonne avait engage."""
        from game.operate.faces import Faces

        # 1. Toute carte qui a CHANGE DE ZONE pour payer retourne d'ou elle
        #    vient. C'est la carte de main depensee comme ressource : elle
        #    attend dans `area_resources` (celle de SON joueur -- un autre
        #    joueur peut aider a payer, « The Power of Leadership »), et sans
        #    ce retour elle y resterait bloquee, `DiscardResourcesArea`
        #    n'etant plus appelee sur un paiement abandonne. Comparer la zone
        #    a celle relevee avant le paiement, plutot que de balayer une
        #    zone de ressources precise, couvre les deux cas d'un coup.
        for face, origine in zones_avant.items():
            if face.card.area != origine:
                Faces.MoveAllTo([face], origine, for_effect)

        # 2. Les couts payes par les moyens de paiement (inclinaison...) se
        #    defont, a partir du RELEVE pris au moment ou ils ont paye. Un
        #    cout qui ne sait pas se defaire est JOURNALISE : on ne fait pas
        #    croire a un rendu complet.
        for paying_effect, cost_func, releve in releves:
            if not cost_func.RollbackCost(paying_effect, releve):
                Log.Assert(CATEGORY_NAME,
                           f"paiement abandonne : {cost_func} de {paying_effect} "
                           f"ne sait pas se defaire, son cout reste paye")

    def AskSpendResources(self, cost: 'Cost', by_effect: 'Effect') -> bool:
        paid_res = self.AskSpendResourcesInternal(cost, by_effect)
        return paid_res != None

    def AskSpendResourcesInternal(self, cost: 'Cost', by_effect: 'Effect') -> 'Resources|None':
        player = self.GetPlayer()

        effects = player.ChooseAbilities(
            by_effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                cost,
            )
        )
        if effects:
            return effects[0].context.paid_this_resources
        return None

    # Will ignore "Requirement"
    def PayCardPrintCost(self, face: 'HasCost', by_effect: 'Effect') -> 'Resources|None':
        player = self.GetPlayer()

        player.world.object_manager.ResetChooseEffect()
        ability = AbilityFactory.ForChoiceAbilityWithCost(
            face.printed_cost,
        )

        message = Message.WhenPlayerChooseAbility(player, by_effect, (1, 1), False)
        message.Send()
        # Fix "01072"
        effect = self.ChooseEffects([Effect(face, ability, world=by_effect.world)], message)
        if effect:
            return effect.context.paid_this_resources
        return None

    # def HasEnoughResources(self, cost: 'Resources'):
    #     return self.GetHasResource().IsMatchCost(cost)

    # Return from top to bottom
    def LookAtDeck(self, deck: 'Deck|Literal["EncounterDeck"]', num: int|Literal["2*"], by_effect: 'Effect', *, from_top: bool=True) -> List['CardFace']:
        from game.operate.faces import Faces
        from game.operate.worlds import Worlds

        player = self.GetPlayer()

        num = Worlds.ConvertPerPlayerIconToInt(num, by_effect)

        if deck == "EncounterDeck":
            deck = Worlds.GetEncounterDeck(by_effect)

        faces = deck.Get(from_top)[:num]
        Faces.LookAt(faces, player, by_effect)

        # reversed_face = faces[::-1]
        return faces

    def SwapTheseCards(self, faces: Sequence['CardFace'], by_effect: 'Effect'):
        from game.operate.faces import Faces
        def action(targets: Sequence['CardFace']):
            Faces.SwapTwoCards(targets, by_effect)

        while True:
            effect = self.MayChooseOneAbility(
                by_effect,
                AbilityFactory.ForChoiceAbility(
                    "Select 2 cards to swap",
                    action
                ).SetTargetInternal(Select.From(faces=faces, range=(2, 2), by_search=True, not_shuffle=True, not_move=True))
            )
            if effect == None:
                break
            if effect.world.is_game_over:
                break

