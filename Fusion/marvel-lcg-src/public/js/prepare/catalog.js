// catalog.js — construit les modèles de haut niveau (héros, scénarios, extensions,
// sets de rencontre) à partir des données brutes + métadonnées de cartes.
"use strict";
import { sansVariantesDeCampagne } from "/public/js/prepare/underlings.js";
import { api, fileName } from "/public/js/prepare/api.js";
import { regrouperVariantes, cleIdentite } from "/public/js/prepare/variantes.js";
import { cards } from "/public/js/prepare/cards.js";
import { auteurUnique } from "/public/js/prepare/auteur.js";

const TEAMS = ["Avenger", "X-Men", "Guardian", "Champion", "Defender", "X-Force", "Inhuman", "S.H.I.E.L.D.", "Web-Warrior"];
const num = (s) => { const m = String(s).match(/^\s*(\d+)/); return m ? +m[1] : 9999; };
const titleize = (s) => String(s).replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

// Nom affiché d'un set de rencontre (18/10/2026). Le fichier du set de Shredder porte un préfixe de
// pack (`ts_chunin`) que titleize rendait « Ts Chunin » ; les cartes, elles, disent « Chunin » : le nom
// sert aussi à retrouver le créateur dans `set_name` (voir `_auteurParSet`). Même règle pour tout
// futur set dont le fichier garde un préfixe : l'ajouter ici.
const NOMS_SETS_RENCONTRE = {
    ts_shredder: "Shredder",
    ts_chunin: "Chunin",
    ts_foot_goon_squad: "Foot Goon Squad",
    ts_shadow_of_the_foot: "Shadow of the Foot",
};
const nomSetRencontre = (n) => NOMS_SETS_RENCONTRE[String(n)] || titleize(n);
const cleanName = (s) => String(s || "").replace(/^\*\s*/, "").trim();

function teamFromTraits(card) {
    if (!card || !card.traits) return "";
    for (const t of TEAMS) if (card.traits.some((x) => String(x).toLowerCase().includes(t.toLowerCase().replace(/\W/g, "")))) return t;
    return card.traits[0] || "";
}
const ASPECTS_DOUBLES = ["aggression", "justice", "leadership", "protection", "'pool", "determination", "venomized"];
function aspectsOfDeck(deck) {
    if (!deck || !deck.player_deck) return [];
    const s = new Set();
    // Double aspect (« aggression;justice », pack tmnt_aspect_dual) : il rejoint un
    // aspect deja present ; seul, il apporte son premier aspect imprime.
    const doubles = [];
    for (const id of deck.player_deck) {
        const a = cards.aspectOf(id);
        const parts = (a || "").split(";").map((p) => p.trim());
        if (parts.length >= 2 && parts.every((p) => ASPECTS_DOUBLES.includes(p))) doubles.push(parts);
        else if (a && a !== "basic") s.add(a);
    }
    for (const parts of doubles) if (!parts.some((p) => s.has(p))) s.add(parts[0]);
    return [...s];
}

/** Traits qui distinguent une identité d'une autre (les traits communs sautent). */
function traitsDistinctifs(traitsA, traitsB) {
    const b = new Set(traitsB || []);
    return (traitsA || []).filter((t) => !b.has(t));
}

/**
 * Lève les HOMONYMES de la grille : dix noms imprimés désignent vingt-deux
 * héros différents, et la vignette n'affiche que ce nom.
 *
 * Signalé en jeu le 09/09/2026 : le filtre FAN-MADE alignait QUATRE tuiles
 * « SPIDER-MAN » côte à côte (Spider-Man 2099, Spider-Man (Rainy) et les deux
 * alter-ego de Superior Spider-Man), impossibles à distinguer autrement qu'en
 * reconnaissant l'illustration. C'est normal côté cartes — Miguel O'Hara et
 * Otto Octavius s'appellent tous « Spider-Man » sur le papier — et ça ne l'est
 * pas côté écran de choix.
 *
 * Les autres groupes touchés : Black Panther, Hawkeye, Hulk, Iron Man, Jessica
 * Jones, Thor, Venom, Wolverine.
 *
 * Règle : on ne touche PAS aux noms uniques. Dans un groupe d'homonymes, chaque
 * héros prend le premier libellé qui le distingue de ses homonymes — le nom de
 * son DECK, sinon le `set_name` de sa face héros. Aucun des deux ne suffit
 * seul : les deux Superior Spider-Man partagent leur `set_name`, Spider-Man et
 * Miles Morales partagent leur nom de deck.
 */
