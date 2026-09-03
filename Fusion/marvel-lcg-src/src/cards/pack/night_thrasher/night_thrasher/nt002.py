from . import *

# Disaster — evenement signature, x2 (n/16 = 1 et 2). ATTACK. SKILL. THWART.
# Cout 2, ressource [physical].
# Hero Action (attack/thwart): Flip the Battle Board upgrade. Then, if it has
#   the:
#   • [[VEHICLE]] trait, remove 3 threat from a scheme.
#   • [[WEAPON]] trait, deal 4 damage to an enemy.
#
# Cartes de reference :
#  - `05015` Tackle / `ho003` / `im002` pour l'evenement a libelle.
#  - **`08013`** Stealth Strike : le ciblage DANS l'operation
#    (`initiator.ChooseAbilities(effect, ForChoiceAbility(...).SetTarget(...))`).
#    C'est le montage impose ici, et pas par confort : la nature de la cible
#    (complot ou ennemi) n'est connue qu'APRES le retournement, donc apres
#    l'annonce. Un `SetTarget` a l'annonce demanderait au joueur de designer
#    une cible du mauvais type une fois sur deux.
#  - `SetLabel('thwart', 'attack')` : DEUX libelles en UN SEUL appel
#    (ability.py:380 leve `assert self.labels == []` si on le chaine).
#  - `RetournerLaPlanche` (helper du set), dont le RETOUR donne la face
#    d'APRES bascule.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Then**, if it has the » : la face se lit APRES le retournement, pas
#    avant. Lire la face d'avant inverserait les deux branches — c'est le
#    piege central de la carte, et c'est pour ca que `RetournerLaPlanche`
#    RELIT le terrain au lieu de supposer.
#  - Les deux branches sont EXCLUSIVES : une planche ne porte jamais les deux
#    traits. Sans planche en jeu, aucune des deux ne tombe.
#  - « **(attack/thwart)** » : les DEUX libelles, donc la carte est livree a
#    Sonne ET a Desoriente. Un seul des deux serait une carte plus forte que
#    l'imprime.
#  - « remove 3 threat from **a scheme** » : principal ou annexe, au choix.
#  - « deal 4 damage to **an enemy** » : sans mot-cle, ni portee ni percant.


def GetAbilities() -> Sequence['Ability']:

    def disaster(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        RetournerLaPlanche(effect)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        if PlancheEstVehicule(effect):
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove 3 threat from a scheme",
                    lambda cibles: this.RemoveThreatFromSchemes(cibles, 3, effect),
                ).SetTarget(Scheme2),
            )
        elif PlancheEstArme(effect):
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Deal 4 damage to an enemy",
                    lambda cibles: this.DealDamage(cibles, 4, effect),
                ).SetTarget(Enemy),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            disaster,
        ).SetPlay().SetLabel('thwart', 'attack')
        .SetHasNoTargetEffect(),
    ]
