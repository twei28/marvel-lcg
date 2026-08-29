from . import *

# * Hawkeye (Kate Bishop)
# Master Archer — Interrupt (attack): When an enemy initiates an attack,
#   remove up to 3 arrow counters from Kate's Bow -> deal 1 damage to that
#   enemy for each arrow counter removed.
#
# Le plafond n'est PAS un `CostFunc.Counter("This", (0, 3), 'arrow')` : Kate's
# Quiver (kb013) le fait passer a 5 tant qu'il est en jeu, et `CostFunc.Counter`
# fige sa taille a la construction de l'ability (`GetAbilities()` n'est pas
# re-evalue par carte en jeu). Le choix « combien de compteurs retirer » est
# donc fait a la main via `player.DeclareNumber`, modele `CostFunc.Counter`
# lui-meme (cost_func.py:836) pour la logique min/max.
#
# Modele du declencheur : Powerful Punch (mut_gen/32014.py), Interrupt sur
# `WhenUnitWouldAttack`.
#
# CORRECTIF DE DONNEES MAJEUR (test de comportement, 29/8/2026) : TOUT le pack
# kate_bishop etait inerte. `CardsDB.FindAbilities` (cards/database.py) resout
# le module Python d'une carte via `cards.pack.{pack}.{CleanName(set_name)}.
# {card_id}` (repli sans set_name si vide) -- JAMAIS via le nom de dossier
# directement. Le `set_name` imprime dans data/cards.json valait "Hawkeye"
# (signatures) / "Hawkeye Nemesis" (nemesis) / "" (kb015), qui donnent apres
# nettoyage "hawkeye" / "hawkeye_nemesis" / rien -- alors que les fichiers
# vivent sous kate_bishop/kate_bishop/ et kate_bishop/kate_bishop_nemesis/.
# AUCUNE des routes tentees ne correspondait : `importlib.import_module`
# echouait en silence (`except: pass`), `GetAbilities()` n'etait JAMAIS
# appelee pour AUCUNE des 21 cartes, et `ability_cache` restait a `[]` --
# sans la moindre exception ni message d'erreur (confirme par sonde : ni
# `GetAbilities()` ni `master_archer()` n'etaient jamais executes). Modele de
# la convention correcte : pack "brawn", set_name "Brawn" / "Brawn Nemesis",
# dossiers brawn/brawn/ et brawn/brawn_nemesis/. Corrige en alignant
# `set_name` sur "Kate Bishop" / "Kate Bishop Nemesis" pour les 21 cartes
# (data/cards.json), qui nettoye exactement vers les dossiers reels.
#
# Second correctif, sur CETTE carte precisement, une fois le module enfin
# charge : `.SetTarget("Trigger")` reste sans effet observable sur une
# capacite PASSIVE (pas de `.SetPlay()`) -- le mecanisme de ciblage qu'il
# active suppose la resolution de jeu d'un evenement joue depuis la main.
# Modele corrige : Invisible Barrier (invisible_woman/iw001c.py), meme
# structure passive (`AbilityType.Interrupt`, ni Play ni CostFunc), qui lit
# l'attaquant directement via `message.attacker` au lieu de `.SetTarget()` +
# `effect.targets`, et `WhenUnitAttackYou` (raccourci de `WhenUnitWouldAttack`
# avec `against_player="You"`) pour restreindre aux attaques subies par Kate,
# pas n'importe quel joueur en partie a plusieurs.


def GetAbilities() -> Sequence['Ability']:

    def master_archer(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Hero)
        player = effect.GetInitiator()
        if player is None:
            return

        arc = TrouverArcEnJeu(effect)
        if arc is None:
            return

        plafond = 5 if Worlds.FindCardOnField(effect, name=NOM_CARQUOIS) else 3
        max_possible = min(plafond, arc.GetCounters('arrow'))
        if max_possible <= 0:
            return

        nombre = player.DeclareNumber(0, max_possible)
        if nombre <= 0:
            return

        Faces.RemoveCountersOn([arc], nombre, 'arrow', effect)
        this.DealDamage([message.attacker], nombre, effect)

    return [
        AbilityFactory.WhenUnitAttackYou(
            AbilityType.Interrupt,
            Enemy,
            master_archer,
        ).SetName("Master Archer"),
    ]
