from . import *

# * Director of Security — AMELIORATION, cout 2, RES [wild]. TITLE.
# Decrease the number of boost icons of the first card revealed from the
#   REGISTERED deck each round by 1.
# Alter-Ego Resource: Exhaust this card -> generate a [wild] resource.
#
# ⚠⚠ C'EST LA CARTE QUI FAIT BAISSER LE PRIX. Le recrutement se paie en ICONES
# DE BOOST, pas en cout de ressource (voir l'en-tete de `__init__.py`) : aucune
# reduction de cout du jeu ne touche le deck REGISTERED, celle-ci si.
#
# CARTES DE REFERENCE
#  - `15009` Scarlet Witch's Crest : `WhenBoostIconsWouldBeCount` +
#    `message.UpdateBoostIcon(-1, effect)`. Le moteur borne deja le resultat a
#    0 (has_boost_icon.py:44, « Fix 15009, cannot decrease lower than 0 »).
#  - `as015` * Scarlet Spider : la meme reduction, cote adverse.
#  - `bt014` * Peter Parker : `CanGenerateResources(AbilityType.
#    AlterEgoResource, Resources("G")).SetCostFunc(CostFunc.Exhaust("This"))`.
#
# TEXTE CONTRE CODE
#  ⚠⚠ « the FIRST card revealed from the REGISTERED deck EACH ROUND » : le
#    moteur envoie `WhenBoostIconsWouldBeCount` pour TOUTES les cartes dont on
#    compte les icones, cartes de boost du vilain comprises (can_boost.py:87).
#    Une simple `LimitOncePerRound()` serait donc brulee par la premiere carte
#    de boost venue. Le filtre doit etre EXACT, et il l'est :
#    `EstLaPremiereReveleeDuRound` (voir `__init__.py`) retient QUELLE FACE a
#    ete revelee en premier du deck REGISTERED ce round. La limite reste par
#    dessus, pour le cas ou l'on compterait deux fois les icones de la meme
#    carte dans le round.
#  ⚠ Le prix peut etre lu A LA FIN DU ROUND (`ip002a` Registration Act fait
#    payer a ce moment-la). Le marqueur porte le numero de round, il tient
#    donc jusque-la — mais pas au-dela, ce qui est exactement le texte.
#  ⚠ La reduction n'est PAS conditionnee au fait de payer : elle s'applique au
#    comptage. Refuser le recrutement ne la rend pas.
#  ⚠ « Alter-Ego Resource » et non « Resource » : Iron Patriot cote heros ne
#    peut pas s'en servir. Le moteur connait le sous-type
#    (`AbilityType.AlterEgoResource`, resources.py:277), rien a arbitrer ici,
#    contrairement a `bt014`.
#  ⚠ `AbilityType.Constant` N EXISTE PAS : la valeur "Constant" est portee par
#    le membre `AbilityType.NonKeyword` (ability_type.py:43). Piege verifie le
#    09/09/2026, `verifier_appels_modules` ne voit pas les membres d enum.
#  ⚠ UNE SEULE `CanGenerateResources` par carte (assert du moteur). Le cas est
#    respecte : c'est la seule.


def GetAbilities() -> Sequence['Ability']:

    def cest_la_premiere_revelee_du_round(
            effect: 'Effect',
            message: 'Message.WhenBoostIconsWouldBeCount') -> bool:
        joueur = JoueurQuiControle(effect.this)
        if joueur is None or message.trigger is None:
            return False
        return EstLaPremiereReveleeDuRound(joueur, effect, message.trigger)

    def moins_une_icone(effect: 'Effect',
                        message: 'Message.WhenBoostIconsWouldBeCount') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.UpdateBoostIcon(-1, effect)

    return [
        AbilityFactory.WhenBoostIconsWouldBeCount(
            AbilityType.NonKeyword,
            moins_une_icone,
            conditions=[cest_la_premiere_revelee_du_round],
        ).LimitOncePerRound(),
        AbilityFactory.CanGenerateResources(
            AbilityType.AlterEgoResource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
