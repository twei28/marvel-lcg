from . import *

# Squad Car : SOUTIEN (VEHICLE), cout 3, [energy].
# You get +1 hand size.
# Alter-Ego Action: Exhaust Squad Car → shuffle 1 RoboCop card from your discard pile into your deck.
#
# CARTES DE REFERENCE
#  - `mf005` / `27191` : `GiveKeywordToInPlayWhenApplyThis("You", hand_size=1)` pour « you get +1 hand size ». `bf010` Sunnydale Library : meme Action (melanger 1 carte
#    d'identite de la defausse dans le deck : `ChoisirUne` + `Faces.ShuffleAllTo`).
#
# TEXTE CONTRE CODE
#  « You get +1 hand size » -> l'identite du joueur, quelle que soit sa forme. « 1 RoboCop card » -> une carte propre a l'identite (classe Hero : le deck de heros, jamais une
#    carte d'aspect) ; le joueur choisit si plusieurs. « from YOUR discard pile into YOUR deck » : le melange est imprime. Alter-Ego Action : forme alter-ego seulement.
#  Chiffres : cout 3, +1 main.


def GetAbilities() -> Sequence['Ability']:

    def squad_car(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)
        joueur = effect.GetInitiator()
        candidates = [f for f in joueur.discard_pile.Get() if ClassCard.IsType(f) and f.IsClass("IdentitySpecific")]
        if not candidates:
            return
        carte = candidates[0] if len(candidates) == 1 else joueur.AskChooseFace(
            candidates, effect, prompt="Squad Car : shuffle 1 RoboCop card into your deck", forced=True)
        if carte is not None:
            Faces.ShuffleAllTo([carte], joueur.player_deck, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            hand_size=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            squad_car,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
