// Deck builder — construction de decks SANS passer par marvelcdb.
//
// Reutilise les modules de l'ecran de preparation (api/cards/catalog) : memes
// donnees (cards.json via CardStatistics), memes images (/<card_id>), meme
// format de deck que deck/starter/*.json.
//
// Sauvegarde :
//   - brouillons -> localStorage (mc-deckbuilder-drafts) ;
//   - deck fini  -> POST /save_deck (fichier dans deck/custom/, alors liste par
//     /list_deck et donc propose automatiquement dans le wizard).
//
// Validation STRICTE (RR) avant « Save to game » :
//   - 40 a 50 cartes au total (cartes signature du heros incluses) ;
//   - un seul aspect (Spider-Woman : exactement deux ; Adam Warlock : libre) ;
//   - copies par TITRE <= MaxPerDeck (3 par defaut).
"use strict";
import { api, cardImageUrl, fileName } from "/public/js/prepare/api.js";
import { cards } from "/public/js/prepare/cards.js";
import { catalog } from "/public/js/prepare/catalog.js";
import { t, synchroniserLangueServeur } from "/public/js/prepare/langue.js";
import { nomFr, texteFr } from "/public/js/prepare/cartes-fr.js";

// « 'Pool » : l'apostrophe fait partie du nom d'aspect dans les donnees (Deadpool).
const ASPECTS = ["Aggression", "Justice", "Leadership", "Protection", "'Pool", "Determination"];
// Classes non-aspect jouables : Basic, et les cartes de recompense de Campagne.
const CLASSES_NEUTRES = ["Basic", "Campaign"];
const TYPES_JOUEUR = ["Ally", "Event", "Support", "Upgrade", "Resource", "PlayerSideScheme", "Player_Side_Scheme"];
// Libellés FR affichés pour les types de cartes (les identifiants restent en anglais).
const LIBELLES_TYPES = {
    Ally: "Allié", Event: "Événement", Support: "Soutien", Upgrade: "Amélioration",
    Resource: "Ressource", PlayerSideScheme: "Manigance de joueur", Player_Side_Scheme: "Manigance de joueur",
};
function libelleType(type) { return t(LIBELLES_TYPES[type] || type); }

