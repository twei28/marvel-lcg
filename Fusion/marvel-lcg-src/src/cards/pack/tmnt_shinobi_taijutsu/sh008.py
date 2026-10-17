from . import *

# Drop In — EVENEMENT 1 [mental], Taijutsu (TMNT Shinobi, Inkwire). NYC. TACTIC.
# Action: Ready your identity. If you paid for this card with a DEFENSE event, you may return an ATTACK or THWART
#   event from your discard pile to your hand.
#
# HOMONYME d'une officielle : `night_thrasher/nt004` « Drop In » (Hero Response, apres un changement de forme,
# confusion / etourdissement selon le Battle Board). Scans compares (17/10/2026) : AUCUN rapport, texte, trait ni
# image ; classement NOUVELLE, card_id distincts. Aucune ability_link.
#
# Mots-cles : aucun (classe Taijutsu, fiche shinobi.md).
#
# Cartes de reference :
#  - « Action: ... ready your identity » : `27032` Double Life (`WhenInYourPlayTurn(Action, op).SetPlay()` +
#    `Faces.ReadyAll([identite], effect)`) ;
#  - « you may return an X event from your discard pile to your hand » : `54003` Black Widow (cible dans
#    `YourDiscardPile`, `Faces.ReturnToHand`), avec le choix OPTIONNEL `MayChooseFace` ;
#  - « if you paid for this card with a DEFENSE event » : `jennika/tj004` (`PayeAvecUnEvenement`).
#
# TEXTE CONTRE CODE
#  ⚠ « Action » nu : jouable en alter-ego ET en forme heros (pas « Hero Action ») ; « ready your IDENTITY » : la
#    carte d'identite (pas « your hero »).
#  ⚠ « you MAY return » : optionnel ; « an ATTACK OR THWART event » : un evenement portant l'un des deux traits (un
#    evenement DEFENSE seul, une carte d'un autre type, ne convient pas) ; « from YOUR discard pile ».
#  ⚠ Le retour se fait APRES le redressement, sous la condition « paid ... with a DEFENSE event ».


def GetAbilities() -> Sequence['Ability']:

    def drop_in(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        Faces.ReadyAll([joueur.GetIdentity()], effect)

        if not PayeAvecUnEvenement(effect, "DEFENSE"):
            return
        candidats = [f for f in joueur.discard_pile.Get()
                     if Event.IsType(f) and (f.HasTrait("ATTACK") or f.HasTrait("THWART"))]
        if not candidats:
            return
        choisie = joueur.MayChooseFace(candidats, effect)
        if choisie:
            Faces.ReturnToHand([choisie], joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            drop_in,
        ).SetPlay().SetLabel(),
    ]
