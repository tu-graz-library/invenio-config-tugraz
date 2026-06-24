// Copyright (C) 2024-2026 Graz University of Technology.
//
// invenio-config-tugraz is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

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
  });
}