function leverLesHomonymes(heros) {
    const parNom = new Map();
    for (const h of heros) {
        const groupe = parNom.get(h.name) || [];
        groupe.push(h);
        parNom.set(h.name, groupe);
    }
    for (const groupe of parNom.values()) {
        if (groupe.length < 2) continue;
        const candidats = groupe.map((h) => {
            const carte = cards.get(h.heroCardId);
            return [cleanName(h.deck && h.deck.name), cleanName(carte && carte.set_name)]
                .filter(Boolean);
        });
        for (let i = 0; i < groupe.length; i++) {
            // Unique DANS LE GROUPE : ailleurs dans la grille le nom ne
            // collisionne pas, sinon ce héros serait dans ce groupe.
            const seul = (libelle) => candidats.every(
                (autres, j) => j === i || !autres.includes(libelle));
            // Dernier recours : le nom du deck. Il n'a jamais échoué sur les
            // 129 decks du dépôt, mais un doublon parfait resterait ambigu
            // plutôt que de faire disparaître un héros.
            const libelle = candidats[i].find(seul) || candidats[i][0] || groupe[i].name;
            if (libelle === groupe[i].name) continue;
            groupe[i].name = libelle;
            // La botte de foin suit le libellé, sinon taper « 2099 » ne rendrait
            // rien alors que la tuile l'affiche.
            groupe[i].recherche += " " + libelle.toLowerCase();
        }
    }
    return heros;
}

/** Identités jouables d'un héros : la face de base, puis `metadata.hero_alts`.
 *  Renvoie [] quand il n'y a pas de variante, pour que le wizard n'affiche
 *  aucun sélecteur dans le cas courant. */
function identityVariants(deck, heroCardId, heroCard) {
    const alts = (deck.metadata && deck.metadata.hero_alts) || [];
    if (!alts.length) return [];
    const base = {
        hero: deck.hero,
        heroCardId,
        cle: cleIdentite({ hero: deck.hero, heroCardId }),
        name: cleanName(heroCard && heroCard.name) || deck.name,
        traits: (heroCard && heroCard.traits) || [],
    };
    const out = [base];
    for (const alt of alts) {
        if (!alt || !alt.hero || !alt.hero.length) continue;
        const id = String(alt.hero[0]).split(",")[0];
        const c = cards.get(id);
        out.push({
            hero: alt.hero,
            heroCardId: id,
            // ⚠ La clé est le COUPLE de faces : Superior Spider-Man garde la
            // même face héros et change d'alter ego.
            cle: cleIdentite({ hero: alt.hero, heroCardId: id }),
            name: alt.name || cleanName(c && c.name) || base.name,
            traits: (c && c.traits) || [],
        });
    }
    // Ce qui différencie chaque identité des autres : sert de libellé.
    for (const v of out) {
        const autres = out.filter((x) => x !== v).flatMap((x) => x.traits);
        v.distinctif = traitsDistinctifs(v.traits, autres);
    }
    return out.length > 1 ? out : [];
}
/* --------------------------------------------------------------------------
 * Les vagues de sortie
 *
 * REGLE : une vague s'ouvre sur une GRANDE BOITE et court jusqu'a la suivante.
 * Le Set de base est a part — c'est le point de depart, pas une vague.
 * L'exception est la vague 1, qui n'a pas de grande boite a son ouverture : elle
 * regroupe tout ce qui a suivi le Set de base jusqu'a Hulk (7/8/2020), La
 * Chute du Crane Rouge (4/9/2020) ouvrant la vague 2.
 *
 * La table est indexee par le NUMERO que porte la cle d'extension dans
 * sets_info.json (« 12. Ant-Man » -> 12). Ce numero est deja l'ordre de sortie
 * du jeu, donc la table se lit comme une frise et un nouveau paquet se range
 * en ajoutant une seule borne.
 *
 * Sources : dates de sortie de marvelcdb.com/api/public/packs, et le decoupage
 * des vagues 1 a 7 publie par la communaute. Les vagues 8 a 11 prolongent la
 * MEME regle (Age of Apocalypse, Agents du S.H.I.E.L.D., Civil War, Fear No
 * Evil ouvrent chacune la leur) sans qu'une liste publiee ne les confirme
 * encore : si FFG les decoupait autrement, il suffirait de deplacer une borne.
 *
 * Les paquets fan-made (98 et au-dela) n'ont pas de vague : ils vivent derriere
 * le bouton « Fan-made », qui ne les melange jamais aux officiels.
 * ------------------------------------------------------------------------ */
