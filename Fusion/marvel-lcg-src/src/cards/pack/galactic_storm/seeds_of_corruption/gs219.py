from . import *

# Psychic Shackles — COMPLOT ANNEXE (Seeds of Corruption). Menace 3 (fixe), 2 icones de boost.
# Hinder 1[per_hero].
# Players cannot play cards with a printed [mental] resource.
#
# Cartes de reference :
#  - **`iron_patriot/ip035`** « You're in My World » : `AbilityFactory.PlayersCannotPlayCardWhile("AnyPlayer",
#    conditions=[...])` avec `message.check_effect.this` + `FacesCounter.GetPrintedResources([face]).
#    HasColorPrinted(couleur)` = « players cannot play cards of the named resource ».
#  - Hinder : base AUTOMATIQUE (`desc.Hinder = "1*"`, fiche hinder.md).
#
# ⚠ Mots-pieges : « PLAYERS » (tous les joueurs) ; « cannot PLAY » (les depenser comme ressource reste
# permis) ; « with a PRINTED [mental] resource » (icone mentale imprimee ; un joker ne compte pas) ; l'effet
# tombe quand le complot est dejoue.


def GetAbilities() -> Sequence['Ability']:

    def carte_mentale(effect: 'Effect', message: 'Message.CheckEffectCondition') -> bool:
        Unused(effect)
        face = message.check_effect.this
        return face is not None and AUneRessourceMentaleImprimee(face)

    return [
        AbilityFactory.PlayersCannotPlayCardWhile("AnyPlayer", conditions=[carte_mentale]),
    ]
