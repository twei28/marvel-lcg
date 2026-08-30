from . import *

# Forced Contract — TREACHERY
# Surge.
# When Revealed: The ally with highest ATK takes damage equal to Scarlet
#   Spider's ATK. If there is no ally in play, you take 2 damage.
# [star] Boost: Each friendly character takes 1 damage.
#
# Surge : mot-cle purement declaratif (`desc.Surge`, deja dans cards.json),
# aucun code. "The ally with highest ATK" : modele th015 Friendly Fire
# (`max(x.attack for x in ...)`), applique ici a `player.allies.Get()`
# (modele okoye/okoye/__init__.py, `joueur.allies.Get()`) plutot qu'a tous
# les personnages amis. "Scarlet Spider's ATK" : la face Heros precisement,
# quelle que soit la forme ACTUELLE du joueur (une Treachery se revele sans
# egard a la forme). `player.GetHero()` suppose la forme heros active
# (assertion, `player_get.py:203-208`) -- CORRECTIF : lecture directe parmi
# `player.GetAllIdentityFace()` (les deux faces, quelle que soit celle
# active) filtree par `Hero.IsType`. L'ATK +1 fixe de ss016 (Stings of
# Kaine) s'y applique deja en continu si la carte est en jeu. Boost "each
# friendly character takes 1 damage" : modele officiel exact core/01154.py
# (Concussive Blast), `player.GetControlCharacters()`.
#
# CORRECTIF : `.attack` sur la face Heros quand elle N'EST PAS la face
# active rend 0 (les stats effectives ne se calculent que pour la face
# EN JEU), constate en jeu reel (identite civile au moment de la
# revelation). `printed_attack` (valeur imprimee, 2) est utilise a la
# place : robuste quelle que soit la forme active du joueur au moment ou
# la traitrise est revelee (une Treachery se revele sans egard a la forme).


def GetAbilities() -> Sequence['Ability']:

    def forced_contract_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()

        allies = list(player.allies.Get())
        if not allies:
            this.DealDamage([player.GetIdentity()], 2, effect)
            return

        cible = max(allies, key=lambda a: a.attack)
        hero_face = next((f for f in player.GetAllIdentityFace() if Hero.IsType(f)), None)
        valeur = hero_face.printed_attack if hero_face else 0
        this.DealDamage([cible], valeur, effect)

    def forced_contract_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()

        units = player.GetControlCharacters()
        this.DealDamage(units, 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            forced_contract_revealed,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            forced_contract_boost,
        ),
    ]
