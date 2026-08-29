from . import *

# War Drumming (1/2) — trahison nemesis d'Okoye
# When Revealed (Alter-Ego): This card gains surge.
# When Revealed (Hero): Choose a minion in play. That minion attacks you. If
#   the attacking enemy's ATK is 2 or less, it gains villainous for this
#   attack. If its ATK is 3 or more, it gains overkill for this attack. If
#   there are no minions in play, this card gains surge.
#
# Modele exact : core/rhino/01106.py (Stampede), meme structure
# `AbilityFactory.WhenThisRevealed("Alter-Ego"|"Hero", ...)`, branche
# alter-ego = `ThisCardGainSurge` tel quel. Branche heros : choix du sbire
# (modele kb008, `MayChooseOneText` si plusieurs candidats), puis
# `minion.DoAttackYou(joueur, effect, property=...)` (enemy.py:74, generique
# a TOUT Enemy, pas seulement Villain -- verifie sur Stampede qui l'utilise
# deja pour Rhino).
#
# ECART ASSUME (branche ATK<=2, "gains villainous for this attack") : dans ce
# moteur, "Villainous" n'est PAS une propriete d'attaque temporaire mais un
# mot-cle statique de carte (`desc.Villainous`, "quand ce sbire s'active,
# donne-lui une carte boost" -- verifie sur des dizaines de cartes imprimees,
# ex. gmw/16055 Blackjack O'Hare). Aucun crochet du moteur ne permet
# d'accorder CE mot-cle pour une seule attaque generee hors activation
# normale (contrairement a overkill/piercing/ranged, geres par
# `AttackProperty`). Cette branche reste donc SANS effet code au-dela de
# l'attaque elle-meme -- seul le texte imprime la porte, comme la clause
# "cannot place arrow counters" de kb003.


def GetAbilities() -> Sequence['Ability']:

    def war_drumming_hero(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur is None:
            return

        minions = Worlds.GetOnFieldMinions(effect)
        if not minions:
            ThisCardGainSurge(effect, message)
            return

        cible = minions[0] if len(minions) == 1 else joueur.MayChooseOneText(minions)
        if cible is None:
            return

        gagne_overkill = cible.attack >= 3
        cible.CastTo(Enemy).DoAttackYou(
            joueur, effect,
            property=AttackProperty(overkill=True) if gagne_overkill else None,
        )

    return [
        AbilityFactory.WhenThisRevealed(
            "Hero",
            war_drumming_hero,
        ),
        AbilityFactory.WhenThisRevealed(
            "Alter-Ego",
            ThisCardGainSurge,
        ),
    ]
