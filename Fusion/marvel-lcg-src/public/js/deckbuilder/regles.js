// regles.js — les regles de construction de deck, PURES.
//
// Extraites de js/deckbuilder/app.js le 09/09/2026, quand l'import d'un deck
// MarvelCDB SUR UN AUTRE HEROS a eu besoin du meme verdict que l'editeur. Deux
// ecrans jugent desormais la legalite d'un deck ; un seul code la calcule,
// sinon un deck accepte par l'editeur serait refuse a l'import, ou l'inverse.
//
// Le module ne connait ni le DOM, ni `cards`, ni la langue : le catalogue
// arrive par la fonction `carte(id)` et les libelles par `t(texte)`. Node
// l'execute donc tel quel — voir outils/verifier-marvelcdb.mjs.
"use strict";

// « 'Pool » : l'apostrophe fait partie du nom d'aspect dans les donnees (Deadpool).
export const ASPECTS = ["Aggression", "Justice", "Leadership", "Protection", "'Pool", "Determination", "Venomized"];
// Classes non-aspect jouables : Basic, et les cartes de recompense de Campagne.
export const CLASSES_NEUTRES = ["Basic", "Campaign"];
export const TYPES_JOUEUR = ["Ally", "Event", "Support", "Upgrade", "Resource", "PlayerSideScheme", "Player_Side_Scheme"];
export const SIGNATURE_MARVELOUS = 15;

/**
 * Cartes qu'un ASPECT impose au deck, en plus de ce que la joueuse a choisi.
 *
 * L'aspect fan-made VENOMIZED (ekAugust, set 168) est le seul a ce jour. Son
 * insert : le nombre de cartes du set « Venomized Weakness » depend du COUT
 * CUMULE des cartes Venomized du deck.
 *   1-20 -> 1 carte     21-40 -> 2 cartes
 *
 * ⚠ CES CARTES NE COMPTENT PAS DANS LES 40-50. Elles ne sont pas non plus
 * choisies ici : c'est le MOTEUR qui les tire au hasard au montage de la
 * partie (`PlayerSetup.CartesImposeesParLesAspects`). L'editeur ne fait que
 * l'ANNONCER, pour que la joueuse sache ce qui l'attend.
 *
 * ⚠ La table est la MEME des deux cotes. Si elle change ici, elle doit changer
 * dans `player_setup.py` : c'est le seul point ou les deux implementations
 * doivent se ressembler, et c'est pour cela qu'il est ecrit ici.
 */
export const ASPECTS_A_CARTES_IMPOSEES = [
    { aspect: "Venomized", set: "Venomized Weakness", tranches: [[20, 1], [40, 2]] },
];

/** Le cout cumule des cartes d'un aspect dans la pioche, et ce qu'il impose. */
export function cartesImposees(choisies, carte) {
    const out = [];
    for (const regle of ASPECTS_A_CARTES_IMPOSEES) {
        let cout = 0;
        for (const [id, n] of choisies) {
            const c = carte(id);
            if (!c || c.class !== regle.aspect) continue;
            // ⚠ Un cout « X » n'est pas un nombre : il vaut 0, comme cote
            // moteur. X se decide en jouant la carte, pas en construisant.
            const brut = String((c.desc && c.desc.Cost) ?? c.cost ?? "").trim();
            // ⚠ FOIS `n` : la pioche compte les EXEMPLAIRES, pas les titres.
            // Sans cette multiplication, trois Feed the Hunger pesaient 3 au
            // lieu de 9 et la seconde tranche n'etait jamais atteinte.
            if (/^\d+$/.test(brut)) cout += Number(brut) * n;
        }
        if (cout <= 0) continue;
        // La derniere tranche vaut aussi au-dela de son plafond : le tableau
        // de l'auteur s'arrete a 40, on n'en invente pas un troisieme.
        let nombre = regle.tranches[regle.tranches.length - 1][1];
        for (const [plafond, n] of regle.tranches) {
            if (cout <= plafond) { nombre = n; break; }
        }
        out.push({ aspect: regle.aspect, set: regle.set, cout, nombre });
    }
    return out;
}

/** Traduction par defaut : l'identite. Un appelant sans i18n reste lisible. */
const brut = (s) => s;

export function estStanLee(hero) { return /stan\s*lee/i.test((hero && hero.name) || ""); }
export function estSignature(c) { return !!c && c.class === "Hero"; }

