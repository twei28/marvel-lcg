from cards.pack import *

ID_VULTURE = ("hs080", "hs081", "hs082")
NOM_VULTURE_NATALE = "Vulture (James Natale)"


def Vilain(effect: 'Effect') -> 'Villain|None':
    return Worlds.FindCardOnField(effect, card_type=Villain)


def Vulture(effect: 'Effect') -> 'Villain|None':
    v = Vilain(effect)
    return v if v is not None and any(v.IsCardId(i) for i in ID_VULTURE) else None


def PerdreAerialJusquauTour(face: 'CardFace', effect: 'Effect') -> None:
    face.GainUntilTurnEnd(effect, lose_trait="AERIAL")


def PerdreAerialJusquaLaRonde(face: 'CardFace', effect: 'Effect') -> None:
    face.GainUntilRoundEnd(effect, lose_trait="AERIAL")


def GagnerAerialJusquaLaRonde(face: 'CardFace', effect: 'Effect') -> None:
    face.GainUntilRoundEnd(effect, trait=["AERIAL"])


def MoinsDeLaMoitie(face: 'CardFace') -> bool:
    return 2 * face.health < face.max_health


def DefausserUneCarteDeLaMain(effect: 'Effect', joueur: 'Player') -> bool:
    return len(joueur.DiscardHandCards((1, 1), effect)) > 0


def ActionPerdreAerial(cout: 'Cost|None', *fonctions: 'CostFunc.Base') -> 'Ability':
    """Hero Action d'un attachement : defausse la carte, Vulture perd AERIAL jusqu'a la fin du tour."""

    def agir(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        v = Vulture(effect)
        if v is not None:
            PerdreAerialJusquauTour(v, effect)
        Faces.DiscardAll([effect.this], effect)

    ab = AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, agir)
    if cout is not None:
        ab.SetCost(cout)
    for f in fonctions:
        ab.SetCostFunc(f)
    return ab


def AttacherAVulture(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
    v = Vulture(effect)
    if v is None or not effect.this.CastTo(Attachment).AttachTo2(v, effect):
        Faces.DiscardAll([effect.this], effect)


def AttacherALaRevelation() -> 'Ability':
    return AbilityFactory.WhenThisRevealed(None, AttacherAVulture)


def PorteurEstAttaquant(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
    cible = effect.this.CastTo(Attachment).bind_face
    return cible is not None and message.attacker is cible


def AttaqueContreLeJoueur(message: 'Message.WhenUnitWouldAttack') -> 'Player|None':
    joueur = message.property.against_player
    if joueur is None:
        return None
    return joueur if message.HasTarget(joueur.GetIdentity()) else None


def SiLAttaqueVousBlesse(effect: 'Effect', message: 'Message.WhenCardBecomeBoost', action: 'Callable[[Player, int], None]') -> None:
    """Boost « si cette attaque vous blesse » : compare les PV de l'identite avant et apres l'activation."""
    joueur = message.GetToPlayer()
    identite = joueur.GetIdentity()
    avant = identite.health

    def apres() -> None:
        degats = avant - identite.health
        if degats > 0:
            action(joueur, degats)

    message.AfterThisActivation(effect, apres)


def AbilitesVulture(plus_un: bool) -> 'List[Ability]':
    """Tant que Vulture a AERIAL : on ne l'attaque qu'avec AERIAL ou ranged. Etapes 2 et 3 : +1 ATK contre un personnage blesse."""

    def a_aerial(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        return effect.this.HasTrait("AERIAL")

    def refuser(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        if message.attacker.HasTrait("AERIAL") or message.property.ranged:
            return
        message.SetBeInstead(effect)

    def cible_blessee(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        return any(MoinsDeLaMoitie(t) for t in message.attacked_targets)

    def plus_un_atk(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainATKForThisAttack(1, effect)

    def natale(effect: 'Effect', message: 'Message.CheckIfFaceApplyUniqueRule') -> bool:
        return message.which_face.IsCardId("hs151")

    abilities = [
        Ability(AbilityType.NonKeyword, Message.CheckIfFaceApplyUniqueRule, [natale],
                lambda effect, message: message.IgnoreUniqueRule(effect)),
        AbilityFactory.WhenUnitWouldBeAttacked(AbilityType.NonKeyword, "This", refuser, conditions=[a_aerial]),
    ]
    if plus_un:
        abilities.append(
            AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", plus_un_atk, conditions=[cible_blessee])
        )
    return abilities
