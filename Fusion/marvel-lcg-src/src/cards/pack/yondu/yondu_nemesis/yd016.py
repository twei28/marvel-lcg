from . import *

# Sword-Gun-Arm — ATTACHEMENT nemesis (3/5). WEAPON. +1 ATQ*. Boost 2.
# Attach to Sav'rkk. If you cannot, attach to the minion with the highest ATK.
#   If you cannot, this card gains surge.
# [star] Attached character's attacks gain overkill.
# Forced Response: When attached character has 2 or less remaining hit points,
#   discard Sword-Gun-Arm.
#
# Cartes de reference :
#  - **`ag013`** Hallucination et **`nt016`** Cosmic Ax : l'attachement qui
#    cherche son porteur, avec un repli et un Surge en dernier recours.
#  - `40122a` * Juggernaut's Helmet pour `+1 ATK` lu dans `desc["ATK+"]` (aucun
#    script) et pour `UnitAttackGainKeyword(..., overkill=True)`.
#  - `ag013` pour l'idiome global `ThisCardGainSurge(effect)`.
#  - `Select.From(..., highest_atk=True)` (factory.py:83) pour « the minion
#    with the HIGHEST ATK » : le selecteur du moteur sait deja trier.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - TROIS niveaux de repli, dans cet ordre : Sav'rkk, sinon le sbire a la plus
#    forte ATQ, sinon Surge. Chaque « If you cannot » se verifie AVANT
#    d'essayer, pas apres un refus (piege `wd028`).
#  - « the minion with the **highest ATK** » : un tri, pas un choix du joueur.
#  - « [star] Attached character's attacks gain **overkill** » : le porteur,
#    pas la carte. `[star]` sans « In expert mode » = toujours actif
#    (convention moteur, cf. 04125).
#  - « When attached character has **2 or less** remaining hit points » : un
#    seuil sur les PV RESTANTS, pas sur les degats subis. Et c'est une
#    `Forced Response`, donc la carte part toute seule — elle n'accompagne pas
#    son porteur dans la mort, elle le quitte juste avant.
#  - ⚠ Sav'rkk imprime « Upgrades cannot be removed from Sav'rkk » : cette
#    interdiction porte sur les AMELIORATIONS, et Sword-Gun-Arm est un
#    ATTACHEMENT. Les deux textes ne se contredisent donc pas — c'est le genre
#    de detail qui se lit sur le type de carte, jamais sur le nom.
#  - « +1 ATK* » : valeur par joueur, convertie nativement par le moteur.


def GetAbilities() -> Sequence['Ability']:

    def sword_gun_arm(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(message)

        savrkk = Worlds.FindCardOnField(effect, name="Sav'rkk", card_type=Minion)
        if savrkk is not None:
            this.AttachTo2(savrkk, effect)
            return

        # « If you cannot, attach to the minion with the HIGHEST ATK. »
        sbires = Worlds.FindCardsOnField(effect, card_type=Minion)
        if sbires:
            meilleur = max(sbires, key=lambda f: f.attack)
            this.AttachTo2(meilleur, effect)
            return

        # « If you cannot, this card gains surge. »
        ThisCardGainSurge(effect)

    def sur_le_depart(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(message)

        Faces.DiscardAll([this], effect)

    def porteur_affaibli(effect: 'Effect', message: 'Message2') -> bool:
        this = effect.this
        porteur = Hote(this)
        return porteur is not None and getattr(porteur, "health", 99) <= 2

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            sword_gun_arm,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            "AttachedEnemy",
            overkill=True,
        ),
        # ⚠ `AfterUnitTookDamage` et PAS `AfterFaceBeDealtDamage` : malgre son
        # nom, cette derniere est un alias de `WhenUnitWouldTakeDamage`
        # (damage.py:665-678), donc une fenetre d'AVANT-COUP — les PV n'ont pas
        # encore baisse et le seuil « 2 or less REMAINING hit points » se lirait
        # sur l'etat d'avant. Verifie dans le moteur, pas suppose.
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.ForcedResponse,
            "AttachedEnemy",
            sur_le_depart,
            conditions=[porteur_affaibli],
        ),
    ]
