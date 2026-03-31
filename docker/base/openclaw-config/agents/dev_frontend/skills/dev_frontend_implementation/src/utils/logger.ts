/**
 * Logger utility for structured logging
 */

export interface LogEntry {
  timestamp: string;
  level: "debug" | "info" | "warn" | "error";
  context: string;
  message: string;
  data?: Record<string, any>;
}

export class Logger {
  private context: string;

  constructor(context: string) {
    this.context = context;
  }

  debug(message: string, data?: Record<string, any>) {
    this.log("debug", message, data);
  }

  info(message: string, data?: Record<string, any>) {
    this.log("info", message, data);
  }

  warn(message: string, data?: Record<string, any>) {
    this.log("warn", message, data);
  }

  error(message: string, data?: Record<string, any>) {
    this.log("error", message, data);
  }

  private log(
    level: "debug" | "info" | "warn" | "error",
    message: string,
    data?: Record<string, any>
  ) {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      context: this.context,
      message,
      ...(data && { data }),
    };

    // Output based on environment
    const output = JSON.stringify(entry);
    if (level === "error") {
      console.error(output);
    } else if (level === "warn") {
      console.warn(output);
    } else {
      console.log(output);
    }
  }
}
