from . import *

# The Devourer's Skin — MANIGANCE PRINCIPALE, stade 1, face A (texte de mise en place).
#
# Contents: 3 villain cards: The Hunger Core (I, II and III). 2 main scheme cards (1A/1B and 2A/2B). 1
# environment card: Inside Galactus. 9 Metazombies (villain cards). 32 Metazombie signature cards. 13 cards
# from The Hunger Core set. 10 Hungry Horde cards. 13 Fallen Heroes cards. 5 allies in the Survivor deck.
#
# Setup: Put The Hunger Core (I) into play (Expert: II). Set aside the zombie version of each chosen hero and
# its Trapped Survivor.
# Shuffle the other Metazombies: this is the Horde deck. Put 2 into play.
# Encounter deck: The Hunger Core set, Hungry Horde, Fallen Heroes (without the zombie versions set aside) and
# the Standard set.
# Set aside "Inside Galactus", "The Innards" and the Survivor deck.
#
# Cartes de reference :
#  - « Contents » et le placement du Coeur (villain I ou II selon standard/expert) : AUCUN code, portes par
#    `data/scenarios/the_hunger_core(_expert).json` (champ `villain`), comme TOUS les scenarios du moteur
#    (modele ap005a/ap006a « Contents »).
#  - « Set aside Inside Galactus / The Innards / Survivor deck » : AUCUN code non plus, ce sont les champs
#    `set_aside` (hg006, hg072-076) et `schemes` (hg005a/hg005b, jamais tires avant Deeper Inside) du meme
#    fichier scenario.
#  - « Set aside the zombie version of each chosen hero and its Trapped Survivor » + « Shuffle the other
#    Metazombies: this is the Horde deck » : `commun.RetirerZombiesEtSurvivorsHomonymes` puis
#    `commun.ConstruireLeHordeDeck`, fiche mots-cles/horde-metazombies.md.
#  - « Put 2 into play » : `commun.MettreUnMetazombieEnJeu`, deux fois.
#  - « the villain » (regle multi-mechants, Coeur + Metazombies) : `Villains.SetRule`, modele ap005a, fiche
#    mots-cles/mechants-multiples.md.
#
# ⚠ Mots-pieges :
#  - « Fallen Heroes (without the zombie versions set aside) » : ces cartes sont deja melangees dans le deck
#    de rencontre par la mise en place GENERIQUE du scenario (modular_sets) AVANT que ce Setup ne s'execute ;
#    il faut donc les en retirer explicitement (`SetupCards.SetAsideCards`), pas simplement ne pas les ajouter.
#  - un heros choisi peut n'avoir NI version Metazombie NI version Fallen Heroes (ex. un heros hors de ces 22
#    noms) : les deux fonctions ne font alors rien pour lui, ce qui est le comportement voulu.
#  - Wolverine et Blade sont A LA FOIS des heros jouables officiels ET des noms du Survivor deck : la
#    correspondance se fait par NOM, jamais par trait ou card_id (`commun.NOMS_SURVIVOR`).


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)

        Villains.SetRule(effect, Villains.Rule(the_villain="Active", player_cards="TheVillain"))
        # Le jeton est d'abord pose sur le Coeur (repli si le Horde deck etait vide) ; le PREMIER Metazombie mis en
        # jeu juste apres le reprend (`MettreUnMetazombieEnJeu`), conformement au livret p. 7, etape 7 : « Place
        # the active Metazombie token on the first one in the row. »
        coeur = LeCoeur(effect)
        if coeur is not None:
            Villains.SetActive(coeur, effect)

        noms_exclus = RetirerZombiesEtSurvivorsHomonymes(effect)
        ConstruireLeHordeDeck(effect, noms_exclus)

        joueur = Worlds.GetFirstPlayer(effect)
        MettreUnMetazombieEnJeu(effect, joueur)
        MettreUnMetazombieEnJeu(effect, joueur)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
    ]
