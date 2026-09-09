from . import *

# Scared of the Dark — EVENEMENT, cout 0, RES [energy]. Aucun trait.
# Max 1 per round.
# Hero Action: Remove a tough status card from an enemy -> stun that enemy.
#
# CARTES DE REFERENCE
#  - `32008` Steel Fist et `32009` Bulletproof Protector : le retrait d'une
#    carte de statut Tough, qui est une DEFAUSSE (`Faces.DiscardAll`) de la
#    carte de statut, jamais un drapeau qu'on baisserait.
#  - `selector_target_helper.py:275` (`get_YourHeroTough`) : la carte de statut
#    se lit dans `components.status.GetDeck().FindCards(name="Tough")`. Le
#    moteur ne fournit ce raccourci que pour VOTRE heros ; ici la cible est un
#    ENNEMI, on relit donc la meme zone a la main.
#
# TEXTE CONTRE CODE
#  ⚠ « Remove a tough status card » est le COUT : sans Tough sur l'ennemi, la
#    carte ne fait RIEN — l'ennemi n'est pas etourdi. D'ou le filtre de cible
#    `has_status="Tough"`, qui evite de proposer une cible sans effet.
#  ⚠ « Max 1 per round » -> `LimitOncePerRound()`. Cette limite est IMPRIMEE,
#    elle exige donc un temoin d'epuisement (PROCESSUS-CARTE 7 bis).
#  ⚠ « stun THAT enemy » : celui a qui on a retire le Tough, pas un autre.
def GetAbilities() -> Sequence['Ability']:

    def cartes_tough_de(face: 'CardFace') -> List['CardFace']:
        composants = getattr(face, "components", None)
        if composants is None or getattr(composants, "status", None) is None:
            return []
        return list(composants.status.GetDeck().FindCards(name="Tough"))

    def scared_of_the_dark(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        for ennemi in effect.targets:
            tough = cartes_tough_de(ennemi)
            if not tough:
                continue
            Faces.DiscardAll(tough[:1], effect)
            Faces.GiveStatus([ennemi], "Stunned", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            scared_of_the_dark
        ).SetPlay()
        .SetTarget(Enemy, has_status="Tough")
        .LimitOncePerRound(),
    ]