export function estTypeJouable(c) {
    return TYPES_JOUEUR.includes(String(c.type).replace(/ /g, ""))
        || TYPES_JOUEUR.includes(String(c.type));
}

export function estCarteJoueur(c) {
    if (!c || !c.class) return false;
    if (c.class === "Hero") return false;
    if (!ASPECTS.includes(c.class) && !CLASSES_NEUTRES.includes(c.class)) return false;
    return estTypeJouable(c);
}

/** Carte signature d'un autre heros, empruntable par Stan Lee. */
export function estCarteSignature(c) {
    if (!estSignature(c) || !estTypeJouable(c)) return false;
    // Une vraie carte signature appartient au set d'un heros : cela ecarte les
    // cartes sans set (dont la carte d'exemple de cards_custom.json).
    return !!c.set_name && c.set_name !== "Stan Lee";
}

export function maxParDeck(carte) {
    const b = carte && carte.desc ? carte.desc.MaxPerDeck : undefined;
    const n = Number(b);
    return Number.isFinite(n) && n > 0 ? n : 3;
}

/** Regles de deckbuilding DECLAREES par le heros, dans `metadata.deckbuilding`
 *  de son deck de depart. C'est la meme voie que `metadata.hero_alts` (§5.3 du
 *  GUIDE-CREATION-CONTENU) : le moteur ignore `metadata`, et un heros neuf
 *  apporte ses regles avec lui au lieu d'exiger une retouche de ce fichier.
 *
 *  Forme attendue (toutes les cles sont facultatives) :
 *
 *      "deckbuilding": {
 *          "aspects":         { "min": 1, "max": 1, "label": "…" },
 *          "hors_aspect":     { "max": 6, "traits": ["TECH", "SPELL"], "label": "…" },
 *          // + "types": ["Upgrade"] pour ne compter que certains types (Ares, 07/09/2026)
 *          "types_interdits": ["Ally"]
 *      }
 *
 *  La table cablee plus bas reste la pour les 112 heros officiels, qu'on ne va
 *  pas rouvrir un par un ; le declaratif l'emporte quand il est present. */
export function reglesDeclarees(hero) {
    const m = hero && hero.deck && hero.deck.metadata;
    const d = m && m.deckbuilding;
    return d && typeof d === "object" ? d : null;
}

export function reglesAspect(hero, t = brut) {
    const decl = reglesDeclarees(hero);
    if (decl && decl.aspects) {
        const min = Number(decl.aspects.min) || 0;
        const max = Number.isFinite(Number(decl.aspects.max)) ? Number(decl.aspects.max) : 1;
        return { min, max, label: decl.aspects.label
            || (min === max ? `${t("exactement")} ${max} ${max > 1 ? t("aspects") : t("aspect")}`
                            : max >= 99 ? t("des aspects libres") : t("un seul aspect")) };
    }
    // ⚠ ANCRE SUR L'IDENTIFIANT, JAMAIS SUR LE NOM (correctif du 11/09/2026).
    //
    // Ces quatre lignes testaient le NOM du heros. Or un nom n'a rien d'unique :
    // le pack fan-made « Spider-Woman (Kajislav) » s'appelle aussi
    // « Spider-Woman », et `/spider-?woman/i` lui imposait donc les DEUX
    // aspects de Jessica Drew. Constate par l'utilisateur en construisant son
    // deck : « This hero requires exactly 2 aspects (Spider-Woman) », alors que
    // l'auteur a livre un deck de depart a UN seul aspect, Protection.
    //
    // `hero.id` est le nom du fichier `deck/starter/<id>.json` : il n'a pas
    // d'homonyme. C'est deja la regle que suit `quotaHorsAspect` plus bas, avec
    // le meme avertissement, pour la meme raison (« Doctor Doom » designe aussi
    // un mechant). Elle n'avait simplement jamais ete appliquee ici.
    //
    // ⚠ Un heros maison qui voudrait une regle particuliere ne passe PAS par
    // cette table : il la declare dans les metadonnees de son deck
    // (`reglesDeclarees`), qui l'emporte de toute facon.
    const id = (hero && hero.id) || "";
    if (id === "spider_woman") return { min: 2, max: 2, label: t("exactement 2 aspects (Spider-Woman)") };
    if (id === "cloak_dagger") return { min: 2, max: 2, label: t("exactement 2 aspects (Cloak & Dagger)") };
    if (id === "adam_warlock") return { min: 0, max: 99, label: t("des aspects libres (Adam Warlock)") };
    if (id === "moon_knight") return { min: 0, max: 99, label: t("tous les aspects, coût max 2 (Moon Knight)") };
    return { min: 0, max: 1, label: t("un seul aspect") };
}

