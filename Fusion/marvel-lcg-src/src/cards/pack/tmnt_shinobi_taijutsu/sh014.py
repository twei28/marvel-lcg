from . import *

# * Minarai — AMELIORATION unique 1 [energy], Taijutsu (TMNT Shinobi, Inkwire). TITLE. TRAINING.
# Attach to an ally you control. Max 1 TRAINING upgrade per ally.
# Response: After attached ally takes consequential damage ([consequential]), draw 1 card.
#
# Cartes de reference :
#  - « Attach to an ally ... Max 1 TRAINING upgrade per ally » : `tmnt_aspect_aggression/ua004` Attack Training
#    (`CanPlayThisUpgradeCard(CardFinder(..., card_type=Ally))` ; la regle « Max 1 TRAINING upgrade per ally » est
#    NATIVE : `filter_training_upgrade_per_ally`, ability.py, lue sur le trait TRAINING de la carte) ;
#  - « After attached ally takes consequential damage » : `leonardo/tl009` Taicho (`AfterAllyTakeConsequentialDamage(
#    ..., op, conditions=[allie encore en jeu])`) avec `tmnt_aspect_dual/ud006` pour la forme « Response ».
#
# TEXTE CONTRE CODE
#  ⚠ « an ally YOU CONTROL » : un allie sous VOTRE controle seulement (filtre `GetControlByPlayer`), pas l'allie d'un
#    autre joueur.
#  ⚠ « attached ally TAKES consequential damage » : seulement si des degats consecutifs ont ete REELLEMENT subis
#    (Tough les empeche : pas de Reponse) ; « Response » nu : pas « Hero Response ».
#  ⚠ Si l'allie est vaincu par ces degats, l'amelioration part avec lui : rien a piocher.
#  ⚠ Titre unique (« * ») ; traits TITLE et TRAINING.


def GetAbilities() -> Sequence['Ability']:

    def minarai(effect: 'Effect', message: 'Message.AfterAllyTakeConsequentialDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is not None:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Ally,
                       check_effect_fn=lambda effect, face: face.GetControlByPlayer() == effect.GetInitiator())
        ),
        AbilityFactory.AfterAllyTakeConsequentialDamage(
            AbilityType.Response,
            "AttachedAlly",
            minarai,
            conditions=[lambda effect, message:
                        message.trigger is not None and message.trigger.IsInPlay()],
        ),
    ]
