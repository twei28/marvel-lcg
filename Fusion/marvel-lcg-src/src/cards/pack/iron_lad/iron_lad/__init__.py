from cards.pack import *

# ===========================================================================
# Pack IRON LAD — contenu custom de CptScorp (Marvel Champions Custom
# Project, Cycle 2), reproduit a l'identique.
#
# Iron Lad (Nathaniel Richards, alias Kang enfant venu du futur) est un heros
# tourne autour de la trait TECH : ses cartes signature comptent, deplacent
# et exploitent les cartes TECH qu'il controle (Energy Overflow, Ion
# Amplifiers, Inventive Genius), et manipulent agressivement son propre deck
# et sa defausse (Ion Blast, Seeking Solutions, Stature, Hack).
#
# REGLE SPECIALE IMPRIMEE SUR L'INSERT DE REGLES (pas sur une carte) :
# « When your deck empties and you have to reshuffle, there is an additional
# penalty. Not only do you have to deal yourself an encounter card, like all
# the rest of the heroes, you also have to find and reveal your Nemesis
# Minion. » Cablee dans Setup (voir SetupReshuffleNemesis ci-dessous) : le
# moteur pose deja process_after_shuffle par joueur (player.py:71-73,
# `self.player_deck.BindDiscardPile(self.discard_pile, process_after_shuffle)`),
# jamais surcharge par un heros avant Iron Lad. Aucun helper du moteur ne
# combine "chercher une carte rencontre par nom" et "la faire suivre le
# pipeline de revelation normal (When Revealed inclus)" : le rapprochement
# DealEncounterCard (mise en file d'attente, player_action.py:28) + le
# passage naturel par RevealEncounterCards() est donc fait ici a la main.
# A VERIFIER EN PARTIE REELLE (aucun precedent dans le depot) : la file
# d'attente `dealt_encounter_cards` revele bien LES DEUX cartes (celle du
# reshuffle standard + Kang) dans l'ordre ou elles y sont deposees.
# ===========================================================================

NOM_STATURE = "Stature"
NOM_KANG = "Kang the Conqueror"


def CartesTechControlees(player: 'Player') -> List['CardFace']:
    """Les cartes TECH que le joueur controle (supports + upgrades en jeu),
    lui-meme compris s'il porte le trait. Modele : Iron Man (core/iron_man/
    01029a.py), `player.GetControlCardsByType(CardFinder(trait="TECH"),
    upgrade=True)`, etendu ici aux supports (Vision AI, il009, est TECH)."""
    faces = player.GetControlCardsByType(CardFinder(trait="TECH"), upgrade=True, support=True)
    return [f for f in faces if f.HasTrait("TECH")]


def UpgradesIronLadEnJeu(effect: 'Effect') -> List['CardFace']:
    """Les upgrades du pack Iron Lad (set_name == "Iron Lad") en jeu, tous
    joueurs confondus -- pas un filtre par trait TECH : c'est bien la marque
    du pack qui definit une "carte Iron Lad", comme Early Start et Kang le
    demandent tous les deux."""
    return Worlds.FindCardsOnField(effect, card_type=Upgrade, check_face_fn=lambda f: f.paper.set_name == "Iron Lad")


def StatureEnJeu(player: 'Player') -> 'CardFace|None':
    """L'alliee Stature (il002) en jeu sous le controle de ce joueur, ou
    None. Sert de condition de substitution pour Sudden Plan Change (voir ce
    module : Stature n'est pas une identite heros separee dans ce moteur)."""
    for face in player.allies.Get():
        if face.IsName(NOM_STATURE):
            return face
    return None


def SetupReshuffleNemesis() -> 'Ability':
    """Surcharge process_after_shuffle : en plus du tirage d'encontre
    standard (deja fait par le moteur pour tout heros), cherche et revele
    aussi Kang the Conqueror. Modele de la recherche : Search.EncounterCard
    (game/operate/search.py), meme mecanisme que
    hood/ransacked_armory/__init__.py (SearchEncounterDeckForMinionAndAttachTo).
    Le tirage standard ET Kang sont mis en file via DealEncounterCard avant
    que RevealEncounterCards() ne les revele l'un apres l'autre (meme
    pipeline que le tirage normal, When Revealed inclus)."""

    def setup(effect: 'Effect', message: 'Message.WhenGameBeginSetup') -> None:
        this = effect.this.CastTo(AlterEgo)
        player = this.GetControlByPlayer()

        def process_after_shuffle_avec_kang(deck: 'Deck', by_effect: 'Effect') -> None:
            from game.effect.rule import GameRule
            eff = GameRule(player.GetIdentity())
            player.DealEncounterCards(1, eff)
            kang = Search.EncounterCard(
                eff, player,
                include_discard_pile=True,
                include_set_aside=True,
                name=NOM_KANG,
                card_type=Minion,
                may=True,
            )
            if kang:
                player.DealEncounterCard(kang, eff)

        player.player_deck.BindDiscardPile(player.discard_pile, process_after_shuffle_avec_kang)

    return AbilityFactory.WhenGameBeginSetup(setup)
