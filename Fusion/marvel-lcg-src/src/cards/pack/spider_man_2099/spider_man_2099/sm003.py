from . import *

# Accelerated Decoy — EVENEMENT, cout 2 [energy]. SUPERPOWER.
# Hero Action: Choose to either confuse an enemy or give your hero a tough
#   status card. If you played this card using your Acceleration ability, do
#   both instead.
#
# CARTES DE REFERENCE
#  - `22005` Evasive Maneuvering : le montage exact d'un « choose either A or
#    B » ou chaque branche a SA cible — `ChooseAbilities` + deux
#    `ForChoiceAbility(...).SetTarget(Enemy, canbe_confused=True)`.
#  - `05015` Tackle, `01083` : `Faces.GiveStatus(cibles, "Confused"/"Tough",
#    effect)`.
#  - `ho001a`, `08013` Stealth Strike : le choix a deux branches DANS
#    l'operation.
#
# TEXTE CONTRE CODE
#  ⚠ « do BOTH INSTEAD » : « instead » remplace le choix, il ne le double pas.
#    Sous Acceleration on ne pose donc PAS la question — les deux effets
#    partent. C'est bien un « instead » de deplacement de branche, pas une
#    duplication (lecon The Spot, PROCESSUS-CARTE §5).
#  ⚠ « GIVE YOUR HERO a tough status card » : la cible est l'identite du
#    joueur, pas un personnage au choix. On ne passe donc pas par un
#    `SetTarget` : `Faces.GiveStatus([heros], "Tough", effect)`.
#    ⚠ Et le repli n'est PAS declare en `SetTarget(canbe_tough=True)` : sans
#    cible legale l'abilite ne partirait jamais et la branche « confuse »
#    deviendrait morte (piege `ah007`, RECETTES §2).
#  ⚠ « confuse AN ENEMY » : `canbe_confused=True` dans le selecteur, sans quoi
#    un ennemi Stalwart serait propose pour rien (RECETTES §2).
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def confondre(effect: 'Effect', cibles: Sequence['CardFace']) -> None:
        Faces.GiveStatus(cibles, "Confused", effect)

    def robuste(effect: 'Effect') -> None:
        heros = HerosDuJoueur(effect)
        if heros is not None:
            Faces.GiveStatus([heros], "Tough", effect)

    def leurre(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        if JoueViaAcceleration(effect):
            # « do both INSTEAD » : aucune question, les deux effets partent.
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Confuse an enemy",
                    lambda cibles: confondre(effect, cibles),
                ).SetTarget(Enemy, canbe_confused=True),
            )
            robuste(effect)
            return

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Confuse an enemy",
                lambda cibles: confondre(effect, cibles),
            ).SetTarget(Enemy, canbe_confused=True),
            AbilityFactory.ForChoiceAbility(
                "Give your hero a tough status card",
                lambda cibles: robuste(effect),
            ),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            leurre,
        ).SetPlay(),
    ]
