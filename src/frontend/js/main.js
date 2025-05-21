document.addEventListener('DOMContentLoaded', function() {
    Chart.register(ChartZoom);
    
    const sectors = {
        'Energy': {
            indicators: [
                { name: 'Brent Crude Oil', query: 'getBrentCrudeOil' },
            ],
            color: '#3498db',
            charts: []
        },
    };

    const sectorsContainer = document.getElementById('sectors-container');

    for (const [sectorName, sectorData] of Object.entries(sectors)) {
        const sectorElement = document.createElement('div');
        sectorElement.className = 'sector';

        const sectorHeader = document.createElement('div');
        sectorHeader.className = 'sector-header';
        sectorHeader.textContent = sectorName;
        sectorHeader.style.backgroundColor = sectorData.color;
        
        const sectorContent = document.createElement('div');
        sectorContent.className = 'sector-content';

        sectorElement.appendChild(sectorHeader);
        sectorElement.appendChild(sectorContent);
        sectorsContainer.appendChild(sectorElement);

        sectorData.indicators.forEach(indicator => {
            createChartContainer(sectorContent, indicator);
        });

        sectorHeader.addEventListener('click', async function() {
            const isOpening = !sectorContent.classList.contains('active');
            sectorContent.classList.toggle('active');
            
            if (isOpening && sectorData.charts.length === 0) {
                await loadSectorData(sectorData);
            } else if (isOpening) {
                resetChartsToLastWeek(sectorData.charts);
            }
        });
    }

    function createChartContainer(container, indicator) {
        const chartContainer = document.createElement('div');
        chartContainer.className = 'chart-container';

        const chartTitle = document.createElement('h3');
        chartTitle.className = 'chart-title';
        chartTitle.textContent = indicator.name;

        const canvas = document.createElement('canvas');
        
        chartContainer.appendChild(chartTitle);
        chartContainer.appendChild(canvas);
        container.appendChild(chartContainer);

        indicator.canvas = canvas;
    }

    async function loadSectorData(sectorData) {
        const endDate = new Date();
        const startDate = new Date();
        startDate.setDate(endDate.getDate() - 30);

        const loadingPromises = sectorData.indicators.map(indicator => {
            return fetchIndicatorData(indicator.query, startDate, endDate)
                .then(data => {
                    const chart = createChart(indicator.canvas, indicator.name, data);
                    sectorData.charts.push(chart);
                    return chart;
                })
                .catch(error => {
                    console.error(`Error loading ${indicator.name} data:`, error);
                    indicator.canvas.parentElement.innerHTML += `<p>Error loading data for ${indicator.name}</p>`;
                    return null;
                });
        });

        await Promise.all(loadingPromises);
        resetChartsToLastWeek(sectorData.charts);
    }

    function resetChartsToLastWeek(charts) {
        const now = new Date();
        const weekAgo = new Date();
        weekAgo.setDate(now.getDate() - 7);
        
        charts.forEach(chart => {
            if (chart) {
                chart.options.scales.x.min = weekAgo;
                chart.options.scales.x.max = now;
                chart.update();
            }
        });
    }

    function fetchIndicatorData(indicatorName, startDate, endDate) {
        const formatDate = (date) => {
            return date.toISOString().replace('T', ' ').replace(/\.\d+Z/, '');
        };

        const query = `query { ${indicatorName} { timestamp value units } }`;
        const encodedQuery = encodeURIComponent(query);

        return fetch(`/query?query=${encodedQuery}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                return response.json();
            })
            .then(data => {
                if (!data || !data[indicatorName]) {
                    throw new Error('No data returned');
                }
                return data[indicatorName];
            });
    }

    function createChart(canvas, title, data) {
        data.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

        const timestamps = data.map(item => new Date(item.timestamp));
				const values = data.map(item => item.value);
        const units = data[0]?.units || '';
				let maxTimeStamp = Math.max( ...timestamps );
				maxTimeStamp += 24 * 3600 * 1000;

        const chart = new Chart(canvas, {
            type: 'line',
            data: {
                datasets: [{
                    data: values.map((value, index) => ({
                        x: timestamps[index],
                        y: value
                    })),
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            tooltipFormat: 'yyyy-MM-dd HH:mm',
                            displayFormats: {
                                day: 'MMM d'
                            }
                        },
                        title: {
                            display: true,
                        },
                        min: (new Date()).setUTCDate(timestamps[timestamps.length - 1].getDate() - 1),
                        max: new Date(maxTimeStamp)
                    },
                    y: {
                        title: {
                            display: true,
                            text: units
                        }
                    }
                },
                plugins: {
										legend: {
												display: false
										},

                    zoom: {
												limits: {
														x: {min: Math.min( ...timestamps ), max: maxTimeStamp },
														y: {min: Math.min( ...values ) * 0.9, max: Math.max( ...values ) * 1.1}
												},
                        pan: {
                            enabled: true,
                            mode: 'xy',
                            modifierKey: null,
                        },
                        zoom: {
                            wheel: {
                                enabled: true
                            },
                            pinch: {
                                enabled: true
                            },
                            mode: 'xy'
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ${context.parsed.y}`;
                            }
                        }
                    }
                }
            }
        });
    }
});
