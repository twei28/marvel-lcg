from cards.pack import *
from cards.pack.fne import PeutCouvrirLeCout


def DistribuerLesBoostsDeCeType(effect: 'Effect', message: 'Message.WhenCardBecomeBoost', type_carte, *, attaque: bool, vilain_seulement: bool) -> None:
    """Master Key / Mysterio : « deal each of that activation's boost cards that
    is a <minion|treachery> to yourself as a facedown encounter card ». Meme
    patron que Purple Man (WhenCardBecomeBoost + AfterThisActivation +
    DealEncounterCard) ; `yourself` = le joueur contre qui l'ennemi s'active."""
    carte = message.trigger
    if not type_carte.IsType(carte):
        return
    ennemi = message.activating_enemy
    if vilain_seulement and not Villain.IsType(ennemi):
        return
    if ennemi is not effect.this.GetBindFace() if vilain_seulement else ennemi is not effect.this:
        return
    est_attaque = message.being_message.IsAttack() if message.being_message is not None else False
    if attaque != est_attaque:
        return
    joueur = message.GetToPlayer()

    def donner() -> None:
        if joueur is not None and not carte.IsInPlay():
            joueur.DealEncounterCard(carte, effect)

    message.AfterThisActivation(effect, donner)


def EstUnDeceived(face: 'CardFace') -> bool:
    return Minion.IsType(face) and face.HasTrait("DECEIVED") and face.card.IsAsOtherCard()


def ConvertirEnDeceived(face: 'CardFace', effect: 'Effect') -> 'Minion|None':
    """Baron Zemo : « Treat each ally with threat on it as a DECEIVED minion
    with a blank text box. Its SCH is equal to its base THW and it does not
    take consequential damage. » Copie de la branche diff == 1 de
    `TreatAttachedCardAsMinion` (treat.py), sans le cadre `apply` (qui ne sait
    pas defaire la conversion sur retrait du jeton) ni les temporaires de
    `TreatAsMinion`. PV, degats et jetons vivent sur la CARTE : le sbire les
    garde. Le sbire s'engage avec le controleur de l'allie."""
    from game.card.factory import CardFactory
    from cards.database import CardsDB
    if not Ally.IsType(face) or face.card.IsAsOtherCard():
        return None
    joueur = face.GetControlByPlayer()
    if joueur is None:
        return None
    paper = CardFactory.FindCardPapers("Deceived Minion")[0]
    minion = CardFactory.CreateFace(paper, effect.world)
    minion.pic_id = face.paper.card_id
    minion.SetName(face.printed_name)
    minion.SetSubtitle(face.printed_subtitle)
    minion.printed_attack = face.printed_attack
    minion.printed_scheme = face.printed_thwart
    minion = face.card.SwapCardFace(minion, effect, no_detach=True)
    if not minion.IsInPlay():
        return None
    minion.ability.Add(*CardsDB.FindAbilities(paper.card_id, paper.pack, paper.set_name))
    minion.effect.face = minion
    CardFactory.FaceRegisterEffects(minion)
    # Meme sauvegarde que le correctif du 18/09/2026 dans treat.py : les
    # mots-cles donnes par d'autres faces survivent au ResetKeywords.
    etrangers = {k: {f: v for f, v in d.items() if f is not minion and v}
                 for k, d in minion.keywords.items()}
    minion.ResetKeywords()
    for k, d in etrangers.items():
        for f, v in d.items():
            minion.keywords.setdefault(k, {})
            minion.keywords[k][f] = minion.keywords[k].get(f, 0) + v
    if hasattr(minion, "SetGuardPatrolEffectedBy"):
        minion.SetGuardPatrolEffectedBy(minion.IsGuard(), minion.IsPatrol())
    minion.EngagePlayer(joueur, effect)
    minion.PutIntoPlay(joueur, effect)
    return minion


def RendreLAllie(minion: 'CardFace', effect: 'Effect') -> 'CardFace|None':
    """Le sbire DECEIVED redevient l'allie imprime, sous le controle du joueur
    avec qui il etait engage (= son controleur d'origine) ; les jetons restent
    sur la carte (FAQ : « threat remains »)."""
    if not EstUnDeceived(minion):
        return None
    joueur = minion.CastTo(Minion).GetEngagedPlayer()
    face = minion.card.SwapBackToPrintedCard(effect)
    if face.IsInPlay() and not face.IsDefeated():
        face.PutIntoPlay(joueur, effect, under_control=True)
    else:
        Faces.DiscardAll([face], effect)
    return face
