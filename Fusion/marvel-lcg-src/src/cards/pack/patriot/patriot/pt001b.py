from . import *

# * Elijah Bradley (face alter-ego) — custom « CptScorp »
# PV 11 / REC 3 / MNG 6, trait CIVILIAN.
#
# Leader — During deck building you may include YOUNG AVENGER allies from any
#   aspect.
# Action: Exhaust Elijah Bradley -> search your deck and discard pile for the
#   Patriot's Shield and add it to your hand. Shuffle your deck.
#
# ---------------------------------------------------------------------------
# « LEADER » N'EST PAS UNE CAPACITE DE JEU : RIEN A CODER ICI
#
# C'est une REGLE DE DECK-BUILDING. Le moteur ne valide JAMAIS un deck au
# chargement (GUIDE §5.2) ; ces regles vivent dans le deck-builder,
# `public/js/deckbuilder/app.js`, fonction `exemptDeLaLimiteAspect(hero,
# carte)` (GUIDE §14.1) — la meme fonction qui porte deja *Arachnophilia* de
# Cassandra Webb. La regle y est ajoutee ; aucune capacite ne la rend en jeu,
# et il ne faut surtout pas en inventer une (mot-piege « mot-cle cite mais
# pas imprime sur CETTE carte » du PROCESSUS-CARTE §5).
#
# ⚠ Elle n'a AUJOURD'HUI aucune cible legale : les deux seuls allies YOUNG
# AVENGER du catalogue sont `il002` Stature et `wc002` Hulkling, tous deux de
# classe `Hero`, donc signatures d'autres heros, interdites de deck. Ecart
# documente, pas corrige : on n'invente pas de cible.
#
# ---------------------------------------------------------------------------
# « Action: » NU SUR UNE FACE ALTER-EGO -> `AbilityType.Action`
#
# Modeles : Bruce Banner (10001b), Tony Stark (01029b), Sharon Carter
# (ag001b), Remy LeBeau (37001b), Billy Kaplan (wc001b). `AlterEgoAction`
# designe un AUTRE type d'abilite, reserve aux cartes JOUEUR qui doivent
# declarer ce mode puisqu'elles ne sont pas elles-memes la face alter-ego.
#
# ---------------------------------------------------------------------------
# LA FLECHE EST UN COUT -> UN EFFET
#
# Cout = « Exhaust Elijah Bradley », rendu par
# `.SetCostFunc(CostFunc.Exhaust("This"))`. Le moteur ne propose pas la
# capacite quand la face est deja inclinee (`selector_filter.AddParameter(
# canbe_exhaust=True)`, cost_func.py:227) : cout impayable = rien ne se
# passe, sans une ligne de garde a ecrire.
#
# ---------------------------------------------------------------------------
# ⚠ CHERCHER « Patriot's Shield » SANS L'ETOILE
#
# `pt012` s'appelle « * Patriot's Shield » dans cards.json, mais
# `cards/paper.py:45-46` retire le prefixe « * » d'un nom unique : le nom
# effectif est « Patriot's Shield ». Un `name="* Patriot's Shield"` ne
# trouverait JAMAIS rien, EN SILENCE. D'ou la constante
# `NOM_PATRIOTS_SHIELD`, ecrite sans etoile.
#
# « search your deck AND DISCARD PILE » -> `include_player_deck=True` ET
# `include_discard_pile=True`. « Shuffle your deck » est fait par la
# recherche elle-meme : `SearchForCardsInternal` construit son selecteur avec
# `not_shuffle=False` (search_internal.py:61-66), donc le deck fouille est
# remelange. Aucune ligne a ajouter — modele `gp007` Gwen's Room, meme couple
# `Search.PlayerCard(...)` + `player.GainCard(face, effect)`.
#
# La recherche n'est PAS optionnelle (`may` reste a False) : le texte dit
# « search ... and add it to your hand », pas « you may search ». Si le
# bouclier est deja en main ou en jeu, la recherche ne trouve rien et
# l'action est simplement sans effet — elle aura quand meme incline Elijah,
# ce qui est la lettre de la carte.


def GetAbilities() -> Sequence['Ability']:

    def chercher_le_bouclier(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return

        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            name=NOM_PATRIOTS_SHIELD,
        )
        if face:
            joueur.GainCard(face, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            chercher_le_bouclier,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetName("Search for the Patriot's Shield"),
    ]
