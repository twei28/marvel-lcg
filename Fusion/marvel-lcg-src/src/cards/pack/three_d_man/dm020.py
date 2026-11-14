from . import *

# Prevent Disaster (Event, DEFENSE)
#
# Hero Interrupt (defense): When a boost card with [boost][boost][boost] is revealed during an enemy activation,
#   cancel that activation and ignore any "Boost" ability. Draw 1 card.
#
# CARTES DE REFERENCE
#  - `hc010` Outer Demons (Hellcat) : `AbilityFactory.WhenBoostCardTurnedFaceUp(Interrupt, "Ability", op,
#    boost_for_card=...)` + `message.CancelBoostAbility(effect)` -> "ignore any 'Boost' ability".
#  - `boost.py:241` `WhenBoostCardTurnedFaceUp` : `activate_target` filtre "against you" (ici la carte est en
#    defense : seulement quand l'activation vise LE JOUEUR), `while_attack=True` filtre une ATTAQUE (pas une
#    manigance), `message.boost_icons` = le nombre d'icones de boost actuellement affichees sur la carte revelee.
#  - `can_attack.py:219` : `would_atk_message.is_be_instead` n'est relu qu'UNE FOIS, juste apres l'envoi de
#    `WhenUnitWouldAttack`, bien AVANT que les cartes de boost soient donnees puis retournees (ligne 297 puis
#    373). Poser `message.would_message.SetBeInstead(effect)` depuis cette fenetre (verifie le 04/11/2026, cas
#    reel joue : les degats tombaient quand meme) arrive donc trop tard pour empecher quoi que ce soit --
#    CONTRAIREMENT a `27006` Web Binding, qui annule depuis `WhenEnemyWouldActivate`, un message bien plus TOT
#    (avant meme la distribution des cartes de boost), et n'est donc PAS un modele valable pour ce point de
#    declenchement. `can_attack.py:133` (`WhenUnitWouldAttack.PreventDamage`) est le bon outil : il enregistre
#    une capacite temporaire sur `WhenUnitWouldTakeDamage`, un message envoye PLUS TARD (juste avant que les
#    degats de CETTE attaque soient infliges), donc encore joignable depuis la fenetre de reveal du boost.
#
# TEXTE CONTRE CODE
#  "a boost card WITH [boost][boost][boost]" : exactement 3 icones affichees -> `message.boost_icons >= 3`
#    (aucune carte boost du jeu n'imprime plus de 3 icones -> >= et == sont equivalents en pratique, >= documente
#    l'intention "au moins 3" si jamais une carte en imprimait davantage).
#  "during an ENEMY activation" (pas limite a une attaque de base) : aucun filtre `is_basic_power`.
#  "(defense)" (label imprime) -> seulement quand l'activation est dirigee CONTRE le joueur -> `activate_target
#    ="You"`, `while_attack=True` (une "activation" en defense est forcement une attaque, jamais une manigance).
#  "cancel that activation AND ignore any 'Boost' ability" : DEUX effets distincts, tous les deux systematiques
#    des que le seuil est atteint (pas un choix). ARBITRAGE UTILISATEUR (04/11/2026) : « cancel that activation »
#    devient, au niveau ou le moteur permet encore d'agir, « empeche tous les degats de cette activation »
#    (`would_message.PreventDamage("All", effect)`) -- equivalent pour un Rhino nu (aucune autre consequence
#    attachee a son activation de base dans ce pack). `CancelBoostAbility` reste pose sans condition : sans
#    effet si la carte retournee n'a pas d'etoile Boost (`canbe_cancel=None`, pas "Ability" -- la gate "Ability"
#    de hc010 ne convient PAS ici : son EFFET ENTIER depend d'une capacite Boost a annuler, celui de dm020 non,
#    "cancel that activation" et "draw 1 card" restent utiles meme sans etoile Boost sur la carte retournee).
#
# Chiffres : seuil 3 icones de boost ; draw 1 card.

def GetAbilities() -> Sequence['Ability']:

    def au_moins_trois_icones(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> bool:
        return message.boost_icons >= 3

    def prevent_disaster(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.would_message.PreventDamage("All", effect)
        message.CancelBoostAbility(effect)

        joueur = effect.GetInitiator()
        if joueur is not None:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.WhenBoostCardTurnedFaceUp(
            AbilityType.HeroInterrupt,
            None,
            prevent_disaster,
            while_attack=True,
            activate_target="You",
            conditions=[au_moins_trois_icones],
        ).SetPlay().SetLabel('defense'),
    ]
