from . import *

# The Defenders — RESSOURCE [physical] variable, aspect Basic (Iron Fist 33).
# This card generates a [physical] resource for each DEFENDER character you control (to a maximum of 4) and can be
# spent for another player whose identity has the DEFENDER trait.
#
# MOTS-CLES : aucun. `desc.RES = "R"` est un repere : la carte n'imprime AUCUNE icone de ressource, c'est la capacite
# ci-dessous qui fixe ce qu'elle genere.
#
# CARTES DE REFERENCE
#  - `28019` Everyday Hero : « this card can be spent for any player » = `CheckThisCanDropPay(...).AnyPlayerCanDoThis()`
#    (la ressource se depense depuis la MAIN de son proprietaire pour le cout d'un autre joueur).
#  - `58006` Energy Siphon : ressource a quantite VARIABLE = deux fonctions, `DoDiscardThisToGenerateResources(
#    AbilityType.Interrupt, res_fn=...)` (ce qui est genere au paiement) et `CheckThisCanDropPay(...)` (ce qu'on annonce
#    avant de payer).
#
# TEXTE CONTRE CODE
#  ⚠ « for each DEFENDER character YOU control » : « vous » = le PROPRIETAIRE de la carte (celui qui la depense), pas le
#    joueur qui profite ; identite (forme courante) + allies, maximum 4 (une 5e ne donne rien de plus).
#  ⚠ « a [physical] resource » : du physique (R), jamais du wild ; sans Defender, la carte ne genere RIEN.
#  ⚠ « spent for ANOTHER player whose identity has the DEFENDER trait » : l'identite du joueur qui PAIE (pas du
#    proprietaire) ; le proprietaire, lui, la depense toujours pour lui-meme.


def DefenseursDuProprietaire(effect: 'Effect') -> int:
    proprietaire = effect.this.GetOwnerPlayer()
    nombre = sum(1 for personnage in proprietaire.GetControlCharacters() if personnage.HasTrait("DEFENDER"))
    return min(4, nombre)


def GetAbilities() -> Sequence['Ability']:

    def ressources(effect: 'Effect', message: 'Message2') -> 'Resources':
        Unused(message)
        nombre = DefenseursDuProprietaire(effect)
        return Resources('R' * nombre) if nombre > 0 else Resources('0')

    def pour_un_defender(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> bool:
        payeur = message.GetToPlayer()
        if payeur is None:
            return False
        if payeur == effect.this.GetOwnerPlayer():
            return True
        return payeur.GetIdentity().HasTrait("DEFENDER")

    return [
        AbilityFactory.DoDiscardThisToGenerateResources(AbilityType.Interrupt, res_fn=ressources),
        AbilityFactory.CheckThisCanDropPay(ressources, conditions=[pour_un_defender]).AnyPlayerCanDoThis(),
    ]
