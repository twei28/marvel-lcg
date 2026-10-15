from . import *

# * Hulkling — face HEROS. PV 13, ATK 2, THW 1, DEF 2, main 5. AVENGER.
# Descendant of Both Races — Response: After you play a card with the [[KREE]]
#   or [[SKRULL]] trait from your hand, if you share that trait, draw 1 card.
#   (Limit once per round.)
#
# Cartes de reference :
#  - **`22001b`** * Nebula : « Response: After you play a [[technique]]
#    upgrade, draw 2 cards. (Limit once per round.) » Meme declencheur, meme
#    limite, meme effet : `AfterPlayerPlayedCard(Response, "You", <filtre>,
#    op).LimitOncePerRound()`.
#  - `42001a` * Angel pour le filtre de trait (`CardFinder2("AERIAL", Event)`).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « KREE **or** SKRULL » : `CardFinder(traits=[...])` est un OU (finder.py).
#  - « **from your hand** » : `from_hand=True`. Une carte jouee depuis la
#    defausse (sk014 Nega Rings ne joue pas, il echange ; mais d'autres
#    heros le peuvent) ne compte pas.
#  - « if you **share that** trait » : le trait de LA CARTE JOUEE que
#    Hulkling porte aussi. Une carte KREE jouee en forme Skrull ne pioche
#    pas. Une carte KREE+SKRULL (sk009 Alliance) pioche quelle que soit la
#    forme. Teste dans la CONDITION, pas dans l'effet : sinon la limite d'un
#    round serait consommee par un declenchement qui ne pioche rien.
#  - « Limit once per **round** » : `LimitOncePerRound()`, pas per phase.
#  - La capacite n'existe que sur la face HEROS : Teddy Altman (sk001b) n'a
#    ni ce texte ni les traits d'origine (l'upgrade dit « HULKLING gains »).


def GetAbilities() -> Sequence['Ability']:

    def partage(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> bool:
        return bool(TraitsPartages(message.played_face, IdentiteDe(effect)))

    def descendant(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)

        effect.GetInitiator().DrawUp(1, effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(traits=["KREE", "SKRULL"]),
            descendant,
            from_hand=True,
            conditions=[partage],
        ).SetName("Descendant of Both Races")
        .LimitOncePerRound(),
    ]
