from . import *

# Zenn-La — PLAYER ENVIRONMENT. PLANET. Setup. Pas de cout imprime (entre en
# jeu au Setup, modele pc002 Cosmic Surfboard : `desc` = {"Setup": "1"}, type
# `Support` + trait PLANET, aucun nouveau type de carte invente — lecon du
# 05/11/2026, voir docs/reference/mots-cles/environnement-joueur.md).
#
# Texte imprime :
#  « Arrive: Heal the arriving character 2. »
#  « Depart: Add +1 to the departing character's next basic power. »
#
# Regle de l'auteur (hors carte) : « During setup, start with Zenn-La and
# your Cosmic Surfboard in play. » — Zenn-La n'est PAS mele dans le planet
# deck (contrairement a Sakaar/Newhaven/Xandar/Ego, sans « Setup » imprime) :
# elle y entre directement, seule, au Setup.
#
# CARTES DE REFERENCE
#  - `AfterCharacterArrivePlanet`/`AfterCharacterDepartPlanet` (sender_player.py)
#    + helpers `ArriverA`/`Departir` (__init__.py du pack) : ces deux messages
#    portent `planet_face`, filtre ici par `effect.this == message.planet_face`
#    (PAS la fabrique `AbilityFactory.AfterCharacterArrivePlanet`, qui filtre
#    par PERSONNAGE arrivant, pas par planete — Ability() construite a la main).
#  - `av008` : `this.HealthUnits([cible], n, effect)` pour soigner.
#  - `dazed.py` (status, meme dossier que confused/stunned) : `WhenUnitUseBasicPower`
#    + `message.GainValue(delta, effect)` pour modifier un pouvoir de base.
#  - `cd006.py` (cloak_dagger, Pure Lightforce) : `carte.effect.RegisterTemp(...,
#    unregister_after_exec=True)` pour un bonus qui ne s'applique qu'UNE fois
#    puis disparait — modele du « next basic power ».
#
# TEXTE CONTRE CODE
#  « the ARRIVING/DEPARTING character » : `message.character_face`, jamais le
#    joueur ni Silver Surfer en dur — Zenn-La peut accueillir n'importe qui.
#  « Heal... 2 » : valeur fixe, pas liee aux degats presents (HealthUnits
#    plafonne de lui-meme a 0 s'il y a moins de 2 degats).
#  « the departing character's NEXT basic power » : UNE seule fois
#    (`unregister_after_exec=True`), n'importe lequel des quatre pouvoirs de
#    base (ATQ/CTR/DEF/MNG) — `powers=None` dans la fabrique, pas de filtre.
#  « +1 » : `message.GainValue(1, effect)`, jamais un degat ou une cible.


def GetAbilities() -> Sequence['Ability']:

    def ici(effect: 'Effect', message: 'Message.AfterCharacterArrivePlanet|Message.AfterCharacterDepartPlanet') -> bool:
        return effect.this == message.planet_face

    def arrivee(effect: 'Effect', message: 'Message.AfterCharacterArrivePlanet') -> None:
        effect.this.HealthUnits([message.character_face], 2, effect)

    def depart(effect: 'Effect', message: 'Message.AfterCharacterDepartPlanet') -> None:
        personnage = message.character_face

        def bonus(effect2: 'Effect', message2: 'Message.WhenUnitUseBasicPower') -> None:
            message2.GainValue(1, effect2)

        personnage.effect.RegisterTemp(
            AbilityFactory.WhenUnitUseBasicPower(
                AbilityType.Response,
                personnage,
                bonus,
            ),
            unregister_after_exec=True,
        )

    return [
        Ability(AbilityType.Response, Message.AfterCharacterArrivePlanet, [ici], arrivee),
        Ability(AbilityType.Response, Message.AfterCharacterDepartPlanet, [ici], depart),
    ]
