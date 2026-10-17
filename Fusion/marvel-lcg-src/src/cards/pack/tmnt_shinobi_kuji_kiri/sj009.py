from . import *

# Armageddon (sj009), Kuji-Kiri, complot annexe JOUEUR, unique (Inkwire, TMNT Shinobi).
# Victory 0.
# Forced Response: After Armageddon enters play, deal each player 1 facedown encounter card.
# While Armageddon is in the victory display, each identity gets +1 hand size in hero form.
#
# Mot-cle (fiche lue AVANT le code) : Victory (`victory.md`) : `desc.Victory "0"`, base automatique (la carte va
# a la pile de victoire quand elle est vaincue).
# Cartes de reference : `jj/61020` Run Them to Ground (« Deal each player 1 facedown encounter card » :
# `player.DealEncounterCards(1, effect)` pour chaque joueur, complot annexe joueur a menace par heros « 4* ») ;
# `next_evol/40006` Technovirus Purge (« While X is in the victory display » : `works_in_the_victory_display=True`) ;
# `drs/09026` (« +1 hand size while in hero form » : cible `Hero`, jamais l'alter-ego) ; `deadpool/44024`
# (« each identity gets +N hand size » : `GiveKeywordToInPlayWhenApplyThis(..., hand_size=N)`).
#
# TEXTE CONTRE CODE
#  ⚠ « EACH player » : tous les joueurs (pas seulement vous), 1 carte rencontre FACE CACHEE chacun.
#  ⚠ « After Armageddon ENTERS PLAY » : Reponse Obligatoire a l'entree en jeu (pas a la defaite).
#  ⚠ « While in the VICTORY DISPLAY » : l'effet de taille de main ne vaut QUE dans la pile de victoire, pas
#    tant que le complot est en jeu ; « EACH identity » : tous les joueurs ; « in HERO FORM » : la forme
#    alter-ego ne gagne rien.
#  ⚠ Menace de depart « 5* » : 5 par heros (icone joueur imprimee a cote du 5).


def GetAbilities() -> Sequence['Ability']:

    def armageddon(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this, message)

        for joueur in Worlds.GetPlayers(effect):
            joueur.DealEncounterCards(1, effect)

    return [
        AbilityFactory.CanPlayThisSchemeCard(),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            armageddon,
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Hero,
            works_in_the_victory_display=True,
            hand_size=1,
        ),
    ]
