from . import *

# Assassinate — EVENEMENT 2 [mental], Ninjutsu (TMNT Shinobi, Inkwire). ATTACK.
# Play only if your hero is cloaked.
# Action (attack): Deal 7 damage to a minion. This attack gains piercing.
# « Silence and speed are weapons we wield. » —Splinter
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : Cloak / Cloaked (cloak.md, cloaked.md), Piercing (piercing.md),
# Shinobi (shinobi.md).
#
# Cartes de reference :
#  - `04044` Piercing Strike : `hero.DealDamage(cibles, N, effect, property=AttackProperty(piercing=True))`
#    + `.SetPlay().SetLabel('attack')` ;
#  - `ub033` / `JouableSiVousControlez` : condition de jeu posee en tete des conditions ;
#  - `08003` Covert Ops : evenement en `AbilityType.Action` (ni Hero Action) avec `SetLabel('thwart')`.
#
# TEXTE CONTRE CODE
#  ⚠ « Play only if YOUR HERO is cloaked » : le heros (forme heros) porte une carte Cloaked (`HerosCamoufle`) ; en
#    forme alter-ego il n'y a pas de heros : non jouable (Q-N1, .planning/tmnt/shinobi-ninjutsu-questions.md).
#  ⚠ « Action » (et NON « Hero Action ») : AbilityType.Action, tel qu'imprime ; la condition ci-dessus fait que seule
#    la forme heros peut la jouer. Q-N1 : coquille probable de « Hero Action » ?
#  ⚠ « 7 damage to a MINION » : un sbire, jamais le vilain ; « This attack gains piercing » : l'attaque PERCE
#    (Coriace ignoree d'abord, `AttackProperty(piercing=True)`). Cloaked sur le HEROS n'est pas touche par cette attaque
#    (il ne subit rien).


def GetAbilities() -> Sequence['Ability']:

    def assassinate(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None or not joueur.IsHero():
            return
        joueur.GetHero().DealDamage(effect.targets, 7, effect, property=AttackProperty(piercing=True))

    return [
        JouableSiHerosCamoufle(
            AbilityFactory.WhenInYourPlayTurn(
                AbilityType.Action,
                assassinate,
            ).SetPlay().SetLabel('attack')
            .SetTarget(Minion)
        ),
    ]
