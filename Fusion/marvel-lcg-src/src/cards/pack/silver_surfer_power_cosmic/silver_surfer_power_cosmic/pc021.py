from . import *

# Terrax's Axe — ATTACHEMENT NEMESIS (3/5). POWER COSMIC. WEAPON. +1 ATK au
# personnage porteur (bonus imprime, bas de carte).
#
# Texte imprime :
#  « Attach to Terrax, if Terrax is not in play attach to the villain
#    instead. »
#  « [star] Forced Response: After the attached character attacks, if that
#    attack dealt damage, stun the attacked character. »
#  « Hero Action: Spend ** resources -> discard this card. »
#
# CARTES DE REFERENCE
#  - `62031` Cottonmouth (luke_cage_nemesis) / `59039` Ares (hercules_nemesis) :
#    `AttachToFaceWhenPutIntoPlay(CardFinder(name=.., card_type=Minion),
#    otherwise_attach_to=Villain)` -- modele EXACT pour « attach to X, if X
#    is not in play attach to the villain instead » : geree ICI, pas par
#    les cartes qui la cherchent (`pc019` Terrax, `pc022` Cleave the Way se
#    contentent de la mettre en jeu).
#  ⚠ PIEGE TROUVE le 05/11/2026 : `otherwise_attach_to="EnemyLeader"`
#    (vu sur `57024` Taskmaster/`56161` Namor) resout vers la classe
#    `Leader` (`card_type/leader.py`), un type `FinalType` DISTINCT de
#    `EncounterVillain` malgre l'heritage -- Rhino (comme la plupart des
#    mechants) est `EncounterVillain`, jamais `Leader`. Avec
#    `"EnemyLeader"`, l'attache echouait silencieusement des que Terrax
#    etait absent (aucune cible trouvee, `PutIntoPlay` n'entrait jamais en
#    jeu, sans la moindre erreur). `otherwise_attach_to=Villain` (la classe
#    ABSTRAITE, pas Final) couvre EncounterVillain ET Leader.
#  - desc `"ATK+": "1"` (modele `57024` Taskmaster's Shield, `desc.SCH+`,
#    MEME carte que `AttachToFaceWhenPutIntoPlay` ci-dessus) : « +1 ATK »
#    imprime est une cle de base NATIVE pour un attachement d'ennemi (lue
#    directement dans `card_face.py:53`), PAS `GiveKeywordToAttached` (ca
#    doublerait le bonus -- 57024 n'appelle d'ailleurs jamais cette fabrique
#    pour son propre `SCH+`).
#  - `lj017` Provoked (lockjaw_nemesis) : `AfterUnitAttackEnd(ForcedResponse,
#    "AttachedCharacter", op)` -- modele pour « after the attached character
#    attacks ».
#  - `Faces.GiveStatus([cible], "Stunned", effect)` : « stun the attacked
#    character ».
#  - `ca017` Death Spiral (carnage_nemesis) : `AbilityFactory.
#    PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("YY"))`
#    -- modele EXACT pour « Hero Action: Spend ** resources -> discard this
#    card » (meme icone repetee deux fois = deux [energy] = "YY").
#
# TEXTE CONTRE CODE
#  « ATTACH TO TERRAX, if Terrax is NOT IN PLAY attach to the villain
#    INSTEAD » : jamais les deux, choix automatique a la mise en jeu.
#  « if THAT ATTACK dealt damage » : `message.total_dealt_damage > 0`, pas
#    « si le porteur peut infliger des degats » en general.
#  « stun the ATTACKED character » : la cible reellement touchee
#    (`message.damaged_targets`), pas le porteur de la hache.
#  « Spend ** resources » : DEUX ressources [energy] precisement (meme
#    icone repetee deux fois sur le scan), pas une ressource au choix.


def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        if message.total_dealt_damage <= 0:
            return
        Faces.GiveStatus(message.damaged_targets, "Stunned", effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name="Terrax", card_type=Minion),
            otherwise_attach_to=Villain,
        ),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            "AttachedCharacter",
            apres_attaque,
        ),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("YY")),
    ]
