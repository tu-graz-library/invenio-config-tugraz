// This file is part of invenio-config-tugraz.
// Copyright (C) 2026 Graz University of Technology.
//
// invenio-config-tugraz is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import React, { useState } from "react";
import ReactDOM from "react-dom";
import { http } from "react-invenio-forms";

import "./notices.less";

function Notices({ notices, ackLabel, onAcknowledge }) {
  return (
    <>
      {notices.map((notice) => (
        <div key={notice.key} className="notice">
          <button
            type="button"
            className="notice-close"
            aria-label={ackLabel}
            onClick={() => onAcknowledge(notice.key)}
          >
            &times;
          </button>
          {notice.title && <h2>{notice.title}</h2>}
          {notice.intro && <p>{notice.intro}</p>}
          <ul>
            {notice.items.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
          <button
            type="button"
            className="notice-dismiss"
            onClick={() => onAcknowledge(notice.key)}
          >
            {ackLabel}
          </button>
        </div>
      ))}
    </>
  );
}

function App({ initial, ackLabel }) {
  const [notices, setNotices] = useState(initial);
  const onAcknowledge = (key) => {
    setNotices((current) => current.filter((n) => n.key !== key));
    http.post(`/api/notices/${key}/acknowledge`);
  };
  return <Notices notices={notices} ackLabel={ackLabel} onAcknowledge={onAcknowledge} />;
}

const el = document.getElementById("notices");
if (el) {
  ReactDOM.render(
    <App initial={JSON.parse(el.dataset.notices || "[]")} ackLabel={el.dataset.ackLabel} />,
    el
  );
}
