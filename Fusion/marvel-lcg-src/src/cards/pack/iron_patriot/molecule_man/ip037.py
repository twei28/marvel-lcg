from . import *

# Manipulate Realities — TRAITRISE du set MOLECULE MAN (4/6), x3. Boost 3.
# When Revealed: If Molecule Man is in play, choose a printed resource type
#   ([energy], [mental], [physical], or [wild]) in your hand. Discard each card
#   from your hand with the chosen resource type. Otherwise, this card gains
#   surge.
#
# ⚠ TROIS EXEMPLAIRES DANS LE SET, ET LA CARTE « STARTER DECK » N'EN ANNONCE
# QUE DEUX (rangs 53-54). Le materiel imprime fait foi : MM04, MM05 et MM06
# sont trois fichiers distincts, l'encounter set en compte trois.
#
# CARTES DE REFERENCE
#  - `41028` Psionic Illusion : `joueur.DeclareResourceType()` et
#    `FacesCounter.GetPrintedResources([face]).HasColorPrinted(...)`.
#  - `04077` * Absorbing Man : la bascule « si la carte est en jeu, sinon ».
#
# TEXTE CONTRE CODE
#  ⚠ « If Molecule Man IS IN PLAY » : en jeu, d'ou `Worlds.FindCardOnField`.
#    Sinon surge, et rien d'autre — la main n'est pas touchee.
#  ⚠ « choose a printed resource type IN YOUR HAND » : le choix porte sur une
#    couleur PRESENTE en main. On ne propose donc que celles qu'on y trouve, ce
#    qui evite le choix vide. Main sans aucune icone : rien a defausser.
#  ⚠ « DISCARD EACH card ... with the chosen resource type » : toutes, pas une.
#    C'est ce qui rend la carte brutale a plusieurs icones de meme couleur.
#  ⚠ `HasColorPrinted` ne convertit PAS le joker : [wild] doit etre nomme pour
#    que les cartes [wild] tombent (resources.py:136). C'est bien ce que dit la
#    carte, qui liste [wild] comme un choix a part entiere.


def GetAbilities() -> Sequence['Ability']:

    def manipuler(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        if joueur is None:
            return

        if Worlds.FindCardOnField(effect, name="Molecule Man", card_type=Minion) is None:
            this.GainSurge(1, effect)
            return

        main = [f for f in joueur.hand_cards.Get() if f is not None]
        if not main:
            return
        presentes = FacesCounter.GetPrintedResources(main)
        couleur = joueur.DeclareResourceType(
            r=presentes.HasColorPrinted("R"),
            b=presentes.HasColorPrinted("B"),
            y=presentes.HasColorPrinted("Y"),
            g=presentes.HasColorPrinted("G"),
        )
        a_defausser = [f for f in main
                       if FacesCounter.GetPrintedResources([f]).HasColorPrinted(couleur)]
        if a_defausser:
            Faces.DiscardAll(a_defausser, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            manipuler,
        ),
    ]
