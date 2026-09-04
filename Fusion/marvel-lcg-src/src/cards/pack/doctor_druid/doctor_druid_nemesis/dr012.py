from . import *

# Harness Violent Emotions — MANIGANCE ANNEXE NEMESIS. 2 menaces par joueur,
# 3 icones de boost.
# When Revealed: Search the encounter deck and discard pile for Nekra and
#   reveal her.
# Forced Interrupt: When Nekra attacks you, discard 1 identity-specific card
#   from your hand.
#
# CARTES DE REFERENCE
#  - `yd017` / `yd018` (pack yondu) pour « chercher dans le deck ET la
#    defausse de rencontre puis reveler ».
#  - `beast/beast_nemesis/bt021` pour la defausse d'une carte specifique a
#    l'identite.
#
# TEXTE CONTRE CODE
#  « discard 1 identity-specific CARD » -> ici c'est bien CARD, alors que
#    `dr010` et `dr013` disent EVENT. Trois textes voisins, trois portees.
#  « When NEKRA attacks you » -> le declencheur est nomme : une attaque d'un
#    autre ennemi ne compte pas.
#  « 2 menaces PAR JOUEUR » -> `StartingThreat: "2*"` dans `cards.json`,
#    l'etoile signifiant bien « par joueur » sur une MANIGANCE.


def GetAbilities() -> Sequence['Ability']:

    def convoquer_nekra(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(SchemeSide2)
        Unused(this)
        if NekraEnJeu(effect) is not None:
            return
        trouvee = ChercherNekra(effect)
        if trouvee is not None:
            trouvee.Reveal(message.GetToPlayer(), effect)

    def defausser_une_carte(effect: 'Effect', message: 'Message2') -> None:
        joueur = message.GetToPlayer() if hasattr(message, "GetToPlayer") else None
        if joueur is None:
            joueur = Worlds.GetCurrentPlayer(effect)
        if joueur is None:
            return
        candidates = [f for f in joueur.hand_cards.Get() if EstSpecifiqueIdentite(f)]
        if not candidates:
            return
        Faces.DiscardAll([candidates[0]], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            convoquer_nekra,
        ),
        # ⚠ `which_enemy` est un ARGUMENT POSITIONNEL de la fabrique, pas une
        # condition a ecrire soi-meme : c'est lui qui restreint a Nekra.
        AbilityFactory.WhenEnemyActivateAgainstYou(
            AbilityType.ForcedInterrupt,
            CardFinder(name=NOM_NEKRA),
            defausser_une_carte,
        ),
    ]
