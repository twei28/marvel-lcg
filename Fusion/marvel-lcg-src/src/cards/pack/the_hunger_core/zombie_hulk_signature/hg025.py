from . import *

# Smash — TRAITRISE (deck signature de Zombie Hulk, carte 2/3). Aucun trait imprime.
# When Revealed: Choose support or upgrade and discard each card of that type you control.
# If you control none, your hero takes 3 damage.
#
# ⚠ Le nom imprime de cette carte, « Smash », N'EST PAS le mot-cle officiel Hulk : grep sur
# `data/cards.json` (fiche de l'etape « mot-cle rencontre ») -> aucune carte officielle ne porte
# « Smash » comme mot-cle avec regle precise (uniquement des NOMS de cartes : 10164/91421 « Hulk
# Smash », 23852 « Smash the Problem », 25654 « Sand Smash », 60870 « She-Hulk Smash », 110630
# « Smash! », rien de comparable a un mot-cle en gras suivi d'une regle). C'est donc un titre de
# carte d'AMBIANCE au meme sens que hg023 « Hunger Protocol » ou hg028 « Dead Spider-Sense » :
# aucune capacite n'est attachee au nom lui-meme, tout le texte de regle est dans le bloc «When
# Revealed». Pas de fiche mots-cles a ouvrir.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE (etape 2, une par capacite distincte)
#
# - « Choose support or upgrade » (choix de CATEGORIE, pas de carte-cible precise) : modele de
#   structure `core/iron_man_nemesis/01173.py` (Electric Whip Attack, `player.ChooseAbilities`
#   avec deux `AbilityFactory.ForChoiceAbility`) et `next_evol/juggernaut/40125.py`
#   (Breakthrough, meme fabrique pour un choix a deux branches de nature differente). Ici les deux
#   branches ne sont pas « degats OU defausse » mais « type A OU type B » : chaque option (nommee
#   sobrement "Support" / "Upgrade", pour coller au texte imprime et rester un `choisir_option`
#   simple cote test) delegue a UN MEME helper partage (`resoudre_type`) qui calcule la
#   consequence reelle (defausser tout / infliger 3) une fois le type choisi — aucune des deux
#   options n'a besoin de `.SetTarget()` (pas de ciblage joueur a l'interieur d'un type, et le
#   « hero » cible par les degats est fixe, pas choisi).
# - « discard EACH card of that type you control » (TOUTES les cartes du type, pas une seule) :
#   `player.GetControlCardsByType(upgrade=True)` / `(support=True)` (`player_get.py:107`, deja
#   utilise tel quel par `aos/modok/50119.py` pour recuperer « les upgrades que vous controlez »)
#   puis `Faces.DiscardAll(faces, effect)` (`game/operate/faces.py:8`, defausse INCONDITIONNELLE
#   de toute la liste, sans redemander au joueur — different de `player.DiscardControlCards(...)`
#   qui ne defausse qu'UNE carte choisie, modele `core/standard/01188.py` Caught Off Guard : pas
#   le bon outil ici puisque le texte dit « each », pas « a card »).
# - « If you control none, your hero takes 3 damage » (degats fixes a VOTRE HEROS, quelle que
#   soit la forme ACTUELLE du joueur — une Treachery se revele sans egard a la forme) : modele
#   exact `scarlet_spider/scarlet_spider_nemesis/ss022.py` (commentaire de la carte : « la face
#   Heros precisement, quelle que soit la forme actuelle du joueur ; `player.GetHero()` suppose
#   la forme heros active (assertion) -> lecture directe parmi `player.GetAllIdentityFace()` (les
#   deux faces, quelle que soit celle active) filtree par `Hero.IsType` ») et
#   `fne/daredevil/60012.py` (meme `GetAllIdentityFace()` pour retrouver une face d'identite
#   independamment de la forme en cours). `this.DealDamage([hero_face], 3, effect)` degats
#   DIRECTS (pas une attaque, pas de DoActivate, donc pas de defense possible — different du
#   piege hg017 sur les activations reelles).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE (etape 5, mots-pieges)
#
# « When Revealed » -> `AbilityFactory.WhenThisRevealed`, declencheur a la revelation de CETTE
#   carte (`Condition2.ThisIsTrigger` deja integre a la fabrique).
# « Choose support or upgrade » -> deux options presentees INCONDITIONNELLEMENT (`condition` par
#   defaut = True sur les deux branches de `ForChoiceAbility`) : le joueur peut choisir une
#   categorie meme s'il n'en controle aucune carte (c'est justement ce choix qui declenche les 3
#   degats) — ne jamais masquer l'option vide, ce serait priver le joueur du choix imprime.
# « discard EACH card of THAT type you control » -> « that type » = le type CHOISI, pas « les
#   deux types » : chaque branche de `resoudre_type` ne lit QUE le type correspondant
#   (upgrade=True, support=False ou l'inverse), jamais les deux a la fois.
# « you control » -> `GetControlCardsByType`, qui lit bien ce que le JOUEUR controle (upgrades
#   attaches a son identite ou a ses allies compris, cf. `player_get.py:42-61`), pas tout ce qui
#   est en jeu.
# « If you control NONE » -> le test porte sur la LISTE DEJA FILTREE au type choisi (`if faces:`
#   / `else:`), pas sur un decompte global « aucune carte d'aucun type ».
# « your HERO takes 3 damage » -> `Hero.IsType(f)` sur `GetAllIdentityFace()`, jamais
#   `player.GetIdentity()` nu (qui renverrait la face ACTIVE, Alter-Ego si le joueur est sous
#   cette forme au moment de la revelation) ni `player.GetHero()` (qui leve une assertion si la
#   forme active n'est pas Heros).
# « takes 3 damage » -> degats DIRECTS via `this.DealDamage`, pas une attaque (`DoActivate`) : la
#   carte ne declenche aucune activation de Zombie Hulk, donc aucune defense n'est proposee.
#
# ---------------------------------------------------------------------------
# NOMBRES TEXTE <-> CODE (etape 6)
#
# « 3 damage » (texte imprime, `data/cards_custom.json` hg025) <-> `this.DealDamage([...], 3,
#   effect)` : seule valeur numerique de la carte, un seul endroit a verifier, OK.
#
# ---------------------------------------------------------------------------
# A CONFIRMER
#
# Aucun point laisse en suspens sur cette carte : pas de mot-cle maison, pas de limite imprimee,
# pas de plateau a dessiner (degats et defausse se lisent deja sur les jauges existantes).


def GetAbilities() -> Sequence['Ability']:

    def smash_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()

        def resoudre_type(*, upgrade: bool, support: bool) -> None:
            faces = joueur.GetControlCardsByType(upgrade=upgrade, support=support)
            if faces:
                Faces.DiscardAll(faces, effect)
            else:
                hero_face = next((f for f in joueur.GetAllIdentityFace() if Hero.IsType(f)), None)
                cible = [hero_face] if hero_face else [joueur.GetIdentity()]
                this.DealDamage(cible, 3, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Support",
                lambda targets: resoudre_type(upgrade=False, support=True),
            ),
            AbilityFactory.ForChoiceAbility(
                "Upgrade",
                lambda targets: resoudre_type(upgrade=True, support=False),
            ),
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            smash_revealed,
        ),
    ]
