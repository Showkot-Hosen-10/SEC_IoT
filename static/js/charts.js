function createCharts(data) {
    const ids = data.map(x => x.id);
    const ultrasonic = data.map(x => x.ultrasonic);
    const temperature = data.map(x => x.temperature);
    const humidity = data.map(x => x.humidity);
    const mq135 = data.map(x => x.mq135);
    const current = data.map(x => x.current_mA);

    const isDark = !document.body.classList.contains("light-mode");

    function modeColors(darkColor, lightColor) { return isDark ? darkColor : lightColor; }
    const chartBg = isDark ? "#111" : "#e6f0ff";
    const tickColor = isDark ? "#0ff" : "#1b1b3a";
    const gridColor = isDark ? "rgba(255,255,255,0.1)" : "rgba(0,0,0,0.1)";

    const commonOptions = {
        responsive: true,
        plugins: {
            legend: { labels: { color: tickColor } }
        },
        scales: {
            x: { ticks: { color: tickColor }, grid: { color: gridColor } },
            y: { ticks: { color: tickColor }, grid: { color: gridColor } }
        }
    };

    function drawChart(canvasId, label, borderColor, bgColor, dataArray) {
        const ctx = document.getElementById(canvasId).getContext("2d");
        ctx.canvas.style.backgroundColor = chartBg;
        new Chart(ctx, {
            type: "line",
            data: {
                labels: ids,
                datasets: [{
                    label: label,
                    data: dataArray,
                    borderColor: borderColor,
                    backgroundColor: bgColor,
                    fill: true,
                    tension: 0.3
                }]
            },
            options: commonOptions
        });
    }

    drawChart("ultrasonic_chart", "Ultrasonic", modeColors("#1f77b4","#1b1b8f"), modeColors("rgba(31,119,180,0.2)","rgba(27,27,143,0.2)"), ultrasonic);
    drawChart("temperature_chart", "Temperature", modeColors("#ff7f0e","#8b3e00"), modeColors("rgba(255,127,14,0.2)","rgba(139,62,0,0.2)"), temperature);
    drawChart("humidity_chart", "Humidity", modeColors("#2ca02c","#006400"), modeColors("rgba(44,160,44,0.2)","rgba(0,100,0,0.2)"), humidity);
    drawChart("mq135_chart", "MQ135", modeColors("#d62728","#800000"), modeColors("rgba(214,39,40,0.2)","rgba(128,0,0,0.2)"), mq135);
    drawChart("current_chart", "Current", modeColors("#9467bd","#4b0082"), modeColors("rgba(148,103,189,0.2)","rgba(75,0,130,0.2)"), current);
}

document.addEventListener("DOMContentLoaded", () => { createCharts(data); });
document.getElementById("mode-toggle").addEventListener("click", () => {
    document.querySelectorAll("canvas").forEach(c=>c.remove());
    const container = document.querySelector(".charts-container");
    ["ultrasonic","temperature","humidity","mq135","current"].forEach(id => {
        const canvas = document.createElement("canvas");
        canvas.id = id+"_chart";
        container.appendChild(canvas);
    });
    createCharts(data);
});
