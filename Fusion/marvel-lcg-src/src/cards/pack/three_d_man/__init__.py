from cards.pack import *

# ===========================================================================
# Pack 3-D MAN (Delroy Garrett Jr.) : contenu fan-made de R. Tim Morris (zip
# « 3-D Man », scans EN seuls). Prefixe `dm` (tools/prefixes_fanmade.json),
# set 252. Un seul deck : `three_d_man` (decklist complete fournie par
# l'auteur, starter deck.png).
#
# Restriction de deck-construction IMPRIMEE sur l'alter-ego (dm001b) : le
# deck ne peut contenir que des cartes a 3 ressources (hors cartes
# ressource), jusqu'a 3 aspects d'evenements differents. Consequence directe :
# toutes les cartes de heros signature (sauf Tri-Force Vision et 3-D Man's
# Suit / True Sight, a 1) coutent 3, et les cartes d'aspect bonus de l'auteur
# (dm016-dm021) sont des REECRITURES a 3 couts de cartes de base/aspect
# existantes (She-Hulk, Number Cruncher) ou de nouvelles cartes a 3 couts
# pensees pour cette restriction.
#
# DEUX sets : `3-D Man` (dm001a-dm011 : identite, 9 textes de heros sur 15
# cartes, obligation Arrival of the Triple-Evil!) et `3-D Man Nemesis`
# (dm012-dm015 : Secret Initiative, Magnitude, Skrull Invaders, Skrull
# Infiltrator). dm016-dm021 : six cartes d'aspect/basique fournies par
# l'auteur (set_name vide, scripts ICI, a la racine du pack, modele
# `multiple_man/mm023.py`). dm022-dm024 : reskins Energy/Genius/Strength,
# sans script.
#
# Deux primitives moteur ajoutees pour ce pack (04/11/2026) :
#  - `Message.AfterPlayerLookedAtEncounterDeck` / `AbilityFactory.
#    AfterPlayerLookedAtEncounterDeck` (pose depuis `PlayerAction.
#    LookAtDeck`) : necessaire a dm012 Secret Initiative.
#  - compteurs `skrull` et `apostasy` ajoutes a `card_face.py` (COUNTER).
# ===========================================================================


def EstJoueur(objet: Any) -> bool:
    """`Player.IsType` SANS le risque d'AttributeError (lecon sf002 / sf013)."""
    return objet is not None and hasattr(objet, "IsPlayer") and Player.IsType(objet)


def Hote(face: 'CardFace|None') -> 'CardFace|None':
    """L'hote d'un attachement (modele `blade_nemesis.Hote`, `face.bind_face`)."""
    return getattr(face, "bind_face", None) if face is not None else None


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (modele `carnage_eddie_brock.JoueurDeCetteCarte`) : ⚠ jamais
    `effect.GetInitiator()` en premier -- il leve un assert quand l'initiateur n'est pas un joueur (ex. le
    vilain, qui revele l'obligation dm011 a sa place). AJOUTE le 04/11/2026 : `dm007` l'appelait deja sans que
    ce pack ne la definisse -- latent jusqu'au premier cas de test (`tools/cas/three_d_man.py`)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if EstJoueur(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if EstJoueur(initiateur):
        return initiateur
    return None


def CoutReduit(effect: 'Effect') -> bool:
    """« If you reduced this card's cost » (dm003-dm006, dm018-dm019, dm021) : compare le cout REELLEMENT
    facture au paiement (`effect.context.paid_this_cost`, deja reduit par 3-D Man / 3-D Man's Suit / The Triune
    Understanding / Number Cruncher au moment du calcul) au cout IMPRIME de la carte (`this.printed_cost`).
    ⚠ Ce n'est PAS `effect.GetCostX()` (effect.py:519) : cette methode compare les ressources PAYEES au cout
    FACTURE (deja reduit), donc elle mesure un SURPAIEMENT, jamais une reduction — a 0 meme quand la carte a
    ete reduite et payee pile. Carte de reference pour `paid_this_cost` : `ca013` Rend (`effect.GetCostX()`),
    dont la lecture du champ a ete tracee jusqu'a `effect_context.py:17` pour cette distinction."""
    this = effect.this
    if not HasCost.IsType(this):
        return False
    return effect.context.paid_this_cost.val < this.printed_cost.val