/** Types de cartes que le heros s'interdit (Fatalis : « You cannot include any
 *  additional allies in your deck »). Ses allies SIGNATURE ne sont pas
 *  concernes : ils vivent dans `hero_deck`, jamais dans les cartes choisies. */
export function typesInterdits(hero) {
    const decl = reglesDeclarees(hero);
    const liste = decl && decl.types_interdits;
    return Array.isArray(liste) ? liste.map(String) : [];
}

/**
 * Cartes qui échappent à la limite d'aspect du héros.
 * Arachnophilia (Cassandra Webb) : « You may include allies with the
 * WEB-WARRIOR trait or with "Spider" in their title from any aspect in your
 * deck. » Ces alliés ne comptent donc pas dans le décompte des aspects.
 */
export function exemptDeLaLimiteAspect(hero, carte) {
    // ⚠ CE TEST PORTE ENCORE SUR LE NOM, et c'est le meme piege en sommeil que
    // celui corrige le 11/09/2026 dans `reglesAspect` : un second heros nomme
    // « Madame Web » heriterait silencieusement de la regle d'Arachnophilia.
    // Laisse tel quel faute de conflit AUJOURD'HUI (un seul heros porte ce
    // nom) ; a ancrer sur `hero.id` le jour ou un homonyme arrive, comme le
    // fait `quotaHorsAspect` plus bas.
    const nom = (hero && hero.name) || "";
    if (/madame web/i.test(nom)) {
        if (carte.type !== "Ally") return false;
        return (carte.traits || []).includes("WEB-WARRIOR") || /spider/i.test(carte.name);
    }
    /* Leader (Elijah Bradley / Patriot, pt001b) : « During deck building you
     * may include YOUNG AVENGER allies from any aspect. » Ces alliés ne
     * comptent donc pas dans le décompte des aspects.
     * ⚠ Aucune cible légale à ce jour : les deux seuls alliés YOUNG AVENGER
     * du catalogue (il002 Stature, wc002 Hulkling) sont de classe Hero, donc
     * cartes signature d'autres héros, interdites de deck. La règle est
     * implémentée pour le jour où un allié YOUNG AVENGER d'aspect sortira. */
    /* ⚠ Test ANCRÉ, pas un /patriot/i lâche : le dossier « A créer » contient
     * un pack « Iron Patriot » non encore porté, que la version lâche aurait
     * silencieusement doté de la règle Leader le jour de son arrivée. On
     * n'accepte donc que le nom exact, l'étoile d'unicité en moins
     * (cards/paper.py retire le préfixe « * », mais pas partout côté client). */
    if (/^\*?\s*patriot$/i.test(nom.trim())) {
        if (carte.type !== "Ally") return false;
        return (carte.traits || []).includes("YOUNG AVENGER");
    }
    /* Ms. America (America Chavez, ma001b) : « You may include upgrade cards
     * that modify your basic powers from any aspect in your deck. » Ces
     * améliorations ne comptent donc pas dans le décompte des aspects.
     * ⚠ Test ANCRÉ comme celui de Patriot : le catalogue contient déjà
     * « America Chavez » (l'alter-ego) et un pack « Iron Patriot » attend
     * d'être porté ; un /america/i lâche attraperait n'importe quoi.
     * ⚠ « qui modifient tes pouvoirs de base » n'est PAS un trait : c'est une
     * propriété à dériver. Mesure du 30/08/2026 sur data/cards.json : les clés
     * `ATK+` / `THW+` / `SCH+` du `desc` n'existent QUE sur des ATTACHEMENTS
     * de rencontre (Charge, Enhanced Ivory Horn) — aucune amélioration
     * d'aspect ne les porte, elles expriment leur bonus en CODE
     * (`GiveKeywordToAttached`). Le seul signal fiable est donc le TEXTE, et
     * la formule est stable dans tout le catalogue : « Your hero gets +1 ATK »,
     * « Your alter-ego gets +1 REC », « you get +3 DEF ». On garde les deux
     * voies (desc d'abord, texte ensuite).
     * Ce filtre laisse passer Combat Training, Heroic Intuition, Armored Vest,
     * Aggressive/Defensive/Heroic Conditioning, Brute Force, Innate Reflexes…
     * et ÉCARTE Inspired, Laser Blaster ou Danger Room Training, qui disent
     * « ATTACHED ALLY gets » : ce ne sont pas TES pouvoirs de base. */
    if (/^\*?\s*ms\.?\s*america$/i.test(nom.trim())) {
        if (carte.type !== "Upgrade") return false;
        const d = carte.desc || {};
        if (d["ATK+"] || d["THW+"] || d["DEF+"] || d["SCH+"]) return true;
        const txt = String(carte.text || "").replace(/<[^>]*>/g, " ");
        return /\b(?:your\s+(?:hero|identity|alter-ego)|you)\b[^.]{0,60}?[+−-]\d+\s*(?:ATK|THW|DEF|REC)\b/i.test(txt);
    }
    return false;
}

