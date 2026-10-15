from . import *

# Call for Help — evenement signature, x1 (2/15). Cout 0, ressource [energy].
# Hero Action: Search your deck and discard pile for an ally or the I'm Here to
#   Help player side scheme and add it to your hand. (Shuffle.)
#
# Cartes de reference :
#  - `lady_sif/ls005` To Arms! : meme squelette « fouille deck + defausse,
#    GainCard » (`Search.PlayerCard(include_player_deck=True,
#    include_discard_pile=True)` + `initiator.GainCard`) ;
#  - le « ou » de deux filtres : `vnm/20005` combine deux `CardFinder` par
#    `|` ; `Search.SearchForCards` fait `CardFinder(...) & finder`
#    (search.py:356), donc `finder=A | B` est accepte.
#
# ⚠ Mots-pieges :
#  - « an ally OR the I'm Here to Help side scheme » : UNE seule carte, d'un
#    des deux filtres. La manigance est ciblee par card_id (tm009), pas par
#    nom : « I'm Here to Help » est unique a ce pack mais le card_id est sur.
#  - « deck AND discard pile » : les deux. « add it to your HAND » : GainCard.
#  - Hero Action : jouable en forme de heros seulement (SetPlay()).

def GetAbilities() -> Sequence['Ability']:

    def appel_a_l_aide(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            finder=CardFinder(card_type=Ally) | CardFinder(card_ids=["tm009"]),
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            appel_a_l_aide,
        ).SetPlay(),
    ]
