from . import *

# Unbreakable Guard — evenement signature (QUASAR 9/16 et 10/16, x2). DEFENSE.
# Cout 1, [mental].
# Hero Interrupt (defense): When a friendly character would take any amount of
#   damage, prevent all of that damage. If you paid for this card with Quantum
#   Bands give that friendly character a tough status card.
#
# Cartes de reference :
#  - **`sj010`** Flash Ward : `WhenUnitWouldTakeDamage(HeroInterrupt, Friend,
#    op).SetPlay().SetLabel("defense")` + `message.PreventDamage(n, effect)`
#    (« When a friendly character would take damage »).
#  - **`jennika/tj004`** : « If you paid for this card with <X> » lu dans
#    `effect.context.paid_this_res_effects` (helper `PayeeAvecLesBandes`).
#  - `05015` / `19001a` pour `Faces.GiveStatus([...], "Tough", effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « a FRIENDLY CHARACTER » : l'identite OU un allie (`Friend`), de
#    n'importe quel joueur, et quelle que soit la source des degats (pas
#    seulement une attaque : « any amount of damage »).
#  - « prevent ALL of that damage » : `PreventDamage("All", ...)`.
#  - « THAT friendly character » : celui qui allait subir les degats
#    (`message.trigger`), pas un autre.
#  - « If you paid for this card WITH QUANTUM BANDS » : un des payeurs est la
#    capacite de ressource des Bandes ; payee autrement, pas de Tenace.
#  - « Hero Interrupt (defense) » : forme heros, libelle defense.


def GetAbilities() -> Sequence['Ability']:

    def garde(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.PreventDamage("All", effect)
        if PayeeAvecLesBandes(effect):
            Faces.GiveStatus([message.trigger], "Tough", effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            Friend,
            garde,
        ).SetPlay().SetLabel('defense'),
    ]
