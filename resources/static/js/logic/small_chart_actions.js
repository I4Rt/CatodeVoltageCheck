/**
         * Подготавливает данные для ступенчатого графика
         * @param {number[]} intervals - Массив временных интервалов
         * @param {number[]} values - Массив значений
         * @returns {object} Объект с массивами stepX и stepY
         */
function prepareStepData(intervals, values) {
    const stepX = [];
    const stepY = [];
    
    // == only for sorded list ==
    stepX.push(new Date(intervals[0] * 1000 - 2*60*60*1000)); // Преобразуем временную метку в объект Date
    stepY.push(values[0]);
    // == only for sorded list ==


    for (let i = 0; i < values.length; i++) {
        stepX.push(new Date(intervals[i] * 1000)); // Преобразуем временную метку в объект Date
        stepY.push(values[i]);
    }
    

    return { stepX, stepY };
}

function configureChart(elementId, intervals, values) {
    const { stepX, stepY } = prepareStepData(intervals, values);

    const data = [{
        x: stepX,
        y: stepY,
        type: 'scatter',
        mode: 'lines',
        line: { shape: 'hv', color: 'white', width: 2 },
    }];

    const layout = {
        margin: { l: 0, r: 0, t: 0, b: 0 },
        xaxis: {
            visible: false,
            range: [new Date(Date.now() - 2 * 60 * 60 * 1000), new Date()]
        },
        yaxis: { visible: false, range: [-5, 95] },
        paper_bgcolor: 'rgb(71,71,71)',
        plot_bgcolor: 'rgb(71,71,71)',
    };

    const config = {
        responsive: true,
        displayModeBar: false,
    };

    // Используем Plotly.react вместо Plotly.newPlot
    Plotly.react(`#vault_change_canvas_${elementId}`, data, layout, config);
}

function updateChart(elementId, intervals, values) {
    const { stepX, stepY } = prepareStepData(intervals, values);

    // Добавляем последнее значение в данные
    const currentTime = Math.floor(Date.now() / 1000);
    stepX.push(new Date(currentTime * 1000));
    stepY.push(values[values.length - 1]);

    const updatedLayout = {
        xaxis: {
            visible: false,
            range: [new Date(Date.now() - 2 * 60 * 60 * 1000), new Date()] // Обновляем диапазон для последних 24 часов
        }
    };

    // Используем Plotly.update для обновления графика
    Plotly.update(`#vault_change_canvas_${elementId}`, { x: [stepX], y: [stepY] }, updatedLayout);
}

