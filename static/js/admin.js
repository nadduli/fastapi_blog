document.addEventListener("DOMContentLoaded", () => {
    // Basic config for chart styling
    Chart.defaults.color = "#a0a5cc";
    Chart.defaults.font.family = "'Inter', sans-serif";
    Chart.defaults.plugins.tooltip.backgroundColor = "rgba(15, 17, 26, 0.9)";
    Chart.defaults.plugins.tooltip.titleColor = "#ffffff";
    Chart.defaults.plugins.tooltip.bodyColor = "#a0a5cc";
    Chart.defaults.plugins.tooltip.borderColor = "rgba(255, 255, 255, 0.1)";
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.padding = 12;
    Chart.defaults.plugins.tooltip.displayColors = false;

    // Load data from script tag
    const dataSrc = document.getElementById("dashboard-data");
    let chartLabels = [];
    let chartData = [];

    if (dataSrc) {
        try {
            const data = JSON.parse(dataSrc.textContent);
            chartLabels = data.labels || [];
            chartData = data.data || [];
        } catch (e) {
            console.error("Failed to parse chart data", e);
        }
    }

    // Main Sales Trend Chart
    const ctxMain = document.getElementById("salesChart");
    if (ctxMain) {
        // Create gradient for the line chart fill
        const gradient = ctxMain.getContext('2d').createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(99, 102, 241, 0.5)'); // primary var
        gradient.addColorStop(1, 'rgba(99, 102, 241, 0.0)');

        new Chart(ctxMain, {
            type: 'line',
            data: {
                labels: chartLabels.length ? chartLabels : ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Revenue (UGX)',
                    data: chartData.length ? chartData : [0, 0, 0, 0, 0, 0, 0],
                    borderColor: '#6366f1', // accent-primary
                    backgroundColor: gradient,
                    borderWidth: 3,
                    pointBackgroundColor: '#0f111a',
                    pointBorderColor: '#6366f1',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    fill: true,
                    tension: 0.4 // Smooth curves
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== null) {
                                    label += new Intl.NumberFormat('en-US').format(context.parsed.y);
                                }
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false,
                            drawBorder: false
                        },
                        ticks: {
                            padding: 10
                        }
                    },
                    y: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)',
                            drawBorder: false // Hide the axis line itself
                        },
                        ticks: {
                            padding: 10,
                            callback: function (value) {
                                if (value >= 1000000) {
                                    return (value / 1000000).toFixed(1) + 'M';
                                } else if (value >= 1000) {
                                    return (value / 1000).toFixed(0) + 'k';
                                }
                                return value;
                            }
                        },
                        beginAtZero: true
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index',
                },
            }
        });
    }

    // Popular Plans Doughnut Chart (Mock)
    const ctxSide = document.getElementById("plansChart");
    if (ctxSide) {
        new Chart(ctxSide, {
            type: 'doughnut',
            data: {
                labels: ['24 Hours', '1 Hour', '7 Days', '30 Days'],
                datasets: [{
                    data: [55, 25, 15, 5],
                    backgroundColor: [
                        '#6366f1', // primary
                        '#10b981', // success
                        '#f59e0b', // warning
                        '#ef4444'  // danger
                    ],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    }
                }
            }
        });
    }

    // Sidebar Active Item Logic
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function (e) {
            if (this.querySelector('.logout')) return;

            navItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
        });
    });
});
