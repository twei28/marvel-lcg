from . import *

# Zombie Hawkeye — METAZOMBIE (Fallen Heroes, modulaire). AVENGER. SCH 1. ATK 2. HP 5.
# Guard.
# When Revealed: Deal 2 damage to each ally you control.
#
# Cartes de reference :
#  - « Guard » (mots-cles/guard.md) : cle native `desc.Guard`, aucun script -- meme statut que hg059.
#  - « When Revealed: Deal 2 damage to each ally you control » : `AbilityFactory.WhenThisRevealed(None,
#    op)` sur `Message.WhenCardRevealed`, modele EXACT `01103` * Shocker (« When Revealed: deal 1 damage to
#    each hero » -> `this.DealDamage(Worlds.GetOnFieldHeroes(effect), 1, effect)`), croise avec le filtrage
#    sur « each ally you control » de `24044` Boomerang (« deal 1 damage to each ally you control » ->
#    `this.DealDamage(player.GetControlAllies(), 1, effect)`, ou `player = message.GetToPlayer()`). Les deux
#    cartes utilisent la MEME methode native `this.DealDamage(cibles, N, effect)` sur le Minion revele
#    (`effect.this.CastTo(Minion)`), seule la liste de cibles differe (heros vs allies-du-joueur-vise).
#
# ⚠ Mots-pieges :
#  - « EACH ALLY YOU CONTROL » : le JOUEUR auquel la carte est revelee (`message.GetToPlayer()`), jamais
#    tous les allies de la table ni un joueur fixe par le code -- meme piege que `hg012` Zombie Thor
#    (« each ally THAT PLAYER controls ») transpose a un When Revealed de Minion plutot qu'a une
#    activation de Villain.
#  - « deal 2 damage », SANS lien avec une attaque : degats DIRECTS (`CardFace.DealDamage`, hors
#    `can_attack.py`), insensibles a Toughness-par-defense ni a une reduction d'attaque -- mais PAS
#    insensibles au statut Tough lui-meme (Tough absorbe TOUS les degats, attaque ou non, cf.
#    mots-cles/toughness.md) ni a `IsIgnoreKeyword`. Aucune garde supplementaire a coder : coherent avec
#    `01103`/`24044`, qui n'en codent pas non plus.
#  - « deal 2 damage », SANS condition sur le nombre d'allies : liste vide (joueur sans allie) ne fait rien
#    (natif), plusieurs allies recoivent CHACUN 2 degats separement (pas un partage), comme `24044`.
#  - Un seul declencheur imprime (pas de forme Alter-Ego / Hero distincte comme `tk022`/`tk026`) : un seul
#    `AbilityFactory.WhenThisRevealed(None, ...)`, pas de branche sur la forme du joueur vise (un Minion
#    revele de la meme facon quelle que soit la forme des joueurs).
#  - Trait METAZOMBIE porte par un Minion (pas par un Villain comme le Horde deck) : meme remarque que
#    hg059, sans consequence sur CETTE capacite (qui ne cherche aucun autre Metazombie).
#
# Bloc nombres texte <-> code : SCH 1 / ATK 2 / HP 5 / Guard 1 -> `desc` ; « 2 damage » -> litteral `2`
# passe a `this.DealDamage(..., 2, effect)`, seule valeur numerique du script, identique au texte imprime.


def GetAbilities() -> Sequence['Ability']:

    def hawkeye(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetToPlayer()
        this.DealDamage(joueur.GetControlAllies(), 2, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            hawkeye,
        ),
    ]
