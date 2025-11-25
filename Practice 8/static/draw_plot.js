document.addEventListener('DOMContentLoaded', () => {
    const dataEl = document.getElementById('chart-data');
    const historicalData = JSON.parse(dataEl.dataset.historical);

    const allDatesISO = Array.from(
        new Set(
            Object.values(historicalData).flatMap(series => series.map(([date]) => {
                const [d, m, y] = date.split('.');
                return `${y}-${m}-${d}`;
            }))
        )
    ).sort();

    allDatesISO.map(iso => {
        const [y, m, d] = iso.split('-');
        return `${d}.${m}.${y}`;
    });

    const traces = [];
    const COLORS = [
        '#cb3455', '#36A2EB', '#FFCE56', '#83d32f', '#9966FF', '#FF9F40'
    ];

    let idx = 0;
    for (const [code, series] of Object.entries(historicalData)) {
        const dataMap = new Map(series);
        const y = allDatesISO.map(iso => {
            const [y, m, d] = iso.split('-');
            const displayDate = `${d}.${m}.${y}`;
            return dataMap.get(displayDate) || null;
        });

        traces.push({
            x: allDatesISO,
            y: y,
            type: 'scatter',
            mode: 'lines+markers',
            name: code,
            line: {color: COLORS[idx % COLORS.length], width: 2},
            marker: {size: 4},
            hovertemplate:
                `<b>%{fullData.name}</b><br>` +
                `Курс: %{y:.4f} RUB<extra></extra>`
        });
        idx++;
    }

    const layout = {
        title: {
            text: 'Изменение курса за последние 3 месяца',
            font: {size: 18}
        },
        xaxis: {
            title: 'Дата',
            type: 'date',
            tickformat: '%d.%m.%Y',
            nticks: 10
        },
        yaxis: {
            title: 'Курс (в рублях)',
            autorange: true,
            rangemode: 'normal',
            tickformat: '.4f',
            fixedrange: false
        },
        legend: {x: 0, y: 1.1, orientation: 'h'},
        margin: {t: 80, b: 60, l: 80, r: 60},
        hovermode: 'x unified'
    };

    Plotly.newPlot('currencyPlot', traces, layout, {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['select2d', 'lasso2d']
    });
});