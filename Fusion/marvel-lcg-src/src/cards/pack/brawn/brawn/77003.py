from . import *

# * Ironheart (Riri Williams) — alliee signature ALTERNATIVE, custom « Rainy »
# Multiverse.
# [star] Interrupt: When Ironheart uses a basic power, the Amadeus Cho player
#   puts the top card of their deck into their reserve.
#
# « Uses a basic power » couvre les trois pouvoirs de base d'une alliee :
# attaque, manigance et defense. Le moteur les expose separement, d'ou les
# trois fabriques.

def GetAbilities() -> Sequence['Ability']:

    def carte_du_dessus_en_reserve(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Ally)

        # « the Amadeus Cho player » : le controleur d'Ironheart, seul joueur
        # que la carte peut designer sans ambiguite a une table a plusieurs.
        joueur = this.GetControlByPlayer()
        if not isinstance(joueur, Player):
            return

        dessus = joueur.player_deck.GetTop()
        if dessus is None:
            return
        MettreEnReserve([dessus], joueur, effect)

    return [
        # Attaque et manigance de base, en une seule fabrique.
        AbilityFactory.WhenUnitWouldAttackOrThwart(
            AbilityType.Interrupt,
            "This",
            carte_du_dessus_en_reserve,
            is_basic_power=True,
        ),
        # La defense est le troisieme pouvoir de base, et passe par un autre
        # message.
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.Interrupt,
            "This",
            carte_du_dessus_en_reserve,
            is_basic_defense=True,
        ),
    ]
