from . import *

# Anti-Dogma — TRAITRISE. 1 icone de boost + une etoile.
#
# When Revealed: Gorr the God Butcher schemes. Place 2 threat on the main
#   scheme or discard the top 2 cards of your deck.
# [star] Boost: Place 2 threat on the main scheme or discard the top 2 cards
#   of your deck.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - `Boost` etoile (mots-cles/boost.md) : `WhenCardBecomeBoost`, sans quoi le
#   moteur ne voit aucune etoile. Le texte seul ne suffit pas.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « <Vilain> schemes » : 02029 (Mutagen Formula), `villain.DoSchemes(player,
#   effect)`.
# - Choix entre deux effets impose au joueur : `player.ChooseAbilities` avec
#   deux `ForChoiceAbility` (modele al007, qui emploie la variante FACULTATIVE
#   `MayChooseOneAbility` ; ici le choix est obligatoire, on prend donc
#   `ChooseAbilities` sans option d'annulation).
# - « Place N threat on the main scheme » : `this.PlaceThreatOnSchemes(
#   "MainScheme", 2, effect)`, la brique standard.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « Gorr the God Butcher SCHEMES » -> une vraie manigance du vilain, avec ses
#   cartes de boost, PUIS le choix : deux effets qui s'ajoutent, pas un
#   remplacement.
# « ... OR ... » -> choix du JOUEUR qui revele, pas du vilain ; les deux
#   branches sont toujours possibles (poser 2 menaces l'est toujours ; un deck
#   vide ne bloque pas la seconde, il n'y a simplement rien a defausser).
# « the top 2 cards of YOUR deck » -> le deck du joueur qui revele.
# Le ★ Boost repete EXACTEMENT le choix, sans la manigance.


def GetAbilities() -> Sequence['Ability']:

    def choix_menace_ou_defausse(effect: 'Effect', joueur: 'Player') -> None:
        this = effect.this

        def poser_menace(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            this.PlaceThreatOnSchemes("MainScheme", 2, effect)

        def defausser(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            joueur.DiscardDeckTopCards(2, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Place 2 threat on the main scheme", poser_menace),
            AbilityFactory.ForChoiceAbility(
                "Discard the top 2 cards of your deck", defausser),
        )

    def anti_dogme(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        vilain = TrouverGorr(effect)
        if vilain and joueur:
            vilain.DoSchemes(joueur, effect)
        if joueur:
            choix_menace_ou_defausse(effect, joueur)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur:
            choix_menace_ou_defausse(effect, joueur)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            anti_dogme,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
