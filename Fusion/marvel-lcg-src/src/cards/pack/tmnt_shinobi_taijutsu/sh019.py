from . import *

# Sideswipe — EVENEMENT 0 [mental], Taijutsu (TMNT Shinobi, Inkwire). THWART.
# Hero Action (thwart): Remove 1 threat from a scheme. If this removes the last threat on that scheme, return an
#   ATTACK card from your discard pile to your hand.
#
# Mots-cles : aucun (classe Taijutsu, fiche shinobi.md).
#
# Cartes de reference :
#  - « Hero Action (thwart) : remove N threat ... If this removes the last threat » : `04049` Clear the Area (teste
#    `threat == 0` APRES coup, ce qui se declenche aussi si la manigance n'avait deja plus de menace) ; ici on emploie le
#    crochet exact `RemoveThreatFromSchemes(..., if_this_remove_last_threat=fn)` de `ma015` Break Through / `56009` ;
#  - « return an ATTACK card from your discard pile to your hand » : `54003` Black Widow (`Faces.ReturnToHand`), choix du
#    joueur `AskChooseFaces` comme `se004` Shihan.
#
# TEXTE CONTRE CODE
#  ⚠ « If THIS removes the LAST threat on THAT scheme » : c'est CE retrait qui vide la manigance choisie (pas une manigance
#    deja a 0, pas une autre manigance) ; une menace restante => rien n'est rendu.
#  ⚠ « an ATTACK CARD » : une carte portant le TRAIT ATTACK, de n'importe quel type (pas seulement un evenement) ;
#    « from YOUR discard pile » ; Sideswipe n'est pas ATTACK elle-meme.
#  ⚠ « Hero Action » : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def sideswipe(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        derniere = [False]

        def noter(*args):
            Unused(args)
            derniere[0] = True

        this.RemoveThreatFromSchemes(effect.targets, 1, effect, if_this_remove_last_threat=noter)

        if not derniere[0] or joueur is None:
            return
        candidats = [f for f in joueur.discard_pile.Get() if f.HasTrait("ATTACK")]
        if not candidats:
            return
        if len(candidats) == 1:
            choisie = candidats
        else:
            choisie = joueur.AskChooseFaces(candidats, (1, 1), effect, prompt="Return an ATTACK card to your hand")
        if choisie:
            Faces.ReturnToHand(list(choisie), joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            sideswipe,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
