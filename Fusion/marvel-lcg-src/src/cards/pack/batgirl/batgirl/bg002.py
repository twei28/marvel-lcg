from . import *

# * Black Canary — allie (Multiverse : Nightwing bg003 la remplace). « Hero Interrupt: When Black Canary enters play, stun 1 enemy
# for each [mental] resource used to pay for Black Canary's cost. »
# Cartes de reference : `06012` Valkyrie (`message.paid_resources` lu a l'entree en jeu), `01083` (`Faces.GiveStatus(.., "Stunned")`),
# `01011` Spider-Woman (`AfterCardEnterPlay`). Ici la fenetre est une INTERRUPTION : `WhenCardEnterPlay` (meme message, avant).


def GetAbilities() -> Sequence['Ability']:

    def black_canary(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        n = Compter(effect, message.paid_cost, Icone(effect, "B"))
        for _ in range(n):
            cible = ChoisirUnEnnemi(joueur, effect)
            if cible is None:
                break
            Faces.GiveStatus([cible], "Stunned", effect)

    return [
        AbilityFactory.WhenCardEnterPlay(AbilityType.HeroInterrupt, "This", black_canary),
    ]
