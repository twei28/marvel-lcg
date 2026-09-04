from . import *

# Ravager Redshirts — soutien signature, x1 (n/15 = 11).
# Cout 2, ressource [physical].
# Hero Interrupt: When you would take any amount of damage from an enemy with
#   the Yaka Arrow upgrade attached, exhaust Ravager Redshirts -> prevent up to
#   2 of that damage.
#
# Cartes de reference :
#  - **`im007`** Energy Shield / **`as001a`** * Armored Spidey / `01098`
#    Armored Rhino Suit : `WhenUnitWouldTakeDamage(HeroInterrupt, "You", op)`
#    puis `message.PreventDamage(2, effect)`.
#  - `17022` * Knowhere / `as010` pour `CostFunc.Exhaust("This")`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « from an enemy **WITH THE YAKA ARROW UPGRADE ATTACHED** » : c'est toute
#    la carte. Un ennemi sans la fleche frappe normalement. Le pack recompense
#    donc de planter la fleche sur celui qui va cogner — et `yd001a` a deja
#    fait 1 degat en l'y plantant.
#  - « **any amount** of damage » SANS « from an attack » : toute instance
#    venant de cet ennemi, attaque ou pas.
#  - « exhaust ... **->** » : la fleche en fait un COUT. Deja incline, le
#    soutien ne previent plus rien ce tour-ci.
#  - « prevent **up to** 2 » : 2 au plus. `PreventDamage(2, ...)` plafonne
#    deja, une instance de 1 degat ne gaspille pas l'inclinaison au-dela.
#  - `who_deal_damage` est le parametre qui rend « from an enemy » : le filtre
#    porte sur l'ATTAQUANT, pas sur la victime.
#  - « Hero Interrupt » : rien en forme civile.


def GetAbilities() -> Sequence['Ability']:

    def porteur_de_la_fleche(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        fleche = LaFleche(effect)
        if fleche is None:
            return False
        source = getattr(message, "attacker", None)
        if source is None:
            source = getattr(getattr(message, "would_deal_damage_message", None), "attacker", None)
        return source is not None and Hote(fleche) is source

    def ravager_redshirts(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        message.PreventDamage(2, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            ravager_redshirts,
            who_deal_damage=Enemy,
            conditions=[porteur_de_la_fleche],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
