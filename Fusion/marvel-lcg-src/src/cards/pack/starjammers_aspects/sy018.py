from . import *
# * Blade of the Phoenix (Aggression, amelioration 1 [energy][mental]). ARTIFACT. WEAPON. Unique.
# Linked (Korvus Rook'shir). Attach to an ally.
# Attached ally gets +2 ATK. If the attached ally doesn't have the PSIONIC trait, it takes +1 consequential damage after it attacks.
#
# Cartes de reference : 01074 Inspired (`CanPlayThisUpgradeCard(Ally)` + `*GiveKeywordToAttached(Ally, thwart=1)`) ; bc002
# (`attack_consequential_damage` de `GiveKeywordToAttached`, RECETTES §5 : ajouter un degat consequent passe par la VALEUR, jamais par un
# temp sur `WhenAllyWouldTakeConsequentialDamage`) ; fiche linked.md (« Linked » = mise de cote par la creation de Korvus).
# « If the attached ally doesn't have PSIONIC » : le +1 depend du trait du porteur, relu quand ses traits changent.
# ⚠ Un allie a 0 degat consequent imprime n'en subit pas non plus : le +1 s'ajoute a la valeur imprimee (Korvus 1* -> 2).
def GetAbilities() -> Sequence['Ability']:
    def sans_psionic(effect: 'Effect', face: 'CardFace', ui: List['CardFace']) -> int:
        return 0 if face.HasTrait("PSIONIC") else 1
    return [
        AbilityFactory.CanPlayThisUpgradeCard(Ally),
        *AbilityFactory.GiveKeywordToAttached(Ally, attack=2),
        *AbilityFactory.GiveKeywordToAttached(
            Ally,
            attack_consequential_damage=1,
            get_new_value=sans_psionic,
            ex_change_on_event=OnEvent.Trait("YourAlly"),
        ),
    ]
