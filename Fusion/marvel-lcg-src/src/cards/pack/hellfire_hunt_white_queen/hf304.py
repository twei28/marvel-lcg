from . import *

# Illusory Defender. Attachement ILLUSION PSIONIC. « Attach to your identity. Uses (1 illusion counter). Attacks against you cannot be defended by
# allies or other identities. When Revealed : ... Forced Response : After the villain attacks you, remove 1 illusion counter from here. »
# Cartes de reference : sk201 / 27152 (`UnitCannotDefend`), 55039 (`AfterUnitAttackYou`).
# CIBLE DE L'ATTAQUE (QUESTIONS.md n°3, corrige le 02/11/2026) : le message `CheckIfUnitCanDefendAgainstAttack` porte desormais `attacked_targets`
# (ajout additif moteur : `IsCanDefense(attacker, attacked_targets)`, transmis par la condition de defense d'`ability.py`). « Attacks against YOU »
# = une attaque dont la cible est l'identite du porteur ; « allies or other identities » = tout allie (meme les siens) et toute identite AUTRE que
# celle du porteur (sa propre identite peut donc defendre). Les attaques contre un autre joueur restent defendables. Cible inconnue (appelant
# qui ne la donne pas) : on restreint, comme avant.


def _porteur(effect: 'Effect'):
    return effect.this.GetBindFace()


def _attaque_contre_le_porteur(effect: 'Effect', message: 'Message.CheckIfUnitCanDefendAgainstAttack') -> bool:
    cibles = message.attacked_targets
    porteur = _porteur(effect)
    if cibles is None or porteur is None:
        return True
    joueur = porteur.GetControlByPlayer()
    return any(Identity.IsType(c) and c.GetControlByPlayer() is joueur for c in cibles)


def _defenseur_pas_le_porteur(effect: 'Effect', message: 'Message.CheckIfUnitCanDefendAgainstAttack') -> bool:
    porteur = _porteur(effect)
    defenseur = message.check_unit
    if porteur is None:
        return True
    return not (Identity.IsType(defenseur) and defenseur.GetControlByPlayer() is porteur.GetControlByPlayer())


def GetAbilities() -> Sequence['Ability']:
    def apres_attaque_du_vilain(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        RetirerUnCompteurIllusion(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        PoserUnCompteurSiPsionique(),
        *AbilityFactory.UnitCannotDefend(CardFinder(card_type=Ally | Hero), Enemy, cannot_trigger_defense_ability=False,
                                         conditions=[_attaque_contre_le_porteur, _defenseur_pas_le_porteur]),
        AbilityFactory.AfterUnitAttackYou(AbilityType.ForcedResponse, Villain, apres_attaque_du_vilain),
    ]
