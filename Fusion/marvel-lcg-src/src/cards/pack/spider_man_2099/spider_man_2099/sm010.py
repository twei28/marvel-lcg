from . import *

# Hyper-Agility — AMELIORATION, cout 1 [physical]. CONDITION. SUPERPOWER.
# Your hero gets +1 DEF.
# Hero Response: After you resolve your hero's Acceleration ability WITHOUT
#   PLAYING AN EVENT, reduce the damage you take from attacks by 1 until the
#   end of the round. (Limit once per phase.)
#
# CARTES DE REFERENCE
#  - `ab007` * Donald Pierce : reagir a une capacite nommee portee par une
#    AUTRE carte, `WhenResolveSpecialAbility(CardFinder(...), op)`. Ici sur le
#    message `NOM_ACCEL_FINI`, que `sm001a` envoie APRES coup — c'est ce qui
#    donne son sens au « After » et permet de savoir si un evenement a ete
#    joue (RECETTES : l'ordre entre effets d'un meme message n'est pas
#    garanti, d'ou deux messages distincts).
#  - `50159`, `16098`, `21117` : reduire les degats subis =
#    `WhenUnitWouldTakeDamage(..., op)` + `message.ReduceDamage(n, effect)`,
#    la brique derriere `ReduceCharacterTakeDamageBy`.
#  - `ab001a` : `RegisterTemp(..., until_round_end=True)` pour « until the end
#    of the round ».
#  - `an008`, `ho008` : « Your hero gets +1 DEF ».
#
# TEXTE CONTRE CODE
#  ⚠⚠ « WITHOUT PLAYING AN EVENT » : c'est CETTE carte qui distingue les trois
#    ecoutes du pack. `sm011` Spinnerets et `sm012` Web Cape partent apres
#    TOUTE resolution d'Acceleration ; Hyper-Agility exige que la resolution
#    n'ait joue AUCUN evenement — deck vide, aucun evenement trouve, ou
#    evenement trouve mais non joue. Trois portees, trois conditions
#    differentes : les lire mot a mot.
#  ⚠ « reduce the damage YOU take FROM ATTACKS » : les degats subis par
#    l'identite, et seulement ceux d'attaques (`is_from_attack=True`) — pas
#    les degats indirects de la nemesis, qui sont justement le danger du pack.
#  ⚠ « UNTIL THE END OF THE ROUND », pas « until the end of the phase » :
#    `until_round_end=True`.
#  ⚠ « Limit once per phase » -> `LimitOncePerPhase()`.
#    ⚠⚠ SON TEMOIN D'EPUISEMENT N'EST PAS MONTABLE AVEC LE HARNAIS ACTUEL, et
#    il faut le dire (PROCESSUS-CARTE, « ce que ces blocs ne peuvent pas
#    voir »). Le seul effet observable de cette carte est une reduction de
#    degats, donc il faut se faire frapper pour la mesurer — or le pilote
#    DECLARE UNE DEFENSE des qu'on lance `Puzzle.Attack` sur l'ennemi (piege
#    connu, RECETTES §7bis), et la DEF du heros (2, +1 par cette carte meme)
#    absorbe la difference qu'on cherche a lire. Mesure du 08/09/2026 : Rhino
#    frappe pour 4, le heros encaisse 0, et ce 0 est compatible avec UNE comme
#    avec DEUX reductions. Un cas ecrit dessus serait vert sans rien prouver.
#    → A verifier en partie reelle, ou le jour ou le harnais saura interdire la
#    declaration de defense.
#  ⚠ « Your hero gets +1 DEF » : meme remarque que `sm009`, la DEF n'existe
#    pas en forme civile. Contre-cas dans l'autre forme du.


