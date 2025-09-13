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
                // card.dataset.district = conclusions.district;

                card.innerHTML = `
                    <span>${conclusion.fio} | ${conclusion.cadastral_number} | ${conclusion.phone}</span>
                    <button class="sign-btn" id="${conclusion.id}">Подписать</button>
                `;

                conclusionsList.appendChild(card);
            });
        }

    } catch (error) {
        showToast(`Ошибка загрузки заявок: ${error}`);
        console.error("Ошибка загрузки заявок:", error);
    }
}

async function load_region() {
    try {
        let response = await fetch('http://127.0.0.1:8000/api/applications/region', {
            method: 'GET',
            credentials: 'include'
        });

        if (!response.ok) {
            data = await response.json();
            showToast(`${data.detail}`);
            throw new Error(`Ошибка запроса: ${response.status}`);
        }

        let regionData = await response.json();
        let regions = regionData.regions

        const districtList = document.getElementById("districtList");
        districtList.innerHTML = "";

        
        regions.forEach(region => {
            const regionCard = document.createElement("label");
            regionCard.dataset.district = region.region;

            // создаём чекбокс
            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.name = "district";
            checkbox.value = region.region;

            // добавляем чекбокс и текст
            regionCard.appendChild(checkbox);
            regionCard.appendChild(document.createTextNode(" " + region.region));

            districtList.appendChild(regionCard);
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
                card.dataset.district = application.district;

                card.innerHTML = `
                    <span>${conclusion.fio} | ${conclusion.cadastral_number} | ${conclusion.phone}</span>
                    <button class="sign-btn" id="${conclusion.id}">Подписать</button>
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
        const region = [...document.querySelectorAll("input[name='district']:checked")]
            .map(cb => cb.value);

        // Даты
        const dateFrom = document.getElementById("dateFrom").value;
        const dateTo = document.getElementById("dateTo").value;

        // Формируем query параметры
        const params = new URLSearchParams();
        if (region.length > 0) params.append("region", region.join(","));
        if (dateFrom) params.append("date_from", dateFrom);
        if (dateTo) params.append("date_to", dateTo);

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
        let applications = conclusionsData.conclusion;

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
            applications.forEach(application => {
                const card = document.createElement("div");
                card.className = "app-card";
                card.dataset.district = application.district;

                card.innerHTML = `
                    <span>${conclusion.fio} | ${conclusion.cadastral_number} | ${conclusion.phone}</span>
                    <button class="sign-btn" id="${conclusion.id}">Подписать</button>
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
    load_region();

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
    
    const filterVisit = document.getElementById("filterVisit");

    // --- Сброс фильтров ---
    clearFiltersBtn.addEventListener("click", () => {
        // Сбрасываем чекбоксы
        document.querySelectorAll("input[name='district']").forEach(ch => ch.checked = false);

        // Сбрасываем даты
        dateFrom.value = "";
        dateTo.value = "";

        // Возвращаем текст кнопки выбора районов
        districtBtn.textContent = "Выберите районы ▾";

        load_conclusions();
    });
});