/** Nom de classe CSS sur (« 'Pool » -> pool). */
function classeCss(aspect) { return String(aspect).replace(/[^a-z]/gi, "").toLowerCase(); }
/** Libelle affiche (« 'Pool » -> Pool). */
function labelAspect(aspect) { return String(aspect).replace(/^'/, ""); }
const CLE_BROUILLONS = "mc-deckbuilder-drafts";

const etat = {
    heroes: [],
    hero: null,
    nomDeck: "",
    // cardId -> nombre de copies choisies (player_deck uniquement).
    choisies: new Map(),
    filtres: { texte: "", aspects: new Set(), types: new Set(), couts: new Set() },
    brouillonId: null,
};

/* ---------------- Donnees ---------------- */

/* Stan Lee — « Marvelous » : son deck doit contenir 15 cartes signature
   empruntees a d'autres heros. Il est donc le seul heros pour qui les cartes de
   classe « Hero » sont selectionnables ici. */
const SIGNATURE_MARVELOUS = 15;
function estStanLee(hero) { return /stan\s*lee/i.test((hero && hero.name) || ""); }
function estSignature(c) { return !!c && c.class === "Hero"; }

function estTypeJouable(c) {
    return TYPES_JOUEUR.includes(String(c.type).replace(/ /g, ""))
        || TYPES_JOUEUR.includes(String(c.type));
}

function estCarteJoueur(c) {
    if (!c || !c.class) return false;
    if (c.class === "Hero") return false;
    if (!ASPECTS.includes(c.class) && !CLASSES_NEUTRES.includes(c.class)) return false;
    return estTypeJouable(c);
}

/** Carte signature d'un autre heros, empruntable par Stan Lee. */
function estCarteSignature(c) {
    if (!estSignature(c) || !estTypeJouable(c)) return false;
    // Une vraie carte signature appartient au set d'un heros : cela ecarte les
    // cartes sans set (dont la carte d'exemple de cards_custom.json).
    return !!c.set_name && c.set_name !== "Stan Lee";
}

const _pools = new Map(); // avecSignature -> liste
async function poolJoueur(avecSignature = false) {
    if (_pools.has(avecSignature)) return _pools.get(avecSignature);
    const cs = await cards.load();
    const vus = new Map(); // titre+class+type -> premiere carte (dedoublonne les reimpressions)
    for (const id of Object.keys(cs.const_card_dict)) {
        const c = cs.const_card_dict[id];
        const garde = estCarteJoueur(c) || (avecSignature && estCarteSignature(c));
        if (!garde) continue;
        const cle = `${c.name}|${c.class}|${c.type}`;
        if (!vus.has(cle)) vus.set(cle, { id: String(c.id ?? id).split(",")[0] || id, carte: c });
    }
    // Les cartes signature en tete : c'est la contrainte a satisfaire en premier.
    const rang = (c) => (estSignature(c) ? -1 : ASPECTS.indexOf(c.class));
    const pool = [...vus.values()].sort((a, b) =>
        (rang(a.carte) - rang(b.carte)) || a.carte.name.localeCompare(b.carte.name));
    _pools.set(avecSignature, pool);
    return pool;
}

/** Heros dont proviennent les cartes signature choisies, par nombre de copies. */
function herosEmpruntes() {
    const parHero = new Map();
    for (const [id, n] of etat.choisies) {
        if (!estSignature(cards.get(id))) continue;
        for (const h of etat.heroes) {
            if ((h.deck.hero_deck || []).includes(id)) {
                parHero.set(h, (parHero.get(h) || 0) + n);
                break;
            }
        }
    }
    return [...parHero.entries()].sort((a, b) => b[1] - a[1]).map(([h]) => h);
}

function maxParDeck(carte) {
    const brut = carte && carte.desc ? carte.desc.MaxPerDeck : undefined;
    const n = Number(brut);
    return Number.isFinite(n) && n > 0 ? n : 3;
}

/* ---------------- Validation ---------------- */

function reglesAspect(hero) {
    const nom = (hero && hero.name) || "";
    if (/spider-?woman/i.test(nom)) return { min: 2, max: 2, label: t("exactement 2 aspects (Spider-Woman)") };
    if (/cloak/i.test(nom) && /dagger/i.test(nom)) return { min: 2, max: 2, label: t("exactement 2 aspects (Cloak & Dagger)") };
    if (/adam warlock/i.test(nom)) return { min: 0, max: 99, label: t("des aspects libres (Adam Warlock)") };
    if (/moon knight/i.test(nom)) return { min: 0, max: 99, label: t("tous les aspects, coût max 2 (Moon Knight)") };
    return { min: 0, max: 1, label: t("un seul aspect") };
}

/**
 * Cartes qui échappent à la limite d'aspect du héros.
 * Arachnophilia (Cassandra Webb) : « You may include allies with the
 * WEB-WARRIOR trait or with "Spider" in their title from any aspect in your
 * deck. » Ces alliés ne comptent donc pas dans le décompte des aspects.
 */
function exemptDeLaLimiteAspect(hero, carte) {
    if (!/madame web/i.test((hero && hero.name) || "")) return false;
    if (carte.type !== "Ally") return false;
    return (carte.traits || []).includes("WEB-WARRIOR") || /spider/i.test(carte.name);
}

function valider() {
    const problemes = [];
    if (!etat.hero) return { ok: false, problemes: [t("Choisis un héros")], total: 0 };
    const marvelous = estStanLee(etat.hero);
    // Stan Lee n'a pas de cartes signature a lui : les 15 sont a choisir ici.
    const signature = marvelous ? 0 : (etat.hero.deck.hero_deck || []).length;
    let total = signature;
    let empruntees = 0;
    const parTitre = new Map();
    const aspects = new Set();
    for (const [id, n] of etat.choisies) {
        const c = cards.get(id);
        if (!c) continue;
        total += n;
        parTitre.set(c.name, { n: (parTitre.get(c.name)?.n || 0) + n, max: maxParDeck(c) });
        if (estSignature(c)) empruntees += n;
        else if (c.class && !CLASSES_NEUTRES.includes(c.class)
                 && !exemptDeLaLimiteAspect(etat.hero, c)) aspects.add(c.class);
    }
    if (marvelous && empruntees !== SIGNATURE_MARVELOUS) {
        problemes.push(`${t("Marvelous : exactement")} ${SIGNATURE_MARVELOUS} ${t("cartes signature d’autres héros — actuellement")} ${empruntees}`);
    }
    if (total < 40) problemes.push(`${t("Deck trop petit :")} ${total}/40 ${t("minimum (cartes signature incluses)")}`);
    if (total > 50) problemes.push(`${t("Deck trop grand :")} ${total}/50 maximum`);
    const regle = reglesAspect(etat.hero);
    if (aspects.size < regle.min) problemes.push(`${t("Ce héros requiert")} ${regle.label} — ${t("actuellement")} ${aspects.size}`);
    if (aspects.size > regle.max) problemes.push(`${t("Trop d’aspects")} (${[...aspects].join(", ")}) — ${t("autorisé :")} ${regle.label}`);
    for (const [titre, x] of parTitre) {
        if (x.n > x.max) problemes.push(`${t("Trop d’exemplaires de")} « ${titre} » : ${x.n}/${x.max}`);
    }
    if (!etat.nomDeck.trim()) problemes.push(t("Donne un nom au deck"));
    return { ok: problemes.length === 0, problemes, total, aspects: [...aspects], signature, empruntees };
}

/* ---------------- Deck JSON ---------------- */

function deckJson() {
    const base = etat.hero.deck;
    const marvelous = estStanLee(etat.hero);
    const player_deck = [];
    const empruntees = [];
    for (const [id, n] of etat.choisies) {
        const cible = marvelous && estSignature(cards.get(id)) ? empruntees : player_deck;
        for (let i = 0; i < n; i++) cible.push(id);
    }
    // Marvelous : l'obligation et le nemesis viennent d'un des heros empruntes
    // (« au hasard » sur la carte ; on prend celui le plus represente).
    const source = marvelous ? herosEmpruntes()[0] : null;
    return {
        version: base.version || "0.5.8",
        name: etat.nomDeck.trim() || etat.hero.name,
        metadata: { url: "" },
        hero: base.hero,
        hero_deck: marvelous ? empruntees : (base.hero_deck || []),
        set_aside: base.set_aside || [],
        obligations: (source ? source.deck.obligations : base.obligations) || [],
        nemesis_set: (source ? source.deck.nemesis_set : base.nemesis_set) || [],
        player_deck,
    };
}

function chargerDepuisDeck(d, nom) {
    etat.choisies.clear();
    // Pour Stan Lee, les cartes signature de hero_deck sont des choix du joueur
    // (Marvelous) : elles doivent revenir dans la selection, pas rester figees.
    const sources = estStanLee(etat.hero)
        ? [...(d.hero_deck || []), ...(d.player_deck || [])]
        : (d.player_deck || []);
    for (const id of sources) {
        const cle = String(id).split(",")[0];
        etat.choisies.set(cle, (etat.choisies.get(cle) || 0) + 1);
    }
    etat.nomDeck = nom ?? (d.name || "");
}

/* ---------------- Brouillons (localStorage) ---------------- */

function lireBrouillons() {
    try { return JSON.parse(window.localStorage.getItem(CLE_BROUILLONS) || "{}"); }
    catch { return {}; }
}
function ecrireBrouillons(b) {
    try { window.localStorage.setItem(CLE_BROUILLONS, JSON.stringify(b)); } catch {}
}
function sauverBrouillon() {
    if (!etat.hero) return;
    const b = lireBrouillons();
    const id = etat.brouillonId || `d${Date.now()}`;
    etat.brouillonId = id;
    b[id] = { heroId: etat.hero.id, deck: deckJson(), updated: Date.now() };
    ecrireBrouillons(b);
    statut(`${t("Brouillon sauvegardé")} (${new Date().toLocaleTimeString()})`);
    rendreListesBrouillons();
}

/* ---------------- Rendu ---------------- */

const $ = (sel) => document.querySelector(sel);
/** replaceChildren stringifie les tableaux : on aplatit et on filtre nous-memes. */
function remplacer(zone, ...enfants) {
    zone.replaceChildren(...enfants.flat(9).filter((e) => e != null));
}
function el(tag, attrs = {}, ...enfants) {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
        if (k === "class") n.className = v;
        else if (k.startsWith("on")) n[k] = v;
        else if (v !== undefined && v !== null) n.setAttribute(k, v);
    }
    for (const e of enfants.flat()) if (e != null) n.append(e.nodeType ? e : document.createTextNode(e));
    return n;
}

function statut(texte, erreur = false) {
    const zone = $("#db-status");
    zone.textContent = texte;
    zone.classList.toggle("est-erreur", erreur);
}

function rendreFiltres() {
    const zone = $("#db-filtres");
    remplacer(zone, 
        el("input", {
            class: "db-recherche", type: "search", placeholder: t("Rechercher un nom ou un texte de carte…"),
            value: etat.filtres.texte,
            oninput: (e) => { etat.filtres.texte = e.target.value; rendreGrille(); },
        }),
        el("div", { class: "db-chips" },
            // « Hero » n'apparait que pour Stan Lee : c'est le seul a pouvoir
            // emprunter les cartes signature des autres heros.
            [...(estStanLee(etat.hero) ? ["Hero"] : []), ...ASPECTS, ...CLASSES_NEUTRES].map((a) => el("button", {
                class: `db-chip aspect-${classeCss(a)}${etat.filtres.aspects.has(a) ? " est-actif" : ""}`,
                onclick: () => { basculer(etat.filtres.aspects, a); rendreFiltres(); rendreGrille(); },
            }, a === "Hero" ? "Signature" : labelAspect(a)))),
        el("div", { class: "db-chips" },
            ["Ally", "Event", "Support", "Upgrade", "Resource"].map((t) => el("button", {
                class: `db-chip${etat.filtres.types.has(t) ? " est-actif" : ""}`,
                onclick: () => { basculer(etat.filtres.types, t); rendreFiltres(); rendreGrille(); },
            }, libelleType(t)))),
        el("div", { class: "db-chips" },
            ["0", "1", "2", "3", "4+"].map((c) => el("button", {
                class: `db-chip${etat.filtres.couts.has(c) ? " est-actif" : ""}`,
                onclick: () => { basculer(etat.filtres.couts, c); rendreFiltres(); rendreGrille(); },
            }, `${t("Coût")} ${c}`))),
    );
}
function basculer(set, valeur) { set.has(valeur) ? set.delete(valeur) : set.add(valeur); }

function passeFiltres(carte) {
    const f = etat.filtres;
    if (f.aspects.size && !f.aspects.has(carte.class)) return false;
    if (f.types.size && !f.types.has(carte.type)) return false;
    if (f.couts.size) {
        const cout = Number(carte.cost);
        const cle = Number.isFinite(cout) ? (cout >= 4 ? "4+" : String(cout)) : "";
        if (!f.couts.has(cle)) return false;
    }
    if (f.texte) {
        const t = f.texte.toLowerCase();
        // On cherche dans ce que le joueur LIT : le francais quand il existe.
        const dedans = `${nomFr(carte)} ${texteFr(carte) || ""} ${(carte.traits || []).join(" ")}`.toLowerCase();
        if (!dedans.includes(t)) return false;
    }
    return true;
}

/**
 * Pastille « CUSTOM » des cartes fan-made. Le champ `custom` de cards.json
 * porte le nom de l'auteur : sans lui, une carte d'aspect custom est
 * indiscernable d'une officielle dans la grille du deck-builder.
 */
function badgeCustom(carte) {
    if (!carte || !carte.custom) return null;
    return el("span", {
        class: "db-badge-custom",
        title: `${t("Carte fan-made")} — ${carte.custom}`,
    }, t("CUSTOM"));
}

async function rendreGrille() {
    const pool = await poolJoueur(estStanLee(etat.hero));
    const zone = $("#db-grille");
    const visibles = pool.filter((x) => passeFiltres(x.carte)).slice(0, 400);
    remplacer(zone, 
        ...visibles.map(({ id, carte }) => {
            const n = etat.choisies.get(id) || 0;
            // `data-carte` porte l'identifiant jusqu'au DOM : l'apercu du
            // panneau de droite ecoute la grille entiere plutot que de poser
            // un gestionnaire sur chacune des 400 vignettes.
            return el("div", { class: `db-carte${n ? " est-choisie" : ""}`, "data-carte": id },
                el("img", { src: cardImageUrl(id), loading: "lazy", alt: nomFr(carte), onclick: () => ajouter(id) }),
                badgeCustom(carte),
                el("div", { class: "db-carte-pied" },
                    el("span", { class: `db-aspect-point aspect-${classeCss(carte.class)}` }),
                    el("b", {}, nomFr(carte)),
                    n ? el("span", { class: "db-count" }, `x${n}`) : null,
                ),
                el("div", { class: "db-carte-boutons" },
                    el("button", { onclick: () => retirer(id), disabled: n === 0 ? "" : undefined }, "−"),
                    el("button", { onclick: () => ajouter(id) }, "+"),
                ),
            );
        }),
    );
    $("#db-grille-info").textContent = `${visibles.length} ${t("carte(s)")}`;
}

function ajouter(id) {
    const c = cards.get(id);
    if (!c) return;
    const n = etat.choisies.get(id) || 0;
    if (n >= maxParDeck(c)) { statut(`Maximum ${maxParDeck(c)} ${t("exemplaires de")} « ${c.name} »`, true); return; }
    etat.choisies.set(id, n + 1);
    rendreTout();
}
function retirer(id) {
    const n = etat.choisies.get(id) || 0;
    if (n <= 1) etat.choisies.delete(id); else etat.choisies.set(id, n - 1);
    rendreTout();
}


/* ---------------- Statistiques du deck (courbe de couts, ressources) ------ */

function rendreStatsDeck(lignes) {
    // lignes = [{ id, n, carte }] du deck courant (signature comprise).
    if (lignes.length === 0) return null;

    const parCout = new Map();          // 0..3, "4+"
    const ressources = { R: 0, B: 0, Y: 0, G: 0 };
    const parType = new Map();
    for (const { n, carte } of lignes) {
        const cout = Number(carte.cost);
        if (Number.isFinite(cout)) {
            const cle = cout >= 4 ? "4+" : String(cout);
            parCout.set(cle, (parCout.get(cle) || 0) + n);
        }
        const res = (carte.desc && carte.desc.RES) || "";
        for (const lettre of String(res).toUpperCase()) {
            if (lettre in ressources) ressources[lettre] += n;
        }
        parType.set(carte.type, (parType.get(carte.type) || 0) + n);
    }

    const maxCout = Math.max(1, ...parCout.values());
    const barres = ["0", "1", "2", "3", "4+"].map((cle) => {
        const total = parCout.get(cle) || 0;
        return el("div", { class: "db-stat-barre" },
            el("div", { class: "db-stat-remplissage", style: `height:${Math.round((100 * total) / maxCout)}%` }),
            el("b", {}, String(total)),
            el("span", {}, cle));
    });

    const NOMS_RES = { R: ["physique", "#e74c3c"], B: ["mentale", "#3498db"], Y: ["énergie", "#f1c40f"], G: ["libre", "#2ecc71"] };
    const pastilles = Object.entries(ressources)
        .filter(([, total]) => total > 0)
        .map(([lettre, total]) => el("span", { class: "db-stat-res", style: `--res:${NOMS_RES[lettre][1]}` },
            `${total} ${t(NOMS_RES[lettre][0])}`));

    const types = [...parType.entries()].sort((a, b) => b[1] - a[1])
        .map(([type, total]) => el("span", { class: "db-stat-type" }, `${total} ${libelleType(type)}`));

    return el("div", { class: "db-stats" },
        el("div", { class: "db-stats-courbe" },
            el("span", { class: "db-stats-titre" }, t("Coût")),
            el("div", { class: "db-stat-barres" }, barres)),
        pastilles.length ? el("div", { class: "db-stats-ressources" },
            el("span", { class: "db-stats-titre" }, t("Ressources")), pastilles) : null,
        el("div", { class: "db-stats-types" },
            el("span", { class: "db-stats-titre" }, "Types"), types),
    );
}

function rendreDeck() {
    const zone = $("#db-deck");
    if (!etat.hero) { remplacer(zone, el("p", { class: "db-vide" }, t("Choisis d’abord un héros."))); return; }
    const v = valider();
    const signature = v.signature;
    const lignes = [...etat.choisies.entries()]
        .map(([id, n]) => ({ id, n, carte: cards.get(id) }))
        .filter((x) => x.carte)
        .sort((a, b) => (a.carte.class || "").localeCompare(b.carte.class || "") || a.carte.name.localeCompare(b.carte.name));
    remplacer(zone, 
        el("div", { class: "db-deck-tete" },
            el("b", {}, `${v.total} / 40–50 ${t("cartes")}`),
            el("span", {}, `${signature} signature + ${v.total - signature} ${t("choisies")}`),
            v.aspects && v.aspects.length ? el("span", { class: "db-aspects" }, v.aspects.map(labelAspect).join(" + ")) : null,
        ),
        el("div", { class: "db-deck-lignes" },
            lignes.map(({ id, n, carte }) => el("div", { class: "db-ligne", "data-carte": id, onclick: () => retirer(id) },
                el("span", { class: `db-aspect-point aspect-${classeCss(carte.class)}` }),
                el("span", { class: "db-ligne-nom" }, carte.name),
                badgeCustom(carte),
                el("span", { class: "db-ligne-type" }, libelleType(carte.type)),
                el("b", {}, `x${n}`),
            ))),
        rendreStatsDeck(lignes),
        el("div", { class: `db-validation${v.ok ? " est-ok" : ""}` },
            v.ok ? el("span", {}, t("✔ Deck légal — prêt à sauvegarder"))
                 : v.problemes.map((p) => el("span", {}, `• ${p}`))),
    );
    $("#db-save-game").disabled = !v.ok;
}

function rendreTout() { rendreDeck(); rendreGrille(); }

// La palette de classes depend du heros (« Hero-specific » n'existe que pour
// Stan Lee) : a rappeler quand le heros change, mais PAS a chaque ajout de
// carte, sinon le champ de recherche perd le focus en pleine frappe.
function rendreToutEtFiltres() { rendreFiltres(); rendreTout(); }

/* ---------------- Sources (heros, clonage, brouillons) ---------------- */

async function rendreEnTete() {
    const selHero = $("#db-hero");
    remplacer(selHero, 
        el("option", { value: "" }, t("— Héros —")),
        etat.heroes.map((h) => el("option", { value: h.id, selected: etat.hero && etat.hero.id === h.id ? "" : undefined }, h.name)),
    );
    selHero.onchange = async () => {
        etat.hero = etat.heroes.find((h) => h.id === selHero.value) || null;
        etat.choisies.clear();
        etat.brouillonId = null;
        if (etat.hero && !etat.nomDeck) etat.nomDeck = `${etat.hero.name} custom`;
        $("#db-nom").value = etat.nomDeck;
        await rendreSources();
        rendreToutEtFiltres();
    };
    $("#db-nom").oninput = (e) => { etat.nomDeck = e.target.value; rendreDeck(); };
    $("#db-nom").value = etat.nomDeck;
}

async function rendreSources() {
    const zone = $("#db-sources");
    if (!etat.hero) { remplacer(zone, ); return; }
    const decks = await catalog.decksForHero(etat.hero);
    remplacer(zone, 
        el("span", { class: "db-sources-label" }, t("Partir de :")),
        el("button", { class: "db-chip", onclick: () => { etat.choisies.clear(); etat.brouillonId = null; rendreTout(); } }, t("Vide")),
        decks.map((d) => el("button", {
            class: "db-chip",
            onclick: () => { chargerDepuisDeck(d.deck, `${d.name} (${t("copie")})`); $("#db-nom").value = etat.nomDeck; etat.brouillonId = null; rendreTout(); },
        }, `${d.source === "base" ? t("Base : ") : ""}${d.name}`)),
    );
    rendreListesBrouillons();
}

function rendreListesBrouillons() {
    const zone = $("#db-brouillons");
    const b = lireBrouillons();
    const liste = Object.entries(b)
        .filter(([, x]) => !etat.hero || x.heroId === etat.hero.id)
        .sort((a, c) => c[1].updated - a[1].updated);
    remplacer(zone, 
        liste.length ? el("span", { class: "db-sources-label" }, t("Brouillons :")) : null,
        liste.map(([id, x]) => el("span", { class: "db-brouillon" },
            el("button", {
                class: "db-chip",
                onclick: () => {
                    const hero = etat.heroes.find((h) => h.id === x.heroId);
                    if (hero) { etat.hero = hero; $("#db-hero").value = hero.id; }
                    chargerDepuisDeck(x.deck);
                    etat.brouillonId = id;
                    $("#db-nom").value = etat.nomDeck;
                    rendreSources().then(rendreToutEtFiltres);
                },
            }, `${x.deck.name} (${new Date(x.updated).toLocaleDateString()})`),
            el("button", { class: "db-chip db-suppr", onclick: () => { delete b[id]; ecrireBrouillons(b); rendreListesBrouillons(); } }, "✕"),
        )),
    );
}

/* ---------------- Sauvegarde cote jeu ---------------- */

async function sauverDansLeJeu() {
    const v = valider();
    if (!v.ok) return;
    const deck = deckJson();
    statut(t("Sauvegarde…"));
    try {
        const r = await fetch("/save_deck", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ file_name: deck.name, deck }),
        });
        const rep = await r.json();
        if (!r.ok || rep.error) throw new Error(rep.error || `HTTP ${r.status}`);
        statut(t("Sauvegardé dans le jeu ✔ — il apparaît maintenant dans la préparation de partie (étape Decks)."));
    } catch (e) {
        statut(`${t("Échec de la sauvegarde :")} ${e.message}`, true);
    }
}

