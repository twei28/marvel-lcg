from . import *

# * Dagger — custom « DesignHacker »
# Co-héroïne du pack physique, rendue en alliée signature unique (adaptation).
# Destructive Duo — Dagger gets +2 ATK while Cloak is in play.
# Bright Barrage — Hero Action (attack): Exhaust Dagger → deal damage equal to
#   her ATK divided among enemies as you choose.
#
# « Bright Barrage » est imprimée comme un modificateur de l'attaque de base ;
# le moteur ne sait pas répartir une attaque de base, l'action dédiée la
# remplace (montage Wasp Sting 13006 : deux variantes conditionnées, la
# répartition n'existant que quand l'ATK vaut 3).


def GetAbilities() -> Sequence['Ability']:

    def cloak_en_jeu(effect: 'Effect', ui: List['CardFace']) -> int:
        face = Worlds.FindCardOnField(
            effect,
            name=NOM_CLOAK,
            card_type=Hero,
        )
        if face:
            ui.append(face)
            return 1
        return 0

    def bright_barrage_repartie(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        this.DealDamage(effect.targets, 1, effect)

    def bright_barrage_simple(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        this.DealDamage(effect.targets, this.attack, effect)

    return [
        AbilityFactory.ThisGainKeyword(
            cloak_en_jeu,
            attack=2,
            change_on_event=OnEvent.CardInPlay(
                CardFinder(name=NOM_CLOAK, card_type=Hero)
            ),
        ).SetName("Destructive Duo"),
        # ATK 3 (duo) : jusqu'à 3 dégâts répartis, un par attribution.
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            bright_barrage_repartie,
            conditions=[
                lambda effect, message: CloakEstEnJeu(effect),
            ],
        ).SetName("Bright Barrage")
        .SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Enemy, range=(1, 3), repeat_rules="Health"),
        # ATK de base (solo) : une seule cible, dégâts = ATK courante.
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            bright_barrage_simple,
            conditions=[
                lambda effect, message: not CloakEstEnJeu(effect),
            ],
        ).SetName("Bright Barrage")
        .SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Enemy),
    ]
