from . import *

# Seizure : OBLIGATION, boost 2. A donner au joueur de Destiny.
# You may flip to alter-ego form. Choose:
# • Exhaust Irene Adler -> remove Seizure from the game.
# • Discard 1 [[SKILL]] upgrade you control. If no upgrade was discarded this way, this card gains surge. Discard this obligation.
#
# CARTES DE REFERENCE
#  - `mt011` Psychic Tremor (Mantis) : meme gabarit (`WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm` + `ChooseAbilities`, branche 1 `condition=joueur.IsAlterEgo()` + `Exhaust("YourIdentity")`).
#  - `01165` Eviction Notice / `03026` : obligations a deux branches ; `this.GainSurge(1, effect)`.
#
# TEXTE CONTRE CODE
#  « Exhaust IRENE ADLER » : l'alter-ego (donc seulement s'il est en forme alter-ego, apres l'eventuelle bascule). « remove Seizure FROM THE GAME » : la carte quitte la partie (branche 1). « Discard 1 SKILL upgrade YOU
#    CONTROL » : une amelioration portant SKILL sous le controle du joueur, choisie par lui ; sans aucune, la branche reste offerte et la carte gagne le surge. « If NO upgrade was discarded this way, this card gains surge.
#    Discard this obligation » appartient a la SECONDE branche (comme sur les obligations officielles).
#  Chiffres : boost 2, 1 amelioration.


def GetAbilities() -> Sequence['Ability']:

    def seizure(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(joueur, effect)

        skills = [f for f in joueur.GetControlUpgrade() if f.HasTrait("SKILL")]

        def defausser_et_defausser_celle_ci(cibles: Sequence['CardFace']) -> None:
            Faces.DiscardAll(cibles, effect)
            if not cibles:
                this.GainSurge(1, effect)
            Faces.DiscardAll([this], effect)

        seconde = AbilityFactory.ForChoiceAbility(
            "Discard 1 SKILL upgrade you control. Discard this obligation",
            defausser_et_defausser_celle_ci,
        )
        if skills:
            seconde.SetTarget(Upgrade, trait="SKILL", from_where=["YouControlCards"], canbe_discard=True)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Irene Adler → remove Seizure from the game",
                lambda cibles:
                    Faces.RemoveAllFromGame([this], effect),
                condition=joueur.IsAlterEgo(),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
            seconde,
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            seizure,
        ),
    ]
