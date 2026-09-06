import { Setting } from "./settings.js";
import { Command } from "./command.js";
export class ErrorDialog {
    static async init() {
        ErrorDialog.error_occurred_div = ErrorDialog.createErrorOccurredDiv();
        ErrorDialog.error_occurred_body_div = ErrorDialog.error_occurred_div.querySelector('.error-occurred-body');
        ErrorDialog.error_occurred_body_tip = ErrorDialog.error_occurred_div.querySelector('.error-occurred-tip');
        document.body.appendChild(ErrorDialog.error_occurred_div);
    }
    static createErrorOccurredDiv() {
        const errorDiv = document.createElement('div');
        errorDiv.id = 'error-occurred';
        errorDiv.classList.add('hide');
        const tipDiv = document.createElement('div');
        tipDiv.className = 'error-occurred-tip';
        errorDiv.appendChild(tipDiv);
        const bodyDiv = document.createElement('div');
        bodyDiv.className = 'error-occurred-body';
        errorDiv.appendChild(bodyDiv);
        const footerDiv = document.createElement('div');
        footerDiv.className = 'error-occurred-footer';
        const messageDiv = document.createElement('div');
        messageDiv.style.flex = 'auto';
        footerDiv.appendChild(messageDiv);
        const ignoreButton = document.createElement('button');
        ignoreButton.type = 'button';
        ignoreButton.id = 'error-ignore';
        ignoreButton.textContent = 'Ignore';
        ignoreButton.onclick = () => ErrorDialog.hideError();
        footerDiv.appendChild(ignoreButton);
        const reportButton = document.createElement('button');
        reportButton.type = 'button';
        reportButton.id = 'error-report';
        reportButton.textContent = 'Report';
        reportButton.onclick = () => ErrorDialog.reportError();
        footerDiv.appendChild(reportButton);
        errorDiv.appendChild(footerDiv);
        return errorDiv;
    }
    static showError(text) {
        if (Setting.hide_bug_report) {
            return;
        }
        if (text.endsWith("UndoRequest\n")) {
            ErrorDialog.error_occurred_body_tip.innerHTML = `In most cases, this is NOT a real crash.
• Please undo and try another way.

Please check these before reporting a bug:
• Check if you selected the correct target.
• Check if you met the cost of this effect.
• Check if any forced effects haven't resolved.`;
        }
        else {
            ErrorDialog.error_occurred_body_tip.innerHTML = "";
        }
        ErrorDialog.last_error_text = text;
        ErrorDialog.error_occurred_div.classList.remove('hide');
        ErrorDialog.error_occurred_body_div.innerHTML = text;
    }
    static hideError() {
        ErrorDialog.error_occurred_div.classList.add('hide');
    }
    static reportError() {
        ErrorDialog.hideError();
        Command.uploadSave("Crash", ErrorDialog.error_occurred_body_div.innerText);
    }
}
ErrorDialog.last_error_text = "";
//# sourceMappingURL=error_dialog.js.map