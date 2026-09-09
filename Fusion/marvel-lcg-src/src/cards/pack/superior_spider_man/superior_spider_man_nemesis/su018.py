from . import *

# Goblin Glider — ATTACHEMENT nemesis. Boost 3. +1 ATQ. WEAPON.
# Attach to the enemy with the highest printed hit points and without another
#   Goblin Glider attached. If you cannot, this card gains surge.
# Hero Action: Spend [energy][energy] resources -> discard this card.
#
# CARTES DE REFERENCE
#  - `42027` * Harpoon's Harpoon, `al022` * Frogjolnir :
#    `AttachToFaceWhenPutIntoPlay(CardFinder(...), if_cannot_operation=)` —
#    la branche `if_cannot_operation` porte le « If you cannot ».
#  - `an010` : `this.GainSurge(1, effect)`.
#  - `bl015`, `ar013` : « Spend <ressources> → discard this card » =
#    `CostFunc.Spend(Cost("YY"))` sur une Hero Action.
#
# TEXTE CONTRE CODE
#  ⚠ « the enemy with the HIGHEST PRINTED hit points » : les PV IMPRIMES, pas
#    les PV restants. Un vilain a 3 PV restants sur 18 reste le plus « gros ».
#  ⚠ « and WITHOUT ANOTHER GOBLIN GLIDER attached » : sans ce filtre, deux
#    exemplaires s'empileraient sur le meme ennemi. Le pack n'en a qu'un, mais
#    le texte prevoit le cas et un scenario peut en faire surgir d'autres.
#  ⚠ « IF YOU CANNOT, this card gains surge » : la branche de repli, verifiee
#    AVANT le choix (piege `wd028` : un « if you cannot » doit etre
#    reellement atteignable).
#  ⚠ « +1 ATK » est une BASE lue dans `desc` (`ATK+`), aucun script.
#  ⚠ « Spend [energy][energy] » : deux ENERGIES precises, pas deux ressources
#    quelconques — `Cost("YY")`.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def pv_imprimes(face: 'CardFace') -> int:
        return int(getattr(face, "printed_health", 0) or 0)

    def porte_deja_un_planeur(face: 'CardFace') -> bool:
        for c in list(face.GetPlacedCardArea().Get(True)) + list(face.GetAttachedUpgrades()):
            if c is not None and CardId(c) == "su018":
                return True
        return False

    def cible_valide(face: 'CardFace') -> bool:
        return face is not None and Enemy.IsType(face) and not porte_deja_un_planeur(face)

    def sans_cible(effect: 'Effect', joueur: 'Player') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(joueur)
        this.GainSurge(1, effect)

    def choisir_le_plus_gros(effect: 'Effect') -> 'CardFace|None':
        candidats = [e for e in Worlds.GetOnFieldEnemies(effect) if cible_valide(e)]
        if not candidats:
            return None
        return max(candidats, key=pv_imprimes)

    def se_defausser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(message)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(check_face_fn=lambda f: f is not None and cible_valide(f)),
            if_cannot_operation=sans_cible,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            se_defausser,
        ).SetName("Goblin Glider")
        .SetCost(Cost("YY")),
    ]
