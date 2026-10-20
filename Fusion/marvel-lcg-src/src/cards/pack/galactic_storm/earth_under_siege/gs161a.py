from . import *

# Earthfall (1A) — MANIGANCE PRINCIPALE, stade 1.
# Content: Earth Under Siege, Annihilus, Attuma, Destroyer, Doctor Minerva, Mole Man, Veranke and Standard
#   encounter sets. One modular encounter set (Imperial Guard).
# Setup: Set Annihilus, Attuma, Destroyer, Doctor Minerva, Mole Man, and Veranke encounter sets aside.
#   Create the villain deck (see insert). Reveal the top card of the villain deck and shuffle the rest of
#   its encounter set into the encounter deck. Reveal the Enemies at Large side scheme. Place 6 safety
#   counters here.
#
# Cartes de reference :
#  - « Content » : composition du scenario, portee par data/scenarios/gs_earth_under_siege*.json (aucun
#    code) ; « villain: [] » y coupe la mise en place automatique du moteur (un seul mechant, stades A/B) :
#    rien a desactiver (`skip_put_villain_into_play` inutile, modele `sm/sinister_six/27100a.py` qui, lui,
#    pre-remplit `scenario.villain_deck` et doit vraiment le couper).
#  - « Set [6 ensembles] aside » : deja fait par le moteur a la creation de la partie (cle `set_aside` du
#    scenario, `Message.WhenGameBeginSetup.CreateSetAside`), aucun code ici non plus.
#  - « Create the villain deck » : `Villains.SetRule` (brique du 20/10/2026, Galactic Storm p.16, « the
#    leftmost villain » / « player chooses ») + `Villains.BuildVillainDeck` sur les 6 cartes MECHANT mises
#    de cote (`Worlds.GetSetAsideAreaCards(.., CardFinder(card_type=Villain))`).
#  - « Reveal the top card ... shuffle the rest of its encounter set into the encounter deck » :
#    `RevelerProchainMechantEtMelangerLeReste` (earth_under_siege/__init__.py), reutilise par gs161b et
#    gs162a/b.
#  - « Reveal the Enemies at Large side scheme » : `SetupCards.PutIntoPlay(name=...)` (modele Sinister Six
#    « Light at the End », `sm/sinister_six/27100a.py`) ; la carte (gs162a standard / gs162b expert) est
#    elle aussi mise de cote par le scenario, une seule des deux existe selon le fichier charge.
#  - « Place 6 safety counters here » : `Faces.PlaceCountersOn` (modele gs143 Hala, compteur 'hideout'),
#    compteur maison 'safety' ajoute a `CardFace.COUNTER` (card_face.py).
#
# ⚠ Mots-pieges : CardFinder(card_type=Villain) sur la zone de cote ne doit trouver QUE les 6 cartes stade
# (une par mechant, celle de la difficulte en cours : le scenario standard/expert ne met de cote QUE la
# bonne, jamais les deux a la fois) ; le reste de chaque ensemble (gs168/gs169 pour Annihilus, etc.) reste
# cote jusqu'a ce que CE mechant soit revele (desc.set_name = nom du mechant, pas "Earth Under Siege").


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        premier = Worlds.GetFirstPlayer(effect)

        Villains.SetRule(effect, Villains.Rule(the_villain="Leftmost", player_cards="PlayerChooses"))

        candidats = [f.CastTo(Villain) for f in Worlds.GetSetAsideAreaCards(effect, CardFinder(card_type=Villain))]
        Villains.BuildVillainDeck(candidats, effect)
        RevelerProchainMechantEtMelangerLeReste(effect, premier)

        SetupCards.PutIntoPlay(effect, "FirstPlayer", False, name="Enemies at Large", card_type=EncounterSideScheme)

        this = effect.this.CastTo(MainScheme)
        Faces.PlaceCountersOn([this], 6, 'safety', effect)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
    ]
