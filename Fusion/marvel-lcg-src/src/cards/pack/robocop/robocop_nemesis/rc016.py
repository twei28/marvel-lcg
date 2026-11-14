from . import *

# Fugitives (x2) : SBIRE nemesis (4/5 et 5/5), CREEP. CRIMINAL. PV 4, MNG 1, ATQ 2, boost 2. Patrol.
# Forced Interrupt: When Fugitives activates, players cannot resolve "Interrupt" abilities on cards they control during this activation.
#
# CARTES DE REFERENCE
#  - `AbilityFactory.PlayersCannotTriggerAbility(which_player, which_ability, conditions=..)` (`player.py`) : la restriction ; `04004` Mockingbird : une regle temporaire
#    enregistree sur la carte (`RegisterTemp(.., until_event_end=message)`) qui expire a la fin de l'EVENEMENT (ici l'activation : `WhenEnemyActivateAgainstYou` porte
#    `end_event=AfterEnemyActivationEnd`).
#  - `Patrol` : lu dans `desc` (base automatique, fiche `mots-cles/patrol.md`).
#
# TEXTE CONTRE CODE
#  Pose de la regle : sur WhenUnitWouldAttack/WouldScheme (Interruption forcee), car le moteur ouvre la fenetre des Interruptions AVANT WhenEnemyActivateAgainstYou.
#  « When Fugitives ACTIVATES » -> son activation contre un joueur (attaque OU manigance). « during THIS activation » : la regle tombe a la fin de cette activation, pas
#    de la phase. « Interrupt abilities » -> Interrupt, Hero Interrupt, Alter-Ego Interrupt (les Interruptions FORCEES restent : elles ne sont pas « resolues par les joueurs »).
#  « on cards THEY control » -> DECISION UTILISATEUR du 01/11/2026 : les cartes du joueur EN JEU (identite, ameliorations, allies, soutiens) ET ses evenements a
#    Interruption EN MAIN (No Collateral) sont interdits pendant l'activation.
#  Chiffres : PV 4, MNG 1, ATQ 2, boost 2.


def GetAbilities() -> Sequence['Ability']:

    def carte_du_joueur(effect: 'Effect', message: 'Message.CheckEffectCondition') -> bool:
        # « cards they control » : DECISION UTILISATEUR du 01/11/2026 -- les cartes du joueur EN JEU et ses evenements EN MAIN (No Collateral inclus).
        face = message.check_effect.this
        return face.GetControlByOrOwner() == message.check_effect.initiator

    def fugitives(effect: 'Effect', message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldScheme') -> None:
        this = effect.this.CastTo(Minion)
        this.effect.RegisterTemp(
            AbilityFactory.PlayersCannotTriggerAbility(
                "AnyPlayer",
                "Interrupt",
                conditions=[carte_du_joueur],
            ),
            unregister_after_exec=False,
            until_event_end=message,
        )

    # Le moteur ouvre la fenetre d'Interruption (`WhenUnitWouldAttack`, No Collateral) AVANT d'envoyer `WhenEnemyActivateAgainstYou` (`can_attack.py`) : la regle
    # doit donc etre posee des le debut de l'attaque (ou de la manigance), Interruption forcee resolue avant celles des joueurs.
    return [
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", fugitives),
        AbilityFactory.WhenUnitWouldScheme(AbilityType.ForcedInterrupt, "This", fugitives),
    ]