/** Regles « hors aspect A QUOTA », que `exemptDeLaLimiteAspect` ne sait pas
 *  exprimer : celle-ci est un booleen par carte, sans memoire, donc incapable
 *  de dire « jusqu'a 6 ». Le quota se compte dans `validerDeck()`.
 *
 *  Retourne { max, test, label } ou null.
 *
 *  ⚠ Test ancre sur l'IDENTIFIANT du heros, pas sur son nom : « Doctor Doom »
 *  designe AUSSI un mechant officiel. `hero.id` est le nom du fichier
 *  deck/starter/<id>.json, il n'a pas d'homonyme. */
export function quotaHorsAspect(hero, t = brut) {
    const decl = reglesDeclarees(hero);
    const q = decl && decl.hors_aspect;
    if (!q) return null;
    const max = Number(q.max);
    if (!Number.isFinite(max) || max <= 0) return null;
    const traits = (Array.isArray(q.traits) ? q.traits : []).map((x) => String(x).toUpperCase());
    // `types` (ajoute le 07/09/2026 pour Ares, « up to 5 TACTIC UPGRADES ») :
    // restreint le quota a certains TYPES de carte. Sans lui, un evenement
    // TACTIC d'aspect serait compte comme une amelioration TACTIC.
    const types = (Array.isArray(q.types) ? q.types : []).map((x) => String(x));
    return {
        max,
        // Sans liste de traits ni de types, le quota porte sur N cartes hors
        // aspect QUELLES QU'ELLES SOIENT : c'est le cas degenere, pas une erreur.
        test: (c) => (!traits.length || (c.traits || []).some((tr) => traits.includes(String(tr).toUpperCase())))
            && (!types.length || types.includes(String(c.type))),
        label: q.label || `${max} ${t("cartes")} ${traits.join("/")} ${t("d’autres aspects")}`,
    };
}

/** Les cartes CHOISIES PAR LE JOUEUR dans un deck fini, sous la forme attendue
 *  par `validerDeck` : une Map card_id -> nombre.
 *
 *  ⚠ Stan Lee fait exception. Ses 15 cartes signature sont EMPRUNTEES a d'autres
 *  heros (Marvelous), donc choisies, et elles vivent dans `hero_deck`. Les
 *  oublier le declarerait a court de 15 cartes a chaque import.
 */
export function choisiesDuDeck(hero, deck) {
    const sources = estStanLee(hero)
        ? [...((deck && deck.hero_deck) || []), ...((deck && deck.player_deck) || [])]
        : ((deck && deck.player_deck) || []);
    const m = new Map();
    for (const id of sources) {
        const cle = String(id).split(",")[0];
        m.set(cle, (m.get(cle) || 0) + 1);
    }
    return m;
}

/**
 * Verdict de legalite d'un deck.
 *
 * @param {Object}   o
 * @param {Object}   o.hero      heros du catalogue ({ id, name, deck })
 * @param {Iterable} o.choisies  paires [card_id, nombre] de la PIOCHE (hors signatures du heros)
 * @param {Function} o.carte     (card_id) -> carte du catalogue, ou undefined
 * @param {Function} [o.t]       traduction
 */