const BORNES_VAGUES = [
    { depuis: 1,  vague: 0 },    // Set de base
    { depuis: 2,  vague: 1 },    // Bouffon Vert -> Hulk
    { depuis: 4,  vague: 2 },    // The Rise of Red Skull
    { depuis: 5,  vague: 1 },    // (la boite 4 s'intercale dans l'ordre du jeu)
    { depuis: 11, vague: 2 },    // Kang -> Sorciere Rouge
    { depuis: 16, vague: 3 },    // The Galaxy's Most Wanted
    { depuis: 21, vague: 4 },    // The Mad Titan's Shadow
    { depuis: 27, vague: 5 },    // Sinister Motives
    { depuis: 32, vague: 6 },    // Mutant Genesis
    { depuis: 40, vague: 7 },    // NeXt Evolution
    { depuis: 45, vague: 8 },    // Age of Apocalypse
    { depuis: 50, vague: 9 },    // Agents of S.H.I.E.L.D.
    { depuis: 56, vague: 10 },   // Civil War
    { depuis: 60, vague: 11 },   // Fear No Evil
    { depuis: 61, vague: null }, // au-dela : hors vague (modulaires, defis)
];

/* Le NOM d'une vague est celui de la grande boite qui l'ouvre — c'est la meme
 * regle que les bornes ci-dessus, lue dans l'autre sens, donc les deux tables
 * se completent ligne a ligne et une nouvelle vague s'ajoute aux deux endroits.
 *
 * Titres EN : ceux que portent les cles d'extension dans sets_info.json et le
 * `nom_en` des campagnes. Ils ne passent pas par le dictionnaire. Les titres
 * FRANCAIS (imprimes sur les boites vendues en France) vivent depuis le
 * 29/09/2026 dans `titres-extensions.js` (`TITRES_FR`, par numero), appliques
 * par l'ecran de preparation (`nomExtension`, `titreDeBoite`).
 *
 * La vague 1 n'est pas ici : sans grande boite, elle n'a pas de titre a copier.
 * Son libelle est du texte a nous, donc traduit comme le reste (voir
 * `nomDeVague` dans app.js). */
const NOMS_VAGUES = {
    2:  "The Rise of Red Skull",
    3:  "The Galaxy's Most Wanted",
    4:  "The Mad Titan's Shadow",
    5:  "Sinister Motives",
    6:  "Mutant Genesis",
    7:  "NeXt Evolution",
    8:  "Age of Apocalypse",
    9:  "Agents of S.H.I.E.L.D.",
    10: "Civil War",
    11: "Fear No Evil",
};

/** Titre de la grande boite qui ouvre une vague. "" si la vague n'en a pas —
 *  le Set de base (0), ou une vague future dont la table ignore encore le nom :
 *  l'appelant retombe alors sur le seul numero, jamais sur un trou. */
function titreDeVague(vague) {
    return NOMS_VAGUES[vague] || "";
}

/** Vague d'une extension, d'apres le numero que porte sa clé. null si aucune
 *  (fan-made, sets modulaires, defis hebdomadaires). */
function vagueDeLExtension(cle) {
    const n = parseInt(String(cle || ""), 10);
    if (!Number.isFinite(n) || n >= 90) return null;
    let vague = null;
    for (const borne of BORNES_VAGUES) {
        if (n >= borne.depuis) vague = borne.vague;
    }
    return vague;
}

/** Seconde identité d'un héros qui en compte DEUX pour un seul joueur.
 *
 *  Le pack Cloak & Dagger est bâti ainsi : `linked_identity` porte une identité
 *  complète (faces héros/alter-ego + son propre mini-deck), jouée en même temps
 *  que la principale et par le même joueur. C'est la seule clé qui le dit, donc
 *  la seule sur laquelle s'appuyer : aucun identifiant en dur ici, un futur duo
 *  bâti pareil sera montré double sans rien toucher.
 *
 *  Renvoie null pour les 66 autres héros, qui gardent exactement leur rendu. */
function identiteLiee(deck) {
    const lie = deck.linked_identity;
    if (!lie || !lie.hero || !lie.hero.length) return null;
    const heroCardId = String(lie.hero[0]).split(",")[0];
    const c = cards.get(heroCardId);
    return {
        hero: lie.hero,
        heroCardId,
        name: cleanName(c && c.name) || "",
        hp: c ? c.hp : undefined,
    };
}

/** Héros fan-made : soit rattaché à une extension « Custom » (ex. « 99. Custom
 *  (Rainy) » pour Thor Jane Foster), soit rattaché à aucune extension officielle
 *  (Stan Lee, Hulk (Rainy)). Rien à maintenir à la main. */
function isHomebrew(extension) {
    return !extension || /custom/i.test(extension);
}
/** Un paquet du tableur est COMPLET quand il peut faire un deck a lui seul
 *  avec les 15 cartes signature : au moins 24 cartes (Venomized en a 24, les
 *  autres 30). Les colonnes bi-aspect de Spider-Woman (11 cartes) ne le sont
 *  pas : elles n'existent qu'assemblees par deux (resoudrePackage). */
const PAQUET_COMPLET_MIN = 24;

