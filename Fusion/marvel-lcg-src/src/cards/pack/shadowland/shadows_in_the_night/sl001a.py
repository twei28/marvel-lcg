from . import *
from cards.pack.shadowland.campaign import CampaignSetup

# A Barricade of Blades (1A) — MANIGANCE PRINCIPALE, stade 1.
# Contents : Shadows in the Night, Dark Protege and Standard encounter sets. One modular encounter set (Ninja Swarm).
# Setup : Put each The Streets Below environment into play. Set the Dark Protege encounter set aside. Choose 1 random villain from that set and reveal its side A,
#   then shuffle each card linked to that villain into the encounter deck.
#
# Cartes de reference : mts/loki/55033a (Setup : `SetupCards.PutIntoPlay(effect, name=..., card_type=Environment)` et vilain tire au hasard parmi ceux mis de cote :
# `Rand.RandomChoice` + `Reveal(None, effect)`), sm/sinister_six/27101a et mts/loki/21165a (`ChooseSetAsideVillainAtRandom`), fne/art_museum_heist/60121a (`Faces.ShuffleAllTo(..., "EncounterDeck")`).
# ⚠ Mots-pieges :
#  - « each The Streets Below environment » : DEUX cartes du meme nom (la position du vilain sl003 et celle du heros sl004), a trouver par le NOM dans la zone de
#    mise de cote du scenario (leurs deux faces sont UNE carte recto-verso) ;
#  - « Dark Protege encounter set aside » : le scenario met ce set de cote (`set_aside`) ; le tirage ne porte que sur ses VILAINS, les 5 autres restent de cote ;
#  - « linked to that villain » : le texte de la carte nomme TROIS vilains (`VilainsLies`), pas un seul ; les cartes liees aux autres vilains restent de cote ;
#  - « reveal its side A » : la face A du vilain (les vilains sont des cartes recto-verso a retourner, pas des stades separes).


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        # DEUX cartes portent ce nom (sl003 position du vilain, sl004 position du heros) : `SetupCards.PutIntoPlay` n'en met qu'UNE par appel.
        for _ in range(2):
            SetupCards.PutIntoPlay(effect, name='The Streets Below', card_type=Environment)
        # CAMPAGNE (livret FR) : les Sombres Proteges deja utilises ou partageant le nom d'un heros sont retires du tirage (`VilainsTirables`).
        vilains = VilainsTirables(effect)
        if not vilains:
            return
        vilain = Rand.RandomChoice(vilains, effect)
        nom = NomDuVilain(vilain)
        vilain.Reveal(None, effect)
        liees = [x for x in Worlds.GetSetAsideAreaCards(effect) if not Villain.IsType(x) and nom in VilainsLies(x)]
        if liees:
            Faces.ShuffleAllTo(liees, "EncounterDeck", effect)

    return [
        AbilityFactory.WhenCardSetup('This', mise_en_place),
        # Campagne (livret FR) : le niveau est le numero du scenario dans `data/campagnes/shadowland.json`.
        *CampaignSetup(1),
    ]
