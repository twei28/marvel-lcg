from . import *

# * Spider-Man (Otto Octavius) — HEROS. THW 2 / ATK 2 / DEF 2, main 5, 10 PV.
# AVENGER. WEB-WARRIOR.
# Spider-Sense — Interrupt: When the villain OR A VILLAINOUS MINION initiates
#   an attack against you, draw 1 card.
#
# CARTES DE REFERENCE
#  - `01001a` * Spider-Man (Peter Parker, Core Set) : LE modele, meme nom de
#    capacite et meme fabrique
#    `WhenUnitInitiatesAttackAgainst(Interrupt, <attaquant>, "You", op)`.
#
# TEXTE CONTRE CODE
#  ⚠⚠ « THE VILLAIN **OR A VILLAINOUS MINION** » : la carte officielle `01001a`
#    dit seulement « when the villain initiates an attack », et son module vise
#    donc `Villain` tout court. Rainy a ELARGI la capacite, et recopier le
#    module officiel tel quel la rendrait deux fois moins bonne — sans que rien
#    ne le signale. D'ou le `CardFinder(check_face_fn=...)` : le vilain, OU un
#    sbire portant `Villainous`.
#  ⚠ « VILLAINOUS » est une base automatique lue dans `desc` (fiche
#    `mots-cles/villainous.md`) : on la LIT ici (`face.villainous`), on ne la
#    recode pas.
#  ⚠ « against YOU » : `against_player="You"`, sinon la capacite partirait aussi
#    quand le vilain frappe un autre joueur.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet. C'est voulu — la carte
#    peut piocher plusieurs fois par phase vilain s'il y a plusieurs ennemis.


def GetAbilities() -> Sequence['Ability']:

    def est_villain_ou_sbire_villainous(face: 'CardFace') -> bool:
        if face is None:
            return False
        if Villain.IsType(face):
            return True
        return bool(Minion.IsType(face) and getattr(face, "villainous", 0))

    def spider_sense(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        joueur.DrawUp(1, effect)

    return [
        AbilityFactory.WhenUnitInitiatesAttackAgainst(
            AbilityType.Interrupt,
            CardFinder(check_face_fn=est_villain_ou_sbire_villainous),
            "You",
            spider_sense,
        ).SetName("Spider-Sense"),
    ]
