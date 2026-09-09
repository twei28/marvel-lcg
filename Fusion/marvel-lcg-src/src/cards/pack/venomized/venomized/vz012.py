from . import *

# Forceful Bonding — EVENEMENT, cout X, RES [physical]. Aucun trait.
# Alter-Ego Action: Discard the top X cards of your deck. If any of those cards
#   is a SYMBIOTE or Venomized (black) card, change to your hero form.
#
# CARTES DE REFERENCE
#  - `14006` Speed Cyclone / `br005` Star Jump : le cout X, lu par
#    `effect.GetCostX()`.
#  - `gb010` Necro-Raven (maison) : `joueur.DiscardDeckTopCards(n, effect)`,
#    qui REND les faces defaussees — sans quoi on ne pourrait pas les relire.
#  - `Identity.ChangeToForm` (`identity.py:77`) : le changement de forme.
#
# TEXTE CONTRE CODE
#  ⚠ « Alter-Ego Action » : la carte n'existe qu'en forme civile, et son effet
#    est justement d'en sortir. Une Action de heros n'aurait aucun sens.
#  ⚠ « IF ANY of those cards » : UNE SEULE suffit, et le changement de forme
#    n'est pas repete. `any(...)`, pas une boucle.
#  ⚠ « SYMBIOTE OR Venomized (black) » : un OU entre un TRAIT et une CLASSE.
#    Meme lecture que vz029 Doctor Steven, d'ou les deux helpers du set.
#  ⚠ X = 0 : le texte ne l'interdit pas, mais rien n'est defausse donc rien ne
#    peut correspondre. On sort sans changer de forme.
def GetAbilities() -> Sequence['Ability']:

    def forceful_bonding(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        x = effect.GetCostX()
        if x <= 0:
            return

        defaussees = joueur.DiscardDeckTopCards(x, effect)
        if not any(PorteLeTraitSymbiote(c) or EstUneCarteVenomized(c) for c in defaussees):
            return

        identite = joueur.GetIdentity()
        identite.ChangeToForm(Hero, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            forceful_bonding
        ).SetPlay(),
    ]
