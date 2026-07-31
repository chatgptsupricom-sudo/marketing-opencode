import { NextRequest } from 'next/server';

export function validateApiKey(request: NextRequest): boolean {
  const apiKey = request.headers.get('X-API-Key');
  return apiKey === process.env.API_KEY;
}
