from . import *

# Mutant Science Program — complot annexe nemesis (5/5). Menace 5[per_hero].
# Boost 2.
# When Revealed: Place 1 test counter on this side scheme for every ally in
#   your discard pile. If there are 0 allies in your discard pile, place
#   2[per_hero] test counters instead.
# Forced Response: Whenever you draw an ally into your hand -> remove 1 test
#   counter and discard the ally and find the Lizard-Fied Minion in the
#   encounter or discard pile and put it into play.
#
# Cartes de reference :
#  - squelette « When Revealed » de complot annexe : an011 Hel's Retribution,
#    `WhenThisRevealed(None, op)`, et `message.GetToPlayer()` pour atteindre
#    le joueur vise (une carte de rencontre n'a pas le joueur pour initiateur).
#  - pose de compteurs sur la carte elle-meme : `face.PlaceCountersInternal(n,
#    'test', effect)`, comme aos/campaign.py:131 pour ses compteurs 'secret'.
#    Le compteur `test` existait DEJA dans l'enum COUNTER : rien a ajouter.
#  - « whenever you draw » : `AfterPlayerDrewCards(type, which_player,
#    which_card, op)` (factory/player.py:372). Le filtre `which_card` porte
#    deja sur les cartes piochees : `Ally` suffit, inutile de relire la main.
#  - fouille du deck de rencontre ET de sa defausse :
#    `Search.EncounterCards(effect, player, include_discard_pile=True, ...)`
#    (search.py:11), puis `face.PutIntoPlay(...)` comme aa014.
#  - la conversion de `2[per_hero]` en nombre reel :
#    `Worlds.ConvertPerPlayerIconToInt("2*", effect)`, que `Search` et
#    `RemoveThreatFromSchemes` emploient deja en interne.
#
# ⚠ ARBITRAGE (utilisateur, 31/08/2026), DEUX points :
#  - « the **Lizard-Fied Minion** » ne designe aucune carte : le sbire du set
#    s'appelle « Lizard-Fied Mutant**s** » (bt020). Codee sur bt020.
#  - le texte ne dit pas ce qui arrive a 0 compteur : la manigance RESTE en
#    jeu, sa capacite cesse simplement de partir, et il faut la contrer
#    normalement. Consigne au §6 du journal de portage, points 2 et 3.
#
# ⚠ L'ASYMETRIE DU « When Revealed » EST VOULUE : 1 compteur PAR ALLIE dans la
# defausse, mais 2 PAR HEROS s'il n'y en a aucun. Le second nombre porte
# l'icone [per_hero] sur le scan, pas le premier — verifie sur l'image apres
# rotation. Un joueur qui n'a encore rien defausse prend donc le tarif plein.
#
# ⚠ « for every ally IN YOUR DISCARD PILE » : la defausse du joueur vise, pas
# celle de tout le monde (mot-piege `each` de PROCESSUS-CARTE etape 5).
#
# ⚠ « remove 1 test counter AND discard the ally » : les deux, plus la mise en
# jeu du sbire. Aucune des trois parties n'est optionnelle, et « Forced »
# confirme que le joueur ne choisit pas (mot-piege `and remove`, cout a
# plusieurs parties).

def GetAbilities() -> Sequence['Ability']:

    def compte_allies_en_defausse(player: 'Player') -> int:
        return len([f for f in player.discard_pile.Get(True) if Ally.IsType(f)])

    def mutant_science_program(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(SchemeSide2)

        joueur = message.GetToPlayer()
        if joueur is None:
            return

        allies = compte_allies_en_defausse(joueur)
        if allies > 0:
            this.PlaceCountersInternal(allies, 'test', effect)
        else:
            this.PlaceCountersInternal(
                Worlds.ConvertPerPlayerIconToInt("2*", effect), 'test', effect)

    def pioche_un_allie(effect: 'Effect', message: 'Message.AfterPlayerDrewCards') -> None:
        this = effect.this.CastTo(SchemeSide2)

        if this.GetCounters('test') <= 0:
            return

        joueur = message.to_player
        if joueur is None:
            return

        allies = [f for f in message.drew_faces if Ally.IsType(f)]
        if not allies:
            return

        this.RemoveCountersInternal(1, 'test', effect)
        Faces.DiscardAll(allies[:1], effect)

        sbire = Search.EncounterCards(
            effect,
            joueur,
            include_discard_pile=True,
            card_ids=["bt020"],
        )
        if sbire:
            sbire[0].PutIntoPlay(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            mutant_science_program,
        ),
        AbilityFactory.AfterPlayerDrewCards(
            AbilityType.ForcedResponse,
            "You",
            Ally,
            pioche_un_allie,
        ),
    ]
