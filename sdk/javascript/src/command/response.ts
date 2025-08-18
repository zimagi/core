/**
 * Command response handler for the Zimagi JavaScript SDK
 */

import { DataMessage } from '../messages';

export interface CommandMessage {
  type: string;
  name?: string | null;
  message: string;
  isError(): boolean;
  format(): string;
}

export class CommandResponse {
  aborted: boolean;
  messages: CommandMessage[];
  named: { [key: string]: CommandMessage };
  errors: CommandMessage[];

  constructor() {
    this.aborted = true;
    this.messages = [];
    this.named = {};
    this.errors = [];
  }

  add(messages: CommandMessage | CommandMessage[]): void {
    if (!Array.isArray(messages)) {
      messages = [messages];
    }

    for (const message of messages) {
      if (message.type === 'StatusMessage') {
        this.aborted = !message.message;
      } else {
        this.messages.push(message);
        if (message.name) {
          this.named[message.name] = message;
        }
        if (message.isError && message.isError()) {
          this.errors.push(message);
        }
      }
    }
  }

  error(): boolean {
    return this.aborted;
  }

  errorMessage(): string {
    return this.errors.map((message) => message.format()).join('\n\n');
  }

  getNamedData(name: string): any {
    const message = this.named[name] as DataMessage | null;
    if (message) {
      try {
        return message.data;
      } catch (error) {
        return message.message;
      }
    }
    return null;
  }

  *[Symbol.iterator](): Iterator<CommandMessage> {
    yield* this.messages;
  }

  get activeUser(): any {
    return this.getNamedData('active_user');
  }

  get logKey(): any {
    return this.getNamedData('log_key');
  }
}
