from . import *

# Tailblock — evenement signature, x2 (n/16 = 10 et 11). DEFENSE. SKILL.
# Cout 1, ressource [mental].
# Hero Interrupt (defense): When you would take any amount of damage, if the
#   Battle Board upgrade has the:
#   • [[VEHICLE]] trait, prevent 1 of that damage and draw 2 cards.
#   • [[WEAPON]] trait, prevent 3 of that damage.
#
# Cartes de reference :
#  - **`im007`** Energy Shield / **`as001a`** * Armored Spidey / `01098`
#    Armored Rhino Suit : `WhenUnitWouldTakeDamage(HeroInterrupt, "You", op)`
#    puis `message.PreventDamage(n, effect)`.
#  - `09015` Desperate Defense / `sg016` Unbeatable! pour le libelle
#    `('defense')` sur une interruption d'evenement.
#  - `bt023` pour `DrawUp`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **any amount** of damage » SANS « from an attack » : toute instance,
#    d'ou l'ABSENCE de `is_from_attack`. C'est la difference exacte avec
#    `as001a` Armor Protection du pack precedent, qui, elle, precise
#    « from an attack ». Une traitrise, un degat indirect, un degat que le
#    heros s'inflige : tous ouvrent la fenetre.
#  - « prevent **1** ... and draw **2** » cote VEHICLE, « prevent **3** » cote
#    WEAPON : la face arme protege trois fois mieux mais ne pioche pas. Ne pas
#    intervertir, et ne pas ajouter la pioche a la branche WEAPON.
#  - Les deux branches sont EXCLUSIVES, et AUCUNE ne tombe sans planche : la
#    carte est alors depensee pour rien. C'est le texte, et c'est pourquoi
#    `nt012` Practice et `nt014` Cemented, qui bloquent le retournement, font
#    si mal.
#  - « **(defense)** » : le libelle livre la carte a Desoriente et la fait
#    compter comme une defense. Un seul `SetLabel`.
#  - « Hero Interrupt » : rien en forme civile.


def GetAbilities() -> Sequence['Ability']:

    def tailblock(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        if PlancheEstVehicule(effect):
            message.PreventDamage(1, effect)
            initiator = effect.GetInitiator()
            if initiator is not None:
                initiator.DrawUp(2, effect)
        elif PlancheEstArme(effect):
            message.PreventDamage(3, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            tailblock,
        ).SetPlay().SetLabel('defense'),
    ]
