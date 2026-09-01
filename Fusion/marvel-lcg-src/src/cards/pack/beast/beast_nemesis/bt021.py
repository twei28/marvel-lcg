from . import *

# Dark Transformation — traitrise nemesis (3/5). Boost 1.
# When Revealed: Discard the top 5 cards from your deck. You take 1 damage
# for every hero-specific card you discarded this way.
#
# Cartes de reference :
#  - squelette « When Revealed » d'une carte du set nemesis : an011 Hel's
#    Retribution, meme `WhenThisRevealed(None, op)` et meme facon d'atteindre
#    le joueur vise, `message.GetToPlayer()` (recette moteur §1). Comparable
#    parce que les deux defaussent le dessus du DECK DU JOUEUR depuis un When
#    Revealed, et que l'initiateur d'une carte de rencontre n'est PAS le
#    joueur : le prendre par `effect.GetInitiator()` viserait a cote.
#  - defausse du dessus du deck joueur : 42025 * Harpoon, via an011,
#    `joueur.DiscardDeckTopCards(n, effect)`.
#  - degats a l'identite depuis une carte nemesis : 50062 (nick_fury_nemesis),
#    `this.DealDamage([identity], n, effect)`.
#  - « hero-specific card » : 11020 Depowered, seule carte officielle a
#    employer l'expression. Le moteur ne la rend PAS par `desc.Class ==
#    "Hero"` mais par la classe `"IdentitySpecific"` ; le test face par face
#    est celui de `player_action.py:574`, `ClassCard.IsType(face) and
#    face.IsClass("IdentitySpecific")`.
#
# ⚠ « for EVERY hero-specific card » : 1 degat PAR carte, pas 1 degat s'il y
# en a au moins une (mot-piege `for each`, PROCESSUS-CARTE.md etape 5).
#
# ⚠ « from YOUR deck » : le deck du JOUEUR, pas le deck de rencontre.
#
# ⚠ Un deck plus court que 5 cartes ne pose pas de probleme :
# `DiscardDeckTopCards` remelange la defausse et rend ce qu'il a pu prendre ;
# on compte sur la liste RENDUE, jamais sur le 5 imprime.

def GetAbilities() -> Sequence['Ability']:

    def dark_transformation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()
        if joueur is None:
            return

        faces = joueur.DiscardDeckTopCards(5, effect)

        nombre = 0
        for face in faces:
            if ClassCard.IsType(face) and face.IsClass("IdentitySpecific"):
                nombre += 1

        if nombre > 0:
            identity = joueur.GetIdentity()
            if identity is not None:
                this.DealDamage([identity], nombre, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            dark_transformation,
        ),
    ]
