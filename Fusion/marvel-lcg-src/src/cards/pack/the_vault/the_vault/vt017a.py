from . import *

# The Vault Breakout (1A) — MANIGANCE PRINCIPALE, stade 1.
# Contents: All villains (I) (stages (II) instead for expert mode). The Vault and Standard encounter sets. One modular
#   encounter set (Sinister Syndicate).
# Setup: Create the Villain deck (see insert). Put The Vault environment into play. Then, place the top 4 villain cards and
#   each player's nemesis (✦) minion beneath it facedown. Set the Inspection of the Vault obligation aside, out of play.
#
# Cartes de reference :
#  - « Contents » : data/scenarios/the_vault*.json (aucun code, modele gs161a Earthfall).
#  - « Create the Villain deck » : `Villains.SetRule` + `Villains.BuildVillainDeck` (brique du 20/10/2026, modele gs161a) ; la
#    regle ajoutee ici (`the_villain="LowestActivationOrder"`, `activation_order=True`) rend « the villain » = le plus petit
#    Activation Order (livret p.1) et distribue les activations par ordre (livret p.2, `Enemies.ActivationVillainsParOrdre`).
#  - « Put The Vault environment into play » : `SetupCards.PutIntoPlay(name=..., card_type=Environment)` (modele gs161a
#    Enemies at Large) ; « place ... beneath it facedown » : `CardFace.TuckCardUnderHere` (fiche mots-cles/tuck.md).
#  - « Set the Inspection ... aside » : déjà de côté (cle `set_aside` du scenario) : rien a coder.
#
# ⚠ Mots-pieges : « the top 4 villain cards » = les 4 du DESSUS du deck de vilains (les 4 restants servent a la partie) ;
# « each player's nemesis minion » = le sbire MARQUE nemesis du set de chaque joueur (`is_nemesis=joueur`), pas tout le set ;
# un joueur sans sbire nemesis (set emprunte sans sbire marque) ne glisse rien.


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        Villains.SetRule(effect, Villains.Rule(the_villain="LowestActivationOrder", player_cards="PlayerChooses",
                                               activation_order=True))

        candidats = [f.CastTo(Villain) for f in Worlds.GetSetAsideAreaCards(effect, CardFinder(card_type=Villain))]
        Villains.BuildVillainDeck(candidats, effect)

        SetupCards.PutIntoPlay(effect, "FirstPlayer", False, name=NOM_VAULT, card_type=Environment)

        dessous = list(Villains.TopOfVillainDeck(effect, 4))
        for joueur in Worlds.GetPlayers(effect):
            dessous += Worlds.GetSetAsideAreaCards(effect, CardFinder(card_type=Minion, is_nemesis=joueur))
        PoserSousLeVault(dessous, effect)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
    ]
