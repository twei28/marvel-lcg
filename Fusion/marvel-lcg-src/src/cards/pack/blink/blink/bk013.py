from . import *

# * Morph (Kevin Sidney) — ALLIE BASIC, cout 2, PV 3. X-MEN.
# Action: Shuffle Morph into the encounter deck.
# When Revealed: Discard Morph.
#
# ⚠ UNE CARTE JOUEUR QUI PORTE UN « WHEN REVEALED ». Morph se sacrifie pour
# DILUER le deck de rencontre : chaque exemplaire melange dedans est une carte
# de rencontre en moins qui frappe. Cas rare — le pack `gorr` a le meme en
# sens inverse (gb021/gb022, cartes a DOS JOUEUR melangees aux decks joueurs).
#
# ⚠ HOMONYME : l'allie OFFICIEL `45174` * Morph est lui aussi de classe BASIC.
# Les deux ne peuvent pas etre en jeu ensemble (regle d'unicite), et le
# deck-builder montrera deux « Morph » distincts. Documente dans le deck.


def GetAbilities() -> Sequence['Ability']:

    def se_melanger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        # ⚠ `Faces.ShuffleAllToEncounterDeck` N'EXISTE PAS — API inventee, que
        # `test_cards` ne voit pas (c'est un acces d'attribut a l'execution) et
        # que le moteur AVALE : Morph restait tranquillement en jeu. La seule
        # methode est `ShuffleAllTo`, dont le deck de rencontre est un litteral.
        Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    def se_defausser(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            se_melanger,
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            se_defausser,
        ),
    ]
