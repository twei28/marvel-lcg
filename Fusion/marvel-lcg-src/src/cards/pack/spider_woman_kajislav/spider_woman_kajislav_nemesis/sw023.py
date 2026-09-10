from . import *

# Bad Inspiration — TRAITRISE de nemesis (3/5). Boost 1.
# When Revealed: Search your discard pile for an ally and put it into play
#   engaged with you. Treat the ally as a minion with a blank text box.
#   Minion's SCH is equal to its printed THW and it does not take consequential
#   damage. If no ally entered play this way, this card gains surge.
#
# ⚠⚠ L'INVERSE EXACT DU DECK REGISTERED d'Iron Patriot : la, un sbire devenait
# allie ; ici, un allie est retourne contre vous. Et la brique EXISTE DEJA :
# `TreatAsMinion` (`game/ability/factory/treat.py:3`) fait tout le travail, y
# compris les deux phrases que l'auteur a pris la peine d'ecrire —
#   « Minion's SCH is equal to its printed THW » : `minion.printed_scheme =
#     face.printed_thwart` (treat.py:31), mot pour mot ;
#   « does not take consequential damage » : le gabarit n'a ni etoile d'ATQ ni
#     etoile de MNG, donc aucun degat consecutif. Le moteur porte meme le
#     commentaire « it does not take consequential damage » a la ligne 41.
#
# CARTES DE REFERENCE
#  - `27171` Manipulated Mind (pack sm) : MEME TEXTE, a l'attachement pres.
#    Elle emploie le gabarit nomme « Minion » et recopie nom et sous-titre de
#    l'allie sur le sbire. On fait pareil : sans cela, le plateau afficherait
#    « Minion » et le joueur ne saurait pas QUEL allie s'est retourne.
#  - `agent_anti_venom_nemesis/__init__.py` : le precedent d'appel DIRECT de
#    `TreatAsMinion` depuis une capacite (et non depuis un attachement).
#
# ⚠ LES PV NE SONT PAS DANS LE GABARIT (« HP »: « 0 ») et c'est VOULU : le
# composant de sante appartient a la CARTE (`component/health.py`, `Component`
# prend un `Card`), pas a la face. L'echange de face laisse donc l'allie avec
# ses points de vie. Ne pas « corriger » ce 0.
#
# TEXTE CONTRE CODE
#  ⚠ « search YOUR DISCARD PILE » : la defausse du joueur, pas son deck.
#    `Search.PlayerCard(include_player_deck=False, include_discard_pile=True)`.
#  ⚠ « blank text box » SANS la parenthese « (except for traits) » de 27171 :
#    on ne recopie donc PAS les traits. Un allie AVENGER retourne n'est plus
#    AVENGER.
#  ⚠ « engaged with YOU » : il devient VOTRE probleme.
#  ⚠ « If NO ALLY entered play this way » : defausse sans allie, ou conversion
#    refusee, et seulement alors, deferlement.
#  ⚠ Le retour a la face d'allie quand le sbire quitte le jeu est inscrit par
#    `TreatAsMinion` lui-meme (treat.py:48). Rien a ajouter.


def GetAbilities() -> Sequence['Ability']:

    GABARIT = "Minion"

    def reprendre_l_allie(minion: 'Any', allie: 'Any', effect: 'Effect') -> None:
        Unused(effect)
        minion.SetName(allie.printed_name)
        minion.SetSubtitle(allie.printed_subtitle)
        minion.printed_health = allie.printed_health
        minion.starting_health = allie.printed_health

    def mauvaise_inspiration(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        retourne = False

        if joueur is not None:
            allie = Search.PlayerCard(
                effect, joueur,
                include_player_deck=False,
                include_discard_pile=True,
                not_move=True,
                card_type=Ally)
            if allie is not None:
                retourne = TreatAsMinion(allie, GABARIT, joueur, effect,
                                         process=reprendre_l_allie)

        if not retourne:
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, mauvaise_inspiration),
    ]
