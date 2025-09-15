async function load_conclusions() {
    try {
        let response = await fetch('http://127.0.0.1:8000/api/conclusion/all', {
            method: 'GET',
            credentials: 'include'
        });

        if (!response.ok) {
            data = await response.json();
            showToast(`${data.detail}`);
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        let conclusionsData = await response.json();
        let count = conclusionsData.count
        let conclusions = conclusionsData.conclusions

        let foundCount = document.getElementById('foundCount')
        let textSearch = document.getElementById('textSearch')
        let word = document.getElementById('word')
        
        foundCount.textContent = count
        textSearch.textContent = "Всего: "
        word.textContent = declension(count)

        const conclusionsList = document.getElementById("applicationsList");
        conclusionsList.innerHTML = "";

        if (count == 0) {
            const emptyBlock = document.createElement("div");
            emptyBlock.className = "empty-block";
            emptyBlock.textContent = "Список заявлений пуст.";
            conclusionsList.appendChild(emptyBlock);
        } else {
            conclusions.forEach(conclusion => {
                const card = document.createElement("div");
                card.className = "app-card";
                
                let formatted = new Date(conclusion.create_date).toLocaleDateString("ru-RU").replace(/\./g, "-");
                
                card.innerHTML = `
                    <div class="application" style="display: flex; gap: 15px; padding: 10px; border-radius: 8px;">
                        <span>${conclusion.conclusion_id}</span>
                        <span><b>ФИО:</b> ${conclusion.fio}</span>
                        <span><b>Адрес:</b> ${conclusion.address}</span>
                        <span><b>Телефон:</b> ${conclusion.phone}</span>
                        <span><b>Дата создания:</b> ${formatted}</span>
                    </div>
                    ${conclusion.signed ? "": `<button class="sign-btn" id="${conclusion.id}">Подписать</button>`}
                `;

                conclusionsList.appendChild(card);
            });
        }

    } catch (error) {
        showToast(`Ошибка загрузки заявок: ${error}`);
        console.error("Ошибка загрузки заявок:", error);
    }
}

async function load_street() {
    try {
        let response = await fetch('http://127.0.0.1:8000/api/applications/street', {
            method: 'GET',
            credentials: 'include'
        });

        if (!response.ok) {
            data = await response.json();
            showToast(`${data.detail}`);
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        let streetData = await response.json();
        let streets = streetData.streets

        const districtList = document.getElementById("districtList");
        districtList.innerHTML = "";

        
        streets.forEach(street => {
            const streetCard = document.createElement("label");
            streetCard.dataset.district = street.street;

            // создаём чекбокс
            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.name = "district";
            checkbox.value = street.street;

            // добавляем чекбокс и текст
            streetCard.appendChild(checkbox);
            streetCard.appendChild(document.createTextNode(" " + street.street));

            districtList.appendChild(streetCard);
        });
        

    } catch (error) {
        showToast(`Ошибка загрузки заявок: ${error}`);
        console.error("Ошибка загрузки заявок:", error);
    }
}

function declension(num) {
  num = Math.abs(num) % 100;
  const n1 = num % 10;
  if (num > 10 && num < 20) return "заявлений";
  if (n1 > 1 && n1 < 5) return "заявления";
  if (n1 === 1) return "заявление";
  return "заявлений";
}

async function search_conclusions() {
    try {
        let searchInput = document.getElementById("searchInput")
        text = searchInput.value
        let response = await fetch(`http://127.0.0.1:8000/api/conclusion/search/${text}`, {
            method: 'GET',
            credentials: 'include'
        });

        if (!response.ok) {
            data = await response.json();
            showToast(`${data.detail}`);
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        let conclusionsData = await response.json();
        let count = conclusionsData.count
        let conclusions = conclusionsData.conclusions

        let foundCount = document.getElementById('foundCount')
        let textSearch = document.getElementById('textSearch')
        let word = document.getElementById('word')
        
        foundCount.textContent = count
        textSearch.textContent = "Найдено: "
        word.textContent = declension(count)

        const conclusionsList = document.getElementById("applicationsList");
        conclusionsList.innerHTML = "";

        if (count == 0) {
            const emptyBlock = document.createElement("div");
            emptyBlock.className = "empty-block";
            emptyBlock.textContent = "Ничего не найдено по вашему запросу.";
            conclusionsList.appendChild(emptyBlock);
        } else {
            conclusions.forEach(conclusion => {
                const card = document.createElement("div");
                card.className = "app-card";

                let formatted = new Date(conclusion.create_date).toLocaleDateString("ru-RU").replace(/\./g, "-");
                
                card.innerHTML = `
                    <div class="application" style="display: flex; gap: 15px; padding: 10px; border-radius: 8px;">
                        <span>${conclusion.conclusion_id}</span>
                        <span><b>ФИО:</b> ${conclusion.fio}</span>
                        <span><b>Адрес:</b> ${conclusion.address}</span>
                        <span><b>Телефон:</b> ${conclusion.phone}</span>
                        <span><b>Дата создания:</b> ${formatted}</span>
                    </div>
                    ${conclusion.signed ? "": `<button class="sign-btn" id="${conclusion.id}">Подписать</button>`}
                `;

                conclusionsList.appendChild(card);
            });
        }

    } catch (error) {
        showToast(`Ошибка загрузки заявок: ${error}`);
        console.error("Ошибка загрузки заявок:", error);
    }
}


async function apply_filters() {
    try {
        // Собираем выбранные районы
        const street = [...document.querySelectorAll("input[name='district']:checked")]
            .map(cb => cb.value);

        // Даты
        const dateFrom = document.getElementById("dateFrom").value;
        const dateTo = document.getElementById("dateTo").value;

        const signed = document.getElementById("signedVisit").checked;

        // Формируем query параметры
        const params = new URLSearchParams();
        if (street.length > 0) params.append("street", street.join(","));
        if (dateFrom) params.append("date_from", dateFrom);
        if (dateTo) params.append("date_to", dateTo);
        if (signed) params.append("signed", "true");

        // Отправляем запрос
        let response = await fetch(`http://127.0.0.1:8000/api/conclusion/filter?${params.toString()}`, {
            method: 'GET',
            credentials: 'include'
        });

        if (!response.ok) {
            const data = await response.json();
            showToast(`${data.detail}`);
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        let conclusionsData = await response.json();
        let count = conclusionsData.count;
        let conclusions = conclusionsData.conclusions;

        let foundCount = document.getElementById('foundCount');
        let textSearch = document.getElementById('textSearch');
        let word = document.getElementById('word');
        
        foundCount.textContent = count;
        textSearch.textContent = "Найдено: ";
        word.textContent = declension(count);

        const conclusionsList = document.getElementById("applicationsList");
        conclusionsList.innerHTML = "";

        if (count === 0) {
            const emptyBlock = document.createElement("div");
            emptyBlock.className = "empty-block";
            emptyBlock.textContent = "Ничего не найдено по выбранным фильтрам.";
            conclusionsList.appendChild(emptyBlock);
        } else {
            conclusions.forEach(conclusion => {
                const card = document.createElement("div");
                card.className = "app-card";
                card.dataset.district = conclusion.district;

                let formatted = new Date(conclusion.create_date).toLocaleDateString("ru-RU").replace(/\./g, "-");
                
                card.innerHTML = `
                    <div class="application" style="display: flex; gap: 15px; padding: 10px; border-radius: 8px;">
                        <span>${conclusion.conclusion_id}</span>
                        <span><b>ФИО:</b> ${conclusion.fio}</span>
                        <span><b>Адрес:</b> ${conclusion.address}</span>
                        <span><b>Телефон:</b> ${conclusion.phone}</span>
                        <span><b>Дата создания:</b> ${formatted}</span>
                    </div>
                    ${conclusion.signed ? "": `<button class="sign-btn" id="${conclusion.id}">Подписать</button>`}
                `;

                conclusionsList.appendChild(card);
            });
        }

    } catch (error) {
        showToast(`Ошибка загрузки фильтров: ${error}`);
        console.error("Ошибка загрузки фильтров:", error);
    }
}


document.addEventListener("DOMContentLoaded", () => {
    // Загрузка заявлений
    load_conclusions();
    // Загрузка регионов
    load_street();

    // Поиск
    const searchBtn = document.getElementById("searchBtn");
    searchBtn.addEventListener("click", async () => {
        await search_conclusions();
    });

    // Применение фильтров
    const applyFilters = document.getElementById("applyFilters");
    applyFilters.addEventListener("click", async () => {
        await apply_filters();
    });


    const dateFrom = document.getElementById("dateFrom");
    const dateTo = document.getElementById("dateTo");

    const clearFiltersBtn = document.getElementById("clearFilters");
    
    const filterVisit = document.getElementById("signedVisit");

    // --- Сброс фильтров ---
    clearFiltersBtn.addEventListener("click", () => {
        // Сбрасываем чекбоксы
        document.querySelectorAll("input[name='district']").forEach(ch => ch.checked = false);

        // Сбрасываем даты
        dateFrom.value = "";
        dateTo.value = "";

        filterVisit.checked = false

        // Возвращаем текст кнопки выбора районов
        districtBtn.textContent = "Выберите районы ▾";

        load_conclusions();
    });

    const assignBtn = document.getElementById("assignBtn");

    assignBtn.addEventListener("click", () => {
        window.location.href = "/conclusion_create/conclusion_create.html";
    });
});