/** L'ordre de presentation des paquets, apres ceux que le tableur conseille :
 *  les generiques d'abord (un aspect, aucun trait exige), puis les paquets
 *  d'equipe (X-Men, Guardian, Champion...) et les speciaux (Venomized, Silly
 *  'Pool), dans l'ordre du tableur. */
const GENERIQUES_D_ABORD = [
    "Brutish Aggression", "Graceful Aggression", "Warrior's Aggression", "Reckless Aggression",
    "Defiant Justice", "Evasive Justice", "Strategic Justice",
    "Courageous Leadership", "Commanding Leadership", "Sacrificial Leadership",
    "Unyielding Protection", "Debilitating Protection",
];

/** Un heros a un deck de base quand son fichier porte une moitie d'aspect :
 *  les officiels, et les fan-made dont l'auteur a publie sa decklist. Les
 *  autres ont `player_deck` vide (PROCESSUS-HEROS, etape 3) : leur deck de
 *  base ne se joue pas, on ne le propose pas. */
export function aDeckDeBase(hero) {
    return !!(hero && hero.deck && (hero.deck.player_deck || []).length);
}

/** Les trois ressources de base, socle commun à TOUTES les colonnes du tableur.
 *
 *  Vérifié colonne par colonne : sur les 32 paquets, aucun ne se passe d'Energy,
 *  Genius et Strength. Les cinq colonnes de Spider-Woman sont les seules à
 *  n'avoir AUCUNE carte Basic — elles ne listent que l'aspect, parce qu'elles
 *  sont faites pour être jouées par deux. Voir resoudrePackage(). */
const SOCLE_BASIC = ["01088", "01089", "01090"]; // Energy, Genius, Strength

function encounterKind(name) {
    if (name.startsWith("standard") || name.startsWith("tmnt_standard")) return "standard";
    if (name.startsWith("expert") || name.startsWith("tmnt_expert")) return "expert";
    if (name.endsWith("_nemesis")) return "nemesis";
    return "modular";
}

let _extensions = null, _heroes = null, _encounterSets = null;
// Index `set_name` -> createur du contenu fan-made (18/09/2026), bati une fois.
let _auteurParSet = null;
// Sets de rencontre d'une extension marquee `indisponible` dans sets_info.json.
// Rempli par extensions(), lu par encounterSets() : l'ecran de preparation ne
// propose pas un set mis de cote. Meme principe que `_setsMasques` juste en
// dessous, mais pour les sets modulaires plutot que pour les cartes signature.
let _setsRencontreMasques = new Set();
// `set_name` des héros marqués `metadata.indisponible` dans leur deck de
// départ. Rempli par heroes(), lu par setsMasques() : le deckbuilder s'en sert
// pour ne pas proposer les cartes signature d'un héros retiré du jeu.
let _setsMasques = new Set();
// `set_name` des cartes d'une extension marquee `indisponible` dans sets_info.json
// (cle `set_names`). Rempli par extensions(), fusionne dans _setsMasques par heroes().
let _setsMasquesExt = new Set();
const _scenariosByExt = new Map();

