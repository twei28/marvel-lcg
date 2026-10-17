from . import *

# Santōryū Ōgi — AMELIORATION SKILL, classe Bushido (Inkwire, TMNT Shinobi). Cout 0, [wild].
# Max 1 per deck. Attached upgrade loses the restricted keyword.
# Response: After this card enters play, search your deck and discard pile for a WEAPON upgrade. (Shuffle.) Put that upgrade into
#   play (paying its resource cost) with this card attached.
#
# ⚠⚠ CARTE NON TERMINEE : LECTURE PROVISOIRE, voir `.planning/tmnt/shinobi-bushido-questions.md` (Q-B2). Le texte imprime ne dit pas
# OU cette carte s'attache quand on la joue (aucun « Attach to »), ni ce qu'elle devient si la recherche ne ramene rien ; « attached
# upgrade » et « with this card attached » designent l'amelioration ARME qui la porte. LECTURE CODEE :
#  - jouee comme toute amelioration sans « Attach to » : elle entre en jeu attachee a l'IDENTITE du joueur ;
#  - Reponse : recherche dans le deck ET la defausse d'une amelioration WEAPON (melange), la met en jeu en PAYANT son cout, puis cette
#    carte SE DETACHE de l'identite et s'attache a cette arme ;
#  - tant qu'elle est attachee a une amelioration, celle-ci perd le mot-cle Restricted (elle ne compte plus dans la limite de deux).
#  - sans arme trouvee / jouable (aucune arme, cout impayable), la carte reste attachee a l'identite.
#
# Mots-cles (fiches lues AVANT le code) : Restricted (restricted.md : compteur `Restricted` lu dans `desc`, limite de deux par heros
# via `limit_restricted`) ; « Max 1 per deck » : base automatique (`desc.MaxPerDeck = "1"`, verifiee au deck-builder).
#
# Cartes de reference :
#  - « search your deck and discard pile for X ... and put it into play, paying its cost » : `superior_iron_man/si008` Stark Island
#    (`Search.PlayerCard(include_player_deck=True, include_discard_pile=True, ...)` + `joueur.PlayACard(face, True)`, mecanisme
#    cree pour ce texte) ;
#  - une carte qui s'attache A POSTERIORI a une autre : `CanAttach.AttachTo2(hote, effect)` (`player_actions` du moteur) ;
#  - « attached upgrade loses/gains a keyword » : `GiveKeywordToAttached(card_finder, apply=fn)` (`apply(effect, hote, diff)` :
#    +1 a l'attache, -1 au detachement) et `HasRestricted.GainRestricted` (compteur du mot-cle).
#
# TEXTE CONTRE CODE
#  ⚠ « Attached UPGRADE loses the restricted keyword » : l'amelioration qui porte cette carte (l'arme), pas le heros.
#  ⚠ « search your deck AND discard pile » : les deux a la fois ; « a WEAPON upgrade » : trait WEAPON, type amelioration ;
#    « (Shuffle.) » : melange apres la recherche.
#  ⚠ « (paying its resource cost) » : le cout de l'arme est PAYE (pas de mise en jeu gratuite) ; arme impayable : elle n'entre pas en jeu.
#  ⚠ « Max 1 per deck » : une seule copie dans le deck (verifiee au deck-builder, `MaxPerDeck`).


def GetAbilities() -> Sequence['Ability']:

    def perd_restricted(effect: 'Effect', hote: 'CardFace', diff: int) -> None:
        # +1 quand cette carte s'attache, -1 quand elle se detache : on retire (resp. rend) le compteur Restricted imprime de l'hote.
        if HasRestricted.IsType(hote) and hote.printed_restricted:
            hote.GainKeyword(-diff * hote.printed_restricted, 'Restricted', effect)

    def ogi(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = this.GetControlByPlayer()
        if joueur is None:
            return
        arme = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            trait="WEAPON",
            card_type=Upgrade,
        )
        if arme is None:
            return
        joueur.PlayACard(arme, True)
        if arme.IsInPlay():
            this.AttachTo2(arme, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(Upgrade, apply=perd_restricted),
        AbilityFactory.AfterCardEnterPlay(AbilityType.Response, "This", ogi),
    ]
