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
    }
  }
}

Cypress.Commands.add("login", (_username = "admin", _password = "admin") => {
  cy.session([_username, _password], () => {
    window.localStorage.setItem("panel_token", "e2e-test-token-stub");
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

export {};
