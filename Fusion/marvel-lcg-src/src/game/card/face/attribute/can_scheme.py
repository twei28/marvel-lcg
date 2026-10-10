from . import *

@dataclass
class SchemeProperty(PowerProperty):
    do_not_give_boost: bool = field(default=False)
    against_player: 'Player|None' = field(default=None)
    would_act_message: 'Message.WhenEnemyWouldActivate|None' = field(default=None)
    give_additional_boost: int = field(default=0)

    def GetScheme(self, this: 'CardFace') -> int:
        value = 0
        if self.is_basic_power:
            if HasScheme.IsType(this):
                value = this.scheme
        return self.additional_value + value

class HasScheme(HasAttribute):
    @override
    def __init__(self, paper: 'Paper') -> None:
        self.base_scheme = 0
        self.printed_scheme = 0

        super().__init__(paper)

        self.RegisterAttribute("SCH", "printed_scheme")
        self.RegisterInfoDict('scheme')

    @override
    def OnResetKeywords(self, by_effect: 'Effect'):
        self.base_scheme = self.printed_scheme
        self.GainScheme(self.base_scheme, by_effect)
        return super().OnResetKeywords(by_effect)

    @final
    def SetBaseScheme(self, value: int, by_effect: 'Effect'):
        if self.base_scheme != value:
            diff = value - self.base_scheme
            self.base_scheme = value
            self.GainScheme(diff, by_effect)

    @final
    def GainScheme(self, diff: int, by_effect: 'Effect', *, render_ui: bool=False):
        self.GainKeyword(diff, 'SCH', by_effect, render_ui=render_ui)

    @property
    def scheme(self) -> int:
        return max(0, self.GetKeyword('SCH'))

