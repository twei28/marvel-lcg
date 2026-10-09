from cards.pack import *

ID_LIZARD = ("hs054b", "hs055b", "hs056b")
MAX_HONTE = 3


def Rage(effect: 'Effect') -> 'Environment|None':
    return Worlds.FindCardOnField(effect, name="Reptilian Rage", card_type=Environment)


def Honte(effect: 'Effect') -> int:
    rage = Rage(effect)
    return rage.CastTo(CanPlaceCounter).GetCounters('shame') if rage else 0


def PlacerHonte(effect: 'Effect', n: int) -> None:
    """Pose n compteurs de honte, sans jamais depasser 3."""
    rage = Rage(effect)
    if rage is None:
        return
    n = min(n, MAX_HONTE - Honte(effect))
    if n > 0:
        Faces.PlaceCountersOn([rage], n, 'shame', effect)


def CompleterHonte(effect: 'Effect') -> None:
    PlacerHonte(effect, MAX_HONTE)


def RetirerHonte(effect: 'Effect', n: int) -> None:
    rage = Rage(effect)
    if rage is None or n <= 0:
        return
    n = min(n, Honte(effect))
    if n > 0:
        Faces.RemoveCountersOn([rage], n, 'shame', effect)


def Vilain(effect: 'Effect') -> 'Villain|None':
    return Worlds.FindCardOnField(effect, card_type=Villain)


def LizardEnJeu(effect: 'Effect') -> bool:
    v = Vilain(effect)
    return v is not None and any(v.IsCardId(i) for i in ID_LIZARD)


def EstLizard(face: 'CardFace') -> bool:
    return any(face.IsCardId(i) for i in ID_LIZARD)


def EstReptile(face: 'CardFace') -> bool:
    return face.HasTrait("REPTILE")


def NombreReptiles(effect: 'Effect') -> int:
    """Cartes REPTILE en jeu, le Lizard compris, rattachements compris."""
    return len(Worlds.FindCardsOnField(effect, trait="REPTILE"))


def EtapeDuVilain(effect: 'Effect') -> int:
    v = Vilain(effect)
    return v.printed_stage if v else 1


def AuFondDeLaDefausse(effect: 'Effect', face: 'CardFace') -> None:
    face.card.MoveToArea(Worlds.GetEncounterDiscardPile(effect), effect, index=0)


def AbilitesCurtis(n: int) -> 'List[Ability]':
    """Faces A : ne subit aucun degat, attaque en posant n honte, manigance a 3, puis se retourne."""

    def au_lieu_dattaquer(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.SetBeInstead(effect)
        PlacerHonte(effect, n)
        if Honte(effect) >= MAX_HONTE:
            effect.this.CastTo(Enemy).DoSchemes(message.GetAgainstPlayer(), effect)

    def apres_manigance(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        effect.this.card.Flip(effect)

    return [
        AbilityFactory.UnitCannotTakeDamageWhile(AbilityType.NonKeyword, "This"),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", au_lieu_dattaquer),
        AbilityFactory.AfterUnitSchemeEnd(AbilityType.ForcedResponse, "This", apres_manigance),
    ]


def AbilitesLizard(defausse: int, tous_les_joueurs: bool) -> 'List[Ability]':
    """Faces B : se retourne apres avoir manigance ; defausse des cartes en fin de phase du vilain."""

    def apres_manigance(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        effect.this.card.Flip(effect)

    def fin_de_phase(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        faces = Worlds.DiscardEncounterCards(defausse * len(Worlds.GetPlayers(effect)), effect)
        if not tous_les_joueurs:
            for f in faces:
                if Attachment.IsType(f) and EstReptile(f):
                    f.Reveal(Worlds.GetFirstPlayer(effect), effect)
            return
        for joueur in Worlds.GetPlayers(effect):
            cartes = [c for c in Worlds.GetEncounterDiscardPileCards(effect)
                      if Attachment.IsType(c) and EstReptile(c)]
            if cartes:
                cartes[0].Reveal(joueur, effect)

    return [
        AbilityFactory.AfterUnitSchemeEnd(AbilityType.ForcedResponse, "This", apres_manigance),
        AbilityFactory.WhenVillainPhaseEnd(AbilityType.ForcedInterrupt, fin_de_phase),
    ]


IDS_BOA = ("hs068", "hs069")


def BoaSurLIdentite(player: 'Player') -> bool:
    return any(any(a.IsCardId(i) for i in IDS_BOA) for a in player.GetIdentity().GetAttachedAttachments())


def RevelerAttachementReptile(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
    """Curtis (le vilain) manigance avec +1[per_hero] SCH, puis l'attachement se fixe au Lizard."""
    v = Vilain(effect)
    if v is None:
        return
    bonus = Worlds.ConvertPerPlayerIconToInt("1*", effect)
    v.CastTo(Enemy).DoSchemes(message.GetToPlayer(), effect, property=SchemeProperty(additional_value=bonus))
    v = Vilain(effect)
    if v is not None:
        effect.this.CastTo(Attachment).AttachTo2(v, effect)


def AttacherAuLizard() -> 'Ability':
    return AbilityFactory.WhenThisRevealed(None, RevelerAttachementReptile)


def ActionHeros(cout: 'Cost|None'=None, *fonctions: 'CostFunc.Base') -> 'Ability':
    """Hero Action d'un attachement REPTILE : bloquee par Boa Constricted, finit au fond de la defausse."""

    def agir(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        AuFondDeLaDefausse(effect, effect.this)

    def pas_de_boa(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        return not BoaSurLIdentite(message.to_player)

    ab = AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, agir, conditions=[pas_de_boa])
    if cout is not None:
        ab.SetCost(cout)
    for f in fonctions:
        ab.SetCostFunc(f)
    return ab
