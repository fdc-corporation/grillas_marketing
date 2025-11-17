/** @odoo-module **/

import { registry } from "@web/core/registry";

const field = registry.category("fields").get("project_task_state_selection");

if (field?.component) {
  const ProjectTaskStateSelection = field.component;

  console.log("✅ Patch aplicado a ProjectTaskStateSelection");

  // Sobrescribimos el getter `options`
  Object.defineProperty(ProjectTaskStateSelection.prototype, "options", {
    get: function () {
      const selection =
        this.props?.field?.selection || this.props?.selection || [];

      if (!Array.isArray(selection) || !selection.length) {
        console.warn("⚠️ selection no es un array o está vacío", selection);
        return [];
      }

      console.log("🟢 Opciones de selección recibidas:", selection);

      const labels = new Map(selection);
      const currentState = this.props.record.data[this.props.name];

      const states = ["1_canceled", "1_done"];
      if (currentState !== "04_waiting_normal") {
        states.unshift(
          "01_in_progress",
          "02_changes_requested",
          "03_approved",
          "en_revision"
        );
      }

      return states
        .filter((state) => labels.has(state))
        .map((state) => [state, labels.get(state)]);
    },
  });
} else {
  console.warn(
    "❌ Componente project_task_state_selection no encontrado en el registry"
  );
}
