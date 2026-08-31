from . import *

# Single Out — evenement. TACTIC. Cout 0. x3
# Hero Interrupt: When a treachery card is revealed from the encounter deck,
#   cancel its "When Revealed" effects. Search the encounter deck for a minion
#   and put it into play engaged with any player.
#
# Cartes de reference :
#  - wd136 Team Spider-Sense (pack web_of_deceit), jumeau exact pour la
#    premiere phrase : `WhenPlayerRevealCard(<type>, "AnyPlayer", Treachery,
#    "WhenRevealed", ..., from_encounter=True)` puis
#    `message.CancelWhenRevealedEffect(effect)`.
#  - ss019 * Bella Donna (pack scarlet_spider) pour `Search.EncounterCard(...)`
#    suivi d'une mise en jeu.
#
# ⚠ Le sbire arrive « engaged with ANY player » : c'est un CHOIX du joueur qui
# resout, pas forcement lui-meme. En solo la question ne se pose pas.
#
# ⚠ Ce n'est pas une carte defensive malgre les apparences : mettre un sbire en
# jeu ALIMENTE le moteur du pack (an001a Frenzy, an004 Murderous Glare, an007
# Asgard's Assassin, an009 Xiphos paient tous quand un sbire tombe). L'annulation
# et le sbire ne sont pas deux effets separes, c'est un echange volontaire.

def GetAbilities() -> Sequence['Ability']:

    def single_out(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.CancelWhenRevealedEffect(effect)

        face = Search.EncounterCard(
            effect,
            include_discard_pile=False,
            card_type=Minion,
        )
        if face is None:
            return
        joueur = effect.GetInitiator()
        if isinstance(joueur, Player):
            face.PutIntoPlay(joueur, effect)

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "AnyPlayer",
            Treachery,
            "WhenRevealed",
            single_out,
            from_encounter=True,
        ).SetPlay(),
    ]
