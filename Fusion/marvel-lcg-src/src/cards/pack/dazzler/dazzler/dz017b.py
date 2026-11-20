from . import *

# Showtime!
# Permanent.
# When Revealed: Resolve the "Showtime!" ability on each card in the Setlist,
#   in any order. Then, discard all cards from the Setlist. If 4 cards were
#   discarded this way, you may either deal 4 damage to an enemy or remove 4
#   threat from a scheme. Flip this card.
#
# La face active de Live Concert (dz017a). Le retournement se fait par la Hero
# Action de l'autre face ; « Flip this card » a la fin nous ramene la.
#
# « If 4 cards were discarded this way » se lit sur le nombre REELLEMENT
# defausse, pas sur la taille de la Setlist avant : une Setlist de 3 ne donne
# pas la prime.


def GetAbilities() -> Sequence['Ability']:

    def montrer(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Upgrade)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        setlist = Setlist(effect)
        # « in ANY ORDER » : le joueur choisit, a chaque pas, la chanson dont le
        # Showtime! part. L'ordre compte (Doll pose une Tough que Velvet Sky
        # peut retirer ensuite). Jusqu'au 20/10/2026 le module imposait l'ordre
        # de la zone, du dessus vers le dessous (backlog 12).
        restantes = list(setlist)
        while restantes:
            choisie = joueur.AskChooseOneText(restantes) \
                if len(restantes) > 1 else restantes[0]
            if choisie is None or choisie not in restantes:
                choisie = restantes[0]
            restantes.remove(choisie)
            ResoudreShowtime([choisie], joueur, effect)

        # Les compteurs sound sont la memoire de Rehearsal DANS la Setlist :
        # ils partent avec les cartes (`OublierLaSetlist`, prevu pour cela mais
        # jamais appele ici avant le 20/10/2026 ; une chanson rejouee apres
        # Encore arrivait marquee, donc non repetable).
        OublierLaSetlist(effect, setlist)
        partis = Faces.DiscardAll(setlist, effect)
        nombre = len(partis)

        if nombre >= PLACES_SETLIST:
            def degats(targets: Sequence['CardFace']) -> None:
                this.DealDamage(targets, 4, effect)

            def menace(targets: Sequence['CardFace']) -> None:
                this.RemoveThreatFromSchemes(targets, 4, effect)

            # « you MAY EITHER... » : les deux branches sont offertes, et le
            # moteur ecarte de lui-meme celle qui n'a aucune cible legale.
            # Sans menace sur la moindre manigance, seul « Deal 4 damage »
            # apparait ; c'est le comportement standard du moteur, pas un
            # manque de cette carte.
            joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility("Deal 4 damage", degats)
                .SetTarget(Enemy),
                AbilityFactory.ForChoiceAbility("Remove 4 threat", menace)
                .SetTarget(Scheme2),
            )

        Faces.FlipAllTo([this], None, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenThisRevealed(None, montrer),
    ]
