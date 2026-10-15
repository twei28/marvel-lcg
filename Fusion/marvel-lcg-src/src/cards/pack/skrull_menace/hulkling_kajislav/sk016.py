from . import *

# * Mur-G'nn — allie d'aspect PROTECTION (n° 16). KREE. SKRULL.
# Cout 3 [mental]. THW 2* / ATK 2* (1 degat consecutif chacun), 2 PV.
# Action: Exhaust Mur-G'nn and deal 1 damage to her → discard the top card of
#   your deck. If that card's printed resource has:
#   [physical] - Ready a card your control.
#   [energy] - Give an identity a tough status card.
#   [mental] - Heal 3 damage from a character.
#
# Cartes de reference :
#  - **`09004`** Magic Blast / `01050` * Hulk : « discard the top card of your
#    deck. If that card's printed resource has: ... » =
#    `initiator.DiscardDeckTopCard(effect)` + `FacesCounter.GetPrintedResources`
#    et un test par couleur.
#  - **`22012`** * Wraith : cout « exhaust X and deal 1 damage to him → » =
#    `CostFunc.Exhaust("This")` + `CostFunc.DealDamage(1, "This")`.
#  - `40041` Luck Be a Lady pour les choix cibles (`ForChoiceAbility(...)
#    .SetTarget(Unit2, canbe_heal=True)`).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « printed resource **has** » : chaque couleur PRESENTE declenche son
#    effet, une fois (deux icones physiques = un seul redressement).
#  - **WILD** : decision de l'utilisateur (15/10/2026), lecture litterale :
#    un wild n'est ni physique, ni energie, ni mental => AUCUN effet. Hulk et
#    Magic Blast listent le wild a part ; Mur-G'nn ne le fait pas.
#  - « Ready a card **you control** » (coquille imprimee « your control ») :
#    `from_where=["YouControlCards"]`.
#  - « **an identity** » : n'importe quel joueur ; « **a character** » : tout
#    personnage, y compris un ennemi (le joueur choisit).
#  - « Action » nue : utilisable dans les deux formes.
#  - Les PV de Mur-G'nn sont 2 : se blesser deux fois la detruit.


def GetAbilities() -> Sequence['Ability']:

    def murgnn(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)

        joueur = effect.GetInitiator()
        face = joueur.DiscardDeckTopCard(effect)
        if face is None:
            return
        res = FacesCounter.GetPrintedResources([face])

        if res.r:
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Ready a card you control",
                    lambda cibles: Faces.ReadyAll(cibles, effect),
                ).SetTarget(from_where=["YouControlCards"]),
            )
        if res.y:
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Give an identity a tough status card",
                    lambda cibles: Faces.GiveStatus(cibles, "Tough", effect),
                ).SetTarget(Identity, canbe_tough=True),
            )
        if res.b:
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Heal 3 damage from a character",
                    lambda cibles: this.HealthUnits(cibles, 3, effect),
                ).SetTarget(Unit2, canbe_heal=True),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            murgnn,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.DealDamage(1, "This")),
    ]
