from . import *

# * Slash — ALLIE 2 [energy], ATK 3 (1), THW 0 (1), PV 5. MUTANIMAL. TURTLE. (TMNT Starter, Inkwire)
# Forced Response: After Slash enters play, take 3 damage.
#
# CARTES DE REFERENCE
#  - `01083` * Mockingbird : « After X enters play » = `AfterCardEnterPlay(..., "This", ...)`.
#  - `27166` / `27083` : « take N damage » (le joueur) = `joueur.GetIdentity().TakeDamage(this, N, effect)`.
# TEXTE CONTRE CODE
#  ⚠ « take 3 damage » sans sujet : lecture codee = VOUS (votre identite), convention des cartes joueur
#    (Blood Rage, Rampage). ⚠ Question Q-UA2 (aspects-aggression-questions.md) : Slash lui-meme (5 PV -> 2) ?
#    Carte NON terminee tant que la reponse n'est pas rendue.
#  ⚠ « Forced » : obligatoire. Homonyme de `tm002` * Slash (pack michelangelo) : meme titre, unicite partagee.


def GetAbilities() -> Sequence['Ability']:

    def slash(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        joueur = this.GetControlByOrOwner()
        if Player.IsType(joueur):
            joueur.GetIdentity().TakeDamage(this, 3, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            slash,
        ),
    ]
