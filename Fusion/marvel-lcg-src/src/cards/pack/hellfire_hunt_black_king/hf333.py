from . import *

# Energy Absorption (x2, hf332-hf333). Attachement SUPERPOWER. « Max 1 per character. Attach to Sebastian Shaw. Otherwise, attach to the villain.
# Forced Interrupt : When the attached character would take any amount of damage, heal that character for that amount instead of dealing damage. If
# no damage was healed this way, give that character a tough status card. Set aside this card. »
# Cartes de reference : 90129 Wounded Civilians (`SetBeInstead` sur `WhenUnitWouldTakeDamage`), hf101b (WQ : meme message, `PreventDamage`), 60113a,
# `Faces.SetAside` (27100a Sinister Six), `HealthUnits` (rend la quantite REELLEMENT soignee).
# ⚠ « instead of dealing damage » : les degats sont REMPLACES par le soin (la carte reste donc sans effet sur Absorb) ; « If no damage was healed »
# (personnage deja intact) : statut Robuste ; la carte part ensuite de cote DANS TOUS LES CAS.


def GetAbilities() -> Sequence['Ability']:
    def avant_degats(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this
        porteur = message.trigger
        quantite = message.will_take_damage
        message.SetBeInstead(effect)
        soignes = this.HealthUnits([porteur], quantite, effect)
        if soignes <= 0:
            Faces.GiveStatus([porteur], "Tough", effect)
        Faces.SetAside([this], effect)

    return [
        AttacherAShawOuAuVilain(),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, "AttachedEnemy", avant_degats),
    ]
