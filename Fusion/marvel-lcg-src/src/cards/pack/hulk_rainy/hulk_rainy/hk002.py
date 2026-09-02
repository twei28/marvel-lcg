from . import *

# * Black Widow (Natasha Romanoff) — ALLIE signature, x1 (n/15 = 1).
# AVENGER. S.H.I.E.L.D. SPY. Cout 3 / PV 3 / THW 2* / ATK 1*
# Ressource imprimee : etoile VERTE = wild (RES = "G").
# [star] Response: After Black Widow thwarts, remove 1 threat from another
#   scheme.
# Hero Action: Exhaust Black Widow -> flip to your alter-ego form.
#
# Cartes de reference :
#  - `aa019` * Wiccan (pack agatha_harkness) : meme declencheur exact
#    « After <allie> thwarts », rendu par `AfterUnitAttackOrThwart(Response,
#    "This", op, conditions=[seulement_thwart])` — la fabrique couvre les
#    deux, on filtre sur le TYPE du message ;
#  - `ag005` Parting Shots pour la bascule de forme :
#    `joueur.GetIdentity().ChangeToForm(AlterEgo, effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « from ANOTHER scheme » : pas celle qu'elle vient de contrer.
#    `exclude=` sur le selecteur, avec les manigances effectivement menees
#    (`message.schemes`). Sans ça, la carte retirerait deux fois de la meme,
#    ce que le texte interdit.
#  - Le `[star]` en tete de la Response : capacite permanente de la carte,
#    toujours active, PAS une capacite de boost (fiche mots-cles/special.md).
#    Aucun montage particulier, c'est une Response ordinaire.
#  - « Exhaust Black Widow -> » : la fleche fait de l'epuisement un COUT.
#  - « flip to YOUR alter-ego form » : l'identite du joueur, pas l'alliee.
#  - `Hero Action` : indisponible en forme civile — ce qui est coherent, la
#    carte sert justement a QUITTER la forme heros.
#  - THW 2* et ATK 1* : l'etoile est le degat consequent, lu nativement dans
#    `desc`, aucun script.


def GetAbilities() -> Sequence['Ability']:

    def seulement_thwart(effect: 'Effect', message: 'Message2') -> bool:
        Unused(effect)
        return isinstance(message, Message.AfterUnitThwartEnd)

    def apres_avoir_contre(effect: 'Effect', message: 'Message.AfterUnitThwartEnd') -> None:
        this = effect.this.CastTo(Ally)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        # « ANOTHER scheme » : on exclut celle(s) que Black Widow vient de
        # contrer, sinon la carte se retirerait de la meme deux fois.
        deja = [s for s in (message.schemes or []) if s is not None]

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 1 threat from another scheme",
                lambda cibles: this.RemoveThreatFromSchemes(cibles, 1, effect),
            ).SetTarget(Scheme2, exclude=deja, has_threat=True),
        )

    def basculer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        identite = initiator.GetIdentity()
        if identite is not None and initiator.IsHero():
            identite.ChangeToForm(AlterEgo, effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.AfterUnitAttackOrThwart(
            AbilityType.Response,
            "This",
            apres_avoir_contre,
            conditions=[seulement_thwart],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            basculer,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
