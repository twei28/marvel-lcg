from . import *

# * Franklin Richards — ALLIE (Survivor deck, carte 1/5). Cout 0. THW 1[star]. ATK 0. PV 2. RES wild.
#   SURVIVOR. FANTASTIC.
# Action: Exhaust Franklin Richards -> choose one:
# - Remove 2 infection counters from a hero.
# - Heal 2 damage from a friendly character.
#
# ---------------------------------------------------------------------------
# ETAPE 2 : CARTES DE REFERENCE
#
# - Charpente « Action: Exhaust <nom> -> choose one: ... » (un cout d'inclinaison PUIS un choix a deux
#   branches) : modele officiel `09002` Wong (pack `drs/doctor_strange`) : `AbilityFactory.
#   WhenInYourPlayTurn(AbilityType.Action, wong).SetCostFunc(CostFunc.Exhaust("This"))`, puis
#   `initiator.ChooseAbilities(effect, ForChoiceAbility(...).SetTarget(...), ForChoiceAbility(...)
#   .SetTarget(...))` a l'interieur du callback. Repris ici a l'identique (meme fabrique, meme cout, meme
#   charpente a deux branches).
# - « Remove 2 infection counters from A HERO » (cible choisie par le joueur, PAS « from your identity » ni
#   « each player ») : aucune carte officielle ne pose de compteur « infection » (compteur maison de ce
#   scenario), donc pas de carte de reference pour le COMPTEUR precis -- mais la MECANIQUE « cibler un
#   personnage puis retirer un compteur nomme de SON identite » est deja celle de `commun.PoserInfection`
#   (`cards/pack/the_hunger_core/commun.py:307`, deja utilisee par hg001-hg003/hg037), qui pose le compteur
#   sur `joueur.GetIdentity()` et PAS sur la face Hero. Le symetrique (retrait) suit la meme regle : on cible
#   une face Hero (`SetTarget(Hero)`), on en deduit SON joueur via `CardFace.GetOwnerPlayer()`
#   (`card_face.py:1249`), puis on retire le compteur de `joueur.GetIdentity()`, jamais de la face Hero
#   elle-meme (ce qui echouerait silencieusement : aucun compteur n'y est jamais pose).
#   `Faces.RemoveCountersOn` (`operate/faces.py:227`) est le symetrique documente de `Faces.PlaceCountersOn`
#   deja utilise par `PoserInfection`.
# - « Heal 2 damage from a friendly character » : modele officiel `lj024` Wet Slobbering Kiss (pack
#   `lockjaw`) : `this.HealthUnits(effect.targets, 3, effect)`, cible `Ally` (lj024 restreint en prose a « qui
#   n'est pas votre identite », donc UNIQUEMENT alliee). Ici le texte dit « a FRIENDLY CHARACTER », sans
#   cette restriction : porte a la fois les heros ET les allies -- c'est exactement la classe `Friend`
#   (`game/card/face/base/friend.py`, ancetre commun de `Hero` et `Ally`, deja utilisee par `ally.py` comme
#   base de `Ally`). `SetTarget(Friend, canbe_heal=True)` plutot que `SetTarget(Ally, canbe_heal=True)` de
#   lj024.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - « Action » : type de capacite de base du moteur (`AbilityType.Action`), pas un mot-cle a ficher --
#   aucune fiche `mots-cles/` n'existe pour « Action » / « Response » / « Interrupt », ces types de capacite
#   sont une categorie du moteur, pas un mot-cle imprime a definir.
# - « infection counter » : deja tranche sur `hg002`/`hg037` de ce meme scenario -- PAS un mot-cle (ni gras ni
#   italique sur le texte imprime), un COMPTEUR DE CARTE/SCENARIO nomme ordinaire (meme critere que `flame`,
#   `rage`, `web` au README des mots-cles). Rien a ouvrir, rien a creer.
# - Aucun autre terme en gras sur cette carte (seul « Action » l'est, par convention de mise en page, pas par
#   mecanique a cataloguer).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE (etape 5, mots-pieges)
#
# - « Exhaust Franklin Richards » (cout, PAS un cout a plusieurs parties) -> `CostFunc.Exhaust("This")` seul,
#   comme Wong -- aucun degat a soi dans le cout (contrairement a `19002` Mantis ou `dt066` Misty Knight, qui
#   EUX s'infligent des degats en cout : rien de tel n'est imprime ici).
# - « choose one » -> DEUX branches `ForChoiceAbility`, jamais un seul callback qui ferait les deux.
# - « Remove 2 infection counters FROM A HERO » -> cible = UNE face `Hero` (le joueur choisit LAQUELLE, parmi
#   tous les heros en jeu, y compris le sien) ; le compteur est retire de l'IDENTITE de son controleur
#   (`commun.PoserInfection` pose le compteur sur l'identite, jamais sur la face Hero -- la lecture inverse,
#   necessaire pour retirer le MEME compteur, piege deja identifie a l'etape 2 ci-dessus).
# - « Heal 2 damage from A FRIENDLY CHARACTER » -> `Friend` (heros OU allie), jamais `Ally` seul (`lj024` la
#   restreint a « qui n'est pas votre identite », cette carte NE porte PAS cette restriction : un heros EST un
#   choix valide).
# - Pas de `unless`/`otherwise`/`instead`/`if you cannot`/limite imprimee sur cette carte : rien d'autre a
#   coder.
#
# ---------------------------------------------------------------------------
# ETAPE 6 : BLOC NOMBRES, TEXTE <-> CODE
#
# - « Remove 2 infection counters » -> `Faces.RemoveCountersOn([identite], 2, 'infection', effect)`, `2`
#   explicite.
# - « Heal 2 damage » -> `this.HealthUnits(targets, 2, effect)`, `2` explicite.
# - `desc.THW = "1*"` : LU NATIVEMENT par le moteur (`can_thwart.py`, le `*` apres un THW/ATK d'Allie est
#   l'icone officielle « degats consequents », pas le symbole generique « par heros » -- voir note genurale
#   ci-dessous) -- base automatique, aucun script requis (meme traitement que `Toughness`/`Restricted`,
#   PROCESSUS-CARTE.md etape 6).
#
# ⚠ NOTE GENERALE SUR LE « * » DES STATS D'ALLIE DE CE LOT (hg072-hg076) : `desc.HP`/`desc.StartingThreat`
# emploient le « * » comme symbole « par heros » (`FormatPlayerNumValue`, `has_attribute.py:17`, remplace
# "2*" par "2*nombre_de_joueurs" puis evalue). CE N'EST PAS LE CAS pour `desc.ATK`/`desc.THW` : ces deux
# attributs ont chacun leur PROPRE fonction d'analyse (`can_attack.py:78`, `can_thwart.py:21`), qui lit
# chaque `*` comme UNE ETOILE DE DEGATS CONSEQUENTS imprimee sur l'icone (regle de base officielle : un
# allie qui attaque/manigance subit autant de degats que d'etoiles apres son ATK/THW). `desc.THW = "1*"` sur
# cette carte veut donc dire « THW 1, une etoile » = Franklin Richards subit 1 degat CONSEQUENT apres avoir
# manigance -- comportement NATIF de la classe `Ally` (`card_type/ally.py:30-58`), aucune ligne a ecrire.
# Verifie en lisant le parseur avant d'ecrire CE fichier (jamais assume a vue, lecon Lockjaw du guide).
#
# A CONFIRMER EN PARTIE REELLE : aucun outil de ce lot ne lance l'autoplay ni `test_capacites.py` (consigne
# de la tache) -- la carte n'a donc ete prouvee que par lecture du moteur et cas ecrits ci-dessous (a
# fusionner dans `tools/cas/the_hunger_core.py` par un tiers), jamais executes par moi.


def GetAbilities() -> Sequence['Ability']:

    def franklin(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        initiator = effect.GetInitiator()

        def retirer_infection(targets: Sequence['CardFace']) -> None:
            for hero in targets:
                joueur = hero.GetOwnerPlayer()
                Faces.RemoveCountersOn([joueur.GetIdentity()], 2, 'infection', effect)

        def soigner(targets: Sequence['CardFace']) -> None:
            this.HealthUnits(targets, 2, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 2 infection counters from a hero",
                retirer_infection,
            ).SetTarget(Hero),
            AbilityFactory.ForChoiceAbility(
                "Heal 2 damage from a friendly character",
                soigner,
            ).SetTarget(Friend, canbe_heal=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            franklin,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
