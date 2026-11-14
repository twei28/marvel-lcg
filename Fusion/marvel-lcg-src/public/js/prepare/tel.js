// tel.js : les briques du mode téléphone de l'assistant de préparation
// (refonte du 09/10/2026, fiche .planning/todos/2026-10-09-mode-telephone-refonte.md).
//
// Pures du point de vue de l'assistant : rien ici ne connaît les héros, les
// decks ni les méchants. app.js les appelle ; au-dessus de 768 px, aucune de
// ces fonctions ne fait quoi que ce soit (le PC reste identique).

const REQUETE = window.matchMedia("(max-width: 767px)");

/** Téléphone portrait (sous 768 px). La V2 expérimentale (`ui_version=v2`)
 *  n'a pas de mise en page téléphone à elle : l'exclure laissait le compte
 *  d'essai sur la mise en page PC, débordante (retour de l'utilisateur, 24/10/2026). */
export function estTel() {
    return REQUETE.matches;
}

function majClasse() {
    document.documentElement.classList.toggle("tel", estTel());
}

/** Pose `html.tel` tout de suite et à chaque franchissement de 768 px
 *  (rotation, redimensionnement) ; `rappel` redessine l'écran. */
export function suivreTel(rappel) {
    majClasse();
    REQUETE.addEventListener("change", () => { majClasse(); rappel(); });
}
majClasse();

/* ---- Retour Android = étape précédente ------------------------------------
   Chaque écran (accueil, étapes 0 à 3) est une entrée d'historique. Un recul
   par l'interface (« Retour », étape cliquée en arrière) rejoue le recul du
   système quand l'entrée précédente EST la cible : la pile reste propre. */
let cleCourante = null;

export function installerHistorique(appliquer) {
    window.addEventListener("popstate", (e) => {
        const s = e.state;
        if (!estTel() || !s || !s.tel) return;
        cleCourante = s.cle;
        appliquer(s.cle);
    });
}

/** À appeler après chaque rendu avec la clé de l'écran affiché. */
export function noterEcran(cle) {
    if (!estTel() || cle === cleCourante) return;
    const prec = cleCourante;
    cleCourante = cle;
    try {
        if (prec === null) history.replaceState({ tel: 1, cle, prec: null }, "");
        else history.pushState({ tel: 1, cle, prec }, "");
    } catch (e) { /* historique indisponible : le jeu marche sans */ }
}

/** Recule d'un cran si l'entrée précédente est `cle`. Rend true si c'est fait
 *  (le rendu viendra du popstate), false sinon (l'appelant rend lui-même). */
export function reculerVers(cle) {
    const s = history.state;
    if (estTel() && s && s.tel && s.prec === cle) { history.back(); return true; }
    return false;
}

/* ---- Bandeau qui rétrécit au défilement -----------------------------------
   Le bandeau est posé en absolu au-dessus d'un conteneur défilant dont le
   padding-top vaut sa hauteur pleine : sa hauteur suit le défilement sans
   jamais redimensionner le conteneur (pas de scintillement). */
const BANDEAU_MINI = 52;

export function brancherBandeau() {
    const equipe = document.querySelector(".tel-assistant .team-b");
    const defil = equipe && equipe.querySelector(".tb-droite");
    if (!defil) return;
    const plein = Math.round(Math.min(240, Math.max(150, window.innerHeight * 0.25)));
    equipe.style.setProperty("--bandeau-plein", plein + "px");
    const maj = () => {
        const h = Math.max(BANDEAU_MINI, plein - defil.scrollTop);
        equipe.style.setProperty("--bandeau-h", h + "px");
        equipe.classList.toggle("compact", h <= 70);
    };
    let attente = false;
    defil.addEventListener("scroll", () => {
        if (attente) return;
        attente = true;
        requestAnimationFrame(() => { attente = false; maj(); });
    }, { passive: true });
    maj();
}

/* ---- Feuille basse fermable en glissant ------------------------------------ */
const SEUIL_FERMETURE = 90;

/** Pose la poignée (zone de 44 px) en tête du panneau d'une feuille basse. */
export function ajouterPoignee(panneau, fermer) {
    if (!estTel() || panneau.querySelector(":scope > .tel-poignee")) return;
    const poignee = document.createElement("div");
    poignee.className = "tel-poignee";
    poignee.setAttribute("role", "button");
    poignee.setAttribute("aria-label", "Fermer");
    poignee.append(document.createElement("span"));
    panneau.prepend(poignee);
    let depart = null;
    poignee.addEventListener("pointerdown", (e) => {
        depart = e.clientY;
        try { poignee.setPointerCapture(e.pointerId); } catch (err) { /* capture facultative */ }
        panneau.style.transition = "none";
    });
    poignee.addEventListener("pointermove", (e) => {
        if (depart === null) return;
        panneau.style.transform = "translateY(" + Math.max(0, e.clientY - depart) + "px)";
    });
    const fin = (e) => {
        if (depart === null) return;
        const dy = e.clientY - depart;
        depart = null;
        panneau.style.transition = "";
        if (dy > SEUIL_FERMETURE || Math.abs(dy) < 5) fermer();
        else panneau.style.transform = "";
    };
    poignee.addEventListener("pointerup", fin);
    poignee.addEventListener("pointercancel", () => {
        depart = null;
        panneau.style.transition = "";
        panneau.style.transform = "";
    });
}
