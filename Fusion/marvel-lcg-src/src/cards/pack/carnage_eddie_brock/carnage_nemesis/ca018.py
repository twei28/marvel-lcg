from . import *

# * Closing the Loops : TRAITRISE (x2), boost 1. Set « Carnage Nemesis ».
# When Revealed: Torment attacks you (even in alter-ego form). If no attack was made this way, this card gains surge.
# [star] Boost: This card gets +1 boost icon if you have more than 2 classifications in play (identity-specific, aspect, or basic).
#
# CARTES DE REFERENCE
#  - « X attacks you (even in alter-ego) ; if no attack... surge » : `ld013` (Lash Out) : `ennemi.DoAttackYou(joueur, effect, ..)` (attaque dans les deux formes) ; `if_no_attack_was_made=` (enemy.py:110) pour le surge.
#  - Boost etoile « +1 boost icon » : `sk116` (Skrull Assault) : `WhenCardBecomeBoost("This", op)` + `message.GainBoostIcon(n, effect)`.
#
# TEXTE CONTRE CODE
#  « TORMENT attacks you » : Torment en JEU (introuvable ou pas en jeu : aucune attaque -> surge) ; « even in alter-ego form » : `DoAttackYou` attaque aussi l'alter-ego. « If NO attack was made this way » : `if_no_attack_was_made` (aussi quand Torment est absent).
#  « [star] Boost: +1 boost icon IF you have MORE THAN 2 classifications IN PLAY » : plus de 2 classifications DISTINCTES parmi les cartes sous le controle du joueur (identite comprise : IdentitySpecific ; un aspect compte par aspect ; Basic). Meme `ClassificationDe` que Torment.
#    ⚠ LECTURE A CONFIRMER : l'identite elle-meme compte comme « identity-specific in play » (lecture litterale : elle est une carte en jeu). Sans elle, il faudrait trois classifications parmi les seules cartes du deck. Chiffres : boost 1 (+1), seuil > 2.


def GetAbilities() -> Sequence['Ability']:

    def closing_the_loops(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        torment = Worlds.FindCardOnField(effect, name=NOM_TORMENT, card_type=Enemy)
        if torment is None or not torment.IsInPlay() or joueur is None:
            this.GainSurge(1, effect)
            return
        torment.CastTo(Enemy).DoAttackYou(
            joueur,
            effect,
            if_no_attack_was_made=lambda: this.GainSurge(1, effect),
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = effect.world.GetCurrentPlayer()
        if joueur is None:
            return
        classifications: set = set()
        for face in joueur.GetControlCards():
            if face.IsInPlay():
                classifications |= ClassificationDe(face)
        if len(classifications) > 2:
            message.GainBoostIcon(1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            closing_the_loops,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
