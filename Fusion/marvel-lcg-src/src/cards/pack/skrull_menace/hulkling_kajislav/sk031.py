from . import *

# Interracial Hatred — OBLIGATION du set Hulkling (n° 31). 1 icone boost.
# Give to the Teddy Altman player.
# Cards with the [[KREE]] and [[SKRULL]] trait you control cannot ready.
# Alter-Ego Action: Exhaust Teddy Altman → discard this obligation.
#
# Cartes de reference :
#  - **`40160`** Manufactured Drama : « Supports you control cannot ready. ...
#    Alter-Ego Action: ... discard this card » = `*CardCannotReady(Support,
#    control_by="You")` + `WhenInYourPlayTurn(AlterEgoAction, op)` qui
#    `Faces.DiscardAll([this])`. L'obligation reste en jeu (Obligation.
#    OnWhenCardRevealed la met dans la zone d'obligations du joueur).
#  - `28021` Weight of the World : `CostFunc.Exhaust("YourAlterEgo")`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « KREE **and** SKRULL » : decision de l'utilisateur (15/10/2026) = les
#    cartes KREE ET les cartes SKRULL, donc toute carte qui porte l'UN des deux
#    (`CardFinder(traits=[...])` est un OU). Hulkling en forme heros a
#    toujours l'un des deux (son origine) : il ne se redresse plus.
#  - « you control » : `control_by="You"`, le porteur de l'obligation.
#  - Teddy Altman (HYBRID) n'a NI KREE NI SKRULL : en forme civile il peut
#    se redresser, et c'est lui qui paie l'Action de defausse. C'est la sortie
#    prevue par la carte.
#  - « Exhaust **Teddy Altman** → » : `Exhaust("YourAlterEgo")`.
#  - « **discard** this obligation » (pas « remove from the game »).


def GetAbilities() -> Sequence['Ability']:

    def defausser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)
        Faces.DiscardAll([this], effect)

    return [
        *AbilityFactory.CardCannotReady(
            CardFinder(traits=["KREE", "SKRULL"]),
            control_by="You",
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            defausser,
        ).SetCostFunc(CostFunc.Exhaust("YourAlterEgo")),
    ]
