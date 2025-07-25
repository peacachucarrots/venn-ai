import { useEffect, useRef } from "react";
import Chart from "chart.js/auto";

export default function RadarScores({ scores, size = 320 }) {
    const canvasRef = useRef(null);
    const chartRef = useRef(null);

    useEffect(() => {
        const labels = Object.keys(scores);
        const data = Object.values(scores);

        if (chartRef.current) chartRef.current.destroy();

        chartRef.current = new Chart(canvasRef.current, {
            type: "radar",
            data: {
                labels,
                datasets: [{ label: "Scores", data }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {legend: {display: false}},
                scales: {
                    r: {
                        min: 1,
                        max: 4,
                        ticks: {display: false},
                        angleLines: {color: "rgba(255,255,255,0.1)"},
                        grid: {color: "rgba(255,255,255,0.1)", circular: true},
                        pointLabels: {color: "#fff", font: {size: 12}}
                    }
                }
            },
        });

        return () => chartRef.current?.destroy();
    }, [scores]);

    return (
        <div className="radar-wrapper" style={{ width: size, height: size, margin: "0 auto" }}>
            <canvas ref={canvasRef} />
        </div>
    );
}