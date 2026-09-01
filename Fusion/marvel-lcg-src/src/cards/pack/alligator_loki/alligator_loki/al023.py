from . import *

# Little Rascals — evenement Team-Up. Basic. Cout 2, [physical].
# Team-Up (Alligator Loki and Honey Badger/Gabby Kinney). Max 1 per deck.
# Action: Stun and confuse the villain. If you cannot, ready Alligator Loki
#   or Honey Badger.
#
# Cartes de reference :
#  - 12020 Swarm Tactics, 51025 Heart of the Panther : un evenement Team-Up
#    se joue par `.SetTarget("TeamUp")` ; la cle `TeamUp` de `desc`
#    (has_teamup.py:16) verifie que les deux personnages nommes sont en jeu,
#    identite OU allie (`GetTeamUpUnits`), et le moteur bloque la carte sinon ;
#  - `Faces.GiveStatus([vilain], "Stunned"|"Confused", effect)` rend 1 si le
#    statut a ete pose, 0 sinon (faces.py:169) : c'est la ou « if you cannot »
#    se lit. `GainStatus` refuse deja Stalwart, un statut deja present, ou
#    un vilain immunise (can_status.py:76-79).
#
# ⚠ « IF YOU CANNOT » : on tente les deux statuts ; si l'un des deux n'a pas
# pu etre pose, le joueur redresse. Un vilain deja etourdi mais pas confus
# recoit donc le confus ET donne le redressement : la carte dit « stun AND
# confuse », l'effet n'a pas pu se resoudre en entier.
# ⚠ « ready Alligator Loki OR Honey Badger » : le joueur choisit, parmi les
# personnages amis en jeu portant l'un de ces noms (Honey Badger est un
# allie, chez n'importe quel joueur : sinon la carte ne se jouerait pas).
# En alter-ego, l'identite s'appelle aussi Alligator Loki : redressable.
# ⚠ Honey Badger = 43003 (x23) ou wx003 (fan-made), meme nom, meme
# sous-titre : `IsName("Honey Badger")` les couvre tous deux.

NOM_HONEY_BADGER = "Honey Badger"


def GetAbilities() -> Sequence['Ability']:

    def little_rascals(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        vilain = Worlds.FindVillain(effect)
        reussi = False
        if vilain is not None and vilain.card.IsOnField():
            etourdi = Faces.GiveStatus([vilain], "Stunned", effect)
            confus = Faces.GiveStatus([vilain], "Confused", effect)
            reussi = etourdi > 0 and confus > 0
        if reussi:
            return

        candidats = [
            f for f in Worlds.GetOnFieldFriendlyCharacters(effect)
            if f is not None and f.card.IsOnField() and not f.IsReady()
            and (f.IsName(NOM_HEROS) or f.IsName(NOM_HONEY_BADGER))
        ]
        if not candidats:
            return
        cible = joueur.AskChooseFace(candidats, effect, prompt="Ready")
        if cible is not None:
            Faces.ReadyAll([cible], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            little_rascals,
        ).SetPlay()
        .SetTarget("TeamUp"),
    ]
