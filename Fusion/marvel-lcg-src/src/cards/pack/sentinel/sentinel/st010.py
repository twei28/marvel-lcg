from . import *

# * Juston Seyfert — Soutien 1 [wild], unique, classe Hero. PERSONA.
# Action: Attach to a side scheme.
# Hero Action: Exhaust Juston Seyfert → remove 1 threat from attached side
#   scheme.
# Forced Response: After attached side scheme is defeated, put Juston Seyfert
#   in play under your control. Ready Sentinel or up to 2 [[COMPONENT]]
#   upgrades.
#
# Cartes de reference :
#  - `04135` Twisted Reality et `03032` Followed : une carte attachee a une
#    manigance annexe qui se declenche quand celle-ci est vaincue,
#    `WhenSchemeBeDefeated(..., "AttachedSideScheme", ...)`.
#  - `09009` Cloak of Levitation pour l'action a inclinaison.
#  - `dz037` pour le choix entre deux branches (`ChooseAbilities`, obligatoire
#    ici : le texte dit « Ready X **or** Y », sans possibilite de refuser).
#
# ⚠ CORRECTIF MOTEUR ASSUME. Le moteur ne savait attacher que les `Asset2`
# (ameliorations et attachements) : `Support` n'heritait pas de `CanAttach`, et
# « Action: Attach to a side scheme » sur un SOUTIEN etait donc impossible.
# Plutot que de mentir sur le type imprime (la carte dit SUPPORT, image a
# l'appui), `CanAttach` a ete ajoute a `Support`
# (src/game/card/face/card_type/support.py). L'ajout est inerte pour les
# soutiens existants : tous les points d'entree de `CanAttach` testent d'abord
# `bind_face`, qui reste None sans appel explicite a `AttachTo2`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Attach to a **side** scheme » : annexe uniquement, `SchemeSide2`
#    couvre les deux familles (rencontre et joueur), pas le complot principal.
#  - « **put** Juston Seyfert in play » : il revient EN JEU, normalement, sous
#    le controle du joueur. Il quitte la manigance vaincue, il ne la suit pas
#    a la defausse. La fenetre est donc « When ... be defeated », avant que la
#    manigance n'emporte ses cartes attachees.
#  - « Ready Sentinel **or up to 2** COMPONENT upgrades » : un choix entre deux
#    branches, pas les deux. La seconde branche accepte zero, une ou deux
#    cartes, et vise les Component des DEUX faces (rien n'exige INTACT ici).


def GetAbilities() -> Sequence['Ability']:

    def poser_juston(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        joueur = effect.GetInitiator()
        this.PutIntoPlay(joueur, effect)

        if effect.targets:
            this.CastTo(CanAttach).AttachTo2(effect.targets[0], effect)

    def deminer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        manigance = this.GetBindFace()
        if manigance is not None:
            this.RemoveThreatFromSchemes([manigance], 1, effect)

    def revenir_au_bercail(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        joueur = effect.GetInitiator()
        this.PutIntoPlay(joueur, effect)

        def redresser(cibles: Sequence['CardFace'], e: 'Effect') -> None:
            Faces.ReadyAll(cibles, e)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility3("Ready Sentinel", redresser)
            .SetTarget("YourIdentity", canbe_ready=True),
            AbilityFactory.ForChoiceAbility3(
                "Ready up to 2 COMPONENT upgrades", redresser)
            .SetTarget(
                Upgrade,
                trait=TRAIT_COMPONENT,
                canbe_ready=True,
                from_where=["YouControlCards"],
                range=("Zero", 2),
            ),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.PlayTurnOption,
            poser_juston,
            conditions=[
                lambda effect, message:
                    Condition.FieldHasNotThisUniqueType(effect.this, effect)
            ],
        ).SetPlay().SetTarget(SchemeSide2),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            deminer,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.ForcedResponse,
            "AttachedSideScheme",
            revenir_au_bercail,
        ),
    ]
