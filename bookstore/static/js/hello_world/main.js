const timeElement = document.getElementById('current-time')

getCurrentTime(timeElement);

function getCurrentTime(timeElement) {
    const daysOfWeek = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'];
    const monthsOfYear = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];

    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = monthsOfYear[currentDate.getMonth()];
    const currentDay = String(currentDate.getDate()).padStart(2, '0');
    const currentDayOfWeek = daysOfWeek[currentDate.getDay()];
    console.log(currentDayOfWeek)
    timeElement.innerHTML = `<em>${currentDayOfWeek}, ${currentDay} de ${currentMonth} de ${currentYear}</em>`;
}
