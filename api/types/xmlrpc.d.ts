declare module 'xmlrpc' {
  interface Client {
    methodCall(
      method: string,
      params: any[],
      callback: (err: Error | null, ...args: any[]) => void
    ): void;
  }

  interface Options {
    url: string;
    path: string;
    port?: number;
    headers?: Record<string, string>;
  }

  function createSecureClient(options: Options): Client;
  function createClient(options: Options): Client;
}
