from . import *

# Upper West Side (U1) — LIEU Uptown (environnement LOCATION).
# Hero Interrupt: When a hero uses a basic power, choose to get either +1 or -1 to that power for this use. (Limit once per phase.)
#
# Cartes de reference : iron_man_model_42/im010 Rocket Boots (`WhenUnitUseBasicPower(HeroInterrupt, "You", op)` + `message.GainValue(1, effect)` : le bonus
# se pose sur le pouvoir EN COURS), pu031 / pu034 (capacite de lieu : `Ville.Occupe`, limite), `ChooseAbilities` + `ForChoiceAbility` (01084).
# ⚠ Mots-pieges :
#  - « a HERO uses a basic power » : ATK, THW, DEF d'un heros (forme heros) ; pas REC (alter-ego) ni un allie ;
#  - « a hero » = n'importe quel heros PRESENT dans ce lieu (R3 : on n'interagit qu'avec le lieu occupe), pas seulement celui qui occupe la carte en premier ;
#  - « choose to get either +1 OR -1 » : le JOUEUR du heros choisit, a l'usage ; pas facultatif une fois l'Interrupt declenche ; « to THAT power » : celui
#    en cours (`message.GainValue`), jamais un bonus durable ;
#  - « Limit once per PHASE » : `LimitOncePerPhase`, globale (une seule utilisation de la carte par phase, tous joueurs).

def GetAbilities() -> Sequence['Ability']:

    def present(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> bool:
        joueur = message.trigger.GetControlByPlayer()
        return joueur is not None and Ville.Occupe(effect, joueur, effect.this)

    def choisir(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        joueur = message.trigger.GetControlByPlayer()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("+1 to that power for this use", lambda cibles: message.GainValue(1, effect)),
            AbilityFactory.ForChoiceAbility("-1 to that power for this use", lambda cibles: message.GainValue(-1, effect)),
        )

    return [
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt, Hero, choisir, powers=["ATK", "THW", "DEF"], conditions=[present],
        ).LimitOncePerPhase(),
    ]
