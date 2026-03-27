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

const PUBLIC_API_URL = process.env.NEXT_PUBLIC_API_URL;

function normalizeWsUrl(url: string): string {
  if (url.startsWith("https://")) return url.replace("https://", "wss://");
  if (url.startsWith("http://")) return url.replace("http://", "ws://");
  return url;
}

export function getApiBaseUrl(): string {
  // Prefer explicit public API URL when provided for external deployments.
  if (PUBLIC_API_URL) return PUBLIC_API_URL;

  // In browser, route through same-origin Next.js rewrite (/api/*).
  if (typeof window !== "undefined") return "/api";

  // Server-side fallback for local development.
  return process.env.API_INTERNAL_URL ?? "http://localhost:8000";
}

export function getWsBaseUrl(): string {
  if (PUBLIC_API_URL) return normalizeWsUrl(PUBLIC_API_URL);

  // In browser, route WS via same-origin Next.js rewrite (/api/ws/*).
  if (typeof window !== "undefined") {
    return `${window.location.origin.replace(/^http/, "ws")}/api`;
  }

  return "ws://localhost:8000";
}