/* ---------------- Demarrage ---------------- */

/** Libellés statiques de deck-builder.html, traduits au chargement.
    t() est l'identité en français : la passe est alors sans effet. */
function traduirePageStatique() {
    document.title = t("Éditeur de deck") + " — Marvel Champions";
    const lien = document.querySelector(".db-tete a");
    if (lien) lien.textContent = t("← Préparation");
    const titre = document.querySelector(".db-titre");
    if (titre) titre.textContent = t("Éditeur de deck");
    const nom = $("#db-nom");
    if (nom) nom.placeholder = t("Nom du deck…");
    const brouillon = $("#db-save-draft");
    if (brouillon) { brouillon.textContent = t("Sauver le brouillon"); brouillon.title = t("Sauver un brouillon dans ce navigateur"); }
    const exporter = $("#db-export");
    if (exporter) { exporter.textContent = t("Exporter"); exporter.title = t("Télécharger le deck en fichier JSON"); }
    const sauver = $("#db-save-game");
    if (sauver) { sauver.textContent = t("Sauvegarder dans le jeu"); sauver.title = t("Sauvegarder dans le jeu (apparaît dans la préparation)"); }
}

/** Montre en grand, dans le panneau de droite, la carte que l'on pointe.
 *
 *  Un SEUL ecouteur, pose sur la page : la grille se refait a chaque ajout de
 *  carte, et des gestionnaires poses sur 400 vignettes seraient a reposer a
 *  chaque fois. La delegation survit aux rendus sans qu'on y pense.
 *
 *  Il ecoute aussi les lignes du deck : survoler « Vibranium Shield » dans la
 *  liste de droite montre la carte, ce qui evite de la rechercher dans la
 *  grille pour verifier ce qu'elle fait.
 *
 *  L'apercu NE SE VIDE PAS quand on s'eloigne : la derniere carte pointee
 *  reste. C'est ce qu'on veut en construisant un deck — on lit la carte, puis
 *  on va cliquer ailleurs sans qu'elle disparaisse en cours de route. */
