from . import *

# Aided Defense — EVENEMENT signature, custom « CptScorp »
# Cout 0, ressource [energy], trait DEFENSE. Deux exemplaires physiques :
# pt003 et pt004, meme texte, meme code (pt004 importe celui-ci).
#
# Hero Interrupt (defense): When your hero defends against an attack, exhaust
#   an ally you control -> you get +1 DEF for each remaining hit point on the
#   exhausted ally. If you take no damage from that attack, ready the
#   exhausted ally.
#
# ---------------------------------------------------------------------------
# CARTE DE REFERENCE : `09015` Desperate Defense (Doctor Strange) et `58033`
# Disarming Defense (Wonder Man). Meme montage exact :
# `WhenUnitDefendAgainstAttack(AbilityType.HeroInterrupt, "YourHero", ...)`
# `.SetPlay()`, puis `message.GainDEFForThisAttack(n, effect)` et
# `message.IfYouTakeNoDamage(action)`.
#
# `.SetLabel('defense')` : le libelle imprime entre parentheses. C'est lui qui
# fait de la carte une reponse de DEFENSE au sens du jeu (une capacite
# libellee « defense » n'est pas une defense de base et ne fait donc pas
# reduire les degats par la DEF du heros — voir le commentaire de
# `GainDEFForThisAttack`, sender_unit.py:139-141).
# `SetLabel` AVANT `SetTarget` / `SetCostFunc` : ordre impose par le depot.
#
# ---------------------------------------------------------------------------
# LA FLECHE EST UN COUT -> UN EFFET
#
# Cout = « exhaust an ally you control », rendu par
# `.SetCostFunc(CostFunc.Exhaust("YourAlly"))` (modele `03017` Strength In
# Numbers, seule carte du depot qui incline un allie comme COUT d'un
# evenement). `"YourAlly"` est la cible-chaine du moteur pour « les allies
# que TU controles » (selector_target_helper.py:180-182), et
# `CostFunc.Exhaust` ajoute lui-meme `canbe_exhaust=True` au filtre
# (cost_func.py:227).
#
# Consequence directe et VOULUE : sans allie pret sous son controle, le
# joueur ne peut pas payer, `CostFunc.Base.HasTargets` rend False, et la
# carte n'est PAS proposee. Cout impayable = rien ne se passe.
#
# ⚠ L'allie qui DEFEND n'est pas un candidat : defendre l'a deja incline.
#
# ---------------------------------------------------------------------------
# « +1 DEF FOR EACH REMAINING HIT POINT »
#
# « remaining hit point » = les PV COURANTS de l'allie epuise, pas ses PV
# imprimes : `face.health` (les degats subis sont deja deduits). Le +1 PV de
# Hawkingbird (pt002) compte donc, puisqu'il passe par `Gain(health=...)` et
# releve `max_health` comme `health`.
#
# L'allie epuise est relu sur le COUT :
# `effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards`
# (cost_func.py:200-206), exactement comme `03017`. On ne le redemande pas au
# joueur : ce serait une seconde question, et surtout le texte dit « THE
# exhausted ally » (mot-piege `that <nom>` du PROCESSUS-CARTE §5).
#
# ---------------------------------------------------------------------------
# « IF YOU TAKE NO DAMAGE FROM THAT ATTACK, READY THE EXHAUSTED ALLY »
#
# `message.IfYouTakeNoDamage(action)` (sender_unit.py:153-176) : le moteur
# enregistre une capacite temporaire qui ne part qu'a la fin de l'attaque, et
# seulement si le defenseur n'a rien encaisse. C'est la brique employee par
# `09015`, `48018`, `38016` et `58033`. La redresse vise L'ALLIE EPUISE, pas
# le heros (difference avec 09015, qui redresse le heros).


def GetAbilities() -> Sequence['Ability']:

    def aided_defense(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        epuises = list(effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards)
        if not epuises:
            return

        # « +1 DEF for each remaining hit point on the exhausted ally »
        bonus = 0
        for allie in epuises:
            bonus += max(0, allie.CastTo(Unit2).health)
        if bonus > 0:
            message.GainDEFForThisAttack(bonus, effect)

        # « If you take no damage from that attack, ready the exhausted ally. »
        def redresser():
            vivants = [x for x in epuises if x.IsInPlay()]
            if vivants:
                Faces.ReadyAll(vivants, effect)

        message.IfYouTakeNoDamage(redresser)

    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.HeroInterrupt,
            "YourHero",
            aided_defense,
        ).SetPlay()
        .SetLabel('defense')
        .SetCostFunc(CostFunc.Exhaust("YourAlly")),
    ]
