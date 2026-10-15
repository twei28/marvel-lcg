from cards.pack import *

# ===========================================================================
# Set modulaire DARD'VAN SECT (Skrull Menace, Kajislav) — sk184-188.
# Obligatoire avec le scenario Skrull Pantheon, mais jouable avec n'importe quel
# mechant (insert p.14) : aucune carte du set ne suppose Kly'bn ni Sl'gur't.
#
# Mecanique commune : « choose a card in play with a "When Revealed" ability and
# resolve that ability » (Dard'van Priest, Sectarian Practices). Une carte en jeu
# « a » un When Revealed quand elle porte une capacite de type WhenRevealed et que
# son texte n'est pas traite comme blanc ; l'effet se resout SEUL
# (`Faces.ResolveAbility`, modele 27083 For Whom the Bell Tolls / sk046 Mole).
# ===========================================================================

ENSEMBLE = "Dard'van Sect"


def CartesAvecRevelation(effect: 'Effect') -> List['CardFace']:
    """Les cartes EN JEU qui portent un « When Revealed » resolvable (complots, mechant, sbires, environnements,
    attachements, ... ; la carte en cours de resolution n'est pas en jeu)."""
    return [f for f in Worlds.GetOnFieldCards(effect)
            if f.IsInPlay() and not f.is_treat_as_if_blank and f.effect.Find(type=AbilityType.WhenRevealed)]


def ChoisirEtResoudreRevelation(effect: 'Effect', joueur: 'Player') -> bool:
    """« Choose a card in play with a "When Revealed" ability and resolve that ability. » Le joueur choisit ;
    rend True si une capacite a ete resolue, False s'il n'y avait rien a choisir (« If you cannot »)."""
    candidates = CartesAvecRevelation(effect)
    if not candidates:
        return False
    choisie = joueur.AskChooseFace(candidates, effect)
    if choisie is None:
        return False
    Faces.ResolveAbility([choisie], joueur, AbilityType.WhenRevealed, effect)
    return True
