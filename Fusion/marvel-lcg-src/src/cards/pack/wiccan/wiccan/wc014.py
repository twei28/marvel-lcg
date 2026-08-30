from . import *

# Warping Reality — custom « CptScorp »
# Cout 0, [wild], classe Hero, traits SPELL / SUPERPOWER.
# Action: Reduce the cost of the next card played this round by 1+X, where X
#   is the number of boost icons on the top card of the encounter deck.
#
# Mecanisme -> `Worlds.UpdateNextCardPlayCost(player, -valeur, effect,
# in_this=...)` (game/operate/worlds.py:808), la brique unique du depot pour
# « reduce the cost of the next card played ». Modeles : Helicarrier
# (`core/01092.py`, « the next card that player plays this phase ») et Pore
# Over the Evidence (`jessica_jones/on_the_job/jj015.py`, meme brique sur un
# joueur nomme).
#
# ECART ASSUME, DOCUMENTE : le texte imprime dit « this ROUND ». Le moteur
# ne connait que `in_this="Phase"` et `in_this="Turn"` (worlds.py:815 :
# `in_this: Literal["Phase", "Turn"]`) — il n'existe AUCUNE variante « Round »,
# ni ici ni ailleurs (meme lecon que le pack Dazzler). « Phase » est retenu,
# c'est la plus large des deux : elle couvre TOUTE la phase des joueurs, donc
# les tours des autres joueurs aussi, la ou « Turn » s'arreterait a la fin du
# tour courant. Ce qui reste hors de portee, c'est la phase du VILAIN du meme
# round — une carte jouee en reaction pendant la phase du vilain ne
# beneficiera pas de la reduction, alors que le texte imprime le permettrait.
# Restriction plus severe que la carte, jamais plus permissive : c'est le sens
# de l'ecart qu'on accepte.
#
# `1+X` -> `1 + IconesBoostDuDessus(...)`. La reduction vaut donc AU MOINS 1,
# meme a 0 icone, meme sur un deck de rencontre vide, meme quand l'obligation
# wc018 a eteint le comptage : le « 1 » est imprime en dur, seul X depend des
# icones. `UpdateNextCardPlayCost` attend une valeur NEGATIVE pour une
# reduction (Helicarrier passe -1), d'ou le `-valeur`.
#
# « Action: » nu -> `AbilityType.Action`, jouable dans les deux formes.

def GetAbilities() -> Sequence['Ability']:

    def warping_reality(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        valeur = 1 + IconesBoostDuDessus(effect, initiator)
        Worlds.UpdateNextCardPlayCost(
            initiator,
            -valeur,
            effect,
            in_this="Phase",
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            warping_reality,
        ).SetPlay(),
    ]
