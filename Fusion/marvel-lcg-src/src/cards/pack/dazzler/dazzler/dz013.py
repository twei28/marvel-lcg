from . import *

# "Velvet Sky"
# SONG.
# Hero Interrupt: When a treachery is revealed from the encounter deck, cancel
#   all of its effects and discard it.
# Showtime!: Remove a status card from a friendly character.
#
# Modele Protective Ward (09007), qui porte EXACTEMENT la meme phrase imprimee
# et l'ecrit en une ligne : `CancelAllEffectsAndDiscardIt`, avec le niveau
# d'annulation « All ».
#
# CORRECTIF (partie reelle) : la version precedente annulait « WhenRevealed » et
# defaussait a la main. Or « cancel ALL of its effects » englobe les MOTS-CLES
# — le moteur le dit lui-meme (sender_card.py:474 : « Canceling the effects of
# a treachery card, means canceling all of the effects on that card, including
# keywords ») et n'eteint le surge que sur `cancel_all_effects`
# (face_on_event.py:326). Mesure : Exhaustion (01191, Surge) annulee par
# l'ancienne version faisait quand meme distribuer 1 carte Rencontre de plus.
#
# Showtime! : « a FRIENDLY character » = `SetTarget(Friend)` (tout personnage du
# cote des joueurs) ; la cible etait `"YouControlUnit"` jusqu'au 20/10/2026.
# « a status card » : `RetirerUnStatut` (dazzler/__init__.py) couvre toutes les
# cartes d'etat et laisse le joueur choisir quand il y en a plusieurs.


def GetAbilities() -> Sequence['Ability']:

    def ciel_de_velours(effect: 'Effect',
                        message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.CancelAllEffectsAndDiscardIt(effect)

    def showtime(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        # Le joueur CHOISIT la cible : `ResolveAbility` prendrait sinon la
        # premiere cible legale sans rien demander (cf. CiblesShowtime).
        for cible in CiblesShowtime(effect):
            RetirerUnStatut(cible, effect)

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "AnyPlayer",
            Treachery,
            "All",
            ciel_de_velours,
            from_encounter=True,
        ).SetPlay(),
        Showtime(showtime).SetTarget(Friend, has_status="Any",
                                    range=(0, 1)),
    ]
