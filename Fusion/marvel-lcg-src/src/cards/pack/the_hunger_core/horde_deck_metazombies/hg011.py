from . import *

# Zombie Captain Marvel — METAZOMBIE (Horde deck). AVENGER. KREE. SCH 1. ATK 1. PV 10[per_hero].
# Absorption — Forced Response: After she is attacked, place 1 energy counter on this card (max. 5). She gets
# +1 ATK for each energy counter.
# Forced Response: After she attacks, remove 1 energy counter from this card.
#
# Cartes de reference :
#  - « After she is attacked, place 1 energy counter ... (max. 5) » : `AbilityFactory.AfterUnitAttackUnit(
#    ForcedResponse, CardFinder(card_type=Hero|Ally), "This", ...)` + `Faces.PlaceCountersOn([this], 1, 'energy',
#    effect, maximum=5)`, modele `55044` Avatar of Loki / `ap304` (« After [Hero or Ally] attacks this card »,
#    meme role cote VICTIME) ; role symetrique a `19001a` Drax (« Response: After Villain attacks Drax » ->
#    `AbilityFactory.AfterUnitAttackUnit(Response, Villain, "This", drax)`, meme « This = attaque »). Le
#    compteur 'energy' existe deja nativement (`CardFace.COUNTER`), utilise par Captain Marvel cote JOUEUR
#    (`01018`, `56098`, `56103`...) -- aucun ajout a `card_face.py` necessaire pour cette carte.
#  - « She gets +1 ATK for each energy counter » : `AbilityFactory.ThisGainKeyword(lambda effect, ui:
#    effect.this.CastTo(Villain).GetCounters('energy'), attack=1, change_on_event=OnEvent.Counter("This",
#    'energy'))`, modele EXACT `19001a` Drax (`GetCounters('vengeance')` -> `attack=1` -> `OnEvent.Counter`).
#  - « After she attacks, remove 1 energy counter » : `AbilityFactory.AfterUnitAttackUnit(ForcedResponse, "This",
#    CardFinder(card_type=Identity|Ally), ...)` + `Faces.RemoveCountersOn([this], 1, 'energy', effect)`, modele
#    `hg009` Zombie Hulk (`toujours_overkill`, meme filtre `CardFinder(card_type=Identity|Ally)` pour « elle
#    attaque », puisqu'un vilain frappe toujours soit l'identite soit un allie defenseur).
#
# ⚠ Mots-pieges :
#  - « Absorption » est un NOM D'AMBIANCE propre a cette carte, pas un mot-cle officiel (absent de
#    `docs/reference/mots-cles/README.md`, aucune autre carte du moteur ne le reprend comme mot-cle, aucun
#    vilain officiel ne l'imprime -- grep `data/cards.json` sur `"Absorption"` : aucun resultat) : rien a
#    ouvrir avant de coder, le texte qui suit EST la regle complete.
#  - « After SHE is attacked » SANS condition de degats ni de defense : TOUTE attaque dirigee contre elle pose
#    le compteur, qu'elle soit defendue par une alliee ou non, et qu'elle subisse des degats ou non (une
#    alliee avec Toughness, par exemple, pourrait annuler les degats sans annuler l'attaque). D'ou
#    `AfterUnitAttackUnit` SANS `dealt_damage`/`target_took_damage` (les deux `None` par defaut -> condition
#    toujours vraie), a la difference de `AfterUnitAttackAndDamageUnit` (hg010) qui, lui, EXIGE des degats.
#  - PIEGE DE HARNAIS, pas du moteur (mesure le 27/10/2026) : le premier cas de test « Absorption » restait a 0
#    compteur apres `"declencher": ["Puzzle.Attack('01001a')"]` SANS `"cibles"`, et SANS trace d'erreur -- a
#    tort impute d'abord au code de la carte (essai avec `(CardFinder(card_type=Hero) | CardFinder(card_type=
#    Ally))` au lieu de `CardFinder(card_type=Hero|Ally)`, les DEUX formes se sont revelees rigoureusement
#    equivalentes une fois le vrai defaut corrige). La cause reelle : SANS `"cibles": ["hg011"]` explicite, le
#    pilote de `Puzzle.Attack` sur un heros ne lance PAS d'attaque du tout meme s'il n'y a qu'un seul ennemi en
#    jeu (`"degats": [["hg011", 0]]` constate -- aucune attaque n'a eu lieu, donc aucun message
#    `AfterUnitAttackUnit` n'a jamais ete envoye : la capacite n'avait rien a declencher). A la difference des
#    cas `hg001`/`hg009`/`hg010` ou le vilain personnalise ETAIT deja la cible implicite d'une attaque D'ENNEMI
#    (`Puzzle.EnemyAttacks`) ou la seule cible RESTANTE apres refus d'une autre (Shielded by the Horde), ici
#    c'est le HEROS qui attaque un vilain personnalise sans autre ennemi en jeu : `"cibles": ["hg011"]` reste
#    necessaire meme seul en jeu (modele confirme : `alien_vs_predator_d.py` ligne 127, `ap304`, qui passe
#    `cibles=["ap304"]` bien que ce soit le seul ennemi present).
#  - « (max. 5) » : plafond porte par le parametre natif `maximum=5` de `PlaceCountersOn`
#    (`can_place_counter.py:PlaceCountersInternal`), qui tronque l'ajout plutot que de le refuser en bloc --
#    pas de garde manuelle a ecrire.
#  - « for each energy counter » : lu dynamiquement a CHAQUE calcul d'ATK (`ThisGainKeyword` + lambda), jamais
#    fige au moment de la pose/retrait -- `change_on_event=OnEvent.Counter("This", 'energy')` est ce qui
#    force le moteur a recalculer des que le compteur change (modele Drax, meme piege deja documente sur
#    `hg008` Upgrades pour `OnEvent.AttachedMove`).
#  - « After she ATTACKS » (elle est l'ATTAQUANTE), a ne pas confondre avec la premiere capacite (elle est
#    l'ATTAQUEE) : deux abonnements distincts a la MEME fabrique `AfterUnitAttackUnit`, qui ne se recoupent
#    jamais puisque l'un fixe `attacker="This"` et l'autre `who_be_attacked="This"`.
#  - « remove 1 energy counter », SANS minimum impose par le texte : `RemoveCountersOn` avec `forced=True`
#    (par defaut dans le wrapper `Faces.RemoveCountersOn`) ne casse rien si le compteur est deja a 0
#    (`Counter.RemoveCounters` renvoie `False` sans effet si le nom n'existe pas encore dans le dict interne).
#    Pas de garde `if this.GetCounters('energy') > 0` a ecrire : coherent avec hg009 (`HealHealth` idem,
#    aucune garde supplementaire necessaire si l'appel natif est deja sans danger a vide).


def GetAbilities() -> Sequence['Ability']:

    def absorption(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Unused(message)
        this = effect.this.CastTo(Villain)
        Faces.PlaceCountersOn([this], 1, 'energy', effect, maximum=5)

    def apres_son_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Unused(message)
        this = effect.this.CastTo(Villain)
        Faces.RemoveCountersOn([this], 1, 'energy', effect)

    return [
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui: effect.this.CastTo(Villain).GetCounters('energy'),
            attack=1,
            change_on_event=OnEvent.Counter("This", 'energy'),
        ),
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            CardFinder(card_type=Hero|Ally),
            "This",
            absorption,
        ),
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            "This",
            CardFinder(card_type=Identity|Ally),
            apres_son_attaque,
        ),
    ]
