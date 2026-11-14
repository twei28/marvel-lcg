from . import *

# Fractured Psyche : OBLIGATION, boost 2 (« Menace 2 »). A donner au joueur de Robert Reynolds.
# You may flip to alter-ego form. Choose:
# • Exhaust Robert Reynolds → remove Fractured Psyche from the game.
# • Place 3 balance counters on Duality Aspect. Discard this obligation.
#
# CARTES DE REFERENCE
#  - `ca014` (Essential Bloodlust, meme gabarit) / `dy013` / `my015` : `WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm` + `ChooseAbilities`, branche 1 `condition=joueur.IsAlterEgo()` + `Exhaust("YourIdentity")`.
#  - « place 3 balance counters » : helper `PoserEquilibre` (The Watchtower peut en detourner UN, `WhenCardWouldBePlacedCounter`).
#
# TEXTE CONTRE CODE
#  « You may flip to alter-ego form » : bascule facultative avant le choix. « Exhaust ROBERT REYNOLDS » : l'alter-ego, PRET et en forme alter-ego (apres l'eventuelle bascule).
#  « Place 3 balance counters on Duality Aspect. Discard this obligation » : la defausse appartient a la SECONDE branche (la premiere la retire de la partie). Aucun surge (le texte n'en parle pas).
#  Chiffres : boost 2 (Menace 2), 3 compteurs.


def GetAbilities() -> Sequence['Ability']:

    def fractured_psyche(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(joueur, effect)

        def trois_compteurs_puis_defausser(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            PoserEquilibre(effect, 3)
            Faces.DiscardAll([this], effect)

        premiere = AbilityFactory.ForChoiceAbility(
            "Exhaust Robert Reynolds → remove Fractured Psyche from the game",
            lambda cibles:
                Faces.RemoveAllFromGame([this], effect),
            condition=joueur.IsAlterEgo() and joueur.GetIdentity().IsReady(),
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))

        seconde = AbilityFactory.ForChoiceAbility(
            "Place 3 balance counters on Duality Aspect. Discard this obligation",
            trois_compteurs_puis_defausser,
        ).SetHasNoTargetEffect()

        joueur.ChooseAbilities(effect, premiere, seconde)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            fractured_psyche,
        ),
    ]
