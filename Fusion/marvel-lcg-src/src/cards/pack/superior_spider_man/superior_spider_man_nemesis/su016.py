from . import *

# * Hobgoblin — SBIRE nemesis. 6 PV, SCH 2, ATQ 1. Villainous. ELITE. GOBLIN.
# [star] Forced Response: After Hobgoblin attacks you, take 2 indirect damage.
# [star] Boost: Take 2 indirect damage.
#
# CARTES DE REFERENCE
#  - `al022` * Frogjolnir : « Forced Response: After <ennemi> attacks you, take
#    N indirect damage » = `AfterUnitAttackYou(ForcedResponse, "This", op)` +
#    `message.GetAgainstPlayer()` + `identite.TakeIndirectDamage(this, N, e)`.
#  - `an013`, `16140`, `ho015` : « [star] Boost: ... » =
#    `WhenCardBecomeBoost("This", op)`.
#
# TEXTE CONTRE CODE
#  ⚠ « attacks YOU » : le joueur ATTAQUE, lu sur le MESSAGE. Une carte de
#    rencontre n'a pas de controleur joueur (lecon `bl011` The Thirst), et
#    `AfterUnitAttackYou` garantit qu'un Hobgoblin frappant un AUTRE joueur ne
#    blesse pas celui-ci.
#  ⚠ La capacite Boost vise « YOU » aussi : sur une capacite Boost, « you »
#    designe LE JOUEUR QUI DEFEND, le moteur l'ecrit lui-meme
#    (sender_card.py:688). `message.GetToPlayer()` rend deja ce joueur.
#  ⚠ « Villainous » est une BASE AUTOMATIQUE (`desc.Villainous`) : aucun script.
#    C'est elle qui fait entrer Hobgoblin dans le champ du Spider-Sense de
#    `su001a` (« the villain OR A VILLAINOUS MINION »).
#  ⚠ L'etoile a cote de « 1 ATK » n'est pas une valeur : chez Rainy elle pointe
#    la statistique visee par la capacite etoile (ici l'attaque). Meme
#    convention que `bl013` Dracula et `sm015` Electro.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetAgainstPlayer()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            identite.TakeIndirectDamage(this, 2, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            identite.TakeIndirectDamage(this, 2, effect)

    return [
        AbilityFactory.AfterUnitAttackYou(
            AbilityType.ForcedResponse,
            "This",
            apres_attaque,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
