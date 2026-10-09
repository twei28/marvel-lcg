from . import *

# hs152 The Red Vulture
# When Revealed : cherchez Vulture (James Natale) dans le deck et la defausse de rencontre, mettez-le en jeu engage
# avec l'identite ayant le moins de PV restants.

def GetAbilities() -> Sequence['Ability']:

    def chercher(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueurs = Worlds.GetPlayers(effect) if hasattr(Worlds, "GetPlayers") else [message.GetToPlayer()]
        cible = min(joueurs, key=lambda j: j.GetIdentity().health)
        Find.FindAndPutIntoPlay(
            effect, cible,
            finder=CardFinder(card_type=Minion, check_face_fn=lambda f: f.IsCardId("hs151") and not f.IsInPlay()),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, chercher),
    ]
