from . import *

# Covered Fire — EVENEMENT signature, custom « CptScorp »
# Cout 1, ressource [energy], trait DEFENSE. Deux exemplaires physiques :
# pt005 et pt006, meme texte, meme code.
#
# Hero Interrupt (defense): When your hero defends against an attack, choose
#   an ally you control -> deal damage to an enemy equal to that ally's ATK
#   value or remove threat from a scheme equal to that ally's THW value.
#
# ---------------------------------------------------------------------------
# CARTE DE REFERENCE : `09015` Desperate Defense pour le declencheur
# (`WhenUnitDefendAgainstAttack(AbilityType.HeroInterrupt, "YourHero", ...)`
# `.SetPlay().SetLabel('defense')`) ; `60044` Choreography pour le « ou »
# rendu par un `player.ChooseAbilities` a deux branches, chacune portant sa
# propre cible.
#
# ---------------------------------------------------------------------------
# ⚠ NE PAS COPIER pt003 SUR pt005 : L'ALLIE EST **CHOISI**, PAS EPUISE
#
# Aided Defense (pt003/pt004) dit « EXHAUST an ally you control » : c'est un
# `CostFunc.Exhaust`. Covered Fire dit « CHOOSE an ally you control » :
# l'allie n'est PAS incline, il est seulement designe. Le cout de la fleche
# est donc la DESIGNATION elle-meme, rendue par un `.SetTarget("YourAlly",
# range=(1, 1))` porte par la capacite : quand le joueur ne controle aucun
# allie, le selecteur n'a aucune cible legale, `CanPlayBy` rend False et la
# carte reste en main. Cout impayable = rien ne se passe, sans une ligne de
# garde.
#
# Corollaire pratique : un allie DEJA INCLINE (qui vient de defendre, par
# exemple) reste un choix legal. C'est la lettre de la carte.
#
# ---------------------------------------------------------------------------
# « THAT ALLY'S ATK / THW VALUE » : LES VALEURS COURANTES
#
# `allie.attack` et `allie.thwart` sont les valeurs COURANTES, bonus compris
# (Inspired, Commander's Orders...), pas les valeurs imprimees
# (`printed_attack` / `printed_thwart`). C'est ce que dit la carte.
#
# ⚠ CE N'EST PAS UNE ATTAQUE DE L'ALLIE. Les degats partent de l'EVENEMENT
# (`this.DealDamage`, qui route vers l'identite via
# `Event`/`CardPlayer.OnDealDamage`), sans `AttackProperty` : donc pas de
# degats consecutifs pour l'allie, pas de riposte de l'ennemi, pas de
# declenchement des « apres une attaque ». Meme chose pour le retrait de
# menace, qui n'est pas un contre (`RemoveThreatFromSchemes`, la meme brique
# que `10004` Sub-Orbital Leap).
#
# Une valeur de 0 (Hawkingbird a ATQ 0) laisse la branche sans effet : c'est
# la lettre de la carte, on ne l'interdit pas.


def GetAbilities() -> Sequence['Ability']:

    def covered_fire(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None or not effect.targets:
            return

        allie = effect.targets[0].CastTo(Ally)
        atk = allie.attack
        thw = allie.thwart

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                f"Deal {atk} damage to an enemy (that ally's ATK)",
                lambda targets:
                    this.DealDamage(list(targets), atk, effect),
            ).SetTarget(Enemy, range=(1, 1)),
            AbilityFactory.ForChoiceAbility(
                f"Remove {thw} threat from a scheme (that ally's THW)",
                lambda targets:
                    this.RemoveThreatFromSchemes(list(targets), thw, effect),
            ).SetTarget(Scheme2, range=(1, 1)),
        )

    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.HeroInterrupt,
            "YourHero",
            covered_fire,
        ).SetPlay()
        .SetLabel('defense')
        .SetTarget("YourAlly", range=(1, 1)),
    ]
