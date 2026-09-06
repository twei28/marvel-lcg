from . import *

# * Electro Noir — SBIRE nemesis (N 2/5). CRIMINAL. ELITE. UNIQUE.
#   MNG 1* / ATQ 1* — 6 PV, 2 icones de boost. Retaliate 1.
# [star] Forced Interrupt: When Electro Noir activates against you, give him a
#   random encounter card tucked under your identity as a boost card.
#   Otherwise, give him a facedown boost card from the top of the encounter
#   deck.
#
# ⚠ LA CARTE QUI RETOURNE LE PACK CONTRE LUI-MEME. Chaque carte glissee sous
# l'identite est +1 ATQ et +1 CTR pour le heros ; Electro la lui PREND pour
# s'en faire une carte de boost. Il frappe donc d'autant plus fort que le
# heros etait fort, et le laisse a 0/0 s'il vide la pile.
#
# MOTS-CLES (fiches lues avant d'ecrire)
#  - `retaliate` (mots-cles/retaliate.md) : BASE AUTOMATIQUE,
#    `desc.Retaliate = "1"`. AUCUN SCRIPT.
#  - `special` (mots-cles/special.md) : le `[star]` n'a pas de mention « In
#    expert mode », il est donc code TOUJOURS actif. Il porte ici un type
#    imprime (`Forced Interrupt`), c'est donc ce type qu'on ecrit.
#  - ⚠ `ELITE` N'EST PAS UN MOT-CLE, c'est un TRAIT : il va dans `traits`,
#    jamais dans `desc` (encadre du README des mots-cles).
#
# CARTES DE REFERENCE
#  - `WhenEnemyWouldActivate` / `WhenEnemyActivateAgainstYou` : la fenetre
#    « when X activates against you ».
#  - `sd020` Inspirational Art : le pipeline complet des cartes de boost, et
#    `GiveBoostCard` / `GiveFacedownBoostCards` pour en donner une.
#  - `02035` Intimidation : `Faces.GiveFacedownBoostCards(<ennemis>, 1, effect)`.
#  - `Rand.RandomChoice` : « a RANDOM encounter card ».
#
# TEXTE CONTRE CODE
#  ⚠ « a random ENCOUNTER CARD tucked under your identity » -> UNE CARTE DE
#    RENCONTRE, pas n'importe laquelle. La pile peut contenir un SBIRE vaincu
#    glisse par `sn002`, un complot annexe glisse par `sn009`, une traitrise
#    glissee par `sn001a` : toutes sont des cartes de rencontre. Le filtre est
#    donc large, mais il est ecrit — une carte JOUEUR ne pourrait pas servir
#    de carte de boost.
#  ⚠ « OTHERWISE » -> le repli n'est PAS un choix : il tombe quand la pile ne
#    contient aucune carte de rencontre. Mot-piege « otherwise » (branche
#    alternative non codee), releve a l'etape 5.
#  « as a BOOST CARD » -> elle rejoint le paquet de boost d'Electro, elle
#    n'est pas defaussee : ses icones compteront a son activation.
#  « against YOU » -> le joueur engage avec lui.


def GetAbilities() -> Sequence['Ability']:

    def se_nourrir_de_la_pile(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        joueur = this.GetEngagedPlayer()
        if not Player.IsType(joueur):
            return
        identite = joueur.GetIdentity()

        candidates: List['CardFace'] = []
        if identite is not None:
            candidates = [f for f in identite.GetPlacedCardArea().Get()
                          if f is not None and EncounterNonVillainCard.IsType(f)]

        if candidates:
            volee = Rand.RandomChoice(candidates, effect)
            this.GiveBoostCard(volee, effect)
        else:
            # « Otherwise, give him a facedown boost card from the top of the
            #   encounter deck. »
            Faces.GiveFacedownBoostCards([this], 1, effect)

    return [
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.ForcedInterrupt,
            "This",
            se_nourrir_de_la_pile,
        ),
    ]
