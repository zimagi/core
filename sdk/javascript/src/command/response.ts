/**
 * Command response handler for the Zimagi JavaScript SDK
 */

export class CommandResponse {
  aborted: boolean;
  messages: Array<any>;
  named: { [key: string]: any };
  errors: any[];

  constructor() {
    this.aborted = true;
    this.messages = [];
    this.named = {};
    this.errors = [];
  }

  add(messages: any | any[]): void {
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

  get error(): boolean {
    return this.aborted;
  }

  errorMessage(): string {
    return this.errors.map((message) => message.format()).join('\n\n');
  }

  getNamedData(name: string): any {
    const message = this.named[name];
    if (message) {
      try {
        return message.data;
      } catch (error) {
        return message.message;
      }
    }
    return null;
  }

  *[Symbol.iterator](): Iterator<any> {
    yield* this.messages;
  }

  get activeUser(): any {
    return this.getNamedData('active_user');
  }

  get logKey(): any {
    return this.getNamedData('log_key');
  }
}
