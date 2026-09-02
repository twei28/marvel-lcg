from . import *

# Welcome to Darkness 3A — COMPLOT PRINCIPAL, face de transition.
#
# When Revealed: If the Godbomb environment is in play, remove all timer
#   counters from it and flip it to its All-Black Necroverse side. Otherwise,
#   put the set-aside All-Black Necroverse environment into play. Shuffle the
#   set-aside Necroverse modular encounter set into the encounter deck.
#   Shuffle 1 copy of the Stalking Berserker minion into each player's deck.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Retourner un environnement recto-verso en cours de partie : 50090a (Alert
#   Level, pack aos) — `Faces.RemoveTokensOn` puis `this.card.Flip(effect)`.
#   Ici c'est une AUTRE carte qui retourne l'environnement, on appelle donc
#   `env.card.Flip(effect)` sur la face trouvee.
# - « put the set-aside <environnement> into play » : 50087a, cf. gb005a.
# - « Shuffle the set-aside <set> into the encounter deck » : campaign_setup.py
#   (pack aoa), `Faces.ShuffleAllTo(faces, 'EncounterDeck', effect)`.
# - « Shuffle 1 copy of <sbire> into each player's deck » : meme montage que
#   Heroes' Labor en gb005a (creation DANS `player.player_deck` pour obtenir
#   un dos de carte joueur, exige par le PDF de l'auteur).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « IF ... OTHERWISE » -> deux branches exclusives. La premiere n'existe que
#   si le complot 2B a ete traverse (c'est lui qui pose l'environnement) ; en
#   expert, le vilain III peut sauter directement de 1B a 3A et la seconde
#   branche est la seule possible.
# « remove ALL timer counters » -> "All", pas une valeur.
# « flip it to ITS ALL-BLACK NECROVERSE SIDE » -> `Flip` sur la carte, qui
#   n'a que deux faces : le retournement est deterministe.
# « Shuffle the SET-ASIDE Necroverse modular encounter set » -> les cartes que
#   gb004a a mises de cote, retrouvees par leur `set_name`, pas des copies.
#   ⚠ Ce set est EXTERNE au pack et n'est pas encore porte (voir gb004a) : la
#   recherche ne rend rien aujourd'hui, sans casser le reste de la
#   revelation.
# ⚠ Ordre : le retournement AVANT le melange du modulaire, sinon les Black
#   Berserker entrent avant que leur compteur de reference existe.


def GetAbilities() -> Sequence['Ability']:

    def bienvenue_dans_les_tenebres(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this, message)

        godbomb = TrouverGodbomb(effect)
        if godbomb is not None:
            Faces.RemoveCountersOn([godbomb], "All", 'timer', effect)
            godbomb.card.Flip(effect)
        else:
            # ⚠ On cherche la CARTE (gb007a), pas le nom de sa face B : dans
            # la reserve, elle est rangee sur sa face A « Godbomb », et une
            # recherche par `name="All-Black Necroverse"` ne trouve rien.
            # `flip_to_name` la retourne ensuite sur la bonne face.
            SetupCards.PutIntoPlay(
                effect,
                card_ids=["gb007a"],
                card_type=Environment,
                flip_to_name=NOM_NECROVERSE,
            )

        # `GetSetAsideAreaCards` (worlds.py:382) balaie la reserve du monde ET
        # celle de chaque joueur ; le filtre passe par un `CardFinder`, la
        # fonction ne prend pas de mot-cle.
        mises_de_cote = Worlds.GetSetAsideAreaCards(
            effect, CardFinder(set_name="Necroverse"))
        if mises_de_cote:
            Faces.ShuffleAllTo(mises_de_cote, 'EncounterDeck', effect)

        monde = effect.world
        for joueur in Worlds.GetPlayers(effect):
            copie = CardFactory.GenerateCard("gb022", joueur.player_deck, monde)
            Faces.ShuffleAllTo([copie.face], joueur.player_deck, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            bienvenue_dans_les_tenebres,
        ),
    ]
