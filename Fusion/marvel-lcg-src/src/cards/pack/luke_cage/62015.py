from . import *

# Take a Stand
# TACTIC.
# Hero Response: After your hero defends, each ally you control gets +1 THW and
#   +1 ATK until the end of the player phase.


def GetAbilities() -> Sequence['Ability']:
    def take_a_stand(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        player = effect.GetInitiator()
        for ally in player.GetControlCardsByType(ally=True):
            # CORRECTIF (29/08/2026) : le bonus etait PERMANENT.
            # `GainAttack` / `GainThwart` accordent le gain sans echeance ; le
            # texte dit « UNTIL THE END OF THE PLAYER PHASE ». Les allies
            # gardaient donc +1/+1 pour le reste de la partie, et le bonus
            # s'empilait a chaque defense. Modele officiel : Wakandan Training
            # (51024), meme formulation, meme appel.
            # CORRECTIF (10/10/2026) : echeance « fin de la phase des JOUEURS ».
            # Sans `end_phase`, le bonus tombait a la fin de la phase du mechant,
            # celle ou l'on defend : il ne servait jamais.
            ally.GainUntilPhaseEnd(effect, attack=1, thwart=1, end_phase="Player")

    return [
        # CORRECTIF (29/08/2026) : `.SetPlay()` manquait.
        # Take a Stand est un EVENEMENT, il se joue de la main en reaction.
        # Sans capacite de jeu, `CardFactory.CreateFace` (factory.py:120) exige
        # exactement UNE capacite `Play` sur un evenement et levait
        # `AssertionError: face.paper.card_id='62015'` : le deck luke_cage ne
        # montait pas. Et la carte n'aurait de toute facon pas ete jouable.
        AbilityFactory.AfterUnitDefendEnd(
            AbilityType.HeroResponse,
            "YourHero",
            take_a_stand,
        ).SetPlay(),
    ]
