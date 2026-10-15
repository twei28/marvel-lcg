from . import *

# Spy Training — COMPLOT ANNEXE (Skrull Elite - Crusader). Menace 3[per_hero], 1 icone de boost,
# icone HAZARD (carte penchee nue : lecture du 15/10/2026, voir defs/modulaires_questions.md).
# When Revealed: Defeat an ally you control and give the villain 1 facedown boost card.
#
# Cartes de reference :
#  - « Defeat an ally you control » : **`ls015`** Skurge, Boost (`ChooseAbilities` + `ForChoiceAbility(...)
#    .SetTarget(Ally, from_where=["YouControlCards"])` + `Faces.DefeatUnits`).
#  - « Give the villain 1 facedown boost card » : **`sk167`** White Tiger (`Faces.GiveFacedownBoostCards`).
#  - Hazard : natif (`desc.Hazard`, fiche mots-cles/hazard.md).
#
# ⚠ Mots-pieges : « an ally YOU control » (le joueur qui revele choisit parmi SES allies, jamais ceux
# d'un autre joueur) ; « AND give the villain » : deux effets independants (sans allie, la carte de boost
# est donnee quand meme : lecture a confirmer, defs/modulaires_questions.md) ; « DEFEAT » (vaincre : la
# defaite passe par les fenetres When Defeated / Victory, pas une defausse).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        if list(joueur.allies.Get()):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Defeat an ally you control",
                    lambda cibles: Faces.DefeatUnits(list(cibles), this, effect),
                ).SetTarget(Ally, from_where=["YouControlCards"]),
            )
        DonnerBoostAuMechant(effect, 1)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
