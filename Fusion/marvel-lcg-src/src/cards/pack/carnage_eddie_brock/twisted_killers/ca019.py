from . import *

# * Muse : SBIRE (CRIMINAL. ELITE. KILLER.), SCH 2, ATK 1 (consecutif), PV 6, boost 3. Set modulaire « Twisted Killers ».
# Steady. Villainous.
# [star] Forced Interrupt: When Muse attacks, he attacks the character with the fewest remaining hit points. This attack gains piercing. If this attack defeats a character, heal 1 damage from Muse for each point of excess damage dealt to that character by that attack.
#
# CARTES DE REFERENCE
#  - Steady / Villainous : natifs (`desc`, fiches steady.md / villainous.md), aucun code.
#  - « attacks X instead » : `41028` (Psionic Illusion) / `ca022` : `WhenUnitWouldAttackUnit(ForcedInterrupt, .., op)` + `message.ChangeTarget(unit, effect)` ; « gains piercing » : `message.GainPiercing(effect)` (sender_damage.py:395, fiche piercing.md).
#  - Soin de l'exces : `AfterUnitDefeatedUnit(.., is_from_attack=True, has_excess_damage=True)` + `message.excess_damage` (ca001a Death-Dealer, ar005) ; `HealthUnits([muse], n, effect)` (my001b).
#
# TEXTE CONTRE CODE
#  « the CHARACTER with the FEWEST REMAINING hit points » : personnage AMI (identite, allies) du joueur attaque, PV RESTANTS (`health`) ; ex aequo : le joueur choisit. LECTURE : « character » = ami (contraste avec Murderous Nature, qui nomme expressement « or other enemy »).
#  « This attack gains PIERCING » : tous ses attaques via cette Interruption. « If this attack DEFEATS a character, heal 1 damage FROM MUSE for EACH point of EXCESS damage » : soin de Muse = exces de CETTE attaque ; aucun exces = aucun soin. Chiffres : PV 6, ATK 1, SCH 2, boost 3.
#  ⚠ Meme limite que ca022 : aucune redirection vers un ennemi (il n'y en a pas ici : ami seulement).


def GetAbilities() -> Sequence['Ability']:

    def muse_attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        joueur = message.target.GetControlByPlayer() if hasattr(message.target, "GetControlByPlayer") else None
        amis = PersonnagesAmisEnJeu(effect, joueur)
        plus_faibles = PlusFaibleEnPV(amis)
        if plus_faibles:
            cible = plus_faibles[0]
            if len(plus_faibles) > 1 and joueur is not None:
                choisie = joueur.AskChooseFace(plus_faibles, effect, forced=True)
                if choisie is not None:
                    cible = choisie
            if cible is not message.target:
                message.ChangeTarget(cible, effect)
        message.GainPiercing(effect)

    def muse_se_soigne(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        exces = int(getattr(message, "excess_damage", 0) or 0)
        if exces > 0:
            effect.this.HealthUnits([effect.this], exces, effect)

    return [
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.ForcedInterrupt,
            "This",
            Unit2,
            muse_attaque,
        ),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.ForcedResponse,
            "This",
            Unit2,
            muse_se_soigne,
            is_from_attack=True,
            has_excess_damage=True,
        ),
    ]
