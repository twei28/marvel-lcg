from . import *

class CanStatus(HasVulnerable, HasSteady, HasToughness, HasStalwart):
    BASE_MAX_TOUGH = 1

    DISCARD_RULE = Literal["All", "Steady"]|int

    @override
    def __init__(self, paper: 'Paper') -> None:
        super().__init__(paper)

    def ResetStates(self):
        self.components.status.OnParentReset()

    @override
    def OnReset(self, message: 'Message.WhenCardReset_Text') -> None:
        if not message.is_flip:
            self.ResetStates()
        return super().OnReset(message)

    @override
    def OnAfterCardLeavePlay(self, message: 'Message.AfterCardLeavePlay') -> None:
        self.ResetStates()
        return super().OnAfterCardLeavePlay(message)

    ################################################################################
    #
    @property
    def confused(self) -> int:
        return self.components.status.confused
    @property
    def stunned(self) -> int:
        return self.components.status.stunned
    @property
    def tough(self) -> int:
        return self.components.status.tough
    @property
    def exposed(self) -> int:
        # CORRECTIF (12/09/2026, pack `sentinel`) : quatrieme carte d'etat.
        return self.components.status.exposed
    @property
    def cloaked(self) -> int:
        return self.components.status.cloaked
    @property
    def dazed(self) -> int:
        return self.components.status.dazed
    @property
    def intensified(self) -> int:
        # AJOUT (16/10/2026) : 7e carte d'etat, Intensified (TMNT, Inkwire).
        return self.components.status.intensified

    @property
    def tough_max(self) -> int:
        from game.message import Message
        from game.card.face.base import Unit2

        value = CanStatus.BASE_MAX_TOUGH
        message = Message.GettingUnitAdditionalTough(self.card.CastTo(Unit2))
        message.Send()
        additional = message.return_value
        if additional:
            value += additional
        return value

    @property
    def cloaked_max(self) -> int:
        # CORRECTIF (pack shredder) : un personnage n'a qu'UNE carte Cloaked,
        # sauf mention contraire (Shredder : 2, 3 ou 4 selon son stade).
        from game.message import Message
        from game.card.face.base import Unit2

        value = 1
        message = Message.GettingUnitAdditionalCloaked(self.card.CastTo(Unit2))
        message.Send()
        if message.return_value:
            value += message.return_value
        return value

    # @property
    # def stun_max(self) -> int:
    #     return 1

    # @property
    # def confuse_max(self) -> int:
    #     return 1

    # @staticmethod
    # def ToCounterName(name: str) -> 'CardFace.COUNTER':
    #     return Cast(CardFace.COUNTER, {
    #         'Confused': 'confused',
    #         'Stunned': 'stunned',
    #         'Tough': 'tough',
    #     }[name])

    def GainStatus(self, name: "CardFace.STATUS", by_effect: 'Effect') -> bool:
        from game.message import Message
        from game.operate.faces import Faces
        from game.effect.rule import GameRule

        if not self.card.IsOnField():
            #  or self.card.face.IsDefeated():
            return False
        # BRIQUE 2 (20/10/2026) : une carte joueur ne pose aucun etat sur une
        # face insensible aux cartes joueur (Galactic Storm p.14).
        from game.operate.immunity import PlayerCardImmunity
        if PlayerCardImmunity.Refuses(self, by_effect):
            return False
        # assert name in ['tough', 'stunned', 'confused'], f"{name=}"

        # AJOUT (16/10/2026, te201 Intense Combatants) : « When a status card would be
        # placed on a character, if that character ALREADY HAS 1 COPY of that status
        # card on them, intensify them instead. » La fenetre s'ouvre AVANT les plafonds
        # (Stunned/Confused/Dazed : un seul ; Tough : tough_max ; Cloaked : cloaked_max),
        # sans quoi le second Sonne, refuse par `CanbeStunned`, n'atteindrait jamais
        # te201. Message DISTINCT de `WhenStatusWouldCardPlaceOn` : les cartes qui
        # repondent a une pose reelle (56175 Spider-Woman, ah006) ne doivent pas voir
        # une pose que le plafond aurait de toute facon refusee. Intensified elle-meme
        # n'est jamais « intensifiee » (sans quoi la seconde Intensified bouclerait).
        if name != "Intensified" and self.HasStatus(name):
            encore = Message.WhenStatusWouldCardPlaceOnAgain(self, name, by_effect)
            encore.Send()
            if encore.is_be_instead:
                return False

        # AJOUT (16/10/2026) : « This card cannot be given to a character that has no
        # status cards » (carte d'etat Intensified). Plafond 1, 2 si Steady (CanbeIntensified).
        if name == "Intensified" and not self.CanbeIntensified():
            return False
        if name == "Confused" and not self.CanbeConfused():
            return False
        if name == "Stunned" and not self.CanbeStunned():
            return False
        if name == "Tough" and self.IsTough() and self.tough >= self.tough_max:
            return False
        # AJOUT (16/10/2026, Baxter Stockman v3) : « a character can only have one Dazed
        # status card on them » (insert Dazed). Ni Stalwart ni Steady n'y changent rien
        # (insert : « Can I Daze a steady/stalwart character? Yes »).
        if name == "Dazed" and not self.CanbeDazed():
            return False
        if name == "Cloaked" and self.cloaked >= self.cloaked_max:
            return False

        would_message = Message.WhenStatusWouldCardPlaceOn(self, name, by_effect)
        would_message.Send()
        if would_message.is_be_instead:
            return False

        status_face = self.components.status.GiveStatusCard(name, by_effect)
        placed_message = Message.AfterStatusCardPlaceOn(status_face, would_message)
        placed_message.Send()

        if self.CastTo(HasVulnerable).IsVulnerable():
            if self.IsStunned() or self.IsConfused():
                rule = GameRule(self)
                Faces.DiscardAll([self], rule)
        return True

    def LoseState(self, name: "CardFace.STATUS", by_effect: 'Effect', rule: DISCARD_RULE) -> int:
        if not self.card.IsOnField():
            return False
        # BRIQUE 2 (20/10/2026) : une carte joueur ne defausse aucun etat d'une
        # face insensible aux cartes joueur, Robuste par perforant compris
        # (Galactic Storm p.14). Retourne 0 : rien n'a ete defausse.
        from game.operate.immunity import PlayerCardImmunity
        if PlayerCardImmunity.Refuses(self, by_effect):
            return 0
        return self.components.status.DiscardStatusCard(name, by_effect, rule)

    # def GainConfused(self, by_effect: 'Effect') -> bool:
    #     return self.GainStatus("Confused", by_effect)
    # def GainStunned(self, by_effect: 'Effect') -> bool:
    #     return self.GainStatus("Stunned", by_effect)
    # def GainTough(self, by_effect: 'Effect') -> bool:
    #     return self.GainStatus("Tough", by_effect)

    def DiscardConfused(self, by_effect: 'Effect', *, rule: 'DISCARD_RULE') -> int:
        return self.LoseState("Confused", by_effect, rule)
    def DiscardStunned(self, by_effect: 'Effect', *, rule: 'DISCARD_RULE') -> int:
        return self.LoseState("Stunned", by_effect, rule)
    def DiscardTough(self, by_effect: 'Effect', *, rule: 'DISCARD_RULE') -> int:
        return self.LoseState("Tough", by_effect, rule)

    def DiscardCloaked(self, by_effect: 'Effect', *, rule: 'DISCARD_RULE') -> int:
        return self.LoseState("Cloaked", by_effect, rule)

    def DiscardDazed(self, by_effect: 'Effect', *, rule: 'DISCARD_RULE') -> int:
        return self.LoseState("Dazed", by_effect, rule)

    def DiscardIntensified(self, by_effect: 'Effect', *, rule: 'DISCARD_RULE') -> int:
        return self.LoseState("Intensified", by_effect, rule)

    def DiscardAllTough(self, by_effect: 'Effect') -> int:
        return self.DiscardTough(by_effect, rule="All")

    def DiscardEachStatus(self, by_effect: 'Effect'):
        # AJOUT (16/10/2026) : « defaussez CHAQUE carte d'etat » emporte aussi les
        # Intensified, et elles ne remplacent rien pendant ce vidage (`vidage`), sans
        # quoi le premier Desoriente defausse serait remplace et resterait en place.
        status = self.components.status
        status.vidage += 1
        try:
            self.DiscardConfused(by_effect, rule="All")
            self.DiscardStunned(by_effect, rule="All")
            self.DiscardAllTough(by_effect)
            self.DiscardCloaked(by_effect, rule="All")
            self.DiscardDazed(by_effect, rule="All")
            self.DiscardIntensified(by_effect, rule="All")
        finally:
            status.vidage -= 1

    def IsConfused(self) -> bool:
        from game.card.face.base import Unit2
        if self.card.CastTo(Unit2).IsSteady():
            return self.confused > 1
        else:
            return self.confused > 0
    def IsTough(self) -> bool:
        return self.tough != 0
    def IsCloaked(self) -> bool:
        return self.cloaked != 0
    def IsDazed(self) -> bool:
        return self.dazed != 0
    def IsIntensified(self) -> bool:
        return self.intensified != 0
    def IsStunned(self) -> bool:
        from game.card.face.base import Unit2
        if self.card.CastTo(Unit2).IsSteady():
            return self.stunned > 1
        else:
            return self.stunned > 0

    def CanGainTough(self) -> bool:
        if not self.IsInPlay():
            return False
        return self.tough < self.tough_max

    def CanbeDazed(self) -> bool:
        """Un seul Dazed par personnage (insert Dazed) ; ni Stalwart ni Steady n'interviennent."""
        if not self.IsInPlay():
            return False
        if self.IsDazed():
            return False
        return True

    def CanbeIntensified(self) -> bool:
        """« This card cannot be given to a character that has no status cards. »
        Plafond : decision de l'utilisateur (16/10/2026), Intensified suit les regles des
        cartes d'etat : UNE par personnage, DEUX pour un personnage Solide (Steady),
        comme Sonne / Desoriente."""
        from game.card.face.base import Unit2
        if not self.IsInPlay():
            return False
        if self.GetStatusSize() == 0:
            return False
        plafond = 2 if self.card.CastTo(Unit2).IsSteady() else 1
        return self.intensified < plafond

    def CanbeStunned(self) -> bool:
        if not self.IsInPlay():
            return False
        if self.IsStalwart():
            return False
        if self.IsStunned():
            return False
        if self.GetBuff(BuffCannotBeStunned):
            return False
        return True

    def CanbeConfused(self) -> bool:
        if not self.IsInPlay():
            return False
        if self.IsStalwart():
            return False
        if self.IsConfused():
            return False
        if self.GetBuff(BuffCannotBeConfused):
            return False
        return True

    ################################################################################
    #
    # def CopyStates(self, unit: 'Unit2') -> bool:
    #     from game.card.face.component.unit_state import UnitState
    #     if self.GetComponent(UnitState).CopyStates(unit.GetComponent(UnitState)):
    #         Send.UnitCopyState_Text(self, unit)
    #         return True
    #     else:
    #         return False

    def HasStatus(self, name: "CardFace.STATUS|Literal['Any']") -> bool:
        if name == "Any":
            # CORRECTIF (12/09/2026, pack `sentinel`) : « Exposed » compte
            # parmi les statuts. Sans lui, `has_status="Any"` aurait ignore la
            # quatrieme carte d'etat, et l'assertion plus bas aurait fait
            # PLANTER toute carte qui demande `HasStatus("Exposed")`.
            return self.confused > 0 or self.stunned > 0 or self.tough > 0 \
                or self.exposed > 0 or self.cloaked > 0 or self.dazed > 0 \
                or self.intensified > 0
        if name == "Confused":
            return self.confused > 0
        if name == "Stunned":
            return self.stunned > 0
        if name == "Tough":
            return self.tough > 0
        if name == "Exposed":
            return self.exposed > 0
        if name == "Cloaked":
            return self.cloaked > 0
        if name == "Dazed":
            return self.dazed > 0
        if name == "Intensified":
            return self.intensified > 0
        assert False, f"{self=} {name=}"

    def GetStatusSize(self) -> int:
        return self.components.status.GetStatusSize()

class CanNoStatus(CanStatus):
    @override
    def CanGainTough(self) -> bool:
        return False

    @override
    def CanbeStunned(self) -> bool:
        return False

    @override
    def CanbeConfused(self) -> bool:
        return False

    @override
    def CanbeDazed(self) -> bool:
        return False

    @override
    def CanbeIntensified(self) -> bool:
        return False
