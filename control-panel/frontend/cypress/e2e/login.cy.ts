/**
 * E2E tests for the Login page (/login).
 *
 * Covers page rendering, successful login, credential errors,
 * network failures, form validation, and loading state.
 * All API calls are intercepted so tests run deterministically.
 */

const LOGIN_API = "/api/auth/login";

describe("Login page", () => {
  beforeEach(() => {
    cy.visit("/login");
  });

  // ─── Page rendering ──────────────────────────────────────────────────

  describe("page rendering", () => {
    it("displays brand title and subtitle", () => {
      cy.contains("ClawDevs AI").should("be.visible");
      cy.contains("Control Panel").should("be.visible");
    });

    it("renders username and password fields", () => {
      cy.get('[data-testid="login-username"]').should("be.visible");
      cy.get('[data-testid="login-password"]').should("be.visible");
    });

    it("renders the submit button with correct text", () => {
      cy.get('[data-testid="login-submit"]')
        .should("be.visible")
        .and("contain.text", "Entrar");
    });

    it("renders the login form", () => {
      cy.get('[data-testid="login-form"]').should("exist");
    });
  });

  // ─── Successful login ────────────────────────────────────────────────

  describe("successful login", () => {
    it("authenticates and redirects to home page", () => {
      cy.intercept("POST", LOGIN_API, {
        statusCode: 200,
        fixture: "login.json",
      }).as("loginRequest");

      cy.get('[data-testid="login-username"]').type("admin");
      cy.get('[data-testid="login-password"]').type("admin");
      cy.get('[data-testid="login-submit"]').click();

      cy.wait("@loginRequest").its("request.body").should("deep.equal", {
        username: "admin",
        password: "admin",
      });

      // After successful login, token is stored and user is redirected
      cy.location("pathname").should("eq", "/");
      cy.window().then((win) => {
        expect(win.localStorage.getItem("panel_token")).to.eq(
          "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e2e-test-fake-token"
        );
      });
    });
  });

  // ─── Failed login ────────────────────────────────────────────────────

  describe("failed login", () => {
    it("shows error message for wrong credentials", () => {
      cy.intercept("POST", LOGIN_API, {
        statusCode: 401,
        body: { detail: "Incorrect username or password" },
      }).as("loginFail");

      cy.get('[data-testid="login-username"]').type("wrong");
      cy.get('[data-testid="login-password"]').type("wrong");
      cy.get('[data-testid="login-submit"]').click();

      cy.wait("@loginFail");

      cy.get('[data-testid="login-error"]')
        .should("be.visible")
        .and("contain.text", "Usuário ou senha incorretos");

      // User stays on login page
      cy.location("pathname").should("eq", "/login");
    });

    it("clears error on new submission attempt", () => {
      // First: fail
      cy.intercept("POST", LOGIN_API, {
        statusCode: 401,
        body: { detail: "Unauthorized" },
      }).as("loginFail");

      cy.get('[data-testid="login-username"]').type("bad");
      cy.get('[data-testid="login-password"]').type("bad");
      cy.get('[data-testid="login-submit"]').click();
      cy.wait("@loginFail");
      cy.get('[data-testid="login-error"]').should("be.visible");

      // Second: succeed — error should clear
      cy.intercept("POST", LOGIN_API, {
        statusCode: 200,
        fixture: "login.json",
      }).as("loginOk");

      cy.get('[data-testid="login-username"]').clear().type("admin");
      cy.get('[data-testid="login-password"]').clear().type("admin");
      cy.get('[data-testid="login-submit"]').click();
      cy.wait("@loginOk");

      cy.get('[data-testid="login-error"]').should("not.exist");
    });
  });

  // ─── Network error ───────────────────────────────────────────────────

  describe("network error", () => {
    it("shows connection error when server is unreachable", () => {
      cy.intercept("POST", LOGIN_API, { forceNetworkError: true }).as(
        "networkError"
      );

      cy.get('[data-testid="login-username"]').type("admin");
      cy.get('[data-testid="login-password"]').type("admin");
      cy.get('[data-testid="login-submit"]').click();

      cy.wait("@networkError");

      cy.get('[data-testid="login-error"]')
        .should("be.visible")
        .and("contain.text", "Erro de conexão com o servidor");
    });
  });

  // ─── Loading state ───────────────────────────────────────────────────

  describe("loading state", () => {
    it("disables button and shows loading text during submission", () => {
      cy.intercept("POST", LOGIN_API, (req) => {
        req.reply({
          statusCode: 200,
          fixture: "login.json",
          delay: 1000,
        });
      }).as("slowLogin");

      cy.get('[data-testid="login-username"]').type("admin");
      cy.get('[data-testid="login-password"]').type("admin");
      cy.get('[data-testid="login-submit"]').click();

      // While loading: button disabled, text changes
      cy.get('[data-testid="login-submit"]')
        .should("be.disabled")
        .and("contain.text", "Entrando...");

      cy.wait("@slowLogin");
    });
  });

  // ─── Form validation ─────────────────────────────────────────────────

  describe("form validation", () => {
    it("does not submit when username is empty", () => {
      const spy = cy.spy().as("loginSpy");
      cy.intercept("POST", LOGIN_API, spy);

      cy.get('[data-testid="login-password"]').type("admin");
      cy.get('[data-testid="login-submit"]').click();

      // Native HTML validation prevents submission
      cy.get("@loginSpy").should("not.have.been.called");
    });

    it("does not submit when password is empty", () => {
      const spy = cy.spy().as("loginSpy");
      cy.intercept("POST", LOGIN_API, spy);

      cy.get('[data-testid="login-username"]').type("admin");
      cy.get('[data-testid="login-submit"]').click();

      cy.get("@loginSpy").should("not.have.been.called");
    });
  });
});
