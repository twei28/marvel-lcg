from . import *

# Psionic Mindlock : AMELIORATION (CONDITION. PSIONIC.), cout 2, [mental]. Hero Class.
# Attach to an enemy. If attached enemy has stalwart, it loses stalwart and gains steady.
# Hero Response: After attached enemy activates, discard Psionic Mindlock → deal 3 damage to that enemy and confuse it.
# (Version du 04/03/2024 de l'auteur, relevee sur son Drive le 24/11/2026 : l'ancienne « Hero Response (attack) : apres l'entree en jeu d'un sbire, 2 degats et Desoriente » (cout 1, PREPARATION)
#  est devenue une CONDITION attachee a un ennemi, cout 2, qui frappe apres SON activation.)
#
# CARTES DE REFERENCE
#  - `ho012` « That Had to Hurt » (amelioration « Attach to an enemy » : `CanPlayThisUpgradeCard(Enemy)` + `GiveKeywordToAttached(stalwart=-1, steady=-1)`) et `wd161` Webbed (« Attached enemy loses steady
#    and stalwart », meme fabrique, `get_new_value` pour une valeur calculee).
#  - `ra028` Malekith / `nt013` : `AfterEnemyActivationEnd` (« After [the] enemy activates »), cible nommee `"AttachedEnemy"` comme `wd161` / `ho012`.
#
# TEXTE CONTRE CODE
#  « Attach to an ENEMY » : vilain ou sbire (pas un allie). « IF attached enemy HAS stalwart, it LOSES stalwart AND gains steady » : UN seul interrupteur pour les DEUX mouvements : tant que l'ennemi porte
#    Robuste (imprime ou donne par une autre carte), il le perd ET gagne Solide ; sans Robuste, rien ne se passe (pas de Solide offert). Le test ne peut pas relire le Robuste que la carte vient d'enlever :
#    on le reconstitue (valeur lue + 1 si notre propre retrait est en vigueur) pour que l'interrupteur ne clignote pas. « Hero Response » -> sous-type dedie, forme heros seulement. « After attached enemy
#    ACTIVATES » : apres l'activation de CET ennemi (attaque ou manigance), pas apres celle d'un autre. « discard Psionic Mindlock » = COUT. « 3 damage to THAT enemy » PUIS Desoriente, le meme ennemi.
#  Chiffres : cout 2, 3 degats.


def GetAbilities() -> Sequence['Ability']:

    def robuste_ou_non(effect: 'Effect', face: 'CardFace', faces: List['CardFace']) -> int:
        """1 tant que l'ennemi porte Robuste HORS de notre propre retrait, 0 sinon."""
        Unused(faces)
        this = effect.this
        actif = getattr(this, "_mt009_robuste_retire", 0)
        valeur = 1 if face.stalwart + actif > 0 else 0
        this._mt009_robuste_retire = valeur
        return valeur

    def psionic_mindlock(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        ennemi = message.trigger
        this.DealDamage([ennemi], 3, effect)
        Faces.GiveStatus([ennemi], "Confused", effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            Enemy,
        ).SetPlay(),
        *AbilityFactory.GiveKeywordToAttached(
            "Character",
            get_new_value=robuste_ou_non,
            stalwart=-1,
            steady=1,
        ),
        AbilityFactory.AfterEnemyActivationEnd(
            AbilityType.HeroResponse,
            "AttachedEnemy",
            psionic_mindlock,
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
