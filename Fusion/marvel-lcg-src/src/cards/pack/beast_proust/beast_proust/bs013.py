from . import *

# Overworked : OBLIGATION, boost 3. A donner au joueur de Hank McCoy.
# Discard all cards tucked under Beast's Lab, then discard Overworked. If no TECH upgrade is discarded this way, deal yourself 1 facedown encounter card, then shuffle Overworked into the encounter deck.
#
# CARTES DE REFERENCE
#  - `dy013` Seizure / `mt011` : `WhenThisObligationGiveToYou(op)` ; une obligation reste en jeu tant qu'on ne la defausse pas : `Faces.DiscardAll([this], effect)` explicite.
#  - `mf017` / `sl029` : `Faces.ShuffleAllTo([this], "EncounterDeck", effect)` ; `ar012` / `16118` : `joueur.DealEncounterCards(1, effect)`.
#
# TEXTE CONTRE CODE
#  « Discard ALL cards tucked under » : toutes, sans choix. « THEN discard Overworked » : la carte part a la defausse RENCONTRE. « If NO TECH UPGRADE is discarded THIS WAY » : on compte les ameliorations TECH
#    defaussees depuis le Lab (une amelioration TECH ailleurs, en jeu ou en main, ne compte pas ; une carte glissee non TECH non plus). « Deal yourself 1 FACEDOWN encounter card, THEN shuffle Overworked into the
#    encounter deck » : la carte distribuee d'abord, puis Overworked (retiree de la defausse) est melangee dans le deck rencontre : elle ne peut donc pas etre la carte distribuee. Sans Lab en jeu : rien de
#    defausse, donc la seconde moitie s'applique.
#  Chiffres : boost 3, 1 carte distribuee.


def GetAbilities() -> Sequence['Ability']:

    def surexploite(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()

        glissees = GlisseesSousLab(joueur)
        a_defausser = list(glissees)
        tech = [f for f in a_defausser if Upgrade.IsType(f) and f.HasTrait("TECH")]
        if a_defausser:
            Faces.DiscardAll(a_defausser, effect)
        Faces.DiscardAll([this], effect)
        if not tech:
            joueur.DealEncounterCards(1, effect)
            Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            surexploite,
        ),
    ]
