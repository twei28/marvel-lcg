from . import *

# Mallard Magic (1/2) — ATTACK. THWART — evenement, cout 3
# Hero Action: Choose:
# • Stun an enemy and deal 5 damage to it.
# • Confuse an enemy and remove 4 threat from a scheme.
#
# Exemplaire physique 1 de 2 (hd003 RES mental, hd004 RES energie : meme
# texte, deux card_id distincts — modele ok004/ok005).
#
# UNE SEULE ability `.SetPlay()`, les deux branches etant offertes par
# `initiator.ChooseAbilities` a la resolution (modele ok019 Funeral Rites /
# ok004 Adored Ones). C'est OBLIGATOIRE ici : `game/card/factory.py:95-121`
# n'accepte qu'un `play_count == 1` par evenement, sauf liste blanche codee en
# dur — deux `.SetPlay()` feraient PLANTER la creation de partie du heros.
#
# Branche 1 : « an enemy » puis « deal 5 damage to IT » — LA MEME cible
# (piege `that <nom>` du tableau) : un seul `SetTarget(Enemy)`, reutilise pour
# le statut ET les degats. `Faces.GiveStatus(targets, "Stunned", effect)`
# (modele core/spider_man/32008.py Steel Fist).
# Branche 2 : deux cibles INDEPENDANTES (un ennemi a desorienter, une
# manigance a nettoyer). `ForChoiceAbility` n'expose pas `effect.targets2` a
# son handler : la seconde cible passe par un `ChooseAbilities` imbrique
# (modele ok008 Spear Thrust, qui enchaine deja des choix de cible dans son
# handler).


def GetAbilities() -> Sequence['Ability']:

    def mallard_magic(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        def sonner_et_frapper(targets: Sequence['CardFace']) -> None:
            if not targets:
                return
            Faces.GiveStatus(targets, "Stunned", effect)
            this.DealDamage(targets, 5, effect)

        def desorienter_et_nettoyer(targets: Sequence['CardFace']) -> None:
            if targets:
                Faces.GiveStatus(targets, "Confused", effect)

            def retirer(schemes: Sequence['CardFace']) -> None:
                if schemes:
                    this.RemoveThreatFromSchemes(schemes, 4, effect)

            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove 4 threat from a scheme",
                    retirer,
                ).SetLabel('thwart').SetTarget(Scheme2),
            )

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Stun an enemy and deal 5 damage to it",
                sonner_et_frapper,
            ).SetLabel('attack').SetTarget(Enemy, canbe_stunned=True),
            AbilityFactory.ForChoiceAbility(
                "Confuse an enemy and remove 4 threat from a scheme",
                desorienter_et_nettoyer,
            ).SetLabel('thwart').SetTarget(Enemy, canbe_confused=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            mallard_magic,
        ).SetPlay().SetLabel(),
    ]
