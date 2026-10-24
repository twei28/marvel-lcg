from . import *

# Cosmic Speed — Evenement, cout 3, ressource [energy]. COSMIC. THWART.
# Hero Action (thwart): Choose one:
#  • Remove 4 threat from a scheme.
#  • Discard The Silver Surfboard -> remove up to 3 threat from each scheme in play.
#
# Cartes de reference :
#  - `08013` Stealth Strike (bkw) / `14004` Double Time (qsv) : UN SEUL module `Play` qui fait le choix
#    lui-meme par `joueur.ChooseAbilities(effect, ForChoiceAbility(...).SetTarget(...))`. Choisir ainsi evite
#    la liste blanche des evenements a DEUX capacites de jeu (`game/card/factory.py`, lecon ls005).
#  - `13003` Giant Help (wsp) : `SetLabel('thwart')`.
#  - `RemoveThreatFromSchemes("EachScheme", n, effect)` (card_face.py) pour « each scheme in play ».
#
# ⚠ Mots-pieges :
#  - « up to 3 threat from EACH scheme in play » : toutes les manigances (principale et annexes), 3 maximum
#    chacune ; ce n'est PAS un choix de cible.
#  - « Discard The Silver Surfboard -> » : la defausse est un COUT, la 2e option n'existe que si la planche
#    est EN JEU chez le joueur ; elle passe par `Faces.DiscardAll`, donc l'Interruption de sv003 se propose.
#  - « (thwart) » : l'evenement compte comme une action de contre (statut Desoriente).


def GetAbilities() -> Sequence['Ability']:

    def vitesse_cosmique(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        def retirer_quatre(cibles: Sequence['CardFace']) -> None:
            this.RemoveThreatFromSchemes(cibles, 4, effect)

        def tout_balayer(cibles: Sequence['CardFace']) -> None:
            planche = LaPlanche(effect, joueur)
            if planche is None:
                return
            Faces.DiscardAll([planche], effect)
            this.RemoveThreatFromSchemes("EachScheme", 3, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 4 threat from a scheme",
                retirer_quatre,
            ).SetTarget(Scheme2),
            AbilityFactory.ForChoiceAbility(
                "Discard The Silver Surfboard → remove up to 3 threat from each scheme in play",
                tout_balayer,
                condition=LaPlanche(effect, joueur) is not None,
            ).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            vitesse_cosmique,
        ).SetPlay().SetLabel('thwart'),
    ]
