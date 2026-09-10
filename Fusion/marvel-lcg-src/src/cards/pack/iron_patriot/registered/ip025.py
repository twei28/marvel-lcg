from . import *

# * Ghost — SBIRE du deck REGISTERED (12/20). 4 PV, ATQ 1, MNG 3, boost 3.
# ELITE. SPY.
# Incite 1. Patrol.
# [star] Divide threat from Ghost's scheme or thwart among each scheme as
#   evenly as possible.
# Intangible Espionage — Special: Remove 1 threat from each scheme for each
#   [crisis], [acceleration], [amplify], and [hazard] in play.
#
# ⚠ LA CARTE EST SYMETRIQUE : sbire, elle repartit SA menace sur toutes les
# manigances ; alliee, elle repartit SON CONTRE de la meme facon. Le meme
# geste, dans les deux sens — d'ou une seule phrase pour les deux.
#
# CARTES DE REFERENCE
#  - `dt104` Divert Attention : la boucle « aussi egalement que possible »,
#    `manigances[i % len(manigances)]`, sur `Worlds.GetOnFieldSchemes`.
#  - `29033` * Bombshell : `divided_evenly` cote attaque. Rien d'equivalent
#    n'existe cote menace, d'ou les deux interceptions ci-dessous.
#  - `Worlds.GetIconsNum(effect, ["Crisis", "Acceleration", "Amplify",
#    "Hazard"])` (worlds.py:343) : le moteur compte DEJA ces quatre icones
#    ensemble, et cette fonction n'existe que pour cela.
#
# TEXTE CONTRE CODE
#  ⚠⚠ Les quatre glyphes de la carte ont ete identifies un par un contre la
#    police du moteur (`public/fonts/ChampionsIcons.ttf`, releve du
#    09/09/2026) : ce sont crisis, acceleration, amplify et hazard, dans cet
#    ordre. Ce ne sont PAS les quatre symboles d'aspect, qui leur ressemblent
#    en petit.
#  ⚠ « Remove 1 threat from EACH scheme FOR EACH icon » : le total part sur
#    CHAQUE manigance, pas reparti entre elles. C'est l'inverse exact de la
#    ligne du dessus, qui, elle, repartit. Deux phrases voisines, deux sens
#    opposes : c'est le piege de lecture de la carte.
#  ⚠⚠ COTE MANIGANCE, on n'annule PAS l'activation : `SetBeInstead` ferait
#    sauter les cartes de boost, le journal de phase et la fenetre
#    d'activation. On intercepte `WhenRecalculateSchemeValue`, juste avant la
#    pose (can_scheme.py:156) : on garde sur la cible sa part, et on pose la
#    main les parts des autres.
#  ⚠⚠ COTE CONTRE, le moteur sait deja repartir : il suffit de passer
#    `property.is_divided = True` et de lister CHAQUE manigance autant de fois
#    qu'elle recoit (can_thwart.py:143, `curr_thwart = schemes_dict[target] *
#    thwart` avec `thwart = 1`). `ReplaceTarget` pose la liste.
#  ⚠ Une seule manigance en jeu : il n'y a rien a repartir, on laisse le
#    moteur faire son travail habituel.
#  ⚠ Incite et Patrol sont des BASES NATIVES de sbire, qui disparaissent avec
#    la conversion en allie. Correct : un allie n'incite personne.


def GetAbilities() -> Sequence['Ability']:

    def parts_egales(manigances: Sequence['CardFace'], total: int) -> Dict['CardFace', int]:
        parts: Dict['CardFace', int] = {}
        for i in range(total):
            cible = manigances[i % len(manigances)]
            parts[cible] = parts.get(cible, 0) + 1
        return parts

    def repartir_la_menace(effect: 'Effect', message: 'Message.WhenRecalculateSchemeValue') -> None:
        this = effect.this
        manigances = list(Worlds.GetOnFieldSchemes(effect))
        if len(manigances) <= 1 or message.value <= 0:
            return
        cible = message.scheme
        ordre = [cible] + [m for m in manigances if m is not cible]
        parts = parts_egales(ordre, message.value)
        message.value = parts.get(cible, 0)
        for manigance, part in parts.items():
            if manigance is not cible and part > 0:
                this.PlaceThreatOnSchemes([manigance], part, effect)

    def repartir_le_contre(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        this = effect.this.CastTo(Unit2)
        manigances = list(Worlds.GetOnFieldSchemes(effect))
        if len(manigances) <= 1:
            return
        total = message.property.GetThwart(this)
        if total <= 0:
            return
        deja = [c for c in message.targets if c is not None]
        ordre = deja + [m for m in manigances if m not in deja]
        parts = parts_egales(ordre, total)
        message.property.is_divided = True
        etalement: List['CardFace'] = []
        for manigance, part in parts.items():
            etalement += [manigance] * part
        message.ReplaceTarget(*etalement)

    def espionnage_intangible(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this
        Unused(message)
        valeur = Worlds.GetIconsNum(
            effect, ["Crisis", "Acceleration", "Amplify", "Hazard"])
        if valeur <= 0:
            return
        this.RemoveThreatFromSchemes("EachScheme", valeur, effect)

    return [
        AbilityFactory.WhenRecalculateSchemeValue(
            AbilityType.NonKeyword,
            repartir_la_menace,
            conditions=[lambda effect, message: message.trigger == effect.this],
        ),
        AbilityFactory.WhenUnitWouldThwart(
            AbilityType.NonKeyword,
            "This",
            repartir_le_contre,
        ),
        SpecialRegistered("Intangible Espionage", espionnage_intangible),
    ]
