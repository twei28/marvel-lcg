from core import *
from game.card.face import *
from game.ability import *
from game.ability.factory import *
from game.message import *
from game.player import *
from cards.paper import Paper

@final
class MainScheme(Scheme2, HasStage, EncounterCard, FinalType):
    @override
    def __init__(self, paper: 'Paper') -> None:
        self.printed_target_threat: int|None = None
        self.target_threat = 0

        self.escalation_threat = 0
        self.is_completed = False

        super().__init__(paper)

        self.RegisterAttribute("TargetThreat", "printed_target_threat")
        self.RegisterAttribute("EscalationThreat", "escalation_threat")
        self.RegisterInfoDict('target_threat')
        self.RegisterInfoDict('escalation_threat')
        self.RegisterInfoDict('is_completed')

    @override
    def GetAbilities(self) -> List['Ability']:
        abilities: List['Ability'] = []
        if "<b>If this stage is completed, the players lose the game" in self.paper.text or \
            "<b>If this scheme is completed, the players lose the game" in self.paper.text:
            abilities = [
                AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame()
            ]
        return abilities + super().GetAbilities()

    @override
    def CheckPrintedValue(self):
        assert self.printed_target_threat == None or self.printed_target_threat >= 0
        assert self.escalation_threat >= 0
        return super().CheckPrintedValue()

    def ResetTargetThreat(self):
        self.target_threat = self.printed_target_threat

    @override
    def OnReset(self, message: 'Message.WhenCardReset_Text') -> None:
        self.ResetTargetThreat()
        self.is_completed = False
        return super().OnReset(message)

    @override
    def OnFlip(self, by_effect: 'Effect', origin_face: 'CardFace|None'):
        self.ResetTargetThreat()
        return super().OnFlip(by_effect, origin_face)

    @override
    def OnWhenCardRevealed(self, revealed_message: 'Message.WhenCardRevealed') -> None:
        if not self.IsInPlay():
            from game.effect.rule import GameRule
            first_player = self.card.world.GetFirstPlayer()
            self.PutIntoPlay(first_player, GameRule(self))
        # Une etape A se montre AVANT ses capacites « When Revealed » : le
        # joueur voit la manigance avant ce qu'elle met en jeu (Tower Defense,
        # The Armies of Thanos 2A et ses Black Order Besieger).
        if self == self.card.printed_faces[0] and self.card.world.rule.confirm_scheme_setup_order:
            self.card.world.ConfirmMainSchemeReveal(self)
        return super().OnWhenCardRevealed(revealed_message)

    @override
    def OnAfterCardRevealedEnd(self, message: 'Message.AfterCardRevealedEnd') -> None:
        from game.effect.rule import Advance

        if self == self.card.printed_faces[0]:
            if self.printed_target_threat == None:
                effect = Advance(self)
                self.Advance(None, effect)
        return super().OnAfterCardRevealedEnd(message)

    @override
    def OnPutIntoPlay(self, message: 'Message.WhenCardPutIntoPlay') -> 'bool':
        from game.operate.faces import Faces
        world = self.card.world
        if self.card.area == world.area_schemes_main or \
            Faces.MoveAllTo([self], world.area_schemes_main, message.by_effect):
            return super().OnPutIntoPlay(message)
        else:
            return False

    ################################################################################
    #
    def Phase(self) -> None:
        # "21098a"
        # This scenario has two main scheme cards in play at the 
        # same time: Stage 1B and Stage 2B. Both main schemes 
        # are active each round. Encounter cards that refer to “the 
        # main scheme” refer to both main scheme cards. Each 
        # main scheme gains threat during step 1 of the villain 
        # phase, and they are each affected by any acceleration 
        # and crisis icons in play.
        # When a someone plays a card that refers to “the main 
        # scheme,” that card’s controller must choose which of the 
        # two schemes it is referring to. If a constant effect on a 
        # player card refers to “the main scheme,” that card always 
        # refers to the scheme card with the attachment “Focused 
        # Defense” attached to it.

        # This scenario has two villains: Proxima Midnight and 
        # Corvus Glaive. Each of these villains is paired with one 
        # of the main schemes. Stage 1B is identified as Proxima 
        # Midnight’s scheme, and stage 2B is identified as Corvus 
        # Glaive’s scheme. When either of the two villains schemes, 
        # place the threat on their matching main scheme card 
        # only. For example, when Proxima Midnight schemes, 
        # place the threat only on stage 1B. 
        from game.message import Message
        from game.effect.rule import MainSchemePhasePlaceThreat
        from game.operate.worlds import Worlds

        acceleration_icons: List['HasAccelerationIcon'] = []
        acceleration_tokens: List['CanAccelerationToken'] = []

        for face in Worlds.GetAccelerationIconFaces(self.card.GetGameArea()):
            acceleration_icons.append(face)

        for face in Worlds.GetAccelerationTokenFaces(self.card.GetGameArea()):
            # 21-the_mad_titans_shadow_rulebook
            # SCENARIO #2 - TOWER DEFENSE
            # This scenario has two main scheme cards in play at the
            # same time: Stage 1B and Stage 2B. Both main schemes
            # are active each round. Encounter cards that refer to “the
            # main scheme” refer to both main scheme cards. Each
            # main scheme gains threat during step 1 of the villain
            # phase, and they are each affected by any acceleration
            # and crisis icons in play.
            acceleration_tokens.append(face)

        message = Message.CalcMainSchemeEscalation(self, self.escalation_threat, acceleration_icons, acceleration_tokens)
        message.Send()

        place_message = self.PlaceThreatInternal(message.escalation_threat, MainSchemePhasePlaceThreat(self))

        # Journal de la phase du mechant (voir WorldStat.RecordFaitMechant) :
        # le POINT 1 de la carte de reference y inscrit sa pose de menace.
        #
        # ICI, et nulle part ailleurs. `Phase()` n'a qu'un seul appelant,
        # `place_threat()` dans world.VillainPhase (game/world/world.py), qui
        # la joue une fois par manigance principale a l'etape 1 : un fait par
        # evenement, sans doublon possible. Les autres poses de menace (une
        # carte revelee, un sbire qui complote) passent par
        # `PlaceThreatInternal` sans passer par `Phase()` — elles
        # n'appartiennent pas au point 1, et le journal les couvre deja par
        # ailleurs (`can_attack.JournaliserManigance`).
        #
        # `place_message` est absent quand rien n'a ete pose (escalade nulle,
        # ou pose remplacee par un autre effet) : pas de menace, pas de fait,
        # et le cartouche du plateau se tait plutot que d'annoncer un « +0 ».
        #
        # Le dictionnaire est construit POUR CET APPEL : `RecordFaitMechant`
        # en fait sa propre copie, rien n'est mute ici.
        if place_message is not None:
            world = self.card.world
            # La DECOMPOSITION du montant (cartouche, 04/10/2026) : « 1 par
            # joueur + 1 acceleration = 2 ». `escalade` est la valeur passee a
            # `CalcMainSchemeEscalation`, `acceleration` tout ce qu'il y a
            # ajoute (icones, jetons, effets de carte). Sous garde : un journal
            # d'affichage ne doit pas pouvoir interrompre la phase.
            try:
                decomposition = {
                    'escalade': self.escalation_threat,
                    'acceleration': message.escalation_threat - self.escalation_threat,
                    'joueurs': world.GetPlayerNumIcon(),
                }
            except Exception:
                decomposition = {}
            world.stat.RecordFaitMechant(world.round_id, {
                'genre': 'menace',
                'phase': world.GetPhaseText(),
                'cible': self.name,
                'cible_id': self.card.object_id,
                # La menace REELLEMENT posee, apres remplacements et
                # modificateurs : `AfterSchemePlaceThreat.value`, pas la
                # valeur demandee.
                'montant': place_message.value,
                # L'etat de la manigance APRES la pose, seuil compris : le
                # client affiche « 3/12 » sans relire la carte, qui a pu
                # avancer de stade dans la foulee de cette meme pose.
                'restant': self.threat,
                'plafond': self.target_threat,
                **decomposition,
                # 13/10/2026 : les cartes qui ont reduit cette pose, et de combien.
                **world.stat.ChampReductions(world, self.card.object_id),
            })

    def Advance(self, to_face: Literal["2A", "3A"]|CardFace|None, by_effect: 'Effect') -> None:
        self.card.world.AdvanceMainScheme(self, to_face, by_effect)

    ################################################################################
    #
    @override
    def RemoveThreatInternal(self, by_face: 'CardFace', value: Literal["All"]|INT_TYPE, by_effect: 'Effect', thw_message: 'Message.WhenSchemeBeingThwart|None' = None) -> int:
        from game.operate.worlds import Worlds
        ignored_crisis = False
        ignored_patrol = False

        crisis_faces = Worlds.GetCrisisFaces(self.card.GetGameArea())
        if crisis_faces:
            if not by_effect.IsIgnoreKeyword('Crisis', by_effect):
                message = Message.IconsActivate_Text(self, crisis_faces, 'Crisis')
                message.Send()
                return 0
            else:
                ignored_crisis = True

        patrol_faces: Sequence[CardFace] = []
        if by_effect.IsIgnoreKeyword('Patrol', by_effect):
            patrol_faces = MainScheme.GetPatrolFaces(by_effect)
            if patrol_faces:
                ignored_patrol = True
        elif getattr(by_effect.context, 'patrouille_levee_au_ciblage', False) and by_effect.IsPlayerInitiator():
            # CORRECTIF (20/10/2026, gs315 Quantum Jump de Quasar ; vaut aussi
            # pour hc006 On the Prowl) : la Patrouille ne verrouillait qu'AU
            # CIBLAGE (`CanBeThwartBy` plus bas). Une carte dont l'ignorance
            # DEPEND DU PAIEMENT (rien n'est paye au ciblage : la cible reste
            # offerte) n'etait jamais rattrapee a la resolution : payee sans
            # la ressource voulue, elle contrecarrait quand meme le complot
            # principal sous Patrouille. Meme verrou que la Crise ci-dessus,
            # mais SEULEMENT pour un effet dont le ciblage a franchi la
            # Patrouille grace a une ignorance : tout le reste est inchange.
            patrouilleurs = MainScheme.GetPatrolFaces(by_effect)
            if patrouilleurs:
                message = Message.IconsActivate_Text(self, patrouilleurs, 'Patrol')
                message.Send()
                return 0

        ret_value = super().RemoveThreatInternal(by_face, value, by_effect, thw_message)

        if ignored_crisis:
            ignore_message = Message.AfterIgnoreKeywordOnCard(by_face, crisis_faces, "Crisis")
            ignore_message.Send()

        if ignored_patrol:
            ignore_message = Message.AfterIgnoreKeywordOnCard(by_face, patrol_faces, "Patrol")
            ignore_message.Send()

        return ret_value

    @override
    def PlaceThreatInternal(self, value: INT_TYPE, by_effect: 'Effect', sch_message: 'Message.WhenUnitWouldScheme|None'=None) -> 'Message.AfterSchemePlaceThreat|None':
        from game.effect.rule import Advance
        from game.message import Message
        place_message = super().PlaceThreatInternal(value, by_effect, sch_message)
        # Defaut corrige le 07/09/2026 (audit A4, Important 1 releve par la
        # relecture d'A2) : cette methode rendait `None` des que
        # `target_threat` valait `None`, MEME quand la menace avait bien ete
        # posee (`place_message` non vide). `MainScheme.Phase()`
        # (scheme_main.py plus haut) se fie a ce retour pour savoir s'il faut
        # inscrire le fait de menace du journal (`RecordFaitMechant`) : le
        # garde sautait alors l'ecriture pour les manigances SANS seuil (pas
        # de `TargetThreat` imprime), par exemple `32063b` Stalked by
        # Sabretooth. Le controle du seuil reste EXCLUSIVEMENT conditionne a
        # `target_threat`, qui garde tout son sens (pas de seuil, pas
        # d'accomplissement) : seul le RETOUR reflete desormais ce que la
        # pose a reellement fait, seuil ou non.
        if place_message and self.target_threat != None:
            if self.threat >= self.target_threat and not self.is_completed:
                would_complete_message = Message.WhenMainSchemeStageWouldBeCompleted(self, sch_message)
                would_complete_message.Send()
                if not would_complete_message.is_be_instead:
                    self.is_completed = True
                    when_complete_message = Message.WhenMainSchemeStageCompleted(self, would_complete_message)
                    when_complete_message.Send()
                    effect = Advance(self)
                    self.Advance(None, effect)
                    after_message = Message.AfterMainSchemeCompleted(self, when_complete_message)
                    after_message.Send()
        return place_message

    @staticmethod
    def GetPatrolFaces(effect: 'Effect') -> Sequence['CardFace']:
        if effect.initiator.IsPlayer():
            return [x for x in effect.GetInitiator().GetEngagedMinions() if x.IsPatrol()]
        else:
            return []

    @override
    def CanBeThwartBy(self, effect: 'Effect') -> bool:
        from game.operate.worlds import Worlds
        main_scheme = Worlds.FindMainScheme(self)
        if main_scheme == self:
            if MainScheme.GetPatrolFaces(effect) != []:
                if not effect.IsIgnoreKeyword('Patrol', effect) and effect.IsPlayerInitiator():
                    return False
                # CORRECTIF (20/10/2026) : note que CE ciblage a franchi la
                # Patrouille grace a une ignorance, pour la reverifier a la
                # resolution (RemoveThreatInternal plus haut). Remis a faux
                # par `EffectContext.ResetAfterOperation`.
                if effect.IsPlayerInitiator():
                    effect.context.patrouille_levee_au_ciblage = True
            # CRISE : meme verrou que Patrouille juste au-dessus, ajoute le
            # 11/09/2026 apres un rapport de joueur.
            #
            # ⚠ POURQUOI IL MANQUAIT, ET CE QUE CA COUTAIT. La Crise etait la
            # SEULE des trois icones de verrouillage a ne bloquer qu'A LA
            # RESOLUTION (`RemoveThreatInternal` plus haut rend 0). Garde
            # bloque au ciblage (`Villain.CanBeAttackBy`), Patrouille aussi
            # (ligne du dessus) ; la Crise laissait donc CHOISIR le complot
            # principal, puis ne retirait rien : la carte partait en defausse
            # pour rien, sans un mot. Un joueur l'a signale, et avait rejoue
            # trois fois le meme coup en croyant a un bug d'annulation.
            #
            # La condition est la MEME que celle de la resolution, sans
            # `IsPlayerInitiator()` : une divergence entre ce qu'on propose et
            # ce qu'on resout serait pire que le trou d'origine.
            # `IsIgnoreKeyword` couvre deja les cartes de rencontre
            # (`encounter_cards_ignore_crisis`, effect.py:484).
            if Worlds.GetCrisisFaces(self.card.GetGameArea()):
                if not effect.IsIgnoreKeyword('Crisis', effect):
                    return False
        return super().CanBeThwartBy(effect)

    def GainTargetThreatValue(self, value: int, effect: 'Effect'):
        # AJOUT (20/10/2026, Galactic Storm gs198b Protectors of the Kree Empire) : « The target threat
        # value of this scheme cannot be changed. » Toute modification (ajout ET retrait d'un bonus) est
        # ignoree, ce qui garde l'aller-retour symetrique. Meme lecture du texte imprime que la regle
        # « If this stage is completed, the players lose the game » (GetAbilities ci-dessus).
        if "target threat value of this scheme cannot be changed" in self.paper.text:
            return
        if self.target_threat != None:
            self.target_threat += value

