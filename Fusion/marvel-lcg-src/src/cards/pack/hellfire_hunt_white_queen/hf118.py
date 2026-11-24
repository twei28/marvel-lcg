from . import *

# Fractured Loyalties (x2). Traitrise ILLUSION PSIONIC. « When Revealed : Choose an ally you control. It makes a basic attack against you (with
# exhausting and taking the consequential damage). If no attack was made this way, this card gains surge. »
# Cartes de reference : 02030 I See You (`DoAttackYou`), 56098 (`BasicAttack`), 01133 (`if_no_attack_was_made`), 01029b (`AskChooseFace`).
# ⚠ « with exhausting » : l'allie s'incline pour attaquer ; un allie DEJA incline ne peut pas : sans allie pret, la carte gagne surge.
# Les degats consequents viennent de l'etoile imprimee sur l'ATQ de l'allie (`can_attack.py` : `printed_attack_consequential_damage`).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        allies = [f for f in joueur.GetControlCards(CardFinder(card_type=Ally)) if f.IsInPlay() and f.IsReady()]
        if not allies:
            ThisCardGainSurge(effect)
            return
        allie = allies[0] if len(allies) == 1 else joueur.AskChooseFace(allies, effect)
        if allie is None:
            ThisCardGainSurge(effect)
            return
        Faces.ExhaustAll([allie], effect)
        allie.BasicAttack([joueur.GetIdentity()], effect, if_no_attack_was_made=lambda: ThisCardGainSurge(effect))

    return [AbilityFactory.WhenThisRevealed(None, revelee)]
