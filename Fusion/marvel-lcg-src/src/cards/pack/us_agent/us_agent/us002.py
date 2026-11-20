from . import *

# Bouncing Bulwark — evenement signature, x3 (1/15, 2/15, 3/15). ATTACK. TACTIC. Cout 0, ressource [physical].
# Hero Action (attack): Discard U.S. Agent's Shield → deal 4 damage to an enemy. Then, if this attack deals 2 or more
# excess damage, put U.S. Agent's Shield into play from your discard pile.
#
# Cartes de reference :
#  - `13013` Into the Fray / `28013` No Quarter : « for each point of EXCESS damage dealt by this attack » =
#    `this.DealDamage(cibles, N, effect, if_this_attack_deal_excess_damage=fn)`, `fn(excess)` recevant le surplus.
#  - `54023` Winter, Widow, Soldier, Spy / `bk008` : `face.PutIntoPlay(joueur, effect)` pour poser une amelioration depuis
#    la defausse ou la main.
#  - `RECETTES-MOTEUR` §7 « Une carte permanente... » / §5 : `CostFunc.Discard("YouControlCards", name=..., card_type=Upgrade)`.
#
# ⚠ Mots-pieges :
#  - « Discard U.S. Agent's Shield → » est un COUT : sans le bouclier EN JEU, la carte est injouable ; il part en defausse
#    AVANT l'attaque, et c'est de la DEFAUSSE qu'il revient.
#  - « 2 OR MORE excess damage » : `excess_damage >= 2`, pas `> 0` (un surplus de 1 ne ramene rien).
#  - « put INTO PLAY from your discard pile » : le bouclier revient en jeu equipe au heros, pret (jamais en main).
#  - « Hero Action (attack) » : libelle `attack` (alimente Sonne / Desoriente) ; une seule cible ennemie.


def GetAbilities() -> Sequence['Ability']:

    def bouncing_bulwark(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()

        def reprendre_le_bouclier(surplus: int) -> None:
            if surplus < 2:
                return
            for face in list(initiator.discard_pile.Get()):
                if face.IsName(NOM_BOUCLIER) and Upgrade.IsType(face):
                    face.PutIntoPlay(initiator, effect)
                    return

        this.DealDamage(effect.targets, 4, effect, if_this_attack_deal_excess_damage=reprendre_le_bouclier)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            bouncing_bulwark,
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Discard("YouControlCards", name=NOM_BOUCLIER, card_type=Upgrade))
        .SetTarget(Enemy),
    ]
