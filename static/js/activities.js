document.addEventListener("DOMContentLoaded", function() {

    const yearElement = document.getElementById("currentYear");
    if (yearElement) yearElement.textContent = new Date().getFullYear();

    const form = document.getElementById("registerForm");
    const resultElement = document.getElementById("result");
    const clubSelect = document.getElementById("club");
    const nameInput = document.getElementById("name");
    const emailInput = document.getElementById("email");

    const setMsg = (input, emptyMsg, typeMsg) => {
        input.oninvalid = function(e) {
            e.target.setCustomValidity("");
            if (e.target.validity.valueMissing) {
                e.target.setCustomValidity(emptyMsg);
            } else if (typeMsg && e.target.validity.typeMismatch) {
                e.target.setCustomValidity(typeMsg);
            }
        };
        input.oninput = function(e) { e.target.setCustomValidity(""); };
    };

    if (nameInput) setMsg(nameInput, "Будь ласка, введіть ПІБ студента.");
    if (clubSelect) setMsg(clubSelect, "Будь ласка, оберіть гурток зі списку.");
    
    if (emailInput) {
        emailInput.oninvalid = function(e) {
            e.target.setCustomValidity("");
            if (e.target.validity.valueMissing) {
                e.target.setCustomValidity("Будь ласка, введіть вашу пошту.");
            } else if (e.target.validity.typeMismatch) {
                e.target.setCustomValidity("Адреса пошти має містити символ '@'.");
            }
        };
        emailInput.oninput = function(e) { e.target.setCustomValidity(""); };
    }

    window.selectClub = function(clubName) {
        if (clubSelect) {
            clubSelect.value = clubName;
            clubSelect.style.borderColor = "#4834d4";
            setTimeout(() => { clubSelect.style.borderColor = "#dfe6e9"; }, 600);
        }
    };

    if (form) {
        form.addEventListener("submit", function(e) {
            e.preventDefault();
            const name = nameInput.value;
            const club = clubSelect.value;

            resultElement.style.display = "block";
            resultElement.style.background = "#e1fadc";
            resultElement.style.color = "#27ae60";
            resultElement.style.border = "1px solid #2ecc71";
            resultElement.style.padding = "15px";
            resultElement.style.borderRadius = "10px";
            resultElement.style.marginTop = "20px";

            resultElement.innerHTML = `✅ <strong>${name}</strong>, ви успішно записані на гурток: <br>🚀 ${club}`;
            
            this.reset();
        });
    }
});