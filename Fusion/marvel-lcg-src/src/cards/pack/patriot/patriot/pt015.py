from . import *

# Throwing Stars — AMELIORATION signature, custom « CptScorp »
# Cout 1, ressource [physical], `MaxPerUnit "1"`, trait WEAPON.
#
# Attach to an ally. Max 1 per ally.
# Interrupt (attack): When the attached ally attacks, discard Throwing Stars
#   -> deal 3 damage divided as you choose. This attack gains piercing and
#   ranged.
#
# ---------------------------------------------------------------------------
# « ATTACH TO AN ALLY. MAX 1 PER ALLY. »
#
# `CanPlayThisUpgradeCard(Ally)` (modeles `01074`, `03031`, `12018`).
# `MaxPerUnit` est lu NATIVEMENT (`HasMaxPer.max_per_unit`, relu par
# `Asset2.CanAttachTo`, base/asset.py:69-73) : aucun module pour lui.
#
# ---------------------------------------------------------------------------
# DECLENCHEUR ET COUT
#
# `WhenUnitWouldAttack(AbilityType.Interrupt, "AttachedAlly", ...)` :
# `"AttachedAlly"` est la cible-chaine du moteur pour « le porteur de cet
# attachement, s'il est un allie » (condition/card_type.py:37 et 182). Modele
# du montage « attachement -> interruption sur l'attaque du porteur » :
# `04072` Laser Rifle, qui emploie `"AttachedVillain"` de la meme facon.
#
# ⚠ LE LIBELLE `(attack)` IMPRIME N'EST **PAS** POSE — CONTRAINTE DU MOTEUR
#
# Le scan imprime « Interrupt *(attack)* », mais `Ability.Initialize`
# (ability.py:196) n'autorise QUE les libelles `['defense', 'thwart']` sur un
# `AbilityType.Interrupt` ; `'attack'` y est reserve aux HeroAction, Action,
# HeroInterrupt, Response et HeroResponse. Un `.SetLabel('attack')` fait donc
# PLANTER le setup de la partie (AssertionError seche, trouvee par
# `verifier_tous_les_decks.py` le 30/08/2026 : « label='attack' ... [pt015] »).
#
# Deux issues, une seule acceptable :
#   - passer en `HeroInterrupt` ferait accepter le libelle, mais changerait la
#     REGLE : la carte ne partirait plus qu'en forme heros, alors que le texte
#     imprime « Interrupt » nu. REFUSE ;
#   - ne pas poser le libelle. Ecart PUREMENT TECHNIQUE, sans effet en jeu :
#     un libelle ne sert qu'a classer une capacite de JEU d'une carte jouee
#     depuis la main (« you cannot play attack events »), or celle-ci est une
#     interruption d'une amelioration DEJA EN JEU, jamais une capacite « Play ».
#     RETENU, et documente ici comme dans docs/patriot_cartes.md.
#
# LA FLECHE EST UN COUT -> UN EFFET : cout = « discard Throwing Stars » ->
# `CostFunc.Discard("This")`. Si la carte ne peut pas etre defaussee,
# l'interruption n'est pas proposee et l'attaque de l'allie se resout nue.
#
# ---------------------------------------------------------------------------
# « DEAL 3 DAMAGE **DIVIDED AS YOU CHOOSE** »
#
# Vraie repartition, pas 3 degats sur une seule cible. Le moteur la rend par
# le selecteur `repeat_rules="Health"` : la meme cible peut etre designee
# plusieurs fois, dans la limite de ses PV, et chaque designation vaut UN
# point (`DealDamage(targets, 1, effect)` sur la liste, les doublons comptant
# chacun — `FacesHelper.ListToDict`). Modeles : `15011` Wiccan (officielle,
# repartition depuis un handler via `ForChoiceAbility(...).SetTarget(Enemy,
# range=(1, n), repeat_rules="Health")`) et `13006` Wasp Sting (« a total of
# 4 damage divided among enemies you choose »).
#
# ⚠ Les doublons de `all_legal_targets` sont du SENS, pas du bruit (GUIDE
# §10) : un clic = une attribution, il en faut trois.
#
# CES 3 DEGATS NE SONT PAS UNE ATTAQUE : ils partent de l'amelioration
# (`this.DealDamage`, route vers l'identite du controleur), sans
# `AttackProperty`. Ils ne provoquent donc ni riposte, ni degats consecutifs
# pour l'allie, et ils s'AJOUTENT a l'attaque de l'allie, qui se resout
# normalement ensuite.
#
# ---------------------------------------------------------------------------
# « THIS ATTACK GAINS PIERCING AND RANGED »
#
# « This attack » = l'ATTAQUE DE L'ALLIE, celle qui vient de declencher
# l'interruption : c'est la seule attaque dans la phrase, et les 3 degats
# ci-dessus n'en sont pas une (on ne peut pas donner un mot-cle d'attaque a
# ce qui n'attaque pas). `message.GainPiercing(effect)` et
# `message.GainRanged(effect)` sur le `WhenUnitWouldAttack`
# (sender_damage.py:95 et 107). Modele des deux ensemble depuis un
# interrupt : `dt099` Marrow.
#
# ⚠ QUESTION OUVERTE, REMONTEE A L'UTILISATEUR : la carte pourrait aussi se
# lire « les 3 degats sont perces et a distance ». La lecture retenue est la
# lecture litterale (RAW), et c'est aussi la moins permissive des deux : elle
# ne fait pas ignorer les jetons Robuste ni les ripostes aux 3 degats. Tant
# que l'arbitrage n'est pas rendu, on reste sur la version severe.
#
# ⚠ RANGED IGNORE LA **RIPOSTE**, PAS LE GARDE. `can_retaliate.py:38` est le
# SEUL lecteur d'`IsRanged()` dans tout le moteur : un mot-cle Garde continue
# de forcer le choix de cible. Voir la fiche
# docs/reference/mots-cles/retaliate.md.
#
# PIERCING : ignore les jetons Robuste de la cible.


def GetAbilities() -> Sequence['Ability']:

    def throwing_stars(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)

        # « This attack gains piercing and ranged. » -> l'attaque de l'allie.
        message.GainPiercing(effect)
        message.GainRanged(effect)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        # « deal 3 damage divided as you choose »
        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 3 damage divided as you choose",
                lambda targets:
                    this.DealDamage(list(targets), 1, effect),
            ).SetTarget(Enemy, range=(1, 3), repeat_rules="Health"),
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(Ally),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.Interrupt,
            "AttachedAlly",
            throwing_stars,
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
