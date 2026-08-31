from . import *

# Hel's Retribution — complot annexe. Boost 3. Hazard 1. Menace 2[per_hero].
# When Revealed: The active player discards cards from their deck equal to
#   ASGARD cards in play.
# (Hazard Icon: Deal +1 encounter card during the villain phase.)
#
# Carte de reference : 42025 * Harpoon (pack angel) pour
# `player.DiscardDeckTopCards(...)` depuis un When Revealed.
#
# ⚠ L'ICONE A ETE IDENTIFIEE PAR COMPARAISON D'IMAGE, pas a vue (lecon
# Lockjaw) : « + » sur une CARTE inclinee = hazard (01107), a ne pas confondre
# avec la MAISON soulignee de l'acceleration (01109). Meme icone que vp012.
# Elle est lue dans `desc`, aucun module a ecrire pour elle.
#
# ⚠ « ASGARD cards IN PLAY », pas « que tu controles » : on compte sur tout le
# plateau. Les sbires nemesis Hela (an012) et Disir (an014) portent eux-memes
# le trait ASGARD et aggravent donc la carte — c'est voulu par l'auteur.

def GetAbilities() -> Sequence['Ability']:

    def hels_retribution(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # CORRECTIF 31/08/2026 : `SideScheme` n'existe pas dans l'espace
        # cards.pack (NameError constate sur le meme appel dans ho014) — la
        # classe moteur est `SchemeSide2`. Le When Revealed plantait donc a
        # CHAQUE revelation en partie reelle, et aucun cas ne le couvrait.
        this = effect.this.CastTo(SchemeSide2)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur is None:
            return
        nombre = len(Worlds.FindCardsOnField(effect, trait="ASGARD"))
        if nombre > 0:
            joueur.DiscardDeckTopCards(nombre, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            hels_retribution,
        ),
    ]
