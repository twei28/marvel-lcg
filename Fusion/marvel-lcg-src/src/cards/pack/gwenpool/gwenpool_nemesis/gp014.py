from . import *

# "Future Me Scares Me" — custom « ekAugust » (traîtrise némésis de Gwenpool)
# Incite 0 (1 en multijoueur) / Incite 1 (2 en expert).
# CORRECTIF (31/08/2026) : le module disait « le moteur ne porte qu'une valeur
# d'Incite » et figeait le tout a 1. C'est faux : `AbilityFactory.ThisGainIncite`
# prend une fonction de test (modele jj021, du MEME auteur fan-made, pour la meme
# forme de texte) et `IfExpertModeThisGainKeyword(incite=1)` est une fabrique
# DEDIEE au mode expert.
# Les deux lignes imprimees sont DEUX instances du mot-cle qui s'ADDITIONNENT
# (verifie sur le visuel, assets/pics/gp014.png : rien dans l'en-tete, les deux
# lignes seules dans le pave de texte). Donc : solo standard 0 + 1 = 1 (la valeur
# du `desc`, qui reste juste), multijoueur 1 + 1 = 2, expert 0 + 2 = 2,
# multijoueur expert 1 + 2 = 3. Seuls les deux bonus conditionnels manquaient.
# When Revealed: If Evil Gwenpool is in play, add 2 threat to Rules of the
# Universe and shuffle this card into the encounter deck.

def GetAbilities() -> Sequence['Ability']:

    def future_me_scares_me(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        evil = Worlds.FindCardOnField(effect, name="Evil Gwenpool", card_type=Minion)
        if not evil:
            return

        rules = Worlds.FindCardOnField(effect, name="Rules of the Universe")
        if rules:
            this.PlaceThreatOnSchemes([rules], 2, effect)
        Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    return [
        # « Incite 0 (incite 1 instead, if this is a multiplayer game). »
        *AbilityFactory.ThisGainIncite(
            lambda effect: Worlds.GetPlayerNum(effect) > 1,
            incite=1,
        ),

        # « Incite 1 (incite 2 instead, if this is an expert mode game). » La
        # valeur de base 1 est imprimee dans le `desc` ; seul le +1 est ici.
        AbilityFactory.IfExpertModeThisGainKeyword(incite=1),

        AbilityFactory.WhenThisRevealed(
            None,
            future_me_scares_me
        ),
    ]
