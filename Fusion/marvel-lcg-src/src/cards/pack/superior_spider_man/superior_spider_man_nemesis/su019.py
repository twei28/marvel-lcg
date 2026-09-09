from . import *

# Pumpkin Bombs — ATTACHEMENT nemesis. Boost 2. WEAPON.
# Attach to Hobgoblin. Otherwise attach to the villain.
# [star] Forced Response: After attached enemy attacks you, discard Pumpkin
#   Bombs and take 2 indirect damage.
# Hero Action: Spend [physical][physical] resources -> discard this card.
#
# CARTES DE REFERENCE
#  - `al022` * Frogjolnir : `AttachToFaceWhenPutIntoPlay(CardFinder(card_ids=
#    [...]), if_cannot_operation=)` et `AfterUnitAttackYou(ForcedResponse,
#    "AttachedMinion", op)`.
#  - `su018` Goblin Glider (meme set) pour la Hero Action a cout en ressources.
#
# TEXTE CONTRE CODE
#  ⚠⚠ « ATK ★ » IMPRIME, ET AUCUN BONUS D'ATTAQUE. La pastille ATQ de cette
#    carte porte une ETOILE et non un chiffre, la ou `su018` Goblin Glider
#    affiche « +1 ». **Arbitrage utilisateur du 08/09/2026 : aucun bonus
#    d'ATK.** L'etoile renvoie a la capacite etoile de la carte (« [star] Forced
#    Response: After attached enemy ATTACKS you »), exactement comme les petites
#    etoiles que Rainy pose a cote des statistiques sur Blade, Ares et
#    Spider-Man 2099 pour pointer la stat visee. `desc` ne porte donc PAS de
#    cle `ATK+`.
#  ⚠ « Attach to Hobgoblin. OTHERWISE attach to the villain » : deux cibles
#    dans l'ordre, pas un choix. Hobgoblin se retrouve par `card_ids`, jamais
#    par nom.
#  ⚠ « After ATTACHED ENEMY attacks you » : l'ennemi qui la porte, pas
#    n'importe lequel. `"AttachedEnemy"` et non `"AttachedMinion"` — la carte
#    peut etre sur le VILAIN.
#  ⚠ « DISCARD Pumpkin Bombs AND take 2 indirect damage » : les deux, et dans
#    cet ordre. La carte part toute seule apres une attaque : elle ne frappe
#    qu'UNE fois.
#  ⚠ « Spend [physical][physical] » : deux PHYSIQUES precises — `Cost("RR")`.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def sur_le_vilain(effect: 'Effect', joueur: 'Player') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(joueur)
        vilain = next((e for e in Worlds.GetOnFieldEnemies(effect)
                       if e is not None and Villain.IsType(e)), None)
        if vilain is not None:
            vilain.PlaceCardHere(this, True, effect)

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetAgainstPlayer()
        Faces.DiscardAll([this], effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            identite.TakeIndirectDamage(this, 2, effect)

    def se_defausser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(message)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_ids=[ID_HOBGOBLIN]),
            if_cannot_operation=sur_le_vilain,
        ),
        AbilityFactory.AfterUnitAttackYou(
            AbilityType.ForcedResponse,
            "AttachedEnemy",
            apres_attaque,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            se_defausser,
        ).SetName("Pumpkin Bombs")
        .SetCost(Cost("RR")),
    ]
