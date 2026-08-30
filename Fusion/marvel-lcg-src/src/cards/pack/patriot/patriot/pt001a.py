from . import *

# * Patriot (face heros) — custom « CptScorp »
# PV 11 / ATQ 1 / CTR 1 / DEF 2 / MNG 5, trait YOUNG AVENGER.
#
# Will to Protect — Interrupt: When an ally you control would take
#   consequential damage, move that damage to Patriot. (Limit once per round.)
#
# ---------------------------------------------------------------------------
# CARTE DE REFERENCE : `dt009` Savior Complex (pack determination), qui
# imprime le MEME remplacement et l'ecrit exactement comme ceci :
# `Ability(AbilityType.<Interrupt>, Message.WhenAllyWouldTakeConsequentialDamage,
# [check_your_ally], operation)`, puis `message.SetBeInstead(effect)` suivi
# d'un `TakeDamage` sur le heros. `60007` Elektra (pack fne) porte le meme
# remplacement mais sur elle-meme (`is_local=True`), ce qui ne convient pas
# ici : la capacite ecoute TOUS les allies du controleur.
#
# ---------------------------------------------------------------------------
# « CONSEQUENTIAL DAMAGE » ET RIEN D'AUTRE
#
# Les degats consecutifs sont ceux que subit un allie a l'etoile (`1*`) apres
# avoir utilise un pouvoir de base ; ils sont envoyes par
# `Ally.take_consequential_damage` (card_type/ally.py:35-58) sous la forme
# d'un `Message.WhenAllyWouldTakeConsequentialDamage`. C'est le SEUL message
# ecoute ici : les degats d'ATTAQUE subis par un allie passent par
# `WhenUnitWouldTakeDamage` et ne declenchent RIEN. Coder l'un pour l'autre
# aurait fait de Patriot un paratonnerre universel, ce que la carte ne dit
# pas.
#
# ---------------------------------------------------------------------------
# « MOVE THAT DAMAGE » : LE DEGAT PART, IL N'EST PAS DUPLIQUE
#
# Lecon The Spot (mot-piege `instead` du PROCESSUS-CARTE §5) : un
# deplacement veut dire que la chose PART d'un endroit et ARRIVE ailleurs.
# `message.SetBeInstead(effect)` annule la partie « l'allie subit » (ally.py
# ligne 53 : `if would_take_consequential_message.is_be_instead: return`),
# et le `TakeDamage` qui suit la fait arriver sur Patriot. Sans le
# `SetBeInstead`, l'allie ET Patriot encaisseraient : deux fois le degat.
#
# Le brief evoquait `ChangeDealtToTarget` (Hercules `59008` Amadeus Cho) :
# cette methode-la vit sur `Message.WhenUnitWouldTakeDamage`
# (sender_damage.py:848) et n'existe PAS sur
# `WhenAllyWouldTakeConsequentialDamage`. Verifie avant d'ecrire une ligne,
# comme l'exige le guide. Le couple `SetBeInstead` + `TakeDamage` de dt009
# fait exactement la meme chose sur le bon message.
#
# ---------------------------------------------------------------------------
# GARDES
#
# - « an ally YOU CONTROL » : l'allie declencheur doit etre controle par le
#   joueur de Patriot. `Ally.GetControlByPlayer()` des deux cotes, comme
#   dt009. Sans cette garde, Patriot encaisserait pour l'allie du voisin.
# - Patriot doit pouvoir encaisser : la capacite vit sur la FACE HEROS, elle
#   n'existe donc pas en identite civile, mais on verifie quand meme que la
#   face est en jeu (une capacite peut etre resolue apres un changement
#   d'etat).
# - `.LimitOncePerRound()` : « (Limit once per round.) » imprime entre
#   parentheses. Un seul degat deplace par round, quel que soit le nombre
#   d'allies.
#
# ⚠ PAS de `SetTarget('Trigger')` ici : la capacite ne CIBLE rien, elle lit
# `message.trigger` directement (comme dt009). `SetTarget` n'est requis que
# lorsqu'un effet doit DESIGNER la carte d'une autre unite.
#
# Les valeurs ATQ 1 / CTR 1 / DEF 2 / REC (aucune, face heros) / MNG 5 et les
# 11 PV sont lues nativement dans `desc` : aucun module ne les recode.


def GetAbilities() -> Sequence['Ability']:

    def check_allie_du_joueur(effect: 'Effect', message: 'Message.WhenAllyWouldTakeConsequentialDamage') -> bool:
        this = effect.this.CastTo(Hero)
        allie = message.trigger.CastTo(Ally)
        return allie.GetControlByPlayer() == this.GetControlByPlayer()

    def will_to_protect(effect: 'Effect', message: 'Message.WhenAllyWouldTakeConsequentialDamage') -> None:
        this = effect.this.CastTo(Hero)
        if not this.IsInPlay():
            return

        degats = message.will_take_damage
        if degats <= 0:
            return

        # Le degat PART de l'allie...
        message.SetBeInstead(effect)
        # ... et ARRIVE sur Patriot.
        this.CastTo(Unit2).TakeDamage(this, degats, effect)

    return [
        Ability(
            AbilityType.Interrupt,
            Message.WhenAllyWouldTakeConsequentialDamage,
            [check_allie_du_joueur],
            will_to_protect,
        ).LimitOncePerRound(),
    ]
