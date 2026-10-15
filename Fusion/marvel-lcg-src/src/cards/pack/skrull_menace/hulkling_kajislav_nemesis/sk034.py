from . import *

# Inhibited — ATTACHEMENT nemesis de Hulkling (n° 34, 3/5). CONDITION.
# Attach to your identity.
# You cannot change form or play cards that share a [[TRAIT]] with your identity.
# Action: Spend [physical][physical] resources → discard this card.
#
# Cartes de reference :
#  - **`21158`** Frozen : « Attach to your identity. ... » =
#    `AttachToFaceWhenPutIntoPlay("YourIdentity")` + `PlayerActionToDiscardThis(
#    ...).SetCost(Cost("YR"))`.
#  - **`36030`** Claustrophobia : « You cannot change forms » =
#    `PlayersCannotChangeForms(NonKeyword, "AttachedPlayer")`. Le blocage annule
#    `WhenUnitWouldChangeForm`, que la forme d'origine envoie aussi
#    (`ChangerDOrigine`, set Hulkling) : retourner l'origine est donc bloque.
#  - **`56029b`** Teddy Altman (officiel) : `PlayersCannotPlayCardWhile("You",
#    <filtre>, conditions=[...])`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « change **form** » : heros <-> civil ET forme d'origine (livret p. 4).
#    L'Action de sk002a/b n'est d'ailleurs plus proposee
#    (`PeutChangerDeForme`, qui lit cette carte).
#  - « share **a** TRAIT » : N'IMPORTE quel trait commun avec l'identite
#    ACTUELLE (AVENGER + KREE/SKRULL en heros, HYBRID en civil) :
#    `identite.ShareTrait(carte)`. Lu a chaque tentative de jeu.
#  - « Action » nue (pas Alter-Ego) : utilisable dans les deux formes.
#  - « Spend [physical][physical] » : `Cost("RR")`.
#  - « Attach to **your** identity » : le joueur qui la revele.


def GetAbilities() -> Sequence['Ability']:

    def partage_un_trait(effect: 'Effect', message: 'Message.CheckEffectCondition') -> bool:
        joueur = message.check_effect.initiator
        if joueur is None or not Player.IsType(joueur):
            return False
        identite = joueur.GetIdentity()
        carte = message.check_effect.this
        return identite is not None and carte is not None and identite.ShareTrait(carte)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourIdentity",
        ),
        AbilityFactory.PlayersCannotChangeForms(
            AbilityType.NonKeyword,
            "AttachedPlayer",
        ),
        AbilityFactory.PlayersCannotPlayCardWhile(
            "AttachedPlayer",
            conditions=[partage_un_trait],
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.Action,
        ).SetCost(Cost("RR")),
    ]
