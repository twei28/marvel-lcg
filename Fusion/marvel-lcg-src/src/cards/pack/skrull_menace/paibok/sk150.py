from . import *

# Ice Control — ATTACHEMENT (Paibok). POWER SKRULL. MNG +1 ; badge ATQ a etoile seule ; boost 1 + etoile.
# Attach to Paibok.
# [star] Forced Response: After Paibok attacks you, exhaust a character you control.
# Hero Action: Spend 3 resources of any type → discard this card.
# [star] Boost: Exhaust a character you control.
#
# Cartes de reference :
#  - Reponse forcee + Boost « exhaust a character you control » : **`mut_gen 32073`** Avalanche
#    (`AfterUnitAttackYou(ForcedResponse, ...)` + `ForChoiceAbility(...).SetTarget("YouControlUnit",
#    canbe_exhaust=True)`) ; ici l'attaquant est l'hote (« AttachedEnemy »).
#  - Cout « 3 resources of any type » : **`sunfire sf014`** Silver Samurai's Katana (`Cost("3")`).
#  - Attache + defausse : `01100` Enhanced Ivory Horn.
#
# ⚠ Mots-pieges : « After Paibok attacks YOU » (le joueur attaque, pas l'allie) ; « a character YOU
# control » (le joueur attaque choisit) ; badge ATQ a etoile seule = « voir le texte », SANS valeur
# (decision utilisateur du 15/10/2026) : seul le +1 MNG est chiffre (`SCH+`) ; l'etoile devant
# « Forced Response » est une marque d'impression (pas un NonKeywordStar).


def GetAbilities() -> Sequence['Ability']:

    def epuise(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        joueur = message.GetAgainstPlayer()
        if joueur:
            AuChoixDuJoueur(effect, joueur, lambda cibles: Faces.ExhaustAll(cibles, effect), canbe_exhaust=True)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        AuChoixDuJoueur(effect, message.GetToPlayer(), lambda cibles: Faces.ExhaustAll(cibles, effect), canbe_exhaust=True)

    return [
        AttacherAPaibok(),
        AbilityFactory.AfterUnitAttackYou(AbilityType.ForcedResponse, "AttachedEnemy", epuise),
        ActionDefausserPouvoir(Cost("3")),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
