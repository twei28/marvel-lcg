from . import *

# Shapeshifter (Changement de Forme) : AMELIORATION (CONDITION. SUPERPOWER.), sans cout, [energy]. Permanent.
# Action: Exhaust Shapeshifter -> choose a shapeshift form upgrade and flip that card.
# (Le « Setup: Put the Shapeshifter upgrade into play » est imprime sur my001b ; ici `desc.Setup` + `desc.Permanent` : le moteur la met en jeu a la mise en place.)
#
# CARTES DE REFERENCE
#  - `21187a` Norn Stone : `WhenInYourPlayTurn(HeroAction, op)` + `this.card.Flip(effect)` ; ici le retournement vise une AUTRE carte (une forme).
#  - `bs002` / `dy002` : amelioration Permanent + Setup, sans script pour l'entree en jeu.
#
# TEXTE CONTRE CODE
#  « Action » nue : jouable aussi en alter-ego (comme les formes). « Exhaust Shapeshifter » : cout. « choose a shapeshift form upgrade » : l'une des trois formes en jeu, visible OU cachee ; « flip that card » :
#    elle change de face (cachee -> visible, mais aussi visible -> cachee). Le declenchement « turned faceup » des formes (retourner les autres) est SUR LES FORMES (my003-my005).
#  Chiffres : aucun cout imprime.


def GetAbilities() -> Sequence['Ability']:

    def changement_de_forme(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        formes = Formes(joueur)
        if not formes:
            return
        choisie = joueur.AskChooseFace(formes, effect, prompt="Choose a shapeshift form upgrade to flip", peek=True, not_move=True)
        if choisie is not None:
            Retourner(choisie, effect)

    def une_forme_en_jeu(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return bool(Formes(effect.GetInitiator()))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            changement_de_forme,
            conditions=[une_forme_en_jeu],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
