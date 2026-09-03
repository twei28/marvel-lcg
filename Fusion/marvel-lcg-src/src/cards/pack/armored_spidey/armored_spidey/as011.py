from . import *

# * Parker Industries — soutien signature, x1. LOCATION. Cout 1,
# ressource [wild].
# Alter-Ego Action: Exhaust Parker Industries -> look at the top 3 cards of
#   your deck. Add 1 to your hand and discard the others.
#
# Cartes de reference :
#  - **`lj005`** * Kamala's Room (pack lockjaw) : MEME TEXTE, au nom pres.
#    Le module y a deja ete corrige le 9/8/2026 — `LookAtDeck` n'accepte ni
#    `gain` ni `discard_other`, et `"PlayerDeck"` n'est pas une valeur
#    reconnue. La forme juste est : relever le dessus du deck AVANT la
#    recherche, `Faces.LookAt`, `Search.PlayerDeckTop`, `GainCard`, puis
#    `Faces.DiscardAll` sur le reste.
#  - `01029b` * Tony Stark (Futurist) pour le meme texte sans l'inclinaison.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « discard **the others** » : les 2 cartes NON gardees vont a la
#    DEFAUSSE, pas au fond du deck. C'est la difference exacte avec `15007`
#    * Agatha Harkness, qui imprime « place the rest on the bottom of your
#    deck ».
#  - Le dessus du deck se releve AVANT la recherche : `Search.PlayerDeckTop`
#    peut remanier le deck, et il faut savoir quelles cartes defausser
#    ensuite (correctif lj005).
#  - Un deck de moins de 3 cartes ne fait pas tomber la capacite : la liste
#    est tronquee, et un deck vide sort sans rien faire.
#  - « **Alter-Ego** Action » : rien en forme heros.


def GetAbilities() -> Sequence['Ability']:

    def parker_industries(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        dessus = list(initiator.player_deck.Get(True))[:3]
        if not dessus:
            return

        Faces.LookAt(dessus, initiator, effect)

        gardee = Search.PlayerDeckTop(effect, initiator, 3)
        if gardee is None:
            return
        initiator.GainCard(gardee, effect)

        autres = [face for face in dessus if face is not gardee]
        if autres:
            Faces.DiscardAll(autres, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            parker_industries,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
