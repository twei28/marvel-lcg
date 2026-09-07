from . import *

# Bandolier of Stakes — ATTACHEMENT nemesis (N 5/8). ITEM. Sans icone de boost.
# Surge. Uses (3 stake counters).
# When Revealed: You may spend 1 resource of any type to attach this card to
#   your identity. Otherwise, discard this card.
# Hero Interrupt: When your hero makes a basic attack, remove 1 stake counter
#   from here -> your hero gets +1 ATK for that attack and that attack gains
#   piercing.
#
# CARTES DE REFERENCE
#  - `39048` Bandolier of Stakes (Mojo, set Horror) : COPIE EXACTE. `desc.Uses
#    = "3,stake"`, `desc.Surge`, `player.AskSpendResources(Cost("1"), effect)`,
#    `WhenUnitMakeAttack(HeroInterrupt, "YourHero", op, is_basic_attack=True)`
#    + `CostFunc.Counter("This", 1, 'stake')`.
#
# TEXTE CONTRE CODE
#  ⚠ « YOUR hero makes a BASIC attack » -> ici `is_basic_attack=True` et
#    `GainATKForThisAttack` (qui ASSERT une attaque de base) : ce n'est PAS le
#    Bandolier du deck (bl007), qui vise « a hero attacks », toute attaque.
#  ⚠ « You MAY spend 1 resource of any type » -> `Cost("1")` : un chiffre ne
#    demande qu'un nombre (element/cost.py:35). Refuser = la carte est
#    defaussee (Surge a deja joue).
#  ⚠ Attache a l'IDENTITE : elle suit Blade et Eric Brooks, seule la face heros
#    peut s'en servir (Hero Interrupt).


def GetAbilities() -> Sequence['Ability']:

    def bandolier_revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        if EstJoueur(joueur) and joueur.AskSpendResources(Cost("1"), effect):
            this.AttachTo2(joueur.GetIdentity(), effect)
        else:
            Faces.DiscardAll([this], effect)

    def planter_un_pieu(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(this)
        message.GainATKForThisAttack(1, effect)
        message.GainPiercing(effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            bandolier_revele,
        ),
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.HeroInterrupt,
            "YourHero",
            planter_un_pieu,
            is_basic_attack=True,
        ).SetCostFunc(CostFunc.Counter("This", 1, COMPTEUR_PIEU)),
    ]
