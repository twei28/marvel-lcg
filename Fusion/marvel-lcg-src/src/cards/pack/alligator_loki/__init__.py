from cards.pack import *

# ===========================================================================
# Pack ALLIGATOR LOKI — contenu custom de « Ripper3 ». Set 140, prefixe `al`.
#
# Deux sets : `Alligator Loki` (al001a-al017 et al023, dossier
# alligator_loki/alligator_loki/) et `Alligator Loki Nemesis` (al018-al022,
# dossier alligator_loki/alligator_loki_nemesis/).
#
# al020 et al021 « Lightning Bolt » portent un `ability_link` vers **02044**
# (pack gob, set Power Drain), dont elles reprennent le texte au mot pres :
# elles n'ont donc AUCUN module, et c'est voulu (database.py:124).
#
# ---------------------------------------------------------------------------
# LE CONCEPT DU PACK : LE HEROS S'ACCROCHE A UN ENNEMI
#
# Alligator Loki mord et ne lache plus. Six cartes lisent ou modifient cet
# etat : al001a (l'accrochage lui-meme et le malus a l'ennemi), al001b (Nap
# Time detache), al003-al006 (Chomp! frappe plus fort et peut accrocher),
# al013 (Unbreakable Grip empeche le detachement).
#
# ⚠ CE QUE LE MOTEUR FAIT, ET CE QU'IL NE FAIT PAS. L'extension est dans
# `game/card/face/card_type/identity.py` : le HEROS porte lui-meme le lien
# (`attached_enemy`), avec `AttachHeroTo` et `DetachHero`. Sa carte NE BOUGE
# PAS de la zone du joueur, parce que `Player.GetIdentity` (player_get.py:191)
# rend l'insert du monde des que `area_hero` est vide — le commentaire complet
# est sur place. Cote regles c'est bien « le heros EST l'attachement » : aucune
# carte marqueur n'existe.
#
# ⚠ TOUJOURS passer par `DetacherLeHeros` ci-dessous, JAMAIS par
# `heros.DetachHero` en direct : c'est le helper qui offre a Unbreakable Grip
# sa fenetre d'interposition, que le moteur ne fournit pas (il n'emet
# `AfterCardDetachFrom` qu'APRES coup, jamais un « would detach »).
# ===========================================================================

NOM_HEROS = "Alligator Loki"


def RetirerMenaceDUneManigance(effect: 'Effect', valeur: int) -> None:
    """« Remove N threat from a scheme. »

    Le premier joueur choisit, et on ne propose que les manigances qui portent
    reellement de la menace : un choix entre des cartes a zero n'a aucun sens.
    Reprend mot pour mot le helper du pack web_of_deceit, dont c'est le meme
    texte imprime.
    """
    # ⚠ « a scheme » sans restriction : le complot PRINCIPAL compte autant que
    # les annexes. `GetAllSideSchemes` seul (le helper de web_of_deceit) aurait
    # prive Throg de sa meilleure cible.
    schemes = [x for x in (list(Worlds.GetMainSchemes(effect))
                           + list(Worlds.GetAllSideSchemes(effect)))
               if x.CastTo(CanPlaceToken).GetTokens('threat') > 0]
    if not schemes:
        return
    joueur = Worlds.GetFirstPlayer(effect)
    cible = joueur.AskChooseFace(schemes, effect, prompt="Remove threat from")
    Faces.RemoveTokensOn([cible or schemes[0]], valeur, 'threat', effect)


def HerosAccrocheur(effect: 'Effect', joueur: 'Player|None'=None) -> 'Hero|None':
    """La face HEROS d'Alligator Loki, meme quand le joueur est en alter-ego.

    `GetHeroFace()` (identity.py:66) rend l'objet de la face heros quelle que
    soit la face active : indispensable pour al001b « Nap Time », qui detache
    APRES le passage en alter-ego, donc a un moment ou `GetIdentity()` rend la
    face civile.
    """
    if joueur is None:
        joueur = effect.GetInitiator()
    identite = joueur.GetIdentity()
    if identite is None:
        return None
    heros = identite.GetHeroFace()
    if heros is None or not heros.IsName(NOM_HEROS):
        return None
    return heros


def EnnemiAccroche(effect: 'Effect', joueur: 'Player|None'=None) -> 'CardFace|None':
    """L'ennemi que ce heros tient, ou None."""
    heros = HerosAccrocheur(effect, joueur)
    if heros is None:
        return None
    # Un ennemi vaincu quitte le terrain sans prevenir : `GetHeldEnemy` ne
    # rend jamais une carte qui n'est plus en jeu (et oublie le lien), sinon
    # Chomp! compterait ses 6 degats contre un fantome.
    return heros.GetHeldEnemy()


def EstAccrocheA(effect: 'Effect', face: 'CardFace', joueur: 'Player|None'=None) -> bool:
    return EnnemiAccroche(effect, joueur) is face


def AccrocherLeHeros(effect: 'Effect', ennemi: 'CardFace',
                     joueur: 'Player|None'=None) -> bool:
    """« Attach Alligator Loki to that enemy. »"""
    heros = HerosAccrocheur(effect, joueur)
    if heros is None or ennemi is None:
        return False
    return heros.AttachHeroTo(ennemi, effect)


def DetacherLeHeros(effect: 'Effect', joueur: 'Player|None'=None,
                    *, force: bool=False) -> bool:
    """« Detach Alligator Loki. » — SEUL point d'entree autorise.

    ⚠ C'est ici que vit l'interposition d'al013 « Unbreakable Grip » :
    « Hero Interrupt: When you would detach Alligator Loki from an enemy in
    play, exhaust Unbreakable Grip instead. » Le moteur n'a aucune fenetre
    « would detach » (`DetachFrom2` n'emet que `AfterCardDetachFrom`, une fois
    le detachement acquis), donc la fenetre est ouverte a la main, au seul
    endroit par lequel tout le pack passe.
    """
    if joueur is None:
        joueur = effect.GetInitiator()
    heros = HerosAccrocheur(effect, joueur)
    if heros is None or EnnemiAccroche(effect, joueur) is None:
        return False

    if not force:
        # « Interrupt », donc FACULTATIF : `forced=False` laisse le joueur
        # refuser et lacher prise. Le cout est l'inclinaison de la carte, donc
        # une Grip deja inclinee ne peut rien retenir.
        grips = [f for f in joueur.GetControlCards(CardFinder(name="Unbreakable Grip"))
                 if f.IsInPlay() and not f.IsExhaust()]
        if grips:
            grip = grips[0]

            def tenir_bon(targets: Sequence['CardFace']) -> None:
                Unused(targets)
                Faces.ExhaustAll([grip], effect)

            effets = joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Unbreakable Grip: exhaust instead of detaching",
                    tenir_bon,
                ).SetHasNoTargetEffect(),
                forced=False,
            )
            if effets:
                return False

    return heros.DetachHero(effect)
