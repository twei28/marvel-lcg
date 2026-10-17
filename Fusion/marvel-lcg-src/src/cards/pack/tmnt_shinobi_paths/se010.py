from . import *

# Onmitsu — PATH hybride (avance), classes Ninjutsu + Taijutsu (Inkwire, TMNT Shinobi). NINJUTSU. TAIJUTSU.
# Permanent. You get -1 hand size.
# Gardener — Hero Response: After you play an ATTACK or DEFENSE event, take 1 damage -> daze an enemy.
#
# Mots-cles (fiches lues AVANT le code) : Daze (daze.md / dazed.md) ; Permanent (permanent.md) ;
# Shinobi / Path (shinobi.md).
#
# Cartes de reference :
#  - « After you play a <filtre> » : `jennika/tj011` / `michelangelo/tm011`
#    (`AfterPlayerPlayedCard(Response, "You", CardFinder(...), op)`) ;
#  - « take 1 damage -> » : `45043` Blood Rage (`CostFunc.TakeDamage(1, "YourIdentity")`) ;
#  - « daze an enemy » : `Faces.GiveStatus([ennemi], "Dazed", effect)` (`tx016` Wrapped Up), cible `Enemy`.
#
# TEXTE CONTRE CODE
#  ⚠ « an ATTACK OR DEFENSE EVENT » : un EVENEMENT portant le trait ATTACK ou le trait DEFENSE (pas THWART seul,
#    pas une amelioration ou un allie) ; « After YOU play » : par le joueur.
#  ⚠ « take 1 damage -> daze » : le degat est un COUT (si le joueur ne peut pas le subir, rien ne part).
#  ⚠ « daze AN ENEMY » : un ennemi au choix (sbire ou vilain) ; un ennemi deja hebete n'en recoit pas une seconde.
#  ⚠ Aucune limite imprimee, aucune inclinaison : la capacite part a CHAQUE evenement ATTACK/DEFENSE joue.


def GetAbilities() -> Sequence['Ability']:

    def gardener(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Path)
        Unused(this, message)
        ShinobiDaze(effect, [t for t in effect.targets if t is not None])

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("You", hand_size=-1),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.HeroResponse,
            "You",
            CardFinder(card_type=Event, traits=["ATTACK", "DEFENSE"]),  # type: ignore
            gardener,
        ).SetCostFunc(CostFunc.TakeDamage(1, "YourIdentity"))
        .SetTarget(Enemy),
    ]
