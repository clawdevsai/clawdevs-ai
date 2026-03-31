/**
 * LogEntry - Represents a single log entry with timestamp and context
 */
export interface LogEntry {
  level: 'debug' | 'info' | 'warn' | 'error';
  timestamp: Date;
  message: string;
  data?: Record<string, any>;
}

/**
 * Logger - Structured logging service for tracking execution flow
 */
class Logger {
  private logs: LogEntry[] = [];

  /**
   * Log a message at a specific level
   */
  public log(level: 'debug' | 'info' | 'warn' | 'error', message: string, data?: Record<string, any>): void {
    const entry: LogEntry = {
      level,
      timestamp: new Date(),
      message,
      data,
    };

    this.logs.push(entry);

    const prefix = `[${entry.timestamp.toISOString()}] [${level.toUpperCase()}]`;
    if (data) {
      console.log(`${prefix} ${message}`, data);
    } else {
      console.log(`${prefix} ${message}`);
    }
  }

  /**
   * Log a debug-level message
   */
  public debug(message: string, data?: Record<string, any>): void {
    this.log('debug', message, data);
  }

  /**
   * Log an info-level message
   */
  public info(message: string, data?: Record<string, any>): void {
    this.log('info', message, data);
  }

  /**
   * Log a warning-level message
   */
  public warn(message: string, data?: Record<string, any>): void {
    this.log('warn', message, data);
  }

  /**
   * Log an error-level message
   */
  public error(message: string, data?: Record<string, any>): void {
    this.log('error', message, data);
  }

  /**
   * Retrieve all accumulated log entries
   */
  public getLogs(): LogEntry[] {
    return [...this.logs];
  }

  /**
   * Clear all accumulated log entries
   */
  public clear(): void {
    this.logs = [];
  }

  /**
   * Get logs filtered by level
   */
  public getLogsByLevel(level: 'debug' | 'info' | 'warn' | 'error'): LogEntry[] {
    return this.logs.filter((entry) => entry.level === level);
  }

  /**
   * Get the total count of all logged entries
   */
  public getCount(): number {
    return this.logs.length;
  }
}

export const logger = new Logger();
export default Logger;
