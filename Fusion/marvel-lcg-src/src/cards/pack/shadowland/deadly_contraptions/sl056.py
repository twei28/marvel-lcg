from . import *

# Tripwire — TRAITRISE. TRAP! Boost 2.
# When Revealed : Choose :
#  • Avoid — Discard an ATTACK event from your hand.
#  • Disarm — Discard a support you control, then remove 3 threat from a scheme.
#  • Trip — Discard cards from the top of the encounter deck until a side scheme is discarded, then reveal it.
#
# Cartes de reference : sl050 (gabarit), sl053 (« remove N threat »), punisher_mcdc_2026/locations_the_big_apple/pu032 (`DiscardEncounterCardsUntil(card_type=EncounterSideScheme)`).
# ⚠ Mots-pieges : « a support YOU CONTROL » (soutien en jeu du joueur) ; « from A scheme » : UNE manigance au choix (principale ou annexe), pas le complot principal d'office ;
#  « then » : la menace ne part que si le soutien a ete defausse ; Trip : jusqu'a la premiere manigance ANNEXE defaussee, revelee a CE joueur.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        this = effect.this

        def evite() -> None:
            DefausserUneCarteDeLaMain(effect, joueur, EvenementsDeLaMain(joueur, "ATTACK"))

        def desarme() -> None:
            if DefausserUneCarteEnJeu(effect, joueur, list(joueur.supports.Get())) is None:
                return
            cible = ChoisirUneCarte(effect, joueur, [s for s in Worlds.GetOnFieldSchemes(effect) if s.threat > 0])
            if cible is not None:
                this.RemoveThreatFromSchemes([cible], 3, effect)

        def declenche() -> None:
            annexe = Worlds.DiscardEncounterCardsUntil(effect, card_type=EncounterSideScheme)
            if annexe is not None:
                annexe.Reveal(joueur, effect)

        ChoixDePiege(effect, joueur,
                     OptionDePiege(effect, joueur, PIEGE_AVOID, "Discard an ATTACK event from your hand", evite, faisable=bool(EvenementsDeLaMain(joueur, "ATTACK"))),
                     OptionDePiege(effect, joueur, PIEGE_DISARM, "Discard a support you control, then remove 3 threat from a scheme", desarme,
                                   faisable=bool(joueur.supports.Get())),
                     OptionDePiege(effect, joueur, PIEGE_TRIP, "Discard cards from the top of the encounter deck until a side scheme is discarded, then reveal it", declenche))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
