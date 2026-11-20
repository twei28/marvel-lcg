from . import *
from cards.pack.hellfire_hunt.campaign import CampaignSetup

# Diplomatic Sabotage (1A). « Setup : Remove Cassandra Nova minion from the game. Put the Cassandra Domination environment into play. In expert
# mode, advance to stage 2A. » + mise en place de CAMPAGNE du scenario 5 (livret p.16) : `CampaignSetup(5)` (cards.pack.hellfire_hunt.campaign :
# Tactical Help et Enemy Of Enemy melanges au deck de rencontre, Rally the Survivors revelee, pas de Xavier's Institute, deck Recruited Mutants,
# Emma Frost dedans si sa Redemption n'est pas cochee, PV restants et pion Acceleration en expert).
# Cartes de reference : hf104a (retrait des sbires homonymes), `Faces.RemoveAllFromGame`, gs / sm (environnement mis de cote puis mis en jeu),
# hg (`Worlds.IsExpert`, `MainScheme.Advance`).
# ⚠ « In expert mode, advance to stage 2A » est porte par hf604b (`AfterGameSetup`) : au Setup de la face A le moteur n'a pas encore fait
# avancer le complot a la face B (`World` etape 12 : `scheme.Setup(False)` PUIS `scheme.Advance(None)`), un `Advance("2A")` ici ne ferait que
# retourner la carte.
# ⚠ Mot-piege : « minion named Cassandra Nova » : le VILAIN porte le meme nom ; le filtre est `Minion.IsType`. L'environnement est « mis de
# cote » par le scenario (data/scenarios `set_aside`), donc cherche dans la zone de cote.


def GetAbilities() -> Sequence['Ability']:
    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        sbires = [f for f in Worlds.GetEncounterDeckCards(effect) if Minion.IsType(f) and f.IsName(NOM_CN)]
        if sbires:
            Faces.RemoveAllFromGame(sbires, effect)
        for face in list(effect.world.aside_deck.Get(True)):
            if getattr(face.paper, "card_id", None) == ID_DOMINATION:
                face.PutIntoPlay(Worlds.GetFirstPlayer(effect), effect)
                break

    return [AbilityFactory.WhenCardSetup("This", mise_en_place), *CampaignSetup(5)]
