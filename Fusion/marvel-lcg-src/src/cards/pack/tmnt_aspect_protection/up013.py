from . import *

# * Groo the Wanderer — ALLIE 2 [physical], aspect Protection (TMNT Reskins, Inkwire). BARBARIAN.
# THW 2 (2 degats consecutifs), ATK 3 (1), PV 4.
# Forced Response: After Groo the Wanderer enters play under your control, deal yourself 1 facedown
#   encounter card.
#
# MODIFIEE de `20016` Star-Lord (texte de la Reponse forcee repris mot pour mot, SANS la ligne
# « [star] Star-Lord's attacks gain ranged »). Script propre : l'ability_link apporterait le ranged.
#
# CARTE DE REFERENCE : `20016` Star-Lord, `AfterCardEnterPlay(ForcedResponse, "This", ...)` puis
# `DealEncounterCards(1)`. `10012` Sentry porte le meme effet.
#
# TEXTE CONTRE CODE
#  ⚠ « deal YOURSELF » : le joueur qui le controle (`GetInitiator`), une carte face cachee (distribuee,
#    pas revelee : `DealEncounterCards`).
#  ⚠ Aucun mot-cle ranged (difference avec 20016).


def GetAbilities() -> Sequence['Ability']:

    def groo(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        effect.GetInitiator().DealEncounterCards(1, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            groo,
        ),
    ]
