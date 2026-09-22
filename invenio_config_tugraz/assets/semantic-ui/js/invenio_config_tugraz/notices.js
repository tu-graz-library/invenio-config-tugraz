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

const STORAGE_KEY = "tug-notices-acknowledged";

function acknowledgedLocally() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch (e) {
    return [];
  }
}

function rememberLocally(key) {
  try {
    const keys = acknowledgedLocally();
    if (!keys.includes(key)) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify([...keys, key]));
    }
  } catch (e) {
    // storage disabled
  }
}

function Notices({ notices, ackLabel, onAcknowledge }) {
  return (
    <>
      {notices.map((notice) => (
        <div
          key={notice.key}
          className={notice.accent ? "notice notice--accent" : "notice"}
        >
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
          {notice.outro && <p className="notice-outro">{notice.outro}</p>}
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

function App({ initial, ackLabel, authenticated }) {
  const seen = authenticated ? [] : acknowledgedLocally();
  const [notices, setNotices] = useState(initial.filter((n) => !seen.includes(n.key)));

  const onAcknowledge = (key) => {
    setNotices((current) => current.filter((n) => n.key !== key));
    if (authenticated) {
      http.post(`/api/notices/${key}/acknowledge`);
    } else {
      rememberLocally(key);
    }
  };

  return <Notices notices={notices} ackLabel={ackLabel} onAcknowledge={onAcknowledge} />;
}

const el = document.getElementById("notices");
if (el) {
  ReactDOM.render(
    <App
      initial={JSON.parse(el.dataset.notices || "[]")}
      ackLabel={el.dataset.ackLabel}
      authenticated={el.dataset.authenticated === "true"}
    />,
    el
  );
}
