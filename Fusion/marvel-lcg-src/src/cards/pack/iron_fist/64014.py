from . import *

# * Iron Fist (Lin Lie) — ALLIE 4 [physical], aspect Protection (Iron Fist 14). AGENT OF ATLAS. MARTIAL ARTIST.
#   PV 3, THW 1*, ATK 2**.
# [star] Response: After Iron Fist (this ally) attacks an enemy who has been attacked by a hero this phase, stun that
#   enemy. If Iron Fist defeated that enemy, he takes −2 consequential damage (✪) from this attack.
#
# CARTES DE REFERENCE
#  - `32091` Cannonball : « takes -N consequential damage after he attacks and defeats a minion » =
#    `AfterUnitAttackAndDefeatUnit(NonKeywordStar, ..., fn)` + `this.GainForThisActive(effect, message.GetWouldAtkMessage(),
#    attack_consequential_damage=-N)`.
#  - `01077` Counter-Punch / `64004` : `Faces.GiveStatus(cibles, "Stunned", effect)` apres une attaque.
#  - moteur : `world.stat.this_phase_made_attack` (AJOUT du 22/10/2026), voir 64021.
#
# TEXTE CONTRE CODE
#  ⚠ « attacked BY A HERO » : un HEROS (identite en forme heros), pas un allie ni un alter-ego. L'attaque d'Iron Fist
#    (allie) n'en est pas une, meme sur sa 2e attaque de la phase.
#  ⚠ « THIS PHASE » : toute la phase, tous les joueurs (multijoueur compris).
#  ⚠ « stun THAT enemy » : l'ennemi attaque, s'il est encore en jeu ; un ennemi vaincu n'est pas etourdi.
#  ⚠ « If Iron Fist DEFEATED that enemy » : −2 sur les degats consecutifs de CETTE attaque (ATK 2** = 2 imprimes -> 0),
#    seulement si l'ennemi etait deja attaque par un heros ; sinon les 2 degats consecutifs s'appliquent.


def AttaqueParUnHerosAvant(effect: 'Effect', cibles: Sequence['CardFace']) -> bool:
    this = effect.this
    for attaquant, _, attaquees in effect.world.stat.this_phase_made_attack:
        if attaquant is this or attaquant is None or not Hero.IsType(attaquant):
            continue
        if any(c in attaquees for c in cibles if c is not None):
            return True
    return False


def GetAbilities() -> Sequence['Ability']:

    def iron_fist_lin_lie(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        cibles = [c for c in message.attacked_targets if c is not None and c.IsInPlay()]
        Faces.GiveStatus(cibles, "Stunned", effect)

    def sans_consecutif(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Ally)
        this.GainForThisActive(effect, message.GetWouldAtkMessage(), attack_consequential_damage=-2)

    def ennemi_deja_attaque_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        return AttaqueParUnHerosAvant(effect, message.attacked_targets)

    def ennemi_deja_attaque_defait(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> bool:
        return AttaqueParUnHerosAvant(effect, [message.target])

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.Response,
            "This",
            iron_fist_lin_lie,
            conditions=[ennemi_deja_attaque_attaque],
        ),
        AbilityFactory.AfterUnitAttackAndDefeatUnit(
            AbilityType.NonKeywordStar,
            "This",
            Enemy,
            sans_consecutif,
            conditions=[ennemi_deja_attaque_defait],
        ),
    ]
