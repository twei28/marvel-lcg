from . import *

# Onmitsu — PATH hybride (avance), classes Ninjutsu + Taijutsu (Inkwire, TMNT Shinobi). NINJUTSU. TAIJUTSU.
# Permanent. You get -1 hand size.
# Gardener — Hero Response: After you play a Shinobi event, deal 1 damage to your identity -> daze an enemy.
#   (TEXTE CHANGE LE 17/11/2026, fichier Inkwire du 20/10/2026 : avant « an ATTACK or DEFENSE event, take 1 damage ».
#   « Shinobi event » = un EVENEMENT portant l'une des classes Bushido / Ninjutsu / Kuji-Kiri / Taijutsu (docs/reference/
#   mots-cles/shinobi.md) ; le degat reste un COUT, inflige a l'identite du joueur.)
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
#  ⚠ « a SHINOBI EVENT » : un EVENEMENT d'une des quatre classes Shinobi (Dual compris), quel que soit son trait (ATTACK,
#    DEFENSE, THWART...) ; ni un Path, ni une amelioration, ni un allie, ni un evenement Basic/aspect ; « After YOU play » :
#    par le joueur.
#  ⚠ « deal 1 damage to your identity -> daze » : le degat est un COUT (si le joueur ne peut pas le subir, rien ne part).
#  ⚠ « daze AN ENEMY » : un ennemi au choix (sbire ou vilain) ; un ennemi deja hebete n'en recoit pas une seconde.
#  ⚠ Aucune limite imprimee, aucune inclinaison : la capacite part a CHAQUE evenement Shinobi joue.


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
            CardFinder(card_type=Event, card_classes=list(CLASSES_SHINOBI)),  # type: ignore
            gardener,
        ).SetCostFunc(CostFunc.TakeDamage(1, "YourIdentity"))
        .SetTarget(Enemy),
    ]
