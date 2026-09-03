from . import *

# * Enchantress — SBIRE nemesis (N 2/5). ASGARD. ELITE.
# MNG 3 / ATQ 2 / PV 5. 3 icones de boost.
# Forced Interrupt: When Enchantress is attacked, declare the engaged hero the
#   defender (without exhausting). If you cannot, cancel that attack and place
#   2 threat on the main scheme instead. (Limit once per phase.)
# (Lady Sif's nemesis minion.)
#
# Cartes de reference (le dossier de prepa n'en avait identifie AUCUNE ; le
# grep du 03/09/2026 en a rendu quatre) :
#  - **`48006` Bamf!** (pack ncrawler) : `message.DeclareDefender(hero,
#    effect)`, et son commentaire donne la definition officielle —
#    « declaring X the defender without exhausting encompasses the character
#    making a basic defense and using their DEF to reduce damage dealt » ;
#  - `56047` "I Can Do This All Day" pour la meme methode sur un evenement ;
#  - **`dd003` Doombot**, dont le commentaire pose la regle qu'on applique
#    ici : **`DeclareDefender` N'INCLINE PAS de lui-meme** (`32017` Mutant
#    Protectors appelle `Faces.ExhaustAll` juste avant, parce que SA carte
#    incline). Ne rien appeler, c'est tout le sens de « without exhausting » ;
#
# ⚠ LA FENETRE EST `WhenUnitWouldAttack`, PAS `WhenUnitBeingAttack`, et ces
# deux cas de test ont coute deux passes pour le voir :
#  1. `CancelThisAttack` n'est definie QUE sur `WhenUnitWouldAttack`
#     (sender_damage.py:181). L'appeler sur le message de `WhenUnitBeingAttack`
#     levait un `AttributeError` que le moteur AVALE : l'attaque passait, les
#     2 menaces ne tombaient pas, et RIEN dans le journal.
#  2. Meme en la reprenant sur `message.would_atk_message`, l'annulation
#     arrive TROP TARD depuis `WhenUnitBeingAttack` : les menaces tombaient
#     bien, mais Enchantress encaissait quand meme les degats.
# `WhenUnitWouldAttack` regle les deux, et c'est la fenetre qu'emploient les
# deux modeles de declaration de defenseur, `48006` Bamf! et `56047`. La cible
# se filtre par `attack_targets="This"`, non par le second parametre, qui
# designe l'ATTAQUANT.
#
# ⚠ ARBITRAGE DE L'UTILISATEUR (03/09/2026) — « **If you cannot** ».
# Trois lectures etaient possibles ; l'utilisateur a tranche pour **le test
# a posteriori** : on TENTE la declaration, puis on regarde si un defenseur a
# reellement ete pose (`message.defender`). Sinon, on annule et on pose les
# 2 menaces. Ce choix couvre :
#  - le cas principal, REELLEMENT atteignable : le joueur engage est en forme
#    ALTER-EGO et c'est un ALLIE qui frappe Enchantress — il n'y a alors
#    aucune face heros a declarer ;
#  - tout autre refus du moteur qu'on n'aurait pas su lister.
# C'est le contraire du piege `wd028`, ou un « If you cannot » testait un cas
# impossible et laissait la carte a moitie morte.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « the ENGAGED hero » : le heros du joueur avec lequel Enchantress est
#    engagee, pas l'attaquant. En solo c'est le meme ; a deux joueurs, un
#    allie d'un autre joueur peut la frapper, et c'est quand meme SON joueur
#    engage qui defend.
#  - « cancel that attack ... **instead** » : l'annulation REMPLACE la
#    declaration, elle ne s'y ajoute pas. Les deux branches sont exclusives.
#  - « (Limit once per phase.) » : une seule fois par phase, meme si le joueur
#    l'attaque trois fois.
#  - `Forced` : aucun choix pour le joueur.
#  - `ELITE` est un TRAIT, pas un mot-cle : il se declare dans `traits` et le
#    moteur ne lui associe aucune mecanique.


def GetAbilities() -> Sequence['Ability']:

    def enchantress(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)

        # ⚠ `Player.GetHero()` LEVE UN ASSERT si le joueur n'est pas en forme
        # de heros (player_get.py:208), et le moteur avale l'exception : la
        # capacite s'arretait alors AVANT le repli, l'attaque passait, et
        # aucune menace ne tombait. Constate au premier passage de la batterie
        # le 03/09/2026. On garde donc par `IsHero()`.
        joueur = this.GetEngagedPlayer()
        heros = joueur.GetHero() if (joueur is not None and joueur.IsHero()) else None

        if heros is not None:
            message.DeclareDefender(heros.CastTo(Unit2), effect)

        # « If you cannot » : on ne DEVINE pas les cas ou la declaration
        # echoue, on regarde si un defenseur a vraiment ete pose.
        if message.defender is None:
            message.CancelThisAttack(effect)
            this.PlaceThreatOnSchemes("MainScheme", 2, effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            None,
            enchantress,
            attack_targets="This",
        ).LimitOncePerPhase(),
    ]
