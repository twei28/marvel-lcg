from . import *

# Magic Manipulation — custom « CptScorp »
# Cout 0, [mental], classe Hero, traits SPELL / SUPERPOWER.
# Alter-Ego Action: Shuffle 1 card from your discard pile back into your deck
#   for each boost icon on the top card of the encounter deck. Then, draw 1
#   card.
#
# « Alter-Ego Action: » IMPRIME sur une carte JOUEUR (pas sur la face
# alter-ego elle-meme) -> `AbilityType.AlterEgoAction`, exactement comme
# Soul World (21033, meme fabrique) et contrairement a wc001b, dont le
# « Action: » nu figure sur la face d'identite. La distinction est celle
# rappelee dans ag001b.
#
# « Shuffle 1 card ... for each boost icon » -> X = `IconesBoostDuDessus`,
# puis `initiator.AskChooseFaces(defausse, (n, n), effect, not_move=True)` et
# `Faces.ShuffleAllTo(faces, initiator.player_deck, effect)`
# (game/operate/faces.py:48). Modele du remelange depuis la defausse vers le
# deck du joueur : `okoye/okoye/ok001b.py` (Marshalling Forces) et
# `ok011.py` (Upanga), qui font tous deux ce trajet defausse -> deck.
#
# n est BORNE par la taille de la defausse (`min`) : « shuffle 1 card ... for
# each boost icon » ne peut pas remonter plus de cartes qu'il n'y en a. La
# plage est FERMEE (n, n) et non (0, n) : le texte n'imprime pas « up to »,
# le remelange est obligatoire des lors que des cartes sont disponibles.
#
# « Then, draw 1 card » -> `initiator.DrawUp(1, effect)`, la brique standard
# (modele 15004 Hex Bolt, palier « 2 icones »). Elle est INCONDITIONNELLE :
# elle a lieu meme a 0 icone, meme sur une defausse vide, meme quand
# l'obligation wc018 a eteint le comptage.

def GetAbilities() -> Sequence['Ability']:

    def magic_manipulation(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        icones = IconesBoostDuDessus(effect, initiator)
        defausse = list(initiator.discard_pile.Get())
        nombre = min(icones, len(defausse))

        if nombre > 0:
            choisies = initiator.AskChooseFaces(
                defausse,
                (nombre, nombre),
                effect,
                prompt="Shuffle back into your deck",
                not_move=True,
            )
            if choisies:
                Faces.ShuffleAllTo(choisies, initiator.player_deck, effect)

        initiator.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            magic_manipulation,
        ).SetPlay(),
    ]
