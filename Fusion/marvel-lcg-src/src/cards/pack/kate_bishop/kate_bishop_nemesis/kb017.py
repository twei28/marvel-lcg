from . import *

# * Madame Masque — sbire nemesis de Hawkeye (Kate Bishop), MASTERS OF EVIL
# [star] Madame Masque's ATK and SCH are equal to the ATK and THW,
#   respectively, of the hero form of the identity she is engaged with.
#
# Modele exact : Mystique (mut_gen/mystique/32080.py), qui aligne ATK/SCH sur
# ceux du vilain via `AbilityFactory.ThisSetKeyword` (un `check_fn` qui
# renvoie `(valeur, valeur_a_change)`). Ici la source n'est pas le vilain
# mais « la forme heros de l'identite engagee » : `minion.GetEngagedPlayer()`
# (minion.py:146) puis `identity.GetHeroFace()` (identity.py:66), qui renvoie
# TOUJOURS la face Heros meme si le joueur est actuellement en alter-ego.
#
# CORRIGE (test de comportement) : `GetHeroFace()` renvoie bien le bon OBJET
# face quelle que soit la forme active, mais `heros.attack`/`heros.thwart`
# (proprietes CALCULEES via `GetKeyword`) renvoient 0 -- pas l'imprime -- pour
# une face d'identite qui N'EST PAS la face ACTUELLEMENT AFFICHEE : ces
# proprietes lisent `self.keywords['ATK'/'THW']`, peuple seulement par
# `OnResetKeywords`, lui-meme appele uniquement par `OnFlip`/`Reset`
# (face_on_event.py) sur la face qui DEVIENT active. La face Heros jamais
# affichee (Kate demarre et reste en alter-ego) n'a jamais eu ce peuplement.
#
# `printed_attack`/`printed_thwart` (can_attack.py/can_thwart.py) echappent a
# ce cycle : remplis une seule fois par `Initialize()` (card_face.py) depuis
# `paper.desc`, pour CHAQUE face a la construction, actif ou non. Pattern deja
# utilise ailleurs pour lire le stat d'UNE AUTRE carte (av013.py, av014.py,
# ag012.py) -- correction au niveau carte, aucun fichier moteur touche.
# Confirme par sonde : Kate en alter-ego -> ATK=2/SCH=2 copies (imprimes de
# kb001a) ; Kate en heros -> memes valeurs.


def GetAbilities() -> Sequence['Ability']:

    def forme_heros_engagee(effect: 'Effect') -> 'Hero':
        this = effect.this.CastTo(Minion)
        joueur = this.GetEngagedPlayer()
        return joueur.GetIdentity().GetHeroFace()

    def madame_masque_atk(effect: 'Effect', ui: List['CardFace']) -> Tuple[int, bool]:
        this = effect.this.CastTo(Minion)
        heros = forme_heros_engagee(effect)
        ui.append(heros)
        valeur = heros.printed_attack
        return valeur, valeur != this.attack

    def madame_masque_sch(effect: 'Effect', ui: List['CardFace']) -> Tuple[int, bool]:
        this = effect.this.CastTo(Minion)
        heros = forme_heros_engagee(effect)
        ui.append(heros)
        valeur = heros.printed_thwart
        return valeur, valeur != this.scheme

    return [
        AbilityFactory.ThisSetKeyword(
            madame_masque_atk,
            attack=1,
            change_on_event=OnEvent.CardKeyword("Character"),
        ).SetName("Masters of Evil (ATK)"),
        AbilityFactory.ThisSetKeyword(
            madame_masque_sch,
            scheme=1,
            change_on_event=OnEvent.CardKeyword("Character"),
        ).SetName("Masters of Evil (SCH)"),
    ]
