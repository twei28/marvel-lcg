from . import *

# Cosmic Cube Creation — COMPLOT ANNEXE (Shaper of Worlds). Menace 2 (fixe), Hinder 4[per_hero],
# Victory 2, Acceleration, 3 icones de boost.
# Hinder 4[per_hero]. Victory 2.
# When Revealed: Put the set-aside Shaper of Worlds into play engaged with you.
# When Defeated: Each player chooses a copy of the set-aside Cosmic Cube Fragment resource and
#   shuffles it into their deck.
# + INSERT du set : a la mise en place, le sbire et les quatre fragments sont mis de cote.
#
# Cartes de reference :
#  - Mise de cote : **`60038`** (`WhenGameBeginSetup(...).NoOutOfPlayLimit()` : une capacite de
#    mise en place d'une carte encore hors jeu) ; ici `AfterGameSetup` (WhenGameWouldBegin), seule
#    fenetre posterieure a la creation du deck rencontre. `Faces.SetAside` (modele Overthrow sk105).
#  - « When Defeated » : **`sk100`** Emperor's Throne (`WhenSchemeBeDefeated(WhenDefeated, "This", ...)`).
#  - « engaged with you » : **`sk136`** Bel-Dann (sbire `PutIntoPlay(joueur)`).
#  - « Each player chooses ... shuffles it into their deck » : `Players.ForEachPlayer` +
#    `AskChooseFace` + `Faces.ShuffleAllTo(faces, joueur.player_deck, effect)`.
#
# ⚠ Mots-pieges : « SET-ASIDE » Shaper (pas celui du deck : il n'y en a qu'un exemplaire et il est
# a cote) ; « put into play engaged with YOU » (PutIntoPlay, pas Reveal : rien n'est revele) ;
# « EACH player CHOOSES a copy » : chaque joueur choisit parmi les fragments restants (un fragment
# pris n'est plus offert au suivant) ; « shuffles it into THEIR deck » ; Hinder/Victory/Acceleration
# sont natifs (desc).


def GetAbilities() -> Sequence['Ability']:

    def mise_de_cote(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        Unused(message)
        # Mode campagne Skrull Menace : le carnet DIT ou est chaque carte du set (en jeu, mis de cote,
        # ailleurs), `cards/pack/skrull_menace/campaign.py` les place une a une a la mise en place. Les
        # remettre toutes de cote ici defairait ce qu'il vient de poser (un Shaper « in another game
        # area » doit rester dans le deck rencontre).
        if Worlds.IsCampaign(effect):
            return
        if effect.this.card.area.flags.is_encounter_deck:
            MettreDeCoteLeSet(effect)

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        shaper = ShaperMisDeCote(effect)
        if shaper is not None:
            MettreEnJeuEngage(effect, shaper, message.GetToPlayer())

    def vaincu(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        Unused(message)

        def choisir(joueur: 'Player') -> None:
            fragments = FragmentsMisDeCote(effect)
            if not fragments:
                return
            choisi = joueur.AskChooseFace(fragments, effect)
            if choisi is not None:
                Faces.ShuffleAllTo([choisi], joueur.player_deck, effect)
        Players.ForEachPlayer(effect, choisir)

    return [
        AbilityFactory.AfterGameSetup(mise_de_cote).NoOutOfPlayLimit(),
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