function installerApercu() {
    const zone = $("#db-apercu");
    if (!zone) return;

    const vider = () => remplacer(zone, el("span", { class: "db-apercu-vide" },
        t("Survole une carte pour la voir en grand")));
    vider();

    let derniere = null;
    document.addEventListener("mouseover", (evenement) => {
        const cible = evenement.target.closest?.("[data-carte]");
        if (!cible) return;
        const id = cible.getAttribute("data-carte");
        if (!id || id === derniere) return;
        derniere = id;
        const carte = cards.get(id);
        remplacer(zone, el("img", { src: cardImageUrl(id), alt: carte ? carte.name : id }));
    });
}

async function demarrer() {
    synchroniserLangueServeur();
    traduirePageStatique();
    installerApercu();
    statut(t("Chargement des cartes…"));
    await cards.load();
    etat.heroes = await catalog.heroes();
    const params = new URLSearchParams(window.location.search);
    const heroParam = params.get("hero");
    if (heroParam) etat.hero = etat.heroes.find((h) => h.id === heroParam) || null;
    if (etat.hero) etat.nomDeck = `${etat.hero.name} custom`;
    await rendreEnTete();
    await rendreSources();
    rendreFiltres();
    rendreTout();
    statut("");
    $("#db-save-draft").onclick = sauverBrouillon;
    $("#db-save-game").onclick = sauverDansLeJeu;
    $("#db-export").onclick = () => {
        const deck = deckJson();
        const blob = new Blob([JSON.stringify(deck, null, 4)], { type: "application/json" });
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = `${deck.name.replace(/[^a-zA-Z0-9_-]+/g, "_")}.json`;
        a.click();
    };
}

demarrer().catch((e) => statut(`${t("Échec du chargement :")} ${e.message}`, true));
