from . import *

# Savage Destruction — traitrise NEMESIS (5/5). Boost 1.
# When Revealed: If Sav'rkk is in play, he attacks you. Otherwise, summon
#   Sav'rkk and reveal him.
#
# Cartes de reference :
#  - `yd017` Hard to Kill, sa JUMELLE de structure : meme « Otherwise, summon
#    Sav'rkk and reveal him », seule la premiere moitie change (il ATTAQUE au
#    lieu de se soigner). Deux cartes au texte quasi identique dont une seule
#    ligne differe : exactement le genre de paire ou un copier-coller se voit
#    en partie et pas en lecture (leçon vp014/vp015).
#  - `27082` Biting Retort / `45075a` pour `minion.DoActivate(joueur, effect)`,
#    qui fait AGIR un ennemi hors de son tour.
#  - `ConvoquerRencontre` (helper du set) pour le mot-cle MAISON `summon`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « he **ATTACKS** you » : une attaque, pas une activation libre — un sbire
#    qui « s'active » pourrait manigancer. Il faut donc la branche ATTAQUE de
#    `DoActivate`, comme le fait `Puzzle.Attack` cote harnais.
#  - « **Otherwise** » : les deux moities s'EXCLUENT.
#  - « summon ... **and reveal him** » : en jeu, pas en main.
#  - Aucune icone [star] ici, contrairement a `yd017` : cette carte n'a PAS de
#    capacite de boost. Ne pas en inventer une par symetrie.


def GetAbilities() -> Sequence['Ability']:

    def savage_destruction(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        savrkk = Worlds.FindCardOnField(effect, name="Sav'rkk", card_type=Minion)

        if savrkk is not None:
            if joueur is not None:
                savrkk.CastTo(Enemy).DoAttackYou(joueur, effect)
            return

        # « Otherwise, summon Sav'rkk and reveal him. »
        trouve = ConvoquerRencontre(effect, "Sav'rkk", Minion)
        if trouve is not None:
            trouve.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            savage_destruction,
        ),
    ]
