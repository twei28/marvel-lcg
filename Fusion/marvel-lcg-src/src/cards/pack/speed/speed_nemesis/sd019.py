from . import *

# * Coat of Arms — SBIRE NEMESIS de Speed, custom « CptScorp »
# PV 4, ATQ 1*, MNG 2, 2 icones de bonus, Quickstrike 1, Nemesis « Thomas
# Shepherd », trait ANTI HERO.
# Quickstrike.
# [star] When Coat of Arms attacks, if it deals damage, deal 1 additional
#   damage to each character you control.
#
# ---------------------------------------------------------------------------
# `Quickstrike` N'EST PAS CODE ICI, et c'est volontaire. Le mot-cle est lu
# NATIVEMENT depuis `desc.Quickstrike` : `CanQuickstrike.ResolveQuickstrike`
# est appele par `Minion.OnEngagePlayer`. Coder l'attaque a la main serait une
# « capacite fantome » (fiche docs/reference/mots-cles/quickstrike.md, piege
# explicite). Ce fichier ne porte donc QUE la capacite etoilee.
#
# `ATK "1*"` : l'etoile d'une stat est lue nativement (`can_attack.py:48-52`,
# elle alimente `printed_attack_consequential_damage`, sans effet sur un
# sbire — seuls les ALLIES subissent des degats consecutifs). C'est la
# convention du depot pour un sbire nemesis a capacite etoilee : `58026` Grim
# Reaper (« ATK 2* »), `60061` Kingpin (« ATK 2* »). Rien a coder non plus.
#
# ---------------------------------------------------------------------------
# LA CAPACITE ETOILEE -> `AbilityFactory.AfterUnitAttackUnit(AbilityType
# .NonKeywordStar, "This", None, ..., dealt_damage=True)`
# (factory/do_attack.py:552).
#
# ARBITRAGE DE TIMING : le texte imprime dit « WHEN Coat of Arms attacks, IF
# IT DEALS DAMAGE ». Les deux moities sont incompatibles a la meme fenetre :
# « si elle inflige des degats » ne peut se savoir qu'APRES la resolution de
# l'attaque. On s'accroche donc a `AfterUnitAttackUnit` avec
# `dealt_damage=True` — la seule fenetre ou la condition imprimee est
# decidable. Modeles du meme genre : `58026` Grim Reaper (« After Grim Reaper
# attacks AND DEFEATS an ally ») et `47011` Chamber, tous deux sur une fenetre
# « After » pour une clause conditionnelle a la resolution.
#
# `dealt_damage=True` -> `check_dealt_damage` (do_attack.py:427) exige
# `message.dealt_damage > 0` : une attaque entierement defendue ou prevenue ne
# declenche rien, ce qui est le mot imprime.
#
# ---------------------------------------------------------------------------
# « DEAL 1 ADDITIONAL DAMAGE TO EACH CHARACTER YOU CONTROL » :
#
# - « YOU » = le joueur ATTAQUE (regle du jeu pour une carte rencontre : « you »
#   designe le joueur contre qui la carte agit). On le lit sur
#   `message.to_player`, pose par le constructeur du message depuis
#   `would_atk_message.property.against_player` (sender_damage.py:521). On
#   n'appelle PAS `message.GetToPlayer()` : cette methode contient un `assert
#   self.by_effect.this.paper.card_id == "44014"` en repli (sender_damage.py:535)
#   qui ferait planter la partie si `attacked_you` etait nul.
#
# - « EACH CHARACTER » = son IDENTITE ET SES ALLIES, y compris celui qui vient
#   d'encaisser l'attaque (rien ne l'exclut). L'identite d'abord, puis
#   `joueur.GetControlAllies()`.
#
# - CE N'EST PAS UNE ATTAQUE : `this.DealDamage(...)` sans `AttackProperty` et
#   hors de toute fenetre `WhenUnitWouldAttack`. Donc aucun re-declenchement
#   d'un effet « apres une attaque », aucune declaration de defenseur, aucune
#   riposte sur ces degats-la. C'est bien « deal 1 ADDITIONAL damage », un
#   supplement de l'attaque deja resolue.


def GetAbilities() -> Sequence['Ability']:

    def coat_of_arms(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Minion)

        joueur = message.to_player
        if not Player.IsType(joueur):
            return

        personnages: List['CardFace'] = []
        identite = joueur.GetIdentity()
        if identite is not None:
            personnages.append(identite)
        personnages += joueur.GetControlAllies()

        if not personnages:
            return

        this.DealDamage(personnages, 1, effect)

    return [
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.NonKeywordStar,
            "This",
            None,
            coat_of_arms,
            dealt_damage=True,
        ),
    ]
