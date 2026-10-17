// regles.js — les regles de construction de deck, PURES.
//
// Extraites de js/deckbuilder/app.js le 09/09/2026, quand l'import d'un deck
// MarvelCDB SUR UN AUTRE HEROS a eu besoin du meme verdict que l'editeur. Deux
// ecrans jugent desormais la legalite d'un deck ; un seul code la calcule,
// sinon un deck accepte par l'editeur serait refuse a l'import, ou l'inverse.
//
// Le module ne connait ni le DOM, ni `cards`, ni la langue : le catalogue
// arrive par la fonction `carte(id)` et les libelles par `t(texte)`. Node
// l'execute donc tel quel — voir tools/tests-lanceur/regles-aspect.test.mjs.
"use strict";

import { exclusiveRefusee } from "../prepare/arts-cartes-choix.js";
import { CLASSES_SHINOBI, typesShinobi, estShinobi, estPath, reglesDuPath, reglesDuPathPropre, admiseParLePath } from "./paths-shinobi.js";
export { CLASSES_SHINOBI, typesShinobi, estShinobi, estPath };

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
/** La classe qui compte pour la construction. Le catalogue porte des classes
 *  doubles : « Hero;Aggression » (les quatre evenements signature de
 *  Spider-Woman) et « Campaign;Basic ». Une signature reste « Hero », sinon
 *  l'aspect l'emporte, sinon la classe neutre. Audit du 03/10/2026 : sans ce
 *  tri, tout deck marvelcdb de Spider-Woman etait refuse a l'import. */
export function classeDeConstruction(classe) {
    const liste = String(classe || "").split(";").map((x) => x.trim()).filter(Boolean);
    if (liste.length < 2) return classe;
    if (liste.includes("Hero")) return "Hero";
    // Carte DUAL SHINOBI (« Bushido;Kuji-Kiri », pack tmnt_shinobi_dual) : ses DEUX types restent lisibles
    // (livret p.7 : elle compte comme les deux), ils ne sont ni des aspects ni « Basic ».
    if (typesShinobi(classe).length) return classe;
    return liste.find((x) => ASPECTS.includes(x)) || liste.find((x) => CLASSES_NEUTRES.includes(x)) || liste[0];
}

/** Les ASPECTS d'une classe (« Aggression;Justice » -> les deux ; « Hero;Aggression »
 *  -> [« Aggression »] ; « Basic » -> []). */
export function aspectsDeClasse(classe) {
    return String(classe || "").split(";").map((x) => x.trim()).filter((x) => ASPECTS.includes(x));
}

/** Carte DOUBLE ASPECT (pack tmnt_aspect_dual, Inkwire, 16/10/2026) : sa classe ne
 *  porte QUE des aspects, au moins deux (bandeau « AGGRESSION/JUSTICE »). Elle entre
 *  dans un deck de l'un OU de l'autre, sans y ajouter d'aspect. « Hero;Aggression »
 *  (signatures de Spider-Woman) n'en est pas une. */
export function estDoubleAspect(c) {
    if (!c || !c.class) return false;
    const parts = String(c.class).split(";").map((x) => x.trim()).filter(Boolean);
    return parts.length >= 2 && parts.every((x) => ASPECTS.includes(x));
}

const avecClasseDeConstruction = (c) => {
    if (!c) return c;
    const classe = classeDeConstruction(c.class);
    return classe === c.class ? c : Object.assign(Object.create(Object.getPrototypeOf(c)), c, { class: classe });
};

export function estSignature(c) { return !!c && classeDeConstruction(c.class) === "Hero"; }

export function estTypeJouable(c) {
    return TYPES_JOUEUR.includes(String(c.type).replace(/ /g, ""))
        || TYPES_JOUEUR.includes(String(c.type));
}

/** Sets dont les cartes n'entrent dans un deck que par la mise en place de leur
 *  campagne (« These cards cannot be included in any deck unless playing the
 *  Skrull Menace campaign », livret p.5) : absentes du constructeur. */
export const SETS_RESERVES_A_LA_CAMPAGNE = ["Skrull Menace Campaign"];

