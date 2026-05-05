// Copyright (C) 2024-2026 Graz University of Technology.
//
// invenio-config-tugraz is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import $ from "jquery";

async function generateForm() {
  // get email from `/api/me`
  let email = "???";
  const response = await fetch("/api/me");
  if (response.ok) {
    const json = await response.json();
    email = json?.email || "???";
  }

  // show form
  $.getScript("https://ub-support.tugraz.at/assets/form/form.js", () => {
    $("#anchor-unlock-form").ZammadForm({
      attributes: [
        {},
        { defaultValue: email },
        {
          defaultValue: `Could you unlock my account (${email}) for research-uploads?`,
        },
      ],
      modal: false,
    });

    document.getElementById("zammad-form-name-inline").focus();
  });
}

$(function () {
  const generateFormElement = document.getElementById("generate-unlock-form");
  if (generateFormElement) {
    generateFormElement.onclick = generateForm;
  }
});
