from . import *
# Intimidate — EVENEMENT cout 0 [mental]. SKILL. Hero Interrupt : when a deterrence card is revealed or flipped as a boost card, cancel its surge
# effect and its additional boost card effect. You may pay 1 resource of any type to shuffle this card back into your deck.
# « Cancel » = DEUX drapeaux poses sur la carte de dissuasion (`sans_surge`, `sans_boost_sup`) que ses propres operations lisent
# (SurgeDeLaDissuasion, BoostSupplementaireAnnule) : le reste de la carte (degats, menace...) se joue normalement.
# Reference : sn004 (interruption sur `WhenBoostCardWouldTurnedFaceUp`), bg007 (`WhenPlayerRevealCard`).
def GetAbilities() -> Sequence['Ability']:
    def intimider(effect: 'Effect', message: 'Message2') -> None:
        carte = message.trigger
        joueur = JoueurDeCetteCarte(effect)
        etat = EtatBm(carte)
        etat["sans_surge"], etat["sans_boost_sup"] = True, True
        if joueur is not None and joueur.AskSpendResources(Cost("1"), effect):
            Faces.ShuffleAllTo([effect.this], joueur.player_deck, effect)
    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt, "You", None, None, intimider,
            conditions=[lambda effect, message: EstDissuasion(message.trigger)],
        ).SetPlay(),
        AbilityFactory.WhenBoostCardWouldTurnedFaceUp(
            AbilityType.HeroInterrupt, intimider,
            conditions=[lambda effect, message: EstDissuasion(message.trigger)],
        ).SetPlay(),
    ]
