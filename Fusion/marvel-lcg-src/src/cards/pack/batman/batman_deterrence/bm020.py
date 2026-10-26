from . import *
# Detective Work — TRAITRISE DETERRENCE (Boost 1 + [star]). When Revealed : choose a player. That player chooses two cards in their discard pile and either
# puts them on the bottom of their deck or shuffles them into their deck. This card gains surge. [star] Boost : Investigate. Give the enemy 1 additional
# boost card for this activation.
# ⚠ « Investigate » n'est defini ni dans le livret ni dans le moteur officiel (mot-cle maison de jessica_jones, sur une manigance) : QUESTION EN ATTENTE ;
# provisoirement, aucun effet en plus de la carte de boost supplementaire.
def GetAbilities() -> Sequence['Ability']:
    def revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        MarquerResolue(this)
        joueur = JoueurRevelation(effect, message)
        ReactionDeSplitDecision(effect, joueur)
        joueurs = Worlds.GetPlayers(effect)
        cible = joueur
        if len(joueurs) > 1 and joueur is not None:
            identite = joueur.AskChooseFace([j.GetIdentity() for j in joueurs], effect)
            cible = next((j for j in joueurs if j.GetIdentity() == identite), joueur)
        if cible is not None:
            defausse = list(cible.discard_pile.Get(True))
            n = min(2, len(defausse))
            if n:
                choisies: List['CardFace'] = []
                cible.ChooseAbilities(
                    effect,
                    AbilityFactory.ForChoiceAbility("Choose two cards in your discard pile", lambda c: choisies.extend(c))
                    .SetTarget(defausse, range=(n, n), not_move=True, not_shuffle=True),
                )
                def dessous(t) -> None:
                    Faces.MoveAllToDeck(choisies, cible.player_deck, "Bottom", effect)
                def melanger(t) -> None:
                    Faces.ShuffleAllTo(choisies, cible.player_deck, effect)
                if choisies:
                    cible.ChooseAbilities(
                        effect,
                        AbilityFactory.ForChoiceAbility("Put them on the bottom of your deck", dessous).SetHasNoTargetEffect(),
                        AbilityFactory.ForChoiceAbility("Shuffle them into your deck", melanger).SetHasNoTargetEffect(),
                    )
        SurgeDeLaDissuasion(effect)
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        MarquerResolue(this)
        if not BoostSupplementaireAnnule(this):
            message.GiveBoostCardForThisActivation(Villain, 1, effect)
    return [
        AbilityFactory.WhenThisRevealed(None, revealed),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
