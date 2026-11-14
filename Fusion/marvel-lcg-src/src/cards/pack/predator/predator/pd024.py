from . import *

# Razor Hunt — EVENEMENT BASIC, cout 1, [physical]. ATTACK. Team-Up (Wolverine and Predator). Max 1 per deck.
# Hero Action (attack): Deal 1 damage each to Wolverine and Predator. Deal 3 damage to an enemy. Deal 3 damage to an enemy.
#
# Cartes de reference :
#  - `br011` Hammer Time / `al023` Little Rascals / `12020` Swarm Tactics : UN EVENEMENT TEAM-UP PORTE `.SetTarget("TeamUp")`
#    (assert de `database.py:223`) ; `desc.TeamUp "Wolverine;Predator"` et `desc.MaxPerDeck` sont des bases automatiques
#    (fiche mots-cles/teamup.md : les allies comptent) ;
#  - `Worlds.GetOnFieldFriendlyCharacters(effect)` (al023) pour retrouver Wolverine et Predator ; `core/01053` pour l'attaque.
#
# ⚠ Mots-pieges :
#  - « 1 damage EACH to Wolverine AND Predator » : 1 degat a CHACUN des deux (ils se blessent eux-memes : cout de la carte) ;
#  - « Deal 3 damage to AN enemy. Deal 3 damage to AN enemy. » : DEUX applications independantes, chacune CHOISIT son ennemi
#    (le meme deux fois ou deux differents) ; texte litteral, question posee a l'auteur (QUESTIONS-AUTEUR.md) ;
#  - « Wolverine » : tout personnage ami de ce nom (allie 32041, ou heros) ; ce n'est pas une carte du deck de Predator seule.


def GetAbilities() -> Sequence['Ability']:

    def chasse_au_rasoir(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        amis = [f for f in Worlds.GetOnFieldFriendlyCharacters(effect)
                if f is not None and f.card.IsOnField() and (f.IsName("Wolverine") or f.IsName("Predator"))]
        if amis:
            this.DealDamage(amis, 1, effect)
        for _ in range(2):
            ennemis = [e for e in Worlds.GetOnFieldEnemies(effect) if e is not None]
            if not ennemis:
                return
            cible = joueur.AskChooseFace(ennemis, effect, prompt="Deal 3 damage to")
            joueur.GetHero().DealDamage([cible or ennemis[0]], 3, effect, property=AttackProperty())

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            chasse_au_rasoir,
        ).SetPlay().SetLabel('attack')
        .SetTarget("TeamUp"),
    ]