def GetAbilities() -> Sequence['Ability']:

    def pas_encore_cette_phase(effect: 'Effect', message: Any) -> bool:
        """La limite « once per phase », comptee par la carte.

        ⚠ PRECAUTION, PAS CORRECTIF D'UN DEFAUT MESURE. `LimitOncePerPhase()`
        est posee juste en dessous, mais elle vit sur une ability
        `AbilityType.Special` (le type que FORCE `WhenResolveSpecialAbility`),
        et le dépôt a déjà vu une limite silencieusement inerte sur une famille
        entiere (`AfterUnitDefeatedUnit`, corrige le 03/09/2026, RECETTES §1).
        Ce comptage maison — le meme que celui du helper pour l'Acceleration —
        garantit la limite quoi qu'il arrive.
        ⚠⚠ ET IL N'EST PAS PROUVE PAR UN TEST. Le temoin d'epuisement exige par
        l'etape 7 bis reste NON MONTABLE : le seul effet observable de cette
        carte est une reduction de degats, donc il faut se faire frapper pour
        la lire — or la DEF du heros (2, +1 par cette carte) absorbe l'ecart
        cherche, et deux attaques de base prealables n'ont pas suffi a empecher
        le pilote de declarer une defense (mesure du 08/09/2026 : Hydra Soldier
        annonce 2, l'identite encaisse 0, ce qui est compatible avec UNE comme
        avec DEUX reductions). Un cas ecrit dessus serait vert sans rien
        prouver : il a ete RETIRE plutot que maquille.
        """
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return False
        # ⚠ On distingue par la CARTE, jamais par le nom de l'ability : ce nom
        # doit rester `NOM_ACCEL_FINI`, c'est LUI qui route le message
        # (`check_ability_name`, factory/resolve.py:17), et `sm011` Spinnerets
        # comme `sm012` Web Cape le portent aussi. Les compter ensemble
        # brouillerait les trois limites.
        registre = getattr(effect.world.stat, "once_per_phase_player_effects", {}) or {}
        return not any(getattr(x, "this", None) is effect.this
                       for x in registre.get(joueur, []))

    def sans_evenement(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> bool:
        """« WITHOUT PLAYING AN EVENT » : aucun evenement joue par la
        resolution qui vient de s'achever. Le marqueur du pack est remis a
        zero a l'ouverture de chaque Acceleration, il ne peut donc pas garder
        la trace d'une resolution precedente."""
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return False
        return EvenementJoueParAcceleration(joueur) is None

    def esquiver(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        identite = IdentiteDuJoueur(effect, joueur)
        if identite is None or joueur is None:
            return

        # ⚠ RECETTES §1 : le registre NE S'ALIMENTE PAS TOUT SEUL. Lire une
        # limite sans jamais l'inscrire revient a ne poser aucune limite
        # (lecon `gb020` You Are My God).
        effect.world.stat.RecordEffectWithPlayer(effect, joueur)

        this.effect.RegisterTemp(
            AbilityFactory.WhenUnitWouldTakeDamage(
                AbilityType.Temp0,
                CardFinder(check_face_fn=lambda f: f is identite),
                lambda e2, dmg_message: dmg_message.ReduceDamage(1, e2),
                is_from_attack=True,
            ),
            unregister_after_exec=False,
            until_round_end=True,
        )

    return [
        *AbilityFactory.GiveKeywordToAttached(
            # ⚠ `Hero` et non `"You"` : le texte dit « YOUR HERO gets ». Sur
            # cette carte-ci la nuance est invisible (ni ATQ ni DEF n'existent
            # en alter-ego), mais `sm012` Web Cape a montre le 08/09/2026 que
            # `"You"` fait bien fuir le bonus sur l'autre face — on s'aligne.
            Hero,
            defense=1,
        ),

        AbilityFactory.WhenResolveSpecialAbility(
            CardFinder(card_ids=[ID_HEROS]),
            esquiver,
            conditions=[sans_evenement, pas_encore_cette_phase],
        ).SetName(NOM_ACCEL_FINI)
        .LimitOncePerPhase(),
    ]