export function validerDeck({ hero, choisies, carte, t = brut }) {
    const problemes = [];
    if (!hero) return { ok: false, problemes: [t("Choisis un héros")], total: 0 };
    const marvelous = estStanLee(hero);
    // Stan Lee n'a pas de cartes signature a lui : les 15 sont a choisir ici.
    const signature = marvelous ? 0 : ((hero.deck && hero.deck.hero_deck) || []).length;
    let total = signature;
    let empruntees = 0;
    const parTitre = new Map();
    // On COMPTE par aspect au lieu de collectionner les noms : le quota de
    // Fatalis a besoin de savoir lequel pese le plus lourd (c'est l'aspect
    // « choisi ») et combien de cartes sont empruntees a chacun des autres.
    const parAspect = new Map();    // classe -> nombre de cartes
    const admissibles = new Map();  // classe -> cartes de cette classe qui passent le test du quota
    const quota = quotaHorsAspect(hero, t);
    const interdits = typesInterdits(hero);
    const horsDeckJoueur = [];   // cartes de rencontre, ou signatures d'un autre heros
    const typesRefuses = [];     // « no additional allies » et consorts
    for (const [id, n] of choisies) {
        const c = carte(id);
        if (!c) continue;
        total += n;
        parTitre.set(c.name, { n: (parTitre.get(c.name)?.n || 0) + n, max: maxParDeck(c) });
        // Rien ne garantissait jusqu'ici que la carte soit seulement JOUABLE :
        // un attachement de rencontre (Magical Suspension, 15026) passait tous
        // les controles, faute de `class`, et sortait « deck legal ».
        if (!estCarteJoueur(c) && !(marvelous && estCarteSignature(c))) horsDeckJoueur.push(c.name);
        else if (interdits.includes(String(c.type))) typesRefuses.push(c.name);
        if (estSignature(c)) empruntees += n;
        else if (c.class && !CLASSES_NEUTRES.includes(c.class)
                 && !exemptDeLaLimiteAspect(hero, c)) {
            parAspect.set(c.class, (parAspect.get(c.class) || 0) + n);
            if (quota && quota.test(c)) admissibles.set(c.class, (admissibles.get(c.class) || 0) + n);
        }
    }

    // Quota hors aspect : l'aspect choisi est le plus fourni ; un autre aspect
    // ne sort du decompte que si TOUTES ses cartes passent le test. S'il en
    // reste une seule qui echoue, la classe entiere reste comptee et c'est la
    // limite d'aspects ordinaire qui parle — le joueur voit alors quel aspect
    // de trop il a introduit, ce qu'un quota silencieux masquerait.
    let horsAspect = 0;
    if (quota && parAspect.size > 1) {
        const principal = [...parAspect.entries()].sort((a, b) => b[1] - a[1])[0][0];
        const sortis = [];
        for (const [classe, n] of parAspect) {
            if (classe === principal) continue;
            if ((admissibles.get(classe) || 0) === n) { horsAspect += n; sortis.push(classe); }
        }
        for (const classe of sortis) parAspect.delete(classe);
    }
    const aspects = new Set(parAspect.keys());
    if (horsDeckJoueur.length) {
        problemes.push(`${t("Cartes qui n’appartiennent pas à un deck de joueur :")} ${[...new Set(horsDeckJoueur)].join(", ")}`);
    }
    if (typesRefuses.length) {
        problemes.push(`${t("Ce héros refuse ce type de carte :")} ${[...new Set(typesRefuses)].join(", ")}`);
    }
    if (marvelous && empruntees !== SIGNATURE_MARVELOUS) {
        problemes.push(`${t("Marvelous : exactement")} ${SIGNATURE_MARVELOUS} ${t("cartes signature d’autres héros — actuellement")} ${empruntees}`);
    }
    if (total < 40) problemes.push(`${t("Deck trop petit :")} ${total}/40 ${t("minimum (cartes signature incluses)")}`);
    if (total > 50) problemes.push(`${t("Deck trop grand :")} ${total}/50 maximum`);
    const regle = reglesAspect(hero, t);
    if (aspects.size < regle.min) problemes.push(`${t("Ce héros requiert")} ${regle.label} — ${t("actuellement")} ${aspects.size}`);
    if (aspects.size > regle.max) {
        problemes.push(`${t("Trop d’aspects")} (${[...aspects].join(", ")}) — ${t("autorisé :")} ${regle.label}`
            + (quota ? ` ${t("+ au plus")} ${quota.label}` : ""));
    }
    if (quota && horsAspect > quota.max) {
        problemes.push(`${t("Hors aspect : au plus")} ${quota.label} — ${t("actuellement")} ${horsAspect}`);
    }
    for (const [titre, x] of parTitre) {
        if (x.n > x.max) problemes.push(`${t("Trop d’exemplaires de")} « ${titre} » : ${x.n}/${x.max}`);
    }
    return { ok: problemes.length === 0, problemes, total, aspects: [...aspects], signature, empruntees,
             horsAspect, quotaMax: quota ? quota.max : 0,
             imposees: cartesImposees(choisies, carte) };
}
