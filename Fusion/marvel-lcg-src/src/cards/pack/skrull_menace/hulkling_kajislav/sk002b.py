from . import *

# Kree Origin — face B de l'upgrade d'origine (forme additionnelle).
# Upgrade PERMANENT, classe Hero, sans cout : pose au Setup par sk001b.
# Origin form. Permanent.
# Hulkling gains the [[KREE]] trait.
# Action: Exhaust this card → flip this card.
# Response: After you spend a card with the [[SKRULL]] trait, exhaust this card
#   → draw 1 card.
#
# Cartes de reference :
#  - **`as002a/as002b`** Spider Armor : upgrade PERMANENT recto-verso pose par
#    le Setup de l'alter-ego, retourne par sa propre capacite.
#  - **`17008`** Jet Boots / `01017` Cosmic Flight : « X gains the [[Aerial]]
#    trait » = `GiveKeywordToAttached(CardFinder(name=...), trait=...)`.
#  - **`65001a`** * Wave : Ability brute sur `AfterCardsBeSpendAsResource`
#    (« after you spend »), cartes depensees dans `message.faces`.
#  - Le changement de FORME additionnelle : `Identity.ChangeAdditionalFrom`,
#    chemin de `Form.ChangeFormInternal` (Vision 26001, Shadowcat). Voir
#    `ChangerDOrigine` dans le __init__ du set.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Hulkling** gains » : NOM PROPRE de la face heros. En forme civile,
#    Teddy Altman (HYBRID) n'a ni KREE ni SKRULL. `CardFinder(name="Hulkling")`
#    et pas "You" (piege an002).
#  - « Origin form » : retourner = CHANGER DE FORME (livret p. 4). Ne compte
#    PAS dans la limite d'un passage heros/civil par tour, mais declenche
#    tout « after you change form » (sk001b, sk004, sk006).
#  - « **Action** » (pas Hero Action) : utilisable dans les DEUX formes.
#  - « spend a card **with the SKRULL trait** » : le trait OPPOSE a celui que
#    donne cette face. Seule une carte DEFAUSSEE DE LA MAIN compte (decision
#    utilisateur du 15/10/2026 : Excelsior en jeu ne « depense » rien).
#  - « exhaust this card → » : la fleche fait de l'inclinaison un COUT ;
#    une origine deja inclinee (par son Action) ne pioche pas.
#  - « Permanent. » : base automatique (desc.Permanent), aucun script.
#  - Pas de limite imprimee : l'inclinaison en tient lieu.


def GetAbilities() -> Sequence['Ability']:
    return OrigineAbilities(trait_donne="KREE", trait_depense="SKRULL")
