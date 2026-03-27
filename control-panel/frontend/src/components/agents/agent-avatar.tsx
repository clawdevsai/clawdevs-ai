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

import { cn } from "@/lib/utils"

// Deterministic color from slug string
function slugColor(slug: string): string {
  const colors = [
    "#00FF9C", // primary green
    "#00C2FF", // cyan
    "#A78BFA", // purple
    "#F472B6", // pink
    "#FB923C", // orange
    "#34D399", // emerald
    "#60A5FA", // blue
    "#FBBF24", // amber
    "#F87171", // red
    "#4ADE80", // green
    "#38BDF8", // sky
    "#C084FC", // violet
    "#E879F9", // fuchsia
  ]
  let hash = 0
  for (let i = 0; i < slug.length; i++) {
    hash = (hash * 31 + slug.charCodeAt(i)) >>> 0
  }
  return colors[hash % colors.length]
}

function getInitials(name: string): string {
  return name
    .split(/[\s_-]+/)
    .map((part) => part[0])
    .join("")
    .toUpperCase()
    .slice(0, 2)
}

type AvatarSize = "sm" | "md" | "lg"

const sizeClasses: Record<AvatarSize, string> = {
  sm: "h-8 w-8 text-xs",
  md: "h-10 w-10 text-xs",
  lg: "h-16 w-16 text-lg",
}

interface AgentAvatarProps {
  slug: string
  displayName: string
  size?: AvatarSize
  className?: string
}

export function AgentAvatar({
  slug,
  displayName,
  size = "md",
  className,
}: AgentAvatarProps) {
  const color = slugColor(slug)
  const initials = getInitials(displayName || slug)

  return (
    <div
      className={cn(
        "rounded-full flex items-center justify-center shrink-0 font-bold border",
        sizeClasses[size],
        className
      )}
      style={{
        backgroundColor: `${color}1A`, // ~10% opacity
        borderColor: `${color}4D`,     // ~30% opacity
        color,
      }}
      aria-label={displayName}
    >
      {initials}
    </div>
  )
}
