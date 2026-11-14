from . import *

# Deception (Se Reveler) (x3) : EVENEMENT (SHAPESHIFTER. TACTIC.), cout 1, [mental]. Max 1 per round.
# Action: Flip all shapeshift form upgrades facedown and ready them. Draw 1 card. Choose a shapeshift form upgrade and flip that card faceup.
#
# CARTES DE REFERENCE
#  - `03015` Avengers Assemble! : `.SetPlay().MaxOnePerRound()` (« Max 1 per round » vaut deja pour toute la table, limit-max.md) + `Faces.ReadyAll`.
#  - `21187a` : `card.Flip(effect)` ; `my002` : choix d'une forme par `AskChooseFace`.
#
# TEXTE CONTRE CODE
#  « Flip ALL form upgrades FACEDOWN and READY THEM » : les trois formes passent cachees (celles qui le sont deja ne bougent pas), puis les trois sont redressees (meme celles qui n'ont pas change). « Draw 1 card » :
#    une carte. « CHOOSE a form and flip THAT card FACEUP » : apres la pioche, une forme au choix passe visible (toutes sont alors cachees ; elle retourne les AUTRES facedown par sa Reponse forcee, sans objet ici).
#    « Max 1 per round » : `MaxOnePerRound`, partage entre les trois exemplaires. « Action » nue : jouable aussi en alter-ego.
#  Chiffres : cout 1, pioche 1.


def GetAbilities() -> Sequence['Ability']:

    def deception(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        for forme in Formes(joueur):
            RetournerCachee(forme, effect)
        Faces.ReadyAll(Formes(joueur), effect)
        joueur.DrawUp(1, effect)
        formes = Formes(joueur)
        if not formes:
            return
        choisie = joueur.AskChooseFace(formes, effect, prompt="Choose a shapeshift form upgrade to flip faceup", peek=True, not_move=True)
        if choisie is not None:
            RetournerVisible(choisie, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            deception,
        ).SetPlay().SetLabel()
        .MaxOnePerRound(),
    ]
