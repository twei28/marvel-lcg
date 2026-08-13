from . import *

# * Darkhawk

def GetAbilities() -> Sequence['Ability']:

    # Le moteur ne sait pas poser un pion SUR une statistique. Mais le pion n'est
    # qu'un marqueur : ce qui compte est QUEL pouvoir recoit le +2. On garde donc
    # le pion sur la carte (pour l'affichage et pour « Uses ») et le pouvoir vise
    # sur la face, ou l'Action le deplace. Les deux gains sont poses, chacun
    # conditionne par le pouvoir courant : un seul est actif a la fois.
    def pouvoir_vise(face: 'CardFace') -> str:
        return getattr(face, "pouvoir_configuration", "ATK")

    def sur_atk(effect: 'Effect', ui: List['CardFace']) -> int:
        this = effect.this.CastTo(Ally)
        return 1 if (this.GetCounters('configuration') > 0
                     and pouvoir_vise(this) == "ATK") else 0

    def sur_thw(effect: 'Effect', ui: List['CardFace']) -> int:
        this = effect.this.CastTo(Ally)
        return 1 if (this.GetCounters('configuration') > 0
                     and pouvoir_vise(this) == "THW") else 0

    def deplacer_le_pion(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        # « son AUTRE pouvoir de base » : le deplacement bascule, il ne demande
        # pas de choisir.
        this.pouvoir_configuration = "THW" if pouvoir_vise(this) == "ATK" else "ATK"
        # Le pion est retire puis repose : c'est ce qui reveille les deux gains,
        # qui ecoutent le compteur.
        this.SetCounters(0, 'configuration', effect)
        this.SetCounters(1, 'configuration', effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(1, 'configuration'),
        AbilityFactory.ThisGainKeyword(
            sur_atk,
            attack=2,
            change_on_event=OnEvent.Counter("This", 'configuration'),
        ),
        AbilityFactory.ThisGainKeyword(
            sur_thw,
            thwart=2,
            change_on_event=OnEvent.Counter("This", 'configuration'),
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            deplacer_le_pion
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
