from . import *

# Ancestors — soutien signature (12/16). KREE. SKRULL. Cout 1 [wild].
# Uses (2 individual counters).
# Action: Exhaust this card and remove 1 individual counter from it → choose 1
#   card in your hand or in play. That card gains the [[KREE]] or [[SKRULL]]
#   trait until the end of the round.
#
# Cartes de reference :
#  - **`22034`** Defensive Training : « Uses (2 training counters). Action:
#    Exhaust this card and remove 1 training counter from this → ... » Meme
#    montage de cout : `CostFunc.Exhaust("This")` + `CostFunc.Counter("This",
#    1, 'training')` ; `desc.Uses = "2,training"` (le moteur defausse la carte
#    quand le dernier compteur part, mot-cle Uses).
#  - **`im004`** Take Flight : `face.GainUntilRoundEnd(effect, trait=...)`
#    (face_action.py), « gains the X trait until the end of the round ».
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « individual counters » : simple NOM de compteur (`individual`, ajoute a
#    l'enum COUNTER le 15/10/2026), 2 utilisations.
#  - « in your hand **or in play** » : decision de l'utilisateur (15/10/2026),
#    lecture litterale : TOUTE carte en jeu, y compris celles des autres
#    joueurs et du mechant, en plus de ta main.
#  - « the KREE **or** SKRULL trait » : UN seul des deux, au choix du joueur.
#  - « until the end of the **round** », pas de la phase.
#  - « Action » (pas Hero Action) : les deux formes.
#  - Usage typique (FAQ du livret p. 21) : donner a Hulkling le trait qu'il
#    n'a pas, pour qu'il ait les DEUX (sk006 Shift and Strike desoriente ET
#    etourdit).


def GetAbilities() -> Sequence['Ability']:

    def ancetres(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        joueur = effect.GetInitiator()
        candidates = list(joueur.hand_cards.Get()) + [
            f for f in Worlds.GetOnFieldCards(effect) if f.IsInPlay()
        ]
        if not candidates:
            return
        choisie = joueur.AskChooseFace(
            candidates, effect,
            prompt="Choose a card: it gains the KREE or SKRULL trait until the end of the round",
        )
        if not choisie:
            return

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "KREE",
                lambda cibles: choisie.GainUntilRoundEnd(effect, trait="KREE"),
            ),
            AbilityFactory.ForChoiceAbility(
                "SKRULL",
                lambda cibles: choisie.GainUntilRoundEnd(effect, trait="SKRULL"),
            ),
        )
        Unused(this)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            ancetres,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'individual')),
    ]
