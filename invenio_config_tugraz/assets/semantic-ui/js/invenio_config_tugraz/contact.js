// SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
// SPDX-License-Identifier: MIT

import $ from "jquery";

// called on document ready
$(function () {
  importZammadScript();
});

function importZammadScript() {
  let scriptNode = document.createElement("hidden"); //needed for zammad script
  scriptNode.id = "zammad_form_script";
  scriptNode.src = "https://ub-support.tugraz.at/assets/form/form.js";
  document.head.appendChild(scriptNode);

  $.getScript("https://ub-support.tugraz.at/assets/form/form.js", () => {
    $("#feedback-form").ZammadForm({
      messageTitle: "Contact us",
      showTitle: true,
      messageSubmit: "Submit",
      messageThankYou:
        "Thank you for your message, (#%s). We will get back to you as quickly as possible!",
      modal: true,
    });

    // The button sits inside the Semantic UI "Need help?" modal (#contact-modal);
    // hide it when opening the Zammad form so its dimmer does not grey the form.
    $("#feedback-form").on("click", () => {
      $("#contact-modal").modal("hide");
    });
  });
}
