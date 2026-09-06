export class HistoryLog {
    static close() {
        if (HistoryLog.isOpen()) {
            HistoryLog.toggle();
        }
    }
    static isOpen() {
        return !HistoryLog.history_div?.classList.contains('hide');
    }
    static toggle() {
        HistoryLog.history_div?.classList.toggle('hide');
    }
    static addText(id, text) {
        if (id == HistoryLog.last_id) {
            return;
        }
        if (text && HistoryLog.history_text_div) {
            text = text.replaceAll("\n", "");
            HistoryLog.last_id = id;
            text = `<p class='log-id'>${id}</p> <p>${text}</p>`;
            HistoryLog.history_text += text;
            HistoryLog.history_text_div.innerHTML = HistoryLog.history_text;
        }
    }
    static isEmpty() {
        return HistoryLog.history_text_div?.innerHTML == "";
    }
    static showMenu(e, object_id, card_id, card_name) {
        HistoryLog.click_object_id = object_id;
        HistoryLog.click_card_id = card_id;
        HistoryLog.click_card_name = card_name;
        HistoryLog.contextMenu.style.display = 'block';
        HistoryLog.contextMenu.style.left = `${e.pageX}px`;
        HistoryLog.contextMenu.style.top = `${e.pageY}px`;
        HistoryLog.contextMenu.querySelector('#view_in_mdb').innerHTML = card_id;
    }
    static gotoMDB(e) {
        HistoryLog.reportMenuOff();
        window.open(`https://marvelcdb.com/card/${HistoryLog.click_card_id}`);
    }
    static markCard(e) {
        HistoryLog.reportMenuOff();
    }
    static reportMenuOff(e = null) {
        HistoryLog.contextMenu.style.display = 'none';
    }
    ;
}
HistoryLog.history_div = document.getElementById("history");
HistoryLog.history_text_div = document.getElementById("history-text");
HistoryLog.last_id = -1;
HistoryLog.history_text = "";
HistoryLog.contextMenu = document.getElementById('contextMenu');
HistoryLog.click_object_id = 0;
HistoryLog.click_card_id = "";
HistoryLog.click_card_name = "";
(() => {
    HistoryLog.history_div?.addEventListener('click', (e) => {
        let target = e.target;
        if (target !== HistoryLog.contextMenu && !HistoryLog.contextMenu.contains(target)) {
            HistoryLog.reportMenuOff();
        }
    });
})();
window.HistoryLog = HistoryLog;
//# sourceMappingURL=history.js.map