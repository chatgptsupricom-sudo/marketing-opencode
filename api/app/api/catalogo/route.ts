import { NextRequest, NextResponse } from 'next/server';
import { fetchCatalogo } from '@/lib/odoo';
import { validateApiKey } from '@/lib/auth';

// Cache CORTO (30 segundos): suficiente para que multiples pestañas/usuarios
// compartan la misma consulta a Odoo sin saturarlo (429 Too Many Requests).
// El HTML refresca cada 30s asi que siempre recibe datos frescos.

let cache: { data: any; ts: number } | null = null;
const TTL = 30 * 1000; // 30 segundos (antes era 24 horas)

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'X-API-Key, Content-Type',
  'Access-Control-Max-Age': '86400',
};

export async function OPTIONS() {
  return new NextResponse(null, { status: 204, headers: CORS_HEADERS });
}

export async function GET(request: NextRequest) {
  if (!validateApiKey(request)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401, headers: CORS_HEADERS });
  }

  try {
    // Cache hit: si tiene menos de 30s, sirve sin tocar Odoo
    if (cache && Date.now() - cache.ts < TTL) {
      return NextResponse.json({
        productos: cache.data,
        actualizado: new Date(cache.ts).toISOString(),
        cached: true,
      }, { headers: CORS_HEADERS });
    }

    // Fetch fresco desde Odoo
    const productos = await fetchCatalogo();
    cache = { data: productos, ts: Date.now() };

    return NextResponse.json({
      productos,
      actualizado: new Date().toISOString(),
      cached: false,
    }, {
      headers: {
        ...CORS_HEADERS,
        'Cache-Control': 'no-store, no-cache, must-revalidate',
        'Pragma': 'no-cache',
      },
    });
  } catch (error: any) {
    console.error('Error fetching catalog:', error?.message || error);

    // Si hay cache viejo, servirlo con aviso en vez de fallar
    if (cache) {
      return NextResponse.json({
        productos: cache.data,
        actualizado: new Date(cache.ts).toISOString(),
        cached: true,
        stale: true,
      }, { headers: CORS_HEADERS });
    }

    return NextResponse.json(
      {
        error: 'Internal server error',
        message: error?.message || 'Unknown error',
      },
      { status: 500, headers: CORS_HEADERS }
    );
  }
}
