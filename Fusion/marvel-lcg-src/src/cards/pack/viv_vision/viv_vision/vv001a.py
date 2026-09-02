from . import *

# * Viv Vision (face heros) — ANDROID. CHAMPION.
# THW 1 / ATK 1 / DEF 1 — HS 5 / PV 10
# Density Manipulation — Action: Spend a [energy] resource -> you get +2 to a
#   chosen basic power until the end of the round. (Limit once per round.)
#
# Cartes de reference :
#  - 01068 * Vision (allie du Core Set), src/cards/pack/core/01068.py : texte
#    quasi identique (« Spend a [energy] resource -> choose THW or ATK. Until
#    the end of the phase, Vision gets +2 to the chosen power. »), meme
#    montage `WhenInYourPlayTurn(Action, ...).SetCost(Cost("Y"))` + un
#    `ForChoiceAbility` par pouvoir. DEUX ecarts codes ici : la duree est le
#    ROUND et non la phase, et le choix porte sur les TROIS pouvoirs de base ;
#  - ag001b * Sharon Carter (meme auteur, Rainy) pour le couple
#    `.SetName(<nom italique de la capacite>)` + `.LimitOncePerRound()` sur une
#    action d'identite au texte imprime « Action: » nu.
#
# ⚠ NE PAS partir du heros officiel 26001a * Vision : sa capacite est la
# bascule de forme de masse (Dense / Intangible), sans aucun rapport.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « YOU get +2 » et non « Viv Vision gets +2 » : « you » designe
#    l'IDENTITE, donc les deux faces. `GainUntilRoundEnd` a `ignore_flip=True`
#    par defaut et applique le bonus a `this.card.face`, la face COURANTE :
#    le bonus survit donc a un passage en alter-ego, ce qui est le
#    comportement voulu. (Piege documente au §3 de RECETTES-MOTEUR, ligne
#    « NOM gets +X vs YOU get +X », trouve en partie reelle sur an002.)
#  - « a chosen BASIC power » : les pouvoirs de base sont THW, ATK et DEF.
#    Le REC de l'alter-ego n'en est pas un, et la carte est de toute facon
#    portee par la face heros.
#  - « until the end of the ROUND », pas de la phase : `GainUntilRoundEnd`,
#    pas `GainUntilPhaseEnd` comme 01068.
#  - « (Limit once per round.) » : `.LimitOncePerRound()`. La variante du
#    sous-dossier « Vivian alt cards » imprime « once per POWER per round »,
#    elle a ete ecartee (voir le __init__ du pack).


def GetAbilities() -> Sequence['Ability']:

    def density_manipulation(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        def gain_thw(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            this.GainUntilRoundEnd(effect, thwart=2)

        def gain_atk(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            this.GainUntilRoundEnd(effect, attack=2)

        def gain_def(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            this.GainUntilRoundEnd(effect, defense=2)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("THW", gain_thw),
            AbilityFactory.ForChoiceAbility("ATK", gain_atk),
            AbilityFactory.ForChoiceAbility("DEF", gain_def),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            density_manipulation,
        ).SetCost(Cost("Y"))
        .SetName("Density Manipulation")
        .LimitOncePerRound(),
    ]
