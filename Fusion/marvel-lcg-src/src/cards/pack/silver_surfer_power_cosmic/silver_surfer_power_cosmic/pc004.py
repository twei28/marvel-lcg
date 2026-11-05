from . import *

# * Nova Frankie Raye — ALLY. POWER COSMIC. COSMIC. Cout 3, THW 1, ATK 1, HP 5.
#
# Texte imprime : « Action: Choose a planet. I arrive at that PLANET, then
# depart. At the end of the phase, deal 1 damage to me. (Limit once per
# phase.) »
#
# Regle du pack (CLAUDE.md) : « I »/« me » designe la carte elle-meme — ici
# Frankie Raye, PAS Silver Surfer. Les cartes « After Silver Surfer departs a
# PLANET » (Cosmic Blast, Lightspeed Entrance...) ne reagissent donc PAS a ce
# depart-ci (elles filtrent sur le personnage, voir pc00X a venir).
#
# CARTES DE REFERENCE
#  - `pc002` Cosmic Surfboard : meme cible « choose a PLANET »
#    (`.SetTarget(card_type=Support, trait="PLANET")`), meme helpers
#    `ArriverA`/`Departir` (__init__.py du pack).
#  - `61003` Jessica Jones : `this.DealDamage([this], 1, effect)`, modele
#    du dégât à soi-même.
#  - `AbilityFactory.WhenPhaseEnd(ability_type, None, operation)`
#    (turn_phase.py) + `carte.effect.RegisterTemp(..., unregister_after_exec=
#    True)` (modele `cd006.py`) : le degat n'arrive qu'A LA FIN DE CETTE
#    phase-ci, une seule fois, pas a chaque fin de phase pour toujours.
#
# TEXTE CONTRE CODE
#  « I arrive... THEN depart » : pas un aller simple -- `ArriverA` puis
#    `Departir` dans la MEME resolution, immediatement (aucune carte du pack
#    ne reagit entre les deux ici, donc l'ordre n'est observable que par les
#    cartes qui testent specifiquement cette arrivee/ce depart).
#  « At the end of the PHASE » : la phase EN COURS au moment ou l'action est
#    jouee, pas le round -- `WhenPhaseEnd(None)` capte la toute prochaine fin
#    de phase, qui est forcement celle-ci (une Action se joue dans une phase
#    en cours).
#  « (Limit once per phase) » : porte sur l'ACTION elle-meme (combien de fois
#    on peut l'utiliser), pas sur le degat -- `.LimitOncePerPhase()`.


def GetAbilities() -> Sequence['Ability']:

    def voyager(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        if not effect.targets:
            return
        this = effect.this.CastTo(Ally)
        planete = effect.targets[0]

        ArriverA(effect, this, planete)
        Departir(effect, this)

        def degat_de_fin_de_phase(effect2: 'Effect', message2: 'Message.WhenPhaseEnd') -> None:
            this.DealDamage([this], 1, effect2)

        this.effect.RegisterTemp(
            AbilityFactory.WhenPhaseEnd(
                AbilityType.Response,
                None,
                degat_de_fin_de_phase,
            ),
            unregister_after_exec=True,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            voyager,
        ).SetTarget(card_type=Support, trait="PLANET")
        .LimitOncePerPhase()
        .SetName("Choisir une planète"),
    ]
