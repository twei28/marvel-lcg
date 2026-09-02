from . import *

# Brilliant Mind — evenement signature, x2 (n/15 = 2 et 3). THWART.
# Cout 2, ressource [mental].
# Alter-Ego Action (thwart): Remove 3 threat from a scheme. If you paid for
#   this card using only [mental] resources, choose to either remove 2
#   additional threat from that scheme or confuse an enemy.
#
# Cartes de reference :
#  - **`10004` Sub-Orbital Leap** (Hulk officiel) pour « using ONLY » :
#    `effect.GetPaidResources().OnlyHasColor("R")` la-bas, "B" ici ;
#  - `08013` Stealth Strike / `ho001a` pour le choix a deux branches par
#    `ChooseAbilities` + deux `ForChoiceAbility`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « using ONLY [mental] » : `OnlyHasColor`, PAS `HasColor`. La nuance est
#    dans le pack : hk006 imprime « using A [physical] » et prend `HasColor`,
#    hk005 imprime « OVERPAID with » et prend encore autre chose. Trois
#    tournures, trois lectures — detail dans le __init__ du pack.
#    ⚠ Un WILD compte comme mental ici : `OnlyHasColor` convertit le vert par
#    defaut, ce qui est la regle du jeu (un wild vaut la couleur voulue).
#  - « remove 2 additional threat from THAT scheme » : LA MEME manigance que
#    les 3 premieres menaces, pas un second choix. On reutilise
#    `effect.targets`, on ne repose pas de selecteur.
#  - « choose to EITHER ... OR ... » : un choix, pas les deux. Deux
#    `ForChoiceAbility` dans un seul `ChooseAbilities`.
#  - `Alter-Ego Action` : la carte ne se joue QU'EN forme civile. C'est
#    coherent avec le CTR 0 de la face heros : toute la menee de Hulk passe
#    par Bruce Banner.
#  - Le libelle `(thwart)` alimente Sonne/Desoriente : `.SetLabel('thwart')`.


def GetAbilities() -> Sequence['Ability']:

    def brilliant_mind(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.RemoveThreatFromSchemes(effect.targets, 3, effect)

        if not effect.GetPaidResources().OnlyHasColor("B"):
            return

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        def menace_en_plus(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            # « from THAT scheme » : la meme manigance, pas un nouveau choix.
            this.RemoveThreatFromSchemes(effect.targets, 2, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 2 additional threat from that scheme",
                menace_en_plus,
            ),
            AbilityFactory.ForChoiceAbility(
                "Confuse an enemy",
                lambda cibles: Faces.GiveStatus(cibles, "Confused", effect),
            ).SetTarget(Enemy, canbe_confused=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            brilliant_mind,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
