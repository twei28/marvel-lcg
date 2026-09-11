from . import *
# Hot as Hell — TRAITRISE nemesis, boost 2. INFERNAL. x2.
# When Revealed: Discard an upgrade you control. Take damage equal to that
#   card's resource cost.
#
# Modeles : 07058 Headbutt (`GetPrintedCost` -> degats), 31001a
# (`GetControlUpgrade(CardFinder(...))`), `AskChooseFaces` (le joueur choisit
# l'amelioration). Aucune amelioration : rien ne se passe. `GetIdentity()`
# et non `GetHero()` : en alter-ego, c'est Patsy qui encaisse.

def GetAbilities() -> Sequence['Ability']:

    def hot_as_hell(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        ameliorations = joueur.GetControlUpgrade(CardFinder(card_type=Upgrade))
        if not ameliorations:
            return
        choisies = list(joueur.AskChooseFaces(ameliorations, (1, 1), effect, prompt="Discard"))
        if not choisies:
            return
        cout = FacesCounter.GetPrintedCost(choisies)
        Faces.DiscardAll(choisies, effect)
        if cout > 0:
            joueur.GetIdentity().TakeDamage(this, cout, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            hot_as_hell,
        ),
    ]
