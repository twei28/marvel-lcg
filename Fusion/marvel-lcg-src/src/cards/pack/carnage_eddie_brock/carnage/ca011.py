from . import *

# * Vicious Lashing : EVENEMENT (ATTACK. DEFENSE.), cout 2, [physical]. Classe Hero. (x2)
# Hero Interrupt (attack/defense): When an enemy attacks you, deal 4 damage to that enemy. This attack gains ranged.
# Hero Action (attack): Deal 2 damage to an enemy. Deal 2 damage to an enemy. This attack gains ranged.
#
# CARTES DE REFERENCE
#  - Interruption d'evenement « when an enemy attacks you → deal N damage to that enemy » : `05012` (Nova) : `WhenUnitInitiatesAttackAgainst(Interrupt, Enemy, "You", op).SetTarget("Attacker")` ;
#    evenement a libelle `bw005` (`.SetPlay().SetLabel('defense')`) ; mot-cle ranged : fiche mots-cles/ranged.md, `AttackProperty(ranged=True)`.
#  - Action « Deal 2 damage to an enemy. Deal 2 damage to an enemy. » : `bm003` (Violent Means) : deux choix de cible INDEPENDANTS (`Worlds.GetOnFieldEnemies` + `AskChooseFace`), cas `bm003` (`cibles=[VILAIN, VILAIN]`).
#
# TEXTE CONTRE CODE
#  « Hero Interrupt (attack/defense) » : `HeroInterrupt` + `SetLabel('attack', 'defense')`. « When an enemy attacks YOU » : l'attaque vise l'identite du joueur (`"You"`), pas un allie. « deal 4 damage to THAT enemy » : l'attaquant (`SetTarget("Attacker")`).
#  « This attack gains RANGED » : `AttackProperty(ranged=True)` sur les degats (pas de Retaliate en retour). « Deal 2 damage to AN enemy. Deal 2 damage to AN enemy » : DEUX cibles choisies separement, la meme possible.
#  Deux capacites distinctes sur la meme carte : l'Interruption n'est proposee que pendant une attaque ennemie, l'Action pendant le tour du joueur. Chiffres : cout 2, 4 degats / 2 + 2 degats.


def GetAbilities() -> Sequence['Ability']:

    def riposte(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        this.DealDamage(effect.targets, 4, effect, property=AttackProperty(ranged=True))

    def double_coup(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        for _ in range(2):
            ennemis = Worlds.GetOnFieldEnemies(effect)
            if not ennemis:
                return
            cible = joueur.AskChooseFace(ennemis, effect)
            if cible is not None:
                this.DealDamage([cible], 2, effect, property=AttackProperty(ranged=True))

    return [
        AbilityFactory.WhenUnitInitiatesAttackAgainst(
            AbilityType.HeroInterrupt,
            Enemy,
            "You",
            riposte,
        ).SetPlay().SetLabel('attack', 'defense')
        .SetTarget("Attacker"),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            double_coup,
        ).SetPlay().SetLabel('attack'),
    ]