export const catalog = {
    async extensions() {
        if (_extensions) return _extensions;
        const raw = await api.setsInfo();
        // Extensions MISES DE COTE : `indisponible: true` dans sets_info.json.
        // L'entree reste dans le fichier, les cartes restent construites et les
        // cas de test continuent de tourner ; seule l'interface cesse de les
        // montrer. Ajoute le 13/09/2026 pour le set modulaire Muse, qui ne doit
        // pas partir en production. Pour remettre une extension : supprimer la
        // cle `indisponible`.
        _setsRencontreMasques = new Set();
        _setsMasquesExt = new Set();
        Object.entries(raw).forEach(([, v]) => {
            if (!v || !v.indisponible) return;
            (v.set_names || []).forEach((n) => _setsMasquesExt.add(n));
            (v.encounters || []).forEach((n) => _setsRencontreMasques.add(n));
        });
        _extensions = Object.entries(raw).filter(([, v]) => !(v && v.indisponible))
            .map(([key, v]) => ({
            key, code: v.name, scenarios: v.scenarios || [], heroes: v.heroes || [],
            encounters: v.encounters || [], maxId: v.max_id,
            // Fear No Evil (18/09/2026) : manigances a vilain interchangeable,
            // repliees en une tuile par manigance (underlings.js).
            underlings: v.underlings || [], manigances: v.manigances || [],
            // MC×DC 2026 : les variantes de CAMPAGNE (combats 2 et 3), retirees de la liste libre (underlings.js `sansVariantesDeCampagne`).
            scenariosCampagne: v.scenarios_campagne || [],
        })).sort((a, b) => num(a.key) - num(b.key));
        // Onglet synthétique « Défis » : les défis mensuels de data/challenges
        // sont des scénarios complets (méchant fixe + carte Défi via
        // raw.challenges), absents de sets_info.json. Détectés par leur nom.
        try {
            const defis = (await api.listScenarios()).map(fileName)
                .filter((n) => /^24\d{2}_/.test(n) || n === "wild").sort();
            if (defis.length) {
                _extensions.push({ key: "defis", code: "Défis", scenarios: defis, heroes: [], encounters: [], maxId: 0 });
            }
        } catch (e) {}
        return _extensions;
    },

    async heroes() {
        if (_heroes) return _heroes;
        await cards.load();
        const exts = await this.extensions();
        const heroExt = {};
        exts.forEach((e) => e.heroes.forEach((h) => (heroExt[h] = e.key)));
        const ids = (await api.listStarterDecks()).map(fileName);
        const loaded = await Promise.all(ids.map((id) => api.deck(id).then((d) => ({ id, d })).catch(() => null)));
        // Héros RETIRÉS du jeu : `metadata.indisponible` dans leur deck de
        // départ. Le fichier reste dans deck/starter/ — c'est volontaire, pour
        // que les cas de tools/test_capacites.py continuent de tourner (le
        // harnais charge le deck par son nom) : on masque un héros sans perdre
        // sa couverture de test. Ajouté le 01/09/2026 pour Squirrel Girl.
        // Cette liste sert aussi au deckbuilder, qui appelle heroes().
        // ⚠ On collecte les set_name depuis TOUTES les cartes du deck, pas
        // seulement depuis la face héros : un pack en compte souvent plusieurs.
        // Squirrel Girl en a trois (« Squirrel Girl », « Squirrel Deck » pour
        // les six écureuils mis de côté, « Squirrel Girl Nemesis »), et ses six
        // cartes empruntables sont justement dans « Squirrel Deck ».
        _setsMasques = new Set(_setsMasquesExt);
        loaded.forEach((x) => {
            if (!x || !x.d || !x.d.metadata || !x.d.metadata.indisponible) return;
            const d = x.d;
            const listes = [d.hero, d.hero_deck, d.set_aside, d.obligations, d.nemesis_set];
            listes.forEach((liste) => (liste || []).forEach((entree) => {
                const cid = String(entree).split(",")[0];
                const c = cards.get(cid);
                if (c && c.set_name) _setsMasques.add(c.set_name);
            }));
        });
        _heroes = loaded.filter((x) => x && x.d && x.d.hero && x.d.hero.length
                                       && !(x.d.metadata && x.d.metadata.indisponible)).map(({ id, d }) => {
            const heroCardId = d.hero[0].split(",")[0];
            const c = cards.get(heroCardId);
            // La face ALTER-EGO, deuxieme id de l'entree « recto,verso ». Ses
            // traits ne sont pas ceux du heros — Spider-Man est AVENGER, Peter
            // Parker est GENIUS — et la recherche de la grille mord sur les
            // deux : on cherche un heros par ce qu'il EST des deux cotes.
            const alterEgoCardId = String(d.hero[0]).split(",")[1] || "";
            const ae = alterEgoCardId ? cards.get(alterEgoCardId) : null;
            const traitsHeros = c ? c.traits || [] : [];
            const traitsAlterEgo = ae ? ae.traits || [] : [];
            const traitsDesDeuxFaces = [...traitsHeros, ...traitsAlterEgo];
            const traitsCherchables = traitsDesDeuxFaces.concat(
                traitsDesDeuxFaces
                    .map((x) => String(x).replace(/[^0-9a-zA-Z]+/g, ""))
                    .filter((x, i) => x !== traitsDesDeuxFaces[i]));
            const extension = heroExt[id] || "";
            const nom = cleanName(c && c.name) || cleanName(d.name) || titleize(id);
            const auteur = (c && c.custom) || "";
            return {
                id, heroCardId, baseDeckId: id, deck: d,
                name: nom,
                hp: c ? c.hp : undefined,
                handSize: cards.handSizeOf(heroCardId),
                traits: traitsHeros,
                alterEgoCardId,
                traitsAlterEgo,
                // Botte de foin de la recherche, en minuscules et calculee une
                // seule fois : refaire un toLowerCase() sur deux cents heros a
                // chaque frappe pour un resultat toujours identique serait du
                // travail jete. Les traits restent en anglais dans les deux
                // langues (les textes francais disent « le trait AVENGER »),
                // donc rien a traduire ici.
                //
                // Chaque trait ponctue est range DEUX fois, avec et sans sa
                // ponctuation : personne ne tape « S.H.I.E.L.D » avec ses
                // points, et « webwarrior » doit trouver WEB-WARRIOR autant que
                // « web-warrior ». Meme geste que teamFromTraits plus haut.
                //
                // Le CREATEUR y entre aussi (18/09/2026) : taper « nugget »
                // rend Lockjaw, et « rainy » tout ce que Rainy a dessine. Il
                // est range en entier, donc « bluehg » trouve aussi un pack
                // signe « BlueHG + DesignHacker ».
                recherche: [nom, ...traitsCherchables, auteur].join(" ").toLowerCase(),
                team: teamFromTraits(c),
                extension,
                vague: vagueDeLExtension(extension),
                homebrew: isHomebrew(extension),
                // Créateur du pack fan-made (champ `custom` de la face héros,
                // GUIDE §14) : affiché entre parenthèses derrière le nom.
                auteur,
                aspects: aspectsOfDeck(d),
                // Identités alternatives : même deck, autres faces héros /
                // alter-ego (ex. The Thing en Gardien de la Galaxie). Elles
                // ne créent PAS un second héros dans la grille : le wizard les
                // propose comme un choix d'identité à l'étape des decks.
                variants: identityVariants(d, heroCardId, c),
                // Identité LIÉE : deux héros pour un seul joueur (Cloak &
                // Dagger). Rien à voir avec `variants`, qui propose un choix :
                // ici les deux identités arrivent ENSEMBLE, chacune avec son
                // mini-deck. La grille doit donc les montrer toutes les deux.
                lie: identiteLiee(d),
            };
        });
        // Les homonymes sont levés AVANT le tri : le libellé final est ce qui
        // range la grille, sinon les quatre Spider-Man resteraient collés.
        // Une seule tuile par héros : les decks « variante_de » se replient sous
        // leur base (modale du héros, 11/09/2026). AVANT les homonymes : deux
        // versions d'un même héros ne sont pas des homonymes à distinguer.
        _heroes = leverLesHomonymes(regrouperVariantes(_heroes)).sort((a, b) => a.name.localeCompare(b.name));
        return _heroes;
    },

    /** `set_name` des héros retirés du jeu (`metadata.indisponible`).
     *  Appeler heroes() d'abord : c'est lui qui remplit la liste. */
    async setsMasques() {
        await this.heroes();
        return _setsMasques;
    },

    /** Decks jouables pour un héros donné : base (s'il en a un) + sauvegardés + paquets d'aspect. */
    async decksForHero(hero) {
        await cards.load();
        const out = aDeckDeBase(hero)
            ? [{ id: hero.baseDeckId, name: hero.deck.name || hero.name, source: "base", deck: hero.deck, aspects: hero.aspects }]
            : [];
        try {
            const savedIds = (await api.listSavedDecks()).map(fileName);
            for (const id of savedIds) {
                try {
                    const d = await api.deck(id);
                    if (d && d.hero && d.hero[0] && d.hero[0].split(",")[0] === hero.heroCardId) {
                        // Les decks par heros du tableur « Universal Prebuilt Decks »
                        // (deck/custom/prebuilt_*) ne sont PAS des decks sauvegardes
                        // par le joueur : ils portent leur propre origine.
                        const duTableur = String((d.metadata || {}).source || "").startsWith("Universal Prebuilt Decks");
                        out.push({ id, name: d.name || id, source: duTableur ? "tableur" : "saved", deck: d, aspects: aspectsOfDeck(d) });
                    }
                } catch (e) {}
            }
        } catch (e) {}
        out.push(...await this.packagesAspect(hero));
        return out;
    },

    /** Packages d'aspect proposes a CE heros, assembles a la volee.
     *  Les 30 cartes d'un package ne sont que la partie « aspect » : on y colle
     *  les cartes signature, l'obligation et le nemesis du deck de base.
     *
     *  TOUS les paquets complets du tableur, pour TOUS les heros (decision de
     *  l'utilisateur du 12/09/2026 : « tu les presentes tous pour tous les
     *  personnages »), ceux que le tableur conseille au heros en tete, marques
     *  « Conseille ». Avant, seuls les 4 conseilles (ou 12 generiques) etaient
     *  offerts. Les colonnes bi-aspect (Spider-Woman) n'apparaissent que
     *  composees, dans les conseils. */
    async packagesAspect(hero) {
        let data;
        try {
            data = await api.aspectDecks();
        } catch (e) { return []; }
        const packages = (data && data.packages) || {};
        const reco = (data && data.recommandations) || {};

        // La matrice nomme les heros comme le tableur (« Spider-Man (Peter
        // Parker) ») : on retrouve l'entree par le nom du heros ou de l'alter-ego.
        const identites = [hero.name, ...(hero.deck.hero[0] || "").split(",")
            .map((id) => { const c = cards.get(id); return c ? cleanName(c.name) : ""; })]
            .filter(Boolean).map((x) => x.toLowerCase());
        let conseille = null;
        for (const [cle, valeurs] of Object.entries(reco)) {
            const bas = cle.toLowerCase();
            if (identites.some((n) => n && bas.includes(n))) { conseille = valeurs; break; }
        }

        // Un nom de package peut designer DEUX packages a fusionner : c'est le
        // cas de Spider-Woman, qui joue deux aspects a la fois.
        const resoudrePackage = (nom) => {
            if (packages[nom]) return [nom];
            const m = nom.match(/^(.*?)\s+(\w+)\/(\w+)$/);
            if (m) {
                const [, prefixe, a, b] = m;
                const p1 = `${prefixe} ${a}`, p2 = `${prefixe} ${b}`;
                if (packages[p1] && packages[p2]) return [p1, p2];
            }
            return [];
        };

        const choisis = [];
        const vus = new Set();
        for (const nom of Object.values(conseille || {})) {
            const parties = resoudrePackage(nom);
            if (!parties.length || vus.has(nom)) continue;
            vus.add(nom);
            choisis.push({ libelle: nom, parties, conseille: true });
        }
        const restants = [...GENERIQUES_D_ABORD.filter((n) => packages[n]), ...Object.keys(packages)];
        for (const nom of restants) {
            if (vus.has(nom) || (packages[nom] || []).length < PAQUET_COMPLET_MIN) continue;
            vus.add(nom);
            choisis.push({ libelle: nom, parties: [nom], conseille: false });
        }

        return choisis.map(({ libelle, parties, conseille }) => {
            const cartes = parties.flatMap((p) => packages[p] || []);
            // Un package assemblé à partir de PLUSIEURS colonnes vient des
            // colonnes bi-aspect, qui ne listent que l'aspect : 11 + 11 = 22, là
            // où un générique compte 30 cartes dont 6 Basic. Le deck tombait donc
            // à 37 (15 signature + 22), sous le minimum de 40. En rendant son
            // socle de ressources, la partie joueur revient à 25 cartes —
            // exactement la taille du player_deck de tous les decks de base.
            if (parties.length > 1) cartes.push(...SOCLE_BASIC);
            const deck = { ...hero.deck, name: libelle, player_deck: cartes };
            return {
                id: "aspect:" + libelle, name: libelle, source: "aspect", deck,
                aspects: aspectsOfDeck(deck), recommande: conseille,
            };
        });
    },

    /** Index `set_name` -> createur, bati une fois. Un nom de set porte par
     *  DEUX auteurs (ou par une carte officielle et une fan-made) n'y entre
     *  pas : mieux vaut ne rien attribuer que de se tromper de personne.
     *  « Electro » est exactement ce cas, entre l'officiel et Web of Deceit. */
    _auteurParSet() {
        if (_auteurParSet) return _auteurParSet;
        const parSet = new Map();
        for (const c of cards.all()) {
            const set = c && c.set_name;
            if (!set) continue;
            if (!parSet.has(set)) parSet.set(set, []);
            parSet.get(set).push(c.custom);
        }
        _auteurParSet = new Map();
        for (const [set, customs] of parSet) {
            const a = auteurUnique(customs);
            if (a) _auteurParSet.set(set, a);
        }
        return _auteurParSet;
    },

    _buildScenario(id, raw, extKey, hasExpert) {
        const villains = raw.villain || [];
        const schemes = raw.schemes || [];
        const setAside = raw.set_aside || [];
        const mod = raw.modular_sets || [];
        // Cartes de vilain(s) à afficher :
        //  - villain[] rempli  -> étapes d'UN vilain : on montre la 1re carte.
        //  - villain[] vide    -> scénario multi-vilains : on récupère les cartes de
        //                          type "Villain" dans set_aside (dédupliquées par nom).
        let villainCards;
        if (villains.length) {
            villainCards = [villains[0].split(",")[0]];
        } else {
            const seen = new Set(); villainCards = [];
            for (const c of setAside) {
                const card = cards.get(c);
                if (card && String(card.type).includes("Villain")) {
                    const nm = cleanName(card.name);
                    if (nm && !seen.has(nm)) { seen.add(nm); villainCards.push(String(c).split(",")[0]); }
                }
            }
        }
        const villainNames = villainCards.map((c) => { const card = cards.get(c); return cleanName(card ? card.name : c); });
        // Scénario-défi : on affiche le NOM DU DÉFI (carte challenge) plutôt que
        // celui du scénario de base, plus parlant dans la grille et le récap.
        const challenges = raw.challenges || [];
        let name = cleanName(raw.name) || titleize(id);
        if (challenges.length) {
            const cdefi = cards.get(challenges[0]);
            if (cdefi && cdefi.name) name = cleanName(cdefi.name);
        }
        // Createur, lu sur une carte du scenario lui-meme : le nom de set ne
        // suffirait pas (« Electro » existe en officiel ET chez Ripper3).
        const auteurDe = (cid) => { const c = cards.get(cid); return (c && c.custom) || ""; };
        const auteur = auteurDe(villainCards[0]) || auteurDe(schemes[0]) || auteurDe(setAside[0]);
        return {
            id, name, challenges, version: raw.version, extension: extKey,
            auteur, homebrew: isHomebrew(extKey),
            expert: !!raw.expert, hasExpertVariant: hasExpert,
            villains, schemes, setAside,
            villainCards,
            encounterDeckBase: raw.encounters || [],
            mandatoryEncounterSets: raw.encounter_sets || [],
            recommendedModularSets: mod,
            modularSlots: { min: mod.length, max: Math.max(4, mod.length) },
            tileImage: (villainCards[0] || schemes[0] || "").split(",")[0],
            villainNames,
            rawJson: raw,
        };
    },

    async scenariosForExtension(extKey, options = {}) {
        // `options.campagne` : l'ecran de campagne veut TOUS les scenarios de la boite (les variantes de campagne comprises) ; la partie libre ne les voit pas.
        const cacheComplet = await this._scenariosComplets(extKey);
        const ext = (await this.extensions()).find((e) => e.key === extKey);
        return sansVariantesDeCampagne(cacheComplet, ext, options);
    },

    async _scenariosComplets(extKey) {
        if (_scenariosByExt.has(extKey)) return _scenariosByExt.get(extKey);
        await cards.load();
        const exts = await this.extensions();
        const ext = exts.find((e) => e.key === extKey);
        const avail = new Set((await api.listScenarios()).map(fileName));
        const out = [];
        if (ext) {
            for (const name of ext.scenarios) {
                if (!avail.has(name)) continue;
                try {
                    const raw = await api.scenario(name);
                    out.push(this._buildScenario(name, raw, extKey, avail.has(name + "_expert")));
                } catch (e) {}
            }
        }
        _scenariosByExt.set(extKey, out);
        return out;
    },

    /** Tous les scénarios de toutes les extensions, onglet « Défis » compris
     *  (la roue de « Partie au hasard » fait elle-même le tri, roue.js). */
    async tousLesScenarios() {
        const exts = await this.extensions();
        const parExt = await Promise.all(exts.map((e) =>
            this.scenariosForExtension(e.key).catch(() => [])));
        return parExt.flat();
    },

    /** Variante Expert d'un scénario (fichier *_expert). */
    async expertVariant(scenarioId) {
        try {
            const raw = await api.scenario(scenarioId + "_expert");
            return this._buildScenario(scenarioId + "_expert", raw, "", false);
        } catch (e) { return null; }
    },

    async encounterSets() {
        if (_encounterSets) return _encounterSets;
        // extensions() d'abord : c'est elle qui remplit `_setsRencontreMasques`.
        // Le fichier du set reste dans data/encounter_sets et le moteur sait
        // toujours le monter (autoplay --modulaires s'en sert) ; on le retire
        // seulement des listes que voit un joueur, chips « Personnalises » et
        // tirage « Aleatoire » compris.
        await this.extensions();
        const names = (await api.listEncounterSets()).map(fileName);
        const auteurs = this._auteurParSet();
        _encounterSets = names.filter((n) => !_setsRencontreMasques.has(n))
            .map((n) => {
                const displayName = nomSetRencontre(n);
                return {
                    name: n, displayName, kind: encounterKind(n),
                    auteur: auteurs.get(displayName) || "",
                };
            });
        return _encounterSets;
    },

    /** Createur d'un set de rencontre fan-made, depuis son nom de fichier.
     *  Vide pour un set officiel, ou quand deux auteurs portent le meme nom
     *  de set. Appeler encounterSets() ou extensions() d'abord. */
    auteurSetRencontre(name) {
        return this._auteurParSet().get(nomSetRencontre(name)) || "";
    },

    /** Image d'un set de rencontre (1re carte) — chargée à la demande. */
    async encounterSetImage(name) {
        try { const j = await api.encounterSet(name); return (j.encounters && j.encounters[0]) ? j.encounters[0].split(",")[0] : ""; }
        catch (e) { return ""; }
    },
};

// `vagueDeLExtension` est exportee depuis le 13/09/2026 pour le mode Legacy,
// qui range les extensions par vague. Elle lit BORNES_VAGUES, la SEULE table
// qui dise a quelle vague appartient une boite : la recopier ailleurs aurait
// cree une seconde verite, et la boite du Bouffon Vert (n°2, vague 1) est
// justement le contre-exemple qu'aucune approximation ne retrouve.
export { titleize, nomSetRencontre, titreDeVague, vagueDeLExtension };
