from . import *

# Hammer Time — EVENEMENT BASIC, cout 3, [energy]. AERIAL. ATTACK.
# Alliance. Team-Up (Beta Ray Bill and Thor). Max 1 per deck.
# Hero Action (attack): Search the encounter deck for a minion and put it into
#   play engaged with you -> deal 10 damage to that enemy. This attack gains
#   overkill.
#
# MOTS-CLES : ALLIANCE et TEAM-UP — fiches `alliance.md` et `teamup.md`, lues
# avant d'ecrire. Les DEUX sont des bases automatiques : `desc.Alliance` vaut
# `"1"` et `desc.TeamUp` vaut `"Beta Ray Bill;Thor"`. AUCUN script.
# `Max 1 per deck` est `desc.MaxPerDeck`, lu nativement lui aussi.
#
# CARTES DE REFERENCE
#  - `06005` / `br003` Hammer Throw : `AttackProperty(overkill=True)`.
#  - `al023` Little Rascals et `12020` Swarm Tactics : ⚠ UN EVENEMENT TEAM-UP
#    DOIT PORTER `.SetTarget("TeamUp")`. `database.py:223` pose un assert
#    explicite — `assert selectors[0].target_text == "TeamUp"` — des qu'un
#    evenement a `TeamUp` dans son `desc`. Sans lui, LE DECK NE MONTE AUCUNE
#    PARTIE (`AssertionError: origin_card_id='br011'` au setup), et ni
#    `test_cards` ni `test_capacites` ne le voient : encore la leçon `ls005`,
#    payee ici en une minute parce que `verifier_tous_les_decks` a ete lance
#    juste apres l'ecriture du deck.
#    C'est ce selecteur qui verifie que les DEUX personnages nommes sont en
#    jeu (identite OU allie, `GetTeamUpUnits`).
#
# TEXTE CONTRE CODE
#  ⚠ LA CARTE POSE ELLE-MEME SA CIBLE. « Search the encounter deck for a
#    minion and put it into play engaged with you » est un COUT (fleche) : on
#    convoque un sbire pour le frapper. 10 degats plus le debordement suffisent
#    a tuer la plupart des sbires, mais s'il survit, il reste engage.
#  « deal 10 damage to THAT enemy » -> celui qu'on vient de poser, pas un
#    autre : la cible n'est donc PAS choisie par `SetTarget`.
#  ⚠ Et c'est la carte qui alimente br009 Oathbrother (« after a minion enters
#    play ») : les deux se jouent ensemble.


def GetAbilities() -> Sequence['Ability']:

    def l_heure_du_marteau(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        sbire = Search.SearchForCard(
            effect, joueur,
            include_encounter_deck=True,
            card_type=Minion,
        )
        if sbire is None:
            return
        sbire.PutIntoPlay(joueur, effect)
        sbire.CastTo(Minion).EngagePlayer(joueur, effect)
        this.DealDamage([sbire], 10, effect, property=AttackProperty(overkill=True))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            l_heure_du_marteau,
        ).SetPlay().SetLabel('attack')
        .SetTarget("TeamUp"),
    ]
