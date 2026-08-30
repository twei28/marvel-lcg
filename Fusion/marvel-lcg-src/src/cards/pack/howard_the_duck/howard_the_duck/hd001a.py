from . import *

# * Howard the Duck (face heros) — DEFENDER. GUARDIAN
# Private Eye — Interrupt: When threat would be placed on a scheme, prevent 1
#   of that threat. (Limit once per round.)
# Response: After a side scheme enters play, ready Howard the Duck.
#   (Limit once per round.)
#
# Capacite 1 (Private Eye) : modele exact bkw/08017.py (Counterintelligence),
# meme couple `AbilityFactory.WhenThreatWouldBePlacedOn(...)` +
# `message.PreventThreat(<n>, effect)`. Deux ecarts VOULUS par le texte
# imprime : la portee est « a scheme » (n'importe quelle manigance, donc
# `which_scheme=None`, la ou Counterintelligence vise `MainScheme` seul) et
# la prevention vaut 1 (pas 3). `AbilityType.Interrupt` et non
# `HeroInterrupt` : le texte n'ecrit pas « Hero Interrupt », et la face Heros
# n'est de toute facon en jeu qu'en forme heros.
#
# Capacite 2 : modele `AbilityFactory.AfterCardEnterPlay(Response, <cible>)`
# (ok002 Aneka pour la fabrique, bp/51014.py Manifold a l'origine), cible
# `SchemeSide2` = TOUTE manigance annexe (joueur ou rencontre), ce qui est
# exactement ce que dit « a side scheme ». Redressement : `Faces.ReadyAll`
# (modele il015/ok014).


def GetAbilities() -> Sequence['Ability']:

    def private_eye(effect: 'Effect', message: 'Message.WhenSchemeWouldPlaceThreat') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        message.PreventThreat(1, effect)

    def ready_howard(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)

        Faces.ReadyAll([this], effect)

    return [
        AbilityFactory.WhenThreatWouldBePlacedOn(
            AbilityType.Interrupt,
            None,
            private_eye,
        ).SetName("Private Eye")
        .LimitOncePerRound(),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            SchemeSide2,
            ready_howard,
        ).LimitOncePerRound(),
    ]
