
document.addEventListener("DOMContentLoaded", () => {
  const timeline = document.getElementById("timeline");
  const actorFilter = document.getElementById("actorFilter");

  fetch("data/consolidated_master.json")
    .then(res => res.json())
    .then(data => {
      const items = [
        ...(data.contradictions || []),
        ...(data.evidence_vex || []),
        ...(data.timelines || []),
        ...(data.contradictions_vex || [])
      ];

      function render(filteredItems) {
        timeline.innerHTML = "";
        filteredItems.forEach(item => {
          const div = document.createElement("div");
          div.className = "entry";
          div.innerHTML = `
            <strong>${item.title || item.summary || "Untitled"}</strong><br>
            <span>${item.tags?.join(", ") || "No tags"}</span><br>
            <pre>${JSON.stringify(item, null, 2)}</pre>
          `;
          timeline.appendChild(div);
        });
      }

      actorFilter.addEventListener("change", () => {
        const val = actorFilter.value;
        if (val === "") {
          render(items);
        } else {
          render(items.filter(i => (i.tags || []).includes(val)));
        }
      });

      render(items);
    });
});
