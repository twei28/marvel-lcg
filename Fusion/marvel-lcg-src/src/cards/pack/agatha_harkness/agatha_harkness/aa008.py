from . import *

# * Agatha All Along — manigance-joueur signature. Cout 0. Menace 13.
# Victory 0.
# Response: After Agatha Harkness takes any amount of damage from an attack,
#   remove an equal amount of threat from here.
# While Agatha All Along is in the victory display, Agatha Harkness gets +1
#   to each of her basic powers and +3 hit points.
#
# Cartes de reference (RECETTES) :
#  - 40006 * Technovirus Purge (pack officiel Cable), jumelle structurelle :
#    manigance-joueur Victory 0 dont le bonus vit AU TABLEAU DES VICTOIRES
#    (`GiveKeywordToInPlayWhenApplyThis(..., works_in_the_victory_display=
#    True)` — c'est la carte citee en commentaire du parametre) ;
#  - la Response : aa001a (meme declencheur `AfterUnitTookDamage`,
#    `is_from_attack=True`, montant = `took_damage`) + `RemoveThreatFromSchemes`
#    sur ELLE-MEME (ho014).
#
# ⚠ Version 13 menaces (zip) retenue par l'utilisateur le 31/08/2026 — une
# version a 10 circule sur le Discord de l'auteur.
# ⚠ Ciblage par card_ids (aa001a) et PAS par nom : « Agatha Harkness » est
# aussi 15007, soutien signature du pack officiel Scarlet Witch.

def GetAbilities() -> Sequence['Ability']:

    def absorber(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(PlayerSideScheme)

        n = message.took_damage
        if n > 0:
            this.RemoveThreatFromSchemes([this], n, effect)

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.Response,
            "You",
            absorber,
            is_from_attack=True,
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_ids=["aa001a"]),
            works_in_the_victory_display=True,
            thwart=1,
            attack=1,
            defense=1,
            health=3,
        ),
    ]
