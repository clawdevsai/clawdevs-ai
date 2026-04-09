/**
 * E2E tests for the Login page (/login).
 *
 * Covers page rendering, successful login, credential errors,
 * network failures, form validation, and loading state.
 * All API calls are intercepted so tests run deterministically.
 */

const LOGIN_API = "/api/auth/login";
const SESSION_TOKEN_KEY = "panel_token";

type LoginFixture = {
  access_token: string;
  token_type: string;
};

function fillCredentials(username = "admin", password = "admin") {
  cy.get('[data-testid="login-username"]').clear().type(username);
  cy.get('[data-testid="login-password"]').clear().type(password);
}

function submitLogin() {
  cy.get('[data-testid="login-submit"]').click();
}

function stubDashboardApis(options: {
  expectedAuthToken?: string;
  authFailureStatus?: 401 | 403;
} = {}) {
  const { expectedAuthToken, authFailureStatus } = options;

  cy.intercept("GET", "/api/agents*", (req) => {
    if (expectedAuthToken) {
      expect(req.headers.authorization).to.eq(`Bearer ${expectedAuthToken}`);
    }

    if (authFailureStatus) {
      req.reply({
        statusCode: authFailureStatus,
        body: { detail: "Unauthorized" },
      });
      return;
    }

    req.reply({
      statusCode: 200,
      body: { items: [], total: 0 },
    });
  }).as("getAgents");

  cy.intercept("GET", "/api/approvals*", {
    statusCode: 200,
    body: { items: [], total: 0 },
  });

  cy.intercept("GET", "/api/sessions*", {
    statusCode: 200,
    body: { items: [], total: 0 },
  });

  cy.intercept("GET", "/api/tasks*", {
    statusCode: 200,
    body: { items: [], total: 0 },
  });

  cy.intercept("GET", "/api/activity-events*", {
    statusCode: 200,
    body: { items: [], total: 0 },
  });

  cy.intercept("GET", "/api/api/health/summary*", {
    statusCode: 200,
    body: { healthy: 0, stalled: 0, failed: 0, blocked: 0 },
  });

  cy.intercept("GET", "/api/metrics/overview*", {
    statusCode: 200,
    body: {
      active_agents: 0,
      pending_approvals: 0,
      open_tasks: 0,
      tokens_24h: 0,
      tokens_consumed_total: 0,
      tokens_consumed_avg_per_task: 0,
      backlog_count: 0,
      tasks_in_progress: 0,
      tasks_completed: 0,
    },
  });

  cy.intercept("GET", "/api/metrics/cycle-time*", {
    statusCode: 200,
    body: {
      cycle_time_avg_seconds: 0,
      cycle_time_p95_seconds: 0,
      window_minutes: 30,
    },
  });

  cy.intercept("GET", "/api/metrics/throughput*", {
    statusCode: 200,
    body: {
      window_minutes: 30,
      group_by: "label",
      items: [],
    },
  });

  cy.intercept("GET", /\/api\/metrics(\?.*)?$/, {
    statusCode: 200,
    body: { items: [], total: 0 },
  });
}

describe("Login page", () => {
  beforeEach(() => {
    cy.visit("/login");
    cy.clearPanelSession();
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
    it("stores panel_token, redirects, and sends bearer token after login", () => {
      cy.fixture<LoginFixture>("login.json").then(({ access_token }) => {
        stubDashboardApis({ expectedAuthToken: access_token });

        cy.intercept("POST", LOGIN_API, {
          statusCode: 200,
          fixture: "login.json",
        }).as("loginRequest");

        fillCredentials("admin", "admin");
        submitLogin();

        cy.wait("@loginRequest").its("request.body").should("deep.equal", {
          username: "admin",
          password: "admin",
        });

        cy.location("pathname", { timeout: 10000 }).should("eq", "/");
        cy.window().then((win) => {
          expect(win.localStorage.getItem(SESSION_TOKEN_KEY)).to.eq(access_token);
        });

        // Asserts request interceptor behavior (Authorization: Bearer <token>)
        cy.wait("@getAgents");
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
      cy.window()
        .its("localStorage")
        .invoke("getItem", SESSION_TOKEN_KEY)
        .should("be.null");
    });

    it("clears error on new submission attempt", () => {
      cy.fixture<LoginFixture>("login.json").then(({ access_token }) => {
        stubDashboardApis({ expectedAuthToken: access_token });

        // First: fail
        cy.intercept("POST", LOGIN_API, {
          statusCode: 401,
          body: { detail: "Unauthorized" },
        }).as("loginFail");

        fillCredentials("bad", "bad");
        submitLogin();
        cy.wait("@loginFail");
        cy.get('[data-testid="login-error"]').should("be.visible");

        // Second: succeed — error should clear
        cy.intercept("POST", LOGIN_API, {
          statusCode: 200,
          fixture: "login.json",
        }).as("loginOk");

        fillCredentials("admin", "admin");
        submitLogin();
        cy.wait("@loginOk");

        cy.get('[data-testid="login-error"]').should("not.exist");
        cy.location("pathname", { timeout: 10000 }).should("eq", "/");
        cy.window()
          .its("localStorage")
          .invoke("getItem", SESSION_TOKEN_KEY)
          .should("eq", access_token);
      });
    });
  });

  // ─── Network error ───────────────────────────────────────────────────

  describe("network error", () => {
    it("shows connection error when server is unreachable", () => {
      cy.intercept("POST", LOGIN_API, { forceNetworkError: true }).as(
        "networkError"
      );

      fillCredentials("admin", "admin");
      submitLogin();

      cy.wait("@networkError");

      cy.get('[data-testid="login-error"]')
        .should("be.visible")
        .and("contain.text", "Erro de conexão com o servidor");
      cy.location("pathname").should("eq", "/login");
      cy.window()
        .its("localStorage")
        .invoke("getItem", SESSION_TOKEN_KEY)
        .should("be.null");
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

      fillCredentials("admin", "admin");
      submitLogin();

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

  // ─── Session cleanup contract ────────────────────────────────────────

  describe("session cleanup contract", () => {
    ([401, 403] as const).forEach((statusCode) => {
      it(`clears panel_token and redirects when protected API returns ${statusCode}`, () => {
        cy.fixture<LoginFixture>("login.json").then(({ access_token }) => {
          cy.setPanelToken(access_token);
          stubDashboardApis({
            expectedAuthToken: access_token,
            authFailureStatus: statusCode,
          });

          cy.visit("/");
          cy.wait("@getAgents");
          cy.location("pathname", { timeout: 10000 }).should("eq", "/login");
          cy.window()
            .its("localStorage")
            .invoke("getItem", SESSION_TOKEN_KEY)
            .should("be.null");
        });
      });
    });
  });
});
