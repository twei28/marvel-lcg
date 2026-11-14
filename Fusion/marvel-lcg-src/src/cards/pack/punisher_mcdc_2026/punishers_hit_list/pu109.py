from . import *

# Punisher's Katana — ATTACHEMENT. ARMAMENT. WEAPON. ATQ +1★, Boost ★+1.
# ★ Punisher's attacks gain piercing.
# When Revealed : Find Punisher, reveal him, and attach this to him. Resolve his "Punishment" ability.
# ★ Boost : If this attack defeats an ally, add a counter to Punisher's Hit List.
#
# Cartes de reference : `Find.FindAndReveal` (pu065), gs083 (`UnitAttackGainKeyword("AttachedCharacter", ...)`),
# mut_gen/sabretooth/32069.py (`would_atk_message.IfThisAttackDefeats(Ally, ...)`), `AttachTo2`.
# ⚠ « attach this TO HIM » : quand l'arme est revelee, elle s'attache au Punisher qu'on vient de trouver (pas au vilain).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        punisher = Find.FindAndReveal(effect, joueur, name="Punisher", card_type=Minion)
        if punisher is not None:
            this.AttachTo2(punisher, effect)
        Punishment(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.would_atk_message.IfThisAttackDefeats(Ally, lambda cible: AjouterUnCompteurALaListe(effect), effect)

    return [
        AbilityFactory.UnitAttackGainKeyword("AttachedCharacter", piercing=True),
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
