from . import *

# Cimmerian Counter (x2) — evenement, cout 1* [energy]. ATTACK. THWART.
# [star] Discount 1 (KING).
# Imprime : « Hero Action (attack/thwart): After you defend against an enemy
#   attack, deal damage to an enemy equal to your ATK or remove threat from a
#   scheme equal to your THW. »
#
# ⚠ TEXTE CONTRADICTOIRE (une Action ne part pas « After you defend »).
#   Arbitrage utilisateur du 25/09/2026 : jouee en HERO RESPONSE juste apres
#   avoir defendu contre une attaque ennemie. Precision de l'utilisateur,
#   conforme au Rules Reference v1.8 (Defend, Defense) : jouer une carte
#   « (defense) » pendant l'attaque compte comme avoir defendu.
#
# CARTES DE REFERENCE
#  - `AfterUnitDefendAgainstAttack(type, "YourHero", op)` (factory/do_attack.py,
#    message AfterUnitDefendEnd) ; pt005 Covered Fire pour le choix
#    degats/menace calcule sur une statistique.
#
# TEXTE CONTRE CODE
#  « your ATK » / « your THW » : les valeurs COURANTES du heros (bonus compris).


def GetAbilities() -> Sequence['Ability']:

    def contre_coup(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        Unused(message)
        this = effect.this.CastTo(Event)
        joueur = JoueurDe(effect)
        if joueur is None:
            return
        heros = joueur.GetIdentity()
        atk = heros.CastTo(CanAttack).attack if isinstance(heros, CanAttack) else 0
        thw = heros.CastTo(CanThwart).thwart if isinstance(heros, CanThwart) else 0
        ChoisirDegatsOuMenace(joueur, this, effect, atk, thw)

    return [
        DiscountAbility(1, ["KING"]),
        AbilityFactory.AfterUnitDefendAgainstAttack(
            AbilityType.HeroResponse,
            "YourHero",
            contre_coup,
        ).SetPlay().SetLabel('attack', 'thwart'),
    ]
