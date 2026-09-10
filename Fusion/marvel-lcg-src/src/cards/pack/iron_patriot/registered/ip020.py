from . import *

# H.A.M.M.E.R. Agents — SBIRE du deck REGISTERED (1/20), x3. 2 PV, ATQ 1,
# MNG 1, boost 1. H.A.M.M.E.R.
# When Revealed: If this is the first card revealed from the REGISTERED deck
#   this round, put this card under your control as a REGISTERED ally.
# Reinforcements — Special: Search the REGISTERED deck for a copy of
#   H.A.M.M.E.R. Agents and put it into play under your control as a REGISTERED
#   ally. Shuffle the REGISTERED deck.
#
# ⚠⚠ LA CARTE LA MOINS CHERE DU DECK (1 icone de boost) EST AUSSI LA SEULE QUI
# SE MULTIPLIE. Trois exemplaires, et chacun en appelle un autre : c'est le
# moteur a allies du pack, et la raison d'etre de `ip021` / `ip022`, qui
# comptent les personnages H.A.M.M.E.R. en jeu.
#
# CARTES DE REFERENCE
#  - `__init__.py` du pack : `SiPremiereReveleeAlorsAllie()` porte le « When
#    Revealed », mot pour mot identique sur `ip020`, `ip021` et `ip022`.
#  - `25023` * The Bifrost : `Search.PlayerCard`/`Search.SearchForCard` avec
#    `faces=` pour fouiller un paquet precis, ici le deck REGISTERED.
#
# TEXTE CONTRE CODE
#  ⚠ « put this card under your control as a REGISTERED ally » sans mention de
#    cout : le ralliement du « When Revealed » est GRATUIT. C'est le seul du
#    pack, et il est borne a une fois par round.
#  ⚠ « Search the REGISTERED deck FOR A COPY OF H.A.M.M.E.R. Agents » : un
#    autre exemplaire, pas celui-ci. On fouille le deck, ou celui-ci n'est plus.
#  ⚠ « put it INTO PLAY under your control as a REGISTERED ally » : la carte
#    arrive DEJA alliee, sans passer par la case sbire, et donc sans « When
#    Revealed ». `Faces.PutIntoPlayAll` puis conversion — l'ordre compte, le
#    gabarit d'allie ne s'applique qu'a une carte en jeu.
#  ⚠ « Shuffle the REGISTERED deck » : `Search` remelange deja le paquet
#    fouille quand `not_move` est faux. Rien a ajouter.


def GetAbilities() -> Sequence['Ability']:

    def renforts(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        deck = DeckRegistered(joueur)
        copies = [f for f in deck.Get()
                  if f is not None and f is not this and f.IsName("H.A.M.M.E.R. Agents")]
        if not copies:
            return
        face = Search.SearchForCard(effect, joueur, faces=copies)
        if face is None:
            return
        if face.PutIntoPlay(joueur, effect):
            RecruterCommeAllieRegistered(face, joueur, effect)

    return [
        SiPremiereReveleeAlorsAllie(),
        SpecialRegistered("Reinforcements", renforts),
    ]
