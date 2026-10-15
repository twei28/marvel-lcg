from . import *

# * Fickle Alliance — COMPLOT ANNEXE DE JOUEUR (Leadership / Campaign, n° 272). Cout 0, menace de depart 3.
# Victory 0.
# When Defeated: The player who defeated this scheme may search the encounter deck for a non-ELITE minion and
#   put it into play under their control. (Shuffle.) Treat that minion as an ally with a blank text box
#   (except for TRAITS). Its THW is equal to its printed SCH and it takes 1 consequential damage after it
#   thwarts or attacks.
#
# Cartes de reference :
#  - **`60145`** Baron Zemo (conversion sbire <-> allie) et **`fne/kingpin/__init__.py`** `ConvertirBlackCatEnAlliee` :
#    « treat a minion as an ally » = `Faces.TreatAsAlly(sbire, gabarit_allie, joueur, effect)` (operate/faces.py :
#    recopie nom, image, ATQ et SCH -> THW ; texte BLANC puisque le gabarit n'a aucune capacite ; les degats
#    consecutifs viennent des etoiles du gabarit `skrull_fickle_ally`, ATK 0* / THW 0*).
#  - **`bw002`** : « search the encounter deck for a minion » = `Search.EncounterCard(effect, joueur,
#    include_discard_pile=False, card_type=Minion, non_trait="ELITE", may=True)`.
#  - **`hd010`** : `WhenSchemeBeDefeated(..., has_defeating_player=True)` + `GetDefeatingPlayer()`.
#
# ⚠ Mots-pieges :
#  - « non-ELITE minion » : tout sbire non Elite du deck RENCONTRE (pas la defausse), de n'importe quel set ;
#  - « (except for TRAITS) » : les traits du sbire sont CONSERVES (gabarit sans trait, traits recopies) ;
#  - « Its THW is equal to its PRINTED SCH » : MNG imprime, pas courant ; « 1 consequential damage after it
#    thwarts OR attacks » : une etoile sur THW et une sur ATK du gabarit ;
#  - « under their control » : sous le controle du joueur qui a vaincu le complot ; « (Shuffle.) » : par defaut
#    de la recherche.


def GetAbilities() -> Sequence['Ability']:

    def recompense(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)
        vainqueur = message.GetDefeatingPlayer()
        if vainqueur is None:
            return
        sbire = Search.EncounterCard(
            effect,
            vainqueur,
            include_discard_pile=False,
            card_type=Minion,
            non_trait="ELITE",
            may=True,
        )
        if sbire is None:
            return
        traits = list(sbire.traits)

        def reprendre_le_sbire(allie: 'Any', ancien: 'Any') -> None:
            # PV du sbire (le gabarit en a 0) : l'allie en a autant, sinon il est vaincu en entrant en jeu.
            allie.printed_health = ancien.printed_health
            allie.printed_health_numeral = ancien.printed_health_numeral
            allie.starting_health = ancien.starting_health

        # ⚠ L'effet donne a `TreatAsAlly` ne doit PAS etre celui du complot : le moteur rend l'allie a sa forme de
        # sbire des que `effect.this` QUITTE LE JEU (modele : une amelioration de controle mental), or le complot
        # vaincu part en pile de victoire juste apres. `GameRule(sbire)` : une source qui ne quitte jamais le jeu
        # (la face sbire n'est plus celle de la carte) ; l'allie ne redevient sbire qu'en quittant le jeu lui-meme.
        from game.effect.rule import GameRule
        if Faces.TreatAsAlly(sbire, GABARIT_ALLIE_FICKLE, vainqueur, GameRule(sbire), process=reprendre_le_sbire):
            # « (except for TRAITS) » : les traits imprimes du sbire restent ceux de l'allie. Poses APRES
            # l'echange (l'initialisation de la face les remet a ceux du gabarit, aucun).
            allie = sbire.card.face
            for trait in traits:
                allie.traits_internal[trait] = [allie]

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            recompense,
            has_defeating_player=True,
        ),
    ]
