from . import *

# Bulldozing Charge (2/2) — exemplaire physique 2/2, contenu identique a
# pt021 (voir ce fichier pour le detail des modeles et des arbitrages,
# notamment la portee de « each friendly character »).


def GetAbilities() -> Sequence['Ability']:

    def bulldozing_charge(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()

        def degat_a_chaque_personnage_ami():
            amis = list(Worlds.GetOnFieldFriendlyCharacters(effect))
            if amis:
                this.DealDamage(amis, 1, effect)

        hyde = Worlds.FindCardOnField(effect, name=NOM_MR_HYDE, card_type=Enemy)
        if hyde:
            hyde.DoAttackYou(joueur, effect,
                             if_no_attack_was_made=degat_a_chaque_personnage_ami)
        else:
            degat_a_chaque_personnage_ami()

    def bulldozing_charge_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        message.would_atk_message.GainOverKill(effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            bulldozing_charge,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            bulldozing_charge_boost,
            during_attack=True,
        ),
    ]
