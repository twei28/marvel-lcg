from . import *

# Infrared Web — EVENEMENT BASIC, cout 1, [energy]. ATTACK. DEFENSE. Team-Up (Spider-Man and Predator). Max 1 per deck.
# Hero Interrupt (attack/defense): When an enemy attack would deal damage to you, prevent 3 of that damage. Deal 3 damage to an enemy.
#
# Cartes de reference :
#  - `core/spider_man/01003` Backflip : `WhenUnitWouldTakeDamage(Interrupt, "You", op, is_from_attack=True)` et
#    `message.PreventDamage(n, effect)` ; `.SetTarget("TeamUp")` obligatoire pour un evenement Team-Up (br011, al023).
#
# ⚠ Mots-pieges :
#  - « When an enemy ATTACK would deal damage to YOU » : une attaque ennemie contre toi (`is_from_attack=True`), pas les degats
#    indirects ni ceux d'une traitrise ; « prevent 3 OF THAT damage » : au plus 3 ;
#  - « Deal 3 damage to an enemy » : un ennemi au choix, EN PLUS de la prevention (fiche mots-cles/teamup.md : Spider-Man doit
#    etre en jeu, heros ou allie) ; coquille du scan : « damge » (lu « damage »).


def GetAbilities() -> Sequence['Ability']:

    def toile_infrarouge(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = JoueurDeCetteCarte(effect)
        message.PreventDamage(3, effect)
        if joueur is None:
            return
        ennemis = [e for e in Worlds.GetOnFieldEnemies(effect) if e is not None]
        if ennemis:
            cible = joueur.AskChooseFace(ennemis, effect, prompt="Deal 3 damage to")
            joueur.GetHero().DealDamage([cible or ennemis[0]], 3, effect, property=AttackProperty())

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "You",
            toile_infrarouge,
            is_from_attack=True,
        ).SetPlay().SetLabel('defense')
        .SetTarget("TeamUp"),
    ]
