from . import *

# Psychic Paragon (manigance annexe PSIONIC, Boost 2, menace 4 par joueur). « Emma Frost gets +10 hit point. Each ILLUSION card gains incite 1. When Revealed : Deal 1
# facedown encounter card to each player with no engaged minions. »
# Cartes de reference : 21160 / hf501 (`GiveKeywordToInPlayWhenApplyThis(CardFinder(name=...), health=10)`), 39035 Dial M for Mojo (`GiveKeywordToInPlayWhenApplyThis(
# EncounterCard, incite=1)`), `AbilityFactory.WhenThisRevealed`.
# ⚠ « +10 hit point » : flat (le scan n'imprime pas d'icone « par joueur »). Sur la face A2/B2 (PV infinis) ce bonus ne change rien ; il est RECALCULE au retour sur la face
# active (cas `hf509 ... cycle`). ⚠ L'interruption de defaite d'Emma retire 5 menaces de CHAQUE manigance, celle-ci comprise : a moins de 5 menaces, Paragon est vaincue.


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        DonnerUneCarteFaceCachee(effect, [j for j in JoueursDansLOrdre(effect) if SansSbireEngage(j)])

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(name=NOM_EMMA, card_type=Villain), health=10),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder2(ILLUSION, EncounterCard), incite=1),
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
