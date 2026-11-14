from . import *

# Zen-Like Calm — EVENEMENT 0 [energy], aspect Leadership (Iron Fist 31). TACTIC.
# Action: Heal 1 damage from a Martial Artist character. Then, if that character has no sustained damage, heal 1
#   damage from another character.
#
# CARTES DE REFERENCE
#  - `40197` Safehouse : choix d'une cible de soin, `this.HealthUnits(cibles, N, effect)` + `canbe_heal=True`.
#  - `60068b` Damaged Spine : « Then, if there is no damage here » = test de l'etat APRES le soin dans la meme resolution.
#
# TEXTE CONTRE CODE
#  ⚠ « a MARTIAL ARTIST character » : tout personnage (heros, allie, identite, ou meme ennemi) portant le trait ;
#    lecture litterale du mot « character » (RR) : la carte ne dit pas « you control ».
#  ⚠ « THAT character has no sustained damage » : testee apres le soin, sur la meme carte (0 degat restant).
#  ⚠ « ANOTHER character » : un personnage different du premier, au choix, tout type de personnage.
#  ⚠ Le second soin n'a lieu que si le premier personnage n'a plus aucun degat ; s'il en garde, rien de plus.
#  ⚠ « Action » nue : jouable dans les deux formes (pas « Hero Action »).


def GetAbilities() -> Sequence['Ability']:

    def zen_like_calm(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        premier = [t for t in effect.targets if t is not None]
        if not premier:
            return
        this.HealthUnits(premier, 1, effect)
        cible = premier[0]
        if cible.IsInPlay() and cible.GetLostHealth() > 0:
            return
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        def soigner(cibles: Sequence['CardFace']) -> None:
            this.HealthUnits([c for c in cibles if c is not None], 1, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Heal 1 damage from another character", soigner)
            .SetTarget(CardFinder(card_type=Unit2, check_effect_fn=lambda e, f: f != cible), canbe_heal=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            zen_like_calm,
        ).SetPlay()
        .SetTarget(CardFinder(card_type=Unit2, trait="MARTIAL ARTIST"), canbe_heal=True),
    ]
