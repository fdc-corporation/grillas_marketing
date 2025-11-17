/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProjectTaskStateSelection } from "@project/components/project_task_state_selection/project_task_state_selection";
import { formatSelection } from "@web/views/fields/formatters";

patch(ProjectTaskStateSelection.prototype, {
    setup() {
        super.setup?.();

        console.log("✅ Patch aplicado a ProjectTaskStateSelection");

        // Agregamos visuales del estado en_revision
        this.icons["en_revision"] = "fa fa-eye";
        this.colorIcons["en_revision"] = "text-warning";
        this.colorButton["en_revision"] = "btn-outline-warning";
    },

    get options() {
        const baseOptions = super.options || [];
        const labels = new Map(baseOptions);

        const currentState = this.props.record?.data?.[this.props.name];

        const states = ["1_canceled", "1_done"];

        if (currentState !== "04_waiting_normal") {
            states.unshift(
                "01_in_progress",
                "02_changes_requested",
                "03_approved",
                "en_revision"
            );
        }

        const finalOptions = states.map((state) => {
            return [state, labels.get(state) || state]; // fallback al valor si no hay label
        });

        return finalOptions;
    },

    get label() {
        const baseOptions = super.options || [];

        // findLast puede devolver undefined
        const waitOption = baseOptions.findLast?.(([state]) => state === "04_waiting_normal");

        const allOptions = [...this.options];

        // Solo agregamos si existe y es válido
        if (Array.isArray(waitOption)) {
            allOptions.push(waitOption);
        }

        return formatSelection(this.currentValue, {
            selection: allOptions,
        });
    }
});
