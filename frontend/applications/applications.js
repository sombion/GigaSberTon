document.addEventListener("DOMContentLoaded", function () {
  const districtBtn = document.getElementById("districtBtn");
  const districtList = document.getElementById("districtList");

  districtList.addEventListener("change", function () {
    const checked = [...districtList.querySelectorAll("input[type=checkbox]:checked")];
    if (checked.length === 0) {
      districtBtn.textContent = "Выберите районы ▾";
    } else if (checked.length <= 3) {
    const names = checked.map(cb => cb.value).join(", ");
      districtBtn.textContent = names + " ▾";
    } else {
        districtBtn.textContent = `Выбрано ${checked.length} районов`;
    }
  });
});