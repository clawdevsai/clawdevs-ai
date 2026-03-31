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

type ChatStreamBody = {
  agent_slug?: string;
  message?: string;
  rag_context?: string | null;
};

function normalizeAgentSlug(rawValue: string): string {
  return rawValue.trim().toLowerCase();
}

function resolveAgent(body: ChatStreamBody): string {
  const rawAgentSlug = (body.agent_slug ?? "").trim();
  if (!rawAgentSlug) {
    throw new Response(
      JSON.stringify({ detail: "agent_slug is required" }),
      { status: 422, headers: { "Content-Type": "application/json" } }
    );
  }
  return normalizeAgentSlug(rawAgentSlug);
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
    process.env.NEMOCLAW_GATEWAY_TOKEN?.trim() ||
    process.env.PANEL_NEMOCLAW_GATEWAY_TOKEN?.trim() ||
    ""
  );
}

function resolveGatewayCandidates(): string[] {
  const nemoclConfigured = process.env.NEMOCLAW_GATEWAY_URL?.trim();
  const panelNemoclConfigured = process.env.PANEL_NEMOCLAW_GATEWAY_URL?.trim();
  const defaults = [
    "http://nemoclaw:18789",
    "http://host.docker.internal:18789",
    "http://localhost:18789",
    "http://127.0.0.1:18789",
    "http://clawdevs-ai:18789",
  ];
  const all = [nemoclConfigured, panelNemoclConfigured, ...defaults]
    .filter(Boolean)
    .map((value) => (value as string).replace(/\/+$/, ""));
  return Array.from(new Set(all));
}

type GatewayStreamResult =
  | {
      kind: "success";
      response: Response;
    }
  | {
      kind: "upstream_error";
      status: number;
      detail: string;
    }
  | {
      kind: "network_error";
    };

async function streamFromGateway(
  gatewayUrl: string,
  gatewayToken: string,
  payload: unknown
): Promise<GatewayStreamResult> {
  try {
    const upstreamResponse = await fetch(`${gatewayUrl}/v1/chat/completions`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${gatewayToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!upstreamResponse.ok) {
      const rawBody = await upstreamResponse.text();
      let detail = rawBody.trim() || `Gateway returned HTTP ${upstreamResponse.status}`;
      try {
        const parsed = JSON.parse(rawBody) as { detail?: string; message?: string };
        detail = (parsed.detail ?? parsed.message ?? detail).trim();
      } catch {
        // Keep plain text fallback.
      }
      return {
        kind: "upstream_error",
        status: upstreamResponse.status,
        detail,
      };
    }

    if (!upstreamResponse.body) {
      return {
        kind: "upstream_error",
        status: 502,
        detail: "OpenClaw gateway returned an empty stream body",
      };
    }

    return {
      kind: "success",
      response: new Response(upstreamResponse.body, {
        status: 200,
        headers: {
          "Content-Type": "text/event-stream; charset=utf-8",
          "Cache-Control": "no-cache, no-transform",
          Connection: "keep-alive",
          "X-Accel-Buffering": "no",
        },
      }),
    };
  } catch {
    return { kind: "network_error" };
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

    const agentSlug = resolveAgent(body);
    const ragContext = normalizeRagContext(body.rag_context);

    const gatewayToken = resolveGatewayToken();
    if (!gatewayToken) {
      return NextResponse.json(
        { detail: "NEMOCLAW_GATEWAY_TOKEN is not configured" },
        { status: 500 }
      );
    }

    const modelPrefix = process.env.NEMOCLAW_MODEL_PREFIX?.trim() || "nemoclaw";
    const upstreamPayload = {
      model: `${modelPrefix}/${agentSlug}`,
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
    let upstreamError: { status: number; detail: string } | null = null;
    for (const candidate of gatewayCandidates) {
      const streamResult = await streamFromGateway(
        candidate,
        gatewayToken,
        upstreamPayload
      );

      if (streamResult.kind === "success") {
        return streamResult.response;
      }

      if (streamResult.kind === "upstream_error" && !upstreamError) {
        upstreamError = {
          status: streamResult.status,
          detail: streamResult.detail,
        };
      }
    }

    if (upstreamError) {
      return NextResponse.json(
        { detail: upstreamError.detail },
        { status: upstreamError.status }
      );
    }

    return NextResponse.json(
      { detail: "Failed to connect to NemoClaw runtime" },
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
