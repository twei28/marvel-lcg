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
# ⚠ CAS LIMITE ASSUME, identique a 15012 : l'ignorance depend du PAIEMENT, qui
#   vient APRES le ciblage. Declaree sans condition, la carte reste ciblable ;
#   payee sans « mental seulement » sous Crise, elle ne retire rien (la
#   resolution applique la regle). Le bandeau « Crise » du plateau previent.
#   Gate : tools/verifier_ignore_crise.py.

def GetAbilities() -> Sequence['Ability']:

    def on_the_prowl(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        mental = PayeSeulementEnMental(effect)
        this.RemoveThreatFromSchemes(effect.targets, 6 if mental else 4, effect, ignore_crisis=mental)

    def si_paye_en_mental_seulement(effect: 'Effect') -> bool:
        # Au CIBLAGE rien n'est encore paye : on laisse la cible offerte. A la
        # RESOLUTION le paiement est connu : la Crise ne s'ignore que payee en
        # mental seulement. (Corrige le 11/09/2026 : declaree SANS condition,
        # l'ignorance valait aussi a la resolution et la Crise ne mordait plus
        # jamais — le temoin « payee en energie sous Crise » l'a vu.)
        paye = effect.GetPaidResources()
        if paye.val == 0:
            return True
        return paye.OnlyHasColor("B")

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            on_the_prowl,
        ).SetPlay().SetLabel('thwart')
        .SetIgnoreKeyword('Crisis', 'Patrol', condition=si_paye_en_mental_seulement)
        .SetTarget(Scheme2),
    ]
