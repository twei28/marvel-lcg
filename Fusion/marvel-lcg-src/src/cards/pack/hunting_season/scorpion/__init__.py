from cards.pack import *

NOM_QUEUE = "Scorpion’s Tail"
ETAT = {"deplacement": False}


def QueueDe(scorpion: 'CardFace') -> 'Attachment|None':
    for a in scorpion.GetAttachedAttachments():
        if a.IsCardId("hs036"):
            return a
    return None


def AttacherLaQueue(effect: 'Effect', scorpion: 'CardFace') -> None:
    """Cherche Scorpion’s Tail hors jeu et l’attache à Scorpion."""
    if QueueDe(scorpion) is not None:
        return
    queue = Find.Find(effect, finder=CardFinder(name=NOM_QUEUE, card_type=Attachment,
                                                check_face_fn=lambda f: not f.IsInPlay()))
    if queue is None:
        return
    queue.CastTo(Attachment).AttachTo2(scorpion, effect)


def ForcedInterruptQueue(operation=None):
    """Capacité * de Scorpion : en fin de phase du vilain, remettre la Queue."""
    def fin_de_phase(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        AttacherLaQueue(effect, effect.this)

    def sans_queue(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> bool:
        return QueueDe(effect.this) is None

    return AbilityFactory.WhenVillainPhaseEnd(
        AbilityType.ForcedInterrupt, fin_de_phase, conditions=[sans_queue],
    )


def MettreEnJeuLeSoutien(effect: 'Effect') -> None:
    premier = Worlds.GetFirstPlayer(effect)
    deja = Worlds.FindCardsOnField(effect, name="J. Jonah Jameson")
    if not deja:
        Find.FindAndPutIntoPlay(
            effect, premier,
            finder=CardFinder(name="J. Jonah Jameson", card_type=Support,
                              check_face_fn=lambda f: not f.IsInPlay()),
        )


def PlacerUneBlessureSurJameson(effect: 'Effect') -> None:
    for jj in Worlds.FindCardsOnField(effect, name="J. Jonah Jameson"):
        Faces.PlaceCountersOn([jj], 1, 'wound', effect)


def ScorpionEtQueue(effect: 'Effect') -> 'tuple[CardFace|None, Attachment|None]':
    for scorpion in Worlds.FindCardsOnField(effect, name="Scorpion"):
        queue = QueueDe(scorpion)
        if queue is not None:
            return scorpion, queue
    return None, None


def DeplacerDegatsDeLaQueue(effect: 'Effect', scorpion: 'CardFace', queue: 'Attachment') -> None:
    n = min(5, queue.GetTokens('damage'))
    if n > 0:
        Faces.RemoveTokensOn([queue], n, 'damage', effect)
        ETAT["deplacement"] = True
        try:
            scorpion.TakeDamage(scorpion, n, effect)
        finally:
            ETAT["deplacement"] = False


def ArmureDe(queue: 'CardFace') -> 'Attachment|None':
    for a in queue.GetAttachedAttachments():
        if a.IsCardId("hs037"):
            return a
    return None


def PlacerDegatsSurLaQueue(effect: 'Effect', scorpion: 'CardFace', queue: 'Attachment', degats: int) -> None:
    armure = ArmureDe(queue)
    if armure is not None:
        Faces.PlaceTokensOn([armure], degats, 'damage', effect)
        if armure.GetTokens('damage') >= 8:
            Faces.DiscardAll([armure], effect)
        return
    Faces.PlaceTokensOn([queue], degats, 'damage', effect)
    if queue.GetTokens('damage') >= Worlds.ConvertPerPlayerIconToInt("10*", effect):
        Faces.SetAside([queue], effect)
        scorpion.TakeDamage(scorpion, Worlds.ConvertPerPlayerIconToInt("8*", effect), effect)
        DefausserLesCoiledUp(effect)


def DefausserLesCoiledUp(effect: 'Effect') -> None:
    for joueur in Worlds.GetPlayers(effect):
        for a in list(joueur.GetIdentity().GetAttachedAttachments()):
            if a.IsCardId("hs040") or a.IsCardId("hs041"):
                Faces.DiscardAll([a], effect)


def AttacherALaQueue(cette_carte: 'Attachment', effect: 'Effect') -> None:
    """Attachements TAIL : 5 dégâts de la Queue vers Scorpion, puis s'attache à la Queue, sinon surge."""
    scorpion, queue = ScorpionEtQueue(effect)
    if queue is None:
        ThisCardGainSurge(effect)
        return
    DeplacerDegatsDeLaQueue(effect, scorpion, queue)
    cette_carte.AttachTo2(queue, effect)


def ScorpionPorteCetteQueue(effect: 'Effect', attaquant: 'CardFace') -> bool:
    queue = effect.this.bind_face
    return queue is not None and queue.bind_face is attaquant
