from . import *

# The Ultimate Hunt (1B) — COMPLOT PRINCIPAL, stade 1. Seuil 8[per_hero], escalade +1[per_hero] (★), depart 0.
# [star] Forced Response: After resolving step one of the villain phase, if there is no threat on each villain's side scheme, deal 2 damage
#   to each villain.
# Forced Response: After a villain activates, move the active counter to the next villain.
# Insert « Ultimate Hunt 1B » : si Alien Queen ET Predator Warlord ont chacun 2 PV et qu'aucune de leurs manigances permanentes ne porte
#   de menace, ils tombent a 0 PV ensemble et les joueurs GAGNENT.
#
# Cartes de reference :
#  - « After resolving step one of the villain phase » : `AfterResolveVillainPhaseStep(ForcedResponse, 1, op)` (07001b Breakout) ;
#  - « deal 2 damage to each villain » : `DealDamage(mechants, 2)` en UNE fois (simultane) ;
#  - « After a villain activates » : `AfterEnemyActivationEnd(ForcedResponse, Villain, op)` (activation = attaque OU manigance, y compris
#    celles des traitrises : « The villain schemes ») ; « move the active counter » : `PasserLeCompteur` (Villains.SetActive) ;
#  - mechant SONNE / DESORIENTE dont la carte d'etat remplace l'activation : `AfterStatusDiscardFrom` (la carte d'etat se defausse
#    elle-meme) -> le compteur passe aussi (arbitrage du 25/10/2026 : « l'alternance ne se casse jamais »).
#
# ⚠ Mots-pieges :
#  - « no threat on EACH villain's side scheme » : les deux manigances a 0 (une manigance absente ne porte pas de menace) ;
#  - « EACH villain » : les deux, en meme temps : la Reine vaincue par ces degats ne fait pas soigner le Warlord AVANT qu'il prenne les
#    siens ; si les deux tombent ensemble, l'insert tranche : victoire (pas de face Defeated jouee) ;
#  - « do not move the active villain counter » (Advance Again, Assault, Alien Assault) : la garde est consommee par `PasserLeCompteur`.


def TomberaitAZero(mechant: 'Villain', degats: int) -> bool:
    """Les `degats` le reduiraient-ils a 0 PV ? (une carte Tenace absorbe les degats.)"""
    return mechant.health <= degats and not mechant.IsTough()


def GetAbilities() -> Sequence['Ability']:

    def etape_un(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(message)
        mechants = Mechants(effect)
        if not mechants:
            return
        for mechant in mechants:
            manigance = ManiganceDe(effect, NomDuMechant(mechant))
            if manigance is not None and manigance.threat > 0:
                return
        if len(mechants) >= 2 and all(TomberaitAZero(m, 2) for m in mechants):
            Worlds.SetGameOver(True, effect)
            return
        this.DealDamage(mechants, 2, effect)

    def apres_activation(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        Unused(message)
        PasserLeCompteur(effect)

    def etat_qui_remplace(effect: 'Effect', message: 'Message.AfterStatusDiscardFrom') -> bool:
        """La carte Sonne / Desoriente s'est defaussee ELLE-MEME : elle vient de remplacer une activation du mechant."""
        Unused(effect)
        return message.status.name in ("Stunned", "Confused") and \
            getattr(getattr(message, "by_effect", None), "this", None) is message.status and \
            bool(NomDuMechant(message.trigger))

    def activation_remplacee(effect: 'Effect', message: 'Message.AfterStatusDiscardFrom') -> None:
        Unused(message)
        PasserLeCompteur(effect)

    return [
        AbilityFactory.AfterResolveVillainPhaseStep(AbilityType.ForcedResponse, 1, etape_un),
        AbilityFactory.AfterEnemyActivationEnd(AbilityType.ForcedResponse, Villain, apres_activation),
        AbilityFactory.AfterStatusDiscardFrom(AbilityType.ForcedResponse, Villain, None, activation_remplacee,
                                              conditions=[etat_qui_remplace]),
    ]
