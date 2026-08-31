from . import *

# Ruler of Manhattan — complot annexe nemesis. Menace 5. Boost 3. Hazard 1.
# When Revealed: Discard cards from the top of the encounter deck until a
#   side scheme is discarded. Reveal that side scheme. Remove threat from
#   here equal to the number of boost icons on that card.
# (Green Goblin's nemesis side scheme.)
#
# Cartes de reference :
#  - squelette When Revealed de complot annexe : an011 Hel's Retribution
#    (`WhenThisRevealed`) ;
#  - defausse du deck rencontre : 15004 Hex Bolt,
#    `Worlds.DiscardEncounterCards(1, effect)` en boucle ;
#  - revelation d'une carte DEPUIS la defausse : an015 Back from Hel,
#    `face.Reveal(None, effect)` ;
#  - comptage d'icones de boost : 15004 encore,
#    `FacesCounter.CountTotalBoostIcons([face])`.
#
# ⚠ Texte imprime avec deux coquilles (« is discard », « eqial »), corrigees
# a la saisie — le sens est sans ambiguite.
# ⚠ « Remove threat from HERE » : la menace part de CE complot-ci, pas du
# complot principal. Et « on THAT card » : les icones comptees sont celles du
# complot annexe defausse puis revele, boosts etoiles non comptes (la fonction
# du moteur compte les icones imprimees).
# ⚠ Garde-fou : si le deck rencontre ne contient AUCUN complot annexe, la
# boucle s'arrete apres un cycle complet (deck + defausse) au lieu de tourner
# sans fin — meme prudence que le correctif Underling du 20/08.

def GetAbilities() -> Sequence['Ability']:

    def ruler(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # ⚠ la classe moteur est `SchemeSide2` (scheme_side.py), il n'existe
        # AUCUN nom `SideScheme` dans l'espace `cards.pack` — an011 et 50074
        # portent le meme appel latent jamais execute, a corriger un jour.
        this = effect.this.CastTo(SchemeSide2)

        deck = Worlds.GetEncounterDeck(effect)
        defausse = Worlds.GetEncounterDiscardPile(effect)
        limite = deck.GetSize() + defausse.GetSize()

        trouve = None
        while limite > 0 and trouve is None:
            limite -= 1
            faces = Worlds.DiscardEncounterCards(1, effect)
            if not faces:
                break
            if SchemeSide2.IsType(faces[0]):
                trouve = faces[0]

        if trouve is None:
            return
        trouve.Reveal(None, effect)
        icones = FacesCounter.CountTotalBoostIcons([trouve])
        if icones > 0:
            this.RemoveThreatFromSchemes([this], icones, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            ruler,
        ),
    ]
