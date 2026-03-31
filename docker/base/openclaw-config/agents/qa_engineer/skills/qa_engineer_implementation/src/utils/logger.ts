/**
 * Logging utility for qa_engineer
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
  private logs: LogEntry[] = [];

  constructor(context: string) {
    this.context = context;
  }

  debug(message: string, data?: Record<string, any>): void {
    this.log("debug", message, data);
  }

  info(message: string, data?: Record<string, any>): void {
    this.log("info", message, data);
  }

  warn(message: string, data?: Record<string, any>): void {
    this.log("warn", message, data);
  }

  error(message: string, data?: Record<string, any>): void {
    this.log("error", message, data);
  }

  private log(
    level: "debug" | "info" | "warn" | "error",
    message: string,
    data?: Record<string, any>
  ): void {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      context: this.context,
      message,
      data,
    };
    this.logs.push(entry);
  }

  getLogs(): LogEntry[] {
    return this.logs;
  }

  clearLogs(): void {
    this.logs = [];
  }
}
