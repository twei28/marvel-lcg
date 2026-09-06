import { Setting } from './settings.js';
import { UI } from './ui.js';
import { HoverCard } from './hover.js';
import { Button } from './buttons.js';
import { HistoryLog } from './history.js';
import { Replay } from './replay.js';
import { SelectStep } from './select.js';
import { Effect } from './effect.js';
export class WindowLoad {
    static onClick(event) {
        document.querySelectorAll('.deck.clicked').forEach(div => {
            div.classList.remove('clicked');
            if (UI.temp_sorted_deck_div) {
                UI.tempSortDeck(false);
                UI.temp_sorted_deck_div = null;
            }
        });
    }
    static onKeyUp(event) {
        if (!event.altKey) {
            UI.hold_alt = false;
            document.body.classList.remove('hold-alt');
        }
        if (!event.ctrlKey) {
            UI.hold_ctrl = false;
            UI.updateAnimeTime();
            document.querySelector("#skipping-icon").classList.add('hide');
            document.body.classList.remove('hold-ctrl');
        }
        if (!event.shiftKey) {
            UI.hold_shift = false;
        }
    }
    static onKeyDown(event) {
        if (event.altKey) {
            UI.hold_alt = true;
            document.body.classList.add('hold-alt');
        }
        if (event.ctrlKey) {
            document.body.classList.add('hold-ctrl');
        }
        if (event.shiftKey) {
            if (UI.hold_shift == false) {
                if (UI.temp_sorted_deck_div) {
                    UI.tempSortDeck(false);
                }
            }
            UI.hold_shift = true;
            UI.temp_sorted_deck_div = document.querySelector('.deck.clicked');
            UI.tempSortDeck(true);
        }
        if (event.key == "Pause") {
            Button.togglePause();
            event.preventDefault();
        }
        else if (event.ctrlKey) {
            if (event.key === 's') {
                event.preventDefault();
                Button.doSave(0);
            }
            else if (event.key.toLowerCase() === 'z' && event.shiftKey) {
                event.preventDefault();
                Button.doOldUndo();
            }
            else if (event.key === 'z') {
                event.preventDefault();
                Button.doUndo();
            }
            else if (event.key === 'y') {
                event.preventDefault();
                Replay.doReplay(true);
            }
            else if (event.key === 'q') {
                event.preventDefault();
                Replay.doReplay();
                Button.doToEnd();
            }
            else if (event.key === 'e') {
                event.preventDefault();
                Replay.doReplay();
            }
            else if (event.ctrlKey) {
                UI.hold_ctrl = true;
                UI.updateAnimeTime();
                HoverCard.hide();
                document.querySelector("#skipping-icon").classList.remove('hide');
            }
        }
        else {
            if (event.key === "F1") {
                UI.focusOnPlayer(0);
                event.preventDefault();
            }
            else if (event.key === "F2") {
                UI.focusOnPlayer(1);
                event.preventDefault();
            }
            else if (event.key === "F3") {
                UI.focusOnPlayer(2);
                event.preventDefault();
            }
            else if (event.key === "F4") {
                UI.focusOnPlayer(3);
                event.preventDefault();
            }
            else if (event.key === "Tab") {
                Button.doToggleHistory();
                event.preventDefault();
            }
            else if (event.key === "1") {
                let deck_div = document.querySelector(`.deck.player-${Setting.player_id}.player-deck`);
                deck_div.classList.toggle('clicked');
                event.preventDefault();
            }
            else if (event.key === "2") {
                let deck_div = document.querySelector(`.deck.player-${Setting.player_id}.player-discard-pile`);
                deck_div.classList.toggle('clicked');
                event.preventDefault();
            }
            else if (event.key === "3") {
                let deck_div = document.querySelector(`.deck.player-${Setting.player_id}.additional-deck`);
                deck_div.classList.toggle('clicked');
                event.preventDefault();
            }
            else if (event.key === "4") {
                let deck_div = document.querySelector(`.deck.player-${Setting.player_id}.additional-discard-pile`);
                deck_div.classList.toggle('clicked');
                event.preventDefault();
            }
            else if (event.key == "+") {
                event.preventDefault();
                Replay.doReplay(true, 1, true);
            }
            else if (event.key === "Enter") {
                Button.doPost(true);
                event.preventDefault();
            }
            else if (event.key === "Escape") {
                if (HistoryLog.isOpen()) {
                    HistoryLog.toggle();
                }
                if (HoverCard.center_preview.has_image) {
                    Button.disablePause();
                }
                else if (Effect.isExEffect() && (SelectStep.isTargets() || SelectStep.isCost()) && Effect.select_effect_obj.selected_targets.length > 0) {
                    Effect.onCancel();
                }
                else if (SelectStep.isCard() ||
                    Effect.isExEffect() && (SelectStep.isTargets() || SelectStep.isCost()) && Effect.select_effect_obj.selected_targets.length == 0 ||
                    Effect.isExEffect() && SelectStep.isEffect() ||
                    Effect.is_in_event == 'response' ||
                    Effect.is_in_event == 'interrupt') {
                    Button.doRedo();
                }
                else {
                    Button.doCancel();
                }
                event.preventDefault();
            }
            else if (event.key === "Tab") {
                Button.doToggleHistory();
                event.preventDefault();
            }
            else if (event.key === " ") {
                Button.togglePause();
                event.preventDefault();
            }
            else if (event.key === "Alt") {
                event.preventDefault();
            }
            else if (event.key === 'Backspace') {
                event.preventDefault();
                Button.doToEnd();
            }
            else if (event.key === "q") {
                HoverCard.rotate(-1);
                event.preventDefault();
            }
            else if (event.key === "e" || event.key === "r") {
                HoverCard.rotate(+1);
                event.preventDefault();
            }
            else if (event.key === "f") {
                HoverCard.flip();
                event.preventDefault();
            }
        }
    }
    ;
}
WindowLoad.mouse_y = 0;
WindowLoad.mouse_x = 0;
(() => {
    window.oncontextmenu = function (event) {
        if (!event.shiftKey) {
            return false;
        }
    };
    window.onmousemove = (event) => {
        let x = event.clientX;
        let y = event.clientY;
        WindowLoad.mouse_x = x;
        WindowLoad.mouse_y = y;
        HoverCard.onMouseMove(x, y, 1, 1);
    };
    window.onmousedown = (event) => {
        if (event.button == 1 || event.buttons == 4) {
            HoverCard.rotate(+1);
            event.preventDefault();
        }
    };
    window.onblur = function (event) {
        UI.hold_ctrl = false;
        UI.hold_alt = false;
        UI.updateAnimeTime();
        document.body.classList.remove('hold-alt');
        document.querySelector("#skipping-icon").classList.add('hide');
    };
    window.onkeydown = function (event) {
        WindowLoad.onKeyDown(event);
    };
    window.onkeyup = function (event) {
        WindowLoad.onKeyUp(event);
    };
    window.onclick = function (event) {
        WindowLoad.onClick(event);
    };
})();
export class SwipeDetector {
    static handleTouchStart(event) {
        SwipeDetector.touchStartX = event.changedTouches[0].screenX;
    }
    static handleTouchEnd(event) {
        SwipeDetector.touchEndX = event.changedTouches[0].screenX;
        SwipeDetector.handleGesture();
    }
    static handleGesture() {
        if (SwipeDetector.touchEndX < SwipeDetector.touchStartX) {
            console.log('Swiped left');
            SwipeDetector.div.classList.add('clicked');
        }
        if (SwipeDetector.touchEndX > SwipeDetector.touchStartX) {
            console.log('Swiped right');
            SwipeDetector.div.classList.remove('clicked');
        }
    }
    static attachSwipeListeners() {
        const element = document.querySelector('body');
        element.addEventListener('touchstart', SwipeDetector.handleTouchStart, false);
        element.addEventListener('touchend', SwipeDetector.handleTouchEnd, false);
    }
}
SwipeDetector.touchStartX = 0;
SwipeDetector.touchEndX = 0;
SwipeDetector.div = document.getElementById('right-side-bar');
//# sourceMappingURL=window.js.map