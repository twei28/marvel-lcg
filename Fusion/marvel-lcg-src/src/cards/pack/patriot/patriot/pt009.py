from . import *

# Commander's Orders — AMELIORATION signature, custom « CptScorp »
# Cout 1, ressource [mental], aucun trait.
#
# Hero Interrupt: When an ally you control would activate, exhaust
#   Commander's Orders -> switch its ATK and THW values for that activation.
#
# ---------------------------------------------------------------------------
# « WOULD ACTIVATE » POUR UN ALLIE = UTILISER UN POUVOIR DE BASE
#
# Le mot « activation » designe une ACTIVATION D'ENNEMI dans le vocabulaire
# du moteur (`WhenEnemyWouldActivate`). Un ALLIE, lui, ne s'active pas : il
# utilise un pouvoir de base, ATQ ou CTR. Le message correspondant est
# `Message.WhenUnitUseBasicPower` (sender_unit.py:8-34), envoye par
# `can_attack.py:162` et `can_thwart.py:111` juste APRES le
# `WhenUnitWouldAttack` / `WhenUnitWouldThwart` et AVANT tout calcul de
# degats ou de menace : la fenetre est donc bien une INTERRUPTION, et le
# bonus pose la est pris en compte.
#
# Fabrique : `AbilityFactory.WhenUnitUseBasicPower(AbilityType.HeroInterrupt,
# Ally, ..., powers=["ATK", "THW"], control_by="You")`.
# - `Ally` : « an ally », pas le heros (le heros a aussi DEF et REC).
# - `control_by="You"` : « you control » (factory/friend.py:351-354).
# - `powers=["ATK", "THW"]` : les deux seuls pouvoirs d'un allie
#   (`IsAllyPower`, sender_unit.py:18-19). Sans ce filtre la capacite
#   partirait aussi pour un DEF ou un REC, que la carte ne mentionne pas.
#
# ---------------------------------------------------------------------------
# ⚠ `message.power` VAUT 'ATK' / 'THW' / 'DEF' / 'REC' / 'SCH'
#
# JAMAIS 'Attack' ni 'Thwart'. Ce piege a deja produit DEUX conditions mortes
# sur ce projet : une condition qui compare a 'Attack' est toujours fausse,
# la capacite se declenche et ne fait rien, et aucun outil ne le voit. Les
# cinq valeurs sont posees en dur aux quatre sites d'envoi
# (can_attack.py:162, can_thwart.py:111, can_defense.py:54,
# can_recover.py:67, can_scheme.py:86).
#
# ---------------------------------------------------------------------------
# « SWITCH ITS ATK AND THW VALUES FOR THAT ACTIVATION »
#
# On n'echange pas les caracteristiques de la carte : on corrige la valeur de
# CE pouvoir-la, le temps de cette activation. `message.GainValue(diff,
# effect)` (sender_unit.py:21-34) aiguille tout seul vers
# `GainATKForThisAttack` ou `GainTHWForThisThwart` selon le `would_message`
# — c'est exactement la brique du moteur pour « pour cette activation ».
#
#   - pouvoir ATQ : on veut que l'allie frappe pour sa valeur de CTR,
#     donc diff = CTR - ATQ ;
#   - pouvoir CTR : on veut qu'il contre pour sa valeur d'ATQ,
#     donc diff = ATQ - CTR.
#
# C'est la symetrie exacte de `message.UseATKInsteadTHW`
# (sender_friend.py:75-89), la methode officielle du moteur pour « use ATK
# instead of THW » (employee par `jj012`), qui calcule elle aussi
# `diff = atk - thw`. On ne peut pas l'appeler telle quelle ici : elle ne
# couvre qu'un SENS sur les deux, et notre message est un
# `WhenUnitUseBasicPower`, pas un `WhenUnitWouldThwart`.
#
# Un allie dont ATQ = CTR (Hawkingbird apres un bonus, par exemple) donne
# diff = 0 : l'echange est un non-evenement, mais la capacite se declenche et
# le cout est paye. C'est la lettre de la carte — on n'ajoute pas une
# condition qu'elle n'imprime pas.
#
# ---------------------------------------------------------------------------
# LA FLECHE EST UN COUT -> UN EFFET
#
# Cout = « exhaust Commander's Orders » -> `CostFunc.Exhaust("This")`. Une
# amelioration deja inclinee n'est pas proposee. Cout impayable = rien ne se
# passe.
#
# ⚠ PAS de `SetPlay()` sur cette capacite : c'est le piege corrige le
# 4/8/2026 sur `66006` Vanishing Act et `66007` Force Shields — `SetPlay` sur
# la capacite d'une AMELIORATION la rendait inerte une fois la carte posee.
# La capacite « Play » de l'amelioration est fournie automatiquement par
# `Upgrade.GetAbilities` (card_type/upgrade.py:14-18), qui l'attache a
# l'identite du joueur faute de selecteur declare : c'est le comportement
# voulu, la carte ne dit pas « attach to ».


def GetAbilities() -> Sequence['Ability']:

    def commanders_orders(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        allie = message.trigger.CastTo(Ally)
        atk = allie.attack
        thw = allie.thwart

        if message.power == "ATK":
            diff = thw - atk
        elif message.power == "THW":
            diff = atk - thw
        else:
            return

        if diff != 0:
            message.GainValue(diff, effect)

    return [
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            Ally,
            commanders_orders,
            powers=["ATK", "THW"],
            control_by="You",
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
