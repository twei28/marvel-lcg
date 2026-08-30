from . import *

# "I'm Out" — EVENEMENT signature, custom « CptScorp »
# Cout 2, [mental], classe Hero, traits SUPERPOWER / TACTIC. Un seul
# exemplaire dans le deck.
# Hero Interrupt: When you reveal an encounter card, cancel the effects of
#   that card and discard it. If you would resolve Speed's "Hyperkinetic Fuel"
#   ability when playing this event, shuffle 1 event from your discard pile
#   into your deck and draw 1 card instead.
#
# ---------------------------------------------------------------------------
# BLOC 1 : l'annulation. Le libelle imprime est celui de Spycraft (08018),
# Lucky Break (40048) et Foresight (mw009), MOT POUR MOT. Modele le plus
# proche : `mw009` — un EVENEMENT, un Hero Interrupt, rien d'autre autour.
#
#   `AbilityFactory.WhenPlayerRevealCard(AbilityType.HeroInterrupt, "You",
#    None, "All", ..., from_encounter=True)` + `message
#    .CancelAllEffectsAndDiscardIt(effect)`.
#
# Le niveau d'annulation `"All"` (et non `"WhenRevealed"`) est ce que dit le
# texte : « cancel THE EFFECTS of that card », donc tout, mots-cles et
# deferlement compris (sender_card.py:473-476 le commente explicitement, et
# c'est la lecon Dazzler n°5). `from_encounter=True` restreint bien la
# revelation au deck de rencontre.
#
# Difference avec mw009 : Foresight paie « exhaust Madame Web », pas "I'm
# Out". Aucun `SetCostFunc` ici, il n'y a pas de cout imprime au-dela du cout
# de la carte.
#
# ---------------------------------------------------------------------------
# BLOC 2 : le « instead ». Il ne vit PAS dans ce fichier, et c'est voulu.
#
# « If you would RESOLVE Speed's Hyperkinetic Fuel ability WHEN PLAYING THIS
# EVENT » : c'est la capacite du HEROS (sd001a) qui doit demander « la carte
# que je suis en train de voir payer est-elle sd005 ? ». Cette carte-ci n'a
# aucun moyen de se voir en train d'etre payee — quand son propre effet se
# resout, Hyperkinetic Fuel a deja tranche.
#
# Le couplage passe donc par la constante partagee
# `CARTES_QUI_REMPLACENT_HYPERKINETIC_FUEL` et l'aide
# `RemonterUnEvenementEtPiocher` (speed/speed/__init__.py), toutes deux lues
# par sd001a.py.
#
# PORTEE DU « INSTEAD » : il remplace LA RESOLUTION DE HYPERKINETIC FUEL
# (donc : pas de compteur explosif), PAS l'annulation de la carte rencontre,
# qui reste due dans tous les cas. Le texte le dit deux fois : « if you would
# resolve SPEED'S ability », et l'echange propose (remonter un evenement +
# piocher) est exactement la phrase de sd001b, pas une variante de
# l'annulation.
#
# ⚠ La ressource IMPRIMEE de cette carte est MENTALE : le cas « payee
# uniquement en energie » est reel (une main de wilds, Never Ending Spark
# sd015, Top Speed sd011/sd012) mais jamais automatique. Le cas de test dedie
# le construit expres, sans quoi la branche ne serait jamais exercee.


def GetAbilities() -> Sequence['Ability']:

    def im_out(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.CancelAllEffectsAndDiscardIt(effect)

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "You",
            None,
            "All",
            im_out,
            from_encounter=True,
        ).SetPlay().SetLabel(),
    ]
