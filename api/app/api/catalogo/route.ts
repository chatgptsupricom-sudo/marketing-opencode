import { NextRequest, NextResponse } from 'next/server';
import { fetchCatalogo } from '@/lib/odoo';
import { validateApiKey } from '@/lib/auth';

let cache: { data: any; ts: number } | null = null;
const TTL = 24 * 60 * 60 * 1000; // 24 horas

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'X-API-Key',
};

export async function OPTIONS() {
  return new NextResponse(null, { status: 204, headers: CORS_HEADERS });
}

export async function GET(request: NextRequest) {
  if (!validateApiKey(request)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401, headers: CORS_HEADERS });
  }

  try {
    // Cache hit
    if (cache && Date.now() - cache.ts < TTL) {
      return NextResponse.json({
        productos: cache.data,
        actualizado: new Date(cache.ts).toISOString(),
      }, { headers: CORS_HEADERS });
    }

    // Fetch from Odoo
    const productos = await fetchCatalogo();
    cache = { data: productos, ts: Date.now() };

    return NextResponse.json({
      productos,
      actualizado: new Date().toISOString(),
    }, { headers: CORS_HEADERS });
  } catch (error) {
    console.error('Error fetching catalog:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500, headers: CORS_HEADERS }
    );
  }
}
