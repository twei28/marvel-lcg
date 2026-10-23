from . import *

# Into the Labyrinth (1A) — MANIGANCE PRINCIPALE, stade 1.
# Contents : Shifting Corridors (A). Shadow Labyrinth, Dark Protege, Deadly Contraptions, and Standard encounter sets. One modular encounter set (Ninja Swarm).
# Setup : Create the trap deck (see rulebook, p. 12). Set the Dark Protege encounter set aside. Choose 1 random villain from that set, then shuffle each card linked to that
#   villain into the encounter deck (keep the chosen villain set aside).
#
# Cartes de reference : shadowland/shadows_in_the_night/sl001a (meme tirage : `Rand.RandomChoice` parmi les vilains mis de cote + `VilainsLies` + `Faces.ShuffleAllTo`, mais
# ICI le vilain RESTE de cote), hunting_season/trap/__init__ (`CreerPaquetsPiege` : scenario deck + defausse liee), skrull_empire (`CreerPaquetPlanete`).
# ⚠ Mots-pieges :
#  - « Create the trap deck (see rulebook, p. 12) » : livret introuvable, deduit des 8 cartes TRAP! (voir DECISIONS-b.md) : les 8 cartes TRAP! (Whisper in the Dark et les 7
#    pieges de Deadly Contraptions) mises de cote, melangees ; defausse a part ;
#  - « keep the chosen villain set aside » : le vilain tire n'est PAS revele, on retient SON IDENTIFIANT (`MemoriserVilainChoisi`) pour sl040 et sl039a ;
#  - « linked to that villain » : le texte de la carte nomme TROIS vilains (`VilainsLies`) ; seules les cartes liees au vilain tire entrent dans le deck de rencontre.


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        CreerPaquetPiege(effect)
        vilains = [x for x in Worlds.GetSetAsideAreaCards(effect) if Villain.IsType(x)]
        if not vilains:
            return
        vilain = Rand.RandomChoice(vilains, effect)
        MemoriserVilainChoisi(effect, vilain)
        nom = NomDuVilain(vilain)
        liees = [x for x in Worlds.GetSetAsideAreaCards(effect) if not Villain.IsType(x) and nom in VilainsLies(x)]
        if liees:
            Faces.ShuffleAllTo(liees, "EncounterDeck", effect)

    return [
        AbilityFactory.WhenCardSetup('This', mise_en_place),
    ]
