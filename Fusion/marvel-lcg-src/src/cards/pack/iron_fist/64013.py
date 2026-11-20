from . import *

# 22/10/2026 : carte OFFICIELLE du pack Iron Fist (MC64, n° de collection 13), ex-`up015` (aspects TMNT d'Inkwire, meme texte). `up015` n'existe plus : c'est maintenant
# l'art alternatif « tmnt » de `64013` (data/arts_alternatifs.json). Script, cas et gabarit PROCESSUS-CARTE repris tels quels.
# Helpful Bystander — ALLIE 1 [physical], aspect Protection (TMNT Aspects, Inkwire). CIVILIAN.
# THW –, ATK –, PV 1.
# Vulnerable. Max 1 per deck.
# Your hero gets +1 hand size.
# Forced Interrupt: When an enemy attacks you, it attacks Helpful Bystander instead. This attack gains
#   overkill.
#
# NOUVELLE. MOTS-CLES (fiches lues AVANT le code) : Vulnerable (vulnerable.md, `desc.Vulnerable`, aucun
# code), Overkill (overkill.md : « this attack gains overkill » = `message.GainOverKill(effect)` sur le
# message d'attaque). « Max 1 per deck » = `desc.MaxPerDeck`. ATK/THW « – » : cles absentes de `desc`
# (comme la THW de `01050` Hulk).
#
# CARTES DE REFERENCE
#  - `40079` Morlock : « When an enemy attacks you, it attacks X instead » =
#    `WhenUnitWouldAttack(ForcedInterrupt, Enemy, ..., against_player="You")` + `message.ReplaceTarget(this)`.
#  - `an002` Sera : « <hero> gets +1 hand size » depuis un allie =
#    `GiveKeywordToInPlayWhenApplyThis(Hero, control_by="You", hand_size=1)`.
#  - `an013` Hel-Wolf / overkill.md : `attaque.GainOverKill(effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « Your HERO gets +1 hand size » : le heros du joueur (forme heros) ; en alter-ego, pas de bonus
#    (lecture litterale, comme an002).
#  ⚠ « When an enemy attacks YOU » : attaque contre le joueur (pas contre un allie) ; Forced = obligatoire.
#  ⚠ « it attacks Helpful Bystander INSTEAD » : la cible est remplacee (pas une 2e attaque).
#  ⚠ « THIS attack gains overkill » : l'attaque redirigee : l'exces apres les 1 PV va a l'identite
#    (overkill.md : allie vaincu -> identite du controleur).


def GetAbilities() -> Sequence['Ability']:

    def helpful_bystander(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)
        message.ReplaceTarget(this)
        message.GainOverKill(effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Hero,
            control_by="You",
            hand_size=1,
        ),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            Enemy,
            helpful_bystander,
            against_player="You",
        ).SetTarget("Attacker"),
    ]
