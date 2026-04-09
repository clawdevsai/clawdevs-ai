const STUB_PANEL_TOKEN =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjQxMDA4MDAwMDB9.e2e-smoke-signature";

declare global {
  namespace Cypress {
    interface Chainable {
      /**
       * Stub-authenticate by setting a fake token in localStorage.
       * No real backend call is made — works entirely offline.
       */
      login(username?: string, password?: string): Chainable<void>;

      /**
       * Authenticate via the real backend API.
       * Stores the JWT in localStorage under "panel_token".
       * Use this when tests need a real session (e.g. login flow E2E).
       */
      loginByApi(username?: string, password?: string): Chainable<void>;

      /**
       * Set a deterministic panel token in localStorage.
       * Useful when tests need a known auth state without API login.
       */
      setPanelToken(token?: string): Chainable<void>;

      /**
       * Clear panel session token from localStorage.
       */
      clearPanelSession(): Chainable<void>;
    }
  }
}

Cypress.Commands.add("login", (_username = "admin", _password = "admin") => {
  cy.session([_username, _password], () => {
    window.localStorage.setItem("panel_token", STUB_PANEL_TOKEN);
  });
});

Cypress.Commands.add(
  "loginByApi",
  (username = "admin", password = "admin") => {
    cy.session([username, password, "api"], () => {
      cy.request("POST", "/api/auth/login", { username, password }).then(
        (res) => {
          window.localStorage.setItem("panel_token", res.body.access_token);
        }
      );
    });
  }
);

Cypress.Commands.add("setPanelToken", (token = STUB_PANEL_TOKEN) => {
  cy.window({ log: false }).then((win) => {
    win.localStorage.setItem("panel_token", token);
  });
});

Cypress.Commands.add("clearPanelSession", () => {
  cy.window({ log: false }).then((win) => {
    win.localStorage.removeItem("panel_token");
  });
});

export {};
