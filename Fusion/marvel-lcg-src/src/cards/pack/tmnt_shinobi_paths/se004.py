from . import *

# Shihan — PATH (la Voie du Shihan), classe Taijutsu (Inkwire, TMNT Shinobi). TAIJUTSU.
# Permanent. You get -1 hand size.
# Recenter — Hero Interrupt: When the player phase ends, discard the top 2 cards of your deck -> return 1
#   Taijutsu card from your discard pile to your hand.
#
# Mots-cles (fiches lues AVANT le code) : Permanent (permanent.md) ; Shinobi / Path (shinobi.md).
#
# Cartes de reference :
#  - « -1 hand size » : `sentinel/st005b` ;
#  - « When the player phase ends » : `skrull_menace/paibok/sk145b` (`WhenPlayerPhaseEnd`, message general
#    `Message.WhenPhaseEnd("Player")`) ;
#  - « discard the top N cards of your deck -> » en cout : `rainy/rescue_rainy/90122`
#    (`CostFunc.DiscardDeckTopCards("YourDeck", n)`) ;
#  - retour d'une carte de la defausse en main : `Faces.AddToHand`.
#
# TEXTE CONTRE CODE
#  ⚠ « When the PLAYER phase ends » : `WhenPhaseEnd("Player")`, envoye par `world.py` APRES
#    `PlayersEndPhase` (defausse a la taille de main, PIOCHE jusqu'a la taille de main, redressement) et AVANT la
#    phase du mechant : c'est exactement la precision du livret (FAQ p.8 « after you draw your new hand » ;
#    dos : « AFTER you draw your hand and BEFORE the villain phase starts »).
#  ⚠ « discard the top 2 cards of YOUR deck -> return ... » : le « -> » est un COUT, paye d'abord ; les deux
#    cartes defaussees peuvent etre la carte Taijutsu rendue : le choix se fait donc APRES le cout (dans
#    l'operation, pas par un `SetTarget` pose avant le cout).
#  ⚠ « 1 TAIJUTSU card » (Q-S2, REPONSE de l'utilisateur 17/10/2026 : « Taijutsu + Dual Kuji-Kiri/Ninjutsu ») :
#    une carte portant la classe Taijutsu (les Dual Taijutsu en sont) OU la Dual Kuji-Kiri/Ninjutsu (sc007, sc008) ;
#    le texte imprime reste « 1 Taijutsu card ». « from your discard pile » : sa propre defausse. « return ... to your HAND ».
#  ⚠ « Hero Interrupt » : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def recenter(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this.CastTo(Path)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        # Q-S2 (reponse du 17/10/2026) : « Taijutsu + Dual Kuji-Kiri/Ninjutsu » : toute carte de classe Taijutsu
        # (Dual Taijutsu comprises) OU la Dual Kuji-Kiri/Ninjutsu (sc007 / sc008), qui n'est pas Taijutsu.
        candidats = [f for f in joueur.discard_pile.Get()
                     if EstShinobi(f, "Taijutsu") or (EstShinobi(f, "Kuji-Kiri") and EstShinobi(f, "Ninjutsu"))]
        if not candidats:
            return
        if len(candidats) == 1:
            choisie = candidats
        else:
            choisie = joueur.AskChooseFaces(candidats, (1, 1), effect, prompt="Return 1 Taijutsu card to your hand")
        if choisie:
            Faces.AddToHand(list(choisie), joueur, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("You", hand_size=-1),
        AbilityFactory.WhenPlayerPhaseEnd(
            AbilityType.HeroInterrupt,
            recenter,
        ).SetCostFunc(CostFunc.DiscardDeckTopCards("YourDeck", 2)),
    ]
