from . import *
# On the Prowl — EVENEMENT, cout 2, [mental]. TACTIC. THWART. x2.
# Hero Action (thwart): Remove 4 threat from a scheme. If you paid for this
#   using only [mental] resources, remove an additional 2 threat from that
#   scheme, and this card ignores the crisis icon and patrol keyword.
#
# Modeles : 90119 Search and Rescue (`ignore_crisis=True` a la resolution),
# 15012 Crisis Averted (ignorance DECLAREE sans condition, la resolution
# tranche selon le paiement). Fiche mots-cles/crisis.md, section du
# 11/09/2026 : depuis que la Crise verrouille la CIBLE, un contre qui peut
# l'ignorer doit le declarer par `SetIgnoreKeyword`, sinon le complot
# principal ne lui est plus propose. Patrouille verrouille de la meme facon
# (`MainScheme.CanBeThwartBy`).
#
# ⚠ CAS LIMITE, identique a 15012 : l'ignorance depend du PAIEMENT, qui vient
#   APRES le ciblage. Declaree par `paid_with="B", only=True`, la carte reste
#   ciblable ; payee autrement qu'en mental seulement sous Crise, elle ne
#   retire rien (la resolution applique la regle), et le PLATEAU DEMANDE
#   CONFIRMATION avant d'envoyer un tel paiement (mots-cles/crisis.md,
#   « paid_with »). Gate : tools/verifier_ignore_crise.py.

def GetAbilities() -> Sequence['Ability']:

    def on_the_prowl(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        mental = PayeSeulementEnMental(effect)
        this.RemoveThreatFromSchemes(effect.targets, 6 if mental else 4, effect, ignore_crisis=mental)

    # Au CIBLAGE rien n'est encore paye : la cible reste offerte. A la
    # RESOLUTION le paiement est connu : la Crise (et la Patrouille) ne
    # s'ignorent que payees en mental SEULEMENT (`only=True` : OnlyHasColor).
    # (Corrige le 11/09/2026 : declaree SANS condition, l'ignorance valait
    # aussi a la resolution et la Crise ne mordait plus jamais — le temoin
    # « payee en energie sous Crise » l'a vu.)
    # ⚠ MODALE (11/09/2026 au soir) : la forme `paid_with` remplace la lambda
    # maison. Meme regle, et en plus le rendu sait prevenir le joueur qui va
    # payer avec autre chose que du mental sous une Crise (voir 15012).
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            on_the_prowl,
        ).SetPlay().SetLabel('thwart')
        .SetIgnoreKeyword('Crisis', 'Patrol', paid_with="B", only=True)
        .SetTarget(Scheme2),
    ]
