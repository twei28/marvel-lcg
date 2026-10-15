from . import *

# Faking Death (x2) — EVENEMENT TREACHERY, cout 1 [mental]. Etoile rouge de boost.
# Hero Action: Shuffle this card into the encounter deck.
# When Revealed: Choose to either stun or confuse an enemy.
# ★ Boost: The activating enemy gets -2 SCH and -2 ATK for this activation.
#
# Cartes de reference :
#  - **`22005`** Evasive Maneuvering : « Stun an enemy » / « Confuse an enemy » en
#    `ChooseAbilities(ForChoiceAbility(...).SetTarget(Enemy, canbe_stunned=True))`.
#  - **`50117`** Psionic Force Field / **`08026`** Taskmaster : un Boost lit
#    `message.activating_enemy`, et `GainForThisActive(effect, message.being_message,
#    attack=, scheme=)` modifie les stats de CETTE activation seulement.
#  - **`sf009`** etc. pour `WhenThisRevealed` ; la melange est `MelangerDansLeDeckRencontre`
#    (helper du set). La carte jouee vient du deck rencontre : voir `Event.OnWhenCardRevealed`
#    (event.py), qui la defausse chez son PROPRIETAIRE une fois resolue.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Choose to EITHER stun OR confuse » : un seul des deux, au choix, sur UN ennemi.
#  - « The activating enemy » (Boost) : l'ennemi qui active, pas un ennemi au choix.
#  - « -2 SCH and -2 ATK for THIS activation » : temporaire ; SCH compte quand il
#    manigance, ATK quand il attaque (les deux sont poses, seul l'un sert).
#  - Qui choisit (When Revealed) : le texte ne le dit pas (contrairement a « The Lyja
#    player » des trois autres) : le joueur a qui la carte est revelee ; voir
#    defs/lyja_questions.md.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        # Chooser non precise : le joueur a qui la carte est revelee (regle generale).
        joueur = message.GetToPlayer()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Stun an enemy",
                lambda cibles: Faces.GiveStatus(cibles, "Stunned", effect),
            ).SetTarget(Enemy, canbe_stunned=True),
            AbilityFactory.ForChoiceAbility(
                "Confuse an enemy",
                lambda cibles: Faces.GiveStatus(cibles, "Confused", effect),
            ).SetTarget(Enemy, canbe_confused=True),
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        ennemi = message.activating_enemy
        if ennemi is not None:
            ennemi.GainForThisActive(effect, message.being_message, attack=-2, scheme=-2)

    return [
        MelangerDansLeDeckRencontre(),
        AbilityFactory.WhenThisRevealed(None, revelation),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
