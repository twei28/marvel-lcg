from . import *

# "Beauty and the Beast"
# SONG.
# Hero Action: Search your deck for an ally and put it into play. If that ally
#   is still in play at the end of the phase, add it to your hand.
# Showtime!: Give a friendly character +2 THW until the end of the phase.
#
# Le retour en main est CONDITIONNEL : l'allie peut mourir avant la fin de la
# phase. On enregistre donc une capacite temporaire SUR L'ALLIE, pas sur
# l'evenement — celui-ci part dans la Setlist ou a la defausse aussitot, et une
# capacite accrochee a lui ne survivrait pas.
#
# « a FRIENDLY character » : `SetTarget(Friend)`, tout personnage du cote des
# joueurs (modele 01080 First Aid). Jusqu'au 20/10/2026 la cible etait
# `"YouControlUnit"`, qui excluait les personnages des AUTRES joueurs : ecart
# invisible en solo, corrige au backlog 12 (cas a deux joueurs).


def GetAbilities() -> Sequence['Ability']:

    def la_belle_et_la_bete(effect: 'Effect',
                            message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        allie = Search.PlayerCard(
            effect, joueur, include_player_deck=True, card_type=Ally)
        if allie is None:
            return

        allie.CastTo(Ally).PutIntoPlay(joueur, effect, under_control=True)

        def rappeler(eff: 'Effect', msg: 'Message.WhenPhaseEnd') -> None:
            if allie.IsInPlay():
                Faces.AddToHand([allie], joueur, eff)

        allie.effect.RegisterTemp(
            AbilityFactory.WhenPhaseEnd(
                AbilityType.Temp2,
                "Player",
                rappeler,
            ),
            unregister_after_exec=True,
        )

    def showtime(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        # Le joueur CHOISIT la cible : `ResolveAbility` prendrait sinon la
        # premiere cible legale sans rien demander (cf. CiblesShowtime).
        for face in CiblesShowtime(effect):
            face.GainUntilPhaseEnd(effect, thwart=2)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            la_belle_et_la_bete,
        ).SetPlay().SetLabel(),
        Showtime(showtime).SetTarget(Friend, range=(0, 1)),
    ]
