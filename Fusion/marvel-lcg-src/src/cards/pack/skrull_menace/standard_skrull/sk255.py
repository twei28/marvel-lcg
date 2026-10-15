from . import *

# Cursed by the Past — TRAITRISE (Standard Skrull). 2 icones de boost.
# When Revealed: If your nemesis minion is in play, it activates against you. Otherwise, find your nemesis
#   minion and reveal it. If your nemesis side scheme is in play, place threat on it equal to its starting
#   threat value. Otherwise, find your nemesis side scheme and reveal it. Shuffle your remaining set-aside
#   nemesis set into the encounter deck.
#
# Cartes de reference :
#  - **`fne 60176`** Unrelenting Hate : « nemesis minion en jeu -> il active contre vous, sinon trouvez-le et
#    revelez-le » (`DoActivate` + `Find.FindAndReveal(finder=CardFinder(card_type=Minion, is_nemesis=joueur))`).
#  - **`fne 60173`** Kingpin's Influence : meme logique pour le complot annexe nemesis
#    (`CardFinder(card_type=EncounterSideScheme, is_nemesis=joueur)`, `Find.FindAndReveal`).
#  - **`01190`** Shadow of the Past (core, Standard) / **`aoa 45075b`** : « Shuffle the rest of your set-aside
#    nemesis set into the encounter deck » (`Faces.ShuffleAllTo(rest, encounter_deck, effect, ui_group=False)`).
#
# ⚠ Mots-pieges : « YOUR nemesis minion / side scheme » (celui du joueur qui revele) ; « is in play » PUIS
# « otherwise find » : un seul des deux ; « threat equal to its STARTING threat value » (`start_threat`, deja
# multiplie par le nombre de joueurs) et seulement SI le complot est deja en jeu (sinon il est revele, avec sa menace
# de depart, sans ajout) ; « remaining set-aside nemesis set » : ce qui reste de la pile apres les deux cartes
# trouvees ; les trois temps (sbire, complot, melange) se font TOUJOURS, meme si le sbire etait deja en jeu.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        finder_sbire = CardFinder(card_type=Minion, is_nemesis=joueur)
        finder_complot = CardFinder(card_type=EncounterSideScheme, is_nemesis=joueur)

        sbire = Worlds.FindCardOnField(effect, finder=finder_sbire)
        if sbire is not None:
            sbire.CastTo(Minion).DoActivate(joueur, effect)
        else:
            Find.FindAndReveal(effect, joueur, finder=finder_sbire)

        complot = Worlds.FindCardOnField(effect, finder=finder_complot)
        if complot is not None:
            this.PlaceThreatOnSchemes([complot], complot.CastTo(EncounterSideScheme).start_threat, effect)
        else:
            Find.FindAndReveal(effect, joueur, finder=finder_complot)

        reste = [f for f in joueur.set_aside_nemesis_sets.Get() if f.card.area == joueur.set_aside_nemesis_sets]
        if reste:
            Faces.ShuffleAllTo(reste, Worlds.GetEncounterDeck(effect), effect, ui_group=False)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
