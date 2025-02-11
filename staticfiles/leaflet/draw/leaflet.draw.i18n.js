const withFormsElement = document.getElementById("with-forms");
if (withFormsElement) {
    const withForms = JSON.parse(withFormsElement.textContent);
    if (withForms) {
        // Define a function to safely get text content
        function safeTextContent(id) {
            const element = document.getElementById(id);
            return element ? JSON.parse(element.textContent) : null;
        }

        // Setting Leaflet draw localization with safety checks
        L.drawLocal.draw.toolbar.actions.title = safeTextContent("draw-toolbar-actions-title");
        L.drawLocal.draw.toolbar.actions.text = safeTextContent("draw-toolbar-actions-text");
        L.drawLocal.draw.toolbar.undo.title = safeTextContent("draw-toolbar-undo-title");
        L.drawLocal.draw.toolbar.undo.text = safeTextContent("draw-toolbar-undo-text");
        L.drawLocal.draw.toolbar.buttons.polyline = safeTextContent("draw-toolbar-buttons-polyline");
        L.drawLocal.draw.toolbar.buttons.polygon = safeTextContent("draw-toolbar-buttons-polygon");
        L.drawLocal.draw.toolbar.buttons.rectangle = safeTextContent("draw-toolbar-buttons-rectangle");
        L.drawLocal.draw.toolbar.buttons.circle = safeTextContent("draw-toolbar-buttons-circle");
        L.drawLocal.draw.toolbar.buttons.marker = safeTextContent("draw-toolbar-buttons-marker");
        L.drawLocal.draw.handlers.circle.tooltip.start = safeTextContent("draw-handlers-circle-tooltip-start");
        L.drawLocal.draw.handlers.marker.tooltip.start = safeTextContent("draw-handlers-marker-tooltip-start");
        L.drawLocal.draw.handlers.polygon.tooltip.start = safeTextContent("draw-handlers-polygon-tooltip-start");
        L.drawLocal.draw.handlers.polygon.tooltip.cont = safeTextContent("draw-handlers-polygon-tooltip-cont");
        L.drawLocal.draw.handlers.polygon.tooltip.end = safeTextContent("draw-handlers-polygon-tooltip-end");
        L.drawLocal.draw.handlers.polyline.error = safeTextContent("draw-handlers-polyline-error");
        L.drawLocal.draw.handlers.polyline.tooltip.start = safeTextContent("draw-handlers-polyline-tooltip-start");
        L.drawLocal.draw.handlers.polyline.tooltip.cont = safeTextContent("draw-handlers-polyline-tooltip-cont");
        L.drawLocal.draw.handlers.polyline.tooltip.end = safeTextContent("draw-handlers-polyline-tooltip-end");
        L.drawLocal.draw.handlers.rectangle.tooltip.start = safeTextContent("draw-handlers-rectangle-tooltip-start");
        L.drawLocal.draw.handlers.simpleshape.tooltip.end = safeTextContent("draw-handlers-simpleshape-tooltip-end");

        L.drawLocal.edit.toolbar.actions.save.title = safeTextContent("edit-toolbar-actions-save-title");
        L.drawLocal.edit.toolbar.actions.save.text = safeTextContent("edit-toolbar-actions-save-text");
        L.drawLocal.edit.toolbar.actions.cancel.title = safeTextContent("edit-toolbar-actions-cancel-title");
        L.drawLocal.edit.toolbar.actions.cancel.text = safeTextContent("edit-toolbar-actions-cancel-text");
        L.drawLocal.edit.toolbar.buttons.edit = safeTextContent("edit-toolbar-buttons-edit");
        L.drawLocal.edit.toolbar.buttons.editDisabled = safeTextContent("edit-toolbar-buttons-editDisabled");
        L.drawLocal.edit.toolbar.buttons.remove = safeTextContent("edit-toolbar-buttons-remove");
        L.drawLocal.edit.toolbar.buttons.removeDisabled = safeTextContent("edit-toolbar-buttons-removeDisabled");
        L.drawLocal.edit.handlers.edit.tooltip.text = safeTextContent("edit-handlers-edit-tooltip-text");
        L.drawLocal.edit.handlers.edit.tooltip.subtext = safeTextContent("edit-handlers-edit-tooltip-subtext");
        L.drawLocal.edit.handlers.remove.tooltip.text = safeTextContent("edit-handlers-remove-tooltip-text");
    }
}
