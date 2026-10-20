from . import *

# Kree Sentry (II) — MECHANT, stade 2 (Kree Sentry). KREE. ROBOT. PV 18[per_hero], MNG 2, ATQ 2[star].
# When Revealed: Attach a set aside copy of Sentry's Grasp to Rick Jones.
# [star] Forced Response: After Kree Sentry attacks and damages a character, attach a set aside copy of
#   Sentry's Grasp to that character. If you cannot, place 2 threat on the main scheme.
#
# Cartes de reference :
#  - « After X attacks and damages a character » : `AfterUnitAttackAndDamageUnit(ForcedResponse, ..)`, modele OFFICIEL
#    01118 Sonic Converter (« After Klaw attacks and damages a character, stun that character »). Mais le filtre
#    `target_in_play` n'est PAS pose : un personnage VAINCU par l'attaque a bien ete blesse, la Reponse part et la
#    Poigne ne peut plus s'y attacher -> « If you cannot, place threat ».
#  - « attach a set aside copy ... If you cannot » : `AttacherUnePoigne` (kree_sentry/__init__.py, `AttachTo2`, modele
#    sunfire `AttacherUneBrulure`), faux s'il ne reste aucune copie ou si la cible a quitte le jeu.
#  - « place N threat on the main scheme » : `PlaceThreatOnSchemes("MainScheme", n)` (modele 01121).
#  - « When Revealed: attach a set aside copy ... to Rick Jones » : `WhenThisRevealed` + `AttacherUnePoigne`.
#
# ⚠ Mots-pieges : « attacks AND DAMAGES » (aucun degat = rien) ; « THAT character » ; « a SET ASIDE copy » (la
# reserve, pas une Poigne deja attachee) ; « If you cannot » ; l'etoile de l'ATQ renvoie a ce texte (desc.ATK = "2").


def GetAbilities() -> Sequence['Ability']:

    def poigne(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        if not AttacherUnePoigne(effect, message.attacked):
            effect.this.PlaceThreatOnSchemes("MainScheme", 2, effect)

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        AttacherUnePoigne(effect, RickJones(effect))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "This",
            "Character",
            poigne,
        ),
    ]
