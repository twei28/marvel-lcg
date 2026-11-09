from . import *

# * Famished Power — pacte BARGAIN (Corruptive Offers). Boost 3, Peril (natifs). Communs : `AbilitesDePacteCorrompu`.
# Interrupt : When you use a basic power, place 1 corrupt counter here -> combine the values of 2 basic powers of your hero for this use.
#
# LECTURE (tranchee par l'utilisateur le 09/11, carte montree) : on choisit DEUX pouvoirs de base du heros (ATK, THW, DEF) et LEUR SOMME REMPLACE la
# valeur du pouvoir utilise pour CETTE utilisation (le pouvoir utilise n'est pas forcement l'un des deux). Forme heros seulement (« of your hero »).
# Cartes de reference : mantis/mt001b (`WhenUnitUseBasicPower(.., powers=[..])`), sender_unit `message.GainValue` (redirige vers ATK/THW/DEF/REC de CETTE utilisation).
# ⚠ Mots-pieges : « WHEN you use » (interruption, avant le calcul) ; le compteur corrupt est pose une fois par utilisation ; la valeur s'ajoute seulement pour CETTE utilisation.


def GetAbilities() -> Sequence['Ability']:
    def en_forme_heros(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> bool:
        return Hero.IsType(message.trigger) and message.power in ("ATK", "THW", "DEF")

    def combine(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Attachment)
        heros = message.trigger
        joueur = heros.GetControlByPlayer()
        valeurs = {"ATK": heros.attack, "THW": heros.thwart, "DEF": heros.defense}
        paires = [("ATK", "THW"), ("ATK", "DEF"), ("THW", "DEF")]
        Faces.PlaceCountersOn([this], 1, 'corrupt', effect)
        # La somme REMPLACE la valeur : `GainValue` ajoute, on ajoute donc l'ecart (negatif si la paire vaut moins que le pouvoir utilise).
        joueur.ChooseAbilities(
            effect,
            *[AbilityFactory.ForChoiceAbility(
                f"Combine {a} and {b} ({valeurs[a] + valeurs[b]})",
                lambda targets, a=a, b=b: message.GainValue(valeurs[a] + valeurs[b] - valeurs[message.power], effect))
              for a, b in paires],
        )

    return [
        *AbilitesDePacteCorrompu(),
        AbilityFactory.WhenUnitUseBasicPower(AbilityType.Interrupt, "You", combine, powers=["ATK", "THW", "DEF"], conditions=[en_forme_heros]),
    ]
