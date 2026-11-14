from . import *

# * Elektra — HEROS. DEFENDER. MARTIAL ARTIST. 9 PV, main 5, THW 0 / ATQ 1 / DEF 1 (etoiles imprimees : voir plus bas).
# ★ Villainous. (When this character uses a basic power, give it a boost card.)
# Killer Instinct — Interrupt: When a boost card given to Elektra is turned faceup, cancel its "Boost" ability. Then, that card gains [boost].
#
# CARTES DE REFERENCE
#  - Villainous : mot-cle automatique `desc.Villainous = "1"` (HasVillainous, `Hero` en herite depuis le 01/09/2026 : dd001a Doctor Doom) ; aucun script.
#    ⚠ EXTENSION MOTEUR du 13/11/2026 : la pile de boost d'un heros est maintenant aussi resolue sur DEJOUER et DEFENSE de base
#    (`CanBoost.HeroBoostForBasicPower`, can_thwart.py / can_defense.py), et par INSTANTANE (`ResolveBoostCards`).
#  - Killer Instinct : `hellcat/hc010` Outer Demons (`WhenBoostCardTurnedFaceUp(Interrupt, None, op, boost_for_card=CardFinder(name=...))`
#    + `message.CancelBoostAbility(effect)`) ; l'icone en plus : `GagnerIconeBoostCetteResolution` (set Elektra).
#
# TEXTE CONTRE CODE
#  ⚠ « a boost card GIVEN TO ELEKTRA » : toute carte de boost de l'identite (la sienne par Villainous, ou donnee par une carte).
#  ⚠ « cancel its "Boost" ability » : `CancelBoostAbility` : le ★ Boost de la carte ne part pas ; ses icones imprimees comptent toujours.
#  ⚠ « that card gains [boost] » : +1 icone de boost POUR CETTE RESOLUTION (le pouvoir d'Elektra augmente de 1).
#  ⚠ C'est une INTERRUPTION : le joueur peut la refuser et laisser le Boost de la carte s'executer (cartes Ninja 63002-63004).
#  ⚠ Les etoiles imprimees sur THW / ATQ / DEF sont decrites par ce Villainous (decision utilisateur du 13/11/2026) : aucun effet propre.
#  Chiffres : 9 PV, main 5, THW 0, ATQ 1, DEF 1, Villainous 1, +1 icone.


def GetAbilities() -> Sequence['Ability']:

    def killer_instinct(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)
        message.CancelBoostAbility(effect)
        face = message.trigger
        from game.card.face.attribute.has_boost_icon import HasBoostIcon
        if HasBoostIcon.IsType(face):
            GagnerIconeBoostCetteResolution(face, 1, effect)

    return [
        AbilityFactory.WhenBoostCardTurnedFaceUp(
            AbilityType.Interrupt,
            None,
            killer_instinct,
            boost_for_card=CardFinder(name="Elektra"),
        ).SetName("Killer Instinct"),
    ]