export function estCarteJoueur(c) {
    if (!c || !c.class) return false;
    if (SETS_RESERVES_A_LA_CAMPAGNE.includes(c.set_name)) return false;
    if (c.class === "Hero") return false;
    // TMNT Shinobi (17/10/2026) : une carte Shinobi (classe Bushido / Ninjutsu / Kuji-Kiri / Taijutsu, Dual
    // comprise) ou un PATH est une carte de joueur ; `validerDeck` exige alors un Path et applique ses regles.
    if (estPath(c)) return true;
    if (estShinobi(c)) return estTypeJouable(c);
    // Double aspect (« Aggression;Justice ») : une carte d'aspect comme une autre.
    if (estDoubleAspect(c)) return estTypeJouable(c);
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
 *          // + "compte": "titres" : `max` compte des TITRES, pas des cartes (Maria Hill)
 *          "types_interdits": ["Ally"],
 *          "types_interdits_aspect": ["Ally"]   // seulement les cartes D'ASPECT (Iron Patriot)
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

/** Types de cartes D'ASPECT que le heros s'interdit, les basiques restant
 *  permis (Iron Patriot, ip001b : « your deck cannot include any aspect allies »). */
export function typesInterditsAspect(hero) {
    const decl = reglesDeclarees(hero);
    const liste = decl && decl.types_interdits_aspect;
    return Array.isArray(liste) ? liste.map(String) : [];
}

const aTrait = (carte, trait) => (carte.traits || []).some((tr) => String(tr).toUpperCase().replace(/\.$/, "") === trait);

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
    /* Cable (Nathan Summers, 40001b) : « You may include player side schemes
     * from any aspect in your deck. » Ses manigances annexes ne comptent donc
     * pas dans le décompte des aspects.
     * Signalé en jeu le 22/09/2026 : un deck marvelcdb de Cable bâti autour des
     * manigances annexes était refusé au collage (« Trop d'aspects (Justice,
     * Leadership, Aggression, Protection) »), alors que c'est exactement ce que
     * sa carte autorise.
     * ⚠ ANCRÉ SUR `hero.id` (le nom du fichier `deck/starter/<id>.json`), et
     * non sur le nom comme les trois règles du dessus : c'est la convention que
     * `reglesAspect` a adoptée le 11/09/2026 après qu'un homonyme fan-made a
     * hérité d'une règle qui n'était pas la sienne. Un second « Cable » ne
     * prendra donc pas celle-ci au passage.
     * ⚠ Le TYPE seul suffit, sans filtre de trait ni de texte : la carte ne
     * pose aucune condition. Les deux orthographes du type sont celles de
     * `TYPES_JOUEUR` (le catalogue porte « PlayerSideScheme », marvelcdb
     * « Player_Side_Scheme »). */
    const id = (hero && hero.id) || "";
    if (id === "cable") {
        return String(carte.type).replace(/[ _]/g, "") === "PlayerSideScheme";
    }
    /* Audit du 03/10/2026 (apres le refus du deck Maria Hill d'Aghenatak) :
     * trois autres identites levaient la limite d'aspect sans que la regle
     * soit ecrite. Toutes ancrees sur `hero.id`, comme Cable. */
    // Scott Summers (33001b) : « You may include X-MEN allies from any aspect ».
    if (id === "cyclops") return carte.type === "Ally" && aTrait(carte, "X-MEN");
    // Kate Bishop (kb001b) : « you may include SKILL cards from any aspect ».
    if (id === "kate_bishop") return aTrait(carte, "SKILL");
    // Simon Williams (58001b) : « events with a printed [energy] resource icon
    // from any aspect ». L'energie est la lettre « Y » de `desc.RES`.
    if (id === "wonder_man") {
        return carte.type === "Event" && String((carte.desc && carte.desc.RES) || "").toUpperCase().includes("Y");
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
    // Le catalogue ecrit « S.H.I.E.L.D » comme « S.H.I.E.L.D. » : le point final
    // ne doit pas decider de la legalite.
    const norme = (x) => String(x).toUpperCase().replace(/\.$/, "");
    const traits = (Array.isArray(q.traits) ? q.traits : []).map(norme);
    // `types` (ajoute le 07/09/2026 pour Ares, « up to 5 TACTIC UPGRADES ») :
    // restreint le quota a certains TYPES de carte. Sans lui, un evenement
    // TACTIC d'aspect serait compte comme une amelioration TACTIC.
    const types = (Array.isArray(q.types) ? q.types : []).map((x) => String(x));
    return {
        max,
        // Maria Hill (50001b) : « the maximum number of copies of 3 S.H.I.E.L.D.
        // supports » compte des titres ; les exemplaires restent bornes par titre.
        parTitre: q.compte === "titres",
        // Sans liste de traits ni de types, le quota porte sur N cartes hors
        // aspect QUELLES QU'ELLES SOIENT : c'est le cas degenere, pas une erreur.
        test: (c) => (!traits.length || (c.traits || []).some((tr) => traits.includes(norme(tr))))
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

/* COPIES ET UNICITE (Rules Reference v1.8, « Copy » et « Unique Icon », audit
 * du 03/10/2026). Une copie partage le titre ET le sous-titre : les cinq
 * allies « Spider-Woman » de Madame Web, aux sous-titres differents, ne sont
 * pas des copies (on comptait par titre seul, et son deck etait refuse). Une
 * carte unique (« * » devant le nom) ne figure qu'une fois, et deux cartes
 * uniques, identite comprise, ne peuvent pas « correspondre » :
 *   - meme titre, sans sous-titre ni titre d'alter ego des deux cotes ;
 *   - ou le sous-titre / titre d'alter ego de l'une egale le titre, le
 *     sous-titre ou le titre d'alter ego de l'autre. */
export const titreDe = (c) => String((c && c.name) || "").replace(/^\*\s*/, "").trim();
export const estUnique = (c) => /^\*/.test(String((c && c.name) || ""));
const cleCopie = (c) => `${titreDe(c)}|${String((c && c.subtitle) || "").trim()}`;
const cleCopieU = (u) => `${u.t}|${u.s}`;

export function correspondent(a, b) {
    if (a.t === b.t && !a.s && !b.s && !a.alt && !b.alt) return true;
    const autres = (x) => [x.t, x.s, x.alt].filter(Boolean);
    return [a.s, a.alt].filter(Boolean).some((v) => autres(b).includes(v))
        || [b.s, b.alt].filter(Boolean).some((v) => autres(a).includes(v));
}

/** L'identite, pour la correspondance : chaque face heros porte le titre
 *  d'alter ego (le sien n'existe pas cote catalogue, on prend les faces). */
function identitePourUnicite(hero, carte) {
    const faces = String(((hero.deck && hero.deck.hero) || [])[0] || "").split(",").map((id) => carte(id)).filter(Boolean);
    const heros = faces.filter((f) => f.type === "Hero").map(titreDe);
    const alters = faces.filter((f) => f.type !== "Hero").map(titreDe);
    return heros.flatMap((t) => (alters.length ? alters : [""]).map((alt) => ({ t, s: "", alt })));
}

function problemesUnicite(hero, choisies, carte, t) {
    const out = [];
    const uniques = [];
    for (const [id] of choisies) {
        const c = carte(id);
        if (!c || !estUnique(c)) continue;
        uniques.push({ t: titreDe(c), s: String(c.subtitle || "").trim(), alt: "", nom: titreDe(c) + (c.subtitle ? ` (${c.subtitle})` : "") });
    }
    const signatures = estStanLee(hero) ? [] : ((hero.deck && hero.deck.hero_deck) || []).map((id) => carte(id)).filter(estUnique)
        .map((c) => ({ t: titreDe(c), s: String(c.subtitle || "").trim(), alt: "", nom: titreDe(c) }));
    const identite = identitePourUnicite(hero, carte);
    const vus = new Set();
    for (let i = 0; i < uniques.length; i++) {
        const u = uniques[i];
        const rivaux = [...uniques.slice(i + 1), ...signatures].filter((v) => cleCopieU(v) !== cleCopieU(u) && correspondent(u, v));
        if (identite.some((x) => correspondent(u, x))) rivaux.push({ nom: hero.name || t("l’identité") });
        for (const v of rivaux) {
            const cle = [u.nom, v.nom].sort().join(" / ");
            if (vus.has(cle)) continue;
            vus.add(cle);
            out.push(`${t("Cartes uniques qui se correspondent :")} « ${u.nom} » ${t("et")} « ${v.nom} »`);
        }
    }
    return out;
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
export function validerDeck({ hero, choisies, carte: carteBrute, t = brut }) {
    const carte = (id) => avecClasseDeConstruction(carteBrute(id));
    const problemes = [];
    if (!hero) return { ok: false, problemes: [t("Choisis un héros")], total: 0 };
    const marvelous = estStanLee(hero);
    // Stan Lee n'a pas de cartes signature a lui : les 15 sont a choisir ici.
    // RR « Deck Customization » : les cartes permanent ne comptent pas dans les 40 a 50.
    const estPermanente = (c) => !!(c && c.desc && c.desc.Permanent);
    const signature = marvelous ? 0 : ((hero.deck && hero.deck.hero_deck) || []).filter((id) => !estPermanente(carte(String(id).split(",")[0]))).length;
    let total = signature;
    let empruntees = 0;
    const parTitre = new Map();
    // On COMPTE par aspect au lieu de collectionner les noms : le quota de
    // Fatalis a besoin de savoir lequel pese le plus lourd (c'est l'aspect
    // « choisi ») et combien de cartes sont empruntees a chacun des autres.
    const parAspect = new Map();    // classe -> nombre de cartes
    const admissibles = new Map();  // classe -> cartes de cette classe qui passent le test du quota
    const titresAdmissibles = new Map();  // classe -> titres de ces cartes
    const quota = quotaHorsAspect(hero, t);
    const interdits = typesInterdits(hero);
    const interditsAspect = typesInterditsAspect(hero);
    const idHeros = hero.id || "";
    const horsDeckJoueur = [];   // cartes de rencontre, ou signatures d'un autre heros
    const typesRefuses = [];     // « no additional allies » et consorts
    const exclusivesRefusees = [];  // cartes réservées à une série (TMNT) hors de ses héros
    // Cartes DOUBLE ASPECT : leur aspect se decide APRES le decompte des autres
    // (elles rejoignent un aspect deja present, sinon le moins couteux).
    const doubles = [];          // { aspects, n, c }
    // TMNT Shinobi (17/10/2026) : les cartes Shinobi (ni aspect ni Basic) et le Path choisi.
    const shinobis = [];         // { brute, c }
    const chemins = [];          // { brute, c, id, regles }
    for (const [id, n] of choisies) {
        const c = carte(id);
        if (!c) continue;
        const brute = carteBrute(id);
        if (estPath(brute)) chemins.push({ brute, c, id, n, regles: reglesDuPath(brute, id) });
        else if (estShinobi(brute)) shinobis.push({ brute, c });
        // Carte EXCLUSIVE à une série (TMNT) : seulement dans le deck d'un de ses héros.
        if (exclusiveRefusee(brute.set_name, hero.heroCardId || hero.id)) exclusivesRefusees.push(c.name);
        if (estDoubleAspect(brute)) {
            if (!estPermanente(c)) total += n;
            const copie = cleCopie(c);
            parTitre.set(copie, {
                n: (parTitre.get(copie)?.n || 0) + n,
                max: estUnique(c) ? 1 : maxParDeck(c),
                nom: titreDe(c) + (c.subtitle ? ` (${c.subtitle})` : ""),
            });
            if (!estTypeJouable(c)) horsDeckJoueur.push(c.name);
            else if (interdits.includes(String(c.type)) || interditsAspect.includes(String(c.type))) typesRefuses.push(c.name);
            if (!exemptDeLaLimiteAspect(hero, c)) doubles.push({ aspects: aspectsDeClasse(brute.class), n, c });
            continue;
        }
        if (!estPermanente(c)) total += n;
        const copie = cleCopie(c);
        parTitre.set(copie, {
            n: (parTitre.get(copie)?.n || 0) + n,
            max: estUnique(c) ? 1 : maxParDeck(c),
            nom: titreDe(c) + (c.subtitle ? ` (${c.subtitle})` : ""),
        });
        // Rien ne garantissait jusqu'ici que la carte soit seulement JOUABLE :
        // un attachement de rencontre (Magical Suspension, 15026) passait tous
        // les controles, faute de `class`, et sortait « deck legal ».
        if (!estCarteJoueur(c) && !(marvelous && estCarteSignature(c))) horsDeckJoueur.push(c.name);
        else if (interdits.includes(String(c.type))) typesRefuses.push(c.name);
        else if (interditsAspect.includes(String(c.type)) && ASPECTS.includes(c.class)) typesRefuses.push(c.name);
        if (estSignature(c)) empruntees += n;
        else if (estShinobi(brute) || estPath(brute)) {
            // Ni aspect ni Basic (livret p.8) : rien a compter ici, les regles du Path sont jugees plus bas.
        }
        else if (c.class && !CLASSES_NEUTRES.includes(c.class)
                 && !exemptDeLaLimiteAspect(hero, c)) {
            parAspect.set(c.class, (parAspect.get(c.class) || 0) + n);
            if (quota && quota.test(c)) {
                admissibles.set(c.class, (admissibles.get(c.class) || 0) + n);
                titresAdmissibles.set(c.class, (titresAdmissibles.get(c.class) || new Set()).add(c.name));
            }
        }
    }

    // Doubles aspects : une carte « Aggression;Justice » compte pour un aspect DEJA
    // present dans le deck (le moins fourni des deux s'ils le sont tous les deux,
    // pour l'egalite exigee par Spider-Woman) ; sinon, on ouvre l'aspect qui couvre
    // le plus de doubles restants (le premier imprime a egalite). Un deck n'en
    // compte ainsi jamais plus que necessaire.
    let restants = doubles;
    while (restants.length) {
        const pendants = [];
        for (const d of restants) {
            const presents = d.aspects.filter((a) => parAspect.has(a));
            if (!presents.length) { pendants.push(d); continue; }
            presents.sort((a, b) => parAspect.get(a) - parAspect.get(b));
            parAspect.set(presents[0], parAspect.get(presents[0]) + d.n);
        }
        if (!pendants.length) break;
        const couverture = new Map();
        for (const d of pendants) for (const a of d.aspects) couverture.set(a, (couverture.get(a) || 0) + 1);
        const ouvert = [...couverture.entries()].sort((a, b) => b[1] - a[1])[0][0];
        parAspect.set(ouvert, 0);
        restants = pendants;
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
            if ((admissibles.get(classe) || 0) === n) {
                horsAspect += quota.parTitre ? titresAdmissibles.get(classe).size : n;
                sortis.push(classe);
            }
        }
        for (const classe of sortis) parAspect.delete(classe);
    }
    const aspects = new Set(parAspect.keys());
    // Multiverse (glossaire MC4DB, 29/09/2026) : une carte Multiverse REMPLACE
    // la carte de meme numero de set, elle ne s'y ajoute pas. Les deux versions
    // ne cohabitent donc jamais dans un deck, signatures du heros comprises
    // (`multiverse_of` dans cards.json designe l'originale).
    const presentes = new Map();
    for (const id of ((hero.deck && hero.deck.hero_deck) || [])) {
        const cle = String(id).split(",")[0];
        const c0 = carte(cle);
        if (c0) presentes.set(cle, c0);
    }
    for (const [id] of choisies) {
        const c0 = carte(id);
        if (c0) presentes.set(String(id), c0);
    }
    for (const c0 of presentes.values()) {
        const originale = c0.multiverse_of && presentes.get(String(c0.multiverse_of));
        if (originale) {
            problemes.push(`${t("Multiverse :")} « ${c0.name} » ${t("remplace")} « ${originale.name} », ${t("pas les deux")}`);
        }
    }
    if (horsDeckJoueur.length) {
        problemes.push(`${t("Cartes qui n’appartiennent pas à un deck de joueur :")} ${[...new Set(horsDeckJoueur)].join(", ")}`);
    }
    if (exclusivesRefusees.length) {
        problemes.push(`${t("Cartes réservées aux héros TMNT :")} ${[...new Set(exclusivesRefusees)].join(", ")}`);
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
    // ---- TMNT SHINOBI (17/10/2026) : le Path, ses types Shinobi, ses aspects, ses plafonds ----
    // « Follow your Path deck-building rules in conjunction with the standard deck-building rules » (livret p.5) :
    // les regles du Path S'AJOUTENT a celles du heros. Un Path ne remplace une regle du heros que quand il le dit
    // (The Last Ronin : « any combination of aspect cards »).
    const propre = reglesDuPathPropre(hero);
    const nbPaths = chemins.reduce((s, x) => s + x.n, 0);
    const regles = chemins.length ? chemins[0].regles : propre;
    if (nbPaths > 1 || (propre && nbPaths >= 1)) {
        problemes.push(`${t("Un seul Path par deck :")} ${[...new Set(chemins.map((x) => titreDe(x.c)))].join(", ")}`
            + (propre ? ` (${t("ce héros a déjà sa Voie")})` : ""));
    }
    if (shinobis.length && !regles) {
        problemes.push(`${t("Cartes Shinobi sans Path :")} ${[...new Set(shinobis.map((x) => x.c.name))].join(", ")}`);
    }
    if (regles) {
        const refusees = shinobis.filter((x) => !admiseParLePath(x.brute, regles)).map((x) => x.c.name);
        if (refusees.length) {
            problemes.push(`${t("Types Shinobi non autorisés par le Path")} ${regles.nom} (${regles.types.join(", ")}) : ${[...new Set(refusees)].join(", ")}`);
        }
    }
    let aspectsMax = regle.max;
    let aspectsLabel = regle.label;
    if (regles) {
        const pm = regles.aspects.max;
        if (regles.aspects.libre) { aspectsMax = Math.max(aspectsMax, pm); aspectsLabel = t("une combinaison libre d’aspects (Path)"); }
        else if (Math.min(aspectsMax, pm) >= regle.min) {
            aspectsMax = Math.min(aspectsMax, pm);
            aspectsLabel = pm === 0 ? t("aucun aspect (Path)") : (pm === 1 ? t("un seul aspect (Path)") : aspectsLabel);
        }
    }
    if (aspects.size < regle.min) problemes.push(`${t("Ce héros requiert")} ${regle.label} — ${t("actuellement")} ${aspects.size}`);
    if (aspects.size > aspectsMax) {
        problemes.push(`${t("Trop d’aspects")} (${[...aspects].join(", ")}) — ${t("autorisé :")} ${aspectsLabel}`
            + (quota ? ` ${t("+ au plus")} ${quota.label}` : ""));
    }
    if (quota && horsAspect > quota.max) {
        problemes.push(`${t("Hors aspect : au plus")} ${quota.label} — ${t("actuellement")} ${horsAspect}`);
    }
    // Adam Warlock (21031b) : « You cannot include more than 1 copy of any
    // non-Adam Warlock card » (ses signatures ne sont pas dans `choisies`).
    // The Last Ronin (« You may add only one copy of any card to your deck ») : 1 exemplaire de TOUTE carte.
    const maxPath = regles && regles.maxExemplaires ? regles.maxExemplaires : Infinity;
    const maxCopies = Math.min(idHeros === "adam_warlock" ? 1 : Infinity, maxPath);
    for (const x of parTitre.values()) {
        const max = Math.min(x.max, maxCopies);
        if (x.n > max) problemes.push(`${t("Trop d’exemplaires de")} « ${x.nom} » : ${x.n}/${max}`);
    }
    // Livret Fear No Evil p.3 : une seule CARTE avec starting par deck (deux exemplaires d'un titre comptent deux).
    const starting = [];
    let nbStarting = 0;
    for (const [id, n] of choisies) {
        const c = carte(id);
        if (c && /(^|\n)\s*Starting\b/.test(String(c.text || ""))) { starting.push(c.name); nbStarting += n; }
    }
    if (nbStarting > 1) problemes.push(`${t("Une seule carte Starting par deck :")} ${starting.join(", ")}`);
    problemes.push(...problemesUnicite(hero, choisies, carte, t));
    // Autant de cartes de chaque aspect : Spider-Woman (04031b, ses deux
    // aspects) et Adam Warlock (21031b, les quatre).
    const egaux = idHeros === "spider_woman" ? 2 : idHeros === "adam_warlock" ? 4 : 0;
    if (egaux && aspects.size === egaux) {
        const nombres = [...parAspect.values()];
        if (Math.min(...nombres) !== Math.max(...nombres)) {
            problemes.push(`${t("Il faut autant de cartes de chaque aspect")} (${[...parAspect].map(([a, n]) => `${a} ${n}`).join(", ")})`);
        }
    }
    if (idHeros === "adam_warlock" && aspects.size > 0 && aspects.size < 4) {
        problemes.push(`${t("Il faut les 4 aspects (Adam Warlock)")} — ${t("actuellement")} ${aspects.size}`);
    }
    // Moon Knight (mk001b, Cheap Shots) : aucune carte de cout imprime 3 ou
    // plus, et au moins 4 cartes de chaque aspect.
    if (idHeros === "moon_knight") {
        const chers = [];
        for (const [id] of choisies) {
            const c = carte(id);
            const cout = Number(String((c && c.desc && c.desc.Cost) ?? "").trim());
            if (c && Number.isFinite(cout) && cout >= 3) chers.push(c.name);
        }
        if (chers.length) problemes.push(`${t("Coût imprimé 3 ou plus interdit (Moon Knight) :")} ${[...new Set(chers)].join(", ")}`);
        const manquants = ["Aggression", "Justice", "Leadership", "Protection"].filter((a) => (parAspect.get(a) || 0) < 4);
        if (manquants.length) problemes.push(`${t("Au moins 4 cartes de chaque aspect (Moon Knight) :")} ${manquants.join(", ")}`);
    }
    return { ok: problemes.length === 0, problemes, total, aspects: [...aspects], signature, empruntees,
             horsAspect, quotaMax: quota ? quota.max : 0,
             imposees: cartesImposees(choisies, carte) };
}
