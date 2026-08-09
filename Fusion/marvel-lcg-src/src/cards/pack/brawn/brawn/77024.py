from . import *

# Strong as Silk (team-up) — custom « Rainy »
# Team-Up (Brawn and Silk). Max 1 per deck.
# Hero Action: Brawn and Silk get +1 ATK until the end of the round. Brawn and
#   Silk may each make a basic attack without exhausting.
#
# ARBITRAGE (utilisateur, 7/8/2026) : Silk est ici l'ALLIEE signature 77002, pas
# une identite. La cle `TeamUp` de cards.json suppose DEUX identites en jeu et
# rendrait la carte morte en solo ; la restriction est donc portee par une
# condition de jeu, comme Power Couple 73022 du pack jessica_jones.

# ⚠ NE PAS utiliser `SetCondition(only_if_you_control_face=...)` ici : cette
# clause fouille `GetIdentity().GetInventoryDeck()`, c'est-a-dire les cartes
# ATTACHEES a l'identite (ameliorations), et ne voit donc jamais un allie. Elle
# etait silencieusement toujours fausse — la carte restait injouable meme avec
# Silk en jeu, et le cas de test « injouable sans Silk » passait pour la
# mauvaise raison. Defaut trouve le 7/8/2026 en ecrivant le cas symetrique.
def _silk_en_jeu(effect: 'Effect') -> 'CardFace|None':
    joueur = effect.GetInitiator()
    if not isinstance(joueur, Player):
        return None
    for face in joueur.allies.Get():
        if face.IsName("Silk"):
            return face
    return None


def GetAbilities() -> Sequence['Ability']:

    def strong_as_silk(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        joueur = effect.GetInitiator()
        heros = joueur.GetHero()
        silk = _silk_en_jeu(effect)

        equipe = [face for face in (heros, silk) if face is not None]
        for face in equipe:
            face.GainUntilRoundEnd(effect, attack=1)

        # « may each make a basic attack without exhausting » : l'attaque est
        # offerte, donc facultative. `BasicAttack` resout l'attaque de base sans
        # rien epuiser — c'est l'ACTION de base du joueur qui epuise d'ordinaire,
        # pas l'attaque elle-meme.
        for face in equipe:
            joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    f"{face.GetDisplayName()} makes a basic attack without exhausting",
                    lambda targets, attaquant=face: attaquant.BasicAttack(targets, effect),
                ).SetTarget(Enemy),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            strong_as_silk,
            conditions=[lambda effect, message: _silk_en_jeu(effect) is not None],
        ).SetPlay(hero_form_only=True),
    ]
