/* 
 * Copyright (c) 2026 Diego Silva Morais <lukewaresoftwarehouse@gmail.com>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

import { NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const SESSION_KEY_RE = /^agent:([a-z0-9_-]+):(.+)$/i;

type ChatStreamBody = {
  agent_slug?: string;
  session_key?: string;
  message?: string;
  rag_context?: string | null;
};

function normalizeAgentSlug(rawValue: string): string {
  return rawValue.trim().toLowerCase();
}

function parseSessionKey(sessionKey: string): { agentSlug: string; normalized: string } | null {
  const normalized = sessionKey.trim();
  const match = SESSION_KEY_RE.exec(normalized);
  if (!match) return null;
  return {
    agentSlug: normalizeAgentSlug(match[1]),
    normalized,
  };
}

function resolveAgentAndSessionKey(body: ChatStreamBody): { agentSlug: string; sessionKey: string } {
  const rawSessionKey = (body.session_key ?? "").trim();
  const rawAgentSlug = (body.agent_slug ?? "").trim();

  if (rawSessionKey) {
    const parsed = parseSessionKey(rawSessionKey);
    if (!parsed) {
      throw new Response(
        JSON.stringify({ detail: "session_key must match 'agent:<slug>:<rest>'" }),
        { status: 422, headers: { "Content-Type": "application/json" } }
      );
    }
    if (rawAgentSlug && normalizeAgentSlug(rawAgentSlug) !== parsed.agentSlug) {
      throw new Response(
        JSON.stringify({ detail: "agent_slug does not match session_key agent" }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      );
    }
    return { agentSlug: parsed.agentSlug, sessionKey: parsed.normalized };
  }

  if (!rawAgentSlug) {
    throw new Response(
      JSON.stringify({ detail: "agent_slug is required when session_key is not provided" }),
      { status: 422, headers: { "Content-Type": "application/json" } }
    );
  }

  const agentSlug = normalizeAgentSlug(rawAgentSlug);
  return {
    agentSlug,
    sessionKey: `agent:${agentSlug}:main`,
  };
}

function normalizeRagContext(rawContext?: string | null): string | null {
  if (!rawContext) return null;
  const normalized = rawContext.trim();
  if (!normalized) return null;
  // Keep prompt injection surface bounded.
  return normalized.slice(0, 3500);
}

function resolveGatewayToken(): string {
  return (
    process.env.OPENCLAW_GATEWAY_TOKEN?.trim() ||
    process.env.PANEL_OPENCLAW_GATEWAY_TOKEN?.trim() ||
    ""
  );
}

function resolveGatewayCandidates(): string[] {
  const configured = process.env.OPENCLAW_GATEWAY_URL?.trim();
  const panelConfigured = process.env.PANEL_OPENCLAW_GATEWAY_URL?.trim();
  const defaults = [
    "http://localhost:18789",
    "http://clawdevs-ai:18789",
  ];
  const all = [configured, panelConfigured, ...defaults]
    .filter(Boolean)
    .map((value) => (value as string).replace(/\/+$/, ""));
  return Array.from(new Set(all));
}

async function streamFromGateway(
  gatewayUrl: string,
  gatewayToken: string,
  sessionKey: string,
  payload: unknown
): Promise<Response | null> {
  try {
    const upstreamResponse = await fetch(`${gatewayUrl}/v1/chat/completions`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${gatewayToken}`,
        "Content-Type": "application/json",
        "x-openclaw-session-key": sessionKey,
      },
      body: JSON.stringify(payload),
    });

    if (!upstreamResponse.ok || !upstreamResponse.body) {
      return null;
    }

    return new Response(upstreamResponse.body, {
      status: 200,
      headers: {
        "Content-Type": "text/event-stream; charset=utf-8",
        "Cache-Control": "no-cache, no-transform",
        Connection: "keep-alive",
        "X-Accel-Buffering": "no",
      },
    });
  } catch {
    return null;
  }
}

export async function POST(request: Request) {
  try {
    const authorization = request.headers.get("authorization");
    if (!authorization?.startsWith("Bearer ")) {
      return NextResponse.json({ detail: "Missing authorization token" }, { status: 401 });
    }

    const body = (await request.json()) as ChatStreamBody;
    const message = (body.message ?? "").trim();
    if (!message) {
      return NextResponse.json({ detail: "message is required" }, { status: 422 });
    }

    const { agentSlug, sessionKey } = resolveAgentAndSessionKey(body);
    const ragContext = normalizeRagContext(body.rag_context);

    const gatewayToken = resolveGatewayToken();
    if (!gatewayToken) {
      return NextResponse.json(
        { detail: "OPENCLAW_GATEWAY_TOKEN is not configured" },
        { status: 500 }
      );
    }

    const upstreamPayload = {
      model: `openclaw/${agentSlug}`,
      stream: true,
      messages: [
        ...(ragContext
          ? [
              {
                role: "system",
                content:
                  "Relevant prior context retrieved from RAG. Use when helpful and ignore if not applicable:\n\n" +
                  ragContext,
              },
            ]
          : []),
        { role: "user", content: message },
      ],
    };

    const gatewayCandidates = resolveGatewayCandidates();
    for (const candidate of gatewayCandidates) {
      const streamResponse = await streamFromGateway(
        candidate,
        gatewayToken,
        sessionKey,
        upstreamPayload
      );
      if (streamResponse) {
        return streamResponse;
      }
    }

    return NextResponse.json(
      { detail: "Failed to connect to OpenClaw gateway" },
      { status: 502 }
    );
  } catch (error) {
    if (error instanceof Response) {
      return error;
    }
    return NextResponse.json(
      { detail: error instanceof Error ? error.message : "Unexpected stream proxy error" },
      { status: 500 }
    );
  }
}