################################################################################
#
class CanScheme(CardFace):
    
    def SchemesInternal(self, by_effect: 'Effect', property: SchemeProperty) -> 'Message.AfterUnitSchemeEnd|None':
        from game.message import Message
        from game.card.face.attribute.can_boost import CanBoost
        from game.card.face.base import Unit2
        from game.card.face.base import Enemy
        from game.effect.rule import GameRule, SchemeActive
        from game.operate.worlds import Worlds

        is_base_scheme = property.is_basic_power

        this = self.card.CastTo(Unit2)
        assert Unit2.IsType(this), f"{this=}"

        target_scheme = None
        if Enemy.IsType(this):
            check_scheme_message = Message.GettingEnemySchemeTarget(this, by_effect)
            check_scheme_message.Send()
            if check_scheme_message.target_scheme:
                target_scheme = check_scheme_message.target_scheme

        # ANNONCE de l'activation (fait d'INTENTION, lu par ui-app). Meme place
        # et meme raison que dans can_attack.py : juste avant le message qui
        # ouvre la fenetre d'interruption, et avant que les boosts soient
        # retournes. Les deux moities de la meme notion cote joueur — un ennemi
        # qui s'active — vivent aux memes endroits des deux cotes.
        from game.card.face.attribute.can_attack import CanAttack
        annonce_cible = target_scheme or Worlds.FindMainScheme(self)
        annonce_base = this.scheme if HasScheme.IsType(this) else 0
        annonce_id = CanAttack.AnnoncerActivation(
            this, annonce_cible, 'manigance', annonce_base,
            is_base_scheme, by_effect,
        )

        def cloturer_annonce_non_resolue(par: 'Effect|None' = None) -> None:
            """La manigance annoncee n'a pas eu lieu : on ferme l'intention."""
            nonlocal annonce_id
            if not annonce_id:
                return
            identifiant, annonce_id = annonce_id, 0
            CanAttack.AnnulerActivation(this, annonce_cible, 'manigance', identifiant, by_effect, par)

        would_sch_message = Message.WhenUnitWouldScheme(this, by_effect, property=property)
        would_sch_message.Send()
        if would_sch_message.is_be_instead:
            cloturer_annonce_non_resolue(would_sch_message.be_instead_by)
            return None

        if Enemy.IsType(this):
            activate_message = Message.WhenEnemyActivateAgainstYou(this, property.against_player, by_effect, would_sch_message, property.would_act_message)
            activate_message.Send()
        else:
            activate_message = None

        if is_base_scheme:
            unit = this.card.CastTo(Unit2)
            use_basic_power_message = Message.WhenUnitUseBasicPower(unit, "SCH", would_sch_message)
            use_basic_power_message.Send()
        else:
            use_basic_power_message = None

        if is_base_scheme and CanBoost.IsType(this) and not property.do_not_give_boost:
            boost_size = this.GetBoostCardNum(would_sch_message) + property.give_additional_boost
            this.GiveFacedownBoostCardsInternal(boost_size, GameRule(this), would_sch_message)

        main_scheme = Worlds.FindMainScheme(self)
        if not main_scheme:
            cloturer_annonce_non_resolue()
            return None

        boost_cards: List['CardFace'] = []
        # Ce que chaque carte de boost a ajoute — voir can_attack.py, meme
        # raison : le total seul ne se decompose plus apres coup.
        boost_apports: List[Tuple[str, int, int]] = []
        if is_base_scheme:
            # assert property.base_value == this.scheme
            being_sch_message = Message.WhenSchemeBeingScheme(main_scheme, would_sch_message)
            being_sch_message.Send()

            def gain_sch(face: CardFace, boost_value: int) -> None:
                nonlocal boost_cards
                boost_cards.append(face)
                boost_apports.append((face.name, face.card.object_id, boost_value))
                this.card.CastTo(Unit2).GainForThisActive(
                    GameRule(face),
                    would_sch_message,
                    scheme=boost_value,
                    render_ui=True
                )

            if CanBoost.IsType(this):
                this.ResolveBoostCards(being_sch_message, gain_sch)
                if Worlds.IsGameOver(by_effect):
                    cloturer_annonce_non_resolue()
                    return None

        this = this.CastTo(Unit2)
        value = property.GetScheme(this)

        if not target_scheme:
            target_scheme = Worlds.FindMainScheme(self)
        if not target_scheme:
            cloturer_annonce_non_resolue()
            return None

        recalculate = Message.WhenRecalculateSchemeValue(this, target_scheme, value, would_sch_message)
        recalculate.Send()
        value = recalculate.value

        # ETAT INTERMEDIAIRE (fait `boosts`, voir can_attack.py) : les boosts
        # sont retournes, la menace n'est pas encore posee. Jamais de defenseur.
        CanAttack.JournaliserBoosts(
            this, annonce_cible, 'manigance', annonce_id, annonce_base, None, 0,
            boost_apports, boost_cards, value, by_effect,
        )

        # La menace AVANT la pose : une manigance qui atteint son seuil peut se
        # vider dans la foulee (21099b), `restant` seul ne dit plus d'ou elle partait.
        menace_avant = getattr(target_scheme, 'threat', None)
        if would_sch_message.remove_threat_instead_of_placing:
            target_scheme.RemoveThreatInternal(this, value, would_sch_message.remove_threat_instead_of_placing)
            value *= - 1
        else:
            target_scheme.PlaceThreatInternal(value, SchemeActive(this), would_sch_message)
        # Journal du bilan de phase (ajout local, lu par ui-app), sous garde :
        # un journal d'affichage n'a pas a pouvoir interrompre une activation.
        try:
            journalise = CanAttack.JournaliserManigance(
                this, target_scheme, is_base_scheme, boost_apports, value, by_effect,
                activation_id=annonce_id, boost_cards=boost_cards,
                cible_annoncee=annonce_cible, base_imprimee=annonce_base,
                menace_avant=menace_avant,
            )
            # L'intention n'est CONSOMMEE que si un fait resolu a vraiment pris
            # sa place : `JournaliserManigance` a ses propres gardes et sort
            # alors sans rien inscrire. Meme raison que dans can_attack.py.
            if journalise:
                annonce_id = 0
        except Exception:
            pass

        # this.PlaceThreatOnSchemes([scheme], value, by_effect) # if we call this, the UI is strange with "01186"
        end_message = Message.AfterUnitSchemeEnd(this, value, target_scheme, boost_cards, by_effect, [would_sch_message])
        end_message.Send()

        if activate_message:
            assert Enemy.IsType(this)
            after_activate_message = Message.AfterEnemyActivationEnd(this, end_message, activate_message)
            after_activate_message.Send()

        if use_basic_power_message and not this.IsDefeated():
            unit = this.card.CastTo(Unit2)
            after_use_basic_power_message = Message.AfterUnitUseBasicPower(unit, "SCH", end_message, use_basic_power_message)
            after_use_basic_power_message.Send()
        return end_message

    def BasicSchemes(self, by_effect: 'Effect', *, property: 'SchemeProperty|None' = None) -> 'Message.AfterUnitSchemeEnd|None':
        if not self.IsCanScheme():
            return None
        if property == None:
            property = SchemeProperty(is_basic_power=True)
        else:
            property.is_basic_power = True
        message = self.SchemesInternal(by_effect, property)
        return message

    def IsCanScheme(self) -> bool:
        return self.IsInPlay()

