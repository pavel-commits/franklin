let buttons = document.querySelectorAll('button.standart');
let categories = document.querySelectorAll('.categories-open');

for(let i = 0; i < categories.length; i++) {
  buttons[i].onclick = function() {

    if (buttons[i].textContent == "Скрыть") {
        buttons[i].textContent="Категории";
        categories[i].classList.add("hidden");
    } else {
        buttons[i].textContent="Скрыть";
        categories[i].classList.remove("hidden");

    }
};
}