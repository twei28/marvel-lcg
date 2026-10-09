from cards.pack import *
from cards.pack.hunting_season.trap import *

ID_KRAVEN = ("hs104", "hs105", "hs106")
ID_DERNIER_FILS = "hs109"


def Vilain(effect: 'Effect') -> 'Villain|None':
    return Worlds.FindCardOnField(effect, card_type=Villain)


def Kraven(effect: 'Effect') -> 'Villain|None':
    v = Vilain(effect)
    return v if v is not None and any(v.IsCardId(i) for i in ID_KRAVEN) else None


def AttacherAKraven(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
    v = Kraven(effect)
    if v is None or not effect.this.CastTo(Attachment).AttachTo2(v, effect):
        Faces.DiscardAll([effect.this], effect)


def AttacherALaRevelation() -> 'Ability':
    return AbilityFactory.WhenThisRevealed(None, AttacherAKraven)


def PorteurEstAttaquant(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
    cible = effect.this.CastTo(Attachment).bind_face
    return cible is not None and message.attacker is cible


def CiblePorteur(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
    cible = effect.this.CastTo(Attachment).bind_face
    return cible is not None and cible in message.attacked_targets


def AttaqueContreLeJoueur(message: 'Message.WhenUnitWouldAttack') -> 'Player|None':
    joueur = message.property.against_player
    if joueur is None:
        return None
    return joueur if message.HasTarget(joueur.GetIdentity()) else None


def SiLAttaqueVousBlesse(effect: 'Effect', message: 'Message.WhenCardBecomeBoost', action: 'Callable[[Player, int], None]') -> None:
    joueur = message.GetToPlayer()
    identite = joueur.GetIdentity()
    avant = identite.health

    def apres() -> None:
        degats = avant - identite.health
        if degats > 0:
            action(joueur, degats)

    message.AfterThisActivation(effect, apres)


def PiegeSurAttaque(maximum: int, reveler: bool) -> 'Ability':
    """Forced Interrupt : quand un personnage que vous controlez attaque cette carte, distribue un piege (et les revele tous pour Kraven)."""

    def joueur_de(message: 'Message.WhenUnitWouldAttack') -> 'Player|None':
        return message.attacker.GetControlByPlayer()

    def limite_libre(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        joueur = joueur_de(message)
        if joueur is None:
            return False
        return LimiteParJoueurEtParRound(effect, joueur, effect.this.paper.card_id, maximum, consommer=False)

    def distribuer(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        joueur = joueur_de(message)
        LimiteParJoueurEtParRound(effect, joueur, effect.this.paper.card_id, maximum, consommer=True)
        DonnerPiege(effect, joueur)
        if reveler:
            RevelerPiegesDistribues(effect, joueur)

    return AbilityFactory.WhenUnitWouldBeAttacked(AbilityType.ForcedInterrupt, "This", distribuer, conditions=[limite_libre])


def DonnerPiegeATous(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
    Players.ForEachPlayer(effect, lambda joueur: DonnerPiege(effect, joueur))


def DefausserCetAttachement(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
    Faces.DiscardAll([effect.this], effect)


def InterruptContrePorteur(cout: 'Cost|None'=None, *fonctions: 'CostFunc.Base') -> 'Ability':
    """Interrupt : quand vous attaquez le porteur (Kraven), payez le cout → defaussez cet attachement."""
    ab = AbilityFactory.WhenUnitWouldAttack(AbilityType.HeroInterrupt, "You", DefausserCetAttachement, conditions=[CiblePorteur])
    if cout is not None:
        ab.SetCost(cout)
    for f in fonctions:
        ab.SetCostFunc(f)
    return ab


def PorteurAttaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
    cible = effect.this.CastTo(Attachment).bind_face
    return cible is not None and message.attacker is cible


def MenaceSupplementaire(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
    Faces.PlaceTokensOn([effect.this], Worlds.GetPlayerNumIcon(effect), 'threat', effect)


def AUnPiegeAttache(effect: 'Effect', joueur: 'Player') -> bool:
    identite = joueur.GetIdentity()
    return any(a.bind_face is identite for a in Worlds.FindCardsOnField(effect, card_type=Attachment, trait="TRAP"))


def PiegesDonnesAuJoueur(effect: 'Effect', joueur: 'Player') -> int:
    return len(PiegesDistribues(effect, joueur))
