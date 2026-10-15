from . import *

# Earth Involvement — COMPLOT ANNEXE (Kree-Skrull War). Menace 1[per_hero], aucune
# icone de boost. PERMANENT et SETUP.
# Permanent. Setup.
# While there is at least 1 threat here, this card gains a crisis icon.
# Forced Response: After a card that belongs to the Kree-Skrull War encounter
#   set is revealed, place 2 threat here.
#
# Cartes de reference :
#  - **`60113a`** Establish Trust (pack fne) : complot annexe Permanent + Setup, les
#    deux mots-cles sont des cles `desc` (bases automatiques, aucun script ; fiches
#    permanent.md et setup.md). Il entre en jeu a l'etape 11 de la mise en place.
#  - **`nebu/22013`** Venom Flash : `ThisGainKeyword(op, ..., change_on_event=
#    OnEvent.Threat("This"))` = un bonus qui suit la MENACE de la carte ;
#    **`40109`** Pure Force pour l'icone de crise conditionnelle (`crisis=1`).
#  - **`jj001b`** / **`27190`** : `AfterPlayerRevealCard(ForcedResponse, "AnyPlayer",
#    CardFinder(...), op)` pour « after a card ... is revealed ».
#
# ⚠ Mots-pieges : « AT LEAST 1 threat HERE » (crise seulement tant qu'il reste de
# la menace sur cette carte) ; « a card that BELONGS TO the Kree-Skrull War set » (le
# set de la carte : sk136-sk140, Bel-Dann, Raksor, les deux traitrises ; pas
# Army of Skrulls, pas le scenario) ; « REVEALED » (Raksor mis en jeu par Bel-Dann
# n'est pas revele, une carte revelee en boost non plus : son ★ Boost pose la
# menace lui-meme) ; « 2 threat HERE » (sur cette carte, pas le complot principal) ;
# Permanent : aucune capacite de CE set ne la defausse, donc elle reste meme a 0
# menace.


def GetAbilities() -> Sequence['Ability']:

    def menace_presente(effect: 'Effect', ui: List['CardFace']) -> int:
        this = effect.this.CastTo(EncounterSideScheme)
        return 1 if this.threat >= 1 else 0

    def apres_revelation(effect: 'Effect', message: 'Message.AfterCardRevealedEnd') -> None:
        Unused(message)
        this = effect.this.CastTo(EncounterSideScheme)
        this.PlaceThreatOnSchemes([this], 2, effect)

    return [
        AbilityFactory.ThisGainKeyword(
            menace_presente,
            crisis=1,
            change_on_event=OnEvent.Threat("This"),
        ),
        AbilityFactory.AfterPlayerRevealCard(
            AbilityType.ForcedResponse,
            "AnyPlayer",
            CardFinder(check_face_fn=AppartientAuSet),
            apres_revelation,
        ),
    ]
