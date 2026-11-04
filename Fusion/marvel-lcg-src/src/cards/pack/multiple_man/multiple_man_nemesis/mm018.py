from . import *

# Who's Killing Dupes? : MANIGANCE ANNEXE (set nemesis, 1/5), menace 3, boost 2, icone centrale Amplify 1 (comparee a Vendetta 16054).
# Only a Dupe ally can remove threat from this scheme.
# When Revealed: Discard a Dupe ally from play.
#
# CARTES DE REFERENCE : `bc004` (`ThreatCannotBeRemovedFromWhile("This", by_character=CardFinder(non_name=..))`), `ca016` / `60095` (`WhenThisRevealed(None, op)`).
# TEXTE CONTRE CODE : DECISION UTILISATEUR (04/11) : seul un allie Dupe retire de la menace (evenements et Reabsorb Dupe ne le peuvent pas). « Discard a Dupe ally FROM PLAY » : un Dupe de n'importe quel
#  joueur ; le joueur qui revele choisit s'il y en a plusieurs ; aucun Dupe : sans effet (aucun surge imprime). Amplify : lu dans `desc`. Chiffres : menace 3, boost 2.


def GetAbilities() -> Sequence['Ability']:

    def tuer_un_dupe(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        dupes = DupesEnJeu(effect)
        if not dupes:
            return
        choisi = joueur.AskChooseFace(dupes, effect, forced=True) if len(dupes) > 1 else dupes[0]
        if choisi is not None:
            Faces.DiscardAll([choisi], effect)

    return [
        AbilityFactory.ThreatCannotBeRemovedFromWhile(
            "This",
            by_character=CardFinder(non_name=NOM_DUPE),
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            tuer_un_dupe,
        ),
    ]
