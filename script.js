document.addEventListener("DOMContentLoaded", () => {
  fetch("sample_vitals.json")
    .then((res) => res.json())
    .then((data) => {
      const container = document.getElementById("vitals");

      const vitals = [
        { label: "Patient ID", value: data.patient_id },
        { label: "Temperature (°C)", value: data.temperature },
        { label: "Heart Rate (BPM)", value: data.heart_rate },
        { label: "SpO₂ (%)", value: data.spo2 },
        { label: "Blood Pressure", value: data.bp },
        { label: "Respiratory Rate", value: data.respiratory_rate },
      ];

      vitals.forEach((item) => {
        const row = document.createElement("div");
        row.className = "vital";

        row.innerHTML = `
          <span class="vital-label">${item.label}</span>
          <span class="vital-value">${item.value}</span>
        `;

        container.appendChild(row);
      });
    })
    .catch((err) => {
      console.error("Error loading vitals:", err);
    });
});
